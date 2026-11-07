---
title: "Curriculum vitae"
permalink: /cv/
description: "CV of Amirhossein Samandar, Ph.D. candidate in Physics at Case Western Reserve University (expected January 2027): education, research, publications, software, teaching, talks, awards and references."
redirect_from:
  - /resume
---
{%- assign profile = site.data.profile -%}
{%- assign r = site.data.research -%}
{%- assign firsts = site.publications | where: "position", 1 -%}
<div markdown="0">
<div class="wrap">

<div class="cv-top">
  <p class="lede">{{ profile.role }}, {{ profile.institution }}. Ph.D. expected {{ profile.phd_expected_long | replace: " (expected)", "" }}. {{ profile.availability }}.</p>
  <p><a class="btn btn--primary" href="{{ profile.cv_pdf | relative_url }}">Download full CV <span class="btn__meta">PDF</span></a></p>
  <p class="muted">This page summarizes the PDF CV. If the two ever differ, the PDF is the reference version.</p>
</div>

<section class="cv-section" aria-labelledby="cv-education">
  <h2 id="cv-education" class="section__title">Education</h2>
  <dl class="cv">
    <dt>{{ profile.phd_start }} – {{ profile.phd_expected_long }}</dt>
    <dd><strong>Ph.D. in Physics</strong>, Case Western Reserve University, Cleveland, Ohio, USA.<br>
    Direct Ph.D. from the B.Sc., to be completed in about 3.5 years. Advisor: {{ profile.advisor }}; co-advisor: {{ profile.coadvisor }}. GPA 3.7/4.0.</dd>
    <dt>2018 – 2023</dt>
    <dd><strong>B.Sc. in Physics</strong>, Sharif University of Technology, Tehran, Iran. GPA 18.85/20; rank 4 of 56.</dd>
  </dl>
</section>

<section class="cv-section" aria-labelledby="cv-pubs">
  <h2 id="cv-pubs" class="section__title">Publication summary</h2>
  <ul class="plain-list">
    <li>{% include pub-counts.html %}. {% include metrics.html %}</li>
    <li>First author on {{ firsts | where: "status", "published" | size }} published papers (Parts IIIa and IIIb, JCAP) and on preprint arXiv:2610.17186; second author with a lead contribution on Part IIb (JCAP) and on Don't Pass@k (ICLR 2026).</li>
    <li>Co-author of the COMPACT Collaboration review “The topology of the Universe” (Nature Astronomy, 2026).</li>
  </ul>
  <p class="section-more"><a href="{{ '/publications/' | relative_url }}">Full publication list with individual contributions</a></p>
</section>

<section class="cv-section" aria-labelledby="cv-research">
  <h2 id="cv-research" class="section__title">Research</h2>
  <dl class="cv">
    {%- for p in r.projects %}
    <dt>{{ p.dates }}</dt>
    <dd><a href="{{ '/research/' | relative_url }}#{{ p.id }}"><strong>{{ p.title }}</strong></a> · {{ p.role }} · <span class="muted">{{ p.status }}</span><br>{{ p.lead }}</dd>
    {%- endfor %}
    <dt>{{ r.earlier.dates }}</dt>
    <dd><strong>Scalar-field models and cosmological perturbation theory</strong>, {{ r.earlier.place }}.</dd>
  </dl>
</section>

<section class="cv-section" aria-labelledby="cv-software">
  <h2 id="cv-software" class="section__title">Software</h2>
  <dl class="cv">
    {%- for s in site.data.software %}
    <dt><a href="{{ s.url }}">{{ s.name }}</a></dt>
    <dd>{{ s.description }} {{ s.role }}</dd>
    {%- endfor %}
  </dl>
</section>

<section class="cv-section" aria-labelledby="cv-collab">
  <h2 id="cv-collab" class="section__title">Collaborations</h2>
  <dl class="cv">
    <dt>COMPACT</dt>
    <dd>Cosmic topology collaboration: CWRU, Pittsburgh, Imperial College London, IFT Madrid, INFN Padova.</dd>
    <dt>LiteBIRD</dt>
    <dd>Adjoint member; developing a forecasting pipeline to constrain cosmic topology using high-fidelity E-mode polarization data alongside temperature data.</dd>
  </dl>
