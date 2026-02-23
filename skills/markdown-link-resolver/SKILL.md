---
name: markdown-link-resolver
description: 'Resolve bare or untitled URLs in markdown files into proper markdown links with page titles. Use when asked to resolve links, add titles to URLs, fix bare links, or convert raw URLs to titled markdown links.'
user-invokable: true
argument-hint: '[file or selection]'
---

# SKILL: Convert Raw URLs to Friendly Markdown Links (Idempotent + Section-Aware)

## Goal

Convert one or more raw URLs in the selected text into **friendly Markdown links** while **preserving all surrounding formatting** (bullets, numbering, indentation, punctuation, spacing).

This skill is designed to be **idempotent**: running it repeatedly should result in **no further changes** after the first successful pass.

## Examples

- Input: `https://learn.microsoft.com/en-us/powershell/module/az.compute/grant-azdiskaccess?view=azps-15.3.0`  
  Output: `[Grant-AzDiskAccess](https://learn.microsoft.com/en-us/powershell/module/az.compute/grant-azdiskaccess?view=azps-15.3.0)`

- Input (PowerShell parameter section):  
  `https://learn.microsoft.com/en-us/powershell/module/az.compute/new-azdiskupdateconfig?view=azps-15.3.0#-architecture`  
  Output: `[New-AzDiskUpdateConfig - Architecture](https://learn.microsoft.com/en-us/powershell/module/az.compute/new-azdiskupdateconfig?view=azps-15.3.0#-architecture)`

- Input (Learn heading section):  
  `https://learn.microsoft.com/en-us/azure/reliability/reliability-vmware-solution?pivots=avs-gen1#resilience-to-availability-zone-failures`  
  Output: `[Reliability VMware Solution - Resilience to Availability Zone Failures](https://learn.microsoft.com/en-us/azure/reliability/reliability-vmware-solution?pivots=avs-gen1#resilience-to-availability-zone-failures)`

- Input (autolink):  
  `<https://learn.microsoft.com/en-us/powershell/module/az.compute/set-azdisksecurityprofile?view=azps-15.3.0#-securevmdiskencryptionset>`  
  Output: `[Set-AzDiskSecurityProfile - SecureVMDiskEncryptionSet](https://learn.microsoft.com/en-us/powershell/module/az.compute/set-azdisksecurityprofile?view=azps-15.3.0#-securevmdiskencryptionset)`

---

## When to use

- Notes, README sections, or docs where raw URLs should become readable links.
- Lists where you must not break bullet/number formatting.
- Links to headings/sections where the label should include the section name.

## Selection expectations

- Works on a **selection** that can be a single line or multiple lines.
- Converts **every raw URL** found in the selection.
- Does **not** change any text outside the URL substring(s).

---

## Hard rules (to prevent failures)

1. **Preserve formatting exactly**
   - Do not change bullets, numbering, indentation, whitespace, or line breaks.
   - Only replace the URL substring itself.

2. **Idempotency (critical)**
   - If a URL is already in a Markdown link `[text](url)`, do nothing to that link.
   - Do not “improve” existing link text. If it’s already friendly, leave it as-is.

3. **Autolinks**
   - Convert `<https://...>` to `[Friendly](https://...)` by removing `<` and `>`.

4. **Do not alter URLs**
   - Keep the URL exactly the same inside `( … )`, including query strings and fragments.

5. **Do not touch code fences**
   - Do not convert URLs inside triple-backtick blocks unless the user explicitly asked.

---

## Detection rules (stable + safe)

### What counts as a “raw URL”

- `http://...` or `https://...`
- optionally wrapped as `<https://...>`

### What must be skipped

- Any URL already inside a Markdown link structure:
  - Pattern to treat as “already converted”: `[...] ( ...URL... )` i.e., `[anything](URL)`
- Any URL inside a fenced code block (``` ... ```)

### Punctuation handling (avoid malformed links)

If a raw URL is followed immediately by trailing punctuation in prose, exclude common trailing characters from the URL match:

- `)`, `]`, `}`, `.`, `,`, `;`, `:`, `!`, `?`
Example:
- `See https://example.com/a.` → wrap only the URL, keep the period after it.

---

## Friendly label rules (Page Name + optional Section Name)

### Preferred approach (if available): use `fetch_webpage`

