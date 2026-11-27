# Plain-language principles: adopted

## Purpose

This file records plain-language principles adopted by the editorial-style skill.

The goal is to make technical documents and professional writing easier to find, scan, understand, and act on **without reducing technical precision**.

Primary influences include GOV.UK content guidance and U.S. federal plain-language guidance.

## Authority and precedence

Apply these principles under the following constraints:

1. The house rules and decision register in `../decision-register.md` take precedence.
2. Microsoft Writing Style Guide remains authoritative for Microsoft terminology and Microsoft-specific technical conventions.
3. Plain-language guidance governs clarity, organization, sentence construction, and reader effort when it does not conflict with higher-priority rules.

Plain language is not permission to replace precise technical terms with vague conversational language.

## Core principle

> Simplify language, not meaning.

A successful plain-language revision makes the same technical point easier to understand.

It must not:

- remove an important condition
- weaken a requirement
- collapse meaningful distinctions
- replace official terminology
- reduce necessary precision
- conceal uncertainty
- make a finding sound more certain than the evidence supports

## Write for the reader's task

Before drafting a section, identify what the reader needs to:

- know
- decide
- verify
- configure
- approve
- investigate
- act on

Organize the content around that need rather than around the order in which the author discovered the information.

For technical and planning documents, common reader needs include:

- understand current state
- understand scope
- identify risk
- understand why a finding matters
- decide whether to accept a recommendation
- know what action to take next

## Lead with the main point

Put the most important information early.

Prefer:

> The review identified two workspaces outside the captured resource group.

Then explain the details.

Avoid requiring the reader to process several sentences of setup before discovering the point.

For longer sections, use the opening sentence to establish the section's purpose or principal conclusion.

## One idea per sentence

Treat one idea per sentence as a design principle, not a rigid grammatical rule.

Split a sentence when it contains independent ideas that a reader might need to process separately.

Review sentences that contain several:

- clauses
- conditions
- qualifications
- parenthetical statements
- lists
- changes in actor
- changes in time
- changes in scope

A sentence may be long and still clear. A sentence may also be short and still contain too many ideas. Evaluate cognitive load, not only word count.

### Sentence-length trigger

Use approximately **25 words as a review trigger**, not a hard limit.

When a sentence exceeds that threshold, ask whether:

- it contains more than one main idea
- a list would expose the structure better
- a condition should move to its own sentence
- a parenthetical statement should become a separate statement
- unnecessary words can be removed

Technical sentences may legitimately exceed the threshold when keeping a concept intact improves accuracy.

## Keep paragraphs focused

A paragraph should normally have one primary informational purpose.

As a review trigger, inspect paragraphs longer than about five sentences for possible decomposition.

Do not split a paragraph merely to satisfy a numeric target. Split it when the reader benefits from a clearer conceptual boundary.

## Prefer active voice

Use active voice when the actor matters.

Prefer:

> Azure Monitor evaluates the alert rule.

Over:

> The alert rule is evaluated by Azure Monitor.

Active voice is particularly important for:

- responsibilities
- recommendations
- procedures
- ownership
- approval steps
- remediation actions

Passive voice is acceptable when the actor is irrelevant, unknown, or intentionally de-emphasized.

## Name the actor

Avoid constructions that hide responsibility.

Weak:

> The configuration should be reviewed.

Stronger:

> The platform team should review the configuration.

Or, in a recommendation:

> Review the configuration before deployment.

The correct form depends on whether ownership is known and whether the sentence is procedural or analytical.

## Use concrete verbs

Prefer verbs that state the action directly.

Prefer:

- use
- create
- configure
- review
- compare
- verify
- collect
- monitor
- remove
- replace
- approve

Review abstract constructions such as:

<!-- editorial-check: off -->
- perform an evaluation of
- conduct a review of
- make use of
- provide an implementation of
<!-- editorial-check: on -->

These are not always wrong, but a direct verb is often clearer.

## Remove words that do not add meaning

Review phrases such as:

<!-- editorial-check: off -->
- in order to
- it should be noted that
- it is important to note
- at this point in time
- due to the fact that
- for the purpose of
- in the event that
- with regard to
<!-- editorial-check: on -->

Replace or remove them when the sentence remains accurate.

Do not remove words that communicate:

- scope
- probability
- uncertainty
- timing
- exception
- dependency
- responsibility

## Use familiar words when precision is equal

Prefer the simpler word when both choices mean the same thing for the intended audience.

Examples:

<!-- editorial-check: off -->
- use instead of utilize
- help instead of assist
- begin instead of commence
- about instead of concerning
<!-- editorial-check: on -->

Do not replace a technical term with a simpler word when the technical term is more precise.

For example, do not replace:

> conditional forwarder

with:

> DNS setting

when the distinction matters.

## Treat jargon according to the audience

Technical terminology is not automatically bad.

Use specialist terms when:

- the audience is expected to know them
- they are official product or industry terms
- using a generic substitute would reduce precision

Explain a term when:

- it is important to the conclusion
- part of the audience may not know it
- misunderstanding would affect a decision

