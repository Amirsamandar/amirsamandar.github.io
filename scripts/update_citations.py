#!/usr/bin/env python3
"""Collect every paper that cites my publications and write _data/citations.json.

Sources (each is optional; a source that fails or has no credentials is
skipped, and the last good data for it is kept):

  INSPIRE-HEP       no key needed
  Semantic Scholar  no key needed (S2_API_KEY raises the rate limit)
  OpenAlex          no key needed (OPENALEX_API_KEY / OPENALEX_MAILTO optional)
  NASA ADS          needs ADS_TOKEN  (ui.adsabs.harvard.edu -> Settings -> API Token)
  Google Scholar    per-paper counts scraped from the public profile when
                    Scholar allows it; the list of citing papers needs
                    SERPAPI_KEY (Scholar blocks most automated requests)

The publications are read from _publications/*.md (arxiv, doi, title).
Citing papers found by several databases are merged into one entry using
arXiv id, DOI and normalised title. Manual corrections live in
_data/citations_overrides.yml (drop false matches, add missing papers, pin
database ids for a publication).

Usage:
    python scripts/update_citations.py                 # update the data file
    python scripts/update_citations.py --dry-run       # print a summary only
    python scripts/update_citations.py --only inspire,openalex
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
PUB_DIR = ROOT / "_publications"
OUT = ROOT / "_data" / "citations.json"
OVERRIDES = ROOT / "_data" / "citations_overrides.yml"
PROFILE = ROOT / "_data" / "profile.yml"

ME = ("samandar", "a")  # (surname, first initial) used to flag own citations

SOURCES = {
    "inspire": "INSPIRE-HEP",
    "ads": "NASA ADS",
    "s2": "Semantic Scholar",
    "openalex": "OpenAlex",
    "scholar": "Google Scholar",
}
# Metadata from the first source in this order wins when records are merged.
PRIORITY = ["inspire", "ads", "s2", "openalex", "scholar"]

BROWSER_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def log(msg: str) -> None:
    print(f"[citations] {msg}", file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

class HTTPError(RuntimeError):
    def __init__(self, status: int, msg: str):
        super().__init__(msg)
        self.status = status


def http_get(url: str, headers: dict | None = None, *, as_json: bool = True,
             tries: int = 6, timeout: int = 60):
    """GET with retries and exponential backoff on 429/5xx/network errors."""
    hdrs = {"User-Agent": "amirsamandar.github.io citation updater",
            "Accept": "application/json" if as_json else "text/html"}
    hdrs.update(headers or {})
    delay = 3.0
    last: Exception | None = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read().decode("utf-8", "replace")
            return json.loads(body) if as_json else body
        except urllib.error.HTTPError as e:
            last = HTTPError(e.code, f"HTTP {e.code} for {redact(url)}")
            if e.code in (400, 401, 403, 404):
                raise last
            retry_after = e.headers.get("Retry-After") if e.headers else None
            wait = float(retry_after) if retry_after and retry_after.isdigit() else delay
        except Exception as e:  # noqa: BLE001 - network errors, bad JSON
            last = e
            wait = delay
        if attempt < tries - 1:
            time.sleep(min(wait, 90))
            delay *= 2
    raise RuntimeError(f"giving up on {redact(url)}: {last}")


def redact(url: str) -> str:
    return re.sub(r"(api_key|token)=[^&]+", r"\1=***", url)


# --------------------------------------------------------------------------
# Normalisation helpers
# --------------------------------------------------------------------------

def ascii_fold(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def norm_title(t: str | None) -> str:
    if not t:
        return ""
    t = html.unescape(t)
    t = re.sub(r"<[^>]+>", " ", t)               # html tags (OpenAlex, S2)
    t = re.sub(r"\\[a-zA-Z]+", " ", t)           # latex commands
    t = ascii_fold(t).lower()
    return re.sub(r"[^a-z0-9]+", "", t)


def norm_arxiv(a: str | None) -> str:
    if not a:
        return ""
    a = a.strip()
    a = re.sub(r"^(https?://arxiv\.org/(abs|pdf)/|arxiv:)", "", a, flags=re.I)
    a = re.sub(r"\.pdf$", "", a)
    a = re.sub(r"v\d+$", "", a)
    return a if re.match(r"^(\d{4}\.\d{4,5}|[a-z\-]+(\.[A-Z]{2})?/\d{7})$", a) else ""


def norm_doi(d: str | None) -> str:
    if not d:
        return ""
    d = d.strip().lower()
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", d)
    return d if d.startswith("10.") else ""


def arxiv_from_doi(d: str) -> str:
    m = re.match(r"10\.48550/arxiv\.(.+)$", d or "")
    return norm_arxiv(m.group(1)) if m else ""


def arxiv_from_text(s: str | None) -> str:
    if not s:
        return ""
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([\w.\-/]+?)(?:v\d+)?(?:\.pdf)?(?:[?#]|$)", s, re.I)
    if m:
        return norm_arxiv(m.group(1))
    m = re.search(r"arXiv:\s*(\d{4}\.\d{4,5})", s, re.I)
    return norm_arxiv(m.group(1)) if m else ""


def name_key(name: str) -> tuple[str, str] | None:
    """('surname-last-token', 'first initial') from 'Last, First' or 'First Last'."""
    if not name:
        return None
    n = ascii_fold(html.unescape(name)).strip().strip("…").strip()
    n = re.sub(r"\s+", " ", n)
    if "," in n:
        last, first = [x.strip() for x in n.split(",", 1)]
    else:
        parts = n.split(" ")
        if len(parts) == 1:
            return None
        first, last = " ".join(parts[:-1]), parts[-1]
    last_tok = re.sub(r"[^a-z]", "", last.split(" ")[-1].lower())
    first_init = re.sub(r"[^a-z]", "", first.lower())[:1]
    return (last_tok, first_init) if last_tok and first_init else None


def short_name(name: str) -> str:
    """'Samandar, Amirhossein' -> 'A. Samandar'; 'Amirhossein Samandar' -> same."""
    n = re.sub(r"\s+", " ", html.unescape(name or "")).strip()
    if not n:
        return ""
    if "," in n:
        last, first = [x.strip() for x in n.split(",", 1)]
    else:
        parts = n.split(" ")
        if len(parts) == 1:
            return n
        # Scholar style "A Samandar" / "AH Samandar"
        first, last = " ".join(parts[:-1]), parts[-1]
    inits = []
    for tok in re.split(r"[\s.]+", first):
        if not tok:
            continue
        if "-" in tok:
            inits.append("-".join(p[:1].upper() + "." for p in tok.split("-") if p))
        elif tok.isupper() and len(tok) <= 3:          # "AH" (Scholar initials)
            inits.extend(c + "." for c in tok)
        else:
            inits.append(tok[:1].upper() + ".")
    return (" ".join(inits) + " " + last).strip()


GREEK = {n: chr(c) for n, c in zip(
    "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho "
    "sigma tau upsilon phi chi psi omega".split(), range(0x3B1, 0x3CA)) if c != 0x3C2}
GREEK.update({n.capitalize(): chr(ord(c) - 32) for n, c in GREEK.items()})
GREEK.update({"varepsilon": "ε", "varphi": "φ", "vartheta": "θ", "ell": "ℓ", "sim": "~", "simeq": "≃",
              "approx": "≈", "times": "×", "to": "→", "rightarrow": "→", "leq": "≤", "geq": "≥",
              "lesssim": "≲", "gtrsim": "≳", "pm": "±", "infty": "∞", "odot": "⊙", "prime": "′",
              "&": "&", "%": "%", "_": "_", "#": "#"})


def display_title(t: str) -> str:
    """Make LaTeX in titles readable without a math renderer: '$\\Lambda$CDM' -> 'ΛCDM'."""
    if "$" not in t and "\\" not in t:
        return t
    t = re.sub(r"\\(?:mathbb|mathcal|mathscr|mathfrak|operatorname|mathrm|mathbf|mathit|mathsf|text|textit|textbf|emph|rm|bf|it|boldsymbol)\s*\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\([A-Za-z]+|[&%_#])", lambda m: GREEK.get(m.group(1), m.group(1)), t)
    t = re.sub(r"\^\{([^{}]*)\}|\^(\S)", lambda m: (m.group(1) or m.group(2)), t)
    t = re.sub(r"_\{([^{}]*)\}|_(\w)", lambda m: (m.group(1) or m.group(2)), t)
    t = t.replace("$", "").replace("{", "").replace("}", "").replace("~", "~")
    return re.sub(r"\s+", " ", t).strip()


def date_display(d: str) -> str:
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    parts = (d or "").split("-")
    if len(parts) == 3:
        return f"{int(parts[2])} {months[int(parts[1]) - 1]} {parts[0]}"
    if len(parts) == 2:
        return f"{months[int(parts[1]) - 1]} {parts[0]}"
    return parts[0]


def year_of(date: str | None) -> str:
    m = re.match(r"(\d{4})", date or "")
    return m.group(1) if m else ""


def clean_date(d: str | None) -> str:
    """Keep YYYY, YYYY-MM or YYYY-MM-DD; drop ADS-style '-00' parts."""
    if not d:
        return ""
    d = str(d)[:10]
    d = re.sub(r"-00(-00)?$", "", d)
    d = re.sub(r"-00$", "", d)
    return d if re.match(r"^\d{4}(-\d{2}(-\d{2})?)?$", d) else ""


# --------------------------------------------------------------------------
# Publications
# --------------------------------------------------------------------------

def load_publications() -> list[dict]:
    pubs = []
    for f in sorted(PUB_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        if fm.get("status") == "prep" and not (fm.get("arxiv") or fm.get("doi")):
            continue
        pubs.append({
            "slug": f.stem,
            "title": fm.get("title", ""),
            "short": fm.get("short_title") or fm.get("title", ""),
            "arxiv": norm_arxiv(str(fm.get("arxiv") or "")),
            "doi": norm_doi(str(fm.get("doi") or "")),
            "authors_fm": fm.get("authors", ""),
        })
    return pubs


def load_overrides() -> dict:
    if OVERRIDES.exists():
        return yaml.safe_load(OVERRIDES.read_text(encoding="utf-8")) or {}
    return {}


# --------------------------------------------------------------------------
# A raw citing record, as returned by one source
# --------------------------------------------------------------------------

def rec(source: str, *, title="", authors=None, n_authors=None, collab="", date="",
        venue="", arxiv="", doi="", ids=None, url="", doctype="") -> dict:
    authors = [a for a in (authors or []) if a]
    doi = norm_doi(doi)
    arxiv = norm_arxiv(arxiv) or arxiv_from_doi(doi)
    if arxiv_from_doi(doi):
        doi = ""  # arXiv DOIs are just the arXiv id
    venue = (venue or "").strip()
    if re.search(r"arxiv|ssrn|research ?square|preprints?\.org|zenodo", venue, re.I):
        venue = ""  # preprint servers are shown through the arXiv/DOI link
    return {
        "source": source,
        "title": re.sub(r"\s+", " ", html.unescape(title or "")).strip(),
        "authors": authors,
        "n_authors": n_authors if n_authors is not None else len(authors),
        "collab": collab or "",
        "date": clean_date(date),
        "venue": venue,
        "arxiv": arxiv,
        "doi": doi,
        "ids": ids or {},
        "url": url or "",
        "doctype": doctype or "",
    }


def per_pub(fn):
    """Run fn(pub, pin, ctx) for each publication; one failure keeps that
    publication's previous data instead of failing the whole source."""
    def runner(pubs, pins, ctx):
        out, errors = {}, 0
        for p in pubs:
            try:
                out[p["slug"]] = fn(p, pins.get(p["slug"], {}), ctx)
            except SkipSource:
                raise
            except Exception as e:  # noqa: BLE001
                errors += 1
                log(f"  {p['slug']}: {e}")
                out[p["slug"]] = {"reuse_previous": True, "error": str(e)}
        if pubs and errors == len(pubs):
            raise RuntimeError(f"all {errors} lookups failed")
        return out
    return runner


