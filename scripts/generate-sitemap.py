#!/usr/bin/env python3
"""Generate sitemap.xml from all public HTML files."""

import os
import sys
from datetime import datetime


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://amandaworsfold.com"
EXCLUDE_DIRS = {".git", "node_modules", ".claude", "knowledge-base", "scripts"}
OUTPUT_FILE = os.path.join(REPO_ROOT, "sitemap.xml")


def find_html_files(root):
    """Find all .html files in the repo, excluding certain directories."""
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.endswith(".html"):
                html_files.append(os.path.join(dirpath, fname))
    return sorted(html_files)


def get_url(filepath):
    """Convert a file path to a URL."""
    relpath = os.path.relpath(filepath, REPO_ROOT)
    if relpath == "index.html":
        return SITE_URL + "/"
    return SITE_URL + "/" + relpath


def get_priority(filepath):
    """Assign priority based on page importance."""
    relpath = os.path.relpath(filepath, REPO_ROOT)
    if relpath == "index.html":
        return "1.0"
    if relpath in ("services.html", "contact.html"):
        return "0.9"
    if relpath in ("about.html", "speaking.html", "case-studies.html"):
        return "0.8"
    if relpath in ("build-lab.html", "finally-build-it.html", "the-knowledge-build.html"):
        return "0.7"
    return "0.5"


def generate_sitemap(files):
    """Generate sitemap XML content."""
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for filepath in files:
        url = get_url(filepath)
        priority = get_priority(filepath)
        lastmod = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d")

        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    files = find_html_files(REPO_ROOT)

    if not files:
        print("No HTML files found.")
        sys.exit(1)

    sitemap = generate_sitemap(files)

    with open(OUTPUT_FILE, "w") as f:
        f.write(sitemap)

    print(f"Sitemap generated: {OUTPUT_FILE}")
    print(f"  {len(files)} URL(s) included.")
    sys.exit(0)


if __name__ == "__main__":
    main()
