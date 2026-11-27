---
applyTo: "**/*.sh"
description: "This file contains the shell scripting standards and guidelines for Copilot."
---

# Shell Standards for Copilot (Linux/POSIX)

## 1) Modes

### Mode A — Interactive CLI commands

* Provide concise shell commands intended to be copied and pasted directly into an interactive CLI.
* Use the shortest clear solution that accomplishes the requested task; retain necessary safeguards and error handling.
* Script-file structure, headers, and function requirements do not apply to interactive commands.

### Mode B — Create a new script

* You MAY add code, functions, output, and error handling.
* You MUST follow the Required Script Structure.

### Mode C — Edit an existing script

* Make the changes requested by the user and preserve unrelated behavior and existing conventions.
* Functional changes are allowed when requested. Apply the script standards to new and modified code without unnecessary restructuring.
* For explicitly comment-only, format-only, or other non-functional requests, preserve behavior. Do not add or remove commands, parameters, logic branches, output, or side effects.

> Default to Mode A unless the user asks to create a script (Mode B), edit an existing script (Mode C), or explicitly selects another mode.

---

## 2) Required Script Structure (Mode B)

New scripts in Mode B MUST follow this order:

1. Shebang, followed by a comment header
2. Strict-mode and shell options, selected for the script's intended shell and error-handling needs
3. Script-level configuration and constants
4. `main()` function containing high-level orchestration
5. Helper function definitions
6. Entry point that calls `main "$@"`

### 2.1 Header template (required)

```bash
#!/usr/bin/env bash

# ---------------------------------------------------------------------------
# Description   : Brief description of what the script does
# Context       : Context information (e.g., project, course, or book)
# Author        : Greg Tate & coding agent
# Last Modified : YYYY-MM-DD
# Revision History:
#   YYYY-MM-DD - Initial version
# ---------------------------------------------------------------------------
```

* Keep the description concise; wrap continuation lines so their text begins under the description or context value.
* Use ISO 8601 dates (`YYYY-MM-DD`). Preserve existing dates and revision-history entries when editing; put the newest entry first.

### 2.2 Main function

* Define `main()` before helper functions and call it at the end of the script.
* Keep `main()` limited to high-level orchestration so it reads like an outline of the script.
* Pass script arguments through with `main "$@"` when the script accepts arguments or may need them later.

### 2.3 Helper functions

* Put implementation details in helper functions defined after `main()`.
* Keep functions small and single-purpose, with lowercase names and underscores between words.
* Use descriptive verb-led names, such as `get_data`, `process_data`, or `validate_input`.
* Use `local` for function-scoped variables.

### 2.4 Entry point

Call `main` at the bottom of the script, passing `"$@"` to preserve argument boundaries.

---

## 3) Formatting and Readability (Modes B and C)

### 3.1 Indentation and line breaks

* Use four spaces for indentation; do not use tabs.
* Break long one-line commands across multiple lines when it improves readability.
* Prefer one pipeline segment per line, placing the pipe at the end of the preceding line.
* Use `\` for line continuation when a command does not naturally break at a pipe.
* Indent continuation lines to show their grouping and hierarchy.
* Keep related options together; group short flags when appropriate and separate long options for clarity.
* Keep logical operators visible at the ends of lines. For example:

```bash
command1 && \
    command2 || \
    handle_error
```

#### Pipeline

```bash
ps aux |
    grep -v grep |
    grep python |
    awk '{print $2, $11}' |
    sort -k2
```

#### Command with many arguments

```bash
docker run -d \
    --name myapp \
    -p 8080:8080 \
    -e NODE_ENV=production \
    -e DB_HOST=localhost \
    -e DB_PORT=5432 \
    -v /data:/app/data \
    --restart unless-stopped \
    myapp:latest
```

#### Here-document

```bash
cat > config.yaml << 'EOF'
server:
  host: localhost
  port: 8080
database:
  host: db.example.com
  port: 5432
EOF
```

### 3.2 Quoting and command substitution

* Quote variable expansions as `"$variable"` unless intentional word splitting or glob expansion is required.
* Use `$(...)` instead of backticks for command substitution.
* Quote here-document delimiters when expansion is not wanted, such as `<< 'EOF'`.
* Use here-documents for multi-line strings instead of multiple `echo` commands.

### 3.3 Shell behavior and portability

* Match syntax to the interpreter named by the shebang. Use `[[ ]]` only for Bash scripts; use POSIX `[ ]` for scripts that must run under a POSIX shell.
* Consider `set -euo pipefail` for Bash scripts, but account for its behavior and exceptions rather than applying it mechanically.
* Check command success where subsequent work depends on it, and handle failures intentionally.
* Use `readonly` for script constants and configuration values that should not change.

### 3.4 Blank lines and comments

* Use blank lines to separate logical groups and function definitions.
* Add comments that explain intent when required by the general coding guidelines; avoid comments that merely restate the command.
* Apply formatting and commenting rules to new and modified code. For formatting-only requests, preserve program behavior.

---

## 4) Other Requirements (Modes B and C)

* Provide usage or help text for scripts that accept arguments.
* Use meaningful variable names; avoid single-letter names except for simple loop counters.
* Check command success before proceeding when failure would make later steps unsafe or misleading.
* Use `:` as a placeholder only when an intentionally empty function body is needed.

### Common Verb Mapping

* Check or validate → `check_` or `validate_`
* Display or print → `show_` or `print_`
* Create or make → `create_` or `make_`
* Delete or remove → `remove_` or `delete_`
* Update or modify → `update_` or `modify_`

---

## 5) Example Skeleton (Mode B)

```bash
#!/usr/bin/env bash

# ---------------------------------------------------------------------------
# Description   : Retrieve, process, and save data
# Context       : Example project script
# Author        : Greg Tate & coding agent
# Last Modified : YYYY-MM-DD
# Revision History:
#   YYYY-MM-DD - Initial version
# ---------------------------------------------------------------------------

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

main() {
    get_data
    process_data
    save_results
}

get_data() {
    :
}

process_data() {
    :
}

save_results() {
    :
}

main "$@"
```
