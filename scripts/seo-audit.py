#!/usr/bin/env python3
"""SEO audit: check all HTML pages for required meta tags, OG, canonical, alt text."""

import os
import re
import sys
from html.parser import HTMLParser


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", "node_modules", ".claude", "knowledge-base", "scripts"}
SITE_URL = "https://amandaworsfold.com"


class SEOChecker(HTMLParser):
    """Parse HTML and check for SEO requirements."""

    def __init__(self):
        super().__init__()
        self.has_title = False
        self.has_meta_description = False
        self.has_canonical = False
        self.has_og_title = False
        self.has_og_description = False
        self.has_og_image = False
        self.has_og_url = False
        self.has_og_type = False
        self.has_twitter_card = False
        self.has_viewport = False
        self.has_charset = False
        self.images_without_alt = []
        self._in_head = False
        self._current_line = 0

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        line = self.getpos()[0]

        if tag == "head":
            self._in_head = True
        elif tag == "title" and self._in_head:
            self.has_title = True
        elif tag == "link" and self._in_head:
            if attr_dict.get("rel") == "canonical":
                self.has_canonical = True
        elif tag == "meta" and self._in_head:
            name = attr_dict.get("name", "").lower()
            prop = attr_dict.get("property", "").lower()
            charset = attr_dict.get("charset")

            if charset:
                self.has_charset = True
            if name == "description":
                self.has_meta_description = True
            if name == "viewport":
                self.has_viewport = True
            if name == "twitter:card":
                self.has_twitter_card = True
            if prop == "og:title":
                self.has_og_title = True
            if prop == "og:description":
                self.has_og_description = True
            if prop == "og:image":
                self.has_og_image = True
            if prop == "og:url":
                self.has_og_url = True
            if prop == "og:type":
                self.has_og_type = True
        elif tag == "img":
            alt = attr_dict.get("alt")
            if alt is None or alt.strip() == "":
                src = attr_dict.get("src", "(unknown)")
                self.images_without_alt.append((line, src))

    def handle_endtag(self, tag):
        if tag == "head":
            self._in_head = False


def find_html_files(root):
    """Find all .html files in the repo, excluding certain directories."""
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.endswith(".html"):
                html_files.append(os.path.join(dirpath, fname))
    return sorted(html_files)


def check_file(filepath):
    """Check a single HTML file for SEO issues. Returns list of issues."""
    with open(filepath, "r") as f:
        content = f.read()

    checker = SEOChecker()
    checker.feed(content)

    issues = []
    relpath = os.path.relpath(filepath, REPO_ROOT)

    required_tags = [
        ("title", checker.has_title),
        ("meta description", checker.has_meta_description),
        ("canonical URL", checker.has_canonical),
        ("og:title", checker.has_og_title),
        ("og:description", checker.has_og_description),
        ("og:image", checker.has_og_image),
        ("og:url", checker.has_og_url),
        ("og:type", checker.has_og_type),
        ("twitter:card", checker.has_twitter_card),
        ("viewport", checker.has_viewport),
        ("charset", checker.has_charset),
    ]

    for tag_name, present in required_tags:
        if not present:
            issues.append(f"{relpath} — Missing {tag_name}")

    for line, src in checker.images_without_alt:
        issues.append(f"{relpath}:{line} — Image missing alt text: {src}")

    return issues


def check_internal_links(files):
    """Check for broken internal links between pages."""
    issues = []
    existing_files = set()
    for f in files:
        relpath = os.path.relpath(f, REPO_ROOT)
        existing_files.add("/" + relpath)
        if relpath == "index.html":
            existing_files.add("/")

    link_pattern = re.compile(r'href="(/[^"#]*)"')
    for filepath in files:
        with open(filepath, "r") as f:
            content = f.read()
        relpath = os.path.relpath(filepath, REPO_ROOT)
        for match in link_pattern.finditer(content):
            href = match.group(1)
            if href not in existing_files and not href.startswith("http"):
                line = content[:match.start()].count("\n") + 1
                issues.append(f"{relpath}:{line} — Broken internal link: {href}")

    return issues


def main():
    if len(sys.argv) > 1:
        files = []
        for arg in sys.argv[1:]:
            path = arg if os.path.isabs(arg) else os.path.join(REPO_ROOT, arg)
            if os.path.isfile(path):
                files.append(path)
            else:
                print(f"Warning: File not found: {arg}")
    else:
        files = find_html_files(REPO_ROOT)

    if not files:
        print("No HTML files to check.")
        sys.exit(0)

    all_issues = []
    for filepath in files:
        issues = check_file(filepath)
        all_issues.extend(issues)

    link_issues = check_internal_links(files)
    all_issues.extend(link_issues)

    if all_issues:
        print("SEO AUDIT ISSUES:")
        for issue in all_issues:
            print(f"  {issue}")
        print(f"\n{len(all_issues)} issue(s) found.")
        sys.exit(1)
    else:
        print(f"SEO audit passed. {len(files)} file(s) scanned, 0 issues found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
