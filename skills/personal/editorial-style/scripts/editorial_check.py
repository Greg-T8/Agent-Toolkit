#!/usr/bin/env python3
"""editorial_check: the mechanical half of the editorial-style decision register.

Ported from the Deliverable Accelerator's qeditorial.py, with Greg Tate's
house rules added. It checks Markdown or plain text, and google-workspace-design's
audit_doc.py imports it to run the same checks on a Google Doc.

Enforced (exit 1 when any fires; decision register section 2):

    heading_case()      sentence-style capitalization in headings
    title_case()        title case in a document title (house rule)
    vague_heading()     a heading that says nothing on its own ("Other", "Gaps")
    serial_comma()      a comma before the conjunction in a list of three or more
    bare_identifiers()  resource-style names outside code formatting
    word_choice()       Latin abbreviations, loaded terms, filler phrases, and
                        the house word list
    dashes()            em dashes, and spaced en dashes used as dashes (house rule)
    vague_links()       link text such as "here" or "this link"

review() is advisory. It lists sentences and paragraphs that hit a
decomposition trigger (references/decomposition.md). Every trigger fires on
some correct writing, so it never changes the exit code; reread each item and
decompose it or keep it.

Every check is deliberately narrow. A check that fires on correct writing
teaches people to ignore it, so each one reports the text it matched.

Usage:
    python editorial_check.py FILE.md            Markdown (default for .md)
    python editorial_check.py FILE.txt --text    plain text, such as an email
    python editorial_check.py FILE.md --no-review
    python editorial_check.py FILE.md --json

Words cited as words go in quotation marks and are exempt from the serial-comma
and word-choice checks. Wrap a block of cited examples, such as a list of
phrases to avoid, in <!-- editorial-check: off --> and <!-- editorial-check: on -->.
"""

from __future__ import annotations

import json
import re
import sys

# --------------------------------------------------------------------------
# Headings: sentence-style capitalization
# --------------------------------------------------------------------------

# Common words that are capitalized in a heading only because someone wrote it
# in title case. Proper nouns are not in this list, so "Azure Monitor Agent" or
# "Microsoft Entra ID" in a heading pass. The list is the vocabulary of document
# structure, which is where title case creeps in: section names copied from an
# architecture, a template, or another document.
TITLE_CASE_WORDS = frozenset("""
about action actions aligned analysis answer answers appendices appendix approach
architecture area areas assessment assumptions background baseline by capacity
changes checklist conclusion conclusions configuration considerations constraints
contents context cost costs coverage current cutover decision decisions definitions
dependencies deployment design details effort estimate estimates evidence example
examples executive extract findings for glossary go guide history how implementation
in introduction inventory issues it items key learning made management mitigations
monitoring need needs next notes objectives of on open options or overview path phase
phases plan planning post-migration prerequisites priorities priority questions
recommendation recommendations recommended reference references requirements results
review revision risk risks roadmap rollback scope sequence session sessions state
steps suggested summary target the this to topics troubleshooting understanding
usage validation wave we what where why with works your
a an and at but from into
""".split())

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
_LEADING_ID_RE = re.compile(r"^\s*(?:[A-Z]{2,5}-\d{2,3}|\d+(?:\.\d+)*\.?)\s+")

# Product and feature names whose official capitalization includes a word from
# the list above. Removed from a heading before it is checked. Add to this list
# when a real product name trips the check; never loosen the word list instead.
PROTECTED_NAMES = (
    "Key Vault", "Cost Management", "Change Tracking and Inventory",
    "Update Management", "Configuration Manager", "State Configuration",
    "Baseline Alerts", "Operations Management Suite", "Cloud Adoption Framework",
    "Well-Architected Framework", "Azure Landing Zones", "Security Center",
    "Network Watcher", "Service Map", "Microsoft Learn", "Workload Identity",
    "Log Analytics", "Application Insights", "Recovery Services", "Site Recovery",
    "Writing Style Guide", "Manual of Style", "Recovery Services Vault",
)


