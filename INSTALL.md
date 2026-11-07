# Installing the redesign

This folder is a complete replacement for the `amirsamandar.github.io` repository
(Jekyll on GitHub Pages, no new plugins). Your `.git` history is not included.

## 1. Copy into your repository

```bash
cd path/to/amirsamandar.github.io        # your local clone
git checkout -b redesign-2027
# copy everything from this folder over the clone (keeps your .git):
rsync -av --exclude .git /path/to/unzipped/amirsamandar.github.io/ ./
```

## 2. Remove superseded files

Copying does not delete files. These are replaced or no longer used. Most are
already excluded in `_config.yml`, so the site builds correctly even if you skip
this step, but deleting them keeps the repository clean:

```bash
git rm -q _pages/publications.html _pages/talks.html          # old route owners
git rm -q files/bibtex_*.bib                                  # BibTeX now lives in each _publications record
git rm -q .github/workflows/scrape_talks.yml                  # talk-map scraper (talk map disabled)
git rm -rq _posts _portfolio _teaching                        # template sample content
git rm -q _pages/markdown.md _pages/terms.md _pages/non-menu-page.md \
          _pages/archive-layout-with-content.md _pages/portfolio.html \
          _pages/teaching.html _pages/talkmap.html _pages/cv-json.md \
          _pages/year-archive.html _pages/tag-archive.html \
          _pages/category-archive.html _pages/collection-archive.html \
          _pages/page-archive.html
git rm -q _publications/2026-09-01-beyond-kl-divergence.md    # replaced by 2026-10-12-beyond-kl-divergence.md (old URL redirects)
```

## 3. Add the files only you have

- Optional: `files/Samandar_Research_Statement.pdf`, then set
  `statement_available: true` in `_data/profile.yml`. The hero's "Research
  statement" button then downloads the PDF instead of opening the statement
  section of `/research-plan/`.
- `files/Samandar_CV.pdf` is included (the CV you supplied). Note that it shows
  your phone number and referees' emails, and the site makes it public.

## 4. Open items

`show_todos` is `false` in `_config.yml`, so no placeholder markers appear on the
site; unresolved items show neutral fallback text instead. The open items are
listed under "Placeholders" in `REPORT.md`. To see them highlighted on the
pages while you work through them, set `show_todos: true` temporarily.

## 5. Build and preview locally

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000
```

Then push the branch, open a pull request, and merge to the branch GitHub Pages
publishes from.

## Where to edit things later

| What | File |
|---|---|
| Name, links, availability, PhD date, metrics, mentoring | `_data/profile.yml` |
| Homepage wording (headline, positioning, question, four results) | `_data/home.yml` |
| Research themes, projects, methods | `_data/research.yml` |
| News items | `_data/news.yml` |
| Software cards | `_data/software.yml` |
| One paper (summary, contribution, links, BibTeX, `selected:` rank) | `_publications/*.md` |
| Talks | `_talks/*.md` |
| Navigation | `_data/navigation.yml` |
| Colors, type, layout | `assets/css/custom.scss` (tokens at the top) |
| Research plan text and statement block | `_pages/research-plan.md` |

Publication counts are computed from the `status:` field in each `_publications`
file (`published`, `accepted`, `preprint`, `prep`), so the totals update
automatically. Citation metrics appear only through `_includes/metrics.html`.
