---
title: "Citations"
permalink: /citations/
description: "Papers citing the work of Amirhossein Samandar, collected from INSPIRE-HEP, NASA ADS, Semantic Scholar, OpenAlex and Google Scholar and merged so each citing paper is listed once."
---
{%- assign cd = site.data.citations -%}
{%- assign papers = cd.papers | reverse -%}
<div markdown="0">
<div class="wrap">
  <div class="pub-intro">
    <p class="lede">Every paper I could find that cites my work, collected from INSPIRE-HEP, NASA ADS, Semantic Scholar, OpenAlex and Google Scholar. A paper found by several databases is listed once.</p>
  </div>

  {%- if cd.citing.size == 0 %}
  <p class="notice-empty">Citation data has not been collected yet. It is gathered automatically by the <em>Update citations</em> workflow and appears here after its first run.</p>
  {%- else %}
  <section class="board" aria-labelledby="cite-board-title">
    <h2 id="cite-board-title" class="visually-hidden">Citation totals</h2>
    <dl class="board__stats">
      <div class="board__stat"><dt>Citing papers</dt><dd>{{ cd.summary.citing_papers }}</dd></div>
      <div class="board__stat"><dt>Citations</dt><dd>{{ cd.summary.citations }}</dd></div>
      <div class="board__stat"><dt>Excluding self-citations</dt><dd>{{ cd.summary.citations_noself }}</dd></div>
      <div class="board__stat"><dt>h-index</dt><dd>{{ cd.summary.h_index }}</dd></div>
    </dl>
    <p class="board__source">All databases combined and deduplicated · updated {{ cd.updated | date: "%-d %B %Y" }}</p>
  </section>
  <p class="section__intro">A citing paper that cites two of my papers is one citing paper but two citations. Self-citations follow INSPIRE-HEP's definition: the citing paper shares at least one author with the cited paper.</p>
  <p class="section__intro">Every citation is checked. Where the citing paper is on arXiv, its own bibliography is searched for my paper ({{ cd.summary.verified }} of {{ cd.summary.citations }} confirmed this way, marked &#10003;). The rest are counted only if INSPIRE-HEP or at least two databases agree.{% if cd.summary.unconfirmed > 0 or cd.summary.rejected > 0 %} Matches that could not be confirmed are <a href="#unconfirmed">listed separately</a> and not counted.{% endif %}</p>

  <section class="pub-group" aria-labelledby="by-paper">
    <h2 id="by-paper" class="section__title">By publication</h2>
    <p class="section__intro">“Combined” counts each citing paper once across all databases. The other columns are each database's own count, which can differ because each indexes different sources.</p>
    <div class="table-scroll" tabindex="0" role="region" aria-labelledby="by-paper">
    <table class="cite-table">
      <thead>
        <tr>
          <th scope="col">Publication</th>
          <th scope="col" class="num">Combined</th>
          <th scope="col" class="num">Excl. self</th>
          {%- for s in cd.sources %}{% unless s.status == "skipped" and s.links == 0 %}
          <th scope="col" class="num">{{ s.name | replace: "Semantic Scholar", "Sem. Scholar" | replace: "Google Scholar", "G. Scholar" }}</th>
          {%- endunless %}{% endfor %}
        </tr>
      </thead>
      <tbody>
        {%- for p in papers %}
        <tr>
          <th scope="row"><a href="{{ '/publication/' | append: p.slug | relative_url }}">{{ p.short }}</a></th>
          <td class="num">{% if p.total > 0 %}<a href="?paper={{ p.slug }}#citing" aria-label="Show the {{ p.total }} papers citing {{ p.short | escape }}">{{ p.total }}</a>{% else %}0{% endif %}</td>
          <td class="num">{{ p.total_noself }}</td>
          {%- for s in cd.sources %}{% unless s.status == "skipped" and s.links == 0 %}
          {%- assign n = p.counts[s.id] -%}
          <td class="num">{% if n == nil %}<span class="muted" aria-label="not available">–</span>{% else %}{{ n }}{% endif %}</td>
          {%- endunless %}{% endfor %}
        </tr>
        {%- endfor %}
      </tbody>
    </table>
    </div>
    <ul class="src-status">
      {%- for s in cd.sources %}
      <li><span class="pub__label">{{ s.name }}:</span>
        {%- case s.status -%}
          {%- when "ok" %} updated {{ s.as_of | date: "%-d %b %Y" }}
          {%- when "skipped" %} <span class="muted">not connected ({{ s.note }})</span>
          {%- else %} {% if s.as_of != "" %}data from {{ s.as_of | date: "%-d %b %Y" }}{% endif %} <span class="muted">({{ s.note }})</span>
        {%- endcase -%}
        {%- if s.status == "ok" and s.note != "" %} <span class="muted">({{ s.note }})</span>{% endif -%}
      </li>
      {%- endfor %}
    </ul>
  </section>

  <section class="pub-group" aria-labelledby="citing">
    <h2 id="citing" class="section__title">Citing papers</h2>
    <form class="cite-filters" id="cite-filters" hidden role="search" aria-label="Filter citing papers" onsubmit="return false">
      <label>Cited paper
        <select id="cf-paper">
          <option value="">All publications</option>
          {%- for p in papers %}{% if p.total > 0 %}
          <option value="{{ p.slug }}">{{ p.short }} ({{ p.total }})</option>
          {%- endif %}{% endfor %}
        </select>
      </label>
      <label>Found in
        <select id="cf-source">
          <option value="">Any database</option>
          {%- for s in cd.sources %}{% if s.links > 0 %}
          <option value="{{ s.id }}">{{ s.name }}</option>
          {%- endif %}{% endfor %}
        </select>
      </label>
      <label>Search
        <input type="search" id="cf-q" placeholder="Title, author, journal">
      </label>
      <label class="check"><input type="checkbox" id="cf-noself"> Exclude self-citations</label>
    </form>
    <p class="cite-count" id="cf-count" aria-live="polite">{{ cd.citing.size }} citing papers, newest first.</p>
    <ol class="cites" id="citing-list">
      {%- for c in cd.citing %}{% include citing-item.html c=c %}{% endfor %}
    </ol>
  </section>

  {%- if cd.unconfirmed.size > 0 or cd.rejected.size > 0 %}
  <section class="pub-group" aria-labelledby="unconfirmed">
    <h2 id="unconfirmed" class="section__title">Not counted</h2>
    <p class="section__intro">Database matches that are not included in the totals above.</p>
    {%- if cd.unconfirmed.size > 0 %}
    <details class="pub__bib">
      <summary>Unconfirmed ({{ cd.unconfirmed.size }})</summary>
      <p class="section__intro">Found by only one database, and the citing paper's reference list could not be checked (not on arXiv). They may be correct.</p>
      <ol class="cites">{% for c in cd.unconfirmed %}{% include citing-item.html c=c status="unconfirmed" %}{% endfor %}</ol>
    </details>
    {%- endif %}
    {%- if cd.rejected.size > 0 %}
    <details class="pub__bib">
      <summary>Rejected ({{ cd.rejected.size }})</summary>
      <p class="section__intro">A database linked these, but the citing paper's own reference list does not contain my paper.</p>
      <ol class="cites">{% for c in cd.rejected %}{% include citing-item.html c=c status="rejected" %}{% endfor %}</ol>
    </details>
    {%- endif %}
  </section>
  {%- endif %}
  {%- endif %}
</div>
</div>
<script src="{{ '/assets/js/citations.js' | relative_url }}" defer></script>
