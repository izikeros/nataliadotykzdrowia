# Dotyk Zdrowia

Static Polish-language website for Natalia Safjan / Dotyk Zdrowia, published at
[nataliadotykzdrowia.pl](https://nataliadotykzdrowia.pl).

The site has no runtime dependencies or database. `build.py` generates the
HTML pages and copies the static assets into `docs/`.

## Requirements

- Python 3
- Node.js, for JavaScript syntax checks
- [Prettier](https://prettier.io/), optional for formatting commands
- ImageMagick (`magick`), optional for image optimization

The build reads the source image collection and supporting legal-page fragments
from the adjacent `../dotykzdrowia_wordpress/` project.

## Development

```sh
# Generate readable output in docs/
make build

# Build and serve locally on http://localhost:8081
make serve

# Use a different port
make serve PORT=3000

# Create the project-site output for https://izikeros.github.io/nataliadotykzdrowia/
make github-pages
```

Edit source files, not generated output:

| Path                         | Purpose                                                       |
| ---------------------------- | ------------------------------------------------------------- |
| `build.py`                   | Page markup, navigation, metadata, and generated text content |
| `assets/css/site.css`        | Site styles                                                   |
| `assets/js/site.js`          | Client-side behavior                                          |
| `assets/analiza.html`        | Standalone interactive body-signal analysis questionnaire     |
| `assets/images/`             | Repository-managed images                                     |
| `../dotykzdrowia_wordpress/` | WordPress image and legal-page source collection              |
| `docs/`                      | Generated deployable site; do not edit manually               |

## Validation and release

```sh
# Rebuild and validate pages, local links, and JavaScript
make lint

# Check source formatting
make format-check

# Reformat editable CSS, JavaScript, and Markdown
make format

# Audit emitted image dimensions and payload sizes
make images-audit

# Create and validate the minified release output
make release
```

`make release` generates minified production output, validates HTML and local
links, checks JavaScript syntax, verifies editable-file formatting, and audits
image budgets.

## Deployment paths

`make build`, `make serve`, and `make release` generate root-based URLs. Use
them for local preview (`http://localhost:8081/`) and, after the custom domain
is configured, for `https://nataliadotykzdrowia.pl/`.

Until then, publish the `docs/` directory created by `make github-pages` to
GitHub Pages. It prefixes local asset and page URLs with
`/nataliadotykzdrowia/`, so the site works at
`https://izikeros.github.io/nataliadotykzdrowia/`. When moving to the custom
domain, publish the root-based `make release` output instead; canonical URLs,
the sitemap, and `robots.txt` already name that domain.
