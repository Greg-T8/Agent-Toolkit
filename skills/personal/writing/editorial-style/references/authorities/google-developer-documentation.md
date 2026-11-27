# Google developer documentation style: adopted principles

## Purpose

This file records the Google-derived editorial principles adopted by the editorial-style skill.

It is **not a reproduction of the Google Developer Documentation Style Guide**. It is an operational interpretation of selected Google guidance for Greg Tate's technical documents and professional writing.

## Authority and precedence

Apply these principles in this order of precedence:

1. The house rules and decision register (`../decision-register.md`)
2. Microsoft Writing Style Guide for Microsoft terminology, product names, UI language, and Microsoft-specific technical conventions
3. This adopted Google guidance for technical information structure, clarity, developer-oriented content, and scannability
4. Other editorial references when the preceding authorities are silent

If Google guidance conflicts with an explicit house or Microsoft rule, the higher-priority rule wins.

## Core principle: decompose information

### Give each sentence a clear job

Prefer one primary idea, thought, or action per sentence.

A grammatically valid sentence can still be too complex if it combines several independently useful ideas. Split the sentence when subordinate clauses, lists, qualifications, or transitions introduce a separate concept.

**Review for decomposition when a sentence combines:**

- scope and exclusions
- observation and interpretation
- finding and recommendation
- action and rationale
- current state and future state
- evidence and conclusion
- several unrelated conditions
- multiple independent actions

**Do not shorten merely for the sake of brevity.** The goal is lower cognitive load.

### Give each paragraph one primary purpose

A paragraph should normally have one dominant informational purpose, such as:

- define scope
- establish context
- describe current state
- explain evidence
- identify a limitation
- state a finding
- provide a recommendation
- explain rationale
- describe an implementation step
- identify risk

Supporting sentences may elaborate on that purpose, but the reader should be able to summarize the paragraph with a short phrase.

### Prefer structural clarity over compression

Three clear sentences are often better than one dense sentence.

Do not treat word count as the primary measure of concision. Optimize for:

- comprehension
- scanability
- unambiguous relationships
- clear ownership of actions
- clear separation of ideas

## Voice and sentence construction

### Prefer active voice

Use active voice when the actor matters or when responsibility could otherwise be ambiguous.

Prefer:

> Azure Policy evaluates the resource.

Over:

> The resource is evaluated by Azure Policy.

Passive voice is acceptable when:

- the actor is unknown or irrelevant
- the outcome matters more than the actor
- naming the actor would distract from the point
- the passive construction is more natural and remains unambiguous

### Address the reader directly in instructional content

Use **you** and the imperative mood for procedures and implementation guidance when appropriate.

Prefer:

> Select **Review + create**.

Over:

> The user should select **Review + create**.

Avoid unnecessary first-person plural language such as *we*, *our*, or *let's* unless the author's own team is the intended actor.

### Put conditions where readers need them

When a condition governs an action, place it before the instruction when doing so prevents the reader from acting prematurely.

Prefer:

> If the workspace uses private endpoints, verify DNS resolution before you test connectivity.

Rather than presenting the condition after the action.

## Tone

Write in a professional, direct, natural tone.

The desired tone is:

- knowledgeable
- respectful
- concise
- technically precise
- approachable
- not promotional
- not theatrical
- not unnecessarily formal

Avoid:

- filler phrases
- empty transitions
- hype
- slang
- clichés
- unnecessary metaphors
- culture-specific references
- humor that could distract or translate poorly
- statements such as *simply*, *easy*, or *just* when they minimize complexity

## Headings and navigation

### Use descriptive headings

A heading should tell the reader what information follows.

Prefer:

> Review limitations

Over:

> Gaps

Prefer:

> Configure the DNS forwarding ruleset

Over:

> DNS configuration

when the section is task-oriented.

### Use sentence case

Use sentence case for headings. The house rules make one exception: a document's title uses title case.

### Preserve hierarchy

