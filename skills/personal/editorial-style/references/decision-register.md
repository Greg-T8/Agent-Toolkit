# Decision register

Version 1.0.0, November 25, 2026. Each row is a resolved decision with the
authority behind it, so a draft applies the rule without rereading the guides.
Open an authority file only for a case this register does not cover, and
report that case as a gap so the register can grow.

Rows come from the Deliverable Accelerator's editorial conventions (its
document design spec, section 15), with the Quisitive-specific adaptations
removed and Greg's house rules added.

## 1. House rules

Greg's own rules. They rank above every authority in this register.

| Topic | Rule |
| --- | --- |
| **Spelling** | US English. |
| **Dashes** | No em dashes anywhere, and no spaced hyphen or en dash used as a dash. Use a colon, parentheses, a comma, or a new sentence. A closed en dash in a range ("10–15 minutes") is not a dash and stays. |
| **Document titles** | The document's title (a Google Doc or Word title, a deck title) uses title case: capitalize every word except articles, coordinating conjunctions, and prepositions of three letters or fewer, unless the word is first or last. Keep product and identifier casing. The subtitle and every heading use sentence case, and so does a Markdown file's H1. |
| **Real values** | In implementation guides and procedures, write the real environment values (names, IDs, regions, addresses) into the steps. Use a placeholder only for a value that is genuinely not yet known, and say where it will come from. |
| **Tone** | Concise, practical, and professional. Clarity over polish. Warm where it fits, never overly enthusiastic. Short paragraphs and plain language. |
| **Messages** | Emails and messages get to the point, keep the sender's intent, and cut filler. See [messages](messages.md). |

## 2. Enforced by `editorial_check.py`

These fail a check. Each is narrow by design, because a check that fires on
correct writing teaches people to ignore it.

| Rule | What the check looks for | Authority |
| --- | --- | --- |
| **Sentence-case headings.** Capitalize the first word, the first word after a colon, and proper nouns only. | A heading whose later words include capitalized common words ("Scope And Approach") | Microsoft |
| **Title-case document titles.** | A title word, other than a minor word in the middle, that starts lowercase | House |
| **Serial comma.** In a list of three or more, put a comma before the conjunction. | "A, B and C" or "A, B or C" in body text and table cells | Microsoft |
| **Identifiers in code formatting.** See section 7. | A resource-style name (`rg-app-prod`, `law-ops-01`) outside code formatting | Microsoft; Google |
| **No Latin abbreviations or loaded terms.** "for example", not "e.g."; "that is", not "i.e."; "and so on" or a complete list, not "etc."; "use", not "utilize"; "allow list" and "block list" (two words), not "whitelist" and "blacklist"; "primary" and "secondary", not "master" and "slave"; "check", not "sanity check". | The term, outside code | Microsoft word list; Microsoft and Google bias-free guidance |
| **House word list.** "on-premises", not "on-premise"; "email", not "e-mail"; "or" (or "A, B, or both"), not "and/or". | The term, outside code | Microsoft word list |
| **No filler phrases.** "to", not "in order to"; "because", not "due to the fact that"; "if", not "in the event that"; "now", not "at this point in time"; "about", not "with regard to"; "use", not "make use of". Cut "it should be noted that", "it is important to note", and "please note". | The whole phrase, outside code | Microsoft; plain language |
| **Descriptive headings.** No heading that is only "Other", "Details", "Gaps", "General", "Miscellaneous", or "Additional information". | A heading whose whole text is one of those | Google; W3C; plain language |
| **No dashes.** | An em dash, or a spaced hyphen or en dash, outside code | House |
| **Descriptive link text.** | Link text that is only "here", "click here", "this link", "read more", or "learn more" | Google; Microsoft; W3C |

The checker's advisory review also lists "simply", "just", "easy", "please",
"log in to", "via", and first-person plural for a second look. Each has
correct uses, so none fails a check.

## 3. Mechanics

