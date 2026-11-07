---
title: "Research directions, 2027 onward"
permalink: /research-plan/
description: "Research statement and proposed postdoctoral directions of Amirhossein Samandar: calibrated detectability for CMB and large-scale-structure data, validated simulation-based inference, and calibrated evaluation of ML systems used in science."
kicker: "Research plan"
lede: "My research statement, followed by three proposed directions for a postdoctoral position. The directions are prospective: deliverables are plans, not results."
---
{%- assign profile = site.data.profile -%}
<div markdown="0">
<div class="wrap prose">
<section aria-labelledby="overarching">
  <h2 id="overarching">The overarching question</h2>
  <p class="question">How much does a single realization of the data actually tell us about a model, and how do we report that with an uncertainty that has been checked? In cosmology the answer has to come from one sky. My plan is to turn that question into calibrated tools: exact distributions where the likelihood is Gaussian, simulation-based inference where it is not, with the exact cases serving as tests for the learned methods.</p>
</section>
</div>
</div>

<div class="wrap prose statement" markdown="1">
<h2 id="research-statement">Research statement</h2>

My research centers on how we extract physical information from cosmological data, determine what the data can distinguish, and make demanding analyses computationally feasible without compromising their statistical interpretation. Through my work on cosmic topology, I have approached these questions from both the theoretical and the computational side, and I aim to carry this work to other cosmological observables, including large-scale structure, bringing experience in cosmological modeling, statistical forecasting, and learned inference.

Machine learning makes some of these analyses computationally accessible, but an accurate prediction of an observable does not by itself establish that the inferred constraints are reliable. A narrow posterior may reflect information in the data, restrictive simulation assumptions, or errors in a learned approximation. Understanding these differences is central to the work I propose. I would begin with inference from summary statistics, where reference analyses can establish the accuracy required of an approximation, and then develop a focused extension toward inference of the underlying field and cosmological parameters.

<h3 id="foundation">Research foundation and current work</h3>

