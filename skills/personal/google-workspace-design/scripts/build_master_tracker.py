"""Generate the master tracker: cell values per tab and one formatting batch.

Usage: python build_tracker.py OUTDIR
Writes OUTDIR/values_<Tab>.json (for update_formulas) and OUTDIR/format.json
(requests for update_spreadsheet). Send format.json first (in batches of about
60 requests), then the values; version columns are pre-formatted as text. Run against a new blank Google Sheet whose
first tab is Sheet1 (sheetId 0). Values mirror references/palette.md and references/sheets-spec.md.
"""
import json
import os
import sys

PAL = {
    "ink": "1B2A41", "teal": "0B7A75", "teal_t": "EDF6F5", "body": "24303F",
    "meta": "5F6B7A", "gray_t": "EEF1F4", "note": "1D5FBF", "note_t": "EAF2FD",
    "tip": "276E2B", "tip_t": "EAF5EA", "warn": "9A5B00", "warn_t": "FFF4DE",
    "risk": "B3261E", "risk_t": "FDECEA", "dec": "6B3FA0", "dec_t": "F2ECFA",
    "band": "F4F7F9", "border": "D5DBE1", "white": "FFFFFF",
}
HEAD, BODY, MONO = "Poppins", "Source Sans 3", "JetBrains Mono"
IDS = {"Overview": 0, "Tasks": 1, "Decisions": 2, "Change Log": 3, "References": 4}
TAB_COLOR = {"Overview": "ink", "Tasks": "teal", "Decisions": "dec",
             "Change Log": "meta", "References": "note"}

# status -> (text color, fill, extra text format)
STATUS = {
    "Not Started": ("meta", "gray_t", {}), "In Progress": ("note", "note_t", {}),
    "Blocked": ("risk", "risk_t", {}), "In Review": ("teal", "teal_t", {}),
    "Done": ("tip", "tip_t", {}), "Deferred": ("meta", "gray_t", {"italic": True}),
    "Cancelled": ("meta", "gray_t", {"strikethrough": True}),
}
GATE = {"Not Started": STATUS["Not Started"], "In Progress": STATUS["In Progress"],
        "Blocked": STATUS["Blocked"], "Accepted": ("tip", "tip_t", {})}
DECISION = {"Proposed": ("warn", "warn_t", {}), "Accepted": ("tip", "tip_t", {}),
            "Superseded": ("meta", "gray_t", {"strikethrough": True})}
PRIORITY = {"Critical": "risk", "High": "warn", "Medium": None, "Low": "meta"}


def rgb(k):
    h = PAL[k]
    return {"red": round(int(h[0:2], 16) / 255, 3), "green": round(int(h[2:4], 16) / 255, 3),
            "blue": round(int(h[4:6], 16) / 255, 3)}


def cs(k):
    return {"rgbColor": rgb(k)}


def gr(tab, r0, r1=None, c0=0, c1=None):
    """Grid range from 0-based rows/cols; None leaves the end open."""
    g = {"sheetId": IDS[tab], "startRowIndex": r0, "startColumnIndex": c0}
    if r1 is not None:
        g["endRowIndex"] = r1
    if c1 is not None:
        g["endColumnIndex"] = c1
    return g


def fmt(tab, r0, r1, c0, c1, font=None, size=None, fg=None, bg=None, bold=None,
        italic=None, halign=None, valign=None, wrap=None, number=None):
    f, fields = {}, []
    tf = {}
    if font:
        tf["fontFamily"] = font; fields.append("userEnteredFormat.textFormat.fontFamily")
    if size:
        tf["fontSize"] = size; fields.append("userEnteredFormat.textFormat.fontSize")
    if fg:
        tf["foregroundColorStyle"] = cs(fg)
        fields.append("userEnteredFormat.textFormat.foregroundColorStyle")
    if bold is not None:
        tf["bold"] = bold; fields.append("userEnteredFormat.textFormat.bold")
    if italic is not None:
        tf["italic"] = italic; fields.append("userEnteredFormat.textFormat.italic")
    if tf:
        f["textFormat"] = tf
    if bg:
        f["backgroundColorStyle"] = cs(bg); fields.append("userEnteredFormat.backgroundColorStyle")
    if halign:
        f["horizontalAlignment"] = halign; fields.append("userEnteredFormat.horizontalAlignment")
    if valign:
        f["verticalAlignment"] = valign; fields.append("userEnteredFormat.verticalAlignment")
    if wrap:
        f["wrapStrategy"] = wrap; fields.append("userEnteredFormat.wrapStrategy")
    if number:
        f["numberFormat"] = number; fields.append("userEnteredFormat.numberFormat")
    return {"repeatCell": {"range": gr(tab, r0, r1, c0, c1), "cell": {"userEnteredFormat": f},
                           "fields": ",".join(fields)}}


