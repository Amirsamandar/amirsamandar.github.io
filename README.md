<div align="center">

# Amirhossein Samandar

**Ph.D. candidate in Physics · Case Western Reserve University**

Cosmology · statistical inference · probabilistic machine learning · computational methods

[![Website](https://img.shields.io/badge/website-amirsamandar.github.io-5a3696?style=flat-square)](https://amirsamandar.github.io)
[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-profile-4285F4?style=flat-square&logo=googlescholar&logoColor=white)](https://scholar.google.com/citations?user=cst228UAAAAJ)
[![INSPIRE-HEP](https://img.shields.io/badge/INSPIRE--HEP-profile-0b3d91?style=flat-square)](https://inspirehep.net/authors/2778276)
[![arXiv](https://img.shields.io/badge/arXiv-papers-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/search/?searchtype=author&query=Samandar%2C+A)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0004--4051--1654-a6ce39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0004-4051-1654)

</div>

---

This repository holds the source of my academic website, **[amirsamandar.github.io](https://amirsamandar.github.io)**.

We observe exactly one universe, so knowing what we can reliably learn from it is central to cosmology. My research asks whether non-trivial cosmic topology leaves detectable traces in the cosmic microwave background (CMB), how often a search can actually recover a real signal, and how machine learning trained on simulations can speed up inference while keeping its uncertainties honest. I also work on calibrated Bayesian evaluation of large language models.

I am advised by Glenn D. Starkman and Craig J. Copi and work within the COMPACT Collaboration. **I am seeking postdoctoral positions starting in 2027.**

## Selected work

| Topic | Result |
|---|---|
| **Detectability beyond the KL divergence** | The KL divergence alone does not say how often a search detects a signal. Likelihood-ratio distributions do. [arXiv:2610.17186](https://arxiv.org/abs/2610.17186) |
| **Parity violation from topology** | Spatial topology alone can induce parity-odd TB and EB correlations in the CMB. [JCAP 11 (2024) 020](https://arxiv.org/abs/2407.09400) |
| **Tensor modes in compact spaces** | First spin-2 eigenmodes and CMB correlation matrices for orientable compact flat spaces. [JCAP 08 (2025) 015](https://arxiv.org/abs/2503.08671) |
| **Bayesian LLM evaluation** | A Dirichlet-posterior replacement for Pass@k with credible intervals and more stable rankings. [ICLR 2026](https://arxiv.org/abs/2510.04265) |

**Software:** [CMBtopology](https://github.com/CompactCollaboration/CMBtopology), GPU-parallelized CMB covariance matrices for compact topologies · [Scorio](https://github.com/mohsenhariri/scorio), Bayesian evaluation toolkit for LLMs.

## The website

| Page | What it shows |
|---|---|
| [Home](https://amirsamandar.github.io/) | Research question, headline results, selected papers, news |
| [Research](https://amirsamandar.github.io/research/) | Each project: problem, contribution, result, status |
| [Research plan](https://amirsamandar.github.io/research-plan/) | Proposed postdoctoral directions |
| [Publications](https://amirsamandar.github.io/publications/) | Every paper with my author position, my contribution and BibTeX |
| [Citations](https://amirsamandar.github.io/citations/) | Every paper citing my work, merged from five databases |
| [Talks](https://amirsamandar.github.io/talks/) · [CV](https://amirsamandar.github.io/cv/) · [News](https://amirsamandar.github.io/news/) | Talks, CV with PDF download, dated news |

## Repository layout

```
_data/
  profile.yml               name, links, availability, citation metrics (single source of truth)
  home.yml                  homepage text and headline results
  research.yml              research themes and projects
  news.yml, software.yml    news items, software cards
  navigation.yml            header and footer menus
  citations.json            citing papers (generated, do not edit by hand)
  citations_overrides.yml   manual fixes for the citation data
_publications/              one Markdown file per paper
_talks/                     one Markdown file per talk
_pages/                     the site's pages (home is about.md)
_layouts/, _includes/       page templates
assets/css/custom.scss      all styling (color tokens at the top)
assets/js/                  theme toggle, citation filters
files/                      downloadable PDFs (CV)
images/                     portrait, icons, background
scripts/                    citation and metrics updaters, background generator
.github/workflows/          scheduled updates
```

## Updating the site

| To change… | Edit |
|---|---|
| Name, links, availability, Ph.D. date | `_data/profile.yml` |
| Homepage wording and headline results | `_data/home.yml` |
| Research themes and projects | `_data/research.yml` |
| Add a paper | new file in `_publications/` (copy an existing one; set `status`, `arxiv`, `doi`, `contribution`) |
| Add a talk | new file in `_talks/` |
| News | `_data/news.yml` |
| Menu | `_data/navigation.yml` |
| Colors and fonts | `assets/css/custom.scss` |
| CV PDF | replace `files/Samandar_CV.pdf` |

Set `show_todos: true` in `_config.yml` to see unresolved placeholders highlighted on the pages.

## Automation

Two GitHub Actions keep the numbers current without manual work:

- **Update citations** (`update_citations.yml`) runs every Monday, whenever a publication changes, and on demand. It collects citing papers from INSPIRE-HEP, Semantic Scholar, OpenAlex, NASA ADS and Google Scholar, removes duplicates, flags self-citations, and commits `_data/citations.json`.
- **Update citation metrics** (`update_scholar_metrics.yml`) refreshes the citation count, h-index and i10-index from Google Scholar every Monday.

Optional repository secrets (*Settings → Secrets and variables → Actions*) switch on more sources:

| Secret | Enables |
|---|---|
| `ADS_TOKEN` | NASA ADS ([get a token](https://ui.adsabs.harvard.edu/user/settings/token)) |
| `SERPAPI_KEY` | Reliable Google Scholar data via [SerpAPI](https://serpapi.com) |
| `S2_API_KEY` | Higher Semantic Scholar rate limit |
| `OPENALEX_API_KEY` | Higher OpenAlex daily limit |

To fix a wrong or missing citation, edit `_data/citations_overrides.yml`. The fix is kept on every later run.

## Preview locally

With Ruby and Bundler installed:

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000
```

With Docker, run `docker compose up`. In VS Code, use *Dev Containers: Reopen in Container*. Either way the site is served on port 4000.

To refresh citations locally: `pip install pyyaml && python scripts/update_citations.py --dry-run`.

## Credits

Built with [Jekyll](https://jekyllrb.com) and hosted on GitHub Pages. The repository started from the [AcademicPages](https://github.com/academicpages/academicpages.github.io) template (based on Minimal Mistakes). The current design is custom. Code is under the MIT License (see `LICENSE`). Text, photos and the CV are © Amirhossein Samandar.
