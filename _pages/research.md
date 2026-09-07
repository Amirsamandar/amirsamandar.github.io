---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
---

{% include base_path %}

<p class="lede">
  My work sits at the intersection of statistical inference, cosmological data analysis and probabilistic
  machine learning. Each project below is stated as a problem, a contribution and a result, so the
  specific technical claim is visible rather than implied. Where a project is a direction I intend to
  develop rather than completed work, it says so.
</p>

<div class="method-strip">
  <div class="method-strip__group">
    <h3>Inference &amp; statistics</h3>
    <p>Bayesian inference and MCMC · likelihood-ratio and Neyman–Pearson testing · exact sampling
    distributions of test statistics · KL divergence and information-theoretic model comparison ·
    ROC analysis and coverage calibration · large-scale Monte Carlo design</p>
  </div>
  <div class="method-strip__group">
    <h3>Probabilistic machine learning</h3>
    <p>Uncertainty quantification and posterior calibration · Dirichlet-posterior evaluation of stochastic
    model outputs · classifiers benchmarked against a computable likelihood. Working knowledge of neural
    likelihood and likelihood-ratio estimation, variational autoencoders as likelihood emulators,
    normalizing flows and score-based generative models.</p>
  </div>
  <div class="method-strip__group">
    <h3>Computation</h3>
    <p>GPU-accelerated and HPC/parallel scientific pipelines · numerical linear algebra on large covariance
    matrices · convergence and validation studies · Python, Julia, Mathematica, C · PyTorch, JAX,
    scikit-learn, Ray</p>
  </div>
</div>

{% for p in site.data.research.projects %}
<article class="research-entry" id="{{ p.id }}">
  <header class="research-entry__head">
    <h2 class="research-entry__title">{{ p.title }}</h2>
    <p class="research-entry__meta">
      <span>{{ p.dates }}</span>
      <span>{{ p.role }}</span>
      <span>{{ p.affiliation }}</span>
    </p>
  </header>

  <p class="research-entry__lead">{{ p.lead }}</p>

  <dl class="research-entry__body">
    <dt>Problem</dt><dd>{{ p.problem }}</dd>
    <dt>Contribution</dt><dd>{{ p.contribution }}</dd>
    <dt>Result</dt><dd>{{ p.result }}</dd>
  </dl>

  <p class="research-entry__foot">
    <span class="research-entry__status">{{ p.status }}</span>
    <span class="research-entry__tags">{% for t in p.tags %}<span>{{ t }}</span>{% endfor %}</span>
  </p>
</article>
{% endfor %}

<article class="research-entry" id="earlier">
  <header class="research-entry__head">
    <h2 class="research-entry__title">Earlier research</h2>
    <p class="research-entry__meta">
      <span>2022 – 2023</span>
      <span>Institute for Research in Fundamental Sciences (IPM), Tehran</span>
    </p>
  </header>
  <p class="research-entry__lead">
    Complex scalar-field dark matter in the non-relativistic limit — effective field theory, canonical
    transformations and multi-field axion models (advisor: M. H. Namjoo). Cosmological perturbation
    theory, inflation and primordial non-Gaussianity using <code>xAct</code> (advisor: H. Firouzjahi).
  </p>
</article>

<section class="collab-block">
  <h2 class="section-title">Collaborations</h2>
  <div class="collab-grid">
    <div class="collab-card">
      <h3>COMPACT</h3>
      <p>Cosmic topology collaboration — CWRU, Pittsburgh, Imperial College London, IFT Madrid, INFN Padova.</p>
    </div>
    <div class="collab-card">
      <h3>LiteBIRD</h3>
      <p>Satellite mission for CMB B-mode polarization and constraints on inflation.</p>
    </div>
  </div>
</section>
