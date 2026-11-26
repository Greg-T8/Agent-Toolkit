# Google Sheets spec

Version 1.0.0, November 25, 2026. This spec is the canonical definition of the
personal Google Sheets design, written first for the implementation-planning
task tracker. Colors, status colors, and fonts come from
[the palette](palette.md). The master tracker,
[Personal Tracker Template (master)](https://docs.google.com/spreadsheets/d/1wqDjwWAfDV8x-0xfHKqttQSARyZORg2QpGeIzEgxdRw/edit)
(ID `1wqDjwWAfDV8x-0xfHKqttQSARyZORg2QpGeIzEgxdRw`), in the [Agent Toolkit Templates](https://drive.google.com/drive/folders/1gm07fxx16bvRZuDfAH5idGONyFDXbZiw) Drive
folder, renders every component
with a small sample project. Values in this spec win over the master if the two differ.

Content, tabs, and columns belong to the skill that produces the workbook (for
trackers, implementation-planning's artifact contract). This spec only decides
how they look. Keep its column order and names when they exist.

## 1. Principles

- Follow the principles in [the palette](palette.md).
- **Data tabs stay data.** The header is in row 1 with no title rows above it, so
  filters, dropdowns, open-ended formulas, and new rows keep working.
- **The Overview is the only designed page.** It carries the title block, summary
  tiles, status counts, phase gates, and the current-focus block.
- **Formatting extends to new rows.** Apply formats, validation, and conditional
  formatting to open-ended column ranges (from row 2 to the end), and band with
  alternating colors rather than by filling rows.
- **Every number on the Overview is a formula** over the Tasks tab.

## 2. Workbook settings

| Setting | Value |
| --- | --- |
| Gridlines | Hidden on every tab |
| Base text | Source Sans 3, 10 pt, Body color, on every tab |
| Tab colors | Overview Ink, Tasks Teal, Decisions Decision, Change Log Meta, References Note |
| Tab order | Overview, Tasks, Decisions, Change Log, References |
| Locale | United States; dates display as `mmm d, yyyy` (Nov 25, 2026) |

## 3. Data tabs

Applies to Tasks, Decisions, Change Log, References, and any other register.

| Element | Format |
| --- | --- |
| Header row | Row 1, frozen. Ink fill (from the banding header color), white bold text, vertically centered, wrapped, 32 px high |
| Body cells | Source Sans 3, 10 pt, Body color, top-aligned, clipped; long-text columns wrapped |
| ID column | JetBrains Mono, 10 pt, bold, Ink |
| Banding | Alternating colors over rows 1 to 1000: header Ink, first band White, second band Band |
| Row borders | Border color, solid, between rows and under the last row |
| Filter | Basic filter over the header row and all rows |
| Dates | Date format `mmm d, yyyy`; validated as dates where a date is required |
| Versions | Column formatted as plain text before values are written, so 1.10 stays 1.10 |
| Links | Note color text |
| Frozen columns | Tasks only: column A (Task ID) |

### Status and choice columns

Use a dropdown (strict list, chip display) and one conditional-format rule per
value. The rule sets the fill and bold text color from the palette's status
table. Center the column.

| Column | Values |
| --- | --- |
| Tasks: Status | Not Started, In Progress, Blocked, In Review, Done, Deferred, Cancelled |
| Tasks: Priority | Critical (Risk, bold text), High (Warning, bold text), Medium (Body), Low (Meta). Text color only, no fill |
| Decisions: State | Proposed, Accepted, Superseded |
| Overview: Gate status | Not Started, In Progress, Blocked, Accepted |

### Column widths (px)

| Tab | Widths, in column order |
| --- | --- |
| Tasks | 96, 58, 104, 240, 116, 80, 104, 96, 104, 260, 96, 240, 200, 96, 200 |
| Decisions | 104, 104, 300, 360, 140, 104 |
| Change Log | 104, 96, 96, 150, 300, 240, 200, 110 |
| References | 260, 340, 320 |

Wrapped columns: Task / Deliverable, Acceptance, Evidence, Blocker / Notes, and
Next Action on Tasks; Decision and Rationale on Decisions; Change, Rationale, and
Companion Impact on Change Log; all References columns.

## 4. Overview tab

Six columns, 120 px each. Rows are fixed; the layout does not grow. The tab's
base format clips text at the cell edge, so every text block wider than one
column is merged across the columns it needs.

| Rows | Block | Format |
| --- | --- | --- |
| 1 | Title (project name) | Merged A:F; Poppins 20 pt bold, Navy, 40 px row |
| 2 | Subtitle (`Task tracker`) | Merged A:F; Source Sans 3 12 pt, Meta |
| 3 | Metadata line | Merged A:F; 10 pt Meta: `Plan: <plan name> v<X.Y>  |  Tracker v<X.Y>  |  As of <Mon D, YYYY>`; Teal medium bottom border across A:F |
| 4 | Spacer | 10 px |
| 5 to 6 | Summary tiles | Band fill; labels 9 pt Meta in row 5; numbers Poppins 18 pt bold in row 6; thick white vertical borders between tiles |
| 8 | Section heading `Status` | Poppins 12 pt bold, Teal |
| 9 to 16 | Status table | Ink header (Status, Tasks, Definition); one row per status; status cells use the status colors; Definition merged across C:F; Border-color row rules |
| 18 | Section heading `Phase gates` | As row 8 |
| 19 to 22+ | Phase gates | Ink header (Phase, Exit gate, Gate status, Tasks done, Tasks in phase); Phase in JetBrains Mono bold; Exit gate merged B:C; gate status dropdown with status colors |
| 24 | Section heading `Current focus` | As row 8 |
| 25 to 27 | Focus block | Label in A, text merged B:F, wrapped, 28 px rows. Focus: Note tint and Note label. Next action: Tip tint and Tip label. Blocker: Risk tint and Risk label. Each label cell has a thick left border in its color |

Add phase rows as the project needs; keep one row per phase.

### Tile formulas

| Tile | Formula | Number color |
| --- | --- | --- |
| Tasks | `=COUNTA(Tasks!A2:A)` | Ink |
| Active | Tasks minus the Deferred and Cancelled counts from the status table | Ink |
| Done | The Done count from the status table | Tip |
| In Progress | The In Progress count | Note |
| Blocked | The Blocked count | Risk |
| Complete | `=IF(Active=0,0,Done/Active)`, formatted `0%` | Ink |

Status counts use `=COUNTIF(Tasks!$G$2:$G,A10)` filled down. Phase counts use
`COUNTIFS` over the Tasks Phase and Status columns. Gate status is entered by
hand and is never derived from task completion.

## 5. Build rules (Sheets API)

1. A new spreadsheet's first tab is `Sheet1` with `sheetId` 0; rename it to
   Overview and add the other tabs with fixed `sheetId` values (1 to 4).
2. Send formatting first, in `update_spreadsheet` batches of about 60 requests:
   tab properties, base text format over the whole tab, then specific formats,
   merges (`MERGE_ROWS` over a block of rows), borders, banding, filters, widths
   and heights, validation, and conditional formats.
3. Then write each tab's values and formulas in one `update_formulas` call from
   A1. Version columns are already text; in an unformatted cell, prefix
   number-like text with an apostrophe. Write dates as `11/14/2026`; the date
   format displays them.
4. Use open-ended ranges (no `endRowIndex`) for column formats, validation, and
   conditional formats so they cover new rows. Banding and row borders use rows
   1 to 1000.
5. Field masks list full paths, comma-separated, with no parentheses.
6. Sheets has no font weights: use bold for every "600" or "700" in the palette.
7. Status colors come from conditional formatting, not dropdown chip colors,
   because the API cannot set per-option chip colors.

## 6. Verification checklist

- [ ] Tabs, order, and tab colors match section 2; gridlines are hidden.
- [ ] The Overview title, subtitle, and metadata line are each merged across A:F
      and show in full.
- [ ] Every data tab has a frozen Ink header, banding, row borders, and a filter.
- [ ] Status, Priority, State, and Gate status cells show a dropdown, and each value
      shows its palette color.
- [ ] Overview tiles, status counts, and phase counts are formulas, show no
      errors, and agree with the Tasks tab.
- [ ] Dates display as `mmm d, yyyy`; versions keep their trailing zeros.
- [ ] A new row typed under the last task picks up banding, borders, dropdowns,
      and status colors.
- [ ] If a rendered view is available, check that headers wrap cleanly and no
      text is cut off in a way that hides meaning.

## 7. Maintenance

Change this spec (or the palette) first, then update the master tracker, then
rebuild and re-import the Agent Toolkit bundle. Keep the master tracker, and
any new Sheets master, in the Agent Toolkit Templates folder.
`scripts/build_master_tracker.py`
regenerates the master tracker's values and formatting requests.
