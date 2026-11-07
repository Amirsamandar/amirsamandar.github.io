---
permalink: /
title: "Amirhossein Samandar"
description: "Amirhossein Samandar, Ph.D. candidate in physics at Case Western Reserve University: likelihood-ratio detectability for cosmological models, CMB statistics and cosmic topology, and calibrated evaluation of machine-learning models. Seeking postdoctoral positions starting 2027."
hide_title: true
body_class: home
redirect_from:
  - /about/
  - /about.html
---
{%- assign profile = site.data.profile -%}
{%- assign home = site.data.home -%}
<div markdown="0">

<section class="hero wrap" aria-labelledby="hero-name">
  <div class="hero__text">
    <h1 id="hero-name" class="hero__name">{{ profile.name }}</h1>
    <p class="hero__role">{{ profile.role }}, {{ profile.institution }}</p>
    <p class="hero__headline">{{ home.headline }}</p>
    <p class="hero__positioning">{{ home.positioning }}</p>
    <p class="hero__availability"><span class="dot" aria-hidden="true"></span>{{ profile.availability }}. Ph.D. expected {{ profile.phd_expected }}.</p>
    <ul class="actions" aria-label="Key documents and contact">
      <li><a class="btn btn--primary" href="{{ profile.cv_pdf | relative_url }}">CV <span class="btn__meta">PDF</span></a></li>
      {%- if profile.statement_available %}
      <li><a class="btn" href="{{ profile.statement_pdf | relative_url }}">Research statement <span class="btn__meta">PDF</span></a></li>
      {%- else %}
      <li><a class="btn" href="{{ '/research-plan/#research-statement' | relative_url }}">Research statement</a></li>
      {%- endif %}
      <li><a class="btn" href="{{ '/publications/' | relative_url }}">Publications</a></li>
      <li><a class="btn" href="mailto:{{ profile.email }}">Email</a></li>
    </ul>
    {% include metrics-board.html %}
    {%- unless profile.statement_available %}{% include todo.html note="research statement PDF not yet in /files/; set statement_available: true in _data/profile.yml to show the download button" %}{% endunless %}
  </div>
  <aside class="profile-card" aria-labelledby="side-contact">
    <img class="profile-card__photo" src="{{ profile.portrait | relative_url }}" alt="{{ profile.portrait_alt }}" width="640" height="640">
    <div class="profile-card__body">
      <h2 id="side-contact" class="side__h">Contact</h2>
      <ul class="contact-list">
        <li>
          <svg class="icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>
          <a href="mailto:{{ profile.email }}">{{ profile.email | replace: "@", "@<wbr>" }}</a>
        </li>
        <li>
          <svg class="icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6"/></svg>
          <span>{{ profile.department }}<br>{{ profile.institution }}</span>
        </li>
        <li>
          <svg class="icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M12 21s-6.5-6.2-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21z"/><circle cx="12" cy="9.8" r="2.3"/></svg>
          <span>{{ profile.location }}</span>
        </li>
      </ul>
    </div>
    <div class="profile-card__links">
      <h2 class="side__h">Profiles</h2>
      <ul class="chips">
        {%- for l in profile.links %}
        <li><a class="chip" href="{{ l.url }}" rel="me">{{ l.name }}<span class="chip__arrow" aria-hidden="true">↗</span></a></li>
        {%- endfor %}
      </ul>
    </div>
  </aside>
</section>

<section class="section wrap" aria-labelledby="question">
  <h2 id="question" class="section__title">{{ home.question_title }}</h2>
  <p class="question">{{ home.question }}</p>
</section>

<section class="section wrap" aria-labelledby="results">
  <h2 id="results" class="section__title">Headline results</h2>
  <ul class="cards cards--2">
    {%- for r in home.results %}
    <li class="card result">
      <p class="card__kicker">{{ r.kicker }}</p>
      <p class="result__claim">{{ r.claim }}</p>
      <p class="card__link"><a href="{{ r.url }}">{{ r.link_label }}</a></p>
    </li>
    {%- endfor %}
  </ul>
</section>

<section class="section wrap" aria-labelledby="selected">
  <h2 id="selected" class="section__title">{{ home.selected_title }}</h2>
  <ol class="pubs pubs--compact">
    {%- for i in (1..5) %}
    {%- for p in site.publications %}
    {%- if p.selected == i %}
    {% include pub-card.html pub=p compact=true %}
    {%- endif %}
    {%- endfor %}
    {%- endfor %}
  </ol>
  <p class="section-more"><a href="{{ '/publications/' | relative_url }}">All publications ({% include pub-counts.html %})</a></p>
</section>

<section class="section wrap" aria-labelledby="themes">
  <h2 id="themes" class="section__title">{{ home.themes_title }}</h2>
  <p class="section__intro">{{ site.data.research.themes_intro }}</p>
  <ol class="themes">
    {%- for t in site.data.research.themes %}
    <li class="theme{% if t.planned %} theme--planned{% endif %}">
      <span class="theme__numeral" aria-hidden="true">{{ t.numeral }}</span>
      <h3 class="theme__title"><a href="{{ t.link | relative_url }}">{{ t.title }}</a></h3>
      <p>{{ t.text }}</p>
    </li>
    {%- endfor %}
  </ol>
</section>

<section class="section wrap" aria-labelledby="software">
  <h2 id="software" class="section__title">{{ home.software_title }}</h2>
  <ul class="cards cards--2">
    {%- for s in site.data.software %}
    <li class="card soft">
      <h3 class="card__title"><a href="{{ s.url }}">{{ s.name }}</a></h3>
      <p>{{ s.blurb | default: s.description }}</p>
      <p class="card__meta"><span class="pub__label">My role:</span> {{ s.role }}</p>
      <p class="card__meta muted">{{ s.stack }} · {{ s.version }}</p>
    </li>
    {%- endfor %}
  </ul>
</section>

<section class="section wrap" aria-labelledby="news">
  <h2 id="news" class="section__title">{{ home.news_title }}</h2>
  {% include news-list.html limit=home.news_limit %}
  <p class="section-more"><a href="{{ '/news/' | relative_url }}">All news</a></p>
</section>

<section class="strip" aria-labelledby="collab">
  <div class="wrap">
    <h2 id="collab" class="section__title">Collaborations and service</h2>
    <ul class="strip__list">
      <li><strong>COMPACT</strong> Collaboration member (cosmic topology).</li>
      <li><strong>LiteBIRD</strong> adjoint member: topology forecasts using E-mode polarization with temperature.</li>
      <li><strong>Mentoring</strong>{% if profile.mentoring.count != "" %} {{ profile.mentoring.count }}{% endif %} undergraduate researchers one-on-one{% if profile.mentoring.since != "" %} since {{ profile.mentoring.since }}{% endif %}.{% include todo.html note="confirm mentoring count and start date: brief says seven, 2025–present; CV says several, May 2026–present" %}</li>
      <li><strong>Art Walker Award</strong> for Outstanding Service, CWRU Physics (2026). References available on request.</li>
    </ul>
  </div>
</section>

</div>
