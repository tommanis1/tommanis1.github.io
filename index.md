---
layout: default
title: Home
permalink: /
---

<section class="intro" aria-labelledby="intro-title">
  <div class="intro-content">
    <p class="eyebrow">{{ site.author.role }}</p>
    <h1 id="intro-title">{{ site.author.name }}</h1>
    <span class="title-rule" aria-hidden="true"></span>
    <p class="lead">{{ site.author.affiliation }}</p>
    <p class="intro-bio">
      I work on programming language theory and systems, with a focus on domain-specific languages, parsing, and compiling for high-performance environments.
    </p>
    <div class="intro-links" aria-label="Contact links">
      {% if site.author.email and site.author.email != "" %}
        <a href="mailto:{{ site.author.email }}">
      {% else %}
        <a href="{{ '/contact/' | relative_url }}">
      {% endif %}
          <svg class="icon" aria-hidden="true" viewBox="0 0 24 24">
            <path d="M4 6h16v12H4z"></path>
            <path d="m4 7 8 6 8-6"></path>
          </svg>
          Email
        </a>
      {% if site.author.github %}
        <a href="{{ site.author.github }}">
          <svg class="icon github-icon" aria-hidden="true" viewBox="0 0 24 24">
            <path d="M12 2.4a9.6 9.6 0 0 0-3 18.7c.5.1.7-.2.7-.5v-1.8c-2.8.6-3.4-1.1-3.4-1.1-.5-1.1-1.1-1.4-1.1-1.4-.9-.6.1-.6.1-.6 1 .1 1.6 1 1.6 1 .9 1.5 2.3 1.1 2.8.8.1-.6.3-1.1.6-1.3-2.2-.3-4.6-1.1-4.6-4.8 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.7 1a9.2 9.2 0 0 1 4.9 0c1.9-1.3 2.7-1 2.7-1 .5 1.4.2 2.4.1 2.7.7.7 1 1.6 1 2.7 0 3.7-2.4 4.5-4.6 4.8.4.3.7.9.7 1.8v2.6c0 .3.2.6.7.5A9.6 9.6 0 0 0 12 2.4Z"></path>
          </svg>
          GitHub
        </a>
      {% endif %}
    </div>
  </div>
  <div class="intro-art" aria-hidden="true">
    <span></span>
  </div>
</section>

<section id="publications" class="home-publications" aria-labelledby="publications-title">
  <div class="home-section-heading content-wrap">
    <h2 id="publications-title">Publications</h2>
    {% if site.author.scholar %}
      <p>Selected publications. For the full list see <a href="{{ site.author.scholar }}">Google Scholar</a>.</p>
    {% endif %}
  </div>

  {% assign publications = site.data.publications_resolved | default: site.data.publications %}

  <section class="publication-list content-wrap" aria-label="Publication list">
    {% for publication in publications %}
      <article class="publication-card">
        <svg class="publication-icon icon" aria-hidden="true" viewBox="0 0 24 24">
          <path d="M7 3h7l5 5v13H7z"></path>
          <path d="M14 3v6h5"></path>
          <path d="M10 13h6M10 17h5"></path>
        </svg>
        <div class="publication-body">
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
                <a href="{{ publication.pdf }}">
                  <svg class="icon" aria-hidden="true" viewBox="0 0 24 24">
                    <path d="M7 3h7l5 5v13H7z"></path>
                    <path d="M14 3v6h5"></path>
                    <path d="M10 15h4"></path>
                  </svg>
                  PDF
                </a>
              {% endif %}
              {% if publication.github %}
                <a href="{{ publication.github }}">
                  <svg class="icon" aria-hidden="true" viewBox="0 0 24 24">
                    <path d="m8 9-4 3 4 3M16 9l4 3-4 3M14 5l-4 14"></path>
                  </svg>
                  git
                </a>
              {% endif %}
              {% if publication.playground %}
                <a href="{{ publication.playground }}">Playground</a>
              {% endif %}
            </p>
            {% endif %}
        </div>
      </article>
    {% endfor %}
  </section>
</section>