class SkipSource(Exception):
    """Source deliberately not run (missing credentials)."""


# --------------------------------------------------------------------------
# INSPIRE-HEP
# --------------------------------------------------------------------------

INSPIRE = "https://inspirehep.net/api/literature"


def inspire_venue(md: dict) -> str:
    for pi in md.get("publication_info") or []:
        if pi.get("journal_title"):
            bits = [pi["journal_title"]]
            if pi.get("journal_volume"):
                bits.append(str(pi["journal_volume"]))
            art = pi.get("artid") or pi.get("page_start")
            if art:
                bits.append(str(art))
            s = " ".join(bits)
            if pi.get("year"):
                s += f" ({pi['year']})"
            return s
    dt_ = md.get("document_type") or []
    if "thesis" in dt_:
        return "Thesis"
    if "conference paper" in dt_:
        return "Conference paper"
    return ""


def inspire_lookup(pub: dict, pin: dict) -> dict | None:
    fields = "control_number,titles,authors.full_name,citation_count,citation_count_without_self_citations"
    if pin.get("inspire_recid"):
        q = f"recid:{pin['inspire_recid']}"
    elif pub["arxiv"]:
        q = f"arxiv:{pub['arxiv']}"
    elif pub["doi"]:
        q = f"doi:{pub['doi']}"
    else:
        return None
    data = http_get(f"{INSPIRE}?{urllib.parse.urlencode({'q': q, 'fields': fields, 'size': 1})}")
    hits = data.get("hits", {}).get("hits", [])
    return hits[0]["metadata"] if hits else None


