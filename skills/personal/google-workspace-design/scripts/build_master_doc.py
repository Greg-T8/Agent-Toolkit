"""Generate Docs API batchUpdate requests that build the master Doc.

Usage: python build_master.py > requests.json

Run against a blank Google Doc (body = one empty paragraph). Content is
appended forward, so each index computed at insert time is also its final
index. Values mirror references/palette.md and references/docs-spec.md; change the spec first, then
this script, then rebuild the master Doc.

Order: structure, then every paragraph style, then one base text style over
the body, then text and cell overrides, then bullets. Paragraph styles come
before any text style because setting a named style clears direct text
formatting (spec rule 6.3).
"""
import json
import sys

PAL = {
    "ink": "1B2A41", "teal": "0B7A75", "body": "24303F", "meta": "5F6B7A",
    "note": "1D5FBF", "note_t": "EAF2FD", "tip": "276E2B", "tip_t": "EAF5EA",
    "warn": "9A5B00", "warn_t": "FFF4DE", "risk": "B3261E", "risk_t": "FDECEA",
    "dec": "6B3FA0", "dec_t": "F2ECFA", "teal_t": "EDF6F5", "code_bg": "F1F3F5", "band": "F4F7F9",
    "border": "D5DBE1", "white": "FFFFFF",
}
HEAD, BODY, MONO = "Poppins", "Source Sans 3", "JetBrains Mono"
NBSP = " "


def color(key):
    h = PAL[key]
    return {"color": {"rgbColor": {k: round(int(h[i:i + 2], 16) / 255, 3)
                                   for k, i in (("red", 0), ("green", 2), ("blue", 4))}}}


def pt(v):
    return {"magnitude": v, "unit": "PT"}


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def ts(font=None, weight=None, size=None, fg=None, bg=None, bold=None, link=None,
       underline=None):
    """Text style override with a matching field mask (only what is given)."""
    st, f = {}, []
    if font or weight:
        st["weightedFontFamily"] = {"fontFamily": font or BODY, "weight": weight or 400}
        f.append("weightedFontFamily")
    if size:
        st["fontSize"] = pt(size); f.append("fontSize")
    if fg:
        st["foregroundColor"] = color(fg); f.append("foregroundColor")
    if bg:
        st["backgroundColor"] = color(bg); f.append("backgroundColor")
    if bold is not None:
        st["bold"] = bold; f.append("bold")
    if link:
        st["link"] = {"url": link}; f.append("link")
    if underline:
        st["underline"] = True; f.append("underline")
    return st, ",".join(f)


PF = "namedStyleType,spaceAbove,spaceBelow,keepWithNext,lineSpacing"
STYLES = {  # named style, text override, paragraph style
    "title": ("TITLE", dict(font=HEAD, weight=600, size=26, fg="ink"), dict(spaceBelow=pt(2))),
    "subtitle": ("SUBTITLE", dict(size=14, fg="meta"), dict(spaceBelow=pt(6))),
    "h1": ("HEADING_1", dict(font=HEAD, weight=600, size=18, fg="ink"),
           dict(spaceAbove=pt(20), spaceBelow=pt(6), keepWithNext=True)),
    "h2": ("HEADING_2", dict(font=HEAD, weight=600, size=14, fg="teal"),
           dict(spaceAbove=pt(16), spaceBelow=pt(4), keepWithNext=True)),
    "h3": ("HEADING_3", dict(weight=700, size=12, fg="ink", bold=True),
           dict(spaceAbove=pt(12), spaceBelow=pt(4), keepWithNext=True)),
    "h4": ("HEADING_4", dict(weight=700, fg="meta", bold=True),
           dict(spaceAbove=pt(10), spaceBelow=pt(2), keepWithNext=True)),
    "body": ("NORMAL_TEXT", {}, dict(spaceBelow=pt(8))),
    "item": ("NORMAL_TEXT", {}, dict(spaceBelow=pt(4))),
    "caption": ("NORMAL_TEXT", dict(weight=700, size=8.5, fg="meta", bold=True),
                dict(spaceAbove=pt(6), spaceBelow=pt(2), keepWithNext=True)),
    "meta": ("NORMAL_TEXT", dict(size=10, fg="meta"), dict(spaceBelow=pt(14))),
}
CHIPS = {"APPROVED": ("tip", "tip_t"), "DONE": ("tip", "tip_t"),
         "IN PROGRESS": ("note", "note_t"), "IN REVIEW": ("teal", "teal_t"),
         "DRAFT": ("warn", "warn_t"), "BLOCKED": ("risk", "risk_t")}


