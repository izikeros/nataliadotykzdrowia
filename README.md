# Dotyk Zdrowia

Static Polish-language website for Natalia Safjan / Dotyk Zdrowia, published at
[nataliadotykzdrowia.pl](https://nataliadotykzdrowia.pl).

The site has no runtime dependencies or database. `build.py` generates the
HTML pages and copies the static assets into `dist/`.

## Requirements

- Python 3
- Node.js, for JavaScript syntax checks
- [Prettier](https://prettier.io/), optional for formatting commands
- ImageMagick (`magick`), optional for image optimization

The build expects the source image collection at
`../wp-content/uploads/` and supporting source files at `../misc/`.

## Development

```sh
# Generate readable output in dist/
make build

# Build and serve locally on http://localhost:8081
make serve

# Use a different port
make serve PORT=3000
```

Edit source files, not generated output:

| Path | Purpose |
| --- | --- |
| `build.py` | Page markup, navigation, metadata, and generated text content |
| `assets/css/site.css` | Site styles |
| `assets/js/site.js` | Client-side behavior |
| `assets/images/` | Repository-managed images |
| `../wp-content/uploads/` | Image source collection copied by the build |
| `dist/` | Generated deployable site; do not edit manually |

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

## Deployment

```sh
# Preview the configured deployment
make deploy-dry

# Build, validate, and deploy
make deploy
```

Deployment delegates to `../scripts/deploy-static.sh`; its environment and
target configuration are maintained outside this repository.
