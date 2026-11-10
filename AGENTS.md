# Repository instructions

## Project overview

This repository builds the static Polish-language Dotyk Zdrowia website.
Approved pages are hand-written HTML in `pages/`; `build.py` copies them
(adding canonical, favicon, and missing descriptions), wraps the legal pages in
the shared header/footer, and writes deployable output to `docs/`. Routes:

- `/`, `/o-mnie/`, `/opinie/`, `/analiza-zdrowia/`, `/droga-do-rownowagi/`,
  `/wspolpraca-online/`, `/kurs-online/` (from `pages/`)
- `/polityka-prywatnosci/`, `/regulamin-newslettera/` (legal articles)
- `/oferta/` (redirect to `/droga-do-rownowagi/`)

## Source of truth

- Edit page copy, navigation, and page scripts in `pages/<route>/index.html`;
  routes, head injection, legal shell, redirects, and sitemap in `build.py`.
- Edit styles in `assets/landing-c.css`, `assets/wspolne.css`,
  `assets/legal.css`, or page-level `<style>`; images live in `assets/img/`.
- Treat `docs/` as generated output: regenerate it with `make build` or
  `make release`; never hand-edit its files.
- The builder copies legal articles and the favicon from
  `../dotykzdrowia_wordpress/misc/` and `../dotykzdrowia_wordpress/wp-content/uploads/`. Do not replace those external sources with
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
  changing `build.py`, `pages/`, or assets.

## Commands

```sh
make build          # Generate readable docs/ output
make serve           # Build and serve docs/ at http://localhost:8081
make lint            # Build and validate HTML, metadata, local links
make format-check    # Check Prettier formatting of editable web sources
make release         # Create validated minified production output
make deploy-dry      # Preview the external deployment script
make deploy          # Release and deploy
```

Run `make lint` for HTML, copy, route, link, or JavaScript changes. Run
`make format-check` after editing `assets/legal.css` or Markdown. Run
`make release` before deployment or when changing assets.
