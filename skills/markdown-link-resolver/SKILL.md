---
name: markdown-link-resolver
description: 'Resolve bare or untitled URLs in markdown files into proper markdown links with page titles. Use when asked to resolve links, add titles to URLs, fix bare links, or convert raw URLs to titled markdown links.'
user-invokable: true
argument-hint: '[file or selection]'
---

# SKILL: Convert Raw URLs to Friendly Markdown Links (Idempotent + Section-Aware)

## Goal

Process the selected text to produce clean, consistently formatted Markdown links:

1. **Convert raw URLs** into `[Friendly Label](URL)` links.
2. **Promote standalone links** — any line whose sole content is a Markdown link (whether newly converted or pre-existing) must be a bullet item (`- [Label](URL)`).
3. **Collapse spacing** between consecutive standalone bullet links so they form a tight, unspaced list.

This skill is designed to be **idempotent**: running it repeatedly should result in **no further changes** after the first successful pass.

## Examples

- Input: `https://learn.microsoft.com/en-us/powershell/module/az.compute/grant-azdiskaccess?view=azps-15.3.0`  
  Output: `- [Grant-AzDiskAccess](https://learn.microsoft.com/en-us/powershell/module/az.compute/grant-azdiskaccess?view=azps-15.3.0)`

- Input (PowerShell parameter section):  
  `https://learn.microsoft.com/en-us/powershell/module/az.compute/new-azdiskupdateconfig?view=azps-15.3.0#-architecture`  
  Output: `- [New-AzDiskUpdateConfig - Architecture](https://learn.microsoft.com/en-us/powershell/module/az.compute/new-azdiskupdateconfig?view=azps-15.3.0#-architecture)`

- Input (Learn heading section):  
  `https://learn.microsoft.com/en-us/azure/reliability/reliability-vmware-solution?pivots=avs-gen1#resilience-to-availability-zone-failures`  
  Output: `- [Reliability VMware Solution - Resilience to Availability Zone Failures](https://learn.microsoft.com/en-us/azure/reliability/reliability-vmware-solution?pivots=avs-gen1#resilience-to-availability-zone-failures)`

- Input (autolink):  
  `<https://learn.microsoft.com/en-us/powershell/module/az.compute/set-azdisksecurityprofile?view=azps-15.3.0#-securevmdiskencryptionset>`  
  Output: `- [Set-AzDiskSecurityProfile - SecureVMDiskEncryptionSet](https://learn.microsoft.com/en-us/powershell/module/az.compute/set-azdisksecurityprofile?view=azps-15.3.0#-securevmdiskencryptionset)`

- Input (pre-existing formatted links, missing bullets and separated by blank lines):  

  ```
  [Blob Storage Monitoring Scenarios](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-storage-monitoring-scenarios)

  [Storage Insights Overview](https://learn.microsoft.com/en-us/azure/storage/common/storage-insights-overview)
  ```  

  Output:  

  ```
  - [Blob Storage Monitoring Scenarios](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-storage-monitoring-scenarios)
  - [Storage Insights Overview](https://learn.microsoft.com/en-us/azure/storage/common/storage-insights-overview)
  ```

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
   - **Exception — standalone URL lines:** If a line contains *only* a raw URL (optionally wrapped in `<...>`) with no surrounding text, you **must** prepend `-` to make it a bullet item. This overrides the preserve-whitespace rule for that line.

2. **Idempotency (critical)**
   - If a URL is already inside a Markdown link `[text](url)`, do **not** re-fetch or re-derive its label, and do **not** alter the URL.
   - Do not "improve" existing link text. If it's already friendly, leave it as-is.
   - **Important:** idempotency applies only to label text and URLs. Formatting corrections (bullet promotion and blank-line collapsing) **must still be applied** to pre-existing `[text](url)` lines that are missing a bullet or separated by blank lines.

3. **Autolinks**
   - Convert `<https://...>` to `- [Friendly](https://...)` by removing `<` and `>`.

