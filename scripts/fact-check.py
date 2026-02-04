#!/usr/bin/env python3
"""Fact-check HTML files against known correct facts in facts.json."""

import json
import os
import re
import sys
from html.parser import HTMLParser


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_FILE = os.path.join(REPO_ROOT, "facts.json")
EXCLUDE_DIRS = {".git", "node_modules", ".claude"}


class HTMLTextExtractor(HTMLParser):
    """Extract visible text from HTML, tracking line numbers."""

    def __init__(self):
        super().__init__()
        self.lines = {}  # line_number -> text content
        self._current_line = 1
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


def extract_text_by_line(html_content):
    """Parse HTML and return a dict of line_number -> visible text."""
    extractor = HTMLTextExtractor()
    extractor.feed(html_content)
    return extractor.lines


def load_facts():
    """Load facts.json from the repo root."""
    with open(FACTS_FILE, "r") as f:
        return json.load(f)["facts"]


def check_file(filepath, facts):
    """Check a single HTML file against all facts. Returns list of issues."""
    with open(filepath, "r") as f:
        content = f.read()

    text_by_line = extract_text_by_line(content)
    issues = []

    for fact in facts:
        for pattern in fact["wrong_patterns"]:
            regex = re.compile(pattern, re.IGNORECASE)
            for line_num, text in text_by_line.items():
                match = regex.search(text)
                if match:
                    issues.append({
                        "file": filepath,
                        "line": line_num,
                        "matched": match.group(),
                        "fact_id": fact["id"],
                        "description": fact["description"],
                        "correct": fact["correct"],
                    })

    return issues


def find_html_files(root):
    """Find all .html files in the repo, excluding certain directories."""
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.endswith(".html"):
                html_files.append(os.path.join(dirpath, fname))
    return sorted(html_files)


def main():
    facts = load_facts()

    # Determine which files to check
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
        issues = check_file(filepath, facts)
        all_issues.extend(issues)

    if all_issues:
        print("FACT CHECK FAILED:")
        for issue in all_issues:
            relpath = os.path.relpath(issue["file"], REPO_ROOT)
            print(
                f"  {relpath}:{issue['line']} — "
                f"Found \"{issue['matched']}\" "
                f"({issue['fact_id']}: {issue['description']})"
            )
        print(f"\n{len(all_issues)} issue(s) found.")
        sys.exit(1)
    else:
        print(f"Fact check passed. {len(files)} file(s) scanned, 0 issues found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
