---
permalink: /
title: "Amirhossein Samandar"
excerpt: "Statistical inference for cosmological data — likelihood-ratio methods and their neural counterparts."
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

{% include base_path %}

<div class="hero">
  <p class="hero__kicker">Ph.D. Candidate in Physics · Case Western Reserve University</p>
  <p class="hero__statement">
    I work on <strong>statistical inference for cosmological data</strong>, with a focus on
    <strong>likelihood-ratio methods and their neural counterparts</strong>.
  </p>
  <p class="hero__body">
    My thesis develops exact <strong>detection-probability theory</strong> for Gaussian model comparison and applies
    it to <strong>CMB statistics</strong>. Alongside it I build <strong>simulation-based inference</strong> pipelines
    that replace intractable MCMC scans, and work on <strong>calibrated Bayesian evaluation</strong> of language
    models. I move between analytic derivation, GPU/HPC implementation, and validation of learned inference.
  </p>
  <ul class="hero__tags">
    <li>Statistical inference</li>
    <li>Cosmological data analysis</li>
    <li>Simulation-based inference</li>
    <li>Information theory</li>
    <li>CMB &amp; cosmic topology</li>
    <li>Probabilistic machine learning</li>
  </ul>
  <p class="hero__actions">
    <a class="btn-primary" href="{{ base_path }}/research/">Research</a>
    <a class="btn-ghost" href="{{ base_path }}/publications/">Publications</a>
    <a class="btn-ghost" href="{{ base_path }}/cv/">CV</a>
  </p>
  <p class="hero__seeking">Seeking postdoctoral positions beginning 2027.</p>
</div>

<section class="home-section">
  <h2 class="section-title">The question behind the work</h2>
  <p class="section-lede">
    Cosmology gives us one universe and one sky. Nearly every statistic we use to decide whether a model
    is <em>detectable</em> is an average over an ensemble of universes we will never observe. My research
    asks what those ensemble quantities actually tell us about the single measurement in hand — and builds
    the machinery, analytic and learned, to answer that honestly.
  </p>
  <p class="section-lede">
    The same question turns out to have teeth outside cosmology. A benchmark score for a language model is
    also one noisy draw from a distribution, reported as if it were a number. The methods transfer.
  </p>
</section>

<section class="home-section">
  <h2 class="section-title">Current work</h2>
  <div class="proj-grid">
    {% for p in site.data.research.projects limit: 3 %}
    <article class="proj-card">
      <p class="proj-card__dates">{{ p.dates }}</p>
      <h3 class="proj-card__title"><a href="{{ base_path }}/research/#{{ p.id }}">{{ p.title }}</a></h3>
      <p class="proj-card__lead">{{ p.lead }}</p>
      <ul class="proj-card__tags">
        {% for t in p.tags %}<li>{{ t }}</li>{% endfor %}
      </ul>
    </article>
    {% endfor %}
  </div>
  <p class="section-more"><a href="{{ base_path }}/research/">All research projects &rarr;</a></p>
</section>

<section class="home-section">
  <h2 class="section-title">Selected publications</h2>
  {% assign pubs = site.publications | where: "category", "published" | sort: "date" | reverse %}
  <ul class="pub-list pub-list--compact">
    {% for post in pubs limit: 4 %}{% include pub-card.html %}{% endfor %}
  </ul>
  <p class="section-more"><a href="{{ base_path }}/publications/">Full publication list &rarr;</a></p>
</section>

<section class="home-section">
  <h2 class="section-title">Software</h2>
  <div class="soft-grid">
    <article class="soft-card">
      <h3 class="soft-card__title"><a href="https://github.com/CompactCollaboration/CMBtopology">CMBtopology</a></h3>
      <p>GPU-parallelized Python/HPC package computing CMB covariance matrices for compact Euclidean
      topologies. Adopted collaboration-wide for tensor-mode likelihood analysis.</p>
      <p class="soft-card__meta">Python · CUDA · HPC</p>
    </article>
    <article class="soft-card">
      <h3 class="soft-card__title"><a href="https://github.com/mohsenhariri/scorio">Scorio</a></h3>
      <p>Open-source Bayesian evaluation toolkit for large language models, implementing
      Dirichlet-posterior estimates and credible intervals in place of Pass@<em>k</em>.</p>
      <p class="soft-card__meta">Python · Julia</p>
    </article>
  </div>
</section>