| Topic | Rule | Authority |
| --- | --- | --- |
| **Capitalization** | Sentence case for headings, table headers, list items, captions, and labels. Start each list item with a capital letter. Don't capitalize a common noun for emphasis or because it is important ("the Workspace"). Copy UI labels and product names exactly. | Microsoft |
| **List punctuation** | End a list item with a period only if it is a complete sentence. Keep the items in one list consistent. | Microsoft |
| **Colons** | Use a colon to introduce a list or a short explanatory phrase. A colon never joins two statements: give each its own sentence. In running text, lowercase the word after a colon unless it starts a complete sentence or is a proper noun. | Microsoft; Chicago |
| **Semicolons** | Avoid them in body text. Two sentences are clearer. | Microsoft |
| **Parentheses** | Use sparingly. If the content matters to the main point, give it its own sentence. A sentence that needs several commas, semicolons, or parentheses to stay readable is decomposed before it is punctuated. Repunctuating is not decomposing. | Chicago; decomposition |
| **Quotation marks** | Put periods and commas inside closing quotation marks, except when the quoted text is a literal string the reader types or matches. Better: put literal strings in code formatting and drop the quotation marks. | Microsoft |
| **Exclamation points and ampersands** | No exclamation points in documentation. Use "and", not "&", except in a name or UI label. | Microsoft |
| **Hyphens** | Hyphenate a compound modifier before a noun ("read-only access"), not after it ("access is read only"). Don't hyphenate after an "-ly" adverb. Follow Merriam-Webster for prefixes and closed compounds. | Microsoft; Chicago; Merriam-Webster |
| **Numbers** | In body text, spell out zero through nine and use numerals for 10 or greater. Use numerals in tables and for measurements, percentages, versions, times, money, and anything the reader compares ("42 of 118 servers"). Spell out a number that starts a sentence, or rewrite the sentence. Use commas in numbers of four or more digits, except years, versions, ports, and other identifiers. Present comparable quantities the same way throughout. | Microsoft; Chicago |
| **Units and percentages** | A space between a number and its unit ("500 GB", "15 minutes"). No space before the percent sign ("25%"). | Microsoft |
| **Dates** | Month day, year: "November 25, 2026". No ordinals ("November 25", not "November 25th") and no numeric months in prose, because "11/12" reads differently around the world. Numeric dates are acceptable in table cells where space is tight. | Microsoft; Google |
| **Times** | "10:00 AM", with a space and capital letters. Add the time zone when the reader may be elsewhere ("10:00 AM CT"). Use "noon" and "midnight", not 12:00 PM and 12:00 AM. | Microsoft |
| **Ranges** | In a table cell, a list entry, or a source line, use a closed en dash: "10–15 minutes", "August 23–September 21, 2026". In running prose, use words: "from August 23 through September 21, 2026". Never combine "from" or "between" with an en dash. | Chicago |
| **Contractions** | Use common contractions (it's, don't, isn't, can't, you'll) by default. Avoid noun-plus-verb contractions ("Azure's supported") and ambiguous ones ("it'd"). Write the full form in a formal statement of finding, scope, or limitation, in contractual language, and wherever a contraction could be misread. | Microsoft |
| **Acronyms** | Spell out on first use in each document, with the acronym in parentheses, then use the acronym. Don't spell out ones the audience knows better as acronyms (VM, DNS, IP, URL). Don't introduce an acronym for a term used only once or twice. No periods in acronyms, and no apostrophe in plurals ("VMs"). Keep a glossary when a document has more than about 10. | Microsoft; plain language; Chicago |
| **Quotations** | Quote only when the exact wording matters, and name the source. A quotation supports analysis; it never replaces it. | Chicago |
| **Consistency** | When two forms are acceptable, choose one and keep it through the document: dates, ranges, list punctuation, terms, and source lines. | Chicago |

## 4. Terms and voice

| Topic | Rule | Authority |
| --- | --- | --- |
| **Product names** | Use the current official name and capitalization, as the product's own documentation writes it ("Microsoft Entra ID", "Azure Monitor Agent", "Google Sheets"). Don't use a retired name except to say it was retired. | Microsoft |
| **Microsoft word list** | Sign in and sign out (verbs), sign-in (noun or modifier); set up (verb), setup (noun); email; internet; website; web page; on-premises; Wi-Fi; select, not click; clear, not uncheck or deselect; unavailable, not grayed out; run a program or command, not execute; dialog box, not dialog; pane, not blade. | Microsoft |
| **Permissions and privileges** | A permission is an operation authorized on a resource. A privilege is an elevated permission that allows administrative or sensitive actions. Neither is a synonym for access, a role, an identity, or a service principal. | Microsoft |
| **One term per concept** | Use one term for a concept throughout a document. Don't vary a term to avoid repetition when both words mean the same technical thing ("VM" in one paragraph and "server" in the next). | Google; IBM |
| **Simplify language, not meaning** | Prefer the familiar word when precision is equal ("use", "help", "begin", "about"). Keep a technical or project term when it is more precise: "conditional forwarder", not "DNS setting". | Plain language |
| **Preserve qualifiers** | Keep the words that carry scope, uncertainty, timing, or dependency: "based on the captured configuration", "as of November 25, 2026", "not verified". Simplifying never makes a statement more certain than its evidence. | Plain language |
| **Person** | Instructions address the reader as "you", in the imperative. Narrative names the actor (the team, the service, the script). Use "we" only when the author's own team is the actor, and "I" only in messages Greg sends as himself. Don't mix "you" and third person in one section. | Microsoft; Google |
| **Active voice** | Use active voice where responsibility matters: recommendations, ownership, approvals, remediation, and steps. Passive voice is fine when the actor is unknown or irrelevant. | Google; plain language |
| **Present tense** | Describe what a system does in the present tense ("The function writes to `NewsItems`"), not the future ("will write"). Use the past tense for what was done. | Microsoft; Google |
| **Conditions first** | Put a condition before the action it governs: "If the workspace uses private endpoints, verify DNS resolution before you test connectivity." | Google |
| **Positive statements** | Prefer a positive instruction ("Include the subscription") to a negative one ("Don't omit the subscription"), unless the prohibited action is the point. | Plain language |
| **Global readers** | Literal language. No idioms, culture-specific metaphors, sports references, or humor. Don't use "simply", "just", "easy", or "obviously" where they play down real complexity. | Microsoft; Google |
| **Bias-free language** | Gender-neutral and people-first. No "he or she": rewrite with "you" or singular "they". Avoid terms that use disability or violence as metaphor. | Microsoft; Google |
| **No hedging stacks** | "It may potentially be advisable to consider" says nothing. If confidence is low, say why. | Plain language |

## 5. Structure

| Topic | Rule | Authority |
| --- | --- | --- |
| **Lead with the point** | A document, section, and paragraph each open with their point. An executive summary's first sentence carries the verdict, and none of its paragraphs runs past five sentences. | Plain language; decomposition |
| **Headings say what follows** | A heading names the information under it, so the outline alone explains the document. In a task section, start with a verb: "Configure the DNS forwarding ruleset", not "DNS configuration". Don't skip heading levels. | Google; W3C; plain language |
| **Explicit scope** | State what is included, what is excluded, and, when it matters, why, each in its own sentence: "The review includes ...", "The review excludes ...". Never carry exclusions in the tail of a scope sentence. | Plain language |
| **Fact, interpretation, recommendation** | Keep them in separate sentences when a reader might accept one without the others. A finding states what is; a recommendation states an action, an owner, and a reason. | Plain language |
| **Lists** | Use a list for three or more parallel items or for steps. Introduce it with a sentence ending in a colon unless the relationship is obvious. Every item has the same grammatical form and level of detail. Don't make a list of one or two items. Bullets can't carry "therefore" or "however": an argument stays in prose. | Google; Chicago; Microsoft |
| **Inline series** | A sentence names at most three identifiers in a series. Four or more become a list, or a table when the items carry attributes the reader compares. | Microsoft; Google |
| **Tables** | Use a table when readers compare attributes across items. Three to five columns, six at most. Cells hold fragments; a cell that needs a subordinate clause is prose. Every column earns its place, and values in a column are parallel. Introduce a table before it appears. | Google; Chicago |
| **Notes and callouts** | Reserve a callout for something the reader must not miss: a risk, a decision, a warning, or a key observation. A callout on every page trains readers to skip them. | Microsoft |
| **Links** | Link text is the destination's title or a description that makes sense read on its own. No bare URLs in body text. | Google; Microsoft; W3C |
| **Semantic references** | Refer to a table, figure, or section by name, not by position: "the action groups table", not "the table above". | Google |
| **Source lists** | A document that lists sources closes with a Sources block, one bullet per source, never a sentence of links. Write each entry as source, object, date, then qualification, and keep the pattern: "Azure CLI capture of `rg-ops-prod`, November 20, 2026: 27 resources, read-only queries". Link vendor articles by their official titles. | Chicago; plain language |
| **Emphasis** | Bold only run-in labels and the UI labels a reader acts on. Don't bold, italicize, capitalize, or underline text for emphasis. | Microsoft |
| **Grounding** | Every claim traces to a source. Where the source is silent, the document is silent or says the point is unverified. When sources conflict, say so. | Plain language |

## 6. Instructions and UI text

| Topic | Rule | Authority |
| --- | --- | --- |
| **Steps** | A numbered list for any sequence. One action per step; combine short actions in the same place ("Enter the name, and then select **Create**"). Put the result in its own sentence after the action. | Microsoft |
| **Location before action** | Say where before what: "In the Azure portal, go to **Key vaults**." | Microsoft |
| **Input-neutral verbs** | Select (not click, tap, or hit), enter (not type, for values), open, clear (not uncheck), choose. For a context menu, "select and hold (or right-click)". | Microsoft |
| **UI labels** | Bold the label exactly as it appears, without its trailing colon or ellipsis. Don't add the control type when the label is clear ("select **Save**", not "select the **Save** button"), unless it prevents confusion. | Microsoft |
| **Menu sequences** | Use ">" with a space on each side, bolding the labels but not the bracket: "Select **File** > **Save as**". | Microsoft |
| **Prepositions** | In a pane, dialog box, or window; on a page, tab, or menu. | Microsoft |
| **Politeness** | No "please" in instructions, and no "simply" or "just". | Microsoft |
| **Commands** | A command the reader runs goes in a code block, with a comment line saying what it does. Never put a runnable command inline in a sentence. | Microsoft; Google |
| **Placeholders** | Real values first (house rules). A genuine placeholder is lowercase and hyphenated inside angle brackets in code formatting (`<resource-group-name>`), and the text says where its value comes from. | Microsoft; house |

## 7. Code formatting

Anything the reader types, searches for, or matches verbatim takes code
formatting (backticks in Markdown, the monospace style in a document):

| Element | Example |
| --- | --- |
| Resource names and IDs | `rg-app-prod`, `/subscriptions/<subscription-id>/resourceGroups/rg-app-prod` |
| Table, field, and query names | `NewsItems`, `story_id`, `SecurityEvent` |
| Property names and literal values | `retentionInDays`, `Standard_LRS`, `true` |
| File names, paths, and extensions | `audit_doc.py`, `C:\Users\gregt\LocalCode`, `.md` |
| Commands, cmdlets, and parameters inside a sentence | `Get-AzVM`, `-ResourceGroupName`, `az group list` |
| Environment variables, keys, and tags | `AZURE_SUBSCRIPTION_ID`, `env: prod` |

Not code: product and feature names (Azure Monitor, action group), UI labels
(bold in instructions, plain in narrative), and a plain-language description
("the critical action group"). Headings carry no inline formatting, so an
identifier in a heading appears as plain text.

## 8. Authorities by jurisdiction

Use the most specific authority. When two conflict, the higher one in the row
wins.

| Decision | Authorities, in order |
| --- | --- |
| Terminology, product and feature names, UI labels | This register, then Microsoft |
| Grammar, punctuation, and mechanics | This register, Microsoft, Chicago, then Merriam-Webster for spelling and compounds |
| Technical information structure: sentences, paragraphs, lists, headings, commands, links | This register, Microsoft, Google, then IBM Style |
| Clarity and reader effort | This register, Microsoft, plain-language guidance |
| Accessibility | This register, then W3C Web Accessibility Initiative guidance |

The [authority files](authorities/) record what was adopted from each source
and link to it. They are interpretations, not copies, and the external guide
stays the authority behind each rule. Look up an edge case on the web:

| Authority | Consult for |
| --- | --- |
| [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/welcome/) | Microsoft terminology, the word list, and anything in sections 2 to 7 marked Microsoft |
| [Google developer documentation style guide](https://developers.google.com/style) | Structure, code samples, and its word list |
| [Chicago Manual of Style](https://www.chicagomanualofstyle.org/) | Mechanics beyond this register (subscription) |
| [Merriam-Webster](https://www.merriam-webster.com/) | Spelling, compounds, and hyphenation, after official terms |
| [Digital.gov plain language](https://digital.gov/guides/plain-language/principles) | Plain-language detail |
| [W3C WAI](https://www.w3.org/WAI/) | Headings, link text, alternative text, and tables |
