#!/usr/bin/env python3
"""Validate generated static pages without third-party dependencies."""

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
ROUTES = ("", "oferta", "o-mnie", "opinie", "polityka-prywatnosci", "regulamin-newslettera")
EXPECTED_TESTIMONIALS = {"": 7, "opinie": 32}
HOME_OFFER_LINKS = (
    (
        "/oferta/#terapia-holistyczna",
        "Holistyczna terapia naturalna w gabinecie we Wrocławiu",
    ),
    ("/oferta/#online", "Holistyczna współpraca indywidualna online"),
)


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


def resolve_local_url(url):
    if url.startswith("/assets/"):
        return DIST / url.lstrip("/")
    return DIST / url.lstrip("/") / "index.html"


def main():
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
                if f'href="{href}"' not in document or label not in document:
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
            if not resolve_local_url(url).exists():
                errors.append(f"{page.relative_to(ROOT)}: missing local target {url}")
    for file in ("robots.txt", "sitemap.xml"):
        if not (DIST / file).is_file():
            errors.append(f"Missing {file}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Static HTML routes, metadata, local links, and generated files are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
