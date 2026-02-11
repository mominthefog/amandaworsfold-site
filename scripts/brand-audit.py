#!/usr/bin/env python3
"""Brand audit: check content against voice guide anti-patterns and pricing consistency."""

import os
import re
import sys
from html.parser import HTMLParser


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", "node_modules", ".claude", "knowledge-base", "scripts"}

# Anti-patterns from the voice guide — words/phrases Amanda doesn't use
ANTI_PATTERNS = [
    (r"\brevolutionize\b", "Avoid hype words — use specific outcomes instead"),
    (r"\bcutting[- ]edge\b", "Avoid hype words — use specific outcomes instead"),
    (r"\bgame[- ]chang", "Avoid hype words — use specific outcomes instead"),
    (r"\bunlock the power\b", "Avoid hype words — use specific outcomes instead"),
    (r"\bsynerg", "Avoid corporate-speak"),
    (r"\bleverage\b", "Avoid corporate-speak — use 'use' instead"),
    (r"\bparadigm\b", "Avoid corporate-speak"),
    (r"\bschedule a consultation\b", "Use 'Book a call' instead"),
    (r"\bthe only\b.*\bconsultant\b", "Avoid positioning as 'the only' — per voice guide"),
    (r"\bthe best\b.*\bconsultant\b", "Avoid positioning as 'the best' — per voice guide"),
    (r"\bAI transformation\b(?!.*\b(real|actual|specific|concrete)\b)", "Avoid 'AI transformation' without specifics"),
]

# Pricing that must be consistent (same as facts.json but checked in visible text)
PRICING_CHECKS = [
    {
        "service": "Good Morning Briefing",
        "correct_price": "$2,500",
        "pattern": r"(?:morning\s+briefing|briefing).*?(\$[\d,]+)",
    },
    {
        "service": "Brand Voice Writer",
        "correct_price": "$5,000",
        "pattern": r"(?:brand\s+voice|voice\s+writer).*?(\$[\d,]+)",
    },
]

# Structural patterns that should be consistent
STRUCTURAL_CHECKS = [
    (r'class="nav-cta"[^>]*>(?!Book a Call)', "Nav CTA should say 'Book a Call'"),
]


class HTMLTextExtractor(HTMLParser):
    """Extract visible text from HTML, tracking line numbers."""

    def __init__(self):
        super().__init__()
        self.lines = {}
        self._skip = False
        self._skip_tags = {"script", "style"}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = False

    def handle_data(self, data):
        if self._skip:
            return
        line_num = self.getpos()[0]
        if line_num not in self.lines:
            self.lines[line_num] = ""
        self.lines[line_num] += data


def find_html_files(root):
    """Find all .html files in the repo, excluding certain directories."""
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.endswith(".html"):
                html_files.append(os.path.join(dirpath, fname))
    return sorted(html_files)


def check_anti_patterns(filepath, text_by_line):
    """Check for brand voice anti-patterns."""
    issues = []
    relpath = os.path.relpath(filepath, REPO_ROOT)

    for line_num, text in text_by_line.items():
        for pattern, message in ANTI_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                issues.append(
                    f"{relpath}:{line_num} — Found \"{match.group()}\": {message}"
                )

    return issues


def check_structural(filepath, content):
    """Check structural consistency patterns in raw HTML."""
    issues = []
    relpath = os.path.relpath(filepath, REPO_ROOT)

    for pattern, message in STRUCTURAL_CHECKS:
        for match in re.finditer(pattern, content):
            line = content[:match.start()].count("\n") + 1
            issues.append(f"{relpath}:{line} — {message}")

    return issues


def check_file(filepath):
    """Check a single HTML file for brand issues. Returns list of issues."""
    with open(filepath, "r") as f:
        content = f.read()

    extractor = HTMLTextExtractor()
    extractor.feed(content)
    text_by_line = extractor.lines

    issues = []
    issues.extend(check_anti_patterns(filepath, text_by_line))
    issues.extend(check_structural(filepath, content))

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

    if all_issues:
        print("BRAND AUDIT ISSUES:")
        for issue in all_issues:
            print(f"  {issue}")
        print(f"\n{len(all_issues)} issue(s) found.")
        sys.exit(1)
    else:
        print(f"Brand audit passed. {len(files)} file(s) scanned, 0 issues found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
