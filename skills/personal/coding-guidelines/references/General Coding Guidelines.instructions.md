---
applyTo: "**"
description: "This file contains the coding standards and guidelines for Copilot."
---

# General Coding Standards

## Comment Header Section

1. Always include a comment section at the top of scripts that describes the program.
2. Include a description and a context field. The context should reflect its context from the book.
3. Identify Greg Tate as the author and note that a coding agent assisted with the work.
4. Include a last-modified date and revision history.
5. Preserve existing dates and revision-history entries. Update the last-modified date and append a revision-history entry when making a substantive change.

## Header Format

Use the following format for the script header comment section. Omit a program-name field because filenames may change.

```powershell
# ---------------------------------------------------------------------------
# Description   : Delete (and optionally purge) Azure AD users listed in a JSON file
# Context       : AZ-104 lab — setup identity baseline
#                 Microsoft Azure Administrator
# Author        : Greg Tate & coding agent
# Last Modified : YYYY-MM-DD
# Revision History:
#   YYYY-MM-DD - Initial version
# ---------------------------------------------------------------------------
```

Use the ISO 8601 date format (`YYYY-MM-DD`). Keep the description concise and wrap continuation lines so their text begins under the description or context value. Add the newest revision-history entry first; keep entries brief and describe the change.

## Commenting Rules

You **must** add comments to all code blocks if and only if there is a blank line immediately above it.

- A “code block” is any of:
- A group of declarations/initializations separated by a blank line.
- A single significant assignment separated by a blank line.
- Each loop (`for`, `while`), `if` / `else if` / `else` body.
- The comment must describe the intent of the code block.
