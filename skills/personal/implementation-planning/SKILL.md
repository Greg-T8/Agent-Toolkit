---
name: implementation-planning
description: Create or update a project implementation plan and linked task tracker. Default to an editable Word plan and a native Google Sheets tracker with phases, dependencies, acceptance criteria, and evidence-based status.
metadata:
  author: Greg Tate
  version: "0.1.1"
---

# Create an implementation plan and task tracker

Turn project goals, existing designs, and verified context into two coordinated
deliverables: an editable Word implementation plan (`.docx`) and a native Google
Sheets task tracker. Honor an explicit request for one artifact, another format,
or an existing template. Creating planning artifacts does not authorize executing
the implementation, provisioning resources, or creating scheduled jobs.

## Establish the project baseline

- Identify the project, intended reader, desired outcome, scope, constraints,
  existing environment, and any authoritative design or implementation documents.
  Use available conversation context, repository files, and connected sources
  before asking for information already accessible there.
- When the user refers to prior Google Docs without a link, search Drive using
  project names and terms such as implementation, guide, progress, or tracker.
  Confirm titles and MIME types, then read relevant content. Search metadata alone
  does not establish a document's contents or current implementation state.
- Separate confirmed facts, accepted decisions, proposals, assumptions, and open
  questions. Retain source dates and evidence boundaries. A chosen design or a
  checked-in script does not prove deployment or successful runtime behavior.
- Ask only for missing information that materially changes scope or correctness.
  Continue independent drafting with labeled assumptions where practical. Leave
  unknown owners and target dates unassigned rather than inventing commitments.

The defaults come from Greg's recent planning examples. Read
[source patterns](references/source-patterns.md) when an example's purpose or
provenance matters; those historical projects are not prerequisites or current
facts for a new project. Do not fetch every historical example on every use.

## Design the paired artifacts

Read [the artifact contract](references/artifact-contract.md) before authoring or
reconciling either deliverable. Scale the detail to the project.

- The plan owns scope, architecture, requirements, design decisions, risks,
  implementation sequence, and acceptance criteria.
- The tracker owns task assignments, operational status, blockers, dependencies,
  next actions, and implementation evidence. Decision summaries point back to the
  plan instead of becoming a competing decision record.
- Reuse existing phase, requirement, decision, test, and task identifiers. Assign
  stable IDs where missing and use them across both artifacts. Retire IDs rather
  than renumbering or reusing them.
- Give each phase useful deliverables and an observable exit gate. Break the work
  into executable tasks with prerequisites and testable completion criteria.
  Include validation, handoff, and recovery work when applicable.
- Write an implementation plan by default. Add exact commands, expected output,
  troubleshooting, and stepwise review pauses when the user requests a runbook
  or the project requires operational instructions. Do not impose the Hermes
  one-action-at-a-time operating model on unrelated projects.

## Produce the Word plan

Use the available Word/document authoring skill and its rendering workflow for
the `.docx`. Follow an explicitly supplied template; otherwise use restrained,
readable engineering-document formatting with native headings, lists, and tables.
Render and visually inspect every page before delivery. Report a rendering
limitation accurately rather than claiming text extraction proves layout quality.

Deliver the Word file. Using Google Docs as source context does not change this
format preference. If the user asks to store the Word plan in Drive, upload it
as a Word file; convert to native Google Docs only when requested. Use the
Google Docs workflow for an explicitly requested native Doc.

## Produce the Google Sheets tracker

Use the available Google Sheets skill and connector workflow. For a new tracker,
use its required spreadsheet authoring/import route and verify the result is
native Google Sheets. For an explicitly selected native tracker template, use
the Sheets template-copy workflow and verify the new destination ID. For an
existing tracker, read metadata and bounded ranges before scoped edits.
Format the tracker with the google-workspace-design skill's Sheets spec:
Overview page, banded data tabs, dropdowns, and status colors. The artifact
contract still decides the tabs, columns, and content.

Use the user's destination when supplied; otherwise follow the Google Sheets
skill's location default. Do not substitute a local Excel file or CSV for the
requested native Sheet. If connectivity or the needed authoring capability is
unavailable, finish the accessible work, retain any local draft, and explain
exactly what remains before claiming both deliverables are complete.

## Reconcile and deliver

- Check that plan phases, IDs, decisions, acceptance gates, and tracker references
  agree. Every implementation task needs an acceptance criterion; every in-scope
  phase needs task coverage. Resolve missing or circular dependency references.
- Initialize new implementation tasks as Not Started unless dated evidence
  supports another status. Preserve supported progress on updates. A decision
  accepted in the plan does not make its implementation task Done.
- Link the plan to the verified tracker URL. In the tracker, link to an accessible
  Word location if one exists; otherwise record the exact Word filename/version
  without inventing a cloud URL or linking a local filesystem path as if shared.
- On updates, preserve IDs, evidence, useful history, and unrelated edits. Change
  the owning artifact and reconcile affected references in its companion. Record
  substantive revisions with date, version, affected IDs, rationale, and impact.
- Deliver the Word file and verified native Sheets link. Briefly identify the
  recommended next action and material unresolved decisions or delivery limits.
  Do not describe planned implementation as work already performed.