4. **Do not alter URLs**
   - Keep the URL exactly the same inside `( … )`, including query strings and fragments.
   - Exception: Remove ChatGPT tracking query parameters (e.g., `?utm_source=chatgpt.com`).
     - Example: `https://learn.microsoft.com/en-us/azure/load-balancer/skus?utm_source=chatgpt.com` → stored as `https://learn.microsoft.com/en-us/azure/load-balancer/skus`

5. **Do not touch code fences**
   - Do not convert URLs inside triple-backtick blocks unless the user explicitly asked.

6. **Collapse blank lines between consecutive standalone-link bullet items**
   - After converting a block of consecutive standalone URL lines into `- [Label](URL)` bullets, remove any blank lines that existed between those items so they form a tight, unspaced list.
   - Only collapse blank lines that are *between* two consecutive converted bullet lines; blank lines before the first or after the last item are left unchanged.

---

## Detection rules (stable + safe)

### What counts as a “raw URL”

- `http://...` or `https://...`
- optionally wrapped as `<https://...>`

### What must be skipped (conversion only)

The following are skipped for **URL-to-label conversion only**. They are still subject to the standalone formatting pass (bullet promotion and blank-line collapsing).

- Any URL already inside a Markdown link structure:
  - Pattern to treat as "already converted" for label purposes: `[anything](URL)`
- Any URL inside a fenced code block (``` ... ```) — skip entirely, including formatting.

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

## Transformation procedure (three-pass to reduce errors)

### Pass 1: Analyze only (no edits yet)

1. Scan selection and collect all raw URLs (including `<...>`).
2. Exclude any URL already within `[...](...)` and any inside fenced code blocks.
3. For each remaining URL, compute its label (prefer `fetch_webpage`, else fallback inference).
4. Build a list of *exact* replacements: `(old_substring -> new_substring)`.

### Pass 2: Apply URL conversions

1. Apply replacements from Pass 1:
   - Replace only the URL substring (or `<URL>` substring for autolinks).
   - For a standalone raw-URL line, replace the entire line with `- [Label](URL)`.
   - Preserve all surrounding characters and whitespace for inline URLs.
2. Do not reformat or rewrap any other lines.

### Pass 3: Standalone link formatting (applies to ALL lines, including pre-existing)

This pass runs **after** Pass 2 and is independent of whether any URL conversions occurred.

1. **Bullet promotion** — For every line in the selection whose sole non-whitespace content is a Markdown link (`[anything](URL)`) and that does **not** already begin with a list marker (`-`, `*`, `+`, or a number), prepend `-` to the line.
2. **Blank-line collapsing** — After bullet promotion, scan for runs of consecutive `- [...]( ...)` bullet lines that are separated only by blank lines. Remove those blank lines so the run forms a tight list. Do not collapse blank lines before the first item in a run or after the last item.

---

## Post-checks (must do before returning output)

1. **No-op check**
   - Do **not** return the selection unchanged just because there were zero raw URLs to convert. Pass 3 (standalone formatting) must still run.
   - Return the selection unchanged only if both Pass 2 and Pass 3 produced zero changes.

2. **Idempotency check**
   - Confirm you did not alter the label text or URL of any existing `[text](url)` link.
   - Confirm rerunning would find zero raw URLs to convert and zero lines needing bullet promotion or blank-line collapsing.

3. **Structural check**
   - For each converted link, ensure `URL` exactly equals the original matched URL (including `?` and `#`).
   - Ensure you did not swallow trailing punctuation (e.g., periods should remain outside the `)`).
   - Ensure **every** line whose sole content is a Markdown link now begins with `-` (including pre-existing links).
   - Ensure no blank lines remain between consecutive `- [...]( ...)` bullet items.

---

## Notes for inline chat reliability

- Prefer operations that only replace the selected substring(s); avoid rewriting whole lines unless necessary.
- If the environment supports an edit tool (e.g., `replace_string_in_file` / minimal-diff edit), apply only the computed replacements.
- If `fetch_webpage` is supported but flaky:
  - Attempt it once per unique URL.
  - On failure, immediately fall back to inference (do not retry repeatedly).
