---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
* Ph.D. in Physics (Mastering out in Fall 2025), Case Western Reserve University, Cleveland, Ohio, USA, Aug 2023–present
  * Advisors: Glenn D. Starkman, Craig J. Copi
* B.Sc. in Physics, GPA: 18.85/20 (Rank: 4/56), Sharif University of Technology, Tehran, Iran, 2018–2023

Research Experience
======
* A Novel Bayesian Evaluation Approach in LLMs, June 2025 – Oct 2025
  * Developing a novel Bayesian evaluation framework for LLMs.
  * Designed the method to be more robust and accurate, especially with fewer trials, reducing computational costs for benchmarking sampling decodings and LLM models.
  * Bayes-Kit: A published Bayesian evaluation toolkit for large language models.
    * Implements Python and Julia packages for uncertainty-aware evaluation of sampling decodings.
    * Open-source and publicly available at https://github.com/Amirsamandar/bayes-kit.
  * Related Publication: arXiv:2510.04265 [cs.AI]

* Bayesian Analysis for the Planck CMB Data, May 2025 – Present
  * Applied Bayesian likelihood analysis to constrain cosmic topology using Planck PR4 temperature data, improving constraints from 2013/2015 Planck topology studies.
  * Exploring hierarchical Bayesian methods, training variational autoencoders as emulators for likelihood functions, and developing efficient GPU-parallelized code for computing CMB covariance matrices.

* Large Language Model Optimization Projects, June 2025 – Present
  * Contributed to an anonymous ACL submission (non-author) on asymmetric KV-cache quantization for LLMs, prioritizing bit allocation for keys over values based on norm disparities to enhance inference efficiency on resource-constrained hardware.
  * Contributed to the development of lossless compression techniques (non-author) using Huffman coding, achieving 30% model size reduction with bit-for-bit identical outputs (arXiv:2504.11651).
  * Extending compression methods for more efficient GPU algorithms and planning to apply a Bayesian framework to evaluate quantization techniques, including dynamic approaches, to inform large-scale training pipeline optimizations (forthcoming paper as author).

* Benchmarking Reasoning Capabilities in Large Language Models, April 2025 – Present
  * Developed ReasoningBench, a benchmark for systematically assessing a diverse range of reasoning LLMs, including foundation models, supervised fine-tuned variants, reinforcement learning-based models, and merged hybrid systems.
  * Evaluated models across tasks in math, science, instruction-following (IFEval), and code generation.
  * Employed diverse sampling strategies to evaluate both final answers and the structure of intermediate reasoning; examined how inference-time scaling and post-training techniques impact reasoning performance.
  * Related Publication: under preparation for submission to Transactions on Machine Learning Research (TMLR).

* Machine Learning for Cosmic Topology Classification, Jan 2024 – Present
  * Applied classical machine learning and neural networks to classify non-trivial Universe topologies using CMB simulated data.
  * Developed machine learning alternatives to likelihood-based methods for faster data analysis.
  * Related Publication: arXiv:2404.01236 [astro-ph.CO]

* Cosmic Topology Research, Aug 2023 – Present
  * Exploring the signatures of non-trivial topology in CMB anisotropies by computing the CMB temperature and polarization correlation functions.
  * TopologyPy: A Python-based HPC package designed to compute CMB covariance matrices for ten compact Euclidean topologies, with ongoing development of a likelihood analysis extension.
  * Related Publications: arXiv:2407.09400, 2503.08671, 2510.05030, 2409.02226 [astro-ph.CO]

* Quantum Cosmology, Jan 2022 – Feb 2023, Institute for Research in Fundamental Sciences (IPM), Supervisor: Mohammad Hossein Namjoo
  * Studied complex scalar fields as dark matter candidates in the non-relativistic limit using effective field theory and iterative calculations.
  * Developed canonical transformations for non-relativistic fields and analyzed pressure and energy density in multi-field axion dark matter models.

* Quantum Cosmology, Institute for Research in Fundamental Sciences (IPM), Supervisor: Hassan Firouzjahi
  * Explored cosmological perturbation theory, inflation, and non-Gaussian features of primordial fluctuations.
  * Utilized xAct Mathematica package and in-in formalism, referencing Juan Maldacena’s work.

Skills
======
* Programming Languages: Python, Mathematica, Julia, C
* AI/ML Tools: PyTorch, scikit-learn, Ray, Google JAX
* Libraries and Tools: Pandas, NumPy, Numba, JAX, Mathematica, LaTeX
* Computational Skills: Advanced numerical methods, High-Performance Computing (HPC), Parallel computing, Convergence studies
* Languages: Persian (native), English (fluent)

Publications
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Talks
======
  <ul>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html %}
  {% endfor %}</ul>
  
Teaching
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>

Selected Courses
======
* ML in Physics
* Computational Methods in Physics
* Modern Statistical Physics
* Statistical Physics & AI
* High Performance Computing
* Quantum Computation
* Quantum Cosmology
* Group Theory
* Quantum Field Theory

Achievements
======
* Ranked 20th among 20,000 candidates in Iran’s National University Exam for Master’s Studies.
* Top 0.5% ranking (420th out of 150,000 candidates) in National University Entrance Exam for Undergraduate Studies.

Interests
======
* Geopolitics
* History
* Social Science
* Hiking
* Classical music
* Anthropology

References
======
* Glenn D. Starkman, Distinguished Professor and Vice-Chair, Department of Physics, CWRU, email: glenn.starkman@case.edu
* Michael Hinczewski, Professor of Biophysics and Statistics, Department of Physics, CWRU, email: michael.hinczewski@case.edu
* Craig J. Copi, Professor, Department of Physics, CWRU, email: craig.copi@case.edu
* Yashar Akrami, Assistant Research Professor, Institute for Theoretical Physics (IFT) UAM-CSIC in Madrid, email: yashar.akrami@csic.es
