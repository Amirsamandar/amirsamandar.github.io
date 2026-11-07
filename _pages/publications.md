---
title: "Publications"
permalink: /publications/
description: "Publications of Amirhossein Samandar in cosmic topology, CMB statistics, likelihood-ratio detectability and Bayesian evaluation of language models, with author position and individual contribution for each paper."
---
{%- assign pubs = site.publications | sort: "date" | reverse -%}
{%- assign published = pubs | where: "status", "published" -%}
{%- assign accepted = pubs | where: "status", "accepted" -%}
{%- assign preprints = pubs | where: "status", "preprint" -%}
{%- assign prep = pubs | where: "status", "prep" -%}
<div markdown="0">
<div class="wrap">
  <div class="pub-intro">
    <p class="lede">{% include pub-counts.html %}. Each entry gives my position in the author list and, separately, what I contributed.</p>
    <p>COMPACT Collaboration author lists are ordered first by contribution, then alphabetically. Long author lists are abbreviated; full lists are on arXiv, the journal page and INSPIRE-HEP.</p>
    {% include metrics-board.html %}
    <nav class="toc toc--inline" aria-label="Sections">
      <ul>
        <li><a href="#published">Published ({{ published.size }})</a></li>
        <li><a href="#accepted">Accepted ({{ accepted.size }})</a></li>
        <li><a href="#preprints">Preprints ({{ preprints.size }})</a></li>
        <li><a href="#in-preparation">In preparation ({{ prep.size }})</a></li>
        <li><a href="#software">Software</a></li>
      </ul>
    </nav>
  </div>

  <section class="pub-group" aria-labelledby="published">
    <h2 id="published" class="section__title">Published</h2>
    <ol class="pubs">{% for p in published %}{% include pub-card.html pub=p %}{% endfor %}</ol>
  </section>

  <section class="pub-group" aria-labelledby="accepted">
    <h2 id="accepted" class="section__title">Accepted</h2>
    <ol class="pubs">{% for p in accepted %}{% include pub-card.html pub=p %}{% endfor %}</ol>
  </section>

  <section class="pub-group" aria-labelledby="preprints">
    <h2 id="preprints" class="section__title">Preprints</h2>
    <p class="section__intro">Posted on arXiv; journal status is shown where known.{% include todo.html note="confirm which preprints are under journal review (currently only Part IIc is marked, per the brief) and where" %}</p>
    <ol class="pubs">{% for p in preprints %}{% include pub-card.html pub=p %}{% endfor %}</ol>
  </section>

  <section class="pub-group" aria-labelledby="in-preparation">
    <h2 id="in-preparation" class="section__title">In preparation</h2>
    <p class="section__intro">Not counted in the totals above.</p>
    <ol class="pubs">{% for p in prep %}{% include pub-card.html pub=p %}{% endfor %}</ol>
  </section>

  <section class="pub-group" aria-labelledby="software">
    <h2 id="software" class="section__title">Software</h2>
    <ul class="pubs">
      {%- for s in site.data.software %}
      <li class="pub">
        <h3 class="pub__title"><a href="{{ s.url }}">{{ s.name }}</a></h3>
        <p class="pub__authors">{% include authors.html authors=s.authors %}</p>
        <p class="pub__venue">{{ s.version }} · {{ s.stack }}</p>
        <p class="pub__summary">{{ s.description }}</p>
        <p class="pub__contrib"><span class="pub__label">My contribution:</span> {{ s.role }}</p>
      </li>
      {%- endfor %}
    </ul>
  </section>
</div>
</div>