def chip_ts(word):
    fg, bg = CHIPS[word]
    return dict(weight=700, bold=True, size=9, fg=fg, bg=bg)


class B:
    def __init__(self):
        self.struct, self.pst, self.style, self.late = [], [], [], []
        self.cur, self.prev_table, self.extras = 1, False, 0

    def text(self, s, n, **kw):
        if n:
            st, f = ts(**kw)
            if f:
                self.style.append({"updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": s + n}, "textStyle": st, "fields": f}})

    def pstyle(self, s, e, named, extra, fields=PF):
        ps = dict(extra); ps["namedStyleType"] = named
        self.pst.append({"updateParagraphStyle": {
            "range": {"startIndex": s, "endIndex": max(e - 1, s + 1)},
            "paragraphStyle": ps, "fields": fields}})

    def para(self, kind, runs, bullet=None):
        runs = [(runs, {})] if isinstance(runs, str) else runs
        named, base, pst = STYLES[kind]
        txt = "".join(r[0] for r in runs)
        s = self.cur
        self.struct.append({"insertText": {"location": {"index": s}, "text": txt + "\n"}})
        e = s + u16(txt) + 1
        self.pstyle(s, e, named, pst)
        if kind == "meta":
            self.pst.append({"updateParagraphStyle": {
                "range": {"startIndex": s, "endIndex": e - 1},
                "paragraphStyle": {"borderBottom": {"color": color("teal"), "width": pt(2),
                                                    "padding": pt(6), "dashStyle": "SOLID"}},
                "fields": "borderBottom"}})
        pos = s
        for t, ov in runs:
            self.text(pos, u16(t), **{**base, **ov})
            pos += u16(t)
        if bullet:
            self.late.append({"createParagraphBullets": {
                "range": {"startIndex": s, "endIndex": e - 1}, "bulletPreset": bullet}})
        self.cur, self.prev_table = e, False

    def table(self, rows, widths, cb):
        R, C = len(rows), len(rows[0])
        if self.prev_table:
            i, spacer = self.cur, self.cur
        else:
            i, spacer = self.cur - 1, None
            self.extras += 1
        self.struct.append({"insertTable": {"rows": R, "columns": C, "location": {"index": i}}})
        for r in reversed(range(R)):
            for c in reversed(range(C)):
                if rows[r][c]:
                    self.struct.append({"insertText": {"location": {
                        "index": i + 4 + r * (2 * C + 1) + 2 * c}, "text": rows[r][c]}})
        t = i + 1
        idx, cells = t + 1, {}
        for r in range(R):
            idx += 1
            for c in range(C):
                idx += 1
                cs = idx
                idx += u16(rows[r][c]) + 1
                cells[(r, c)] = (cs, idx)
        first, last = cells[(0, 0)][0], idx
        # every cell paragraph: tight Normal text
        self.pst.append({"updateParagraphStyle": {
            "range": {"startIndex": first, "endIndex": last - 1},
            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT", "spaceBelow": pt(0),
                               "spaceAbove": pt(0), "lineSpacing": 115},
            "fields": PF}})
        for c, w in enumerate(widths):
            self.style.append({"updateTableColumnProperties": {
                "tableStartLocation": {"index": t}, "columnIndices": [c],
                "tableColumnProperties": {"widthType": "FIXED_WIDTH", "width": pt(w)},
                "fields": "widthType,width"}})
        cb(self, t, R, C, cells, rows)
        if spacer is not None:
            self.pstyle(spacer, spacer + 1, "NORMAL_TEXT", dict(spaceBelow=pt(0)))
            self.text(spacer, 1, size=6)
        self.cur, self.prev_table = idx + 1, True

    def cells(self, t, r, c, rs, cs, bg, left=None, border=None, pad=(5, 7)):
        if border:
            b = {"color": color(border), "width": pt(0.75), "dashStyle": "SOLID"}
        else:
            b = {"color": color(bg), "width": pt(0), "dashStyle": "SOLID"}
        st = {"backgroundColor": color(bg), "borderTop": b, "borderRight": b,
              "borderBottom": b,
              "borderLeft": {"color": color(left[0]), "width": pt(left[1]),
                             "dashStyle": "SOLID"} if left else b,
              "paddingTop": pt(pad[0]), "paddingBottom": pt(pad[0]),
              "paddingLeft": pt(pad[1]), "paddingRight": pt(pad[1])}
        self.style.append({"updateTableCellStyle": {
            "tableRange": {"tableCellLocation": {"tableStartLocation": {"index": t},
                                                 "rowIndex": r, "columnIndex": c},
                           "rowSpan": rs, "columnSpan": cs},
            "tableCellStyle": st,
            "fields": "backgroundColor,borderTop,borderRight,borderBottom,borderLeft,"
                      "paddingTop,paddingBottom,paddingLeft,paddingRight"}})

    def done(self):
        if self.extras:
            self.struct.append({"deleteContentRange": {"range": {
                "startIndex": self.cur, "endIndex": self.cur + self.extras}}})
        st, f = ts(font=BODY, weight=400, size=11, fg="body", bold=False)
        base = {"updateTextStyle": {"range": {"startIndex": 1, "endIndex": self.cur},
                                    "textStyle": st, "fields": f}}
        return self.struct + self.pst + [base] + self.style + self.late


