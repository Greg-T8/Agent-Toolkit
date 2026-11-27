# Matt Pocock Skills bundle changelog

## 0.3.1 - 2026-11-27

- Renamed `grill-interview-adapter` to `matt-pocock-adapter` to accommodate additional upstream workflows.

## 0.3.0 - 2026-11-27

- Added upstream `to-spec` at commit `6f7f7831a625f040a8e06a0e7954826b87ce775a` to synthesize conversations into specifications.
- Extended the adapter to route `to-spec`, preserve its test-seam confirmation, and handle tracker and label configuration when the upstream setup skill is unavailable.

## 0.2.0 - 2026-11-27

- Added `grill-interview-adapter` and routed interview requests through it, preserving the upstream skills unchanged.
- Added whole-round questionnaire and Markdown fallback guidance, direct dependency loading, and support for designated native project documents.

## 0.1.0 - 2026-11-27

- Added `grill-me` and `grill-with-docs`, with their `grilling` and `domain-modeling` dependencies, from Matt Pocock's upstream repository at commit `6f7f7831a625f040a8e06a0e7954826b87ce775a`.
- This is Greg's independent packaging of upstream skills. The composed plugin and its cross-skill invocation require testing in ChatGPT.