def border(color, style="SOLID"):
    return {"style": style, "colorStyle": cs(color)}


def widths(tab, px):
    """One request per run of equal widths."""
    out, i = [], 0
    while i < len(px):
        j = i
        while j + 1 < len(px) and px[j + 1] == px[i]:
            j += 1
        out.append({"updateDimensionProperties": {
            "range": {"sheetId": IDS[tab], "dimension": "COLUMNS", "startIndex": i, "endIndex": j + 1},
            "properties": {"pixelSize": px[i]}, "fields": "pixelSize"}})
        i = j + 1
    return out


def height(tab, row, px):
    return {"updateDimensionProperties": {
        "range": {"sheetId": IDS[tab], "dimension": "ROWS", "startIndex": row, "endIndex": row + 1},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}}


def merge(tab, r0, r1, c0, c1):
    """Merge each row of the range across its columns."""
    return {"mergeCells": {"range": gr(tab, r0, r1, c0, c1), "mergeType": "MERGE_ROWS"}}


def chip_rules(tab, ranges, mapping):
    out = []
    for word, (fg, bg, extra) in mapping.items():
        tf = {"foregroundColorStyle": cs(fg), "bold": True, **extra}
        out.append({"addConditionalFormatRule": {"index": 0, "rule": {
            "ranges": ranges,
            "booleanRule": {"condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": word}]},
                            "format": {"backgroundColorStyle": cs(bg), "textFormat": tf}}}}})
    return out


def dropdown(rng, words):
    return {"setDataValidation": {"range": rng, "rule": {
        "condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": w} for w in words]},
        "strict": True, "showCustomUi": True}}}


DATE = {"type": "DATE", "pattern": "mmm d, yyyy"}

# ---------- sample content ----------
TASK_HEAD = ["Task ID", "Phase", "Workstream", "Task / Deliverable", "Plan References",
             "Priority", "Status", "Owner", "Dependencies", "Acceptance / Definition of Done",
             "Target Date", "Evidence / Result", "Blocker / Notes", "Last Updated", "Next Action"]
TASKS = [
    ["TASK-001", "P1", "Storage", "Create the encrypted offsite bucket", "FR-001, ADR-002",
     "Critical", "Done", "Greg Tate", "", "Bucket exists with encryption at rest and access limited to the backup identity",
     "11/14/2026", "Encryption setting verified in the provider console on Nov 14, 2026", "", "11/14/2026", ""],
    ["TASK-002", "P1", "Network", "Measure upload bandwidth to the offsite target", "FR-002",
     "High", "Done", "Greg Tate", "", "Sustained upload of at least 20 Mbps", "11/15/2026",
     "Three test runs averaged 38 Mbps on Nov 15, 2026", "", "11/15/2026", ""],
    ["TASK-003", "P1", "Security", "Create a least-privilege backup service identity", "ADR-002",
     "High", "Done", "Greg Tate", "TASK-001", "Identity can read and write the bucket and nothing else",
     "11/16/2026", "Policy test passed on Nov 16, 2026", "", "11/16/2026", ""],
    ["TASK-004", "P2", "Backup jobs", "Schedule the nightly photo sync", "FR-003",
     "High", "In Progress", "Greg Tate", "TASK-003", "Seven consecutive nightly runs succeed",
     "11/30/2026", "Three of seven runs succeeded as of Nov 24, 2026", "", "11/24/2026",
     "Check run logs daily through Nov 30"],
    ["TASK-005", "P2", "Backup jobs", "Upload weekly VM images", "FR-004, ADR-003",
     "Medium", "Blocked", "Greg Tate", "TASK-003", "Two weekly uploads finish inside the overnight window",
     "12/7/2026", "", "Waiting on the upload cap decision (ADR-003)", "11/24/2026", "Decide the upload cap"],
    ["TASK-006", "P2", "Validation", "Restore test from the offsite copy", "T-001",
     "Critical", "In Review", "Greg Tate", "TASK-004", "Restored photo set matches source checksums",
     "12/1/2026", "Restored 500 files on Nov 23, 2026; checksum report under review", "", "11/23/2026",
     "Review the checksum report"],
    ["TASK-007", "P3", "Cutover", "Retire the USB copy job", "FR-005",
     "Low", "Not Started", "TBD", "TASK-006", "Old scheduled task disabled and removed", "12/10/2026",
     "", "", "", "Start after TASK-006 is Done"],
    ["TASK-008", "P3", "Operations", "Document the restore procedure", "FR-006",
     "Medium", "In Progress", "Greg Tate", "TASK-006", "Runbook covers full and single-file restores",
     "12/12/2026", "Outline drafted on Nov 22, 2026", "", "11/22/2026", "Add single-file restore steps"],
]
DEC_HEAD = ["Decision ID", "State", "Decision", "Rationale / Impact", "Plan Reference", "Last Updated"]
DECS = [
    ["ADR-001", "Superseded", "Use two offsite providers",
     "Superseded by ADR-002: a second provider doubled the cost for little added protection", "Design decisions", "11/12/2026"],
    ["ADR-002", "Accepted", "Use one encrypted offsite bucket for all backup sets",
     "One access policy and one restore path; cost is about the same", "Design decisions", "11/14/2026"],
    ["ADR-003", "Proposed", "Cap weekly VM uploads at 200 GB",
     "Keeps uploads inside the overnight window; needs the ISP data cap confirmed", "Phase 2", "11/24/2026"],
]
LOG_HEAD = ["Date", "Tracker Version", "Plan Version", "Affected IDs", "Change", "Rationale",
            "Companion Impact", "Author"]
