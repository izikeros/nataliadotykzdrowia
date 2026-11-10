# Dotyk Zdrowia

Static Polish-language website for Natalia Safjan / Dotyk Zdrowia, published at
[nataliadotykzdrowia.pl](https://nataliadotykzdrowia.pl).

The site has no runtime dependencies or database. The pages approved by Natalia
(9.11.2026) live as hand-written HTML in `pages/`. `build.py` copies them to
`docs/` unchanged, apart from adding a canonical link, the favicon and, where
missing, a meta description. It also wraps the legal articles in the shared
header and footer, writes the `/oferta/` redirect, and copies the assets.

## Requirements

- Python 3
- [Prettier](https://prettier.io/), optional for formatting commands
- macOS `sips`, for the image audit

The build reads the legal-page articles and the favicon from the adjacent
`../dotykzdrowia_wordpress/` project.

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

| Path                         | Purpose                                                           |
| ---------------------------- | ----------------------------------------------------------------- |
| `pages/<route>/index.html`   | Approved page markup, copy, and inline page styles/scripts        |
| `build.py`                   | Route list, head injection, legal shell, redirects, sitemap       |
| `check.py`                   | Validation of generated routes, metadata, links, and fragments    |
| `assets/landing-c.css`       | Shared styles of the approved subpages                            |
| `assets/wspolne.css`         | Shared header, hero, and icon styles of the approved subpages     |
| `assets/legal.css`           | Styles for the privacy policy and newsletter regulations articles |
| `assets/img/`                | Page images (WebP/AVIF)                                           |
| `assets/analiza.html`        | Standalone interactive body-signal analysis questionnaire         |
| `../dotykzdrowia_wordpress/` | Legal-page articles and favicon source                            |
| `docs/`                      | Generated deployable site; do not edit manually                   |

## Routes

| Route                     | Source                                                                  |
| ------------------------- | ----------------------------------------------------------------------- |
| `/`                       | `pages/index.html`                                                      |
| `/o-mnie/`                | `pages/o-mnie/index.html`                                               |
| `/opinie/`                | `pages/opinie/index.html`                                               |
| `/analiza-zdrowia/`       | `pages/analiza-zdrowia/index.html`                                      |
| `/droga-do-rownowagi/`    | `pages/droga-do-rownowagi/index.html`                                   |
| `/wspolpraca-online/`     | `pages/wspolpraca-online/index.html`                                    |
| `/kurs-online/`           | `pages/kurs-online/index.html`                                          |
| `/polityka-prywatnosci/`  | `polityka_prywatnosci.html` article                                     |
| `/regulamin-newslettera/` | `Regulamin_Newslettera.html` article                                    |
| `/oferta/`                | Redirect to `/droga-do-rownowagi/` (`#online` to `/wspolpraca-online/`) |
| `/analiza.html`           | `assets/analiza.html`                                                   |

To add a page, put it in `pages/<route>/index.html`, then add the route to
`PAGES` in `build.py` and to `ROUTES` in `check.py`. The pages for men
(`/analiza-zdrowia-mezczyzni/`, `/droga-do-rownowagi-mezczyzni/`) will come later.

External services linked from the pages: SimplyBook bookings, the
`sklep.nataliadotykzdrowia.pl` shop, the subscribepage.io newsletter, Google
Fonts and Google reviews. Two images load from `cdn.idealms.net`.

## Validation and release

```sh
# Rebuild and validate pages, metadata, local links, and fragments
make lint

# Check source formatting
make format-check

# Reformat editable CSS and Markdown
make format

# Audit emitted image dimensions and payload sizes
make images-audit

# Create and validate the minified release output
make release
```

`make release` generates minified production output, validates HTML and local
links, verifies editable-file formatting, and audits image budgets.

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
