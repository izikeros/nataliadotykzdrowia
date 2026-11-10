#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the database-free Dotyk Zdrowia static site."""

from pathlib import Path
from shutil import copy2, rmtree
from html import escape
import argparse
import re

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
PAGES_DIR = ROOT / "pages"
DOMAIN = "nataliadotykzdrowia.pl"
WORDPRESS = ROOT.parent / "dotykzdrowia_wordpress"
MISC = WORDPRESS / "misc"
UPLOADS = WORDPRESS / "wp-content" / "uploads"
FAVICON = "/assets/img/favicon-32x32.png"

# Approved, hand-written pages copied verbatim from pages/<route>/index.html.
PAGES = ("", "o-mnie", "opinie", "analiza-zdrowia", "droga-do-rownowagi", "wspolpraca-online", "kurs-online")
# Descriptions injected only when the approved page has none.
FALLBACK_DESCRIPTIONS = {
    "": "Holistyczne terapie naturalne dla kobiet we Wrocławiu i online.",
}
LEGAL_PAGES = (
    ("polityka-prywatnosci", "polityka_prywatnosci.html", "Polityka prywatności", "Polityka prywatności Dotyku Zdrowia."),
    ("regulamin-newslettera", "Regulamin_Newslettera.html", "Regulamin newslettera", "Regulamin newslettera Dotyku Zdrowia."),
)
REDIRECTS = {
    "oferta": ("/droga-do-rownowagi/", {"online": "/wspolpraca-online/"}),
}
ROUTES = PAGES + tuple(route for route, *_ in LEGAL_PAGES)


def url_path(route):
    return "/" + route + ("/" if route else "")


def canonical(route):
    return f"https://{DOMAIN}{url_path(route)}"


def page_source(route):
    return PAGES_DIR / route / "index.html"


def inject_head(document, route):
    extra = []
    if 'rel="canonical"' not in document:
        extra.append(f'<link rel="canonical" href="{canonical(route)}">')
    if 'rel="icon"' not in document:
        extra.append(f'<link rel="icon" href="{FAVICON}" sizes="32x32">')
    if 'name="description"' not in document and route in FALLBACK_DESCRIPTIONS:
        extra.append(f'<meta name="description" content="{escape(FALLBACK_DESCRIPTIONS[route])}">')
    if not extra:
        return document
    return document.replace("</head>", "".join(extra) + "</head>", 1)


def site_chrome():
    """Header and footer markup shared by the approved subpages."""
    source = page_source("o-mnie").read_text(encoding="utf-8")
    header = re.search(r'<div class="wrap"><header class="sitehead">.*?</header></div>', source, re.DOTALL)
    footer = re.search(r'<footer class="footer">.*?</footer>', source, re.DOTALL)
    if not header or not footer:
        raise ValueError("Header or footer not found in pages/o-mnie/index.html")
    return header.group(0).replace(' class="on"', ""), footer.group(0)


def legal_page(filename):
    document = (MISC / filename).read_text(encoding="utf-8")
    match = re.search(r"(<article\b.*?</article>)", document, re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError(f"No legal article found in {filename}")
    return match.group(1)


def legal_document(route, title, description, article):
    header, footer = site_chrome()
    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Dotyk Zdrowia Natalia Safjan</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canonical(route)}">
<link rel="icon" href="{FAVICON}" sizes="32x32">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/landing-c.css">
<link rel="stylesheet" href="/assets/wspolne.css">
<link rel="stylesheet" href="/assets/legal.css">
</head>
<body>
{header}
<main class="section legal"><div class="wrap">{article}</div></main>
{footer}
</body>
</html>
"""


def redirect_document(target, fragments, base_path):
    mapping = ", ".join(f'"{key}": "{base_path}{value.lstrip("/")}"' for key, value in fragments.items())
    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<title>Przekierowanie | Dotyk Zdrowia Natalia Safjan</title>
<link rel="canonical" href="https://{DOMAIN}{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>(function(){{var m={{{mapping}}},h=location.hash.slice(1);if(m[h])location.replace(m[h])}})();</script>
</head>
<body>
<p>Ta strona została przeniesiona: <a href="{target}">przejdź dalej</a>.</p>
</body>
</html>
"""


def minify_html(document):
    # Strip indentation only: collapsing whitespace between tags could join inline words.
    return re.sub(r"\n\s+", "\n", document).strip() + "\n"


def minify_css(path):
    css = path.read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    path.write_text(css.strip() + "\n", encoding="utf-8")


def normalize_base_path(base_path):
    if not re.fullmatch(r"(?:/[A-Za-z0-9._~-]+)*/?", base_path):
        raise ValueError(
            "Base path must be / or a slash-delimited path such as /nataliadotykzdrowia/."
        )
    return "/" if base_path == "/" else f"/{base_path.strip('/')}/"


def prefix_local_urls(document, base_path):
    if base_path == "/":
        return document
    document = re.sub(r"""((?:href|src)=["'])/(?!/)""", rf"\g<1>{base_path}", document)
    document = re.sub(r"""(content="0; url=)/(?!/)""", rf"\g<1>{base_path}", document)
    return prefix_css_text(document, base_path)


def prefix_css_text(css, base_path):
    if base_path == "/":
        return css
    return re.sub(r"""(url\(\s*["']?)/(?!/)""", rf"\g<1>{base_path}", css)


def write(route, document, minify, base_path):
    target = OUT / route / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    document = prefix_local_urls(document, base_path)
    target.write_text(minify_html(document) if minify else document, encoding="utf-8")


def copy_assets(minify, base_path):
    assets = OUT / "assets"
    images = assets / "img"
    images.mkdir(parents=True)
    for image in (ROOT / "assets" / "img").iterdir():
        copy2(image, images / image.name)
    copy2(UPLOADS / "2021/03/cropped-fav-32x32.png", images / Path(FAVICON).name)
    for stylesheet in (ROOT / "assets").glob("*.css"):
        target = assets / stylesheet.name
        copy2(stylesheet, target)
        if minify:
            minify_css(target)
        target.write_text(prefix_css_text(target.read_text(encoding="utf-8"), base_path), encoding="utf-8")


def main(minify=False, base_path="/"):
    base_path = normalize_base_path(base_path)
    if OUT.exists():
        rmtree(OUT)
    copy_assets(minify, base_path)
    copy2(ROOT / "assets/analiza.html", OUT / "analiza.html")
    for route in PAGES:
        document = page_source(route).read_text(encoding="utf-8")
        write(route, inject_head(document, route), minify, base_path)
    for route, filename, title, description in LEGAL_PAGES:
        write(route, legal_document(route, title, description, legal_page(filename)), minify, base_path)
    for route, (target, fragments) in REDIRECTS.items():
        write(route, redirect_document(target, fragments, base_path), minify, base_path)
    (OUT / "CNAME").write_text(f"{DOMAIN}\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n", encoding="utf-8")
    (OUT / "sitemap.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">""" + "".join(
        f"<url><loc>{canonical(route)}</loc></url>" for route in ROUTES
    ) + "</urlset>\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minify", action="store_true", help="Minify generated HTML and CSS.")
    parser.add_argument(
        "--base-path",
        default="/",
        help="URL path where the site is served (default: /).",
    )
    main(**vars(parser.parse_args()))
