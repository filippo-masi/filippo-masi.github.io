---
layout: page
permalink: /repositories/
title: Software
description:
nav: true
nav_order: 1
---

In my research, I contributed to the following software, which was written for the purpose of validating and disseminating conducted research work and teaching. For more information, look at my [github](https://github.com/filippo-masi) and [curriculum vitae](https://filippo-masi.github.io/assets/pdf/FM_CV.pdf) for a detailed description of each software.

<p><font size="+1"><b>software development</b></font></p>

{% if site.data.repositories.github_repos %}
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.html repository=repo %}
  {% endfor %}
</div>
{% endif %}