LOG = [
    ["11/14/2026", "1.0", "1.0", "TASK-001 to TASK-008", "Created the tracker from the implementation plan",
     "Initial baseline", "None", "Greg Tate"],
    ["11/24/2026", "1.1", "1.2", "TASK-005, ADR-003", "Marked TASK-005 Blocked pending the upload cap decision",
     "The ISP data cap is unknown", "Plan 1.2 adds ADR-003", "Greg Tate"],
]
REF_HEAD = ["Source", "URL / Locator", "Supports"]
REFS = [
    ["Implementation plan, version 1.2", "Home lab backup redesign - Implementation plan v1.2.docx",
     "Scope, design decisions, phases, and acceptance criteria"],
    ["rclone documentation", "https://rclone.org/docs/", "Sync options used by TASK-004"],
    ["Restore checksum report, Nov 23, 2026", "Backups/Reports/restore-checksums-2026-11-23.csv",
     "Evidence for TASK-006"],
]
STATUS_DEF = {
    "Not Started": "No work has begun",
    "In Progress": "Work has started and is not yet ready for review",
    "Blocked": "Cannot continue until the blocker in Notes is resolved",
    "In Review": "Work is complete and its evidence is being checked",
    "Done": "Acceptance criterion met, with dated evidence",
    "Deferred": "Postponed; excluded from the completion percentage",
    "Cancelled": "No longer needed; excluded from the completion percentage",
}
GATES = [["P1", "Offsite target reachable, encrypted, and access-controlled", "Accepted"],
         ["P2", "Nightly and weekly jobs succeed and a restore test passes", "In Progress"],
         ["P3", "USB job retired and the restore runbook approved", "Not Started"]]


def overview_values():
    v = [[None] * 6 for _ in range(27)]
    v[0][0] = "Home lab backup redesign"
    v[1][0] = "Task tracker"
    v[2][0] = ("Plan: Implementation plan v1.2  |  Tracker v1.1  |  As of Nov 25, 2026")
    v[4] = ["Tasks", "Active", "Done", "In Progress", "Blocked", "Complete"]
    v[5] = ["=COUNTA(Tasks!A2:A)", "=A6-B15-B16", "=B14", "=B11", "=B12", "=IF(B6=0,0,C6/B6)"]
    v[7][0] = "Status"
    v[8] = ["Status", "Tasks", "Definition", None, None, None]
    for i, (s, d) in enumerate(STATUS_DEF.items()):
        v[9 + i] = [s, f"=COUNTIF(Tasks!$G$2:$G,A{10 + i})", d, None, None, None]
    v[17][0] = "Phase gates"
    v[18] = ["Phase", "Exit gate", None, "Gate status", "Tasks done", "Tasks in phase"]
    for i, (p, g, s) in enumerate(GATES):
        r = 20 + i
        v[19 + i] = [p, g, None, s, f"=COUNTIFS(Tasks!$B$2:$B,$A{r},Tasks!$G$2:$G,\"Done\")",
                     f"=COUNTIF(Tasks!$B$2:$B,$A{r})"]
    v[23][0] = "Current focus"
    v[24] = ["Focus", "Finish Phase 2: nightly sync reliability and the restore test", None, None, None, None]
    v[25] = ["Next action", "Review the TASK-006 checksum report", None, None, None, None]
    v[26] = ["Blocker", "TASK-005 waits on the upload cap decision (ADR-003)", None, None, None, None]
    return v


