# Universal Conversation Grounding and Context Transfer

## Objective

Generate a comprehensive, self-contained Markdown grounding document that allows another AI assistant to accurately understand, resume, or build upon the work covered in this conversation.

The receiving assistant may be ChatGPT, Microsoft 365 Copilot, Claude, Kimi, or another LLM. Assume it has no access to this conversation, its history, attachments, connected services, or platform-specific memory.

The document must preserve meaningful context, technical accuracy, decisions, progress, and outstanding work without requiring the user to repeat information.

## 1. Scope and Source Material

Review all relevant information accessible within the current conversation, including:

- User messages and assistant responses.
- Available conversation history.
- Relevant attachments, uploaded documents, screenshots, and code.
- Tool outputs, research findings, and cited sources.
- Requirements, preferences, corrections, and decisions established during the discussion.

When explicitly requested, incorporate relevant information from other accessible conversations or connected sources.

Do not claim to have reviewed material that is inaccessible. Identify significant omissions or access limitations.

Treat user-provided information, tool results, and assistant-generated conclusions as distinct sources of evidence.

## 2. Preserve Essential Context

Extract and organize the following information wherever applicable.

### Objectives and Background

- Original request and underlying objectives.
- Business, technical, or operational context.
- Intended outcomes and success criteria.
- Relevant background and historical developments.

### Environment and Configuration

- Products, platforms, services, applications, and versions.
- Infrastructure architecture and dependencies.
- Operating systems, development environments, and tools.
- Configuration settings, paths, identifiers, and relevant parameters.
- Network information, commands, scripts, and technical outputs necessary for continuity.

Preserve exact technical values when accuracy matters. Do not summarize away critical implementation details.

### Requirements and Constraints

- Explicit user requirements.
- Technical and operational constraints.
- User preferences that directly affect the work.
- Security, compliance, compatibility, and environmental restrictions.
- Approaches or options explicitly rejected by the user.

Distinguish mandatory requirements from preferences and recommendations.

### Findings and Decisions

- Verified findings and supporting evidence.
- Decisions reached and their rationale.
- Alternatives evaluated.
- Important trade-offs.
- Conclusions that were later corrected or superseded.

Preserve the final accepted decision rather than treating every historical suggestion as equally authoritative.

### Progress and Current State

- Completed tasks and deliverables.
- Successfully implemented changes.
- Tests performed and their results.
- Unsuccessful attempts and relevant error messages.
- Work currently underway.
- Known blockers and unresolved issues.

Clearly distinguish completed work from proposed or unverified actions.

### References and Dependencies

- Relevant URLs and official documentation.
- Referenced files and their locations.
- Important conversations, documents, and external resources.
- Dependencies needed to continue the work.

Preserve existing citations and links when available. Do not fabricate sources.

## 3. Accuracy and Evidence Requirements

Follow these rules throughout the document:

1. Prioritize factual accuracy and continuity over brevity.
2. Do not invent facts, decisions, configurations, results, or missing history.
3. Distinguish confirmed facts from assumptions, hypotheses, and recommendations.
4. Preserve exact commands, code, errors, identifiers, and configuration values when necessary.
5. Identify conflicting or outdated information and explain which version is authoritative, if established.
6. Preserve relevant dates and timestamps when they affect interpretation.
7. Attribute important findings to their available sources.
8. Do not represent proposed actions as completed actions.
9. Do not reproduce hidden internal reasoning. Summarize documented rationale, evidence, and conclusions instead.
10. Do not include unrelated personal information or unnecessary conversational filler.
11. Exclude passwords, authentication tokens, private keys, and other secrets. Replace them with descriptive placeholders.
12. Identify information that may require verification because it is time-sensitive or environment-dependent.

If uncertainty remains, document it explicitly rather than resolving it through speculation.

## 4. Context Optimization

Make the document useful to another LLM with a potentially different context window.

