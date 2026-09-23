# Dotyk Zdrowia static site

The deployed `dist/` directory is a plain static HTML/CSS/JS website. It has no server-side runtime, database, framework, or package dependency.

## Commands

Run all commands from `dotyk_static/`:

```bash
make build                 # Generate readable output
make serve                 # Build and serve at http://localhost:8081
make lint                  # Validate generated HTML/local links and JS syntax
make format                # Format editable CSS, JS, and Markdown
make format-check          # Verify Prettier formatting
make html-compact          # Put each generated HTML file on one line
make html-tidy             # Indent generated HTML for easy reading
make html-format HTML_FORMAT=tidy  # Select either tidy or compact explicitly
make minify                # Generate compact HTML/CSS output
make images-audit          # Check image dimensions and payload budgets
make images-optimize       # Add WebP/AVIF variants in dist/ and audit them
make release               # Minify and run validation
make deploy-dry            # Preview configured staging upload
make deploy                # Upload release output to staging
```

`PORT=8082 make serve` selects another local port. Build output deliberately is not committed; rerun the build whenever copy, images, CSS, or JavaScript changes. `make release` minifies generated HTML and CSS only; JavaScript remains readable because no JavaScript minifier is installed and the file is already small.

`make html-compact` and `make html-tidy` are reversible views of the same generated pages. Both rebuild `dist/` before formatting, then change HTML whitespace only. Use `html-compact` for one-line files and `html-tidy` when inspecting or editing generated markup.

## Image maintenance

`make images-audit` audits only the emitted `dist/assets/images/` files, not the complete WordPress media archive. It reports each image's dimensions and size, then rejects images above the defaults: `2560px` on either edge, `2.5MiB` per image, or `8MiB` total. The 2560px edge limit retains the live site's tall background image while still catching oversized uploads. The aggregate budget counts only the currently served JPEG/PNG sources, so optional WebP/AVIF copies do not triple-count the same visual content.

Override a limit for an intentional exception, for example:

```bash
make images-audit MAX_IMAGE_BYTES=3145728
```

`make images-optimize` preserves source formats and writes additional WebP and AVIF copies to the ignored `dist/` directory using `cwebp` and `avifenc`. It never changes files under `wp-content/uploads/`. The current HTML continues using original-format fallbacks; introduce `<picture>` markup only after comparing visual quality and browser support for the generated variants.

## Newsletter and consent

`assets/js/site.js` waits for explicit optional-cookie consent before displaying the delayed newsletter dialog. The dialog currently has a legal-page CTA only. Before staging, replace that content with the MailerLite-provided embed snippet or form markup; do not add MailerLite API credentials to this repository. Confirm the legal pages accurately describe the final third-party services before publishing.

## Staging deployment

Do not use the WordPress `make deploy` target for this project. Create an isolated staging document root on SEOHost, build `dist/`, then upload only its contents after a dry run. Keep WordPress live until staging has been approved and redirects/cutover are explicitly planned.
