# Information decomposition

The rule that matters most, and the one no punctuation rule can supply:

> **Give each sentence a clear job and each paragraph one primary informational purpose.**

Microsoft style asks for concise writing. Google, plain-language guidance, and
Chicago push harder on separating ideas, and generated prose needs that push.
It tends to produce sentences that are grammatically correct and carry five
jobs at once. The fix isn't shorter sentences. It's fewer concepts per sentence
and per paragraph.

## Principles

**Structural clarity wins over compression.** Three clear sentences beat one
dense one, even when the three are longer in total. Verbal concision still
applies: cut padding, restated points, and hedging. When cutting words and
separating ideas pull in opposite directions, separate the ideas.

**One purpose per paragraph.** Define scope, set context, describe current
state, explain evidence, state a limitation, state a finding, make a
recommendation, explain a rationale, identify a risk, or describe a step.
Supporting sentences serve that purpose. If describing the purpose takes
several phrases joined with "and", split the paragraph.

**Separate these pairs** when they share a sentence and the reader would
process them separately:

- Scope and exclusions
- Observation and interpretation
- Finding and recommendation
- Evidence and conclusion
- Action and rationale
- Current state and future state
- Several unrelated conditions or actions

**Lead with the point.** A paragraph's first sentence tells a scanning reader
what the paragraph is for. Repeat a qualification where it applies instead of
leaving it several paragraphs back.

**Simplify language, not meaning.** A decomposition that drops a condition, a
qualifier, an identifier, or a defined project term has failed.

**Repunctuating isn't decomposing.** Swapping parentheses or a dash for a
colon, or a semicolon for a colon, leaves one sentence carrying two ideas. A
colon introduces a list or a short explanatory phrase; it doesn't join two
statements.

## Review triggers

These call for a second read. None is a rule to satisfy mechanically: a
technical sentence may run long when keeping a concept whole is more accurate.
`editorial_check.py` lists every sentence and paragraph that hits one.

| Trigger | What to ask |
| --- | --- |
| A sentence over about 25 words | Does it carry more than one main idea? Would a list expose the structure? |
| Two or more clause joiners: "which", "while", "whereas", "because", "as well as", "including", "where", "although" | Has one sentence absorbed several statements? |
| A semicolon, or two or more parentheses in one sentence | Is punctuation holding together what should be separate sentences? |
| A colon followed by a clause with its own verb | Is the colon joining two statements, often evidence to its conclusion? Give each its own sentence. |
| An inline series of more than three identifiers | Make it a list, or a table if the items carry attributes. Does the reader need every item, or only the ones the point is about? |
| A paragraph over five sentences | Does it have more than one purpose? |

The inline-series trigger is the exception: the decision register makes it a
rule, so a real series it flags is restructured, not kept. In an executive
summary, the five-sentence paragraph limit and a verdict-first opening are
rules too.

Splitting long sentences inside a paragraph that keeps every purpose isn't
decomposition. The paragraph still has to be split.

## Examples

### A scope paragraph

Before:

> This review covers the backup configuration for the Contoso production
> workloads: the Recovery Services vaults, backup policies, and protected items
> in `rg-backup-prod` (subscription `Contoso-Production`), the retention decision
> from the October 14, 2026, architecture review, and the expected storage cost.
> It follows the scope in the project charter: Azure-native backup with
> geo-redundant storage. It doesn't cover on-premises backups, SQL Server native
> backups, or the third-party archive service, which the architecture review
> placed outside the project.

One paragraph carries eight jobs: what is reviewed, which resources, which
subscription, a prior decision, cost, charter alignment, exclusions, and why
they're excluded.

After:

> This review assesses the backup configuration for the Contoso production
> workloads. It covers the Recovery Services vaults, backup policies, and
> protected items in `rg-backup-prod` in the `Contoso-Production` subscription.
> It also considers the retention decision from the October 14, 2026,
> architecture review and the expected storage cost.
>
> The review follows the scope in the project charter: Azure-native backup with
> geo-redundant storage.
>
> The review excludes on-premises backups, SQL Server native backups, and the
> third-party archive service. The October 14 architecture review placed these
> outside the project.

Scope, governing context, and exclusions are now three paragraphs a reader can
find by scanning. The revision is longer, and clearer.

### An executive summary opening

Before:

> The backup design rests on sound foundations: policy-based protection, a
> dedicated vault per region, and soft delete. Its weakness is coverage. Today,
> machines are added to policies by hand. The November 20, 2026, capture shows
> what that costs: 31 of 140 VMs have no backup. We recommend assigning
> protection through Azure Policy by tag, which keeps the design simple and also
> covers new VMs automatically.

The verdict arrives in sentence four, behind a colon that joins evidence to its
conclusion. The recommendation and its rationale share a sentence, and "we"
names no actor.

After:

> Of the 140 production VMs, 31 have no backup, based on the November 20, 2026,
> capture. Each gap is a VM that was never added to a backup policy by hand.
>
> The platform team should assign backup protection through Azure Policy, by
> tag. New VMs are then covered automatically. The change builds on the
> existing design: policy-based protection, a vault per region, and soft delete.

The verdict is now the first sentence. The finding and the recommendation are
separate paragraphs, the actor is named, and the qualifier "based on the
capture" survives.

### A current-state paragraph with an inline series

Before:

> The subscription holds seven vaults. Four are in `rg-backup-prod`:
> `rsv-prod-eus-01`, `rsv-prod-wus-01`, `rsv-sql-eus-01`, and `rsv-archive-01`.
> The vault health review found `rsv-sql-eus-01` and `rsv-archive-01` had no
> protected items.

An inventory of four identifiers delays the point, which arrives in the last
sentence.

After:

> Two of the seven vaults have no protected items: `rsv-sql-eus-01` and
> `rsv-archive-01`. The vault inventory table lists each vault with its
> resource group.

## Checks before a section is final

- What is each paragraph's purpose?
- Does any sentence do more than one substantial job?
- Does any sentence carry a series of more than three identifiers?
- Are scope, exclusions, rationale, evidence, findings, and recommendations
  mixed?
- Does each heading describe what is under it?
- Are list entries parallel?
- Are identifiers in code formatting, and official terms intact?
- Would the section still work if the reader scanned only headings and first
  sentences?
