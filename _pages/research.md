---
title: "Research"
permalink: /research/
description: "Research projects of Amirhossein Samandar: likelihood-ratio detectability, CMB covariances for cosmic topology, simulation-based inference (planned), and calibrated evaluation of language models."
lede: "Each project is stated as a problem, my contribution, the result and its current status. Completed work and planned directions are labeled separately."
---
{%- assign r = site.data.research -%}
<div markdown="0">

<nav class="wrap toc" aria-label="Projects on this page">
  <ul>
    {%- for p in r.projects %}
    <li><a href="#{{ p.id }}">{{ p.title }}</a></li>
    {%- endfor %}
    <li><a href="#earlier">Earlier research</a></li>
    <li><a href="#methods">Methods</a></li>
  </ul>
</nav>

<div class="wrap">
{%- for p in r.projects %}
<article class="project" id="{{ p.id }}" aria-labelledby="{{ p.id }}-title">
  <header class="project__head">
    <p class="project__status project__status--{{ p.status_kind }}">{{ p.status }}</p>
    <h2 id="{{ p.id }}-title" class="project__title">{{ p.title }}</h2>
    <p class="project__meta"><span>{{ p.dates }}{% include todo.html note=p.dates_todo %}</span><span>{{ p.role }}</span><span>{{ p.affiliation }}</span></p>
    <p class="project__lead">{{ p.lead }}</p>
  </header>
  <dl class="facts">
    <dt>Problem</dt><dd>{{ p.problem }}</dd>
    <dt>Contribution</dt><dd>{{ p.contribution }}</dd>
    <dt>Result</dt><dd>{{ p.result }}{% include todo.html note=p.optional_todo %}</dd>
    <dt>Status</dt><dd>{{ p.status }}{% if p.papers %}: {% for l in p.papers %}<a href="{{ l.url }}">{{ l.label }}</a>{% unless forloop.last %} · {% endunless %}{% endfor %}{% endif %}</dd>
  </dl>
</article>
{%- endfor %}

<article class="project" id="earlier" aria-labelledby="earlier-title">
  <header class="project__head">
    <p class="project__status project__status--done">Completed</p>
    <h2 id="earlier-title" class="project__title">Earlier research</h2>
    <p class="project__meta"><span>{{ r.earlier.dates }}</span><span>{{ r.earlier.place }}</span></p>
  </header>
  <ul class="plain-list">
    {%- for i in r.earlier.items %}<li>{{ i }}</li>{% endfor %}
  </ul>
</article>

<section class="project" id="methods" aria-labelledby="methods-title">
  <h2 id="methods-title" class="project__title">Methods</h2>
  <dl class="facts facts--wide">
    {%- for m in r.methods %}
    <dt>{{ m.group }}</dt><dd>{{ m.items }}</dd>
    {%- endfor %}
  </dl>
</section>

<section class="project" aria-labelledby="collab-title">
  <h2 id="collab-title" class="project__title">Collaborations</h2>
  <dl class="facts facts--wide">
    <dt>COMPACT</dt><dd>Cosmic topology collaboration: CWRU, Pittsburgh, Imperial College London, IFT Madrid, INFN Padova. Author lists are ordered first by contribution, then alphabetically.</dd>
    <dt>LiteBIRD</dt><dd>CMB B-mode polarization satellite. Adjoint member, developing a forecasting pipeline to constrain cosmic topology using high-fidelity E-mode polarization alongside temperature.</dd>
  </dl>
  <p class="section-more"><a href="{{ '/research-plan/' | relative_url }}">Where this goes next: research directions, 2027 onward</a></p>
</section>
</div>

</div>
