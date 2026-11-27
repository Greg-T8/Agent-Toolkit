---
name: build-skill-bundle
description: Build, preview, or validate the Agent Toolkit or Matt Pocock plugin bundle using the repository's PowerShell packaging scripts.
---

# Build a local skill bundle

Use this project skill to build the requested local plugin bundle. Run commands from the repository root. PowerShell 7 and Git are required.

## Choose the bundle

- For the unified Agent Toolkit bundle, use `skills/New-AgentToolkitBundle.ps1`. If the user names no bundle, this remains the default.
- For Matt Pocock's upstream bundle, use `skills/bundles/matt-pocock/matt-pocock.json` and `skills/bundles/matt-pocock/matt-pocock.changelog.md` with `skills/New-SkillArchive.ps1`. Do not run the Agent Toolkit wrapper for this bundle: it refreshes Agent Toolkit coding references and checks only the Agent Toolkit selection.
- Use `New-SkillArchive.ps1` directly for another bundle only when the user names its configuration, output directory, or archive format.

## Build the Agent Toolkit bundle

- For a preview, run `./skills/New-AgentToolkitBundle.ps1 -WhatIf`. This does not synchronize references or write an archive.
- For a build, run `./skills/New-AgentToolkitBundle.ps1`. It refreshes the embedded general, PowerShell, and Shell coding references, then packages the skills selected in `skills/bundles/agent-toolkit/agent-toolkit.json`.

The default output is `skills/_bundles/agent-toolkit.plugin.zip`. Before replacing it, the wrapper compares the selection with its manifest and reports additions, removals, and path moves. For any selection change, it requires a newer version and a matching changelog section naming each added and removed skill. If the guard reports changes, update the version and changelog using its results, distinguish moves from additions and removals, and rerun the build. Review the notes for accuracy; the name check cannot assess their meaning. If the baseline is missing or unreadable, report the limitation and use Git history where available; do not claim the comparison is complete. A preview performs the same checks without writing files.

## Build the Matt Pocock bundle

Use this workflow when the user names Matt Pocock, the `matt-pocock` bundle, or its configuration. Its archive is `skills/_bundles/matt-pocock.plugin.zip`.

1. Read `skills/bundles/matt-pocock/matt-pocock.json`, its matching changelog, the previous local archive when present, and the current upstream checkout under `skills/community/mattpocock`. Check the configured selection, upstream remote and commit, working-tree status, and archive manifest. Do not discard source changes or assume the local archive matches the installed ChatGPT version.
2. Compare the archive's source-file hashes with the currently selected files and licenses, and review configuration and generated-entrypoint changes. If packaged content changed, including the personal adapter or upstream skill contents without a selection change, increment the version and add a matching changelog entry before building. Record the chosen upstream commit for upstream changes. `New-SkillArchive.ps1` does not enforce this version-and-changelog guard. If the archive baseline is missing or unreadable, report that the comparison is incomplete and use available Git history; do not infer that there were no changes.
3. Preview with `./skills/New-SkillArchive.ps1 -ConfigPath ./skills/bundles/matt-pocock/matt-pocock.json -WhatIf`. After updating any required version and changelog, build with the same command without `-WhatIf`. Do not synchronize or modify Matt's upstream files as part of packaging.
4. Confirm `Packaged`, the expected archive path, and the reported skill and entry counts. Reopen the ZIP and check root `plugin.json`, `skills/matt-pocock/bundle-manifest.json`, the configured skill inventory and provenance, file hashes, license notices, and `skills/matt-pocock/SKILL.md`. Confirm the generated entry point routes through the configured `matt-pocock-adapter` and includes the current changelog.
5. Report local packaging separately from ChatGPT import or interactive behavior. The archive check does not prove that the plugin imports or that the host renders interactive questionnaires.

## Check the result

Read the command output and confirm the reported status is `Packaged`, the output path is the expected archive, and the archive exists. The packager reopens the ZIP and checks that its entries match the validated file plan. If the user asks for bundle-content validation or a release review, inspect the archive's root `plugin.json`, embedded `bundle-manifest.json`, selected skill inventory, and generated skill guidance against the configuration and changelog for the requested bundle.

Report the archive path, status, selected skill count, entry count, and any failures. Local archive checks do not establish acceptance by ChatGPT's importer.

## Scope

- Use `skills/New-AgentToolkitBundle.ps1` only for the unified Agent Toolkit bundle so its coding references are refreshed before packaging.
- Use `skills/New-SkillArchive.ps1 -ConfigPath ./skills/bundles/matt-pocock/matt-pocock.json` for the Matt Pocock bundle and apply its manual release checks above.
- Preserve other bundles and source files. Do not commit, upload, or publish the archive unless the user asks.
- Project-maintenance skills live under `.github/skills/`; the packager only accepts explicit selections under `skills/personal/` or `skills/community/`, so these maintenance skills are not included in distributable bundles.