def callout(b, label, body, accent, tint):
    content = f"{label}  {body}"

    def cb(b, t, R, C, cells, rows):
        s, _ = cells[(0, 0)]
        b.cells(t, 0, 0, 1, 1, tint, left=(accent, 4), pad=(7, 11))
        b.text(s, u16(label), weight=700, bold=True, fg=accent)
    b.table([[content]], [468], cb)


def code(b, lines):
    content = "\n".join(lines)

    def cb(b, t, R, C, cells, rows):
        s, e = cells[(0, 0)]
        b.cells(t, 0, 0, 1, 1, "code_bg", left=("teal", 3), pad=(7, 11))
        b.pst.append({"updateParagraphStyle": {
            "range": {"startIndex": s, "endIndex": e - 1},
            "paragraphStyle": {"lineSpacing": 100}, "fields": "lineSpacing"}})
        b.text(s, u16(content), font=MONO, size=9.5)
    b.table([[content]], [468], cb)


def data_table(b, rows, widths):
    def cb(b, t, R, C, cells, rows):
        b.cells(t, 0, 0, R, C, "white", border="border", pad=(4, 7))
        b.cells(t, 0, 0, 1, C, "ink", border="border", pad=(4, 7))
        for r in range(2, R, 2):
            b.cells(t, r, 0, 1, C, "band", border="border", pad=(4, 7))
        b.text(cells[(0, 0)][0], cells[(R - 1, C - 1)][1] - 1 - cells[(0, 0)][0], size=10)
        b.text(cells[(0, 0)][0], cells[(0, C - 1)][1] - 1 - cells[(0, 0)][0],
               weight=700, bold=True, fg="white")
        for r in range(1, R):
            s, e = cells[(r, 0)]
            b.text(s, e - 1 - s, weight=600)
            for c in range(1, C):
                v = rows[r][c].strip(NBSP)
                if v in CHIPS:
                    s, e = cells[(r, c)]
                    b.text(s, e - 1 - s, **chip_ts(v))
        b.late.append({"pinTableHeaderRows": {"tableStartLocation": {"index": t},
                                              "pinnedHeaderRowsCount": 1}})
    b.table(rows, widths, cb)


def chip(word):
    return (f"{NBSP}{word}{NBSP}", chip_ts(word))


