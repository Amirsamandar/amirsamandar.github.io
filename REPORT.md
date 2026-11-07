# Website redesign: report and handoff

Prepared 7 November 2026 from the supplied brief, CV (PDF), publication list
(Samandar_Publications_CITA), and the existing site source only. No facts were
taken from the web.

---

## A. Critique of the previous site (10 points)

1. **Stale facts.** It said "Graduating Fall 2026" (the CV says 16 January 2027, expected) and listed the Nature Astronomy review as "in press" (it was published online 11 September 2026). It also showed the test-time-scaling paper as under review (it is accepted at TMLR) and Beyond KL as "in preparation" (it is arXiv:2610.17186). Part IId was missing.
2. **Contradictory metrics.** It showed 96+ citations on Publications and 78+ on the CV, with no source date.
3. **Author-position errors.** Part IIb was tagged "First author" although you are printed second. Parts Ic and IVa read "X, A. Samandar, et al.", which implies second author, but the site's own BibTeX files show you are not in the first ten.
4. **Overclaims in `_data/research.yml`.** "KL says nothing about detection probability"; the LLR "is a generalized non-central χ²" stated as universal; "supplies the validation layer that learned ratio estimators currently lack"; "almost no applied ML setting offers…"; "three first-author JCAP papers", which counts IIb.
5. **The homepage led with adjectives and tag lists, not results.** There were no headline results, no research plan, and availability sat on a buried line. "Selected publications" was filtered to published papers only, which hid your central first-author preprint.
6. **No individual contribution per collaboration paper.** Only a role badge, which a committee cannot interpret inside 15-author COMPACT lists.
7. **Four unused third-party scripts on every page** (a polyfill service, MathJax, Plotly and Mermaid from public CDNs). They slowed every page, leaked visitor data, and widened the supply-chain risk.
8. **Template residue still published.** Sample blog posts from 2012–2015 plus a "future post" dated 2199 (`future: true`), sample portfolio and teaching items, markdown and terms demo pages, `repository: academicpages/academicpages.github.io`, and a malformed Google verification meta tag.
9. **Accessibility and metadata gaps.** There was no skip link. The theme toggle was an icon-only `<a role=button>`, and the mobile navigation depended on JavaScript. There was no Person JSON-LD (empty `social.links`), no OpenGraph image, and duplicate or empty description tags were possible.
10. **Missing downloads and broken references.** There was no CV PDF at `/files/` and no research statement. The Pass@k BibTeX was malformed, and the IIb BibTeX still pointed to the arXiv preprint.

## A2. Information architecture

```
Header:  Name (home) · Research · Research plan · Publications · Talks · CV · [Dark/Light]
Footer:  Contact · Profiles (Scholar, ORCID, INSPIRE, arXiv, GitHub, ResearchGate) · CV PDF · News · Sitemap · build date

/                 Hero → Question → 4 headline results → 5 selected papers → 4 themes → Software → News (5) → Collaborations & service
/research/        Per project: Problem / Contribution / Result / Status (+ earlier research, methods, collaborations)
/research-plan/   Overarching question → Directions A, B, C (motivation, first-year deliverable, what I bring, fit with your group) → statement block
/publications/    Counts + metrics → Published · Accepted · Preprints · In preparation · Software; each with position badge, lead badge,
                  plain summary, technical detail, "My contribution", arXiv/DOI/links, BibTeX <details>
/publication/*    One page per paper (URLs unchanged from the old site; old Beyond-KL URL redirects)
/talks/, /talks/* Talks, year precision only
/cv/              HTML summary + PDF download + references (names/affiliations only)
/news/            Full dated news list
/sitemap/, /404.html, /sitemap.xml (jekyll-sitemap)
```

---

## B. Files delivered

New or rewritten (complete files):

