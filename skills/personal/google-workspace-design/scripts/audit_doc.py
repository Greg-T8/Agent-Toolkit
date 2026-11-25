"""Audit a Google Doc against the Docs spec.

Usage: python audit_doc.py DOC.json [--tab TAB_ID]
       python audit_doc.py DOC.md

DOC.json is the documents.get response (the Docs connector's read_doc output,
saved to a file). DOC.md is a Doc someone already downloaded with File >
Download > Markdown (.md), for reviewing an export outside the skill workflow;
the workflow never asks for one. The Markdown export cannot show fonts,
semibold, or empty paragraphs, so those checks run only on JSON. Prints counts and examples for each check in
docs-spec.md section 7 and exits 1 when any hard check fails, 0 when all pass.

Hard checks (must be 0): bold past label, commands outside code blocks,
lead-in lines followed by loose paragraphs, callout sentences left as
paragraphs, em dashes, double-numbered or dash-separated headings, unstyled
runs in a document whose Normal style is still Arial, consecutive empty
paragraphs, one-item lists after a lead-in, sentences split across a list,
arrow chains in paragraphs, labels split from their values, label-value settings
outside a list, empty list items, one-column data tables, blank paragraphs
between a paragraph and the table after it, list items ending with a colon
whose sub-items are not nested, a title not in title case. Advisory checks: identifiers not in inline code, short fragments,
field lists that should be schema tables.
"""
import json
import re
import sys

LABEL = re.compile(r"^([A-Z][A-Za-z0-9 /()'\-]{0,45}?):")
COMMAND = re.compile(r"(^|\s)(az|dotnet|func|git|curl|pip|npm|kubectl|terraform|ssh|sudo|"
                     r"systemctl|journalctl|hermes|docker|python3?)\s+[a-z-]{2,}|(^|\s)"
                     r"(Get|Set|New|Remove|Install|Invoke|Start|Stop)-[A-Z][A-Za-z]+")
CALLOUT_WORDS = re.compile(r"^(Note|Important|Warning|Caution|Risk|Decision|Tip|STOP POINT|"
                           r"Safety gate|Do not|Never|Defer\b)", re.I)