def main():
    b = B()
    b.para("title", "Personal document template")
    b.para("subtitle", "Style reference for the Agent Toolkit documentation skill")
    b.para("meta", [chip("APPROVED"),
                    ("  Version 1.0  |  Updated November 25, 2026  |  Owner: Greg Tate", {})])
    b.para("h1", "Title block")
    b.para("body", "Every document opens with a title, a subtitle that names the document "
                   "type, and a metadata line. The metadata line starts with a status chip, "
                   "then the version, date, and owner, separated by vertical bars. A 2 pt "
                   "teal rule closes the title block. There is no cover page and no table "
                   "of contents.")
    b.para("h1", "Headings and body text")
    b.para("body", "Heading 1 marks a major section. Write headings in sentence case and "
                   "never type section numbers by hand.")
    b.para("h2", "Heading 2 for subsections")
    b.para("body", [("Heading 2 is teal Poppins. Body text is Source Sans 3 at 11 pt in a "
                     "dark slate, never pure black. Links are blue and underlined, as in the ", {}),
                    ("Google developer documentation style guide",
                     dict(fg="note", link="https://developers.google.com/style", underline=True)),
                    (".", {})])
    b.para("h3", "Heading 3 for topics within a subsection")
    b.para("body", [("Heading 3 is bold body type in ink. Inline code, such as ", {}),
                    ("Get-Date", dict(font=MONO, size=10)),
                    (", uses JetBrains Mono with no fill.", {})])
    b.para("h4", "Heading 4 for short groupings")
    for t in ("Use bulleted lists for items with no required order.",
              "Keep list items parallel and short."):
        b.para("item", t, bullet="BULLET_DISC_CIRCLE_SQUARE")
    b.para("body", "Use numbered lists for steps that run in order:")
    for t in ("Start each step with a verb.", "Put the expected result after the action."):
        b.para("item", t, bullet="NUMBERED_DECIMAL_ALPHA_ROMAN")
    b.para("h1", "Callouts")
    b.para("body", "A callout is a one-cell table with a tinted fill and a 4 pt left border "
                   "in its color. The label is bold in that color and the text is body color. "
                   "Each color has one meaning, so use only the type that fits.")
    callout(b, "Note", "Background the reader should know but can skip.", "note", "note_t")
    callout(b, "Tip", "A shortcut or a better way to do the task.", "tip", "tip_t")
    callout(b, "Warning", "An action that can lose data or time. Say what to do instead.",
            "warn", "warn_t")
    callout(b, "Risk", "Something that could make the plan fail, and how it is mitigated.",
            "risk", "risk_t")
    callout(b, "Decision", "A choice that was made and the reason for it.", "dec", "dec_t")
    b.para("h1", "Tables")
    b.para("body", "Data tables have an ink header row with white bold text, banded rows, "
                   "light gray borders, and a semibold first column. Status values use chips.")
    data_table(b, [["Workload", "Frequency", "Status"],
                   ["Photos", "Nightly", f"{NBSP}DONE{NBSP}"],
                   ["VM images", "Weekly", f"{NBSP}IN PROGRESS{NBSP}"],
                   ["Offsite copy", "Weekly", f"{NBSP}DRAFT{NBSP}"],
                   ["USB copy job", "Retire", f"{NBSP}BLOCKED{NBSP}"]], [190, 120, 158])
    runs = [("Status chips: ", {})]
    for w in ("DRAFT", "IN REVIEW", "IN PROGRESS", "APPROVED", "DONE", "BLOCKED"):
        runs += [chip(w), (" ", {})]
    b.para("body", runs[:-1])
    b.para("h1", "Code")
    b.para("body", "Code goes in a one-cell table with a light gray fill and a 3 pt teal left "
                   "border, under a caption that names the shell. Keep lines under 90 "
                   "characters.")
    b.para("caption", "POWERSHELL")
    code(b, ['Get-ScheduledTask -TaskName "NightlyCopy" |', "    Disable-ScheduledTask"])
    b.para("body", "Leave one normal paragraph after every table, callout, or code block.")
    reqs = b.done()
    json.dump(reqs, sys.stdout, separators=(",", ":"), ensure_ascii=False)
    print(f"\nrequests={len(reqs)} cur={b.cur} extras={b.extras}", file=sys.stderr)


if __name__ == "__main__":
    main()