Use heading levels in logical order. Do not skip levels merely for visual appearance.

A document should remain understandable from its heading outline alone.

## Lists

Use lists when they expose structure more clearly than prose.

Use:

- numbered lists for ordered procedures or sequences
- bulleted lists for unordered collections
- tables when readers need to compare multiple attributes across items

Keep list items parallel in grammar and level of detail.

Introduce a list when the relationship between the items is not already obvious.

Avoid forcing a list when a short sentence is easier to understand.

## Technical formatting

### Distinguish code and identifiers from prose

Use code formatting for items such as:

- commands
- parameters
- resource names
- file paths
- code elements
- literal values
- configuration keys

Example:

> The workspace `law-ops-prod-01` is outside `rg-monitoring-prod`.

### Preserve official UI labels

Use the official product or interface label and follow Microsoft conventions for Microsoft UI elements.

Do not rewrite UI labels for stylistic consistency.

## Links and cross-references

Use descriptive link text.

Prefer:

> See **Azure Monitor best practices**.

Avoid:

> Click **here**.

The link text should make sense when read out of context.

## Global and inclusive writing

Write so that the content remains understandable to readers from different regions and language backgrounds.

Prefer:

- literal language
- consistent terminology
- unambiguous dates
- simple sentence structures
- explicit relationships between ideas

Avoid:

- idioms
- culturally specific metaphors
- unexplained regional references
- ambiguous pronouns
- unnecessary variation in terminology

Do not substitute different terms merely to avoid repetition when the terms refer to the same technical concept.

## Accessibility

Write content that remains understandable without relying only on visual presentation.

Apply these principles:

- use meaningful headings
- use descriptive link text
- provide alternative text for meaningful images
- do not communicate meaning through color alone
- ensure tables have a clear purpose and understandable structure
- define uncommon abbreviations when first used
- avoid directional references such as *above* or *to the right* when a semantic reference is clearer

## Information-decomposition rule

The editorial-style skill adopts the following operational rule (see `../decomposition.md`):

> Give each sentence a clear job and each paragraph one primary informational purpose.

Apply this rule especially to AI-generated prose, which can be grammatically correct while still compressing too many ideas into one unit.

### Example

**Before**

> This review covers the backup configuration, the resources in the backup resource group, the retention decision from the October 14 review, and expected cost, and it follows the project charter while excluding on-premises backups, SQL Server native backups, and the third-party archive service.

**After**

> This review assesses the backup configuration. It covers the resources in the backup resource group and considers the retention decision from the October 14 review and the expected cost.
>
> The review follows the scope defined in the project charter.
>
> The review excludes on-premises backups, SQL Server native backups, and the third-party archive service.

The revision is not necessarily shorter. It is structurally clearer.

## Editorial checks

Before finalizing a section, ask:

1. What is this paragraph's primary purpose?
2. Does any sentence contain more than one independent idea?
3. Are scope, exclusions, rationale, evidence, findings, or recommendations unnecessarily combined?
4. Is the actor clear where responsibility matters?
5. Can the reader identify the important point by scanning headings and opening sentences?
6. Are list items parallel?
7. Are technical identifiers visually distinct from prose?
8. Is terminology consistent?
9. Can any wording be simplified without losing technical precision?
10. Does Microsoft terminology remain authoritative?

## Sources

Primary references, accessed September 22, 2026:

- Google Developer Documentation Style Guide: https://developers.google.com/style
- Highlights: https://developers.google.com/style/highlights
- Voice and tone: https://developers.google.com/style/tone
- Active voice: https://developers.google.com/style/voice
- Second person and first person: https://developers.google.com/style/person
- Headings and titles: https://developers.google.com/style/headings
- Lists: https://developers.google.com/style/lists
- Write for a global audience: https://developers.google.com/style/translation
- Write accessible documentation: https://developers.google.com/style/accessibility
- Google Technical Writing, Short sentences: https://developers.google.com/tech-writing/one/short-sentences