def data_tab(tab, head, rows, px, id_col=0, wrap_cols=(), date_cols=(), text_cols=()):
    n = len(head)
    R = []
    R.append({"updateSheetProperties": {"properties": {
        "sheetId": IDS[tab], "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": 1 if tab == "Tasks" else 0,
                                                "hideGridlines": True},
        "tabColorStyle": cs(TAB_COLOR[tab])},
        "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount,gridProperties.hideGridlines,tabColorStyle"}})
    R.append(fmt(tab, 0, None, 0, None, font=BODY, size=10, fg="body", valign="TOP", wrap="CLIP"))
    R.append(fmt(tab, 0, 1, 0, n, bold=True, fg="white", valign="MIDDLE", wrap="WRAP"))
    if id_col is not None:
        R.append(fmt(tab, 1, None, id_col, id_col + 1, font=MONO, bold=True, fg="ink"))
    for c in wrap_cols:
        R.append(fmt(tab, 1, None, c, c + 1, wrap="WRAP"))  # one per column; few requests
    for c in date_cols:
        R.append(fmt(tab, 1, None, c, c + 1, number=DATE))
    for c in text_cols:
        R.append(fmt(tab, 1, None, c, c + 1, number={"type": "TEXT"}))
    R.append({"addBanding": {"bandedRange": {"range": gr(tab, 0, 1000, 0, n), "rowProperties": {
        "headerColorStyle": cs("ink"), "firstBandColorStyle": cs("white"),
        "secondBandColorStyle": cs("band")}}}})
    R.append({"updateBorders": {"range": gr(tab, 1, 1000, 0, n),
                                "innerHorizontal": border("border"), "bottom": border("border")}})
    R.append({"setBasicFilter": {"filter": {"range": gr(tab, 0, None, 0, n)}}})
    R += widths(tab, px)
    R.append(height(tab, 0, 32))
    return R


def overview_format():
    t = "Overview"
    R = [{"updateSheetProperties": {"properties": {
        "sheetId": 0, "title": "Overview", "gridProperties": {"hideGridlines": True},
        "tabColorStyle": cs("ink")}, "fields": "title,gridProperties.hideGridlines,tabColorStyle"}}]
    R.append(fmt(t, 0, None, 0, None, font=BODY, size=10, fg="body", valign="MIDDLE", wrap="CLIP"))
    R += widths(t, [120, 120, 120, 120, 120, 120])
    # title block
    R.append(fmt(t, 0, 1, 0, 1, font=HEAD, size=20, bold=True, fg="ink"))
    R.append(fmt(t, 1, 2, 0, 1, size=12, fg="meta"))
    R.append(fmt(t, 2, 3, 0, 1, size=10, fg="meta"))
    R.append({"updateBorders": {"range": gr(t, 2, 3, 0, 6), "bottom": border("teal", "SOLID_MEDIUM")}})
    for row, px in ((0, 40), (1, 22), (2, 24), (3, 10), (4, 22), (5, 38), (6, 14), (16, 14), (22, 14)):
        R.append(height(t, row, px))
    # tiles
    R.append(fmt(t, 4, 6, 0, 6, bg="band"))
    R.append(fmt(t, 4, 5, 0, 6, size=9, fg="meta", valign="BOTTOM"))
    R.append(fmt(t, 5, 6, 0, 6, font=HEAD, size=18, bold=True, fg="ink", valign="TOP"))
    for c, col in ((2, "tip"), (3, "note"), (4, "risk")):
        R.append(fmt(t, 5, 6, c, c + 1, fg=col))
    R.append(fmt(t, 5, 6, 5, 6, number={"type": "PERCENT", "pattern": "0%"}))
    R.append({"updateBorders": {"range": gr(t, 4, 6, 0, 6), "innerVertical": border("white", "SOLID_THICK")}})
    # section headings
    for row in (7, 17, 23):
        R.append(fmt(t, row, row + 1, 0, 1, font=HEAD, size=12, bold=True, fg="teal", valign="BOTTOM"))
    # status table rows 9-16 (0-based 8..15)
    R.append(fmt(t, 8, 9, 0, 6, bg="ink", fg="white", bold=True))
    R.append(merge(t, 8, 16, 2, 6))
    R.append(fmt(t, 9, 16, 0, 2, halign="CENTER"))
    R.append(fmt(t, 8, 9, 1, 2, halign="CENTER"))
    R.append({"updateBorders": {"range": gr(t, 9, 16, 0, 6), "innerHorizontal": border("border"),
                                "bottom": border("border")}})
    # phase gates rows 19-22 (0-based 18..21)
    R.append(fmt(t, 18, 19, 0, 6, bg="ink", fg="white", bold=True))
    R.append(merge(t, 18, 22, 1, 3))
    R.append(fmt(t, 19, 22, 0, 1, font=MONO, bold=True, fg="ink"))
    R.append(fmt(t, 19, 22, 3, 4, halign="CENTER"))
    R.append(fmt(t, 18, 22, 4, 6, halign="CENTER"))
    R.append({"updateBorders": {"range": gr(t, 19, 22, 0, 6), "innerHorizontal": border("border"),
                                "bottom": border("border")}})
    R.append(dropdown(gr(t, 19, 22, 3, 4), list(GATE)))
    R += chip_rules(t, [gr(t, 19, 22, 3, 4)], GATE)
    R += chip_rules(t, [gr(t, 9, 16, 0, 1)], STATUS)
    # focus callouts rows 25-27 (0-based 24..26)
    R.append(merge(t, 24, 27, 1, 6))
    for r, (fg, bg) in zip(range(24, 27), (("note", "note_t"), ("tip", "tip_t"), ("risk", "risk_t"))):
        R.append(fmt(t, r, r + 1, 0, 6, bg=bg, wrap="WRAP"))
        R.append(fmt(t, r, r + 1, 0, 1, fg=fg, bold=True))
        R.append({"updateBorders": {"range": gr(t, r, r + 1, 0, 1), "left": border(fg, "SOLID_THICK")}})
        R.append(height(t, r, 28))
    R.append({"updateBorders": {"range": gr(t, 24, 27, 0, 6), "innerHorizontal": border("white", "SOLID_MEDIUM")}})
    return R


