---
title: "Talks"
permalink: /talks/
description: "Conference talks, workshop talks and invited seminars by Amirhossein Samandar."
lede: "Conference and workshop talks and invited seminars, most recent first."
---
{%- assign talks = site.talks | sort: "date" | reverse -%}
<div markdown="0">
<div class="wrap">
  <ol class="talks">
    {%- for t in talks %}
    {%- if t.pending != true or site.show_todos %}
    <li class="talk">
      <span class="talk__year">{{ t.year }}</span>
      <div>
        <h2 class="talk__title"><a href="{{ t.url | relative_url }}">{{ t.title }}</a></h2>
        <p class="talk__meta">{{ t.type }} · {{ t.venue }}{% if t.location and t.location != "" %} · {{ t.location }}{% endif %}</p>
        {%- include todo.html note=t.todo %}
      </div>
    </li>
    {%- endif %}
    {%- endfor %}
  </ol>
  {% if site.show_todos %}<p class="muted">{% include todo.html note="add any other 2026 talks or posters; month and day in _talks filenames are sort keys only and are not displayed" %}</p>{% endif %}
</div>
</div>