Avoid internal jargon that the reader is unlikely to recognize.

## Control acronyms

Use acronyms only when they reduce effort over the remainder of the document.

Define uncommon acronyms at first meaningful use.

Do not introduce an acronym that appears only once or twice unless it is itself the term readers are most likely to recognize.

Do not repeatedly redefine the same acronym in a short document unless sections may be consumed independently.

## Use positive and direct constructions

When equivalent, prefer a positive statement over a negative construction.

Prefer:

> Include the subscription in the assessment.

Over:

> Do not omit the subscription from the assessment.

Use negative instructions when the prohibited action is the important information.

## Make scope explicit

Scope language should be easy to identify.

Prefer explicit constructions such as:

> The review includes...

> The review excludes...

> The configuration capture covered...

> The assessment did not evaluate...

Do not bury major scope boundaries in subordinate clauses.

## Separate fact, interpretation, and recommendation

For assessment and advisory documents, distinguish:

**Fact**

> The workspace is outside the captured resource group.

**Interpretation**

> As a result, the configuration capture does not provide enough evidence to assess its diagnostic settings.

**Recommendation**

> Capture the workspace configuration before finalizing the monitoring baseline.

Do not compress all three into one sentence when separation improves auditability.

## Use lists when they reveal structure

Use a list when prose contains multiple comparable items or steps.

Lists work well for:

- requirements
- prerequisites
- exclusions
- recommendations
- implementation steps
- evidence sources
- risks
- decision criteria

Keep list items parallel.

Do not turn every group of two items into a list.

## Use headings to answer reader questions

A useful heading identifies what the reader will find.

Prefer:

- Review limitations
- Recommended monitoring architecture
- Cost assumptions
- Resources not included in the capture
- Configure the outbound endpoint

Avoid vague headings such as:

- Other
- Notes
- Details
- Gaps

unless the surrounding template gives the term an explicit, stable meaning.

## Write for scanning

Assume many readers will not read the document linearly.

Support scanning with:

- descriptive headings
- short focused paragraphs
- meaningful opening sentences
- lists
- tables for genuine comparisons
- consistent terminology
- visible separation of findings and recommendations

Do not depend on a reader remembering a qualification buried several paragraphs earlier.

## Preserve nuance and uncertainty

Plain language must not convert uncertainty into certainty.

Preserve phrases such as:

- based on the captured configuration
- as of September 21, 2026
- the available evidence indicates
- the review did not verify
- this estimate assumes
- additional validation is required

These qualifiers are part of the technical meaning.

## Avoid arbitrary readability targets

Do not write to an arbitrary school-grade level unless the project specifically requires one.

The intended audience may include:

- engineers
- architects
- administrators
- IT managers
- security teams
- executives

Plain language means writing appropriately for the audience, not removing domain vocabulary that the audience needs.

## Example: compressed scope paragraph

**Before**

> This review covers the backup configuration for the Contoso production workloads, including the Recovery Services vaults, backup policies, protected items, the retention decision from the October 14 review, and expected cost, and it follows the project charter while excluding on-premises backups, SQL Server native backups, and the third-party archive service.

**After**

> This review assesses the backup configuration for the Contoso production workloads. It covers the Recovery Services vaults, backup policies, and protected items. It also considers the retention decision from the October 14 review and the expected cost.
>
> The review follows the scope defined in the project charter.
>
> The review excludes on-premises backups, SQL Server native backups, and the third-party archive service.

The revision is longer in raw word count but easier to understand because the reader can distinguish scope, governing context, and exclusions.

## Editorial checks

Before finalizing content, ask:

1. Can the reader identify the main point quickly?
2. Does each sentence have a clear job?
3. Does each paragraph have one primary purpose?
4. Are any sentences carrying several independent ideas?
5. Is the actor clear when responsibility matters?
6. Can unnecessary words be removed without changing meaning?
7. Are technical terms necessary and appropriate for the audience?
8. Are uncommon acronyms explained?
9. Are scope and limitations explicit?
10. Are fact, interpretation, and recommendation distinguishable?
11. Do headings accurately describe the content below them?
12. Would a list or table make the structure clearer?
13. Have important qualifiers and uncertainty been preserved?
14. Has simplification retained technical precision?

## Sources

Primary references, accessed September 22, 2026:

- GOV.UK Functional Standards writing style guide: https://www.gov.uk/government/publications/handbook-for-standard-managers/functional-standards-writing-style-guide
- GOV.UK, Use clear language: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
- GOV.UK, Understand content design: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/understand-content-design/
- GOV.UK content principles: https://www.gov.uk/government/publications/govuk-content-principles-conventions-and-research-background/govuk-content-principles-conventions-and-research-background
- Digital.gov, "Principles of plain language": https://digital.gov/guides/plain-language/principles
- Digital.gov, "Short and simple": https://digital.gov/guides/plain-language/principles/short-simple
- National Archives, Principles of Clear Writing: https://www.archives.gov/federal-register/write/legal-docs/clear-writing.html