# Decision register: headings that tell the reader nothing on their own. Matched
# against the WHOLE heading, so "Release notes" or "Configuration details" pass.
# "Notes" is not here: some templates give it a stable meaning, such as a
# procedure's notes block.
VAGUE_HEADINGS = frozenset({
    "other", "others", "details", "gaps", "misc", "miscellaneous",
    "general", "additional information", "more information", "other information",
    "access gaps", "various", "items", "stuff", "things",
})


def vague_heading(text: str) -> bool:
    """True if the heading's whole text is a word that describes nothing."""
    t = re.sub(r"\s+", " ", (text or "").strip().rstrip(":.").lower())
    return t in VAGUE_HEADINGS


def heading_case(text: str) -> str | None:
    """Return the offending words if a heading is in title case, else None.

    The first word, and the first word after a colon, are allowed a capital.
    Acronyms and mixed-case names (ID, DNS, PowerShell) are never flagged.
    """
    if not text:
        return None
    # A leading entry ID ("AMR-03") or outline number ("1.1.1", which Markdown headings
    # carry in their text) is the heading's number, not its first word, so the word after
    # it keeps its capital. Added 2026-11-06; outline numbers added 2026-11-07.
    text = _LEADING_ID_RE.sub("", text)
    for name in PROTECTED_NAMES:
        text = text.replace(name, "X")
    bad = []
    first = True
    for token in re.split(r"(\s+|:)", text.strip()):
        if token == ":":
            first = True
            continue
        if not token or token.isspace():
            continue
        m = _WORD_RE.search(token)
        if not m:
            first = False
            continue
        word = m.group(0)
        if (not first and word[0].isupper() and word[1:].islower()
                and word.lower() in TITLE_CASE_WORDS):
            bad.append(word)
        first = False
    return ", ".join(bad) if bad else None


# --------------------------------------------------------------------------
# Serial comma
# --------------------------------------------------------------------------

# "A, B and C": up to three words per item, one comma, then the conjunction.
_SERIES_RE = re.compile(
    r"(?<![\w,-])(?P<a>[\w.'/-]+(?: [\w.'/-]+){0,2}), "
    r"(?P<b>[\w.'/-]+(?: [\w.'/-]+){0,2}) (?P<conj>and|or) (?P<c>[\w.'/-]+)")

# The first item is really an introductory phrase: "If so, delete them and ..."
_INTRO_WORDS = frozenset("""
if when whenever once after before since because although though while unless until
in on at for from by with without during within under over across today currently
then however otherwise also first second third finally instead meanwhile here there
now so yes no as where whether
""".split())

# The second item opens a clause, not a list item: "... the fleet, the team said
# and ..." is rare in lists and common in prose.
_CLAUSE_OPENERS = frozenset("""
it its they them their we you he she this that these those which who so but yet
there here each every both either neither if when then because although while
across along among around at by during for from in into on to with within without
after before since until than like such per about against and or nor not
including excluding except especially unlike between under over above below behind
beneath beside through throughout toward towards inside outside near available
""".split())


_IDIOM_TAILS = frozenset({("or", "more"), ("or", "less"), ("or", "fewer"), ("and", "so"),
                          ("or", "later"), ("or", "earlier"), ("or", "higher"),
                          ("or", "lower"), ("or", "greater"), ("or", "above"),
                          ("or", "below"), ("or", "not"), ("and", "below"),
                          ("and", "after"), ("and", "off"), ("and", "out")})


