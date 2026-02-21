---
name: markdown-link-resolver
description: 'Resolve bare or untitled URLs in markdown files into proper markdown links with page titles. Use when asked to resolve links, add titles to URLs, fix bare links, or convert raw URLs to titled markdown links.'
user-invokable: true
argument-hint: '[file or selection]'
---

# Markdown Link Resolver

Converts bare URLs and untitled links in markdown files into properly formatted markdown links using the actual page title fetched from each URL.

## When to Use

- Converting bare/raw URLs into titled markdown links
- Replacing placeholder or generic link text with real page titles
- Cleaning up markdown files that contain untitled or poorly titled links

## Scope

Operates on any markdown file in the workspace. Can target a full file, a user-selected range, or a specific section.

## Link Detection

Identify links that need resolution. A link needs resolution if it matches any of these patterns:

| Pattern | Example |
|---------|---------|
| Bare URL on its own line | `https://learn.microsoft.com/en-us/azure/storage/blobs/` |
| Bare URL inline in text | `See https://learn.microsoft.com/en-us/azure/storage/blobs/ for details` |
| Markdown link where display text equals the URL | `[https://example.com](https://example.com)` |
| Markdown link with generic placeholder text | `[link](https://example.com)`, `[here](https://example.com)`, `[click here](https://example.com)` |

Links that already have meaningful, non-URL display text should **not** be modified.

## Process

### Step 1: Collect URLs

Scan the target markdown content and build a deduplicated list of URLs that need resolution.

### Step 2: Fetch Page Titles

Use the `fetch_webpage` tool to retrieve content from each URL. Extract the page title from the fetched content.

- Batch URLs when possible to minimize tool calls.
- If a page cannot be fetched or has no discernible title, leave the link unchanged and report it in the summary.

### Step 3: Clean Titles

Apply these cleaning rules to fetched titles:

1. Remove trailing site-name suffixes separated by ` | ` or ` - ` (e.g., `"Blob Storage overview - Azure Storage | Microsoft Learn"` → `"Blob Storage overview - Azure Storage"`)
2. Remove the final segment only — preserve internal separators that are part of the title
3. Trim leading/trailing whitespace
4. If the cleaned title is empty or generic (e.g., `"Untitled"`, `"404"`, `"Page not found"`), treat as fetch failure

### Step 4: Replace Links

Apply replacements to the markdown content:

| Original Pattern | Replacement |
|-----------------|-------------|
| `https://example.com` (bare) | `[Fetched Title](https://example.com)` |
| `[https://example.com](https://example.com)` | `[Fetched Title](https://example.com)` |
| `[here](https://example.com)` | `[Fetched Title](https://example.com)` |

Preserve surrounding context — do not alter text or formatting outside the link itself.

### Step 5: Report

After all replacements, provide a brief summary:

- **Resolved** — count and list of links updated with titles
- **Skipped** — links already titled (not modified)
- **Failed** — URLs that could not be fetched or had no usable title

## Rules

- Do **not** modify links that already have meaningful display text
- Do **not** alter any content outside of the link being resolved
- Do **not** change the URL itself — only the display text
- Do **not** invent or guess titles — only use titles fetched from the actual page
- Preserve the original markdown structure (bullet lists, tables, paragraphs)
- If a URL appears multiple times, resolve all occurrences consistently with the same title
