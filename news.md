---
layout: default
title: News
permalink: /news/
---

<section class="page-heading" aria-labelledby="news-title">
  <h1 id="news-title">News</h1>
  <p class="lead">Updates and blog posts will appear here.</p>
</section>

{% if site.posts.size > 0 %}
  <div class="post-list">
    {% for post in site.posts %}
      <article class="post-preview">
        <p class="post-date">{{ post.date | date: "%B %-d, %Y" }}</p>
        <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
        {% if post.excerpt %}
          {{ post.excerpt }}
        {% endif %}
      </article>
    {% endfor %}
  </div>
{% else %}
  <section class="section section-single">
    <h2>No Posts Yet</h2>
    <p>Blog posts will be listed here once they are added to <code>_posts</code>.</p>
  </section>
{% endif %}