def inspire_citing(recid: int) -> list[dict]:
    fields = ("control_number,titles,authors.full_name,author_count,collaborations,"
              "arxiv_eprints,dois,publication_info,earliest_date,document_type")
    out, page = [], 1
    while True:
        q = urllib.parse.urlencode({"q": f"refersto:recid:{recid}", "size": 250, "page": page,
                                    "sort": "mostrecent", "fields": fields})
        data = http_get(f"{INSPIRE}?{q}")
        hits = data.get("hits", {}).get("hits", [])
        for h in hits:
            md = h["metadata"]
            authors = [a.get("full_name", "") for a in md.get("authors") or []]
            out.append(rec(
                "inspire",
                title=(md.get("titles") or [{}])[0].get("title", ""),
                authors=authors[:12],
                n_authors=md.get("author_count") or len(authors),
                collab=", ".join(c.get("value", "") for c in md.get("collaborations") or []),
                date=md.get("earliest_date", ""),
                venue=inspire_venue(md),
                arxiv=(md.get("arxiv_eprints") or [{}])[0].get("value", ""),
                doi=(md.get("dois") or [{}])[0].get("value", ""),
                ids={"inspire": md.get("control_number")},
                url=f"https://inspirehep.net/literature/{md.get('control_number')}",
                doctype=",".join(md.get("document_type") or []),
            ) | {"_author_keys": [name_key(a) for a in authors]})
        total = data.get("hits", {}).get("total", 0)
        if page * 250 >= total or not hits:
            break
        page += 1
        time.sleep(1)
    return out


@per_pub
def run_inspire(p, pin, ctx) -> dict:
    md = inspire_lookup(p, pin)
    time.sleep(0.5)
    if not md:
        return {"count": None, "records": [], "note": "not found"}
    recid = md["control_number"]
    ctx["author_keys"][p["slug"]].update(
        k for k in (name_key(a.get("full_name", "")) for a in md.get("authors") or []) if k)
    ctx["ids"][p["slug"]]["inspire"] = recid
    records = inspire_citing(recid)
    time.sleep(0.5)
    return {"count": md.get("citation_count"), "records": records}


# --------------------------------------------------------------------------
# Semantic Scholar
# --------------------------------------------------------------------------

S2 = "https://api.semanticscholar.org/graph/v1/paper"


def s2_headers() -> dict:
    k = os.environ.get("S2_API_KEY", "").strip()
    return {"x-api-key": k} if k else {}


@per_pub
def run_s2(p, pin, ctx) -> dict:
    pace = 1.2 if s2_headers() else 3.5
    pid, md = None, {}
    for ident in ([pin["s2_id"]] if pin.get("s2_id") else []) + \
                 ([f"ARXIV:{p['arxiv']}"] if p["arxiv"] else []) + \
                 ([f"DOI:{p['doi']}"] if p["doi"] else []):
        try:
            md = http_get(f"{S2}/{urllib.parse.quote(ident, safe=':')}?fields=paperId,citationCount,authors.name",
                          s2_headers())
            pid = md["paperId"]
            break
        except HTTPError as e:
            if e.status != 404:
                raise
        finally:
            time.sleep(pace)
    if not pid:
        return {"count": None, "records": [], "note": "not found"}
    ctx["ids"][p["slug"]]["s2"] = pid
    ctx["author_keys"][p["slug"]].update(
        k for k in (name_key(a.get("name", "")) for a in md.get("authors") or []) if k)
    records, offset = [], 0
    fields = "paperId,title,authors,year,venue,externalIds,publicationDate,journal,publicationTypes"
    while offset is not None:
        data = http_get(f"{S2}/{pid}/citations?fields={fields}&limit=1000&offset={offset}", s2_headers())
        time.sleep(pace)
        for item in data.get("data") or []:
            c = item.get("citingPaper") or {}
            if not c.get("title"):
                continue
            ext = c.get("externalIds") or {}
            names = [a.get("name", "") for a in c.get("authors") or []]
            j = c.get("journal") or {}
            venue = j.get("name") or c.get("venue") or ""
            if venue and j.get("volume"):
                venue += f" {j['volume'].strip()}"
            records.append(rec(
                "s2", title=c.get("title"), authors=names[:12], n_authors=len(names),
                date=c.get("publicationDate") or str(c.get("year") or ""),
                venue=venue, arxiv=ext.get("ArXiv", ""), doi=ext.get("DOI", ""),
                ids={"s2": c.get("paperId")},
                url=f"https://www.semanticscholar.org/paper/{c.get('paperId')}",
            ) | {"_author_keys": [name_key(a) for a in names]})
        offset = data.get("next")
    return {"count": md.get("citationCount"), "records": records}


