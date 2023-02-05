---
layout: page
permalink: /scientific production/
title: scientific production
description: Author of 10 articles in major multi-disciplinary scientific journals and leading peer-reviewed international journals. More than 20 communications in prestigious international conferences.
#years: [2022,2021,2020,2019,2018]
nav: true
nav_order: 1
---
<!-- _pages/publications.md -->
<div><font size="+1"><b>Preprints</b></font></div>
<div class="publications">

% bibliography -f papers2 -q

</div>

<div><font size="+1"><b>Refereed journal articles</b></font></div>
<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