- `_config.yml` sets the repository, metadata, `show_todos`, collection defaults, exclusions for template sample content, and plugins (only `jekyll-sitemap` and `jekyll-redirect-from`, both whitelisted).
- `_data/navigation.yml`, `_data/profile.yml` (new single source of truth), `_data/home.yml` (new), `_data/research.yml`, `_data/news.yml` (new), `_data/software.yml` (new).
- `_pages/about.md` (home), `research.md`, `research-plan.md` (new), `publications.md` (replaces `publications.html`), `talks.md` (replaces `talks.html`), `cv.md`, `news.md` (new), `sitemap.md`, `404.md`.
- `_layouts/scholar.html` (base), `_layouts/publication.html`, `_layouts/talk-entry.html`.
- `_includes/scholar/head.html` (meta, OpenGraph, Person JSON-LD, theme init), `scholar/header.html` (skip link, nav, toggle), `scholar/footer.html`.
- `_includes/pub-card.html`, `authors.html`, `position-badge.html`, `pub-counts.html`, `metrics.html`, `news-list.html`, `todo.html`.
- `assets/css/custom.scss` (self-contained; does not import the legacy theme, so there are no competing overrides) and `assets/js/site.js` (theme toggle only).
- `_publications/*.md`: all 14 records rewritten (13 public papers plus Part IIIc). Part IId was added. Beyond KL was moved to `2026-10-12-…` with a redirect from the old URL.
- `_talks/*.md`: 5 talks updated and a COSMO-26 entry added (pending, shown only while `show_todos: true`).
- `files/Samandar_CV.pdf` is the supplied CV.
- `_includes/footer/custom.html` was emptied (it held the CDN scripts; it is used only by legacy layouts).

Removed from the package: `_pages/publications.html`, `_pages/talks.html`, `files/bibtex_*.bib` (their content is now inline per paper), and `.github/workflows/scrape_talks.yml`. See `INSTALL.md` for the matching `git rm` commands.

**Design notes.**
- **Palette.** A warm ivory background with soft violet and amber "nebula" glows and a faint, sparse starfield. The dark mode uses a deep plum-indigo night sky. The accent is #693C7C, taken from your publication-list PDF.
- **Typography.** A serif display face for headings and a system sans for body text. There are no web fonts, no animation, and no external requests.

---

## C. Consistency checklist (verify before applications go out)

**Dates and status**
- [ ] Ph.D. expected **16 January 2027** (CV). The hero says "Ph.D. expected January 2027"; availability reads "Seeking postdoctoral positions starting 2027".
- [ ] Nature Astronomy review published online **11 Sep 2026** (brief), DOI 10.1038/s41550-026-02930-6 (pub list). Title capitalization: the pub list has "The topology of the Universe" and the brief has "The Topology of the Universe". The site uses the pub-list form.
- [ ] Test-time scaling: **accepted at TMLR** (pub list and CV).
- [ ] Part IIc: "Under review at JCAP" comes from the brief only; the pub list says "Preprint".
- [ ] Beyond KL submitted to arXiv 12 Oct 2026; Part IId month (Oct 2026) inferred from its arXiv identifier 2610.xxxxx.
- [ ] Year-only items: TMLR acceptance, Art Walker Award, ICLR 2026 appearance.
- [ ] Talk month/day values in `_talks` filenames are sort keys only and are never displayed. COSMO-25 is labeled "Contributed talk" (CV).

**Counts (computed from `status:` in `_publications/`)**
- [ ] 13 papers: 7 published, 1 accepted, 5 preprints; Part IIIc in preparation, not counted. This matches the pub list. The brief's older "11 counted" is superseded.
- [ ] CV page: "First author on 2 published papers (IIIa, IIIb) and on preprint arXiv:2610.17186; second author with a lead contribution on IIb and Don't Pass@k."

