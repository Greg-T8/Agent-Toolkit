# Palette and type

Version 1.1.0, November 25, 2026. This file is the single source of color and
font values for both the [Docs spec](docs-spec.md) and the
[Sheets spec](sheets-spec.md). Change a value here, then update both master
files, which live in the [Agent Toolkit Templates](https://drive.google.com/drive/folders/1gm07fxx16bvRZuDfAH5idGONyFDXbZiw) Drive folder.

## Principles

- **Color carries meaning.** Each accent has one job. Body text is never colored,
  and no color is decorative.
- **Restraint per view.** Show at most two or three accent colors in one view,
  apart from status values, which are colored by definition.
- **Accessible contrast.** Every text and fill pair below passes WCAG AA (4.5:1).
  Check contrast before adding a pair.

## Colors

API colors use `rgbColor` values from 0 to 1 (Docs and Sheets use the same form).

| Role | Hex | rgbColor (red, green, blue) | Used for |
| --- | --- | --- | --- |
| Ink | `#1B2A41` | 0.106, 0.165, 0.255 | Titles, Heading 1 and 3, table and sheet header fill |
| Teal | `#0B7A75` | 0.043, 0.478, 0.459 | Heading 2, section headings, title-block rule, code rule, In Review |
| Teal tint | `#EDF6F5` | 0.929, 0.965, 0.961 | In Review fill |
| Body | `#24303F` | 0.141, 0.188, 0.247 | All body, list, table, cell, and code text |
| Meta | `#5F6B7A` | 0.373, 0.420, 0.478 | Subtitles, metadata, captions, Heading 4, neutral statuses |
| Gray tint | `#EEF1F4` | 0.933, 0.945, 0.957 | Not Started, Deferred, Cancelled, Superseded fill |
| Note | `#1D5FBF` | 0.114, 0.373, 0.749 | Note callout, links, In Progress, Focus |
| Note tint | `#EAF2FD` | 0.918, 0.949, 0.992 | Note and In Progress fill |
| Tip | `#276E2B` | 0.153, 0.431, 0.169 | Tip callout, Done, Approved, Accepted, Next action |
| Tip tint | `#EAF5EA` | 0.918, 0.961, 0.918 | Tip and Done fill |
| Warning | `#9A5B00` | 0.604, 0.357, 0.000 | Warning callout, Draft, Proposed, High priority |
| Warning tint | `#FFF4DE` | 1.000, 0.957, 0.871 | Warning, Draft, and Proposed fill |
| Risk | `#B3261E` | 0.702, 0.149, 0.118 | Risk callout, Blocked, Critical priority, Blocker |
| Risk tint | `#FDECEA` | 0.992, 0.925, 0.918 | Risk and Blocked fill |
| Decision | `#6B3FA0` | 0.420, 0.247, 0.627 | Decision callout, Decisions tab color |
| Decision tint | `#F2ECFA` | 0.949, 0.925, 0.980 | Decision callout fill |
| Code fill | `#F1F3F5` | 0.945, 0.953, 0.961 | Code block fill (Docs) |
| Band | `#F4F7F9` | 0.957, 0.969, 0.976 | Banded rows, summary tiles |
| Border | `#D5DBE1` | 0.835, 0.859, 0.882 | Table and row borders |
| White | `#FFFFFF` | 1, 1, 1 | Header text, unbanded rows |

Lowest contrast pairs: Teal on Teal tint 4.7:1, Meta on Gray tint 4.8:1, Tip on
Tip tint 5.6:1. White on Ink is 14.4:1.

## Status colors

One vocabulary, used for Docs chips and Sheets status cells. Status text is
bold, in the text color, on the fill.

| Status | Text | Fill | Extra |
| --- | --- | --- | --- |
| Not Started | Meta | Gray tint | |
| Draft | Warning | Warning tint | |
| In Progress | Note | Note tint | |
| In Review | Teal | Teal tint | |
| Blocked | Risk | Risk tint | |
| Done | Tip | Tip tint | |
| Approved, Accepted | Tip | Tip tint | |
| Proposed | Warning | Warning tint | |
| Deferred | Meta | Gray tint | Italic |
| Cancelled, Superseded | Meta | Gray tint | Strikethrough |

## Fonts

All are Google Fonts, available in Docs and Sheets.

| Font | Role |
| --- | --- |
| Poppins | Titles, Heading 1 and 2, sheet titles, section headings, summary numbers |
| Source Sans 3 | All other text |
| JetBrains Mono | Code, and IDs in trackers |

Docs supports font weights (Poppins 600, Source Sans 3 600). Sheets supports only
regular and bold, so use bold where the Docs spec says 600.