# --------------------------------------------------------------------------
# OpenAlex
# --------------------------------------------------------------------------

OA = "https://api.openalex.org"


def oa_params(extra: dict) -> str:
    p = dict(extra)
    if os.environ.get("OPENALEX_API_KEY"):
        p["api_key"] = os.environ["OPENALEX_API_KEY"].strip()
    mail = os.environ.get("OPENALEX_MAILTO", "").strip()
    if mail:
        p["mailto"] = mail
    return urllib.parse.urlencode(p)


OA_SELECT = "id,doi,title,display_name,publication_date,publication_year,authorships,primary_location,locations,ids,type,cited_by_count"


def oa_arxiv(w: dict) -> str:
    a = arxiv_from_doi(norm_doi(w.get("doi") or ""))
    if a:
        return a
    for loc in w.get("locations") or []:
        a = arxiv_from_text(loc.get("landing_page_url") or "") or arxiv_from_text(loc.get("pdf_url") or "")
        if a:
            return a
    return ""


def oa_venue(w: dict) -> str:
    src = ((w.get("primary_location") or {}).get("source") or {})
    name = src.get("display_name") or ""
    if "arxiv" in name.lower():
        return ""
    return name


@per_pub
def run_openalex(p, pin, ctx) -> dict:
    works: dict[str, dict] = {}
    cands = list(pin.get("openalex_ids") or [])
    lookups = [f"doi:{p['doi']}"] if p["doi"] else []
    if p["arxiv"]:
        lookups.append(f"doi:10.48550/arxiv.{p['arxiv']}")
    for wid in cands:
        lookups.append(wid)
    for lk in lookups:
        try:
            w = http_get(f"{OA}/works/{lk}?{oa_params({'select': OA_SELECT})}")
            works[w["id"]] = w
        except HTTPError as e:
            if e.status != 404:
                raise
        time.sleep(0.3)
    # Other versions of the same paper (preprint vs journal) are separate
    # OpenAlex works; find them by exact title.
    words = re.sub(r"[^\w\s]", " ", ascii_fold(p["title"]))
    words = " ".join(words.split()[:20])
    if words:
        data = http_get(f"{OA}/works?{oa_params({'filter': f'title.search:{words}', 'per-page': 25, 'select': OA_SELECT})}")
        for w in data.get("results") or []:
            if norm_title(w.get("title")) == norm_title(p["title"]):
                works[w["id"]] = w
        time.sleep(0.3)
    if not works:
        return {"count": None, "records": [], "note": "not found"}
    ids = [w.rsplit("/", 1)[-1] for w in works]
    ctx["ids"][p["slug"]]["openalex"] = ids
    for w in works.values():
        ctx["author_keys"][p["slug"]].update(
            k for k in (name_key((a.get("author") or {}).get("display_name", ""))
                        for a in w.get("authorships") or []) if k)
    records, cursor = [], "*"
    while cursor:
        data = http_get(f"{OA}/works?{oa_params({'filter': 'cites:' + '|'.join(ids), 'per-page': 200, 'cursor': cursor, 'select': OA_SELECT})}")
        for w in data.get("results") or []:
            names = [(a.get("author") or {}).get("display_name", "") for a in w.get("authorships") or []]
            records.append(rec(
                "openalex", title=w.get("title") or w.get("display_name"),
                authors=names[:12], n_authors=len(names),
                date=w.get("publication_date") or str(w.get("publication_year") or ""),
                venue=oa_venue(w), arxiv=oa_arxiv(w), doi=w.get("doi") or "",
                ids={"openalex": w["id"].rsplit("/", 1)[-1]}, url=w["id"],
                doctype=w.get("type") or "",
            ) | {"_author_keys": [name_key(n) for n in names]})
        cursor = (data.get("meta") or {}).get("next_cursor")
        if not data.get("results"):
            break
        time.sleep(0.3)
    return {"count": sum(w.get("cited_by_count") or 0 for w in works.values()),
            "records": records}


# --------------------------------------------------------------------------
# NASA ADS
# --------------------------------------------------------------------------

ADS = "https://api.adsabs.harvard.edu/v1/search/query"


def ads_query(q: str, fl: str, token: str, rows: int = 2000, start: int = 0) -> dict:
    qs = urllib.parse.urlencode({"q": q, "fl": fl, "rows": rows, "start": start})
    return http_get(f"{ADS}?{qs}", {"Authorization": f"Bearer {token}"})