</section>

<section class="cv-section" aria-labelledby="cv-methods">
  <h2 id="cv-methods" class="section__title">Methods and computation</h2>
  <dl class="cv">
    {%- for m in r.methods %}
    <dt>{{ m.group }}</dt><dd>{{ m.items }}</dd>
    {%- endfor %}
    <dt>Languages</dt><dd>Persian (native), English (fluent)</dd>
  </dl>
</section>

<section class="cv-section" aria-labelledby="cv-mentoring">
  <h2 id="cv-mentoring" class="section__title">Mentoring and teaching</h2>
  <dl class="cv">
    <dt>{% if profile.mentoring.since != "" %}{{ profile.mentoring.since }} – present{% else %}Current{% endif %}</dt>
    <dd><strong>Undergraduate research mentor</strong>, Case Western Reserve University. Mentoring{% if profile.mentoring.count != "" %} {{ profile.mentoring.count }}{% endif %} undergraduate researchers one-on-one on the underlying physics, computational methods, and the interpretation and validation of numerical results.{% include todo.html note="confirm count (brief: seven; CV: several) and start date (brief: 2025; CV: May 2026); add the outcome of the student manuscript previously expected by end of Sept 2026, if any" %}</dd>
    <dt>Spring 2025</dt>
    <dd>Computational Methods in Physics, CWRU.</dd>
    <dt>Fall 2023 – Fall 2024</dt>
    <dd>General Physics Lab, CWRU.</dd>
    <dt>2020 – 2021</dt>
    <dd>Cosmology; Special Relativity; Electrodynamics I and II, Sharif University of Technology.</dd>
  </dl>
</section>

<section class="cv-section" aria-labelledby="cv-talks">
  <h2 id="cv-talks" class="section__title">Talks and conferences</h2>
  <dl class="cv">
    {%- assign talks = site.talks | sort: "date" | reverse -%}
    {%- for t in talks %}
    {%- if t.pending != true or site.show_todos %}
    <dt>{{ t.year }}</dt>
    <dd>{% if t.pending %}{{ t.venue }}.{% else %}“{{ t.title }},” {{ t.venue }} ({{ t.type | downcase }}).{% endif %}{% include todo.html note=t.todo %}</dd>
    {%- endif %}
    {%- endfor %}
  </dl>
</section>

<section class="cv-section" aria-labelledby="cv-awards">
  <h2 id="cv-awards" class="section__title">Awards</h2>
  <ul class="plain-list">
    <li>Art Walker Award for Outstanding Service, Department of Physics, Case Western Reserve University (2026).</li>
    <li>Full graduate funding (Ph.D. in Physics), Case Western Reserve University.</li>
    <li>Iran National University Entrance Exams: ranked 20th of 20,000 (M.Sc.) and 420th of 150,000 (undergraduate, top 0.5%).</li>
  </ul>
</section>

<section class="cv-section" aria-labelledby="cv-refs">
  <h2 id="cv-refs" class="section__title">References</h2>
  <ul class="plain-list">
    <li><strong>Glenn D. Starkman</strong>, Case Western Reserve University (Ph.D. advisor)</li>
    <li><strong>Craig J. Copi</strong>, Case Western Reserve University (Ph.D. co-advisor)</li>
    <li><strong>Andrew H. Jaffe</strong>, Imperial College London (COMPACT)</li>
    <li><strong>Yashar Akrami</strong>, IFT UAM-CSIC, Madrid (COMPACT)</li>
    <li><strong>Michael Hinczewski</strong>, Case Western Reserve University (machine learning)</li>
  </ul>
  <p class="muted">Contact details are in the PDF CV or available on request.{% include todo.html note="the PDF CV lists three referees (Starkman, Jaffe, Akrami); the brief lists five. Confirm all five have agreed to be listed." %}</p>
</section>

</div>
</div>
