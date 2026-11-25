# Source patterns and provenance

These planning sources were inspected through the connected Google Drive tools
on 2026-11-25. The patterns below guide new artifacts; their platform choices,
environment facts, permissions, deadlines, and task statuses are project-specific
historical context. Re-read a source before using it as current project evidence.
The skill retains links and summarized patterns, not copies of project content.

## M365 Knowledge Automation

- [Design and implementation guide](https://docs.google.com/document/d/13IC2yC7B0Hcfhhdd9ez1hS9JyghbpqGqVULXvU6Zp1c/edit)
- [Native Google Sheets progress tracker](https://docs.google.com/spreadsheets/d/1R23eeHOUXLS7lnryeVKnUJBqVUI2PI4SRLty7cvWLZM/edit)

The guide explicitly owns scope, architecture, requirements, decisions, risks,
and acceptance criteria. Its tracker owns task status and implementation evidence.
Stable requirement, phase, test, risk, question, decision, and task IDs connect
the pair. Design acceptance and implementation completion are separate states.
Guide revisions record their effect on the companion tracker.

The tracker has Overview, Tasks, Decisions, Change Log, and References tabs.
Its task fields cover ID, phase, workstream, deliverable, guide references,
priority, status, owner, dependencies, acceptance, target date, evidence, notes,
and update date. The reusable contract adds an explicit next-action field and
requires meaningful dependency entries rather than copying empty baseline cells.

## Hermes

- [Step-by-step implementation guide](https://docs.google.com/document/d/1rH7ZRiIkMR2X11GmFtuV3bRhTZiZSggdrmOq1dMXRWc/edit)
- [Master implementation tracker](https://docs.google.com/document/d/1LAiIqp1ddgauU9N6E1OPBtZKkdzbxD9c0DXnQRk07uQ/edit)

This pair distinguishes readiness work from an application's own authoritative
implementation plan. Milestones have stable task IDs and acceptance gates;
runbook steps state environment, action, expected result, and evidence. The
tracker distinguishes prior verification, partial progress, pending fresh checks,
blocked work, and deferred work. Manual execution and scheduled delivery require
different evidence. One-action-at-a-time review is a deliberate operating mode
for this project, not a universal planning requirement.

## ALZ runner migration

- [Implementation guide](https://docs.google.com/document/d/1D9LvkEuGgECXqNT0BvvD3U1tGI9_aKBqDYcCohYxDk4/edit)
- [Progress tracker](https://docs.google.com/document/d/1rcSpxl0k062yMSowG9I0dJV8Rs0tMzQCG89PfGPMlK4/edit)

This pair contributes environment and ownership boundaries, baseline inventory,
prerequisites, staged migration, rollback, and acceptance gates. Tasks capture
owner, date, evidence, and blockers. Repository scaffolding and static checks
remain distinct from deployed behavior and successful cutover.

## Format choice

The historical plans and two trackers are Google Docs. Greg's explicit preference
for this skill is an editable Word implementation plan and a native Google Sheets
task tracker. Preserve the planning patterns while using those preferred formats;
do not treat a historical file type as an instruction to reproduce it.
