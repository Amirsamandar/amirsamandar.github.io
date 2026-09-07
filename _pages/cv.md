---
layout: archive
title: "Curriculum Vitae"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

<p class="lede">
  Cosmologist working at the intersection of cosmological data analysis, statistical inference,
  probabilistic machine learning, and computational methods. Graduating Fall 2026 and applying for
  postdoctoral positions.
</p>

<h2 class="cv-h">Education</h2>

<div class="cv-entry">
  <div class="cv-entry__when">Aug 2023 – Fall 2026 (expected)</div>
  <div class="cv-entry__what">
    <h3>Ph.D. in Physics</h3>
    <p class="cv-entry__org">Case Western Reserve University, Cleveland, Ohio, USA</p>
    <p><strong>Direct Ph.D. from the B.Sc., completed in 3.5 years.</strong><br>
    Advisors: Glenn D. Starkman, Craig J. Copi · GPA 3.7/4.0</p>
  </div>
</div>

<div class="cv-entry">
  <div class="cv-entry__when">2018 – 2023</div>
  <div class="cv-entry__what">
    <h3>B.Sc. in Physics</h3>
    <p class="cv-entry__org">Sharif University of Technology, Tehran, Iran</p>
    <p>GPA 18.85/20 — <strong>Rank 4 of 56</strong></p>
  </div>
</div>

<h2 class="cv-h">Publication summary</h2>

{% assign published = site.publications | where: "category", "published" %}
{% assign review = site.publications | where: "category", "review" %}
{% assign prep = site.publications | where: "category", "prep" %}

<ul class="cv-summary">
  <li><strong>{{ published.size | plus: review.size }} papers</strong>: {{ published.size }} published / accepted, {{ review.size }} under review. <strong>78+ citations</strong> (Google Scholar and INSPIRE-HEP). Two further first-author manuscripts in preparation, listed separately.</li>
  <li><strong>3 first-author</strong> and <strong>1 second-author</strong> papers among the {{ published.size | plus: review.size }}; both in-preparation manuscripts are first-author.</li>
  <li><strong>8 papers</strong> on CMB statistics and cosmic topology (5 in <em>JCAP</em>), plus a COMPACT Collaboration review in <em>Nature Astronomy</em> (co-author, 20+ authors).</li>
  <li><strong>2 papers</strong> on Bayesian evaluation and inference-time scaling of transformer models, including a main-conference paper at <strong>ICLR 2026</strong>.</li>
</ul>

<p class="section-more"><a href="{{ base_path }}/publications/">Full publication list &rarr;</a></p>

<h2 class="cv-h">Methodological expertise</h2>

<dl class="cv-skills">
  <dt>Inference &amp; statistics</dt>
  <dd>Bayesian inference and MCMC · likelihood-ratio / Neyman–Pearson testing · exact sampling distributions of test statistics · KL divergence and information-theoretic model comparison · ROC analysis and coverage calibration · large-scale Monte Carlo design</dd>

  <dt>Probabilistic ML</dt>
  <dd>Uncertainty quantification and posterior calibration · Dirichlet-posterior evaluation of stochastic model outputs (Scorio) · neural-network and classical classifiers benchmarked against a computable likelihood. Working knowledge of neural likelihood and likelihood-ratio estimation, variational autoencoders as likelihood emulators, normalizing flows and score-based generative models.</dd>

  <dt>Deep learning</dt>
  <dd>Transformer architectures and large language models — evaluation, uncertainty, inference-time (test-time) scaling · neural-network and classical classifiers for cosmological data · PyTorch, JAX, scikit-learn, Ray</dd>

  <dt>Computation</dt>
  <dd>GPU-accelerated and HPC / parallel scientific pipelines · numerical linear algebra on large covariance matrices · convergence and validation studies · Python, Julia, Mathematica, C</dd>

  <dt>Cosmology</dt>
  <dd>CMB temperature and polarization statistics · cosmic topology and eigenmode analysis · perturbation theory · primordial non-Gaussianity · <em>Planck</em> likelihood analysis</dd>

  <dt>Languages</dt>
  <dd>Persian (native), English (fluent)</dd>
</dl>

<h2 class="cv-h">Selected research</h2>