@per_pub
def run_ads(p, pin, ctx) -> dict:
    token = os.environ.get("ADS_TOKEN", "").strip()
    if not token:
        raise SkipSource("no ADS_TOKEN secret set")
    fl = "bibcode,title,author,author_count,pubdate,doi,identifier,pub,volume,page,doctype"
    terms = []
    if pin.get("ads_bibcode"):
        terms.append(f'bibcode:"{pin["ads_bibcode"]}"')
    if p["arxiv"]:
        terms.append(f'identifier:"arXiv:{p["arxiv"]}"')
    if p["doi"]:
        terms.append(f'doi:"{p["doi"]}"')
    if not terms:
        return {"count": None, "records": [], "note": "no identifiers"}
    me = ads_query(" OR ".join(terms), "bibcode,citation_count,author", token, rows=5)
    docs = me.get("response", {}).get("docs", [])
    time.sleep(0.5)
    if not docs:
        return {"count": None, "records": [], "note": "not found"}
    bib = docs[0]["bibcode"]
    ctx["ids"][p["slug"]]["ads"] = bib
    ctx["author_keys"][p["slug"]].update(k for k in (name_key(a) for a in docs[0].get("author") or []) if k)
    records, start = [], 0
    while True:
        data = ads_query(f'citations(bibcode:"{bib}")', fl, token, rows=2000, start=start)
        docs_c = data.get("response", {}).get("docs", [])
        for d in docs_c:
            ident = " ".join(d.get("identifier") or [])
            authors = d.get("author") or []
            venue = d.get("pub") or ""
            if venue and d.get("volume"):
                venue += f" {d['volume']}"
            if venue and d.get("page"):
                venue += f" {d['page'][0]}"
            if "arxiv" in venue.lower():
                venue = ""
            records.append(rec(
                "ads", title=(d.get("title") or [""])[0], authors=authors[:12],
                n_authors=d.get("author_count") or len(authors), date=d.get("pubdate", ""),
                venue=venue, arxiv=arxiv_from_text(ident), doi=(d.get("doi") or [""])[0],
                ids={"ads": d["bibcode"]},
                url=f"https://ui.adsabs.harvard.edu/abs/{urllib.parse.quote(d['bibcode'])}/abstract",
                doctype=d.get("doctype", ""),
            ) | {"_author_keys": [name_key(a) for a in authors]})
        start += len(docs_c)
        if not docs_c or start >= data.get("response", {}).get("numFound", 0):
            break
        time.sleep(0.5)
    return {"count": docs[0].get("citation_count"), "records": records}


# --------------------------------------------------------------------------
# Google Scholar
# --------------------------------------------------------------------------

class _ScholarProfileParser(HTMLParser):
    """Rows of the profile table: title + cites link + count."""

    def __init__(self):
        super().__init__()
        self.rows: list[dict] = []
        self._cur: dict | None = None
        self._grab: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if tag == "tr" and "gsc_a_tr" in cls:
            self._cur = {"title": "", "count": "", "cites_id": ""}
            self.rows.append(self._cur)
        elif self._cur is not None and tag == "a" and "gsc_a_at" in cls:
            self._grab = "title"
        elif self._cur is not None and tag == "a" and "gsc_a_ac" in cls:
            self._grab = "count"
            m = re.search(r"cites=([\d,]+)", html.unescape(a.get("href") or ""))
            if m:
                self._cur["cites_id"] = m.group(1)

    def handle_endtag(self, tag):
        if tag == "a":
            self._grab = None

    def handle_data(self, data):
        if self._cur is not None and self._grab:
            self._cur[self._grab] += data


class _ScholarResultsParser(HTMLParser):
    """Citing papers on a scholar?cites=... results page."""

    def __init__(self):
        super().__init__()
        self.items: list[dict] = []
        self._depth = 0
        self._in_ri = False
        self._grab: str | None = None
        self._cur: dict | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if tag == "div" and "gs_ri" in cls:
            self._cur = {"title": "", "link": "", "meta": ""}
            self.items.append(self._cur)
        elif self._cur is not None and tag == "h3" and "gs_rt" in cls:
            self._grab = "title"
        elif self._cur is not None and self._grab == "title" and tag == "a":
            self._cur["link"] = a.get("href", "")
        elif self._cur is not None and tag == "div" and "gs_a" in cls:
            self._grab = "meta"

    def handle_endtag(self, tag):
        if (tag == "h3" and self._grab == "title") or (tag == "div" and self._grab == "meta"):
            self._grab = None

    def handle_data(self, data):
        if self._cur is not None and self._grab:
            self._cur[self._grab] += data


def scholar_meta(meta: str) -> tuple[list[str], str, str]:
    """'A Tamosiunas, F Cornet-Gomez… - JCAP, 2024 - iopscience.iop.org' -> authors, venue, year."""
    parts = [x.strip() for x in re.split(r"\s+[-‐-—]\s+", meta.replace("\xa0", " "))]
    authors = [a.strip(" …") for a in parts[0].split(",")] if parts else []
    authors = [a for a in authors if a and a != "…"]
    mid = parts[1] if len(parts) > 2 else (parts[1] if len(parts) == 2 and re.search(r"\d{4}", parts[1]) else "")
    m = re.search(r"\b(19|20)\d{2}\b", mid)
    year = m.group(0) if m else ""
    venue = re.sub(r",?\s*\b(19|20)\d{2}\b\s*$", "", mid).strip(" ,…")
    if venue.lower().startswith("arxiv"):
        venue = ""
    return authors, venue, year


def scholar_user(profile_text: str) -> str:
    m = re.search(r"scholar\.google\.[a-z.]+/citations\?user=([\w-]+)", profile_text)
    return m.group(1) if m else ""


def match_pub(title: str, pubs: list[dict]) -> dict | None:
    t = norm_title(title)
    best, score = None, 0.0
    for p in pubs:
        s = difflib.SequenceMatcher(None, t, norm_title(p["title"])).ratio()
        if s > score:
            best, score = p, s
    return best if score >= 0.88 else None


