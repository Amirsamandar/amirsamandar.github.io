---
title: "Sitemap"
permalink: /sitemap/
description: "All pages on amirsamandar.github.io."
---
<div markdown="0">
<div class="wrap prose">
<h2>Pages</h2>
<ul>
  <li><a href="{{ '/' | relative_url }}">Home</a></li>
  {%- for l in site.data.navigation.main %}<li><a href="{{ l.url | relative_url }}">{{ l.title }}</a></li>{% endfor %}
  {%- for l in site.data.navigation.footer %}{% if l.url != "/sitemap/" %}<li><a href="{{ l.url | relative_url }}">{{ l.title }}</a></li>{% endif %}{% endfor %}
</ul>
<h2>Publications</h2>
<ul>
  {%- assign pubs = site.publications | sort: "date" | reverse -%}
  {%- for p in pubs %}{% if p.status != "prep" %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>{% endif %}{% endfor %}
</ul>
<h2>Talks</h2>
<ul>
  {%- assign talks = site.talks | sort: "date" | reverse -%}
  {%- for t in talks %}{% unless t.pending %}<li><a href="{{ t.url | relative_url }}">{{ t.title }} ({{ t.year }})</a></li>{% endunless %}{% endfor %}
</ul>
<p>Machine-readable version: <a href="{{ '/sitemap.xml' | relative_url }}">sitemap.xml</a>.</p>
</div>
</div>
