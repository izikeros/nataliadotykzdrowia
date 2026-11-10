#!/usr/bin/env python3
"""Validate generated static pages without third-party dependencies."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).parent
DIST = ROOT / "docs"
DOMAIN = "nataliadotykzdrowia.pl"
ROUTES = (
    "",
    "o-mnie",
    "opinie",
    "analiza-zdrowia",
    "droga-do-rownowagi",
    "wspolpraca-online",
    "kurs-online",
    "polityka-prywatnosci",
    "regulamin-newslettera",
)
REDIRECTS = {"oferta": "/droga-do-rownowagi/"}
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
        self.ids = set()
        self.local_urls = []
        self.title = False
        self.lang = False
        self.description = False
        self.canonical = None
        self.icon = False
        self.refresh = None

    def handle_decl(self, decl):
        if decl.lower() == "doctype html":
            self.doctypes += 1

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        self.title |= tag == "title"
        self.lang |= tag == "html" and attributes.get("lang") == "pl"
        if tag == "meta":
            self.description |= attributes.get("name") == "description" and bool(attributes.get("content"))
            if attributes.get("http-equiv") == "refresh":
                self.refresh = attributes.get("content", "").partition("url=")[2]
        if tag == "link":
            rel = attributes.get("rel")
            if rel == "canonical":
                self.canonical = attributes.get("href")
            self.icon |= rel == "icon"
        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value and value.startswith("/") and not value.startswith("//"):
                self.local_urls.append(value.partition("?")[0])
        style = attributes.get("style") or ""
        self.local_urls += re.findall(r"""url\(\s*["']?(/[^/"')][^"')]*)""", style)


def audit(page):
    result = PageAudit()
    result.feed(page.read_text(encoding="utf-8"))
    return result


def normalize_base_path(base_path):
    if not base_path.startswith("/") or not base_path.endswith("/"):
        raise ValueError("Base path must start and end with /.")
    return base_path


def resolve_local_url(url, base_path):
    if not url.startswith(base_path):
        return None
    url = "/" + url.removeprefix(base_path)
    if url.startswith("/assets/") or url.endswith(".html"):
        return DIST / url.lstrip("/")
    return DIST / url.lstrip("/") / "index.html"


def check_basics(page, result, errors):
    name = page.relative_to(ROOT)
    if result.doctypes != 1:
        errors.append(f"{name}: expected one HTML5 doctype")
    for required in ("html", "head", "body"):
        if required not in result.tags:
            errors.append(f"{name}: missing <{required}>")
    if not result.lang:
        errors.append(f"{name}: missing lang=pl")
    if not result.title:
        errors.append(f"{name}: missing <title>")


def check_local_urls(name, urls, base_path, errors, audits):
    for url in urls:
        path, _, fragment = url.partition("#")
        target = resolve_local_url(path, base_path)
        if target is None:
            errors.append(f"{name}: local URL does not use base path {base_path}: {url}")
        elif not target.exists():
            errors.append(f"{name}: missing local target {url}")
        elif fragment and target.suffix == ".html":
            if target not in audits:
                audits[target] = audit(target).ids
            if fragment not in audits[target]:
                errors.append(f"{name}: missing fragment target {url}")


def main(base_path="/"):
    base_path = normalize_base_path(base_path)
    errors = []
    ids_cache = {}
    for route in ROUTES:
        page = DIST / route / "index.html"
        if not page.is_file():
            errors.append(f"Missing route output: {page.relative_to(ROOT)}")
            continue
        result = audit(page)
        check_basics(page, result, errors)
        name = page.relative_to(ROOT)
        if not result.description:
            errors.append(f"{name}: missing meta description")
        expected = f"https://{DOMAIN}/{route}{'/' if route else ''}"
        if result.canonical != expected:
            errors.append(f"{name}: canonical {result.canonical!r}, expected {expected}")
        if not result.icon:
            errors.append(f"{name}: missing favicon link")
        check_local_urls(name, result.local_urls, base_path, errors, ids_cache)
    for route, target in REDIRECTS.items():
        page = DIST / route / "index.html"
        if not page.is_file():
            errors.append(f"Missing redirect output: {page.relative_to(ROOT)}")
            continue
        result = audit(page)
        name = page.relative_to(ROOT)
        expected = f"{base_path}{target.lstrip('/')}"
        if result.refresh != expected:
            errors.append(f"{name}: redirect target {result.refresh!r}, expected {expected}")
        check_local_urls(name, result.local_urls, base_path, errors, ids_cache)
    for stylesheet in sorted((DIST / "assets").glob("*.css")):
        urls = re.findall(r"""url\(\s*["']?(/[^/"')][^"')]*)""", stylesheet.read_text(encoding="utf-8"))
        check_local_urls(stylesheet.relative_to(ROOT), urls, base_path, errors, ids_cache)
    for file in ("robots.txt", "sitemap.xml", ".nojekyll"):
        if not (DIST / file).is_file():
            errors.append(f"Missing {file}")
    sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8") if (DIST / "sitemap.xml").is_file() else ""
    listed = set(re.findall(r"<loc>https://" + re.escape(DOMAIN) + r"(/[^<]*)</loc>", sitemap))
    expected_listed = {f"/{route}{'/' if route else ''}" for route in ROUTES}
    if listed != expected_listed:
        errors.append(f"docs/sitemap.xml: expected {sorted(expected_listed)}, found {sorted(listed)}")
    cname = DIST / "CNAME"
    if not cname.is_file() or cname.read_text(encoding="utf-8").strip() != DOMAIN:
        errors.append(f"docs/CNAME: expected custom domain {DOMAIN}")
    for filename, markers in STANDALONE_PAGES.items():
        page = DIST / filename
        if not page.is_file():
            errors.append(f"Missing standalone page output: {page.relative_to(ROOT)}")
            continue
        check_basics(page, audit(page), errors)
        document = page.read_text(encoding="utf-8")
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