def run_scholar(pubs, pins, ctx) -> dict:
    user = scholar_user(PROFILE.read_text(encoding="utf-8")) if PROFILE.exists() else ""
    if not user:
        raise SkipSource("no Google Scholar link in _data/profile.yml")
    key = os.environ.get("SERPAPI_KEY", "").strip()
    prev = ctx["previous_counts"].get("scholar", {})
    res: dict[str, dict] = {}

    # 1. Profile: per-paper counts and the 'cites' id of each paper.
    rows: list[dict] = []
    if key:
        q = urllib.parse.urlencode({"engine": "google_scholar_author", "author_id": user,
                                    "num": 100, "hl": "en", "api_key": key})
        data = http_get(f"https://serpapi.com/search.json?{q}", tries=3)
        for a in data.get("articles") or []:
            cb = a.get("cited_by") or {}
            rows.append({"title": a.get("title", ""), "count": str(cb.get("value") or 0),
                         "cites_id": cb.get("cites_id") or ""})
    else:
        url = f"https://scholar.google.com/citations?user={user}&hl=en&cstart=0&pagesize=100"
        page = http_get(url, {"User-Agent": BROWSER_UA, "Accept-Language": "en-US,en;q=0.9"},
                        as_json=False, tries=2)
        parser = _ScholarProfileParser()
        parser.feed(page)
        rows = parser.rows
        if not rows:
            raise RuntimeError("Scholar profile blocked or layout changed")
    for r in rows:
        p = None
        for slug, pin in pins.items():
            if pin.get("scholar_title") and norm_title(pin["scholar_title"]) == norm_title(r["title"]):
                p = next((x for x in pubs if x["slug"] == slug), None)
        p = p or match_pub(r["title"], pubs)
        if not p:
            continue
        cnt = int(re.sub(r"\D", "", r["count"]) or 0)
        entry = res.setdefault(p["slug"], {"count": 0, "records": [], "cites_ids": []})
        entry["count"] += cnt
        if r["cites_id"]:
            entry["cites_ids"].append(r["cites_id"])

    # 2. Citing papers. Only re-fetched when the count changed (saves SerpAPI
    #    searches and avoids Scholar's rate limits); otherwise kept from last run.
    max_pages = int(os.environ.get("SCHOLAR_MAX_PAGES", "10"))
    for slug, entry in res.items():
        if not entry["count"] or not entry["cites_ids"]:
            continue
        if prev.get(slug) == entry["count"] and not ctx.get("force_scholar"):
            entry["reuse_previous"] = True
            continue
        records: list[dict] = []
        try:
            for cid in entry["cites_ids"]:
                for page_i in range(max_pages):
                    if key:
                        q = urllib.parse.urlencode({"engine": "google_scholar", "cites": cid, "num": 20,
                                                    "start": page_i * 20, "hl": "en", "api_key": key})
                        data = http_get(f"https://serpapi.com/search.json?{q}", tries=3)
                        items = data.get("organic_results") or []
                        for it in items:
                            pi = it.get("publication_info") or {}
                            authors, venue, year = scholar_meta(pi.get("summary", ""))
                            if pi.get("authors"):
                                authors = [a.get("name", "") for a in pi["authors"]] or authors
                            link = it.get("link", "")
                            records.append(rec("scholar", title=it.get("title", ""), authors=authors,
                                               n_authors=len(authors), date=year, venue=venue,
                                               arxiv=arxiv_from_text(link), url=link,
                                               ids={"scholar": it.get("result_id", "")})
                                           | {"_author_keys": [name_key(a) for a in authors],
                                              "_authors_truncated": True})
                        if len(items) < 20:
                            break
                    else:
                        q = urllib.parse.urlencode({"cites": cid, "hl": "en", "start": page_i * 10})
                        page = http_get(f"https://scholar.google.com/scholar?{q}",
                                        {"User-Agent": BROWSER_UA, "Accept-Language": "en-US,en;q=0.9"},
                                        as_json=False, tries=1)
                        parser = _ScholarResultsParser()
                        parser.feed(page)
                        if not parser.items:
                            raise RuntimeError("Scholar results page blocked")
                        for it in parser.items:
                            title = re.sub(r"^\[[A-Z]+\]\s*", "", it["title"].strip())
                            authors, venue, year = scholar_meta(it["meta"])
                            records.append(rec("scholar", title=title, authors=authors,
                                               n_authors=len(authors), date=year, venue=venue,
                                               arxiv=arxiv_from_text(it["link"]), url=it["link"])
                                           | {"_author_keys": [name_key(a) for a in authors],
                                              "_authors_truncated": True})
                        if len(parser.items) < 10:
                            break
                        time.sleep(8)
            entry["records"] = records
        except Exception as e:  # noqa: BLE001
            log(f"scholar: citing list for {slug} unavailable ({e}); keeping previous list")
            entry["reuse_previous"] = True
    return res


RUNNERS = {
    "inspire": run_inspire,
    "ads": run_ads,
    "s2": run_s2,
    "openalex": run_openalex,
    "scholar": run_scholar,
}


# --------------------------------------------------------------------------
# Merging
# --------------------------------------------------------------------------

def rec_keys(r: dict) -> list[str]:
    keys = []
    if r.get("arxiv"):
        keys.append("a:" + r["arxiv"])
    if r.get("doi"):
        keys.append("d:" + r["doi"])
    t = norm_title(r.get("title"))
    if len(t) >= 25:
        keys.append("t:" + t[:160])
    for src, v in (r.get("ids") or {}).items():
        if v and src != "scholar":
            keys.append(f"{src}:{v}")
    return keys


class DSU:
    def __init__(self):
        self.p: dict[int, int] = {}

    def find(self, x: int) -> int:
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        self.p[self.find(a)] = self.find(b)


def override_matches(r: dict, o: dict) -> bool:
    if o.get("arxiv") and norm_arxiv(str(o["arxiv"])) == r.get("arxiv"):
        return True
    if o.get("doi") and norm_doi(str(o["doi"])) == r.get("doi"):
        return True
    if o.get("title") and norm_title(o["title"]) == norm_title(r.get("title")):
        return True
    return False


