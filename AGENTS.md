# Repository instructions

## Project overview

This repository builds the static Polish-language Dotyk Zdrowia website.
`build.py` is the single source of generated page markup and writes deployable
output to `dist/`. The generated routes are:

- `/`
- `/o-mnie/`
- `/oferta/`
- `/opinie/`
- `/polityka-prywatnosci/`
- `/regulamin-newslettera/`

## Source of truth

- Edit page copy, navigation, canonical metadata, and shared markup in
  `build.py`.
- Edit styles in `assets/css/site.css` and behavior in `assets/js/site.js`.
- Treat `dist/` as generated output: regenerate it with `make build` or
  `make release`; never hand-edit its files.
- The builder copies supporting files from sibling paths `../misc/` and
  `../wp-content/uploads/`. Do not replace those external sources with
  repository-local stand-ins unless the task explicitly includes that scope.

## Working conventions

- Preserve Polish copy, `lang="pl"`, accessible alt text, and existing
  semantic HTML.
- For external links opened in a new tab, retain
  `target="_blank" rel="noopener"`.
- Use root-relative URLs for site routes and assets so generated pages work
  from every route.
- Update `check.py` when changing generated routes or validation invariants.
- Keep content, asset paths, and generated links consistent; run a build after
  changing `build.py` or assets.

## Commands

```sh
make build          # Generate readable dist/ output
make serve           # Build and serve dist/ at http://localhost:8081
make lint            # Build, validate HTML/local links, and check JavaScript
make format-check    # Check Prettier formatting of editable web sources
make release         # Create validated minified production output
make deploy-dry      # Preview the external deployment script
make deploy          # Release and deploy
```

Run `make lint` for HTML, copy, route, link, or JavaScript changes. Run
`make format-check` after editing CSS, JavaScript, or Markdown. Run
`make release` before deployment or when changing assets.
