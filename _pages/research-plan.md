---
title: "Research directions, 2027 onward"
permalink: /research-plan/
description: "Research statement and proposed postdoctoral directions of Amirhossein Samandar: cosmic topology with Planck and future CMB polarization data, validated simulation-based inference and calibrated forecasts, and calibrated evaluation of ML systems used in science."
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
  <h3 id="dir-a">Cosmic topology with Planck and future CMB polarization observations</h3>
  <dl class="facts">
    <dt>Motivation</dt>
    <dd>I would like to bring my theoretical work on cosmic topology into closer contact with observations by completing the Planck PR4 analysis and extending it to polarization. The calculations developed within COMPACT tell us how a non-trivial topology changes CMB correlations, but searching for these signatures requires evaluating many models with different spatial scales and observer positions and orientations.</dd>
    <dt>Likelihood emulation for the search</dt>
    <dd>This is where I see a useful role for likelihood emulation. Building on my current work, I would investigate how much it can reduce the cost of the search while retaining the accuracy needed to distinguish topological signatures. Models and angular resolutions for which direct likelihood calculations remain feasible would allow me to examine how the approximation affects the inferred parameters and their uncertainties.</dd>
    <dt>Accuracy on the observed sky</dt>
    <dd>The accuracy needed from an emulator depends on the information available in the observed sky. Masks, instrumental noise, and residual foregrounds affect our sensitivity to topological correlations and may change which approximation errors matter most. Comparing emulated and direct analyses as these effects are included would help establish where emulation is sufficient and where direct calculations are still needed. If the covariance itself is emulated, its parametrization must preserve Hermitian symmetry and positive definiteness. The relevant test is whether the resulting likelihood reproduces the parameter constraints, rather than agreement between individual covariance elements alone.</dd>
    <dt>What polarization adds</dt>
    <dd>I am also interested in what polarization can tell us that temperature alone cannot. My likelihood-ratio framework allows this comparison in terms of detection probabilities and parameter recovery, while accounting for false detections introduced by searching over many models. Applying the same search to simulations of the simply connected model would establish detection thresholds; simulations with non-trivial topology would then show how often a signal is detected and how well its parameters are recovered. Comparing temperature and polarization at the same false-positive rate would reveal whether polarization makes a signature easier to detect, helps locate its parameters, or both. Building on my work with LiteBIRD, I would extend these forecasts to future observations, including the effects of sky coverage, noise, and foreground uncertainty.</dd>
    <dt>Proposed first-year deliverable</dt>
    <dd>The completed Planck PR4 topology analysis, with an emulated likelihood checked against direct calculations on the models and angular resolutions where those remain feasible, and detection thresholds set by applying the same search to simulations of the simply connected model.</dd>
    <dt>What I bring</dt>
    <dd>Spin-2 eigenmodes and CMB covariance matrices for compact Euclidean manifolds (JCAP 08 (2025) 015) and the parity-odd signatures of topology (JCAP 11 (2024) 020); CMBtopology for GPU computation of large covariance matrices; the Planck PR4 topology pipeline and the LiteBIRD forecasting pipeline, both in development; the likelihood-ratio framework for detection probabilities and parameter recovery (arXiv:2610.17186); and current work on neural likelihood emulators validated against conventional Bayesian methods.</dd>
  </dl>
</section>

<section class="direction" aria-labelledby="dir-b">
  <p class="direction__label">Direction B</p>
  <h3 id="dir-b">Validated simulation-based inference and calibrated forecasts beyond topology</h3>
  <dl class="facts">
    <dt>Motivation</dt>
    <dd>The same questions arise well beyond cosmic topology. An accurate prediction of an observable does not by itself establish that the inferred constraints are reliable: a narrow posterior may reflect information in the data, restrictive simulation assumptions, or errors in a learned approximation. Likewise, a forecast based on the KL divergence alone does not say how often a search will detect a signal or recover its parameters, so it needs to account for the analysis that will actually be performed.</dd>
    <dt>Proposed first-year deliverable</dt>
    <dd>Inference from summary statistics, for example in large-scale structure, in a setting where a reference analysis fixes the accuracy an approximation must reach: an amortized neural method compared with conventional Bayesian inference and accepted only after passing calibration and coverage tests, followed by a focused extension toward inference of the underlying field and cosmological parameters.</dd>
    <dt>What I bring</dt>
    <dd>Exact sampling distributions of test statistics, and a likelihood-ratio framework already applied to primordial tensor modes and dark energy as well as topology (arXiv:2610.17186); experience comparing learned classifiers of simulated CMB maps with a directly evaluable likelihood (JCAP 09 (2024) 057); GPU/HPC pipelines; and an ongoing project on whether Koopman-operator methods can reduce the cost of diffusion-based posterior estimation without distorting the inferred distribution.</dd>
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