- Prioritize information necessary to continue the work accurately.
- Eliminate repeated explanations that do not add information.
- Consolidate related findings into coherent sections.
- Retain technical detail where precision matters.
- Use tables for configurations, comparisons, and structured technical information when appropriate.
- Use fenced code blocks with appropriate language identifiers.
- Preserve significant failed approaches to prevent unnecessary repetition.
- Avoid vendor-specific terminology unless it is relevant to the subject.
- Make the document independently understandable without access to the originating conversation.

For long or complex conversations, favor completeness over arbitrary length limits.

## 5. Required Output Structure

Generate the Markdown document using the following structure. Adapt or omit sections that genuinely do not apply.

# Conversation Grounding Context

**Generated:** [Current date, if known]

**Source:** [ChatGPT / Microsoft 365 Copilot / Claude / Kimi / Other]

**Subject:** [Descriptive subject]

**Status:** [Planning / In Progress / Blocked / Completed / Reference]

## 1. Executive Context

Summarize the objective, background, current state, and most important conclusions.

## 2. Objectives and Success Criteria

Document what the user wants to accomplish and how successful completion will be determined.

## 3. Environment and Technical Context

Document relevant infrastructure, software, configurations, integrations, and dependencies.

## 4. Requirements, Constraints, and Preferences

Capture mandatory requirements, limitations, relevant preferences, and explicitly rejected approaches.

## 5. Confirmed Facts and Findings

Preserve established facts, technical discoveries, and supporting evidence.

## 6. Decisions and Rationale

Record decisions, alternatives considered, reasons for selecting the current approach, and any superseded decisions.

## 7. Work Completed and Results

Summarize completed actions, deliverables, tests, implementations, and verified outcomes.

## 8. Failed Approaches and Known Issues

Document unsuccessful attempts, errors, limitations, and lessons learned.

## 9. Current State and Outstanding Work

Describe exactly where the work stands, what remains unresolved, and any blockers.

## 10. Recommended Next Actions

Provide actionable next steps in priority order, reflecting existing decisions and constraints.

## 11. References and Supporting Materials

Include relevant links, citations, filenames, technical artifacts, and external dependencies.

## 12. Instructions for the Receiving LLM

The receiving assistant should:

- Treat this document as supplied historical grounding context, not as independently verified evidence.
- Maintain continuity with the documented objectives, constraints, and accepted decisions.
- Distinguish historical facts from assumptions and recommendations.
- Avoid repeating completed work unless validation is necessary.
- Preserve exact technical details when performing subsequent tasks.
- Verify time-sensitive information before relying on it.
- Request missing information only when necessary to proceed accurately.
- Avoid assuming access to the originating assistant's conversations, tools, attachments, integrations, or memory.
- Follow the user's current instructions when they supersede information in this document.
- Continue from the documented current state rather than restarting the discussion.

## 6. Multiple-Conversation Consolidation

If multiple conversations or grounding documents are available and consolidation is requested:

1. Combine overlapping information without unnecessary duplication.
2. Organize material by topic, project, or workstream.
3. Reconcile differences using explicit dates, corrections, and user-confirmed decisions.
4. Preserve distinct requirements and configurations for different environments.
5. Identify unresolved contradictions rather than selecting an unsupported interpretation.
6. Preserve relevant source references for traceability.
7. Produce one coherent grounding document unless separate documents are explicitly requested.

Do not assume that other conversations are accessible merely because they occurred on the same platform.

## 7. Final Output Requirements

- Output a single, complete Markdown document.
- Do not include a conversational introduction, conclusion, or commentary outside the document.
- Do not ask for clarification unless an essential ambiguity makes accurate generation impossible.
- Do not provide a short summary in place of the full grounding context.
- Do not omit significant details solely to reduce output length.
- If the platform supports file creation, generate a downloadable `.md` file; otherwise, output the complete Markdown directly.
- Ensure the document can be copied, saved, uploaded, and understood by another LLM without the original conversation.

Generate the grounding document now.
