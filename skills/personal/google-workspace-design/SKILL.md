---
name: google-workspace-design
description: Apply Greg Tate's personal visual design to native Google Docs and Google Sheets, including the shared palette, fonts, document components (title block, callouts, code blocks, tables, status chips), and the task-tracker layout (Overview, banded data tabs, status colors). Use when creating, formatting, or restyling a native Google Doc or Sheet, including files produced by the documentation and implementation-planning skills.
metadata:
  author: Greg Tate
  version: "1.3.2"
---

# Design native Google Docs and Sheets

Give every native Google Doc and Sheet the same polished, colorful, readable
look. Other skills decide what a file contains; this skill decides how it looks.
Apply it only to native Google files. Do not change another skill's format
default: if a skill or the user calls for Word or Excel, deliver that format.

## Sources

| File | Use |
| --- | --- |
| [Palette](references/palette.md) | Shared colors, status colors, and fonts. Read first. |
| [Docs spec](references/docs-spec.md) | Page setup, type scale, components, build rules, and checks for Docs |
| [Sheets spec](references/sheets-spec.md) | Workbook settings, data tabs, the tracker Overview, build rules, and checks for Sheets |

Master files render every component and can serve as ChatGPT template reference
files. Both live in the [Agent Toolkit Templates](https://drive.google.com/drive/folders/1gm07fxx16bvRZuDfAH5idGONyFDXbZiw) folder in Greg's personal Google Drive (folder ID
`1gm07fxx16bvRZuDfAH5idGONyFDXbZiw`); keep every master there:

- [Personal Doc Template (master)](https://docs.google.com/document/d/1kIyDWS-94bJnd8DMOh0CyuT0KQCYLdX8f-RK_UPj5kY/edit)
- [Personal Tracker Template (master)](https://docs.google.com/spreadsheets/d/1wqDjwWAfDV8x-0xfHKqttQSARyZORg2QpGeIzEgxdRw/edit)

When a master file and a spec disagree, follow the spec and report the mismatch.

## Workflow

1. **Settle the content first.** Draft with the skill that owns the content
   (documentation skills for Docs, implementation-planning for trackers). Then map
   each part to a component in the matching spec. Choose a component because the
   content calls for it, not to add color.
2. **Translate source markup, never copy it.** Use the Docs spec's label mapping
   (section 5.7): `**Label:** text` becomes a run-in label with plain text after
   it; Important, Warning, and Stop point lines become callouts; fenced code and
   runnable commands become code blocks; typed numbering becomes a real list;
   settings become list items and schemas become data tables; identifiers
   become inline code. Write procedure steps in the Purpose, Action, Expected
   pattern.
3. **Build in the order the spec gives.** Docs: insert content, then named
   paragraph styles, then fonts and colors, then table cell styles, then bullets.
   Sheets: formatting, validation, and conditional formats first, then values and
   formulas.
4. **Format explicitly.** Set fonts, sizes, and colors on every Docs run and every
   Sheets range; never rely on Google's default styles. Reset each new Docs
   block to plain body text before styling its label, because inserted text
   inherits the bold and font of the text before it.
5. **Verify by reading the file back** against the spec's checklist, and fix
   every failure before reporting. For Docs, run the section 7 audit: the
   script audit when the saved read can reach Python, otherwise the read audit
   on your own fresh read. Never ask the user to export the Doc, and never
   report compliance without an audit. If you cannot inspect a rendered view, say so
   rather than claiming visual quality from the read-back alone.

## Editing an existing file

- When adding to a file that already uses this design, match its components
  exactly; do not restyle what is already there.
- Restyle an existing file only when the user asks. Change formatting, not
  content, and preserve comments, suggestions, formulas, links, and history.
- When a file uses another design, keep it unless the user asks to convert it.

## Common failures to check for

- Whole paragraphs in bold where only the label should be bold.
- Commands set inline after `Action:` instead of in a code block below it.
- Important, Warning, or Stop point notes left as bold paragraphs instead of callouts.
- Typed list markers (`Rule 1`, `1.`, `-`) instead of real lists.
- A line ending with a colon followed by loose one-line paragraphs instead of a
  list or table (`Action: Initial retention:` then `14 days` on its own line).
- The reverse fix: a one-item list made to satisfy the colon rule, or a sentence
  split around a list (`Set:`, one item, then `for Include-tagged articles.`).
  One item is one sentence.
- A label on its own line above its value (`Function`, then `CollectInoreader`),
  or loose `Label: value` paragraphs that belong in a list or two-column table.
- Flows written as arrow chains instead of numbered lists.
- Empty list items around tables, and one-column tables of field names.
- Fixing an audit count instead of the structure behind it.
- Field, table, and ID names in plain text instead of inline code.
- Em dashes, and double-numbered headings (`3. Phase 2 ...`).

## Report

Link the file, report the audit counts (paragraphs with excess bold, commands
outside code blocks, callouts created), name any component the tools could not
apply and what was used instead, and state whether the layout was checked
visually or only by read-back.
