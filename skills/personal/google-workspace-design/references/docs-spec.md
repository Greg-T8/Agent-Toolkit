# Google Docs spec

Version 1.4.3, November 25, 2026. This spec is the canonical definition of the
personal Google Docs design. Colors, status colors, and fonts come from
[the palette](palette.md). The master Doc,
[Personal Doc Template (master)](https://docs.google.com/document/d/1kIyDWS-94bJnd8DMOh0CyuT0KQCYLdX8f-RK_UPj5kY/edit)
(ID `1kIyDWS-94bJnd8DMOh0CyuT0KQCYLdX8f-RK_UPj5kY`), in the [Agent Toolkit Templates](https://drive.google.com/drive/folders/1gm07fxx16bvRZuDfAH5idGONyFDXbZiw) Drive
folder, renders every component
below. Values in this spec win over the master Doc if the two ever differ.

## 1. Principles

- Follow the principles in [the palette](palette.md).
- **Content picks the component.** Use a callout for a real note, warning, or
  decision, a table for data the reader compares, and a code block for anything
  the reader copies. Do not add components to make a page colorful.
- Do not stack more than two callouts unless the content is a set of distinct
  warnings or decisions.

## 2. Page setup

| Setting | Value |
| --- | --- |
| Format | Pages (not pageless) |
| Page size | US Letter, 612 x 792 pt |
| Margins | 72 pt (1 in) on all sides; text width 468 pt |
| Front matter | Title block only; no cover page, no table of contents |
| Page numbers | Optional; the user adds them with Insert > Page numbers |

## 3. Palette

Use the colors in [the palette](palette.md) by role name (Ink, Teal, Body, Meta,
and so on). This spec names roles, not hex values.

## 4. Typography

Fonts are Google Fonts: **Poppins** for display headings, **Source Sans 3** for
text, **JetBrains Mono** for code. Set the font, weight, size, and color on every
run; do not rely on named-style definitions.

| Element | Named style | Font and weight | Size | Color | Space above / below | Keep with next |
| --- | --- | --- | --- | --- | --- | --- |
| Title | `TITLE` | Poppins 600 | 26 pt | Ink | 0 / 2 pt | No |
| Subtitle | `SUBTITLE` | Source Sans 3 400 | 14 pt | Meta | 0 / 6 pt | No |
| Metadata line | `NORMAL_TEXT` | Source Sans 3 400 | 10 pt | Meta | 0 / 14 pt | No |
| Heading 1 | `HEADING_1` | Poppins 600 | 18 pt | Ink | 20 / 6 pt | Yes |
| Heading 2 | `HEADING_2` | Poppins 600 | 14 pt | Teal | 16 / 4 pt | Yes |
| Heading 3 | `HEADING_3` | Source Sans 3 bold | 12 pt | Ink | 12 / 4 pt | Yes |
| Heading 4 | `HEADING_4` | Source Sans 3 bold | 11 pt | Meta | 10 / 2 pt | Yes |
| Body | `NORMAL_TEXT` | Source Sans 3 400 | 11 pt | Body | 0 / 8 pt | No |
| List item | `NORMAL_TEXT` | Source Sans 3 400 | 11 pt | Body | 0 / 4 pt (last item 8 pt) | No |
| Code caption | `NORMAL_TEXT` | Source Sans 3 bold | 8.5 pt | Meta | 6 / 2 pt | Yes |
| Action line | `NORMAL_TEXT` | Run-in label only | 11 pt | Ink | 0 / 3 pt | Yes |

Line spacing is 115% everywhere except code (100%).

The title uses title case: capitalize every word except articles (a, an, the),
coordinating conjunctions (and, but, or, nor, for, so, yet), and
prepositions of three letters or fewer, unless the word is first or last, and
keep the casing of product names and identifiers. The subtitle and all headings
use sentence case.

Never type list markers as text.

Google Docs cannot number headings automatically. Number headings only when
readers or a tracker cite sections by number, and then use one scheme:

- Heading 1 for a phase: `Phase 2: Common news store`. Do not add a second
  number in front (`3. Phase 2`).
- Heading 2 for a step inside it: `2.5 Configure retention`, or a step ID:
  `RET-01: Configure retention`. No period after the last number.
- Recurring headings such as Purpose and Acceptance criteria stay unnumbered.
- Separate a number or ID from the text with a colon or a space, never a dash.

Inline elements:

- **Links:** Note color, underlined.
- **Inline code:** JetBrains Mono 400, 10 pt, Body color, no fill. Use it for
  every identifier in running text: table, field, column, key, setting, and
  environment variable names (`NewsItems`, `collected_utc`, `PartitionKey`);
  ID formats (`source_platform:stable_source_identifier`); file and folder
  names; and commands or flags named in a sentence. Not for product or service
  names (Azure Table Storage, Inoreader) or ordinary words.
- **Run-in label:** Source Sans 3 600, Ink, ending with the colon, such as
  `Purpose:` or `Action (Ubuntu shell):`. Only the label takes this style; the
  rest of the paragraph is regular body text. See 5.7.
- **Bold:** only for a run-in label, a callout label, a status chip, or a UI
  string the reader finds on screen. Never bold a whole sentence or paragraph.
  A body paragraph whose bold runs past its label is a defect.

## 5. Components

### 5.1 Title block

Three paragraphs, in order:

1. Title (document name), in title case (section 4).
2. Subtitle naming the document type, for example "Implementation plan" or
   "Decision record".
3. Metadata line: a status chip, two spaces, then `Version X.Y  |  Updated
   <Month D, YYYY>  |  Owner: <name>`, with two spaces around each bar. The
   paragraph has a bottom border: Teal, 2 pt, padding 6 pt, solid.

Use real values. Omit a field that is genuinely unknown rather than writing a
placeholder.

- **Punctuation:** no em dashes anywhere. Use a colon between a label and its
  text (`X: X post ID`), parentheses for an aside, and a new sentence otherwise.

### 5.2 Lists

- Bulleted: `BULLET_DISC_CIRCLE_SQUARE`. Numbered: `NUMBERED_DECIMAL_ALPHA_ROMAN`.
- Apply bullets last, after paragraph and text styles.
- Put an introductory sentence, ending with a colon, before a numbered procedure.
- **A list holds two or more parallel items.** One item is a sentence, not a
  list: write `Action: Create the NewsItems table.`, never `Action: Create:`
  followed by a one-item list.
- **A lead-in ending with a colon introduces that list or a table directly.**
  Never follow it with plain one-line paragraphs, and never wrap a single
  fragment in a list to satisfy this rule.
- **Never split a sentence across a list.** Text that continues after an item
  belongs in the same sentence: `Set intake_disposition to include for
  Include-tagged articles.`, not `Set:`, a list item, then `for Include-tagged
  articles.`
- **Label and value stay in one paragraph.** A label never sits alone above its
  value. Two to five related settings are list items with run-in labels
  (`Trigger: Timer`). Six or more label-value pairs, or pairs that map one thing
  to another (current to target, decision to status), are a two-column data
  table.
- **Flows are numbered lists.** A sequence written with arrows (A → B → C)
  becomes a numbered list under a lead-in such as `Collection flow:`, one step
  per item. No paragraph contains two or more arrows.
- **No empty list items.** A spacer paragraph next to a table has no bullet.
- **Nest sub-lists.** Items under a list item that ends with a colon (`5. Record:`)
  are nested one level inside it, in the same list, so the numbering continues
  after them. To nest existing items, delete the bullets on the whole range,
  insert one tab at the start of each sub-item, then apply
  `createParagraphBullets` to the whole range; Google sets the level from the
  leading tabs and removes them. With `NUMBERED_DECIMAL_ALPHA_ROMAN`, nested
  items are lettered.
- When three or more items share the same attributes (for example, field, type,
  and purpose), use a data table instead (5.5).

### 5.3 Callouts

A callout is a 1 x 1 table, 468 pt wide (fixed width), holding one paragraph:
the bold label, two spaces, then the text.

| Type | Label | Accent | Fill | Use for |
| --- | --- | --- | --- | --- |
| Note | `Note` | Note | Note tint | Background the reader should know but can skip |
| Tip | `Tip` | Tip | Tip tint | A shortcut or better way to do the task |
| Warning | `Warning` | Warning | Warning tint | An action that can lose data or time; say what to do instead |
| Risk | `Risk` | Risk | Risk tint | Something that could make the plan fail, and its mitigation |
| Decision | `Decision` | Decision | Decision tint | A choice that was made and the reason for it |

Cell style:

- Background: the type's fill.
- Left border: the type's accent, 4 pt, solid.
- Top, right, and bottom borders: width 0 (color the fill), solid.
- Padding: 7 pt top and bottom, 11 pt left and right.

Text: paragraph `NORMAL_TEXT`, space above and below 0, line spacing 115%.
Label in Source Sans 3 bold in the accent color; text in Source Sans 3 400,
11 pt, Body color. Keep a callout to one to three sentences.

### 5.4 Code block

A caption paragraph followed by a 1 x 1 table, 468 pt wide.

- **Caption:** the shell or language in capitals, such as `POWERSHELL`,
  `AZURE CLI`, `BASH`, or `JSON` (Code caption style).
- **Cell:** background Code fill; left border Teal, 3 pt, solid; other borders
  width 0; padding 7 pt top and bottom, 11 pt left and right.
- **Text:** one paragraph per line, `NORMAL_TEXT`, space 0, line spacing 100%;
  JetBrains Mono 400, 9.5 pt, Body color.
- Keep lines under 90 characters, use straight ASCII quotes, and never use text-level
  shading in place of the table.
- **Every command the reader runs gets a code block, even a one-line command.**
  Never end a label paragraph with a runnable command, and never set a runnable
  command as an inline code run. Inline code (section 4) is only for a name used
  inside a sentence: a command, file, flag, or service the reader does not run at
  that point.
- In a procedure step (5.7), the Action line replaces the caption.

### 5.5 Data table

- **Header row:** fill Ink; text Source Sans 3 bold, 10 pt, white. Pin it as a
  repeating header row (`pinTableHeaderRows`, count 1).
- **Body rows:** text Source Sans 3 400, 10 pt, Body color. First column
  Source Sans 3 600. Rows 2, 4, and so on (counting the first body row as 1) get the
  Band fill; others are white.
- **Borders:** every cell 0.75 pt, Border color, solid.
- **Padding:** 4 pt top and bottom, 7 pt left and right.
- **Paragraphs in cells:** `NORMAL_TEXT`, space 0, line spacing 115%.
- **Widths:** fixed widths that total 468 pt, sized to the content.

Use a table only for data the reader scans or compares, and give it at least two
columns. Use a list for one-dimensional items. A schema (fields with types or
purposes) is always a data table; set the identifier column in JetBrains Mono
9.5 pt instead of semibold. Field names with nothing else to say about them are
a bulleted list of inline-code names, never a one-column table.

### 5.6 Status chips

A chip is the status word in capitals with a no-break space (U+00A0) on each
side, as one run: Source Sans 3 bold, 9 pt, accent text on its tint as the text
background color.

| Chip | Text color | Background |
| --- | --- | --- |
| `DRAFT` | Warning | Warning tint |
| `IN REVIEW` | Teal | Teal tint |
| `IN PROGRESS` | Note | Note tint |
| `APPROVED` | Tip | Tip tint |
| `DONE` | Tip | Tip tint |
| `BLOCKED` | Risk | Risk tint |

Use only these words. A chip in a table cell replaces the cell's text style for
that run.

### 5.7 Procedure steps

Use this pattern for every runbook, implementation, or how-to step. The master
Doc's "Procedure steps" section shows it rendered.

1. **Heading 2** naming the step, with its ID when the plan uses IDs:
   `OPS-03: Verify the scheduler`.
2. **Purpose:** one body paragraph that starts with the run-in label.
3. **Action (where):** an Action line holding only the label, naming where to
   run it (`Action (Windows terminal):`, `Action (Proxmox GUI):`), then the code
   block directly below. For a step with no command, write the instruction in the
   same paragraph after the label, as regular text.
4. **Expected:** a body paragraph that starts with the run-in label and states
   the observable result.
5. Optional, in this order: a callout (see the mapping below), then plain body
   paragraphs for notes such as what to record.

When an Action sets or creates several things (resources, settings, fields),
write the Action as a lead-in ending with a colon (`Action: Set these retention
values:`) and follow it with a real list or a data table, never with one value
per paragraph. The master Doc's `OPS-04` step shows this. When the Action
creates or sets one thing, name it in the Action sentence instead.

When a step has several commands, give each its own Action line and code block,
in order (`Next action after verification:` is a valid label). Do not put a
second command inside an Expected paragraph; make it the next Action.

Map source labels to components, never to bold paragraphs:

| Source label or markup | Component |
| --- | --- |
| `Purpose:`, `Action:`, `Expected:`, `Result:`, `Evidence:`, `Prerequisites:`, `Rollback:`, `Next action:` | Run-in label (5.7) |
| `Note:`, `Important:`, `Context:` | Note callout |
| `Tip:` | Tip callout |
| `Warning:`, `Caution:`, `Safety gate:` | Warning callout |
| `STOP POINT:`, `Review gate:`, `Approval gate:` | Warning callout labeled `Stop point` |
| `Risk:` | Risk callout |
| `Decision:` | Decision callout |
| `Rule 1:`, `Step 1:`, `1.` and other typed numbering | Numbered list item; a rule name may be a run-in label |
| `Objective:`, `Scope:`, `Summary:` | Plain body paragraph (no label styling) |
| A fenced code block, or a command in backticks the reader must run | Code block (5.4) |
| A standalone sentence that forbids or delays an action (`Do not ...`, `Never ...`, `Defer ... until ...`) | Warning callout |
| `Setting: value` lines, or a label on one line and its value on the next | List items with run-in labels; a two-column data table for six or more |
| `Current: X` then `Then: Y` pairs, or a register of decisions and statuses | Two-column data table |
| A flow written with arrows (`A → B → C`) | Numbered list under a lead-in |
| A lead-in with only one item after it | One sentence, without the colon |
| A list of fields, columns, or keys with types or purposes | Data table (5.5) |
| `**bold**` around a whole sentence | Regular body text |

## 6. Build rules (Docs API)

These rules came from building and verifying the master Doc.

1. **Append forward.** Insert each block at the end of the body, so indexes
   computed for earlier content stay valid.
2. **Order inside a block or batch:** insert text and tables, then
   `updateParagraphStyle` (named style and spacing), then `updateTextStyle`,
   then `updateTableCellStyle` and column widths, then `createParagraphBullets`
   and `pinTableHeaderRows`.
3. **A named style resets text formatting.** Setting `namedStyleType` on a
   paragraph clears direct font, size, and color on its runs. Always set text
   formatting after the named style, and reapply it if a named style changes.
4. **Name only the fields you set** in every `fields` mask. Never use `*`.
5. **Insert a table at the preceding paragraph's `endIndex - 1`.** Google adds an
   empty paragraph after every table; use it as the next insertion point. No
   empty paragraph sits between a paragraph and the table after it. To remove
   one from an existing Doc, delete the preceding paragraph's own newline (its
   `endIndex - 1` to `endIndex`), because the API refuses to delete the newline
   directly before a table; then reapply that paragraph's named style, spacing,
   and text style, which the merge takes from the empty paragraph.
6. **Separate adjacent tables** (for example, consecutive callouts) with one
   empty `NORMAL_TEXT` paragraph whose newline is 6 pt and space below 0.
7. **Leave one normal paragraph after the last table** in the document.
8. **Zero-width borders are valid** and are how callouts and code blocks hide
   their top, right, and bottom edges.
9. **Read-back normalization is expected.** The API may report weight 700 as
   `bold: true` with weight 400, and may omit a size that equals the named
   style's own size. Treat these as correct.
10. **Inserted text inherits the style before it.** Text inserted after a bold
    label, a chip, or a code run takes that run's bold, font, color, and
    background. After inserting a block, first set the whole new range to plain
    body text (`bold: false`, Source Sans 3 400, 11 pt, Body color, no
    background), then style only the label, chip, or inline-code characters.
    Applying bold to a whole paragraph range is never correct in body text.
11. **Code blocks are tables, built in two passes if needed.** Insert the 1 x 1
    table at the Action line's `endIndex - 1`; its cell's text goes at that index
    plus 4. If unsure, insert the table, read the Doc back, and insert the code
    at the cell's `startIndex + 1`. Do not fall back to inline code when the
    table step is hard.

## 7. Verification checklist

Read the Doc back after building and confirm:

- [ ] Title block: Title, Subtitle, and metadata line in order, with the Teal rule.
- [ ] Every heading uses its named style, font, size, color, and keep-with-next.
- [ ] Every text run has an explicit font and color (no Arial or default black).
- [ ] Callouts and code blocks have the right fill, left border, and zero-width
      other borders; adjacent tables have a spacer paragraph between them, and
      no empty paragraph sits between a paragraph and the table after it.
- [ ] Data tables have the Ink header row pinned, banding, borders, and a
      semibold first column; chips use only the listed words and colors.
- [ ] Lists use real bullets or numbering, not typed markers.
- [ ] **Bold audit:** in every body paragraph outside tables, bold and semibold
      characters stop at the run-in label. Count paragraphs whose bold runs past
      the label; the count must be 0.
- [ ] **Code audit:** every Action line is followed by a code block unless its
      instruction is written after the label; no runnable command appears as an
      inline code run or as plain text; no JetBrains Mono run outside a table is
      longer than one name.
- [ ] **Component audit:** every Note, Important, Warning, Stop point, Risk,
      Decision, or Tip from the source is a callout table, not a bold paragraph.
      A runbook with commands but zero tables fails.
- [ ] **Structure audit:** every line ending with a colon is followed by a list
      of two or more items or a table; no sentence continues after a list; no
      label sits alone above its value; no setting sits in a loose paragraph;
      no paragraph holds an arrow chain; no list item is empty; no data table
      has one column.
- [ ] **Identifier audit:** table, field, key, and ID-format names in running
      text are inline code.
- [ ] **Heading and punctuation audit:** no em dashes anywhere; headings follow
      one numbering scheme with no double numbers or trailing periods.
- [ ] No empty headings, double blank paragraphs, or blank paragraphs at the end
      beyond the final one Google requires.
- [ ] If a rendered view is available, check each page for headings stranded at
      page bottoms and cells that wrap badly. Otherwise, say the layout was
      verified by read-back only.

Audit the Doc after every build or revision, before reporting. Use the first
route the session supports.

- **Script audit:** when the `read_doc` result can be saved to a file that
  Python can open, run `python scripts/audit_doc.py DOC.json`. It exits 1 until
  every hard check passes; its identifier, fragment, and schema-table counts
  are advisory but still map to rules in this spec.
- **Read audit:** when the Docs response cannot reach Python (for example, the
  connector and the Python sandbox are separate), audit your own fresh
  `read_doc` result element by element. Never ask the user to export or upload
  the Doc for auditing. Check, in body order:
  1. Bold: in each paragraph outside tables, no run with `bold` or weight 600
     or more continues past the first colon.
  2. Commands: no runnable command (a line starting with a CLI name, a
     cmdlet, or a path to run) sits in a paragraph; each is in a code block.
  3. Lead-ins: each paragraph ending with a colon is followed, skipping no
     paragraphs, by two or more list items or a table. A lead-in to fields,
     columns, or properties is followed by a data table, not a list. No
     paragraph after a list starts with a lowercase word.
  4. Callouts: no paragraph starts with Note, Important, Warning, Tip, Risk,
     Decision, Stop point, Do not, Never, or Defer unless it is inside a 1x1
     callout table or leads a list.
  5. Punctuation and headings: the title is in title case; no U+2014
     character anywhere; no heading such as
     `2.1. Name`, `Phase 2.1 Name`, or `RET-01 - Name`.
  6. Fonts: every text run sets `weightedFontFamily`, and none is Arial.
  7. Empty paragraphs: no two in a row, except one spacer between tables, and
     none between a paragraph or heading and the table after it.
  8. Identifiers: every snake_case name, table name, key, and ID format in a
     paragraph is a JetBrains Mono run.
  9. Labels and settings: no paragraph of three words or fewer without end
     punctuation is followed by a paragraph holding its value; no `Label: value`
     paragraph with a short value sits outside a list, except the procedure
     run-in labels (Purpose, Action, Expected, and the like).
  10. Flows: no paragraph contains two or more arrows.
  11. Lists and tables: no bulleted paragraph is empty; no data table has one
     column; every list item ending with a colon has its sub-items nested one
     level deeper, and a numbered list does not restart after them.

  Fix the structure a failing check describes; never add a list marker, a
  table, or a colon only to bring a count to 0.

  Fix each failure and read again until every count is 0. Report the method as
  "read audit" and give the count for each check; never describe a read audit
  as a script result.

## 8. Maintenance

Change the design in this spec (or the palette) first, then update the master
Doc to match, then rebuild and re-import the Agent Toolkit bundle. Keep the
master Doc, and any new Docs master, in the Agent Toolkit Templates folder. A template
change reaches new documents only after all three steps. Existing documents keep
their formatting until restyled. `scripts/build_master_doc.py` regenerates the
master Doc's `batchUpdate` requests; update it with the spec.
