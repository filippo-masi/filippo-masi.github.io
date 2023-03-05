---
layout: page
permalink: /repositories/
title: software development
description: I contributed to the following software.
nav: true
nav_order: 3
---


<p><font size="+1"><b>software development</b></font></p>

{% if site.data.repositories.github_repos %}
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.html repository=repo %}
  {% endfor %}
</div>
{% endif %}