def merge(raw: list[tuple[str, dict]], pubs: list[dict], ctx: dict, overrides: dict) -> list[dict]:
    """raw: list of (cited_slug, record). Returns merged citing papers."""
    own = {}
    for p in pubs:
        for k in ([f"a:{p['arxiv']}"] if p["arxiv"] else []) + ([f"d:{p['doi']}"] if p["doi"] else []) \
                 + [f"t:{norm_title(p['title'])[:160]}"]:
            own[k] = p["slug"]

    dsu, key_owner = DSU(), {}
    for i, (_, r) in enumerate(raw):
        dsu.find(i)
        for k in rec_keys(r):
            if k in key_owner:
                dsu.union(i, key_owner[k])
            else:
                key_owner[k] = i
    groups: dict[int, list[int]] = {}
    for i in range(len(raw)):
        groups.setdefault(dsu.find(i), []).append(i)

    excl = overrides.get("exclude") or []
    merged = []
    for idxs in groups.values():
        items = [raw[i] for i in idxs]
        recs = sorted((r for _, r in items), key=lambda r: PRIORITY.index(r["source"]))
        best = recs[0]

        def first(field):
            for r in recs:
                if r.get(field):
                    return r[field]
            return ""

        # Use the longest author list from the best source that has one.
        auth_src = next((r for r in recs if r["authors"] and not r.get("_authors_truncated")),
                        next((r for r in recs if r["authors"]), best))
        cites = sorted({slug for slug, _ in items})
        # A paper does not cite itself (versions of the same work).
        cites = [s for s in cites if not any(own.get(k) == s for r in recs for k in rec_keys(r))]
        if not cites:
            continue
        m = {
            "title": first("title"),
            "authors": [short_name(a) for a in auth_src["authors"][:10]],
            "n_authors": max([r["n_authors"] or 0 for r in recs if not r.get("_authors_truncated")] or [len(auth_src["authors"])]),
            "collab": first("collab"),
            "date": max((r["date"] for r in recs if r["date"]), key=len, default=""),
            "venue": first("venue"),
            "arxiv": first("arxiv"),
            "doi": first("doi"),
            "doctype": first("doctype"),
            "ids": {},
            "sources": sorted({r["source"] for r in recs}, key=PRIORITY.index),
            "cites": cites,
        }
        # Prefer the INSPIRE/arXiv date ordering: earliest full date if available.
        dates = sorted((r["date"] for r in recs if len(r["date"]) >= 7), key=lambda d: (d[:7], -len(d)))
        if dates:
            m["date"] = dates[0]
        m["year"] = year_of(m["date"]) or year_of(first("date"))
        for r in recs:
            for k, v in (r.get("ids") or {}).items():
                if v and k not in m["ids"]:
                    m["ids"][k] = v
        m["url"] = (f"https://arxiv.org/abs/{m['arxiv']}" if m["arxiv"]
                    else f"https://doi.org/{m['doi']}" if m["doi"] else first("url"))
        if any(override_matches(m, o) for o in excl):
            continue

        # Self-citations: INSPIRE's definition (any shared author with the
        # cited paper) and the narrower "I am an author".
        akeys = {k for r in recs for k in (r.get("_author_keys") or []) if k}
        m["self_own"] = ME in akeys
        carried = {s for r in recs for s in r.get("_self_for") or []}
        m["self_for"] = [s for s in cites if s in carried or akeys & ctx["author_keys"].get(s, set())]
        merged.append(m)

    # Manual additions.
    for a in overrides.get("add") or []:
        r = rec("manual", title=a.get("title", ""), authors=a.get("authors") or [],
                date=str(a.get("date") or a.get("year") or ""), venue=a.get("venue", ""),
                arxiv=str(a.get("arxiv") or ""), doi=str(a.get("doi") or ""), url=a.get("url", ""))
        cites = [c for c in (a.get("cites") or []) if any(p["slug"] == c for p in pubs)]
        if not cites or not r["title"]:
            continue
        dup = next((m for m in merged if set(rec_keys(m)) & set(rec_keys(r))), None)
        if dup:
            dup["cites"] = sorted(set(dup["cites"]) | set(cites))
            dup["sources"] = sorted(set(dup["sources"]) | {"manual"}, key=lambda s: (s not in PRIORITY, PRIORITY.index(s) if s in PRIORITY else 0))
            continue
        merged.append({
            "title": r["title"], "authors": [short_name(x) for x in r["authors"]],
            "n_authors": len(r["authors"]), "collab": "", "date": r["date"], "year": year_of(r["date"]),
            "venue": r["venue"], "arxiv": r["arxiv"], "doi": r["doi"], "doctype": "", "ids": {},
            "sources": ["manual"], "cites": cites,
            "url": r["url"] or (f"https://arxiv.org/abs/{r['arxiv']}" if r["arxiv"] else f"https://doi.org/{r['doi']}" if r["doi"] else ""),
            "self_own": ME in {name_key(x) for x in r["authors"]},
            "self_for": [s for s in cites if {name_key(x) for x in r["authors"]} & ctx["author_keys"].get(s, set())],
        })

    for m in merged:
        m["title"] = display_title(m["title"])
        m["date_display"] = date_display(m["date"])
        basis = m["arxiv"] or m["doi"] or norm_title(m["title"])
        m["id"] = "c" + hashlib.sha1(basis.encode()).hexdigest()[:10]
        m["search"] = ascii_fold(" ".join([m["title"], " ".join(m["authors"]), m["collab"], m["venue"]])).lower()
    merged.sort(key=lambda m: (m["date"] or "0000", m["title"]), reverse=True)
    return merged


def h_index(counts: list[int]) -> int:
    c = sorted(counts, reverse=True)
    return sum(1 for i, x in enumerate(c, 1) if x >= i)


