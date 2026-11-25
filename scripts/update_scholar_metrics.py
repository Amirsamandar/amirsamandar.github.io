#!/usr/bin/env python3
"""Refresh citation metrics in _data/profile.yml from Google Scholar.

Reads the Google Scholar profile linked in _data/profile.yml, takes the
"All" column of the citation table (citations, h-index, i10-index), and
rewrites only the `metrics:` values in place, so comments and formatting in
the YAML file are preserved. `as_of` is updated only when a number changes.

Google Scholar sometimes blocks automated requests (CAPTCHA). The script then
tries SerpAPI if the SERPAPI_KEY environment variable is set. If every source
fails, it leaves the file untouched and exits 0, so the site keeps the last
known figures instead of breaking.

Usage:
    python scripts/update_scholar_metrics.py            # update profile.yml
    python scripts/update_scholar_metrics.py --dry-run  # print only
    python scripts/update_scholar_metrics.py --html saved_profile.html
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "_data" / "profile.yml"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def log(msg: str) -> None:
    print(f"[scholar-metrics] {msg}", file=sys.stderr)


def scholar_user_id(profile_text: str) -> str:
    m = re.search(r"scholar\.google\.[a-z.]+/citations\?user=([\w-]+)", profile_text)
    if not m:
        raise SystemExit("No Google Scholar link found in _data/profile.yml")
    return m.group(1)


class _StatsParser(HTMLParser):
    """Collects the numbers in <td class="gsc_rsb_std"> cells, in order."""

    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []
        self._in_cell = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        if tag == "td" and "gsc_rsb_std" in (dict(attrs).get("class") or "").split():
            self._in_cell, self._buf = True, ""

    def handle_endtag(self, tag):
        if tag == "td" and self._in_cell:
            self.values.append(self._buf.strip())
            self._in_cell = False

    def handle_data(self, data):
        if self._in_cell:
            self._buf += data


def parse_scholar_html(html: str) -> dict[str, int]:
    p = _StatsParser()
    p.feed(html)
    nums = [v.replace(",", "") for v in p.values]
    # Table layout: [citations_all, citations_since, h_all, h_since, i10_all, i10_since]
    if len(nums) < 6 or not all(n.isdigit() for n in nums[:6]):
        raise ValueError("citation table not found (blocked or page layout changed)")
    return {"citations": int(nums[0]), "h_index": int(nums[2]), "i10_index": int(nums[4])}


def fetch_direct(user: str) -> dict[str, int]:
    url = f"https://scholar.google.com/citations?user={user}&hl=en"
    last_err: Exception | None = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT,
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=30) as r:
                return parse_scholar_html(r.read().decode("utf-8", "replace"))
        except Exception as e:  # noqa: BLE001
            last_err = e
            log(f"direct fetch attempt {attempt + 1} failed: {e}")
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"Google Scholar direct fetch failed: {last_err}")


def fetch_serpapi(user: str, key: str) -> dict[str, int]:
    q = urllib.parse.urlencode({"engine": "google_scholar_author", "author_id": user,
                                "hl": "en", "api_key": key})
    with urllib.request.urlopen(f"https://serpapi.com/search.json?{q}", timeout=60) as r:
        data = json.load(r)
    table = data.get("cited_by", {}).get("table", [])
    out: dict[str, int] = {}
    names = {"citations": "citations", "h_index": "h_index", "i10_index": "i10_index"}
    for row in table:
        for k, v in row.items():
            if k in names:
                out[names[k]] = int(v["all"])
    if len(out) != 3:
        raise RuntimeError(f"SerpAPI response missing metrics: {data.get('error') or table}")
    return out


def format_date(d: dt.date) -> str:
    return f"{d.day} {d:%B %Y}"


def update_profile(text: str, metrics: dict[str, int], today: dt.date) -> tuple[str, bool]:
    """Replace values inside the `metrics:` block only. Returns (new_text, changed)."""
    block = re.search(r"^metrics:\s*\n((?:[ \t]+.*\n?)+)", text, re.M)
    if not block:
        raise SystemExit("No `metrics:` block found in _data/profile.yml")
    body = block.group(1)

    def current(key: str) -> str:
        m = re.search(rf'^\s+{key}:\s*"?([^"\n#]*)"?', body, re.M)
        return m.group(1).strip() if m else ""

    changed = any(current(k) != str(v) for k, v in metrics.items())
    if not changed:
        return text, False

    new_body = body
    values = {k: str(v) for k, v in metrics.items()}
    values["source"] = "Google Scholar"
    values["as_of"] = format_date(today)
    for key, val in values.items():
        new_body, n = re.subn(rf'^(\s+{key}:\s*).*$', rf'\g<1>"{val}"', new_body, count=1, flags=re.M)
        if n == 0:
            new_body = new_body.rstrip("\n") + f'\n  {key}: "{val}"\n'
    return text[:block.start(1)] + new_body + text[block.end(1):], True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--html", help="parse a saved Scholar profile page instead of fetching")
    ap.add_argument("--profile", default=str(PROFILE))
    args = ap.parse_args()

    path = Path(args.profile)
    text = path.read_text(encoding="utf-8")
    user = scholar_user_id(text)

    metrics = None
    if args.html:
        metrics = parse_scholar_html(Path(args.html).read_text(encoding="utf-8"))
    else:
        try:
            metrics = fetch_direct(user)
        except Exception as e:  # noqa: BLE001
            log(str(e))
            key = os.environ.get("SERPAPI_KEY", "").strip()
            if key:
                try:
                    metrics = fetch_serpapi(user, key)
                except Exception as e2:  # noqa: BLE001
                    log(f"SerpAPI failed: {e2}")
            else:
                log("no SERPAPI_KEY set, so no fallback source")

    if not metrics:
        log("could not get metrics; leaving profile.yml unchanged")
        return 0

    log(f"fetched: {metrics}")
    today = dt.datetime.now(dt.timezone.utc).date()
    new_text, changed = update_profile(text, metrics, today)
    if not changed:
        log("metrics unchanged; nothing to do")
        return 0
    if args.dry_run:
        print(new_text)
    else:
        path.write_text(new_text, encoding="utf-8")
        log(f"updated {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