def serial_comma(text: str) -> list[str]:
    """Lists of three or more items with no comma before the conjunction."""
    out = []
    if not text:
        return out
    for m in _SERIES_RE.finditer(text):
        a, b = m.group("a"), m.group("b")
        a_first = a.split()[0].lower()
        b_first = b.split()[0].lower()
        if a_first in _INTRO_WORDS or b_first in _CLAUSE_OPENERS:
            continue
        # "Degraded or unavailable, platform or unknown": pairs, not a list of three
        if re.search(r"\b(and|or)\b", a):
            continue
        # "one or more", "and so on", "or later": an idiom, not the list's last item
        if (m.group("conj"), m.group("c").lower()) in _IDIOM_TAILS:
            continue
        # "September 15, 2026 and later": a date, not a list
        if re.fullmatch(r"\d{4}", b):
            continue
        # "between A and B", "both A and B": two items, not three
        before = text[:m.start()].rstrip().split()
        if before and before[-1].lower() in ("between", "both", "either"):
            continue
        # "When A and B disagree, follow X and Y": the first comma closes an
        # introductory clause that started the sentence.
        start = max(text.rfind(ch, 0, m.start()) for ch in ".!?:;") + 1
        opener = text[start:m.start()].split() + a.split()
        if opener and opener[0].lower().strip("(\"'") in _INTRO_WORDS:
            continue
        # "A, B and C D, E": the "and" sits inside an item of a longer list.
        if re.match(r"(?:\s+[\w'.-]+){0,2},", text[m.end():]):
            continue
        # A match that runs across a sentence end, or starts at a year
        if re.search(r"[.!?]\s", m.group(0)) or re.fullmatch(r"\d{4}", a):
            continue
        out.append(m.group(0))
    return out


# --------------------------------------------------------------------------
# Identifiers outside Code
# --------------------------------------------------------------------------

# Lowercase, hyphen-joined, and either carrying a digit or made of three or more
# parts: law-d4c-prod-01, rg-ent-prd-monitoring-services, azure-ops-critical.
_IDENT_RE = re.compile(r"(?<![\w/`.-])([a-z][a-z0-9]*(?:-[a-z0-9]+){1,})(?![\w`-])")

# A hyphenated English phrase contains a connecting word. An identifier does not.
_ENGLISH_PARTS = frozenset("""
a an and as at by for from in into of off on or out over per plus the than to up
versus with you
""".split())

# Hyphenated English words that carry no connecting word but are not identifiers.
_ENGLISH_COMPOUNDS = frozenset("""
end-to-end day-to-day up-to-date state-of-the-art out-of-the-box point-in-time
read-write read-only non-production pre-production multi-factor two-factor
self-service third-party first-party real-time long-term short-term well-known
""".split())


# Azure resource-type abbreviations from the Cloud Adoption Framework naming
# guidance. A two-part name that starts with one (law-assessment, rg-network) is
# an identifier even without a digit.
_RESOURCE_PREFIXES = frozenset("""
ag agw aks acr afw apim apr appi ar asp bas cosmos dce dcr evh evhns fw kv law lb log
mi nic nsg pe pip rg rsv rt snet sql sqldb st udr vm vmss vnet vpng
""".split())

# Second parts that make a two-part prefix word English: vm-based, rg-level.
_ENGLISH_SUFFIXES = frozenset("""
based level only wide scoped specific side ready related driven like aware friendly
""".split())


def bare_identifiers(text: str) -> list[str]:
    """Resource-style names in text that is not in Code style.

    Call with the text of runs or spans that are NOT code. The caller decides
    what counts as code: a `Code` run in Word, a backtick span in Markdown.
    """
    found = []
    for m in _IDENT_RE.finditer(text or ""):
        tok = m.group(1)
        parts = tok.split("-")
        if tok in _ENGLISH_COMPOUNDS or any(p in _ENGLISH_PARTS for p in parts):
            continue
        has_digit = any(ch.isdigit() for ch in tok)
        prefixed = (parts[0] in _RESOURCE_PREFIXES
                    and not any(p in _ENGLISH_SUFFIXES for p in parts[1:]))
        if has_digit or len(parts) >= 3 or prefixed:
            found.append(tok)
    return found


# --------------------------------------------------------------------------
# Word choice
# --------------------------------------------------------------------------

