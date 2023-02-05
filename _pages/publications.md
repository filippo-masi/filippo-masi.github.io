---
layout: page
permalink: /publications/
title: publications
description: Author of 10 articles in major multi-disciplinary scientific journals and leading peer-reviewed international journals. More than 20 communications in prestigious international conferences.
years: [2022,2021,2020,2019,2018]
nav: false
nav_order: 1
---
<!-- _pages/publications.md -->
<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>


C 6 F Masi, I Stefanou (2022).
Data- and thermodynamics-driven discovery of state variables and
evolution equations, 41st International Workshop on Bayesian Inference and Maximum Entropy
Methods in Science and Engineering (MaxEnt’22). Paris, France, 18-22 July.
C 7 F Masi, I Stefanou (2022). Understanding the behavior of masonry structures subjected to blast
loads, International Conference on Nonlinear Solid Mechanics. Alghero, Italy, 13-16 June.
C 8 F Masi (2022). Deep learning, simulation temps réel et réduction de modèles (invited speaker),
5e Workshop CSMA Junior. Giens, France, 14-16 May.
C 9 F Masi, I Stefanou (2022). Multiscale modeling of inelastic microstructured materials with TANN,
18th European Mechanics of Materials Conference (EMMC18). Oxford, UK, April 4-6.
C 10 F Masi, I Stefanou (2021). Thermodynamics-based Neural Networks: a general framework for
modeling microstructured materials displaying path-dependency, ALERT Geomaterials. Aussois,
France, 27-29 September.
C 11 F Rabie, F Masi, I Stefanou (2021). Thermodynamics-based Artificial Neural Networks for
Nonlinear Seismic Analysis of High-rise Buildings, ALERT Geomaterials. Aussois, France, 27-
29 September.
