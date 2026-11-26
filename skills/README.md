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

The **Agent Toolkit** bundle combines technical documentation, editorial style, implementation planning, Google Workspace design, and coding guidance. Its selected skills and version are defined in [agent-toolkit.json](./bundles/agent-toolkit.json); its release history is in [agent-toolkit.changelog.md](./bundles/agent-toolkit.changelog.md). The shared document-and-checkmark icon identifies the combined workflow.

The implementation-planning skill creates paired Word plans and native Google Sheets trackers, with stable identifiers, phase gates, and evidence-based progress. Its [source patterns](./personal/implementation-planning/references/source-patterns.md) retain links to examples without copying project documents. Word authoring and connected Google Sheets capabilities must also be available in the destination environment.

The editorial-style skill is the house style for every piece of writing the bundle produces, including emails and messages. Its [decision register](./personal/editorial-style/references/decision-register.md) resolves the Microsoft Writing Style Guide, Google developer documentation style, plain-language guidance, and the Chicago Manual of Style into one set of rules, ranks above the community writing skills, and adds Greg's house rules. Its [`editorial_check.py`](./personal/editorial-style/scripts/editorial_check.py) checks Markdown and plain-text drafts, and the Google Docs audit runs the same checks.

The Google Workspace design skill applies only to native Google Docs and Sheets; it does not change the planning skill's Word default. Its [shared palette](./personal/google-workspace-design/references/palette.md), [Docs specification](./personal/google-workspace-design/references/docs-spec.md), and [Sheets specification](./personal/google-workspace-design/references/sheets-spec.md) define the fonts, colors, and components. The [master Doc](https://docs.google.com/document/d/1kIyDWS-94bJnd8DMOh0CyuT0KQCYLdX8f-RK_UPj5kY/edit) and [master tracker](https://docs.google.com/spreadsheets/d/1wqDjwWAfDV8x-0xfHKqttQSARyZORg2QpGeIzEgxdRw/edit) show the designs; both are in the [Agent Toolkit Templates folder](https://drive.google.com/drive/folders/1gm07fxx16bvRZuDfAH5idGONyFDXbZiw).

To discover the implementation-planning skill in local Codex, expose its physical source folder under `~/.agents/skills/implementation-planning`. A directory link keeps the maintained repository copy authoritative. Invoke it with `$implementation-planning`, for example: "Create a Word implementation plan and a Google Sheets task tracker for this project using its existing documents."

## Build and import the plugin

Upload `_bundles/agent-toolkit.plugin.zip` in ChatGPT's New Plugin dialog. After you verify the unified plugin, remove the three previous plugins to avoid duplicate guidance. Previous local archives remain under `_bundles/legacy/` as historical builds; they do not define the active configuration.

The plugin archive contains `plugin.json` at its root and one composed skill under `skills/agent-toolkit/`. The composed skill routes requests to the selected guidance embedded in `references/skills/`. Those source skills are guidance resources within one skill; they are not separate skills with individual selectors.

To create the previous standalone `.skill` format, pass `-Format Skill` to [New-SkillArchive.ps1](./New-SkillArchive.ps1). That format supports `-Layout Folder`. Plugin format requires the root layout. Local archive validation does not test ChatGPT's importer, so verify acceptance in your account.

The package preserves each selected skill's relative file structure and bytes. It does not resolve references outside selected directories, provide tool integrations, install other skills, or adapt machine-specific paths. Packaging never executes source scripts. Review platform assumptions and select any additional guidance the destination needs.

