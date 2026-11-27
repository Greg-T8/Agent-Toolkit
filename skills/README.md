# Skill packaging

If you maintain ChatGPT skills in this repository, use this guide to configure and build their archives. It covers packaging and importing skills, not authoring individual skills. The unified build refreshes embedded coding guidance and packages the selected skills as the Agent Toolkit plugin.

## Before you begin

Install PowerShell 7 and Git. Run the commands in this guide from the Agent-Toolkit repository root.

## Build the Agent Toolkit bundle

To preview the build without refreshing references or creating files, run:

```powershell
# Preview the unified build without copying references or creating files.
./skills/New-AgentToolkitBundle.ps1 -WhatIf
```

To refresh the coding guidance and create the plugin archive, run:

```powershell
# Refresh coding guidance, then package the Agent Toolkit bundle.
./skills/New-AgentToolkitBundle.ps1
```

The build writes `_bundles/agent-toolkit.plugin.zip`. The `_bundles/` directory is excluded from Git. For another bundle or output format, use [New-SkillArchive.ps1](./New-SkillArchive.ps1) directly.

## Agent Toolkit bundle

The **Agent Toolkit** bundle combines technical documentation, editorial style, implementation planning, Google Workspace design, and coding guidance. Its selected skills and version are defined in [agent-toolkit.json](./bundles/agent-toolkit/agent-toolkit.json); its release history is in [agent-toolkit.changelog.md](./bundles/agent-toolkit/agent-toolkit.changelog.md). The shared document-and-checkmark icon identifies the combined workflow.

The implementation-planning skill creates paired Word plans and native Google Sheets trackers, with stable identifiers, phase gates, and evidence-based progress. Its [source patterns](./personal/productivity/implementation-planning/references/source-patterns.md) retain links to examples without copying project documents. Word authoring and connected Google Sheets capabilities must also be available in the destination environment.

The editorial-style skill is the house style for every piece of writing the bundle produces, including emails and messages. Its [decision register](./personal/writing/editorial-style/references/decision-register.md) resolves the Microsoft Writing Style Guide, Google developer documentation style, plain-language guidance, and the Chicago Manual of Style into one set of rules, ranks above the community writing skills, and adds Greg's house rules. Its [`editorial_check.py`](./personal/writing/editorial-style/scripts/editorial_check.py) checks Markdown and plain-text drafts, and the Google Docs audit runs the same checks.

The Google Workspace design skill applies only to native Google Docs and Sheets; it does not change the planning skill's Word default. Its [shared palette](./personal/documents/google-workspace-design/references/palette.md), [Docs specification](./personal/documents/google-workspace-design/references/docs-spec.md), and [Sheets specification](./personal/documents/google-workspace-design/references/sheets-spec.md) define the fonts, colors, and components. The [master Doc](https://docs.google.com/document/d/1kIyDWS-94bJnd8DMOh0CyuT0KQCYLdX8f-RK_UPj5kY/edit) and [master tracker](https://docs.google.com/spreadsheets/d/1wqDjwWAfDV8x-0xfHKqttQSARyZORg2QpGeIzEgxdRw/edit) show the designs; both are in the [Agent Toolkit Templates folder](https://drive.google.com/drive/folders/1gm07fxx16bvRZuDfAH5idGONyFDXbZiw).

To discover the implementation-planning skill in local Codex, expose its physical source folder under `~/.agents/skills/implementation-planning`. A directory link keeps the maintained repository copy authoritative. Invoke it with `$implementation-planning`, for example: "Create a Word implementation plan and a Google Sheets task tracker for this project using its existing documents."

## Build and import the plugin

Upload `_bundles/agent-toolkit.plugin.zip` in ChatGPT's New Plugin dialog. After you verify the unified plugin, remove the three previous plugins to avoid duplicate guidance. Previous local archives remain under `_bundles/legacy/` as historical builds; they do not define the active configuration.

The plugin archive contains `plugin.json` at its root and one composed skill under `skills/agent-toolkit/`. The composed skill routes requests to the selected guidance embedded in `references/skills/`. Those source skills are guidance resources within one skill; they are not separate skills with individual selectors.

To create the previous standalone `.skill` format, pass `-Format Skill` to [New-SkillArchive.ps1](./New-SkillArchive.ps1). That format supports `-Layout Folder`. Plugin format requires the root layout. Local archive validation does not test ChatGPT's importer, so verify acceptance in your account.

