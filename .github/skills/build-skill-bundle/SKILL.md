---
name: build-skill-bundle
description: Build or preview the local Agent Toolkit skill bundle using the repository's PowerShell build scripts. Use when asked to build, rebuild, or validate the local bundle archive.
---

# Build the local skill bundle

Use this project skill to create the Agent Toolkit plugin archive from the repository's configured skill selection.

## Build

Run commands from the repository root. PowerShell 7 and Git are required.

- For a preview, run `./skills/New-AgentToolkitBundle.ps1 -WhatIf`. This does not synchronize references or write an archive.
- For a build, run `./skills/New-AgentToolkitBundle.ps1`. It refreshes the embedded general, PowerShell, and Shell coding references, then packages the skills selected in `skills/bundles/agent-toolkit.json`.

The default output is `skills/_bundles/agent-toolkit.plugin.zip`. Before replacing it, the build compares the selection with its manifest and reports additions, removals, and path moves. For any selection change, it requires a newer version and a matching changelog section naming each added and removed skill. If the guard reports changes, update the version and changelog using its results, distinguish moves from additions and removals, and rerun the build. Review the notes for accuracy; the name check cannot assess their meaning. If the baseline is missing or unreadable, report the limitation and use Git history where available; do not claim the comparison is complete. A preview performs the same checks without writing files.

## Check the result

Read the command output and confirm the reported status is `Packaged`, the output path is the expected archive, and the archive exists. The packager reopens the ZIP and checks that its entries match the validated file plan. If the user asks for bundle-content validation or a release review, inspect the archive's root `plugin.json`, embedded `bundle-manifest.json`, selected skill inventory, and generated skill guidance against `skills/bundles/agent-toolkit.json` and `skills/bundles/agent-toolkit.changelog.md`.

Report the archive path, status, selected skill count, entry count, and any failures. Local archive checks do not establish acceptance by ChatGPT's importer.

## Scope

- Use `skills/New-AgentToolkitBundle.ps1` for the unified Agent Toolkit bundle so the coding references are refreshed before packaging.
- Use `skills/New-SkillArchive.ps1` directly only when the user names a custom bundle configuration, output directory, or archive format.
- Preserve other bundles and source files. Do not commit, upload, or publish the archive unless the user asks.
- Project-maintenance skills live under `.github/skills/`; the packager only accepts explicit selections under `skills/personal/` or `skills/community/`, so these maintenance skills are not included in distributable bundles.