See [OpenAI's skills guidance](https://learn.chatgpt.com/docs/build-skills) for skill metadata and progressive loading. See [plugin packaging](https://developers.openai.com/plugins/build/plugins) for the plugin manifest and skill directory structure.

## Refresh coding guidance

The unified build first refreshes the general, PowerShell, and Shell instruction copies in `personal/coding-guidelines/references`, then packages the skills selected in [agent-toolkit.json](./bundles/agent-toolkit.json). To refresh those embedded references without building an archive, run [Sync-CodingGuidelines.ps1](./Sync-CodingGuidelines.ps1). The lower-level [New-SkillArchive.ps1](./New-SkillArchive.ps1) uses the configured selections but does not refresh the instruction copies.

The build reports the output path, status, selected skill count, archive entry count, and file size. Rebuilding replaces the archive with the same bundle name and leaves other bundles in the output directory. Removing a skill from a configuration removes it from that bundle on the next successful build.

## Choose skills

Edit [agent-toolkit.json](./bundles/agent-toolkit.json) to maintain the bundle selection. A configuration requires `name`, `version`, `description`, and `skills`; unknown keys are rejected. The optional `icon` names a PNG under `skills/bundles/`, relative to `skills/`. Plugin builds use it as the plugin logo and composer icon. Standalone skill archives do not use it. The optional `composerIcon` follows the same path rules and overrides the composer icon without changing the plugin logo.

For example, this configuration selects two personal skills:

```json
{
  "name": "azure-authoring",
  "version": "0.1.0",
  "description": "Use for Azure infrastructure authoring and Mermaid architecture diagram styling.",
  "skills": [
    "personal/bicep-azure",
    "personal/mermaid-styling"
  ]
}
```

Skill paths are relative to the `skills/` directory, regardless of the configuration file's location. Each path must identify an exact physical skill directory under `personal/` or `community/`. The packager rejects wildcards, path traversal, and duplicate skill names. Each selected directory must contain a root `SKILL.md` whose `name` matches the directory name.

Use lowercase letters, digits, and single hyphens for the bundle name; the name can contain up to 64 characters. Set the version to `major.minor.patch`. Write the description to describe the selected skills and trigger their use.

The following table shows example source paths:

| Source | Selection path |
| --- | --- |
| Personal | `personal/bicep-azure` |
| Personal | `personal/terraform-azure` |
| Personal | `personal/terraform-ad-lab` |
| Personal | `personal/mermaid-styling` |
| Personal | `personal/markdown-link-resolver` |
| Wondel.ai | `community/wondelai/technical-documentation` |
| Matt Pocock | `community/mattpocock/skills/engineering/to-spec` |
| Anthropic | `community/anthropic/skills/doc-coauthoring` |

Community sources must already be local Git checkouts with a license file in the skill or one of its ancestor directories. The packager does not clone, update, install, or modify these sources. It retains license text for attribution, but does not determine whether redistribution is permitted. Review each selection's suitability and license before distribution.

## Package a custom bundle

To build a different selection or choose another output directory and layout, run these commands from the repository root:

```powershell
# Package a plugin using a custom bundle configuration.
./skills/New-SkillArchive.ps1 -ConfigPath ./skills/bundles/my-bundle.json

# Create a standalone skill archive in a folder layout.
./skills/New-SkillArchive.ps1 -Format Skill -OutputDirectory ./release -Layout Folder
```

## Validation and provenance

Before creating an archive, the packager validates the full selection and enumerates its files. It checks `SKILL.md` frontmatter delimiters and the required `name` and `description` fields. It accepts single-line scalar values or a block description; it does not validate all YAML syntax.

The packager preserves hidden supporting files and excludes Git metadata, GitHub automation, Python caches and bytecode, virtual environments, Node dependencies, and operating-system metadata. It rejects links and junctions with the offending path. Materialize any required linked content in a maintained physical directory before packaging.

The packager copies ancestor `LICENSE`, `LICENCE`, `COPYING`, and `NOTICE` files into each embedded skill's `licenses/` directory. It retains files inside the selected skill at their original relative paths. The generated manifest records source-relative selections, repository URLs, commits, selected-directory dirty status, and SHA-256 hashes for every embedded source and license file. A commit identifies the checkout base; hashes identify the packaged bytes when local changes exist.

The packager builds the archive in a unique temporary file, reopens it, and checks its entries against the validated plan before replacing the previous output. It removes the temporary file on success or failure. The `-WhatIf` option performs a read-only preflight and reports the target without creating an output directory. Custom output directories must remain outside `personal/` and `community/`.

Use [New-AgentToolkitBundle.ps1](./New-AgentToolkitBundle.ps1) with `-WhatIf` to preview the unified build. When reviewing a release, verify the plugin manifest, embedded bundle version, selected skill inventory, file hashes, and changelog. Local archive checks do not verify acceptance by ChatGPT's importer.