**Author positions and contribution labels**
- [ ] Position badges are shown only where the position is known: Beyond KL 1st, IIIa 1st, IIIb 1st, IIb 2nd, Don't Pass@k 2nd, Nature Astronomy review 4th. All others show "Co-author".
- [ ] "Lead author" badge on Beyond KL, IIIa, IIIb, IIb and Don't Pass@k, taken from the pub-list wording ("I led…", "As a lead author…", "lead author… full first-author contribution", "conceived the project…"). Confirm you want the badge on the two second-author papers.
- [ ] Test-time scaling author order conflicts: the pub list puts you 5th (after V. Singh) and the brief puts you 6th (after K. Ye). The site shows "…V. Singh, et al., including A. Samandar".
- [ ] Parts Ic and IVa show first-five authors from the old BibTeX files, then "including A. Samandar".
- [ ] BibTeX entries with long author lists are abbreviated and say so. Surname format changed to `{Carr{\'o}n Duque}, Javier` and `{Martin Barandiaran}, Mikel`.

**Scientific wording (deliberately narrowed)**
- [ ] "KL divergence alone does not determine detection probability" (not "says nothing").
- [ ] There is no universal "generalized non-central χ²" claim and no claim that NRE lacks validation.
- [ ] "Topology alone **can** induce parity-odd TB/EB correlations."
- [ ] Tensor-mode information growth is stated as "over the multipole range computed".
- [ ] The Part Va numerical comparison (D_KL ≈ 5, 1.37 L_LSS, 12%) is **not** published. A placeholder asks you to check definitions first.
- [ ] Simulation-based inference is labeled "In development … no results yet" (per your research statement). Analytic benchmarks are said to *complement* coverage tests, not replace them.

**Other decisions you should confirm**
- [ ] Selected papers (homepage): Beyond KL, IIIb, IIIa, Don't Pass@k, Nature Astronomy review. Change the `selected:` number in each paper's front matter to reorder or swap.
- [ ] Site meta description changed from "…likelihood-ratio methods and their neural counterparts" (which overstates neural work that has not produced results yet) to a factual summary in `_config.yml`.
- [ ] References: the site lists 5 (brief); the PDF CV lists 3 (Starkman, Jaffe, Akrami). No emails are shown on the site.
- [ ] The public CV PDF contains your phone number and referees' emails.
- [ ] Repository name assumed to be `Amirsamandar/amirsamandar.github.io`.
- [ ] The publication grouping is Published / Accepted / Preprints / In preparation, instead of the brief's "Under review", because review status is documented for only one preprint.
- [ ] The feed (`/feed.xml`) was dropped, since it contained only template posts, along with the unused `jekyll-feed`, `jemoji`, `jekyll-gist` and `jekyll-paginate` plugins. Old `/files/bibtex_*.bib` URLs will now 404.

---

## Update (second pass)

- **Placeholder markers removed from the site.** `show_todos` is now `false`, so no `[[TODO]]` marker renders anywhere; each open item shows neutral fallback text (for example, no mentoring count or citation figure). The items are kept in the source and listed below so nothing is lost. Set `show_todos: true` temporarily to see them highlighted again.
- **Research statement integrated, with position-specific content removed.** The Waterloo Centre for Astrophysics, Prof. Will Percival and galaxy-redshift-survey framing were taken out; "galaxy-clustering summary statistics" was generalized to "summary statistics" and "the underlying matter field" to "the underlying field". The text is on `/research-plan/#research-statement`, in US spelling, with citations turned into paper links. The `[[RESEARCH_STATEMENT_TEXT]]` block is filled, and the "Fit with your group" rows were removed (a comment in the page shows how to add one per application).
- **Website aligned with the statement:**
  - The hero positioning is now your statement's opening sentence.
  - The hero "Research statement" button opens the statement section until a PDF is added.
  - Simulation-based inference is relabeled from "Planned direction" to "In development (no results yet)", because the statement says you now lead this work.
  - The Koopman-operator / diffusion posterior project (with a University of Toronto student) is added as ongoing work.
  - The KL-divergence wording ("gives the expected log-likelihood ratio… does not tell us how often a search will detect a signal") now appears on the research page, the plan and the first headline result.
  - Don't Pass@k now mentions variation across repeated responses and finite-trial uncertainty.
