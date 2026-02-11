#!/usr/bin/env python3
"""Check event pages for stale dates based on events.json."""

import json
import os
import sys
from datetime import datetime, timedelta


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_FILE = os.path.join(REPO_ROOT, "events.json")
STALE_THRESHOLD_DAYS = 7


def load_events():
    """Load events.json from the repo root."""
    with open(EVENTS_FILE, "r") as f:
        return json.load(f)["events"]


def check_events():
    """Check all events for staleness. Returns list of issues."""
    events = load_events()
    today = datetime.now().date()
    issues = []

    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        days_past = (today - event_date).days
        status = event["status"]

        # Flag events that are past their date but not marked as past/archived
        if days_past > 0 and status in ("upcoming", "active"):
            issues.append({
                "id": event["id"],
                "name": event["name"],
                "page": event["page"],
                "type": event["type"],
                "date": event["date"],
                "status": status,
                "days_past": days_past,
                "severity": "error",
                "message": (
                    f"Event date {event['date']} has passed ({days_past} days ago) "
                    f"but status is still '{status}'"
                ),
            })

        # Warn about events marked as past but not yet archived/updated
        if status == "past" and days_past > STALE_THRESHOLD_DAYS:
            if event["type"] == "recurring" and not event.get("next_date"):
                issues.append({
                    "id": event["id"],
                    "name": event["name"],
                    "page": event["page"],
                    "type": event["type"],
                    "date": event["date"],
                    "status": status,
                    "days_past": days_past,
                    "severity": "warning",
                    "message": (
                        f"Recurring event is {days_past} days past with no next_date set. "
                        f"Update dates for the next session."
                    ),
                })
            elif event["type"] == "one-time":
                issues.append({
                    "id": event["id"],
                    "name": event["name"],
                    "page": event["page"],
                    "type": event["type"],
                    "date": event["date"],
                    "status": status,
                    "days_past": days_past,
                    "severity": "warning",
                    "message": (
                        f"One-time event is {days_past} days past. "
                        f"Consider archiving the page."
                    ),
                })

        # Check that the page file actually exists
        page_path = os.path.join(REPO_ROOT, event["page"])
        if not os.path.isfile(page_path):
            issues.append({
                "id": event["id"],
                "name": event["name"],
                "page": event["page"],
                "type": event["type"],
                "date": event["date"],
                "status": status,
                "days_past": days_past,
                "severity": "error",
                "message": f"Page file '{event['page']}' not found",
            })

    return issues


def main():
    if not os.path.isfile(EVENTS_FILE):
        print("No events.json found. Skipping event check.")
        sys.exit(0)

    issues = check_events()

    if not issues:
        events = load_events()
        print(f"Event check passed. {len(events)} event(s) checked, 0 issues found.")
        sys.exit(0)

    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]

    if errors:
        print("EVENT CHECK FAILED:")
        for issue in errors:
            print(f"  ERROR: {issue['name']} ({issue['page']}) — {issue['message']}")

    if warnings:
        print("EVENT WARNINGS:")
        for issue in warnings:
            print(f"  WARNING: {issue['name']} ({issue['page']}) — {issue['message']}")

    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) found.")

    # Exit 1 only on errors (stale upcoming/active events)
    # Warnings (past events needing attention) don't block deploy
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