# --------------------------------------------------------------------------
# Previous data (kept when a source fails)
# --------------------------------------------------------------------------

def previous_raw(prev: dict, source: str, slug: str) -> list[dict]:
    """Rebuild raw records of `source` for `slug` from the last data file."""
    out = []
    for c in prev.get("citing") or []:
        if source in c.get("sources", []) and slug in c.get("cites", []):
            r = rec(source, title=c["title"], authors=c.get("authors"), n_authors=c.get("n_authors"),
                    collab=c.get("collab", ""), date=c.get("date", ""), venue=c.get("venue", ""),
                    arxiv=c.get("arxiv", ""), doi=c.get("doi", ""),
                    ids={k: v for k, v in (c.get("ids") or {}).items() if k == source},
                    url=c.get("url", ""), doctype=c.get("doctype", ""))
            r["_author_keys"] = [name_key(a) for a in c.get("authors") or []]
            if c.get("self_own"):
                r["_author_keys"].append(ME)
            r["_self_for"] = c.get("self_for", [])
            out.append(r)
    return out


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="comma-separated sources to query (others keep previous data)")
    ap.add_argument("--force-scholar", action="store_true", help="re-fetch Scholar citing lists")
    args = ap.parse_args()

    pubs = load_publications()
    overrides = load_overrides()
    pins = overrides.get("papers") or {}
    prev = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    prev_counts = {s: {p["slug"]: (p.get("counts") or {}).get(s) for p in prev.get("papers") or []}
                   for s in SOURCES}
    prev_status = {s["id"]: s for s in prev.get("sources") or []}

    ctx = {
        "author_keys": {p["slug"]: {k for k in (name_key(n) for n in
                        re.split(r",\s*", re.sub(r"et al\.?|including", ",", p["authors_fm"] or ""))) if k}
                        for p in pubs},
        "ids": {p["slug"]: {} for p in pubs},
        "previous_counts": prev_counts,
        "force_scholar": args.force_scholar,
    }
    if "OPENALEX_MAILTO" not in os.environ and PROFILE.exists():
        m = re.search(r'^email:\s*"?([^"\s]+)"?', PROFILE.read_text(encoding="utf-8"), re.M)
        if m:
            os.environ["OPENALEX_MAILTO"] = m.group(1)

    only = set(args.only.split(",")) if args.only else set(SOURCES)
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    raw: list[tuple[str, dict]] = []
    counts: dict[str, dict[str, int | None]] = {p["slug"]: {} for p in pubs}
    status = []

    for src, name in SOURCES.items():
        st = {"id": src, "name": name, "status": "ok", "note": "", "as_of": today}
        results: dict = {}
        if src not in only:
            st.update(status="kept", note="not queried this run",
                      as_of=prev_status.get(src, {}).get("as_of", ""))
        else:
            log(f"querying {name} ...")
            try:
                results = RUNNERS[src](pubs, pins, ctx)
            except SkipSource as e:
                st.update(status="skipped", note=str(e), as_of="")
            except Exception as e:  # noqa: BLE001
                log(f"{name} failed: {e}")
                st.update(status="error", note=f"last run failed ({type(e).__name__}); showing previous data",
                          as_of=prev_status.get(src, {}).get("as_of", ""))
                results = {}
        n_links = 0
        for p in pubs:
            r = results.get(p["slug"])
            if r is not None and not r.get("reuse_previous"):
                recs = r["records"]
                counts[p["slug"]][src] = r.get("count")
            else:
                recs = previous_raw(prev, src, p["slug"])
                counts[p["slug"]][src] = (r or {}).get("count", prev_counts[src].get(p["slug"]))
            n_links += len(recs)
            raw.extend((p["slug"], x) for x in recs)
        if st["status"] == "ok" and not results:
            st.update(status="error", note="no results returned; showing previous data")
        failed = [k for k, v in results.items() if v.get("error")]
        if st["status"] == "ok" and failed:
            st["note"] = f"{len(failed)} paper(s) failed this run; previous data kept for them"
        st["links"] = n_links
        if st["status"] == "skipped" and n_links:
            st["status"] = "kept"
            st["note"] += "; showing data from an earlier run"
            st["as_of"] = prev_status.get(src, {}).get("as_of", "")
        log(f"{name}: {st['status']} ({n_links} citation links) {st['note']}")
        status.append(st)

    merged = merge(raw, pubs, ctx, overrides)

    papers = []
    for p in pubs:
        cit = [m for m in merged if p["slug"] in m["cites"]]
        papers.append({
            "slug": p["slug"], "short": p["short"], "arxiv": p["arxiv"], "doi": p["doi"],
            "ids": ctx["ids"][p["slug"]],
            "counts": counts[p["slug"]],
            "total": len(cit),
            "total_noself": sum(1 for m in cit if p["slug"] not in m["self_for"]),
        })
    totals = [x["total"] for x in papers]
    data = {
        "updated": today,
        "summary": {
            "citing_papers": len(merged),
            "citing_papers_noself": sum(1 for m in merged if set(m["cites"]) - set(m["self_for"])),
            "citations": sum(totals),
            "citations_noself": sum(x["total_noself"] for x in papers),
            "h_index": h_index(totals),
            "papers_cited": sum(1 for t in totals if t),
        },
        "sources": status,
        "papers": papers,
        "citing": merged,
    }

    log(f"{len(merged)} unique citing papers, {sum(totals)} citations, h={data['summary']['h_index']}")
    if args.dry_run:
        print(json.dumps(data["summary"], indent=2))
        for x in papers:
            print(f"{x['total']:4d}  {x['short']}  {x['counts']}")
        return 0

    def stable(d):
        d = json.loads(json.dumps(d))
        d.pop("updated", None)
        for s in d.get("sources", []):
            s.pop("as_of", None)
        return d

    if prev and stable(prev) == stable(data):
        log("no changes")
        return 0
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    log(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