- The SBI start-date conflict (brief: 2025; CV: 2026) is still open; the site shows "Current".

## Update (third pass, 7 Nov 2026)

- News item added: Google Scholar citations reached 122, h-index 7.
- Citation metrics are set once in `_data/profile.yml`, so they now appear on the Publications and CV pages. Refresh `as_of` whenever you update them.
- Test-time scaling author list corrected from your Scholar listing (A. Samandar is sixth, after K. Ye), and the badge now reads "Sixth author".

## Update (fourth pass, 7 Nov 2026)

- **Research plan restructured.** Direction A is now "Cosmic topology with Planck and future CMB polarization observations", using your text (US spelling). It covers completing the Planck PR4 analysis and extending it to polarization, likelihood emulation checked against direct calculations, accuracy under masks, noise and foregrounds, Hermitian and positive-definite covariance emulation, and temperature versus polarization at a fixed false-positive rate. A "Proposed first-year deliverable" row was assembled from that text. Direction B is now "Validated simulation-based inference and calibrated forecasts beyond topology"; Direction C (ML evaluation) is unchanged.
- **Homepage hero has a Contact and Profiles panel** under the portrait (it stacks below the buttons on phones). The footer keeps the same links.
- **Layout fix.** Research plan, paper detail, sitemap and 404 pages were flush left; they now align with the header.

## Placeholders (open items, hidden on the site)

Shown on the pages only if you set `show_todos: true`. Search the source for `todo`.

| # | Placeholder | Where to fix |
|---|---|---|
| 1 | ~~Citations and h-index~~ (done: 122 citations, h-index 7, Google Scholar, 7 Nov 2026) | `_data/profile.yml` |
| 2 | Optional: research statement PDF; then `statement_available: true` | `files/`, `_data/profile.yml` |
| 3 | ~~Research statement text~~ (done: integrated in `/research-plan/`) | — |
| 4 | Mentoring count (brief: seven; CV: several) and start (brief: 2025; CV: May 2026) | `_data/profile.yml` → `mentoring` |
| 5 | Outcome of the student manuscript that was expected by end of Sept 2026 | `_pages/cv.md` |
| 6 | Part IIb label: second author vs documented lead contribution | `_publications/2026-07-01-cosmic-topology-iib.md` (`lead_todo`) |
| 7 | ~~Test-time scaling author position~~ (done: sixth author, per your Google Scholar listing) | — |
| 8 | Part IIIc contribution line | `_publications/2026-09-01-cosmic-topology-iiic.md` |
| 9 | Part Va quantitative result (optional, after checking definitions) | `_publications/2026-08-25-cosmic-topology-va.md` |
| 10 | Which preprints are under review, and where | `_publications/*.md` → `status_note` |
| 11 | SBI start date (brief: 2025; CV: 2026) | `_data/research.yml` → `dates_todo` |
| 12 | ~~Optional diffusion/reservoir paragraph~~ (replaced by the Koopman/diffusion project from your statement; NPSE/reservoir work not mentioned) | — |
| 13 | COSMO-26: talk, poster or attendance; title, dates, location | `_talks/2026-01-01-cosmo-26.md` |
| 14 | Any other 2026 talks or posters | `_talks/` |
| 15 | Exact months and days for year-only news | `_data/news.yml` |
| 16 | Confirm all five referees agreed to be listed | `_pages/cv.md` |
| 17–19 | Optional per-application "Fit with your group" rows (removed from the public page) | `_pages/research-plan.md` |
| 20 | Repository name (assumed `Amirsamandar/amirsamandar.github.io`) | `_config.yml` |

---

## D. Alternatives to choose from