Within the COMPACT Collaboration, my work spans theoretical calculations, computational modeling, and cosmological data analysis. In my first-author work on spin-2 perturbations, I derived eigenmodes and cosmic microwave background (CMB) covariance matrices for orientable Euclidean manifolds, connecting spatial topology to temperature and polarization observables ([JCAP 08 (2025) 015](https://arxiv.org/abs/2503.08671)). I also investigated how topology can generate parity-odd CMB correlations without parity-violating local microphysics ([JCAP 11 (2024) 020](https://arxiv.org/abs/2407.09400)).

I developed [CMBtopology](https://github.com/CompactCollaboration/CMBtopology), a GPU-parallelized Python/HPC package used across the collaboration for tensor-mode likelihood analysis, and I am developing an end-to-end pipeline to constrain cosmic topology using Planck PR4 data. As a LiteBIRD adjoint member, I am also developing a forecasting pipeline to constrain cosmic topology using high-fidelity E-mode polarization data alongside temperature data. I have compared learned classifiers of simulated CMB maps against a directly evaluable likelihood ([JCAP 09 (2024) 057](https://arxiv.org/abs/2404.01236)). I now lead work on neural likelihood emulators and amortized inference, validated against conventional Bayesian methods. Because the likelihood can be evaluated directly in these problems, I can examine where learned approximations succeed and where they alter the inference.

In *Beyond the Kullback–Leibler divergence: the likelihood-ratio distribution as a detectability measure* ([arXiv:2610.17186](https://arxiv.org/abs/2610.17186)), I developed a forecasting pipeline connecting statistical distinguishability to detection probabilities and parameter recovery. For two specified models, the KL divergence gives the expected log-likelihood ratio when data are drawn from the model in its first argument. It does not, by itself, tell us how often a search will detect a signal or recover its parameters. I derive the log-likelihood-ratio distributions for Gaussian data and use simulations to calibrate the full parameter search, including false detections and the effect of the detection criterion on the recovered parameters. Applications to cosmic topology, primordial tensor modes, and dark energy show why a forecast needs to account for the behavior of the analysis that will actually be performed.

I also work on statistical evaluation and inference methods in artificial intelligence. In *Don't Pass@k* ([ICLR 2026](https://arxiv.org/abs/2510.04265)), we developed a Bayesian framework for evaluating language models that accounts for variation across repeated responses and for the uncertainty from a finite number of trials. I also coauthored a study of inference-time scaling ([accepted at TMLR](https://arxiv.org/abs/2608.04001)) that examines how additional computation affects reasoning performance and how those gains are evaluated. In a separate ongoing project with a student at the University of Toronto, we are investigating whether Koopman-operator methods can reduce the computational cost of diffusion-based posterior estimation without distorting the inferred distribution.

</div>

<div markdown="0">
<div class="wrap prose">
<h2 id="directions" class="directions-title">Proposed directions</h2>

<section class="direction" aria-labelledby="dir-a">
  <p class="direction__label">Direction A</p>
  <h3 id="dir-a">Calibrated detectability for coming CMB and large-scale-structure data</h3>
  <dl class="facts">
    <dt>Motivation</dt>
    <dd>Detectability forecasts, including the cosmic-topology forecasts in my collaboration's papers, are commonly summarized by the KL divergence, an expected information gain. It does not, by itself, say how often a search will detect a signal or recover its parameters: the size of the parameter space, its boundaries and the detection criterion also matter, so the relation must be calibrated for each model family and test statistic. Missions such as LiteBIRD and Taurus, and large-scale-structure surveys, need forecasts that account for the analysis that will actually be performed.</dd>
    <dt>Proposed first-year deliverable</dt>
    <dd>A calibrated detectability analysis for one forecast target, for example the tensor-to-scalar ratio from B-mode polarization or a topology search combining temperature and E-mode polarization: likelihood-ratio distributions, simulation-calibrated false-detection rates and detection probabilities, and parameter recovery, released with the code.</dd>
    <dt>What I bring</dt>
    <dd>The likelihood-ratio framework for Gaussian data (arXiv:2610.17186), already applied to cosmic topology, primordial tensor modes and dark energy; full CMB covariance modeling in temperature and polarization; CMBtopology for GPU computation of large covariance matrices; the LiteBIRD topology forecasting pipeline and the Planck PR4 topology pipeline, both in development.</dd>
  </dl>
</section>

<section class="direction" aria-labelledby="dir-b">
  <p class="direction__label">Direction B</p>
  <h3 id="dir-b">Validated simulation-based inference for cosmology</h3>
  <dl class="facts">
    <dt>Motivation</dt>
    <dd>Learned emulators and neural posterior estimators can make demanding analyses computationally feasible, but an accurate prediction of an observable does not by itself establish that the inferred constraints are reliable. A narrow posterior may reflect information in the data, restrictive simulation assumptions, or errors in the learned approximation. Problems where the likelihood can be evaluated directly, including Gaussian problems with known likelihood-ratio distributions, show where an approximation succeeds and where it alters the inference, alongside, not instead of, simulation-based calibration and coverage tests.</dd>
    <dt>Proposed first-year deliverable</dt>
    <dd>Inference from summary statistics in a setting where a reference analysis fixes the accuracy an approximation must reach: an amortized neural method compared with conventional Bayesian inference and accepted only after passing calibration and coverage tests, followed by a focused extension toward inference of the underlying field and cosmological parameters.</dd>
    <dt>What I bring</dt>
    <dd>Exact sampling distributions of test statistics; experience comparing learned classifiers of simulated CMB maps with a directly evaluable likelihood (JCAP 09 (2024) 057); GPU/HPC pipelines; ongoing work, which I lead, on neural likelihood emulators and amortized inference validated against conventional Bayesian methods (in development, no results yet); and an ongoing project on whether Koopman-operator methods can reduce the cost of diffusion-based posterior estimation without distorting the inferred distribution.</dd>
  </dl>
</section>

<section class="direction" aria-labelledby="dir-c">
  <p class="direction__label">Direction C</p>
  <h3 id="dir-c">Calibrated evaluation and uncertainty for ML systems used in science</h3>
  <dl class="facts">
    <dt>Motivation</dt>
    <dd>Machine-learning systems, including language models, are increasingly used inside scientific workflows, and are often compared by scores reported without uncertainty. A score from a finite number of trials is a noisy estimate; it should account for variation across repeated responses, which is the same posterior reasoning used for cosmological data.</dd>
    <dt>Proposed first-year deliverable</dt>
    <dd>An uncertainty-aware evaluation protocol for one class of ML tools used in a scientific pipeline, with posterior estimates and credible intervals in place of point scores, and reporting requirements that separate exact replay from distributional reproducibility.</dd>
    <dt>What I bring</dt>
    <dd>The Bayesian evaluation framework of Don't Pass@k (ICLR 2026); the Scorio toolkit; the study of inference-time scaling and its evaluation (accepted, TMLR); an extension to reinforcement learning, where calibrated evaluation shapes the training signal, now underway.</dd>
  </dl>
</section>
{%- comment %}
  To tailor this page for one application, add a row inside any <dl> above:
    <dt>Fit with your group</dt>
    <dd>…the group's survey, simulator or benchmark, and how this direction plugs in…</dd>
{% endcomment %}

<p class="muted">{% if profile.statement_available %}<a href="{{ profile.statement_pdf | relative_url }}">Download the full research statement (PDF)</a>.{% else %}A full research statement is available on request.{% endif %}</p>
</div>
</div>