If inline chat supports a webpage fetch tool (often called `fetch_webpage`), use it to determine the best label.

**Page Name extraction order**

1. Use the page H1.
2. Else use `<title>` and strip common suffix noise (e.g., `| Microsoft Learn`, `- Microsoft Learn`, `| GitHub`).

**Section Name extraction (fragment links `#...`)**
If the URL includes a fragment:

1. Resolve the fragment to the heading/anchor on the page:
   - element with matching `id`, or a heading anchor referencing it.
2. Use the visible heading/section text as the section name.

**Final label format**

- No fragment: `Page Name`
- With fragment: `Page Name - Section Name`

**Important fallback rule**
If `fetch_webpage` fails, times out, or is unavailable, DO NOT fail the skill—use the inference rules below.

---

## Fallback inference (no fetch tool)

### A) Page Name inference

1. Take the last non-empty path segment (ignore trailing `/`).
2. Remove file extensions (`.html`, `.md`, etc.).
3. URL-decode.
4. Special-case Microsoft Learn PowerShell cmdlet pages:
   - If the URL contains `/powershell/module/`, format the last segment as `Verb-Noun` cmdlet casing:
     - `grant-azdiskaccess` → `Grant-AzDiskAccess`
5. Otherwise:
   - Convert hyphen/underscore slug to Title Case with spaces:
     - `reliability-vmware-solution` → `Reliability VMware Solution`

If the inferred page name is generic (`index`, `overview`, empty), fall back to a short domain label (e.g., `Microsoft Learn`).

### B) Section Name inference (fragment links `#...`)

Let `frag` = text after `#` (URL-decoded).

#### Determine fragment style (reduces wrong casing)

1. **PowerShell parameter-style fragment** if ANY is true:
   - `frag` starts with `-` (e.g., `-asjob`, `-architecture`)
   - OR the URL contains `/powershell/module/`
2. **Heading slug fragment** otherwise (e.g., `resilience-to-availability-zone-failures`)

#### Parameter-style conversion

- Strip one leading `-` if present.
- Convert to PascalCase with no spaces:
  - `securevmdiskencryptionset` → `SecureVMDiskEncryptionSet`
  - `architecture` → `Architecture`
  - `resource-group-name` → `ResourceGroupName`

#### Heading slug conversion

- Convert hyphen/underscore slug to Title Case with spaces:
  - `resilience-to-availability-zone-failures` → `Resilience to Availability Zone Failures`

#### Omit section suffix when not meaningful

If `frag` is empty or clearly non-semantic (`top`, `overview`), do not append `- Section Name`.

### C) Final label format

- If there is a meaningful section name: `Page Name - Section Name`
- Else: `Page Name`

---

## Transformation procedure (two-pass to reduce errors)

### Pass 1: Analyze only (no edits yet)

1. Scan selection and collect all raw URLs (including `<...>`).
2. Exclude any URL already within `[...](...)` and any inside fenced code blocks.
3. For each remaining URL, compute its label (prefer `fetch_webpage`, else fallback inference).
4. Build a list of *exact* replacements: `(old_substring -> new_substring)`.

### Pass 2: Apply minimal replacements

1. Apply replacements from Pass 1 in a way that:
   - Replaces only the URL substring (or `<URL>` substring for autolinks).
   - Preserves all original surrounding characters and whitespace.
2. Do not reformat or rewrap lines.

---

## Post-checks (must do before returning output)

1. **No-op check**
   - If there were zero eligible raw URLs to convert, return the selection unchanged.

2. **Idempotency check**
   - Confirm you did not modify any existing `[text](url)` links.
   - Confirm rerunning would find zero eligible raw URLs.

3. **Structural check**
   - For each converted link, ensure it matches: `[LABEL](URL)`
   - Ensure `URL` exactly equals the original matched URL (including `?` and `#`).
   - Ensure you did not swallow trailing punctuation (e.g., periods should remain outside the `)`).

---

## Notes for inline chat reliability

- Prefer operations that only replace the selected substring(s); avoid rewriting whole lines unless necessary.
- If the environment supports an edit tool (e.g., `replace_string_in_file` / minimal-diff edit), apply only the computed replacements.
- If `fetch_webpage` is supported but flaky:
  - Attempt it once per unique URL.
  - On failure, immediately fall back to inference (do not retry repeatedly).
