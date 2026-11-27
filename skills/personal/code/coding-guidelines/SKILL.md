---
name: coding-guidelines
description: Apply Greg Tate's coding instructions before editing PowerShell or Shell scripts. Read the bundled general coding guide and the applicable language guide first.
---

# Apply the coding instructions

These instructions are bundled with this skill, so they are available in ChatGPT without access to the Agent-Toolkit repository. Before editing code, read the general guide and the applicable specialist guide from `references/`:

- Always read `references/General Coding Guidelines.instructions.md`.
- For `.ps1`, `.psm1`, or `.psd1` files, also read `references/PowerShell Style Guidelines.instructions.md`.
- For Shell scripts, also read `references/Shell Style Guidelines.instructions.md`.

Follow the bundled files as the source of truth. Preserve existing file conventions and unrelated edits. Recheck the finished diff against the general and applicable specialist guide. The Agent-Toolkit bundle builder refreshes these reference copies from the maintained `instructions/` files before packaging.
