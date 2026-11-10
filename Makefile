.DEFAULT_GOAL := help

PYTHON ?= python3
PORT ?= 8081
MAX_IMAGE_DIMENSION ?= 2560
MAX_IMAGE_BYTES ?= 2621440
MAX_IMAGE_TOTAL_BYTES ?= 8388608
HTML_FORMAT ?= tidy

.PHONY: help build serve clean lint format format-check html-format html-compact html-tidy minify images-audit release github-pages deploy deploy-dry

help: ## Show static-site commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'

build: ## Generate readable static output in docs/
	@$(PYTHON) build.py

serve: build ## Serve docs/ locally (override with PORT=...)
	@$(PYTHON) -m http.server $(PORT) --directory docs

clean: ## Remove generated static output
	@rm -rf docs

lint: build ## Validate generated HTML, metadata, and local links
	@$(PYTHON) check.py

format: ## Format editable CSS and Markdown with installed Prettier
	@prettier --write assets/legal.css README.md

format-check: ## Check editable CSS and Markdown formatting
	@prettier --check assets/legal.css README.md

html-format: build ## Format generated HTML (HTML_FORMAT=compact or tidy)
	@$(PYTHON) format_html.py $(HTML_FORMAT)

html-compact: HTML_FORMAT=compact
html-compact: html-format ## Put each generated HTML file on one line

html-tidy: HTML_FORMAT=tidy
html-tidy: html-format ## Indent generated HTML for easy reading

minify: clean ## Generate minified HTML/CSS output in docs/
	@$(PYTHON) build.py --minify

images-audit: build ## Check emitted image dimensions and payload budgets
	@$(PYTHON) image_audit.py --max-dimension $(MAX_IMAGE_DIMENSION) --max-file-bytes $(MAX_IMAGE_BYTES) --max-total-bytes $(MAX_IMAGE_TOTAL_BYTES)

github-pages: format-check ## Create validated GitHub Pages output for nataliadotykzdrowia.pl in docs/
	@$(PYTHON) build.py --minify
	@$(PYTHON) check.py
	@$(PYTHON) image_audit.py --max-dimension $(MAX_IMAGE_DIMENSION) --max-file-bytes $(MAX_IMAGE_BYTES) --max-total-bytes $(MAX_IMAGE_TOTAL_BYTES)

release: minify format-check ## Create validated minified release output
	@$(PYTHON) check.py
	@$(PYTHON) image_audit.py --max-dimension $(MAX_IMAGE_DIMENSION) --max-file-bytes $(MAX_IMAGE_BYTES) --max-total-bytes $(MAX_IMAGE_TOTAL_BYTES)
