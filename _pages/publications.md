---
layout: page
permalink: /scientific production/
title: scientific production
description: List of refereed journal articles, conference proceedings, preprints, and communications.
years: [2022,2021,2020,2019,2018]
nav: true
nav_order: 1
---
<!-- _pages/publications.md -->
<p><font size="+2">preprints</font></p>
<div class="publications">
{% bibliography --file papers2 %}

</div>

<div><font size="+1"><b>refereed journal articles</b></font></div>
<div class="publications">

{% bibliography --file papers %}


</div>

<div><font size="+2">refereed conference proceedings</font></div>
<div class="publications">

{% bibliography --file papers3 %}

</div>

<div><font size="+2">conference communication</font></div>
<div class="publications">

#{% bibliography --file papers %}

</div>
