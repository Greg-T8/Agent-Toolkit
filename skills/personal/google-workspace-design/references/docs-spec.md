# Google Docs spec

Version 1.1.0, November 25, 2026. This spec is the canonical definition of the
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

Line spacing is 115% everywhere except code (100%). Headings use sentence case;
never type section numbers or list markers as text.

Inline elements:

- **Links:** Note color, underlined.
- **Inline code:** JetBrains Mono 400, 10 pt, Body color, no fill.
- **Bold:** for UI labels and strings the reader looks for on screen, not for
  emphasis of whole sentences.

## 5. Components

### 5.1 Title block

Three paragraphs, in order:

1. Title (document name).
2. Subtitle naming the document type, for example "Implementation plan" or
   "Decision record".
3. Metadata line: a status chip, two spaces, then `Version X.Y  |  Updated
   <Month D, YYYY>  |  Owner: <name>`, with two spaces around each bar. The
   paragraph has a bottom border: Teal, 2 pt, padding 6 pt, solid.

Use real values. Omit a field that is genuinely unknown rather than writing a
placeholder.

### 5.2 Lists

- Bulleted: `BULLET_DISC_CIRCLE_SQUARE`. Numbered: `NUMBERED_DECIMAL_ALPHA_ROMAN`.
- Apply bullets last, after paragraph and text styles.
- Put an introductory sentence, ending with a colon, before a numbered procedure.

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

Use a table only for data the reader scans or compares. Use a list for one-
dimensional items.

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
   empty paragraph after every table; use it as the next insertion point.
6. **Separate adjacent tables** (for example, consecutive callouts) with one
   empty `NORMAL_TEXT` paragraph whose newline is 6 pt and space below 0.
7. **Leave one normal paragraph after the last table** in the document.
8. **Zero-width borders are valid** and are how callouts and code blocks hide
   their top, right, and bottom edges.
9. **Read-back normalization is expected.** The API may report weight 700 as
   `bold: true` with weight 400, and may omit a size that equals the named
   style's own size. Treat these as correct.

## 7. Verification checklist

Read the Doc back after building and confirm:

- [ ] Title block: Title, Subtitle, and metadata line in order, with the Teal rule.
- [ ] Every heading uses its named style, font, size, color, and keep-with-next.
- [ ] Every text run has an explicit font and color (no Arial or default black).
- [ ] Callouts and code blocks have the right fill, left border, and zero-width
      other borders; adjacent tables have a spacer paragraph between them.
- [ ] Data tables have the Ink header row pinned, banding, borders, and a
      semibold first column; chips use only the listed words and colors.
- [ ] Lists use real bullets or numbering, not typed markers.
- [ ] No empty headings, double blank paragraphs, or blank paragraphs at the end
      beyond the final one Google requires.
- [ ] If a rendered view is available, check each page for headings stranded at
      page bottoms and cells that wrap badly. Otherwise, say the layout was
      verified by read-back only.

## 8. Maintenance

Change the design in this spec (or the palette) first, then update the master
Doc to match, then rebuild and re-import the Agent Toolkit bundle. Keep the
master Doc, and any new Docs master, in the Agent Toolkit Templates folder. A template
change reaches new documents only after all three steps. Existing documents keep
their formatting until restyled. `scripts/build_master_doc.py` regenerates the
master Doc's `batchUpdate` requests; update it with the spec.