WORD_CHOICE = [
    (re.compile(r"\be\.g\.", re.I), "'e.g.': write 'for example'"),
    (re.compile(r"\bi\.e\.", re.I), "'i.e.': write 'that is'"),
    (re.compile(r"\betc\.?(?=\W|$)", re.I), "'etc.': write 'and so on', or finish the list"),
    (re.compile(r"\butiliz(?:e|es|ed|ing|ation)\b", re.I), "'utilize': write 'use'"),
    (re.compile(r"\bwhite-?list", re.I), "'whitelist': write 'allow list'"),
    (re.compile(r"\bblack-?list", re.I), "'blacklist': write 'block list'"),
    # Filler phrases. Whole phrases only.
    (re.compile(r"\bin order to\b", re.I), "'in order to': write 'to'"),
    (re.compile(r"\bdue to the fact that\b", re.I), "'due to the fact that': write 'because'"),
    (re.compile(r"\bin the event that\b", re.I), "'in the event that': write 'if'"),
    (re.compile(r"\bat this point in time\b", re.I), "'at this point in time': write 'now'"),
    (re.compile(r"\bwith regard(?:s)? to\b", re.I), "'with regard to': write 'about' or 'for'"),
    (re.compile(r"\bmake(?:s|ing)? use of\b|\bmade use of\b", re.I), "'make use of': write 'use'"),
    (re.compile(r"\bit should be noted that\b", re.I), "'it should be noted that': cut it"),
    (re.compile(r"\bit is important to note\b", re.I), "'it is important to note': cut it"),
    (re.compile(r"\bplease note\b", re.I), "'please note': cut it, or use a Note callout"),
]


def word_choice(text: str) -> list[str]:
    return [msg for rx, msg in WORD_CHOICE if rx.search(text or "")]


# --------------------------------------------------------------------------
# One entry point
# --------------------------------------------------------------------------

def lint(headings: list[str], prose: list[str], non_code: list[str]) -> list[str]:
    """Run every enforced check and return issue strings.

    headings  heading texts
    prose     body paragraphs and table cells, markup removed, code INCLUDED
              (a serial comma is punctuation, code or not)
    non_code  the same text with code spans removed, for the identifier and
              word-choice checks
    """
    issues: list[str] = []
    for h in headings:
        if vague_heading(h):
            issues.append(
                f"editorial: heading {h[:60]!r} does not say what follows. Name the "
                "information under it, for example 'Review limitations' rather than "
                "'Gaps' (decision register, enforced rules).")
        bad = heading_case(h)
        if bad:
            issues.append(
                f"editorial: heading {h[:60]!r} is title case ({bad}). Headings are "
                "sentence case: capitalize the first word and proper nouns only "
                "(decision register, enforced rules).")
    seen: set[str] = set()
    for p in prose:
        for s in serial_comma(p):
            if s not in seen:
                seen.add(s)
                issues.append(
                    f"editorial: no serial comma in {s!r}. Put a comma before the "
                    "conjunction in a list of three or more (decision register, enforced rules).")
    idents: dict[str, int] = {}
    words: set[str] = set()
    for t in non_code:
        for tok in bare_identifiers(t):
            idents[tok] = idents.get(tok, 0) + 1
        words.update(word_choice(t))
    for tok, n in idents.items():
        issues.append(
            f"editorial: {tok!r} appears {n} time(s) outside code formatting. Resource "
            "names, table names, and property values take code formatting (decision register, code formatting).")
    for w in sorted(words):
        issues.append(f"editorial: {w} (decision register, enforced rules).")
    return issues


# --------------------------------------------------------------------------
# Decomposition review (advisory), decomposition.md
# --------------------------------------------------------------------------

REVIEW_SENTENCE_WORDS = 25      # a review trigger, not a limit
REVIEW_PARAGRAPH_SENTENCES = 5
# Decision register, inline series: an inline series of more than
# this many `Code` identifiers belongs in a list or a table.
REVIEW_SERIES_IDENTIFIERS = 3

# Words that join clauses. Two or more in one sentence often mean one sentence
# has absorbed several statements.
_JOINERS_RE = re.compile(
    r"\b(which|while|whereas|because|as well as|including|where|although)\b", re.I)

# A sentence ends at . ! or ? followed by space and a capital, digit, quote,
# bracket, or code span. Decimal points and dotted identifiers do not qualify.
_SENTENCE_END_RE = re.compile(r"(?<=[.!?])[\"\u201d')\]]*\s+(?=[A-Z0-9\"\u201c(`*\[])")