{% for p in site.data.research.projects %}
<div class="cv-entry">
  <div class="cv-entry__when">{{ p.dates }}</div>
  <div class="cv-entry__what">
    <h3><a href="{{ base_path }}/research/#{{ p.id }}">{{ p.title }}</a></h3>
    <p class="cv-entry__org">{{ p.affiliation }} · {{ p.role }}</p>
    <p>{{ p.lead }}</p>
  </div>
</div>
{% endfor %}

<p class="section-more"><a href="{{ base_path }}/research/">Full project descriptions &rarr;</a></p>

<h2 class="cv-h">Research mentorship</h2>

<div class="cv-entry">
  <div class="cv-entry__when">Present</div>
  <div class="cv-entry__what">
    <h3>Undergraduate Research Mentor</h3>
    <p class="cv-entry__org">Case Western Reserve University</p>
    <p>Have mentored <strong>seven undergraduate researchers</strong>, working one-on-one on the underlying
    physics, computational methods, and the interpretation and validation of numerical results.
    A manuscript from one of these projects is expected to be submitted by the end of September 2026.</p>
  </div>
</div>

<h2 class="cv-h">Software</h2>

<dl class="cv-skills">
  <dt><a href="https://github.com/CompactCollaboration/CMBtopology">CMBtopology</a></dt>
  <dd>GPU-parallelized Python/HPC package for CMB covariance matrices in compact Euclidean topologies; adopted collaboration-wide for tensor-mode likelihood analysis.</dd>
  <dt><a href="https://github.com/mohsenhariri/scorio">Scorio</a></dt>
  <dd>Open-source Bayesian evaluation toolkit for large language models (Python / Julia).</dd>
</dl>

<h2 class="cv-h">Collaborations</h2>

<dl class="cv-skills">
  <dt>COMPACT</dt>
  <dd>Cosmic topology collaboration — CWRU, Pittsburgh, Imperial College London, IFT Madrid, INFN Padova.</dd>
  <dt>LiteBIRD</dt>
  <dd>Satellite mission for CMB B-mode polarization.</dd>
</dl>

<h2 class="cv-h">Teaching</h2>

<dl class="cv-skills">
  <dt>CWRU</dt>
  <dd>Computational Methods in Physics (2025) · General Physics Lab (2023–2024)</dd>
  <dt>Sharif University</dt>
  <dd>Cosmology · Special Relativity · Electrodynamics I &amp; II (2020–2021)</dd>
</dl>

<h2 class="cv-h">Talks</h2>

<ul class="cv-talks">
{% for post in site.talks reversed %}
  <li>
    <span class="cv-talks__year">{{ post.date | default: "1900-01-01" | date: "%Y" }}</span>
    <span class="cv-talks__body">
      <a href="{{ base_path }}{{ post.url }}">{{ post.title }}</a>{% if post.type %} <em>({{ post.type }})</em>{% endif %}<br>
      <span class="cv-talks__venue">{{ post.venue }}{% if post.location and post.location != "" %}, {{ post.location }}{% endif %}</span>
    </span>
  </li>
{% endfor %}
</ul>

<h2 class="cv-h">Awards</h2>

<ul class="cv-awards">
  <li><strong>Art Walker Award for Outstanding Service</strong>, Department of Physics, Case Western Reserve University (2026)</li>
  <li>Full graduate funding (Ph.D. in Physics), Case Western Reserve University</li>
  <li>Iran National University Entrance Exams: ranked <strong>20th of 20,000</strong> (M.Sc.) and <strong>420th of 150,000</strong> (undergraduate, top 0.5%)</li>
</ul>

<h2 class="cv-h">References</h2>

<ul class="cv-refs">
  <li><strong>Glenn D. Starkman</strong> — Professor of Physics, Case Western Reserve University <em>(Ph.D. advisor)</em></li>
  <li><strong>Craig J. Copi</strong> — Department of Physics, Case Western Reserve University <em>(Ph.D. co-advisor)</em></li>
  <li><strong>Andrew H. Jaffe</strong> — Professor of Astrophysics, Imperial College London <em>(COMPACT)</em></li>
  <li><strong>Yashar Akrami</strong> — Instituto de Física Teórica (IFT) UAM-CSIC, Madrid <em>(COMPACT)</em></li>
  <li><strong>Michael Hinczewski</strong> — Professor of Physics, Case Western Reserve University <em>(machine learning)</em></li>
</ul>
