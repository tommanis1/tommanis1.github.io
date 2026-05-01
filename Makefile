BUNDLE ?= bundle3.2
JEKYLL ?= jekyll
HOST ?= 127.0.0.1
PORT ?= 4000

.DEFAULT_GOAL := serve

.PHONY: help install publications build serve preview clean

help:
	@printf "Targets:\n"
	@printf "  make install  Install Jekyll dependencies into vendor/bundle\n"
	@printf "  make publications  Generate publication data from BibTeX\n"
	@printf "  make build    Build the static site into _site\n"
	@printf "  make serve    Serve the site at http://$(HOST):$(PORT)\n"
	@printf "  make clean    Remove generated Jekyll output\n"

install:
	$(BUNDLE) config set path vendor/bundle
	$(BUNDLE) install

publications:
	$(BUNDLE) exec ruby scripts/build_publications.rb

build: publications
	$(BUNDLE) exec $(JEKYLL) build

serve: publications
	@printf "Serving at http://$(HOST):$(PORT)\n"
	$(BUNDLE) exec $(JEKYLL) serve --host $(HOST) --port $(PORT)

preview: serve

clean:
	$(BUNDLE) exec $(JEKYLL) clean