# Words that make a clause after a colon a statement rather than a list or phrase
# ("shows what that costs: 48 VMs have no alerting"). The decision register and decomposition.md.
_CLAUSE_VERB_RE = re.compile(
    r"\b(is|are|was|were|has|have|had|does|do|did|can|cannot|can't|will|won't|would|"
    r"should|must|may|might|isn't|aren't|doesn't|don't|hasn't|haven't)\b", re.I)

# A dash used as punctuation, not as a hyphen or a range.
_DASH_RE = re.compile(r"\u2014|\s[\u2013-]\s")


def sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return []
    return [s for s in _SENTENCE_END_RE.split(text) if s.strip()]


def _colon_joins_statements(s: str) -> bool:
    """A colon whose tail is a statement with its own verb (decision register, decomposition).

    A list or a short phrase after a colon is fine. Skipped: a short tail (a list
    entry's gloss), a verb inside a relative clause ("a filter that cannot match"),
    and the recommendations "Not verified:" lead-in, which is a label.
    """
    head, colon, tail = s.partition(":")
    if not colon or len(head.split()) < 3 or len(tail.split()) < 8:
        return False
    if re.search(r"\bnot verified\s*$", head, re.I):
        return False
    for m in _CLAUSE_VERB_RE.finditer(tail):
        before = tail[:m.start()].split()[-2:]
        if not any(w.lower().strip(",") in ("that", "which", "who") for w in before):
            return True
    return False


def _sentence_triggers(s: str) -> list[str]:
    """Reasons to reread a sentence, or [] if none applies.

    Length alone is weak evidence in technical prose, so a long sentence is only
    reported when it is well past the trigger, or when it also shows a sign of
    carrying a second idea: a clause joiner, a colon, or a parenthesis.
    """
    reasons = []
    words = len(s.split())
    joiners = [m.group(1).lower() for m in _JOINERS_RE.finditer(s)]
    marks = s.count("(") + len(_DASH_RE.findall(s))
    if words > REVIEW_SENTENCE_WORDS:
        structural = joiners or marks or ":" in s.rstrip(":")
        if structural or words > REVIEW_SENTENCE_WORDS + 10:
            reasons.append(f"{words} words")
    if len(joiners) >= 2:
        reasons.append("joins clauses with " + ", ".join(f"'{j}'" for j in joiners))
    # A semicolon between clauses, not one separating short list entries
    # ("Action groups; Alert processing rules").
    if ";" in s and any(len(seg.split()) > 8 for seg in s.split(";")):
        reasons.append("semicolon")
    if marks >= 2:
        reasons.append(f"{marks} parentheses or dashes")
    if _colon_joins_statements(s):
        reasons.append("colon joins two statements")
    return reasons


# Between two identifiers in a series: a comma, "and", or "or", alone or together.
_SERIES_SEP_RE = re.compile(r"^(?:,|,? ?(?:and|or))$")


def _longest_series(sentence: str, positions: list[tuple[int, int]]) -> int:
    """Items in the longest inline series of identifiers in one sentence.

    `positions` are (start, end) offsets of the identifiers in `sentence`, in
    order. Identifiers separated by a comma, "and", or "or" are separate items.
    A short connecting phrase with no punctuation ("`law-assessment` in
    `rg-identity-services`") keeps both in one item. Anything else, including a
    colon, ends the series: "Five sit in `rg-x`: `a`, `b`, `c`" is a series of three.
    """
    best = 0
    items = 0
    prev_end = None
    for start, end in positions:
        if prev_end is None:
            items = 1
        else:
            between = sentence[prev_end:start].strip()
            if _SERIES_SEP_RE.match(between):
                items += 1
            elif len(between.split()) <= 3 and not re.search(r"[:;.()\u2014]", between):
                pass                                  # a qualifier inside one item
            else:
                items = 1
        best = max(best, items)
        prev_end = end
    return best


