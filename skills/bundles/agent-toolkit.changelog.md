# Agent Toolkit bundle changelog

## 1.3.4 - 2026-11-27

- Removed the `markdown-link-resolver`, `grill-me`, and `grilling` skills from the bundle selection.
- Updated the paths for the retained `coding-guidelines`, `implementation-planning`, `editorial-style`, and `google-workspace-design` skills to reflect their themed folders. No skills were added in this selection change.

## 1.3.3 - 2026-11-25

- Refresh the bundled PowerShell style guide to reference `New-SkillArchive.ps1` and include the current command alias guidance.

## 1.3.2 - 2026-11-25

- Completes the Google Sheets Overview updates: merge the title, subtitle, and metadata across A:F so they are not clipped; use Navy for the title; and align the master tracker builder and verification checklist with the spec. These updates were present in the source after the 1.3.1 archive was built.

## 1.3.1 - 2026-11-25

- Palette 1.2.0 adds Navy (`#1B3A6B`, 11.3:1 on white) for document and Overview titles and Heading 1, and Plum (`#8E2F5E`, 7.7:1 on white) for inline code and the code block's left rule. Ink keeps Heading 3, run-in labels, summary numbers, and header fills; Teal keeps Heading 2, the title-block rule, and In Review. Code block text stays Body.
- Docs spec 1.6.0 and the Sheets spec match. The master Doc, the master tracker's Overview title, and both build scripts are updated.
- Sheets spec: the Overview title, subtitle, and metadata line are merged across A:F, because the tab's base format clips text at the cell edge. The master tracker and `build_master_tracker.py` match, and the checklist checks it.
- `editorial_check.py`: the serial-comma check no longer fires when the second item opens with a preposition or "available" (39 regression cases).

## 1.3.0 - 2026-11-25

- Added the `editorial-style` skill: Greg's house editorial style for all professional writing, including emails and messages. One decision register resolves the Microsoft Writing Style Guide (primary), Google developer documentation style, plain-language guidance, and Chicago, carried over from the Deliverable Accelerator's editorial conventions with the Quisitive-specific adaptations removed and the house rules added (US English, no em dashes, title-case document titles, real values over placeholders). It also adds information decomposition with worked examples, message guidance, adapted principles files for each authority, and `scripts/editorial_check.py` (ported from the Accelerator's `qeditorial.py`, with a Markdown and plain-text front end, house checks, and 35 regression cases). It takes precedence over the community writing skills in the bundle.
- `google-workspace-design` 1.4.0 and Docs spec 1.5.0: the editorial-style skill governs a Doc's text. `audit_doc.py` loads `editorial_check.py` from the sibling skill and reports its enforced checks as the hard check "editorial issues" and its decomposition review as an advisory; it fails rather than skipping when the checker is missing, unless `--no-editorial` is passed. The read audit gains item 12, and drafts are checked as Markdown before building. The master Doc's one semicolon note is fixed.
- `implementation-planning` 0.1.2: plan text follows the editorial-style register and is checked before building.

## 1.2.8 - 2026-11-25

- Docs spec 1.4.3: the document title uses title case (minor words lowercase unless first or last; product and identifier casing kept); the subtitle and headings stay in sentence case. The master Doc's title is now "Personal Document Template".
- `scripts/audit_doc.py` adds a hard check for a title not in title case.

## 1.2.7 - 2026-11-25

- Docs spec 1.4.2: items under a list item that ends with a colon are nested one level inside it, so a numbered procedure continues after them, with the Docs API method for nesting existing items. The read audit includes it.
- `scripts/audit_doc.py` adds a hard check for sub-lists that are not nested.

## 1.2.6 - 2026-11-25

- Docs spec 1.4.1: no empty paragraph between a paragraph or heading and the table after it, with the method for removing one (delete the preceding paragraph's newline, since the API refuses to delete the newline before a table, then restyle it). The checklist and read audit include it.
- `scripts/audit_doc.py` adds a hard check for blank paragraphs before a table, and no longer suggests a schema table for a list that is mostly bare field names.

## 1.2.5 - 2026-11-25

- Docs spec, after the revised News Aggregator plan passed the 1.2.4 audit while still fragmented (35 one-item lists, 15 labels split from their values, 6 arrow chains, 4 sentences split around a list): a list holds two or more items and one item is a sentence; a sentence never continues after a list; a label and its value share a paragraph, with six or more pairs or current-to-target mappings in a two-column table; arrow flows become numbered lists; no empty list items or one-column tables. The mapping table, checklist, and read audit gained matching rows, and a rule against changing structure only to bring an audit count to 0.
- `scripts/audit_doc.py` adds seven hard checks: one-item lists after a lead-in, sentences split across a list, arrow chains, labels split from values, settings outside a list, empty list items, and one-column tables. The master Doc still passes.

## 1.2.4 - 2026-11-25

- Docs spec section 7 now has two audit routes: the script audit when the saved `read_doc` result can reach Python, and a read audit (eight element-by-element checks on the agent's own fresh read) when the connector and the Python sandbox are separate, as in ChatGPT. The skill never asks the user to export a Doc for auditing, never reports compliance without an audit, and never presents a read audit as a script result.
- `scripts/audit_doc.py` no longer flags a "Do not" sentence that leads a list, exempts one spacer paragraph between tables, and reports field lists that should be schema tables as an advisory. It can also audit a Markdown export for review outside the skill workflow.

## 1.2.3 - 2026-11-25

- Docs spec 1.3.0, after the News Aggregator plan review (bold labels now correct; structure was the problem): a line ending with a colon must be followed by a list or table; settings are list items with run-in labels; schemas are data tables; every identifier in running text is inline code; Actions that set several values use a lead-in and a list; standalone "Do not" and "Defer until" sentences become Warning callouts; one heading-numbering scheme with no double numbers; no em dashes.
- Added `scripts/audit_doc.py`, which checks a saved `read_doc` result against the Docs spec and exits 1 until every hard check passes. The master Doc passes; the Hermes guide and News Aggregator plan fail on their known defects.
- Added a rendered `OPS-04` settings step (lead-in list, schema table, Warning callout) to the master Doc and its build script.

## 1.2.2 - 2026-11-25

- Recorded the Agent Toolkit Templates Drive folder that holds the master Doc and master tracker.
- Added procedure-step guidance to the Docs spec after a ChatGPT-revised runbook bolded 63 of 133 body paragraphs and set every command inline: run-in labels (semibold Ink, ending at the colon), the Purpose, Action, Expected step pattern, a source-label-to-component mapping, a rule that every runnable command gets a code block, and the inherited-style build rule behind the bold.
- Added bold, code, and component audits to the Docs checklist, a common-failures list and audit counts to the skill's report, and a rendered "Procedure steps" section to the master Doc and its build script.

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