The package preserves each selected skill's relative file structure and bytes. It does not resolve references outside selected directories, provide tool integrations, install other skills, or adapt machine-specific paths. Packaging never executes source scripts. Review platform assumptions and select any additional guidance the destination needs.

See [OpenAI's skills guidance](https://learn.chatgpt.com/docs/build-skills) for skill metadata and progressive loading. See [plugin packaging](https://developers.openai.com/plugins/build/plugins) for the plugin manifest and skill directory structure.

## Refresh coding guidance

The unified build first refreshes the general, PowerShell, and Shell instruction copies in `personal/code/coding-guidelines/references`, then packages the skills selected in [agent-toolkit.json](./bundles/agent-toolkit/agent-toolkit.json). To refresh those embedded references without building an archive, run [Sync-CodingGuidelines.ps1](./Sync-CodingGuidelines.ps1). The lower-level [New-SkillArchive.ps1](./New-SkillArchive.ps1) uses the configured selections but does not refresh the instruction copies.

The build compares the current skill selection with the existing local archive before replacing it. If skills were added, removed, or moved, it requires a newer version and a changelog section for that version naming each added and removed skill. Update the version and changelog before rebuilding; review the notes for accuracy because the name check does not interpret their meaning. If the previous archive is missing or unreadable, the build warns that no comparison is available. The archive reflects the last local build, which may differ from an uploaded version.

The build reports the output path, status, selected skill count, archive entry count, and file size. Rebuilding replaces the archive with the same bundle name and leaves other bundles in the output directory. Removing a skill from a configuration removes it from that bundle on the next successful build.

## Choose skills

Edit [agent-toolkit.json](./bundles/agent-toolkit/agent-toolkit.json) to maintain the bundle selection. A configuration requires `name`, `version`, `description`, and `skills`; unknown keys are rejected. The optional `routingSkill` names a selected skill that the generated entry point instructs the host to read first. The optional `icon` names a PNG in a bundle directory under `skills/bundles/`, relative to `skills/`. Plugin builds use it as the plugin logo and composer icon. Standalone skill archives do not use it. The optional `composerIcon` follows the same path rules and overrides the composer icon without changing the plugin logo.

For example, this configuration selects two personal skills:

```json
{
  "name": "azure-authoring",
  "version": "0.1.0",
  "description": "Use for Azure infrastructure authoring and Mermaid architecture diagram styling.",
  "skills": [
    "personal/devops/bicep-azure",
    "personal/design/mermaid-styling"
  ]
}
```

Skill paths are relative to the `skills/` directory, regardless of the configuration file's location. Each path must identify an exact physical skill directory under `personal/` or `community/`. The packager rejects wildcards, path traversal, and duplicate skill names. Each selected directory must contain a root `SKILL.md` whose `name` matches the directory name.

Personal skills are grouped under their matching Skills Atlas theme folder:

| Theme | Personal skills |
| --- | --- |
| `code` | `coding-guidelines` |
| `design` | `mermaid-styling` |
| `devops` | `bicep-azure`, `package-skill-bundles`, `terraform-ad-lab`, `terraform-azure` |
| `documents` | `google-workspace-design` |
| `productivity` | `grill-interview-adapter`, `implementation-planning` |
| `writing` | `editorial-style`, `markdown-link-resolver` |

Use lowercase letters, digits, and single hyphens for the bundle name; the name can contain up to 64 characters. Set the version to `major.minor.patch`. Write the description to describe the selected skills and trigger their use.

The following table shows example source paths:

| Source | Selection path |
| --- | --- |
| Personal | `personal/devops/bicep-azure` |
| Personal | `personal/devops/terraform-azure` |
| Personal | `personal/devops/terraform-ad-lab` |
| Personal | `personal/design/mermaid-styling` |
| Personal | `personal/writing/markdown-link-resolver` |
| Wondel.ai | `community/wondelai/technical-documentation` |
| Matt Pocock | `community/mattpocock/skills/engineering/to-spec` |
| Anthropic | `community/anthropic/skills/doc-coauthoring` |

Community sources must already be local Git checkouts with a license file in the skill or one of its ancestor directories. The packager does not clone, update, install, or modify these sources. It retains license text for attribution, but does not determine whether redistribution is permitted. Review each selection's suitability and license before distribution.

## Package a custom bundle

To build a different selection or choose another output directory and layout, run these commands from the repository root:

```powershell
# Package a plugin using a custom bundle configuration.
./skills/New-SkillArchive.ps1 -ConfigPath ./skills/bundles/my-bundle/my-bundle.json

# Create a standalone skill archive in a folder layout.
./skills/New-SkillArchive.ps1 -Format Skill -OutputDirectory ./release -Layout Folder
```

## Release the Matt Pocock bundle

The [Matt Pocock configuration](./bundles/matt-pocock/matt-pocock.json) packages a small selection from the [upstream repository](https://github.com/mattpocock/skills). Its [changelog](./bundles/matt-pocock/matt-pocock.changelog.md) records the bundle's releases. This is Greg's independent packaging, not an upstream publication. It does not change the Agent Toolkit bundle.

The archive contains one composed skill, not independently selectable upstream skills. Its entry point directs interview requests through the personal [grill-interview-adapter](./personal/productivity/grill-interview-adapter/SKILL.md). The adapter loads `grilling` directly for `grill-me`, and both `grilling` and `domain-modeling` for `grill-with-docs`; the upstream files and formats remain unchanged. The documentation workflow needs access to the relevant project and files. Interactive questionnaires depend on host capabilities. Test both routing and behavior in the destination before expanding the selection.

For each release:

1. Inspect the upstream checkout's remote, commit, and working-tree status. Review upstream changes, licenses, skill dependencies, host requirements, and the proposed selection before updating to a chosen commit. Do not discard local changes. Exclude experimental skills unless they have been reviewed for the destination.
2. Compare the previous local archive's manifest and embedded file hashes with the selected source files, licenses, and configuration. The archive is only the last local build, not evidence of the installed version. If it is missing or unreadable, state that the comparison is incomplete and use available Git history; never assume there were no changes.
3. Update the bundle version and matching changelog before packaging. Use a new version whenever packaged content changes, even when the selection is unchanged. Describe additions, removals, moves, relevant upstream changes, and the selected upstream commit. Do not reuse a version already built with different content.
4. Preview and build only this bundle with PowerShell 7:

   ```powershell
   # Validate the selection without creating an archive.
   ./skills/New-SkillArchive.ps1 -ConfigPath ./skills/bundles/matt-pocock/matt-pocock.json -WhatIf

   # Package the reviewed Matt Pocock selection.
   ./skills/New-SkillArchive.ps1 -ConfigPath ./skills/bundles/matt-pocock/matt-pocock.json
   ```

5. Reopen `_bundles/matt-pocock.plugin.zip` and verify the root plugin manifest, bundle manifest, version, source commit and dirty status, selected files and hashes, license notices, and generated guidance and changelog. The shared packager's archive check is a structural check, not a ChatGPT import test.
6. When ready to test in ChatGPT, import the archive and check discovery, adapter routing, whole-round interaction or the Markdown fallback, and both workflows loading their dependencies. Check `grill-with-docs` against an accessible project and its glossary and ADR formats. Record which behaviors worked and any unavailable tools. Only add other engineering workflows after reviewing their setup, repository, issue-tracker, and tool requirements.

The selection and version guard in `New-AgentToolkitBundle.ps1` applies only to the Agent Toolkit build. Custom bundles use the manual comparison and release checks above; `New-SkillArchive.ps1` does not enforce a version increase when content changes.

## Validation and provenance

Before creating an archive, the packager validates the full selection and enumerates its files. It checks `SKILL.md` frontmatter delimiters and the required `name` and `description` fields. It accepts single-line scalar values or a block description; it does not validate all YAML syntax.

The packager preserves hidden supporting files and excludes Git metadata, GitHub automation, Python caches and bytecode, virtual environments, Node dependencies, and operating-system metadata. It rejects links and junctions with the offending path. Materialize any required linked content in a maintained physical directory before packaging.

The packager copies ancestor `LICENSE`, `LICENCE`, `COPYING`, and `NOTICE` files into each embedded skill's `licenses/` directory. It retains files inside the selected skill at their original relative paths. The generated manifest records source-relative selections, repository URLs, commits, selected-directory dirty status, and SHA-256 hashes for every embedded source and license file. A commit identifies the checkout base; hashes identify the packaged bytes when local changes exist.

The packager builds the archive in a unique temporary file, reopens it, and checks its entries against the validated plan before replacing the previous output. It removes the temporary file on success or failure. The `-WhatIf` option performs a read-only preflight and reports the target without creating an output directory. Custom output directories must remain outside `personal/` and `community/`.

Use [New-AgentToolkitBundle.ps1](./New-AgentToolkitBundle.ps1) with `-WhatIf` to preview the unified build. When reviewing a release, verify the plugin manifest, embedded bundle version, selected skill inventory, file hashes, and changelog. Local archive checks do not verify acceptance by ChatGPT's importer.