def _series_per_sentence(paragraph: str, spans: list[str] | None) -> list[tuple[str, int]]:
    """Each sentence of a paragraph, with its longest inline series of identifiers.

    `spans` are the paragraph's code spans in order, as the emitter saw them: a
    run of `Code` runs in Word, a backtick span in Markdown. With no spans given
    (a caller that does not separate code), fall back to resource-style names,
    which finds the hyphenated ones and misses names like `MS-Sentinel`.
    """
    ss = sentences(paragraph)
    if spans is None:
        return [(s, _longest_series(s, [m.span(1) for m in _IDENT_RE.finditer(s)
                                        if bare_identifiers(m.group(1))]))
                for s in ss]
    norm = re.sub(r"\s+", " ", (paragraph or "").strip())
    bounds, pos = [], 0
    for s in ss:
        start = norm.find(s, pos)
        if start < 0:
            start = pos
        bounds.append(start)
        pos = start + len(s)
    per: list[list[tuple[int, int]]] = [[] for _ in ss]
    pos = 0
    for span in spans:
        span = re.sub(r"\s+", " ", span.strip())
        if not span:
            continue
        at = norm.find(span, pos)
        if at < 0:
            continue
        pos = at + len(span)
        for i in range(len(ss) - 1, -1, -1):
            if at >= bounds[i]:
                if at + len(span) <= bounds[i] + len(ss[i]):
                    per[i].append((at - bounds[i], at - bounds[i] + len(span)))
                break
    return [(s, _longest_series(s, per[i])) for i, s in enumerate(ss)]


def review(paragraphs: list[str],
           code_spans: list[list[str]] | None = None) -> list[str]:
    """Sentences and paragraphs to reread for decomposition (decomposition.md).

    paragraphs  body paragraphs and list items, markup removed, code included.
                Not headings and not table cells: a cell is a fragment by design.
    code_spans  optional, parallel to `paragraphs`: each paragraph's code spans
                in order. Used by the inline-series trigger; without
                it, that trigger finds resource-style names instead.

    Advisory. Returns notes, never issues: the caller prints them and the author
    decides, sentence by sentence, whether to decompose or keep.
    """
    notes: list[str] = []
    for i, p in enumerate(paragraphs):
        spans = code_spans[i] if code_spans is not None and i < len(code_spans) else None
        pairs = _series_per_sentence(p, spans)
        if len(pairs) > REVIEW_PARAGRAPH_SENTENCES:
            notes.append(
                f"review: paragraph of {len(pairs)} sentences starting {p.strip()[:60]!r}. "
                "Does it have one primary purpose?")
        for s, n_series in pairs:
            reasons = _sentence_triggers(s)
            if n_series > REVIEW_SERIES_IDENTIFIERS:
                reasons.append(f"inline series of {n_series} identifiers, use a list or "
                               "a table")
            if not reasons:
                continue
            notes.append(f"review: {'; '.join(reasons)}: {s.strip()[:90]!r}")
    return notes


# --------------------------------------------------------------------------
# House rules (decision register section 1)
# --------------------------------------------------------------------------

# Title case: every word capitalized except these, unless first or last.
MINOR_WORDS = frozenset("""
a an the and but or nor for so yet as at by in of off on per to up via
""".split())


def title_case(text: str) -> str | None:
    """Return the offending words if a document title is not in title case."""
    text = _LEADING_ID_RE.sub("", text or "")
    words = [m.group(0) for m in _WORD_RE.finditer(text)]
    bad = [w for n, w in enumerate(words)
           if w[0].islower() and (n in (0, len(words) - 1) or w.lower() not in MINOR_WORDS)]
    return ", ".join(bad) if bad else None


# An em dash anywhere, or an en dash or hyphen with a space on each side used as
# a dash. A closed en dash in a range ("10–15") is correct and passes.
_EM_DASH_RE = re.compile(r"\u2014")
_SPACED_DASH_RE = re.compile(r"\s[\u2013-]\s")


def dashes(text: str) -> list[str]:
    out = []
    for m in _EM_DASH_RE.finditer(text or ""):
        out.append((text[max(0, m.start() - 25):m.end() + 25]).strip())
    for m in _SPACED_DASH_RE.finditer(text or ""):
        # "1.3.0 - 2026-11-25": a separator between a version and a date, not a dash
        if re.search(r"\d$", text[:m.start()]) and re.match(r"\d", text[m.end():]):
            continue
        out.append((text[max(0, m.start() - 25):m.end() + 25]).strip())
    return out


