#!/usr/bin/env python3
"""Regression cases for editorial_check.py. Run: python test_editorial_check.py

Each case is (text, expected): expected is True when an enforced check must
fire and False when the text is correct writing that must pass.
"""

import importlib.util
import pathlib
import sys

spec = importlib.util.spec_from_file_location(
    "editorial_check", pathlib.Path(__file__).with_name("editorial_check.py"))
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)

PROSE = [
    # Serial comma
    ("The review covers backups, restores and retention.", True),
    ("The review covers backups, restores, and retention.", False),
    ("Sections 5.6, 5.8, 8 and 14 changed.", True),
    ("If so, delete them and start again.", False),
    ("When the master and a spec disagree, follow the spec and report it.", False),
    ("It excludes Git metadata, Python caches and bytecode, and virtual environments.", False),
    ("Select clear, not uncheck or deselect.", False),
    ("Use one or more vaults, two regions, or more.", False),
    ("Warm, not effusive. Professional and friendly.", False),
    ("It considers the October 14, 2026, review and the cost.", False),
    ("It covers the writing the bundle produces, including emails and messages.", False),
    ("Rules are 1 px solid, between rows and under the header.", False),
    ("All are Google Fonts, available in Docs and Sheets.", False),
    # Word list and filler
    ("Use the CLI, e.g. Azure CLI.", True),
    ("Use the CLI, for example, the Azure CLI.", False),
    ("In order to restore, open the vault.", True),
    ("The phrase \"in order to\" is filler.", False),
    ("Servers stay on-premise.", True),
    ("Servers stay on-premises.", False),
    ("Add the IP to the whitelist.", True),
    ("Add the IP to the allow list.", False),
    # Dashes
    ("The vault holds 12 items \u2014 all protected.", True),
    ("The vault holds 12 items - all protected.", True),
    ("The window is 10–15 minutes.", False),
    ("Release 1.3.0 - 2026-11-25 shipped.", False),
    # Identifiers
    ("The vault rsv-contoso-prod-01 holds 12 items.", True),
    ("The vault `rsv-contoso-prod-01` holds 12 items.", False),
    ("Use a read-only, end-to-end, noun-plus-verb test.", False),
]

HEADINGS = [
    ("Scope And Approach", True),
    ("Scope and approach", False),
    ("Configure Azure Monitor Agent", False),
    ("Other", True),
    ("Review limitations", False),
    ("RET-01: Retention policy", False),
]

TITLES = [
    ("Microsoft technology intelligence aggregation system", True),
    ("Microsoft Technology Intelligence Aggregation System", False),
    ("Plan for the Migration of Workloads to Azure", False),
]

LINKS = [("here", True), ("Azure Backup overview", False)]


def fires_prose(text):
    issues, _ = ec.check_markdown(text + "\n")
    return bool(issues)


def main():
    failures = []
    for text, want in PROSE:
        if fires_prose(text) != want:
            failures.append(("prose", text, want))
    for text, want in HEADINGS:
        got = bool(ec.check(None, [text], [], []))
        if got != want:
            failures.append(("heading", text, want))
    for text, want in TITLES:
        got = bool(ec.check(text, [], [], []))
        if got != want:
            failures.append(("title", text, want))
    for text, want in LINKS:
        got = bool(ec.check(None, [], [], [], [text]))
        if got != want:
            failures.append(("link", text, want))
    total = len(PROSE) + len(HEADINGS) + len(TITLES) + len(LINKS)
    for kind, text, want in failures:
        print(f"FAIL {kind}: expected {'issue' if want else 'pass'}: {text!r}")
    print(f"{total - len(failures)} of {total} cases pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
