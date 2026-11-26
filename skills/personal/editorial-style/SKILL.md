---
name: editorial-style
description: Apply Greg Tate's house editorial style to any professional writing, including documents, READMEs, plans, guides, specs, Google Docs, emails, and messages. One decision register resolves the Microsoft Writing Style Guide (primary), Google developer documentation style, plain-language guidance, and the Chicago Manual of Style, plus information decomposition and a checker for Markdown and text. Use when drafting, editing, reviewing, or tightening prose. It takes precedence over the other writing and documentation skills in this bundle.
metadata:
  author: Greg Tate
  version: "1.0.0"
---

# Apply the house editorial style

This skill decides how text is written: word choice, capitalization,
punctuation, numbers, sentence and paragraph structure, and the formatting of
text elements. It never decides how a file looks. Fonts, colors, tables, and
callout treatment belong to the format skill in use, such as
`google-workspace-design`.

## Precedence

Apply authorities in this order. When two conflict, the higher one wins.

1. **The user's explicit instruction** for the piece in hand.
2. **The house rules** in [decision register](references/decision-register.md)
   section 1: Greg's own rules, which are stricter than Microsoft in a few
   places (no em dashes, title-case document titles).
3. **The decision register** sections 2 to 7: resolved rules from the
   authorities below. Apply a row without rereading its authority.
4. **The authorities, by jurisdiction** (register section 8): Microsoft for
   terminology and mechanics, then Google for technical structure,
   plain-language guidance for clarity, and Chicago where the others are silent.
5. **Other writing and documentation skills in this bundle.** Use them for
   document structure, templates, and AI-pattern cleanup where this skill is
   silent. Where one disagrees with this skill, this skill wins. For example,
   `technical-documentation` ranks Google above Microsoft, and this skill
   ranks Microsoft first. The overlapping skills are:
   - `technical-documentation`
   - `documentation-authoring`, `documentation-patterns`, and
     `documentation-quality`
   - `avoid-ai-writing` and `writing-clearly-and-concisely`

Nothing overrides an official product or feature name, a UI label, code or
command syntax, a resource identifier, a person's or organization's proper
name, or a project term with a defined meaning. Copy those exactly.

## Sources

| File | Use |
| --- | --- |
| [Decision register](references/decision-register.md) | Every resolved rule, with its authority. Read first. |
| [Information decomposition](references/decomposition.md) | One job per sentence, one purpose per paragraph, review triggers, worked examples |
| [Messages](references/messages.md) | Emails, chat messages, and texts sent as Greg |
| [Microsoft](references/authorities/microsoft-style.md) | What was adopted from the Microsoft Writing Style Guide, and where to look it up |
| [Google](references/authorities/google-developer-documentation.md) | Adopted Google developer documentation principles |
| [Plain language](references/authorities/plain-language.md) | Adopted GOV.UK and U.S. federal plain-language principles |
| [Chicago](references/authorities/chicago-editorial.md) | Adopted Chicago mechanics for gaps the others leave |
| [`scripts/editorial_check.py`](scripts/editorial_check.py) | Enforced checks and advisory review for Markdown and plain text |

## Workflow

1. **Name the reader and the task.** Decide what the reader must know, decide,
   or do after reading. Organize around that, not around the order the
   material was found.
2. **Draft the point first.** Each section and each paragraph opens with its
   point. An executive summary's first sentence carries the verdict.
3. **Decompose.** Give each sentence one clear job and each paragraph one
   purpose ([decomposition](references/decomposition.md)). Separate scope from
   exclusions, findings from recommendations, and evidence from conclusions.
   Simplify the wording, never the meaning.
4. **Apply the register.** Work through mechanics, terms and voice, structure,
   and instruction rules. Put every identifier in code formatting.
5. **Check.** Run the checker on every Markdown or text draft before you
   deliver it or paste it into another tool:

   ```bash
   # Enforced issues exit 1; review notes are advisory.
   python scripts/editorial_check.py draft.md
   python scripts/editorial_check.py email.txt --text
   ```

   Fix every enforced issue. Reread each review note, then decompose the
   sentence or keep it as written. For a Google Doc, the
   `google-workspace-design` skill's `audit_doc.py` runs the same checks on
   the saved read. When neither can run, check the register section 2 rules by
   reading, and say that you did.
6. **Report.** Say which checks ran and their results. Never describe a
   draft as conforming without a check.

## Common failures

- Compression: one sentence carrying scope, exclusions, a prior decision, and
  a reason. Three clear sentences beat one dense one.
- Repunctuating instead of decomposing: swapping parentheses or a dash for a
  colon leaves one sentence carrying two ideas.
- Em dashes, including the spaced hyphen used as a dash.
- Title-case headings copied from a template or another document.
- A missing serial comma in a list of three or more.
- Resource names, file names, property values, and commands in plain text.
- Simplifying away a qualifier ("based on the captured configuration") so a
  finding sounds more certain than its evidence.
- A different word for the same concept in each paragraph.
- Vague headings, such as "Other" or "Details", and vague link text, such as
  "here".
- Hedging stacks and filler: "it may potentially be advisable to consider".
