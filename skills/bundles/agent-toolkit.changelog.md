# Agent Toolkit bundle changelog

## 1.2.1 - 2026-11-25

- Packaged the current Google Workspace design skill with its shared palette, separate Docs and Sheets specifications, and refreshed tracker workflow in implementation-planning.
- The prior local archive was 1.1.1, so the documented 1.2.0 design updates were present in the configuration but not yet in a packaged archive.

## 1.2.0 - 2026-11-25

- Renamed google-docs-design to google-workspace-design and split its spec into a shared palette, a Docs spec, and a new Sheets spec.
- Added the Google Sheets design for implementation-planning task trackers: an Overview with formula-driven summary tiles, status counts, phase gates, and a focus block; banded data tabs with frozen headers, filters, dropdowns, and status colors. The approved master tracker is the visual reference, and a script regenerates it.
- Changed the In Review status color from blue to teal in both specs so it differs from In Progress.
- Pointed implementation-planning's tracker step at the Sheets spec.

## 1.1.1 - 2026-11-25

- Added Matt Pocock's grill-me dispatcher and its grilling interview guidance so the bundled workflow includes both the entry point and its referenced skill.

## 1.1.0 - 2026-11-25

- Added the google-docs-design skill: a personal palette, type scale, and component recipes (title block, callouts, code blocks, data tables, status chips) for native Google Docs, with the approved master Doc as its visual reference.
- Included the Docs API build rules learned while building the master Doc, a read-back verification checklist, and a script that regenerates the master Doc.

## 1.0.1 - 2026-11-25

- Added Obra's writing-clearly-and-concisely skill for clearer, more concise prose across documentation, messages, reports, explanations, and interface text.

## 1.0.0 - 2026-11-25

- Consolidated the documentation, coding-guidelines, and implementation-planning bundles into one Agent Toolkit plugin containing all eight selected skills.
- Added one configuration, one changelog, and a shared document-and-checkmark icon for future releases.
- Made the unified bundle the packager default and renamed the refresh-and-build command to Build-SkillBundle.ps1, including read-only preview support.
- Preserved the three predecessor changelogs below. Their last locally packaged versions were documentation 0.2.3, coding guidelines 0.1.5, and implementation planning 0.1.0; these do not establish uploaded ChatGPT versions.

## Predecessor release histories

The following histories retain the original release notes and version numbers.

# Documentation bundle changelog

## 0.2.3 — 2026-11-25

- Set the plugin display name to Agent Toolkit - Documentation.

## 0.2.2 â€” 2026-11-25

- No changes to selected skill files, licenses, icon, or selection were detected compared with the local 0.2.1 archive.

## 0.2.1 â€” 2026-11-25

- Rebuilt the bundle. No changes to selected skill files, licenses, icon, or selection were detected compared with the local 0.2.0 archive.


# Coding-guidelines bundle changelog

## 0.1.5 - 2026-11-25

- Added interactive-command, new-script, and existing-script modes to the Shell style guide, aligned with the PowerShell guide.
- Added a required shell script structure and header, with Bash and POSIX portability guidance.

## 0.1.4 — 2026-11-25

- Set the plugin display name to Agent Toolkit - Coding Guidelines.

## 0.1.3 â€” 2026-11-25

- Added a distinct composer icon to test its display in ChatGPT.

## 0.1.2 â€” 2026-11-25

- No substantive guidance changes since 0.1.1; rebuilt from the current maintained sources.

## 0.1.1 â€” 2026-11-25

- Reorganized PowerShell guidance into separate modes for interactive commands, new scripts, and edits to existing scripts.
- Clarified that requested functional changes are allowed in edit mode, while comment-only and formatting-only work preserves behavior.


# Implementation-planning bundle changelog

## 0.1.0 - 2026-11-25

- Added the implementation-planning skill with Word plans and native Google Sheets task trackers as the default paired deliverables.
- Derived planning patterns from the M365 Knowledge Automation, Hermes, and ALZ runner migration examples in Google Drive.
- Added stable cross-references, phased acceptance gates, evidence-based status, and coordinated revision guidance.

