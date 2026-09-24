#!/usr/bin/env python3
"""Validate generated static pages without third-party dependencies."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).parent
DIST = ROOT / "docs"
ROUTES = ("", "oferta", "o-mnie", "opinie", "polityka-prywatnosci", "regulamin-newslettera")
EXPECTED_TESTIMONIALS = {"": 7, "opinie": 32}
HOME_OFFER_LINKS = (
    (
        "/oferta/#terapia-holistyczna",
        "Holistyczna terapia naturalna w gabinecie we Wrocławiu",
    ),
    ("/oferta/#online", "Holistyczna współpraca indywidualna online"),
)
CSS_LOCAL_URLS = (
    "/assets/images/tlo.png",
    "/assets/images/markus-spiske-IKvDKHWF_5w-unsplash-scaled.jpg",
    "/assets/images/tlo2.png",
)
STANDALONE_PAGES = {
    "analiza.html": (
        "Kwestionariusz Analizy sygnałów ciała",
        'id="resetBtn"',
        "data-system=",
    ),
}


class PageAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.doctypes = 0
        self.tags = []
        self.local_urls = []
        self.title = False
        self.lang = False
        self.testimonials = 0

    def handle_decl(self, decl):
        if decl.lower() == "doctype html":
            self.doctypes += 1

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attributes = dict(attrs)
        self.title |= tag == "title"
        self.lang |= tag == "html" and attributes.get("lang") == "pl"
        self.testimonials += tag == "img" and attributes.get("alt") == "Opinia klientki"
        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value and value.startswith("/"):
                self.local_urls.append(value.partition("#")[0].partition("?")[0])


def normalize_base_path(base_path):
    if not base_path.startswith("/") or not base_path.endswith("/"):
        raise ValueError("Base path must start and end with /.")
    return base_path


def resolve_local_url(url, base_path):
    if not url.startswith(base_path):
        return None
    url = "/" + url.removeprefix(base_path)
    if url.startswith("/assets/"):
        return DIST / url.lstrip("/")
    return DIST / url.lstrip("/") / "index.html"


def main(base_path="/"):
    base_path = normalize_base_path(base_path)
    errors = []
    for route in ROUTES:
        page = DIST / route / "index.html"
        if not page.is_file():
            errors.append(f"Missing route output: {page.relative_to(ROOT)}")
            continue
        audit = PageAudit()
        audit.feed(page.read_text(encoding="utf-8"))
        if audit.doctypes != 1:
            errors.append(f"{page.relative_to(ROOT)}: expected one HTML5 doctype")
        for required in ("html", "head", "body", "main"):
            if required not in audit.tags:
                errors.append(f"{page.relative_to(ROOT)}: missing <{required}>")
        if not audit.lang:
            errors.append(f"{page.relative_to(ROOT)}: missing lang=pl")
        if not audit.title:
            errors.append(f"{page.relative_to(ROOT)}: missing <title>")
        document = page.read_text(encoding="utf-8")
        if route == "":
            for href, label in HOME_OFFER_LINKS:
                prefixed_href = f"{base_path}{href.lstrip('/')}"
                if f'href="{prefixed_href}"' not in document or label not in document:
                    errors.append(f"{page.relative_to(ROOT)}: missing linked production offer title")
        if "Copyright 2026 Natalia Safjan" not in document:
            errors.append(f"{page.relative_to(ROOT)}: missing production copyright")
        if "Iron Box" in document:
            errors.append(f"{page.relative_to(ROOT)}: obsolete design credit")
        if 'class="scroll-top"' not in document:
            errors.append(f"{page.relative_to(ROOT)}: missing scroll-to-top control")
        expected_testimonials = EXPECTED_TESTIMONIALS.get(route)
        if expected_testimonials is not None and audit.testimonials != expected_testimonials:
            errors.append(
                f"{page.relative_to(ROOT)}: expected {expected_testimonials} testimonial "
                f"images, found {audit.testimonials}"
            )
        for url in audit.local_urls:
            target = resolve_local_url(url, base_path)
            if target is None:
                errors.append(
                    f"{page.relative_to(ROOT)}: local URL does not use base path {base_path}: {url}"
                )
            elif not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: missing local target {url}")
    css = (DIST / "assets" / "css" / "site.css").read_text(encoding="utf-8")
    for url in CSS_LOCAL_URLS:
        prefixed_url = f"{base_path}{url.lstrip('/')}"
        if prefixed_url not in css:
            errors.append(f"docs/assets/css/site.css: missing local target {prefixed_url}")
    for file in ("robots.txt", "sitemap.xml"):
        if not (DIST / file).is_file():
            errors.append(f"Missing {file}")
    for filename, markers in STANDALONE_PAGES.items():
        page = DIST / filename
        if not page.is_file():
            errors.append(f"Missing standalone page output: {page.relative_to(ROOT)}")
            continue
        document = page.read_text(encoding="utf-8")
        audit = PageAudit()
        audit.feed(document)
        if audit.doctypes != 1:
            errors.append(f"{page.relative_to(ROOT)}: expected one HTML5 doctype")
        if not audit.lang:
            errors.append(f"{page.relative_to(ROOT)}: missing lang=pl")
        if not audit.title:
            errors.append(f"{page.relative_to(ROOT)}: missing <title>")
        for marker in markers:
            if marker not in document:
                errors.append(f"{page.relative_to(ROOT)}: missing expected content {marker}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Static HTML routes, metadata, local links, and generated files are valid.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-path",
        default="/",
        help="URL path where the generated site is served (default: /).",
    )
    raise SystemExit(main(**vars(parser.parse_args())))
