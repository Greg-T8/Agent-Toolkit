---
name: package-skill-bundles
description: Prepare release notes and package Agent-Toolkit skill bundles. Use when asked to release or rebuild these bundles with notes and incremented versions.
metadata:
  author: Greg Tate
  version: "1.0.0"
---

# Prepare and package skill bundles

Work in the Agent-Toolkit repository. The user's request to invoke this skill authorizes local release-note preparation and packaging; do not upload, publish, or commit unless separately requested. Use `skills/Package-Skills.ps1` as the packager. Inspect its current parameters and `skills/README.md` before running it: do not assume versioning, bundle discovery, or release-note features have already been implemented.

## Select and inspect bundles

- Unless the user specifies a selection, discover the JSON bundle definitions directly under `skills/bundles/` and process each independently. Read each definition to identify its name, version, selected skills, and icon. Preserve unrelated changes and report a failure for one bundle without abandoning the others.
- For the coding-guidelines bundle, run `skills/Sync-CodingGuidelines.ps1` before comparing and packaging so that the included references match the maintained instructions. Respect `-WhatIf` and do not synchronize during a preview.
- Before replacing an existing archive, inspect its `plugin.json`, `bundle-manifest.json`, and embedded source files. The current default archive is `skills/_bundles/<bundle-name>.plugin.zip`; use the actual destination if specified. Compare the archived bytes and manifest inventory against the current selected content, including licenses, configuration, and icon as relevant. Use Git history and diffs as supporting evidence, including uncommitted changes; do not assume a Git commit captures the archived bytes. Avoid executing embedded files.
- An archive is a baseline for the last **locally packaged** version, not proof of the version uploaded to ChatGPT. If the prior archive or meaningful baseline is unavailable, state that the comparison is incomplete and use only evidence available. Never invent a change or claim that nothing changed because evidence is missing.

## Draft notes and package

Maintain a separate Markdown changelog beside each configuration, named `<configuration-stem>.changelog.md`. Preserve existing entries. Summarize meaningful user-facing changes in a dated section for the new version, and identify uncertain or unverified changes. If a reliable comparison shows no substantive changes, say so; if the baseline is missing, say the comparison was unavailable. Do not equate a rebuild with an uploaded release.

The current packager reads the version from the configuration and packages only one definition per invocation. Unless its interface has since changed, use this procedure:

1. Choose the next patch version from the configuration; honor an explicit minor or major increment by resetting lower components. If the prior archive has a higher version, use the higher local version as the baseline and explain the discrepancy. An uploaded version may be higher still; if the user supplies it, use it as a minimum baseline. Validate three numeric components and reject invalid or ambiguous values rather than guessing.
2. Capture the existing configuration and changelog state, and preserve the old archive until comparison is complete. Update only the configuration's version, preserving its other values and formatting. Add the new changelog entry before invoking `Package-Skills.ps1 -ConfigPath <configuration>` so the generated skill displays the changelog. Confirm the archive exists, both its root `plugin.json` and embedded `bundle-manifest.json` contain the intended version, and its generated `SKILL.md` contains the intended changelog.
3. If packaging fails, restore the configuration and changelog only if each still matches what this invocation wrote and has not otherwise changed. Do not overwrite concurrent edits. Report the failure and any remaining inconsistency. If archive verification fails after packaging, report the exact archive, configuration, and changelog state; do not pretend the build was rolled back. Never reuse a version already present in a successfully created archive without explicitly reconciling it first.

Before applying changes, check for evidence of another active build of the same bundle. If concurrent modification is detected, stop processing that bundle and report it. For a preview, inspect and report selections, proposed versions, notes, and missing baselines without changing configuration, changelogs, source references, or archives. Follow the packager's validation and `-WhatIf` behavior; do not introduce new packager parameters or silently edit the packager to implement this workflow.

Report each bundle's previous and new local version, archive and changelog paths, summary of notes, and failures or baseline limitations. Note that actual ChatGPT acceptance requires an upload and that the service's current version cannot be inferred from a local archive.
