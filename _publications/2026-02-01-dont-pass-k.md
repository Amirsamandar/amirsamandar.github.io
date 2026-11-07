---
title: "Don't Pass@k: A Bayesian Framework for Large Language Model Evaluation"
short_title: "Don't Pass@k"
permalink: /publication/2026-02-01-dont-pass-k
date: 2026-02-01
date_display: "2026"
status: published
selected: 4
authors: "M. Hariri, A. Samandar, M. Hinczewski, V. Chaudhary"
authors_complete: true
position: 2
lead: true
venue: "International Conference on Learning Representations (ICLR 2026)"
venue_display: "ICLR 2026, main conference"
arxiv: "2510.04265"
arxivcat: "cs.AI"
links:
  - label: "Proceedings PDF"
    url: "https://proceedings.iclr.cc/paper_files/paper/2026/file/f04edfc65463d020629673a4bc4c58e7-Paper-Conference.pdf"
  - label: "OpenReview"
    url: "https://openreview.net/forum?id=PTXi3Ef4sT"
  - label: "Code (Scorio)"
    url: "https://github.com/mohsenhariri/scorio"
summary: >-
  Replaces the Pass@k score used to compare language models with a Bayesian estimate that comes with error bars.
detail: >-
  Outcomes are modeled as categorical with a Dirichlet prior, giving a closed-form posterior mean and uncertainty for any weighted rubric. Compared with Pass@k and avg@N, the estimate converges faster and gives more stable rankings at far smaller sample counts.
contribution: >-
  As a lead author, co-developed the Bayesian framework for LLM evaluation, including posterior estimates and credible intervals for finite-sample uncertainty.
why: >-
  Gives benchmark rankings an explicit finite-sample uncertainty, so a difference between two models can be judged against its credible interval.
bibtex: |
  @inproceedings{Hariri:2026passk,
    author        = {Hariri, Mohsen and Samandar, Amirhossein and Hinczewski, Michael and Chaudhary, Vipin},
    title         = {Don't {Pass@k}: A {Bayesian} Framework for Large Language Model Evaluation},
    booktitle     = {Proceedings of the Fourteenth International Conference on Learning Representations (ICLR)},
    year          = {2026},
    eprint        = {2510.04265},
    archivePrefix = {arXiv},
    primaryClass  = {cs.AI}
  }
---
