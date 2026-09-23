.DEFAULT_GOAL := help

PYTHON ?= python3
PORT ?= 8081
MAX_IMAGE_DIMENSION ?= 2560
MAX_IMAGE_BYTES ?= 2621440
MAX_IMAGE_TOTAL_BYTES ?= 8388608
HTML_FORMAT ?= tidy

.PHONY: help build serve clean lint format format-check html-format html-compact html-tidy minify images-audit images-optimize release github-pages deploy deploy-dry

help: ## Show static-site commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'

build: ## Generate readable static output in docs/
	@$(PYTHON) build.py

serve: build ## Serve docs/ locally (override with PORT=...)
	@$(PYTHON) -m http.server $(PORT) --directory docs

clean: ## Remove generated static output
	@rm -rf docs

lint: build ## Validate generated HTML/local links and JavaScript syntax
	@$(PYTHON) check.py
	@node --check assets/js/site.js

format: ## Format editable CSS, JavaScript, and Markdown with installed Prettier
	@prettier --write assets/css/site.css assets/js/site.js README.md

format-check: ## Check editable CSS, JavaScript, and Markdown formatting
	@prettier --check assets/css/site.css assets/js/site.js README.md

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

images-optimize: minify ## Generate WebP/AVIF copies in docs/, then audit them
	@$(PYTHON) optimize_images.py
	@$(PYTHON) image_audit.py --max-dimension $(MAX_IMAGE_DIMENSION) --max-file-bytes $(MAX_IMAGE_BYTES) --max-total-bytes $(MAX_IMAGE_TOTAL_BYTES)

github-pages: format-check ## Create validated GitHub Pages project-site output in docs/
	@$(PYTHON) build.py --minify --base-path /nataliadotykzdrowia/
	@$(PYTHON) check.py --base-path /nataliadotykzdrowia/
	@node --check assets/js/site.js
	@$(PYTHON) image_audit.py --max-dimension $(MAX_IMAGE_DIMENSION) --max-file-bytes $(MAX_IMAGE_BYTES) --max-total-bytes $(MAX_IMAGE_TOTAL_BYTES)

release: minify format-check ## Create validated minified release output
	@$(PYTHON) check.py
	@node --check assets/js/site.js
	@$(PYTHON) image_audit.py --max-dimension $(MAX_IMAGE_DIMENSION) --max-file-bytes $(MAX_IMAGE_BYTES) --max-total-bytes $(MAX_IMAGE_TOTAL_BYTES)