def main(out):
    os.makedirs(out, exist_ok=True)
    reqs = [{"addSheet": {"properties": {"sheetId": IDS[t], "title": t, "index": IDS[t]}}}
            for t in ("Tasks", "Decisions", "Change Log", "References")]
    reqs += overview_format()
    reqs += data_tab("Tasks", TASK_HEAD, TASKS,
                     [96, 58, 104, 240, 116, 80, 104, 96, 104, 260, 96, 240, 200, 96, 200],
                     wrap_cols=(3, 9, 11, 12, 14), date_cols=(10, 13))
    reqs.append(dropdown(gr("Tasks", 1, None, 5, 6), list(PRIORITY)))
    reqs.append(dropdown(gr("Tasks", 1, None, 6, 7), list(STATUS)))
    reqs.append(fmt("Tasks", 1, None, 6, 7, halign="CENTER"))
    reqs += chip_rules("Tasks", [gr("Tasks", 1, None, 6, 7)], STATUS)
    for word, col in PRIORITY.items():
        if col:
            reqs.append({"addConditionalFormatRule": {"index": 0, "rule": {
                "ranges": [gr("Tasks", 1, None, 5, 6)], "booleanRule": {
                    "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": word}]},
                    "format": {"textFormat": {"foregroundColorStyle": cs(col), "bold": col != "meta"}}}}}})
    reqs += data_tab("Decisions", DEC_HEAD, DECS, [104, 104, 300, 360, 140, 104],
                     wrap_cols=(2, 3), date_cols=(5,))
    reqs.append(dropdown(gr("Decisions", 1, None, 1, 2), list(DECISION)))
    reqs.append(fmt("Decisions", 1, None, 1, 2, halign="CENTER"))
    reqs += chip_rules("Decisions", [gr("Decisions", 1, None, 1, 2)], DECISION)
    reqs += data_tab("Change Log", LOG_HEAD, LOG, [104, 96, 96, 150, 300, 240, 200, 110],
                     id_col=3, wrap_cols=(4, 5, 6), date_cols=(0,), text_cols=(1, 2))
    reqs += data_tab("References", REF_HEAD, REFS, [260, 340, 320], id_col=None, wrap_cols=(0, 1, 2))
    reqs.append(fmt("References", 1, None, 1, 2, fg="note"))
    json.dump(reqs, open(f"{out}/format.json", "w"), separators=(",", ":"))
    tabs = {"Overview": overview_values(), "Tasks": [TASK_HEAD] + TASKS,
            "Decisions": [DEC_HEAD] + DECS, "Change Log": [LOG_HEAD] + LOG,
            "References": [REF_HEAD] + REFS}
    for t, v in tabs.items():
        json.dump(v, open(f"{out}/values_{t.replace(' ', '_')}.json", "w"), ensure_ascii=False)
    print(f"requests={len(reqs)} bytes={len(json.dumps(reqs, separators=(',', ':')))}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tracker_out")
