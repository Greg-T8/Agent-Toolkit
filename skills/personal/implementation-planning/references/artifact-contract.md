# Plan and tracker contract

Use this as a content model, not a fixed page count or mandatory set of empty
sections. Preserve an existing project's conventions and identifiers. Combine
sections for small projects and add detail only where it helps implementation.

## Word implementation plan

Start with the project name, document purpose, version, status, and creation and
revision dates. Identify the intended reader and explain what the plan enables
them to build or decide. Include a companion-tracker link and a brief statement
of which artifact owns design and which owns implementation status.

An engineering plan usually needs the following content:

| Content | Useful detail |
| --- | --- |
| Outcome and scope | Problem, expected outcomes, success measures, inclusions, exclusions, and boundaries |
| Baseline and prerequisites | Existing components, verified state and dates, access, tools, versions, licensing or cost constraints, and unresolved prerequisites |
| Target approach | Component responsibilities, interfaces, important flows, environment boundaries, and alternatives that still require a decision |
| Requirements and decisions | Stable IDs, concrete requirements, accepted versus proposed decisions, rationale, and implications |
| Implementation phases | Ordered work, dependencies, deliverables, acceptance tests, exit gates, and relevant tracker IDs |
| Validation and acceptance | Observable pass conditions, required evidence, failure handling, and who accepts the result when known |
| Risks and questions | Impact, mitigation, owner when known, next action, and dependencies on unresolved decisions |
| Operations and handoff | Support responsibilities, monitoring, recovery or rollback, and ongoing maintenance when relevant |
| References and revisions | Descriptive source links, source dates where material, version history, rationale, and tracker impact |

Do not invent infrastructure, products, owners, costs, schedules, or requirements
to fill the outline. Verify changing product behavior against authoritative
sources when it affects the plan. Keep research uncertainty visible.

For each phase, state its purpose, prerequisites, deliverables, task references,
and exit criterion. A phase exit gate describes the working result needed to
advance, beyond merely producing configuration or documentation.

For a runbook, each actionable step also needs its execution environment,
prerequisite, action, expected result, evidence to capture, and relevant failure
or recovery guidance. Add approval or review points where the actual project
requires them. A complete plan may document future actions without authorizing
their execution.

Use existing ID schemes. For a new project, examples include `P0`, `FR-001`,
`ADR-001`, `T-001`, `R-001`, `Q-001`, and `TASK-001`. Use only the families the
project needs. Preserve identifiers during editorial changes and scope revisions.

## Google Sheets tracker

Start with an Overview and Tasks tab. For a project with material decisions,
revision history, and external references, use the five-tab pattern from the
M365 example: Overview, Tasks, Decisions, Change Log, and References. For a
smaller project, keep the latter records in compact sections rather than creating
unused tabs. Add dedicated risk or test registers only when their scale warrants
them. Do not create separate authoritative task lists for each phase.

### Overview

Include project purpose, baseline/as-of date, tracker version, the plan's location
and version, status definitions, phase gates, current focus, next action, and
material blockers. Derive task totals, status counts, and completion from Tasks;
do not type independent progress totals that will drift.

Count populated task IDs, excluding headers and unused rows. Use the same task
population for status counts and percentages. Define the completion denominator;
if Deferred or Cancelled work is excluded, label that policy. Handle zero tasks
without a divide-by-zero error. An accepted decision does not contribute to task
completion. Derive any displayed phase progress from the same underlying rows,
and keep gate acceptance separate from the fraction of tasks completed.

### Tasks

Use one task per row. Keep each task independently assignable and verifiable.
Split a row when its outputs can reach different completion states.

| Field | Meaning |
| --- | --- |
| Task ID | Unique, stable identifier; never the spreadsheet row number |
| Phase | Existing phase or milestone identifier |
| Workstream | Component, environment, or discipline when useful |
| Task / Deliverable | Concrete action and resulting output |
| Plan References | Relevant section, requirement, decision, risk, or test IDs |
| Priority | Critical, High, Medium, or Low unless the project uses another scale |
| Status | One value from the defined status list |
| Owner | Named assignee only when known; otherwise TBD |
| Dependencies | Existing task IDs, with all/any semantics explained if needed |
| Acceptance / Definition of Done | Observable result and validation that closes the task |
| Target Date | Real date when supported; blank when unknown |
| Evidence / Result | Link or evidence locator, observed result, date, and validation scope |
| Blocker / Notes | Reason for a block, unresolved question, or relevant qualification |
| Last Updated | Actual date of the row's latest material update |
| Next Action | Specific next step, especially for blocked or partially completed work |

Adapt names/order to a chosen template while retaining the information needed to
operate it. Preserve existing IDs when converting a document checklist into rows.
Carry forward evidence and qualifications; do not reset verified history merely
because the destination is a spreadsheet.

Default statuses are Not Started, In Progress, Blocked, In Review, and Done. Add
Deferred or Cancelled when useful. Preserve a supported existing vocabulary
instead of silently mapping every historical Verified or Pending state to Done
or Not Started. Record an explicit mapping if conversion is needed.

Done requires the task's acceptance criterion and dated evidence of its observed
result. A code change can close a code-writing task while runtime validation
remains open as a separate task. Similarly, a manual job run does not verify a
recurring schedule. Keep accepted decisions, prior reported verification, static
checks, and fresh runtime proof distinguishable in evidence or notes.

Populate meaningful dependencies from the plan; avoid making every task depend
on every earlier row. Check missing IDs, self-dependencies, cycles, and references
to retired tasks. Record the consequence of unresolved decisions as a blocker
where it actually prevents work. Leave genuinely independent work actionable.

### Decisions, Change Log, and References

- **Decisions:** ID, state, short decision summary, rationale/impact, authoritative
  plan reference, and last update. Separate Proposed, Accepted, and Superseded
  design states from implementation task states.
- **Change Log:** date, tracker and plan versions, affected IDs, change, rationale,
  companion-artifact impact, and author/reviewer when known. Preserve history.
- **References:** source title, verified URL or usable locator, and what it
  supports. Distinguish source evidence from links to generated deliverables.

### Usability and verification

Use native tables or filters, frozen headers, readable column widths, wrapped
descriptions, and restrained status/priority formatting. Keep task tables free of
merged cells. Use native dropdowns for maintained option fields through the
Sheets skill's supported workflow; keep status text usable without color.
Use actual date cells and percentage formatting. Ensure summary formulas and
formatting cover new task rows or document how the table expands.

Before delivery, verify the native spreadsheet type, actual sheet names, headers,
task count, IDs, dependencies, dropdown options, links, and summary formulas.
Inspect rendered or browser views through the available Sheets quality workflow
to confirm the primary view and task detail are readable. Check that completed
rows have evidence and that untouched rows retain their prior values.

## Cross-artifact changes

When a requirement, phase, or decision changes, identify affected task IDs and
update descriptions, acceptance tests, and dependencies as needed. Preserve
completion evidence; if it no longer meets revised criteria, explain the gap and
reopen the task or add a new task rather than silently erasing its history.

When only task ownership, status, or evidence changes, update the tracker without
duplicating a live status table into Word. Update the plan when the new evidence
changes its baseline, design, scope, or acceptance criteria. If a companion cannot
be accessed, record the outstanding reconciliation and identify the affected IDs
instead of claiming the pair is synchronized.