IDENT = re.compile(r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b|\b[a-z_]+:[a-z_]+\b")
RUN_IN = {"purpose", "action", "next action", "expected", "result", "verify", "owner",
          "status", "decision", "rationale", "note", "warning", "tip", "risk"}
HEAD_NUM_BAD = re.compile(r"^\d+\\?\.\s|^\d+(\.\d+)*\s.*\b(Phase|Part|Section)\s+\d")


def load(path, tab_id=None):
    d = json.load(open(path))
    d = d.get("content", d)
    if "tabs" in d:
        tabs = d["tabs"]
        tab = next((t for t in tabs if t["tabProperties"]["tabId"] == tab_id), tabs[0]) if tab_id else tabs[0]
        dt = tab["documentTab"]
        return dt["body"]["content"], {s["namedStyleType"]: s for s in dt["namedStyles"]["styles"]}
    return d["body"]["content"], {s["namedStyleType"]: s for s in d["namedStyles"]["styles"]}


def text(p):
    return "".join(e["textRun"]["content"] for e in p["elements"] if "textRun" in e).rstrip("\n")


def runs(p):
    return [e["textRun"] for e in p["elements"] if "textRun" in e]


def is_bold(s):
    return bool(s.get("bold")) or s.get("weightedFontFamily", {}).get("weight", 400) >= 600


def is_mono(s):
    f = s.get("weightedFontFamily", {}).get("fontFamily", "")
    return "Mono" in f or "Courier" in f or "Consolas" in f


def has_bg(s):
    return bool(s.get("backgroundColor", {}).get("color"))


def kind_of_table(t):
    cell = t["tableRows"][0]["tableCells"][0]
    cs = cell.get("tableCellStyle", {})
    rgb = cs.get("backgroundColor", {}).get("color", {}).get("rgbColor", {})
    fill = tuple(round(rgb.get(k, 0) * 255) for k in ("red", "green", "blue")) if rgb else None
    left = cs.get("borderLeft", {}).get("width", {}).get("magnitude", 0)
    if t["rows"] == 1 and t["columns"] == 1:
        if fill == (241, 243, 245):
            return "code"
        return "callout" if left >= 3 else "one-cell"
    return "data"


HARD_KEYS = ["bold past label", "commands outside code blocks (inline)",
             "commands outside code blocks (plain text)", "lead-in followed by loose paragraphs",
             "callout sentences left as paragraphs", "em dashes",
             "double-numbered or period-numbered headings", "runs falling back to Arial",
             "consecutive empty paragraphs", "one-item lists after a lead-in",
             "sentences split across a list", "arrow chains in paragraphs",
             "labels split from their values", "settings outside a list",
             "empty list items", "one-column tables", "blank paragraphs before a table",
             "sub-lists not nested", "title not in title case"]
ADV_KEYS = ["identifiers not in inline code", "short fragments after a lead-in",
            "field lists that should be schema tables"]
FIELDS = re.compile(r"\b(fields?|columns?|schema|properties)\b", re.I)


def report(tables, hard, adv, ex, skipped=()):
    print("Tables:", ", ".join(f"{k} {v}" for k, v in sorted(tables.items())) or "none")
    print("\nHard checks (must be 0):")
    for key in HARD_KEYS:
        val = "n/a (JSON only)" if key in skipped else hard.get(key, 0)
        print(f"  {key:46s} {val}")
    print("\nAdvisory:")
    for key in ADV_KEYS:
        print(f"  {key:46s} {adv.get(key, 0)}")
    for key, items in ex.items():
        print(f"\n{key}:")
        for item in items:
            print("   ", item)
    return 1 if any(hard.values()) else 0


def unescape(line):
    return re.sub(r"\\([\\`*_{}\[\]()#+\-.!|])", r"\1", line)


def main_markdown(path):
    lines = [unescape(l.rstrip()) for l in open(path, encoding="utf-8")]
    hard, adv, ex, tables = {}, {}, {}, {}

    def hit(bucket, key, sample):
        bucket[key] = bucket.get(key, 0) + 1
        ex.setdefault(key, [])
        if len(ex[key]) < 5:
            ex[key].append(sample[:90])

    is_list = lambda l: bool(re.match(r"^\s*([*+-]|\d+[.)])\s", l))
    is_table = lambda l: l.startswith("|")
    blocks, i = [], 0          # (kind, text)
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1
            continue
        if is_table(l):
            rows = []
            while i < len(lines) and is_table(lines[i]):
                rows.append(lines[i])
                i += 1
            cells = [c for c in rows[0].strip("|").split("|")]
            body_rows = [r for r in rows if not re.match(r"^\|\s*:?-{3,}", r)]
            if len(cells) == 1:
                first = body_rows[0].strip("| ").strip() if body_rows else ""
                kind = "code" if first.startswith("`") else "callout"
            else:
                kind = "data"
            tables[kind] = tables.get(kind, 0) + 1
            blocks.append(("t", kind))
            continue
        kind = "h" if l.startswith("#") else ("l" if is_list(l) else "p")
        blocks.append((kind, l))
        i += 1
    for j, (kind, l) in enumerate(blocks):
        if kind == "t":
            continue
        if "\u2014" in l:
            hit(hard, "em dashes", l)
        if kind == "h":
            h = re.sub(r"^#+\s*", "", l)
            if HEAD_NUM_BAD.search(h):
                hit(hard, "double-numbered or period-numbered headings", h)
            continue
        t = re.sub(r"^\s*([*+-]|\d+[.)])\s+", "", l) if kind == "l" else l
        m = LABEL.match(t.replace("**", ""))
        label_len = len(m.group(0)) if m else 0
        bold = sum(len(b.strip()) for b in re.findall(r"\*\*(.+?)\*\*", t)
                   if not (b.strip().isupper() and len(b.strip()) <= 14))
        if bold > label_len + 2:
            hit(hard, "bold past label", t)
        codes = re.findall(r"`([^`]+)`", t)
        plain = re.sub(r"`[^`]+`", " ", re.sub(r"\[[^\]]*\]\([^)]*\)", " ", t)).replace("**", "")
        if kind == "p":
            for c in codes:
                runnable = COMMAND.search(" " + c) or (" " in c and re.search(r"\s--?\w", c))
                before = t.split("`" + c + "`")[0].replace("**", "")
                placed = (m and m.group(1).lower().startswith(("action", "next action", "run"))) \
                    or before.rstrip().endswith(":")
                if runnable and placed:
                    hit(hard, "commands outside code blocks (inline)", c)
            if COMMAND.search(" " + plain):
                hit(hard, "commands outside code blocks (plain text)", t)
            nxt = blocks[j + 1] if j + 1 < len(blocks) else None
            leads = plain.rstrip().endswith(":")
            if leads and nxt and nxt[0] == "l" and FIELDS.search(plain):
                hit(adv, "field lists that should be schema tables", t)
            if leads and not (nxt and nxt[0] in ("l", "t")):
                hit(hard, "lead-in followed by loose paragraphs", t)
            if CALLOUT_WORDS.match(plain.strip()) and not (leads and nxt and nxt[0] in ("l", "t")):
                hit(hard, "callout sentences left as paragraphs", t)
            prev = blocks[j - 1] if j else None
            if not m and len(plain.strip()) < 50 and not re.search(r"[.!?]$", plain.strip()) \
                    and prev and prev[0] == "p" and prev[1].rstrip().endswith(":"):
                hit(adv, "short fragments after a lead-in", t)
        for ident in IDENT.findall(plain):
            hit(adv, "identifiers not in inline code", ident)
    return report(tables, hard, adv, ex, skipped=("runs falling back to Arial",
                                                  "consecutive empty paragraphs"))


def main(path, tab_id=None):
    body, named = load(path, tab_id)
    arial = named.get("NORMAL_TEXT", {}).get("textStyle", {}).get("weightedFontFamily", {}) \
        .get("fontFamily", "Arial") == "Arial"
    seq = []
    for el in body:
        if "paragraph" in el:
            seq.append(("p", el["paragraph"]))
        elif "table" in el:
            seq.append(("t", el["table"]))
    hard, adv, ex = {}, {}, {}

    def hit(bucket, key, sample):
        bucket[key] = bucket.get(key, 0) + 1
        ex.setdefault(key, [])
        if len(ex[key]) < 5:
            ex[key].append(sample[:90])

    tables = {}
    empty_run = 0
    is_item = lambda x: x is not None and x[0] == "p" and bool(x[1].get("bullet"))
    real = lambda j: next((x for x in seq[j:] if not (x[0] == "p" and not text(x[1]).strip())), None)
    prev_real = lambda j: next((x for x in reversed(seq[:j]) if not (x[0] == "p" and not text(x[1]).strip())), None)
    for i, (k, obj) in enumerate(seq):
        if k == "t":
            kind = kind_of_table(obj)
            tables[kind] = tables.get(kind, 0) + 1
            if kind == "data" and obj["columns"] == 1:
                first = obj["tableRows"][0]["tableCells"][0]["content"][0]
                hit(hard, "one-column tables", text(first.get("paragraph", {"elements": []})) or f"table at body item {i}")
            empty_run = 0
            continue
        if obj.get("bullet") and not text(obj).strip():
            hit(hard, "empty list items", f"at body item {i}")
        nb = seq[i + 1][1].get("bullet") if i + 1 < len(seq) and seq[i + 1][0] == "p" else None
        if obj.get("bullet") and nb and text(obj).rstrip().endswith(":") \
                and nb.get("nestingLevel", 0) <= obj["bullet"].get("nestingLevel", 0):
            hit(hard, "sub-lists not nested", text(obj) + " | " + text(seq[i + 1][1]))
        p = obj
        st = p["paragraphStyle"].get("namedStyleType", "NORMAL_TEXT")
        t = text(p)
        if not t.strip():
            if not p.get("bullet") and 0 < i < len(seq) - 1 and seq[i + 1][0] == "t" \
                    and seq[i - 1][0] == "p" and text(seq[i - 1][1]).strip():
                hit(hard, "blank paragraphs before a table", text(seq[i - 1][1]))
            between_tables = 0 < i < len(seq) - 1 and seq[i - 1][0] == "t" and seq[i + 1][0] == "t"
            empty_run = 0 if between_tables else empty_run + 1
            if empty_run >= 2:
                hit(hard, "consecutive empty paragraphs", f"at body item {i}")
            continue
        empty_run = 0
        rs = runs(p)
        if "\u2014" in t:
            hit(hard, "em dashes", t)
        if st.startswith("HEADING"):
            if HEAD_NUM_BAD.search(t):
                hit(hard, "double-numbered or period-numbered headings", t)
            continue
        if st == "TITLE":
            minor = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet",
                     "as", "at", "by", "in", "of", "off", "on", "per", "to", "up", "via"}
            words = re.findall(r"[A-Za-z][\w'-]*", t)
            bad = [w for n, w in enumerate(words) if w[0].islower()
                   and (n in (0, len(words) - 1) or w.lower() not in minor)]
            if bad:
                hit(hard, "title not in title case", t)
            continue
        if st == "SUBTITLE":
            continue
        nxt_item = seq[i + 1] if i + 1 < len(seq) else None
        if t.isupper() and len(t) <= 30 and nxt_item and nxt_item[0] == "t":
            continue  # code caption above a code block
        if arial and any("weightedFontFamily" not in r.get("textStyle", {}) for r in rs):
            hit(hard, "runs falling back to Arial", t)
        m = LABEL.match(t)
        label_len = len(m.group(0)) if m else 0
        bold = sum(len(r["content"].rstrip("\n")) for r in rs
                   if is_bold(r.get("textStyle", {})) and not has_bg(r.get("textStyle", {})))
        if bold > label_len + 2:
            hit(hard, "bold past label", t)
        before = ""
        for r in rs:
            c = r["content"].strip()
            s = r.get("textStyle", {})
            runnable = COMMAND.search(" " + c) or (" " in c and re.search(r"\s--?\w", c))
            # a command the reader is told to run: after an Action label or a colon
            placed_to_run = (m and m.group(1).lower().startswith(("action", "next action", "run"))) \
                or before.rstrip().endswith(":")
            if is_mono(s) and runnable and placed_to_run:
                hit(hard, "commands outside code blocks (inline)", c)
            before += r["content"]
        plain = "".join(r["content"] for r in rs if not is_mono(r.get("textStyle", {})))
        if COMMAND.search(" " + plain):
            hit(hard, "commands outside code blocks (plain text)", t)
        for ident in IDENT.findall(plain):
            hit(adv, "identifiers not in inline code", ident if isinstance(ident, str) else t)
        nxt_real = next((x for x in seq[i + 1:] if not (x[0] == "p" and not text(x[1]).strip())), None)
        leads_list = t.rstrip().endswith(":") and nxt_real is not None and (
            nxt_real[0] == "t" or nxt_real[1].get("bullet"))
        if CALLOUT_WORDS.match(t) and not p.get("bullet") and not leads_list:
            hit(hard, "callout sentences left as paragraphs", t)
        # a lead-in that ends with a colon must be followed by a list item or a table
        bare_names = False
        if leads_list and nxt_real[0] == "p":
            j = seq.index(nxt_real, i + 1)
            items = []
            while j < len(seq) and is_item(seq[j]):
                items.append(text(seq[j][1]))
                j += 1
            bare_names = bool(items) and sum(len(x.split()) <= 2 for x in items) >= 0.8 * len(items)
        if leads_list and nxt_real[0] == "p" and FIELDS.search(t) and not bare_names:
            hit(adv, "field lists that should be schema tables", t)
        if t.rstrip().endswith(":") and not p.get("bullet"):
            nxt = next((x for x in seq[i + 1:] if not (x[0] == "p" and not text(x[1]).strip())), None)
            ok = nxt is not None and (nxt[0] == "t" or nxt[1].get("bullet"))
            if not ok:
                hit(hard, "lead-in followed by loose paragraphs", t)
        if t.rstrip().endswith(":") and not p.get("bullet"):
            j = next((n for n in range(i + 1, len(seq)) if not (seq[n][0] == "p" and not text(seq[n][1]).strip())), None)
            if j is not None and is_item(seq[j]) and not is_item(real(j + 1)):
                hit(hard, "one-item lists after a lead-in", t + " | " + text(seq[j][1]))
        if not p.get("bullet") and t[:1].islower() and is_item(prev_real(i)):
            hit(hard, "sentences split across a list", t)
        if t.count("\u2192") + t.count("->") >= 2:
            hit(hard, "arrow chains in paragraphs", t)
        nxt_p = real(i + 1)
        if not p.get("bullet") and not m and len(t.split()) <= 3 and not re.search(r"[.!?:]$", t.strip()) \
                and nxt_p is not None and nxt_p[0] == "p" and not nxt_p[1].get("bullet"):
            hit(hard, "labels split from their values", t + " | " + text(nxt_p[1]))
        if m and not p.get("bullet") and m.group(1).lower() not in RUN_IN:
            value = t[len(m.group(0)):].strip()
            if value and len(value.split()) <= 6:
                hit(hard, "settings outside a list", t)
        if not m and not p.get("bullet") and len(t) < 50 and not re.search(r"[.!?]$", t) \
                and i > 0 and seq[i - 1][0] == "p" and text(seq[i - 1][1]).rstrip().endswith(":"):
            hit(adv, "short fragments after a lead-in", t)

    return report(tables, hard, adv, ex)


if __name__ == "__main__":
    args = sys.argv[1:]
    tab = args[args.index("--tab") + 1] if "--tab" in args else None
    if args[0].lower().endswith((".md", ".markdown")) or not open(args[0], encoding="utf-8").read(1) in "{[":
        sys.exit(main_markdown(args[0]))
    sys.exit(main(args[0], tab))