**Positioning statements (one sentence)**
1. *(current)* I work out how much evidence a single cosmological data set actually carries: deriving likelihood-ratio distributions for model detectability, computing CMB covariances for cosmic topology, and applying the same calibration to the evaluation of machine-learning models.
2. I develop calibrated statistical tests for cosmological data, determining when a model is detectable in the one sky we observe, and I apply the same reasoning to uncertainty in machine-learning evaluation.
3. I turn expected-information forecasts into calibrated detection probabilities, with exact results for Gaussian data and computed CMB covariances for cosmic topology, and I am extending the approach to learned inference validated against those exact cases.

**Homepage headlines** (current: "Calibrated inference for the one universe we observe")
1. What one sky can tell us: detectability, CMB statistics and calibrated inference
2. From expected information to detection probability

Edit `_data/home.yml` (`headline`, `positioning`) to switch.

---

## Verification performed

A real Jekyll/GitHub Pages build could **not** be run here: rubygems.org is blocked in this environment, so no Ruby gems could be installed. The checks below were run instead.

- **Sass.** `custom.scss` and the legacy `main.scss` both compile with libsass, the engine GitHub Pages uses.
- **Approximate render.** A Jekyll emulator (LiquidJS with Jekyll-style includes, the same filters, kramdown `markdown="0|1"` handling, collection permalinks and redirects) produced 33 outputs with no duplicate paths. It caught and fixed one mismatched Liquid tag.
- **Browser (Chromium, Playwright).** 7 page types × light/dark × 1280 px and 390 px: no horizontal overflow, no console errors, **no external requests**.
- **axe-core** (WCAG 2.0/2.1 A and AA, plus best-practice) on 11 page types in both themes: **0 violations**, including color contrast over the new background.
- **Keyboard and structure.** The first Tab stop is the skip link, which moves focus to `#main`. BibTeX `<details>` opens with Enter. Every page has exactly one `<h1>` and no skipped heading levels.
- **Theme and no-JS.** The toggle switches theme, sets `aria-pressed` and persists after reload. Without JavaScript the toggle is hidden, the system color scheme is followed, and navigation works.
- **Metadata.** Person JSON-LD parses (6 `sameAs` links, CWRU affiliation). There is exactly one meta description, and the OpenGraph tags are present.
- **Links and copy.** No broken internal links. Homepage copy is about 600 words excluding paper cards; the "question" is 121 words. A search for stale claims (Fall 2026, 96+, 78+, in press, says nothing, non-central, CDN hosts, "passionate/cutting-edge/novel") found nothing.

**Not verified:** the actual GitHub Pages build, live external links, Lighthouse scores, Safari/Firefox/real phones, screen-reader behavior, and Google rich-results validation.

---

## After you deploy (10 checks)

1. Confirm the GitHub Actions/Pages build is green and `https://amirsamandar.github.io/` serves the new homepage.
2. Click every header and footer link on a phone and a laptop, and confirm `/publications/`, `/talks/` and `/research-plan/` each render once.
3. Open `/files/Samandar_CV.pdf` and, once added, `/files/Samandar_Research_Statement.pdf`.
4. Check that old URLs redirect: `/about/`, `/resume`, `/publication/2026-09-01-beyond-kl-divergence`.
5. Spot-check every arXiv, DOI, OpenReview, proceedings and GitHub link.
6. Work through the open items in the placeholder table (optionally with `show_todos: true` locally), then rebuild and re-read every page.
7. In Google Search Console (the verification file `google4fb2cd880434ebe1.html` is kept), submit `/sitemap.xml` and request indexing of `/`.
8. Run Lighthouse (mobile) on `/` and `/publications/` and aim for 95+ on Accessibility, Best Practices and SEO.
9. Run the Rich Results Test or the schema.org validator on `/` to confirm the Person record.
10. Test in Safari iOS and Chrome Android in both light and dark mode, and paste the URL into Slack or email to confirm the preview card.
