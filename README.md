# Personal Website

Minimal Jekyll site for a computer science PhD student, intended for GitHub Pages.

## Edit content

- Site metadata lives in `_config.yml`.
- Homepage sections live in `index.md`.
- BibTeX entries for publications live in `_bibliography/publications.bib`.
- Publication display options live in `_data/publications.yml`. Use `key` to select a BibTeX entry, and keep site-specific fields such as `authors`, `abstract`, `github`, `playground`, and `pdf` there. Values in this YAML file override values read from BibTeX.
- News and blog posts are listed from `news.md`.
- Individual blog posts live in `_posts` and should be named `YYYY-MM-DD-title.md`.
- Shared page chrome lives in `_layouts/default.html`.
- Styles live in `assets/css/main.css`.

Example publication entry:

```yml
- key: pacciani2025p4ddg
  authors:
    - "Tommaso Pacciani"
    - "Damian Frölich"
    - "L. Thomas van Binsbergen"
    - "Chrysa Papagianni"
  abstract: "Short site-facing summary."
  github: "https://github.com/user/project"
  playground: "https://example.com/playground"
```

Run `make publications` after editing the BibTeX or publication YAML. `make build` and `make serve` run it automatically.

## Run locally

Install Ruby and Bundler, then run:

```sh
make install
make serve
```

The site will be available at `http://localhost:4000`.

This machine has Bundler as `bundle3.2`, so the `Makefile` uses that by default. On a machine where the executable is named `bundle`, run `make install BUNDLE=bundle` and `make serve BUNDLE=bundle`.

## Deploy

Push to the `main` branch. The existing GitHub Actions workflow builds and deploys the Jekyll site to GitHub Pages.
