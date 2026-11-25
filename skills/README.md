# Skill packaging

[Package-Skills.ps1](./Package-Skills.ps1) combines explicitly selected personal and
community skills into a plugin ZIP for ChatGPT. Choose the source folders
in [bundles/agent-toolkit.json](./bundles/agent-toolkit.json). Generated archives
go to `_bundles/`, which is excluded from Git.

Run from the Agent-Toolkit root using PowerShell 7 and Git:

```powershell
# Preview the unified build without copying references or creating files.
./skills/Build-SkillBundle.ps1 -WhatIf

# Refresh coding guidance and build Agent Toolkit.
./skills/Build-SkillBundle.ps1

# Build another selection or use a different destination and enclosing layout.
./skills/Package-Skills.ps1 -ConfigPath ./skills/bundles/my-bundle.json
./skills/Package-Skills.ps1 -Format Skill -OutputDirectory ./release -Layout Folder
```

## Agent Toolkit bundle

**Agent Toolkit** is the single bundle for documentation, implementation planning,
and coding guidance. It includes all eight skills from the former documentation
(0.2.3), coding-guidelines (0.1.5), and implementation-planning (0.1.0) bundles.
Its new identity starts at version 1.0.0. Maintain the version and selections in
[agent-toolkit.json](./bundles/agent-toolkit.json) and release notes in
[agent-toolkit.changelog.md](./bundles/agent-toolkit.changelog.md), which also
preserves the three predecessor histories. The shared document-and-checkmark
icon represents the combined workflow.

Upload `_bundles/agent-toolkit.plugin.zip` in ChatGPT's New Plugin dialog.
After verifying the unified plugin, remove the three previous plugins from
ChatGPT to avoid duplicate guidance. Previous local archives are retained under
`_bundles/legacy/`; they are historical builds, not active configurations.

## Implementation-planning skill

[Implementation planning](./personal/implementation-planning/SKILL.md) creates
paired Word implementation plans and native Google Sheets task trackers. It uses
the planning patterns from the M365 Knowledge Automation, Hermes, and ALZ runner
migration examples, with stable identifiers, phase gates, and evidence-based
progress. Its references retain source links without copying project documents.

The unified bundle includes the planning skill and its supporting references.
It contains workflow instructions; Word authoring and connected Google Sheets
capabilities must be available in the destination environment.

For local Codex discovery, expose the physical source skill folder under the user
skills directory, `~/.agents/skills/implementation-planning`. A directory link
keeps the maintained repository copy authoritative. Invoke it with
`$implementation-planning`, for example: "Create a Word implementation plan and
a Google Sheets task tracker for this project using its existing documents."

## Coding-guidelines synchronization

The unified build first refreshes the general, PowerShell, and Shell instruction copies
inside `personal/coding-guidelines/references`, then packages all selected skills
using [bundles/agent-toolkit.json](./bundles/agent-toolkit.json). The
plugin archive is written to `_bundles/agent-toolkit.plugin.zip`.
Run [Sync-CodingGuidelines.ps1](./Sync-CodingGuidelines.ps1) by itself to refresh
the embedded references without building the archive.
The lower-level [Package-Skills.ps1](./Package-Skills.ps1) uses the same default
configuration but does not synchronize instruction copies on its own.

The command returns the output path, status, selected skill count, entry count,
and size. Rebuilding replaces only the bundle with the same name. Other bundles
remain in the output directory; removing a skill from a configuration removes it
from that bundle on the next successful build.

## Choose skills

Edit [bundles/agent-toolkit.json](./bundles/agent-toolkit.json) to maintain the
shared selection. `name`, `version`, `description`, and
`skills` are required; unknown configuration keys are rejected.
An optional `icon` names a PNG directly under `skills/bundles/`, relative to
`skills/`. Plugin builds include it and reference it as the plugin logo and
composer icon; standalone skill archives do not use it.
An optional `composerIcon`, using the same path rules, overrides the composer
icon while leaving the plugin logo unchanged.

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

Paths in `skills` are relative to this directory, independent of the config's
location. Paths must name exact physical skill directories below `personal/` or
`community/`; wildcards, traversal, and duplicate skill names are rejected. The
directory must contain a root `SKILL.md` whose name matches the directory name.
The bundle name uses lowercase letters, digits, and single hyphens (64 characters
maximum); its version uses `major.minor.patch`. The description is the installed
bundle's trigger description: write it to cover the skills you select.

Examples of existing selections:

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

Community sources must already be local Git checkouts and have a license file
inside the skill or an ancestor directory. The command does not clone, update,
install, or modify them. Retaining license text is attribution preservation, not
an automated determination of redistribution rights. Review each selection for
suitability and licensing before distribution.

## Archive contents and import

The default archive contains:

```text
plugin.json
skills/
  agent-toolkit/
    SKILL.md
    bundle-manifest.json
    references/skills/...
```

The generated skill lists and links the selected guidance. It also displays the contents of a matching
`<configuration-stem>.changelog.md` beside the bundle configuration, if present.
Write the changelog before packaging so the archive includes the intended notes.
In ChatGPT's New Plugin dialog, upload the generated `.plugin.zip` file. The plugin manifest is
at the archive root; the composed skill is under `skills/`. Use `-Format Skill`
to create the previous standalone `.skill` format; `-Layout Folder` is available
for that format. Actual acceptance must be checked in your account; local archive
validation does not exercise ChatGPT's importer.

This imports **one composed skill**. Its embedded source skills are guidance
resources, not separately installed skills with individual selectors. Their
relative file structure and bytes are preserved. References outside a selected
directory, tool integrations, other installed skills, and machine-specific paths
are not automatically resolved or adapted. Select any additional guidance needed
and review platform assumptions before use. Packaging never executes source scripts.

[OpenAI's skills guidance](https://learn.chatgpt.com/docs/build-skills) describes
skill metadata and progressive loading.
[Plugin packaging](https://developers.openai.com/plugins/build/plugins) describes
the plugin manifest and skill directory structure used by the default archive.

## Validation and provenance

Before writing output, the command checks the complete selection and enumerates
its files. It checks frontmatter delimiters and required `name` and `description`
fields (single-line scalar values or a block description), not arbitrary YAML
syntax. It preserves hidden supporting files and excludes Git metadata, GitHub
automation, Python caches/bytecode, virtual environments, Node dependencies, and
operating system metadata. Links and junctions are rejected with the offending
path; materialize required content into a maintained physical directory first.

Ancestor `LICENSE`, `LICENCE`, `COPYING`, and `NOTICE` files are copied into each
embedded skill's `licenses/` directory. Files already inside the skill retain
their original paths. The generated manifest records source-relative selections,
origin URLs, current commits, selected-directory dirty status, and SHA-256 hashes
of every embedded source/license file. A commit identifies the checkout base;
hashes identify the actual packaged bytes when local changes exist.

The archive is built in a unique temporary file, reopened, and checked against the
planned entries before replacing the previous output. Temporary files are removed
on success or failure. `-WhatIf` performs read-only preflight and reports the target
without creating an output directory. Custom output cannot be placed in personal
or community source directories.

Use the unified build's `-WhatIf` preview to validate selections before packaging.
The previously documented `tests/Test-PackageSkills.ps1` is absent from this
checkout. Verify the generated plugin manifest, embedded bundle version, selected
skill inventory, file hashes, and changelog when checking a local release.
