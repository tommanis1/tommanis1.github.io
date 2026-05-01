---
layout: default
title: Contact
permalink: /contact/
---

<section class="section" aria-labelledby="contact-page-title">
  <h1 id="contact-page-title">Contact</h1>
  {% if site.author.email and site.author.email != "" %}
    <p>You can reach me at <a href="mailto:{{ site.author.email }}">{{ site.author.email }}</a>.</p>
  {% else %}
    <p>Contact details coming soon.</p>
  {% endif %}
</section>
