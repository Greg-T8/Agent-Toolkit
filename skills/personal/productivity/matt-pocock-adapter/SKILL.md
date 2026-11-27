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

For `grill-with-docs`, use the user's established authoritative artifacts and storage format. When native Google Docs are designated and accessible, read the existing glossary and ADRs. Preserve the upstream domain-modeling principles and ADR criteria, adapting their presentation to the user's writing and document design guidance below. Update resolved glossary terms as the interview progresses; offer ADRs only when the upstream criteria are met. A confirmed interview decision does not by itself authorize implementing the plan.

Read the implementation guide and tracker when relevant to ground decisions, and update them only within the user's requested scope. Use available connectors and report actual writes. If access or a required capability is unavailable, say what could not be applied and provide proposed text instead; do not claim that a document was updated.

## Apply writing and design guidance

For glossaries, ADRs, specifications, and other prose produced by these workflows, read and apply the available Agent Toolkit `editorial-style` guidance and its decision register. Apply `technical-documentation` for documentation structure, with `editorial-style` taking precedence where they overlap. For native Google Docs, also apply `google-workspace-design`, its palette and Docs spec. Resolve these from the available Agent Toolkit skill or plugin; they are not embedded in this bundle. The user's explicit instructions and host instructions take precedence. If the guidance or a required capability is unavailable, say what is missing, apply the available instructions, and do not claim full compliance.

For a glossary, retain the upstream focus on project-specific concepts, concise definitions, canonical terms, relationships, and avoided alternatives where relevant. Give the introduction the glossary's purpose. Alphabetize terms within meaningful groups, and use a two-column term and definition table when the content calls for one. Preserve definitions and decisions when editing; do not invent missing meanings or sources. Include a Sources section with descriptive links to the authoritative artifacts actually used, where appropriate.

For native Google Docs, use the current Docs spec for table styling, fonts, colors, and explicit formatting. Keep definition text in regular weight, emphasize only the intended labels, and use a repeating table header where supported. Match an existing document's design unless the user requests a restyle. Apply the house writing rules, including clear, direct definitions, sentence-case headings, descriptive links, serial commas, and no em dashes. Reconcile edited definitions against accessible authoritative sources without claiming a complete reconciliation unless it was performed.

Check drafts and saved documents using the applicable editorial and Docs audit workflows. Fix identified issues within the authorized scope, read back saved changes, and report which checks ran, any unavailable checks or formatting capabilities, and whether the rendered document was visually inspected. A read-back or inherited formatting alone does not establish visual or explicit-formatting compliance.

## Synthesize a specification

For `to-spec`, use the conversation and relevant, accessible project sources. These may include a code repository, Google Docs and Sheets, a glossary, and ADRs. Honor a user-provided source URL or designated project folder first; otherwise search available sources using the project name. Check a candidate's project identity and role before using it, and ask when multiple candidates cannot be distinguished. Google Workspace sources can supplement a repository or ground a document-centric specification when no matching repository is available.

Read the relevant content of the authoritative implementation guide, tracker, glossary, ADRs, and code when available; discovery or file metadata alone is not a content read. Respect each artifact's stated authority, such as architecture in the guide and task status and evidence in the tracker. Surface conflicts and unresolved authority instead of silently merging them. Record source links, stable project identifiers, and what was actually read; identify inaccessible or unavailable sources as gaps. Do not claim code, tests, or a tracker were reviewed when they were not.

Use those sources to propose the highest practical test seams, then confirm them with the user as the upstream workflow requires. Use the upstream spec template, preserve accepted decisions, and distinguish confirmed decisions from unresolved points. If no codebase is accessible, describe the proposed behavior and testing boundaries from available evidence and state the missing code-level evidence. Do not apply the interview rounds above to this workflow. Confirming test seams does not authorize implementation or changes to project documents.

### Deliver the specification

Follow the user's explicit output format, destination, and publication conditions first. When the conversation establishes native Google Docs as the project's working document format and the user has not specified another format, default to a native Google Doc for the finalized specification. Use the designated project folder when it is verified and writable; determine the folder from the user's instructions or the related project documents' actual location. If the destination is ambiguous or unavailable, do not guess or silently place the Doc elsewhere. Resolve the destination or explain the limitation and provide the specification in an available format.

After the test seams are confirmed, create the specification as a new Google Doc when creation is within the user's authorized scope and host rules. Apply the available editorial and Google Docs design guidance above, read back and audit the saved Doc, and provide its link. Do not modify the source guide, tracker, or other project documents merely because they were used for grounding. If Doc creation, the requested formatting, or verification is unavailable, report the limitation accurately; a downloadable Markdown file is a fallback, not a substitute described as a Google Doc.

Treat Google Doc delivery and issue-tracker publication as separate outcomes. A missing issue tracker or label mapping does not by itself block a Google Doc when the user's instructions permit it. However, an explicit condition on all publication or document creation also applies to the Doc; do not bypass it by calling the Doc a draft or using a different destination. Honor any narrower condition that applies only to issue publication.

For issue publication, use a verified, designated issue tracker and its confirmed triage-label mapping; do not infer either from a source or a similarly named repository. The upstream setup skill is not included in this bundle: if either is missing, ask for the missing details rather than directing the user to an unavailable command. Publish the issue and apply the configured `ready-for-agent` label only when the destination and mapping are established and the action is authorized under the user's instructions and host rules. Report the Doc and issue outcomes separately, including actual links, blocked actions, and reasons. Test-seam approval alone does not authorize implementation or changes to existing project documents.