# Added to the Accelerator's word list from the Microsoft word list and bias-free
# guidance. Each entry is a whole word or phrase with one correct replacement.
HOUSE_WORDS = [
    (re.compile(r"\bon-premise\b(?!s)", re.I), "'on-premise': write 'on-premises'"),
    (re.compile(r"\be-mail", re.I), "'e-mail': write 'email'"),
    (re.compile(r"\band/or\b", re.I), "'and/or': write 'or', or 'A, B, or both'"),
    (re.compile(r"\bmaster/slave\b|\bslaves?\b", re.I),
     "'master/slave': write 'primary/secondary' or the product's own terms"),
    (re.compile(r"\bsanity[- ]check", re.I), "'sanity check': write 'check' or 'confidence check'"),
]
WORD_CHOICE.extend(HOUSE_WORDS)

VAGUE_LINK_TEXT = frozenset({"here", "click here", "this link", "link", "this", "this page",
                             "read more", "more", "learn more"})


def vague_links(link_texts: list[str]) -> list[str]:
    return [t for t in link_texts
            if re.sub(r"\s+", " ", t.strip().lower()).strip(".") in VAGUE_LINK_TEXT]


# Words to reread, not errors: each has correct uses. Reported by review().
REVIEW_WORDS = [
    (re.compile(r"\bvia\b", re.I), "'through', 'by using', or 'with' is usually plainer"),
    (re.compile(r"\b(simply|just|easy|easily|obviously|of course)\b", re.I),
     "may play down real complexity"),
    (re.compile(r"\bplease\b", re.I), "'please' in an instruction adds nothing"),
    (re.compile(r"\blog(?:-| )?(?:in|on) to\b", re.I),
     "Microsoft accounts and Azure use 'sign in to'"),
    (re.compile(r"\b(we|our|let's)\b", re.I),
     "first-person plural: is the author or team really the actor?"),
]


# --------------------------------------------------------------------------
# One entry point for every front end
# --------------------------------------------------------------------------

# Words cited as words ("in order to", "A, B and C") sit in quotation marks and
# are exempt from the serial-comma and word-choice checks.
_QUOTED_RE = re.compile(r'"[^"\n]*"|\u201c[^\u201d\n]*\u201d')


def unquoted(text: str) -> str:
    return _QUOTED_RE.sub(" ", text or "")


def check(title: str | None, headings: list[str], prose: list[str], non_code: list[str],
          link_texts: list[str] | None = None) -> list[str]:
    """Every enforced check. Returns issue strings; any issue fails."""
    issues = lint(headings, [unquoted(t) for t in prose], [unquoted(t) for t in non_code])
    if title:
        bad = title_case(title)
        if bad:
            issues.append(f"editorial: title {title[:60]!r} is not title case ({bad}). "
                          "Capitalize every word except minor words that are not first or "
                          "last (decision register, house rules).")
    seen: set[str] = set()
    # Dashes are checked outside code: "endIndex - 1" in a code span is code.
    for t in [title or ""] + list(headings) + list(non_code):
        for d in dashes(t):
            if d not in seen:
                seen.add(d)
                issues.append(f"editorial: dash in {d!r}. No em dashes or spaced dashes: use "
                              "a colon, parentheses, a comma, or a new sentence (house rules).")
    for t in vague_links(link_texts or []):
        issues.append(f"editorial: link text {t!r} says nothing on its own. Use the "
                      "destination's title (decision register, structure).")
    return issues


def review_all(paragraphs: list[str], code_spans: list[list[str]] | None = None) -> list[str]:
    notes = review(paragraphs, code_spans)
    for p in paragraphs:
        for rx, why in REVIEW_WORDS:
            m = rx.search(unquoted(p))
            if m:
                notes.append(f"review: '{m.group(0)}' ({why}): {p.strip()[:80]!r}")
    return notes


# --------------------------------------------------------------------------
# Markdown and plain-text front ends
# --------------------------------------------------------------------------

_CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")
_LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)]*)\)")
_EMPH_RE = re.compile(r"(\*\*|__|\*|_)(?=\S)(.+?)(?<=\S)\1")


def _plain(md: str) -> str:
    """Markdown inline markup removed; code span text kept."""
    t = _LINK_RE.sub(lambda m: m.group(1), md)
    t = _CODE_SPAN_RE.sub(lambda m: m.group(2), t)
    t = _EMPH_RE.sub(lambda m: m.group(2), t)
    return t.replace("\\", "")


def _non_code(md: str) -> str:
    t = _LINK_RE.sub(lambda m: m.group(1), md)
    t = _CODE_SPAN_RE.sub(" ", t)
    return _EMPH_RE.sub(lambda m: m.group(2), t)


def parse_markdown(text: str) -> dict:
    """Split Markdown into title, headings, paragraphs, cells, code spans, links.

    Skips YAML front matter, fenced code blocks, HTML comments, and blocks
    between editorial-check off and on comments. Block quotes are kept. The first H1 is
    the title only when it is the first heading and no other H1 follows; Markdown
    headings themselves follow sentence case.
    """
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    # <!-- editorial-check: off --> ... <!-- editorial-check: on --> skips a block,
    # such as a list of phrases to avoid. Use it for cited examples only.
    text = re.sub(r"<!--\s*editorial-check:\s*off\s*-->.*?(<!--\s*editorial-check:\s*on\s*-->|\Z)",
                  "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = text.splitlines()
    headings, paras, cells, spans, links = [], [], [], [], []
    buf: list[str] = []
    fence = None

    def flush():
        if buf:
            para = " ".join(s.strip() for s in buf)
            paras.append(para)
            buf.clear()

    for line in lines:
        s = line.strip()
        f = re.match(r"^(```+|~~~+)", s)
        if f:
            flush()
            fence = None if fence and s.startswith(fence) else (fence or f.group(1))
            continue
        if fence:
            continue
        if not s:
            flush()
            continue
        h = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", s)
        if h:
            flush()
            headings.append((len(h.group(1)), h.group(2)))
            continue
        if s.startswith("|"):
            flush()
            if re.fullmatch(r"\|?[\s:|-]+\|?", s):
                continue
            cells.extend(c.strip() for c in s.strip("|").split("|") if c.strip())
            continue
        item = re.match(r"^(?:[-*+]|\d+[.)])\s+(.*)", s)
        if item:
            flush()
            buf.append(item.group(1))
            flush()
            continue
        buf.append(re.sub(r"^>\s?", "", s))
    flush()
    for p in paras + cells:
        links.extend(m.group(1) for m in _LINK_RE.finditer(p) if not m.group(0).startswith("!"))
    return {"headings": headings, "paragraphs": paras, "cells": cells, "links": links}


def check_markdown(text: str, title: str | None = None) -> tuple[list[str], list[str]]:
    d = parse_markdown(text)
    heads = [h for _, h in d["headings"]]
    body = d["paragraphs"] + d["cells"]
    issues = check(title, [_plain(h) for h in heads],
                   [_plain(p) for p in body], [_non_code(p) for p in body], d["links"])
    notes = review_all([_plain(p) for p in d["paragraphs"]],
                       [[m.group(2) for m in _CODE_SPAN_RE.finditer(p)] for p in d["paragraphs"]])
    return issues, notes


def check_text(text: str) -> tuple[list[str], list[str]]:
    """Plain text, such as an email or a chat message: paragraphs only."""
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    issues = check(None, [], paras, paras, [])
    return issues, review_all(paras)


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    if not args:
        print(__doc__)
        return 2
    path = args[0]
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    as_text = "--text" in flags or not path.lower().endswith((".md", ".markdown"))
    issues, notes = check_text(text) if as_text else check_markdown(text)
    if "--no-review" in flags:
        notes = []
    if "--json" in flags:
        print(json.dumps({"issues": issues, "review": notes}, indent=2))
    else:
        print(f"Enforced issues: {len(issues)}")
        for i in issues:
            print("  " + i)
        print(f"Review notes (advisory): {len(notes)}")
        for n in notes:
            print("  " + n)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
