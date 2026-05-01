---
layout: default
title: Home
permalink: /
---

<section class="intro" aria-labelledby="intro-title">
  <p class="eyebrow">{{ site.author.role }}</p>
  <h1 id="intro-title">{{ site.author.name }}</h1>
  <p class="lead">{{ site.author.affiliation }}</p>
  <p class="intro-bio">
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
  </p>
</section>

<section id="publications" class="home-publications" aria-labelledby="publications-title">
  <div class="home-section-heading">
    <h2 id="publications-title">Publications</h2>
  </div>

  {% assign publications = site.data.publications_resolved | default: site.data.publications %}

  <section class="publication-list" aria-label="Publication list">
    {% for publication in publications %}
      <article class="publication-card">
        <h3 class="publication-title">
          {% if publication.url %}
            <a href="{{ publication.url }}">{{ publication.title }}</a>
          {% else %}
            {{ publication.title }}
          {% endif %}
        </h3>
        {% if publication.authors %}
          <p class="publication-authors">{{ publication.authors | join: ", " }}</p>
        {% endif %}
        {% if publication.venue or publication.year %}
          <p class="publication-meta">
            {% if publication.venue %}{{ publication.venue }}{% endif %}{% if publication.venue and publication.year %} &middot; {% endif %}{% if publication.year %}{{ publication.year }}{% endif %}
          </p>
        {% endif %}
        {% assign abstract = publication.abstract | default: publication.description %}
        {% if abstract %}
          <p class="publication-abstract">{{ abstract }}</p>
        {% endif %}
        {% if publication.doi or publication.pdf or publication.github or publication.playground %}
          <p class="publication-links">
            {% if publication.doi %}
              <a href="https://doi.org/{{ publication.doi }}">DOI: {{ publication.doi }}</a>
            {% endif %}
            {% if publication.pdf %}
              <a href="{{ publication.pdf }}">PDF</a>
            {% endif %}
            {% if publication.github %}
              <a href="{{ publication.github }}">git</a>
            {% endif %}
            {% if publication.playground %}
              <a href="{{ publication.playground }}">Playground</a>
            {% endif %}
          </p>
        {% endif %}
      </article>
    {% endfor %}
  </section>
</section>
