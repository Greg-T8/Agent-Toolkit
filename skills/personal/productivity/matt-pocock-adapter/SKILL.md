---
name: matt-pocock-adapter
description: Apply Greg's interview and document preferences when using Matt Pocock's grill-me, grill-with-docs, or to-spec workflows across agent hosts.
---

# Adapt Matt Pocock's workflows

Use this guidance for requests to use `grill-me`, `grill-with-docs`, or `to-spec`, including requests to conduct their interviews or synthesize a specification. Follow the user's instructions and the host's higher-priority instructions. Preserve Matt's methods except for the presentation and storage adaptations below.

## Load upstream guidance

- For `grill-me`, read and apply `grilling`.
- For `grill-with-docs`, read and apply both `grilling` and `domain-modeling`, including the latter's glossary and ADR formats when needed.
- For an explicit `to-spec` request, read and apply [to-spec](../to-spec/SKILL.md). Synthesize the conversation without an interview; its test-seam confirmation still applies.
- In the composed bundle, the upstream skills are sibling directories under `references/skills/`: read [grilling](../grilling/SKILL.md) and [domain-modeling](../domain-modeling/SKILL.md) directly rather than assuming they are independently invocable. Their relative supporting links resolve from their own directories.
- On another host, use installed upstream skills or accessible upstream files. If required guidance is unavailable, say what is missing and ask for access; do not invent its contents or claim it was applied.

## Present each round

Follow the upstream design tree: group all currently independent, answerable questions into the round and defer questions that depend on unsettled decisions. Assign each question a unique ID, state the question, recommend an answer with a brief rationale, and offer choices suited to the decision.

If the host actually provides an interactive questionnaire with the necessary features, present the whole round together. Include an optional free-text field under each question, a completion indicator, editable answers, no preselected answers, and one **Submit round** button. Allow unanswered questions to remain unresolved and submit all answers and comments together.

If the host cannot provide that complete interaction, present the entire round as numbered Markdown questions with optional comments. Accept answers collectively, including partial answers. Never claim a control, completion indicator, or submission has worked without host support. Do not switch to one question at a time merely because interactive controls are unavailable.

Evaluate the submitted answers together. Identify conflicts, unresolved questions, and decision dependencies; do not treat a recommendation as accepted without an explicit answer. Resolve prerequisites before asking dependent questions, then present the next frontier as a new round. Retain the upstream requirement to confirm shared understanding before implementing the resulting plan.

## Maintain documentation

For `grill-with-docs`, use the user's established authoritative artifacts and storage format. When native Google Docs are designated and accessible, read the existing glossary and ADRs, then maintain them using the upstream formats and criteria rather than assuming Markdown files are required. Update resolved glossary terms as the interview progresses; offer ADRs only when the upstream criteria are met. A confirmed interview decision does not by itself authorize implementing the plan.

Read the implementation guide and tracker when relevant to ground decisions, and update them only within the user's requested scope. Use available connectors and report actual writes. If access or a required capability is unavailable, say what could not be applied and provide proposed text instead; do not claim that a document was updated.

## Synthesize a specification

For `to-spec`, inspect the relevant code and accessible authoritative glossary and ADRs, then propose test seams and confirm them with the user as the upstream workflow requires. Use the upstream spec template and distinguish confirmed decisions from unresolved points. Do not apply the interview rounds above to this workflow.

Use the user's designated issue tracker and triage-label mapping when available. The upstream setup skill is not included in this bundle: if the tracker or label mapping is missing, ask for the missing details rather than directing the user to an unavailable command. Publish and apply the configured `ready-for-agent` label only within the user's authorized scope and host instructions. If the requested destination or capability is unavailable, provide the draft and report what remains unpublished.
