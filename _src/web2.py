"""Web console screens 07-13: approvals, reasons, journey plans, handover, users, reports."""
from __future__ import annotations

from charts import StreetMap, donut, map_pin
from data import CLIENT, MGMT, QUARTER, SUPERVISOR, TEAM, rnd_instalment, ugx
from kit import (AMBER, AMBER_D, BLUE, BRAND, BRAND_D, CARD, FAINT, GREEN, GREEN_D, INK, INK2, LINE, LINE2, MUTED,
                 PRODUCT, PRODUCTS, RED, STAGE, STATUS, TEAL, VIOLET, YELLOW, YELLOW_D, avatar, button, card,
                 checkbox, chip, field, para, progress, radio, shade, status_chip, table, tint, toggle, tw)
from web import (CW, H, W, X0, X1, Y0, agent_cell, chip_cell, doc_thumb, filter_btn, kpi, kv, page_head, rule_note,
                 seg, seg_width, shell)


# =====================================================================================
QUEUE = [
    (CLIENT["app_id"], CLIENT["name"], "Sarah Namuli", "SN", "MSE Business Loan", 6_000_000, "7/7", None, "18 min", 0.02),
    ("LU-APP-2609-04811", "Agnes Babirye", "Esther Nakato", "EN", "School Fees Loan", 1_800_000, "7/7", None,
     "3 h", 0.13),
    ("LU-APP-2609-04796", "Godfrey Lubowa", "Peter Kato", "PK", "Civil Servant Loan", 9_500_000, "7/7", None, "5 h",
     0.22),
    ("LU-APP-2609-04790", "Irene Nabukenya", "Ruth Achieng", "RA", "Home Improvement Loan", 5_000_000, "6/7",
     "Title deed photo blurred", "7 h", 0.3),
    ("LU-APP-2609-04772", "Kenneth Mwesigwa", "Ivan Mugabe", "IM", "Civil Servant Loan", 11_000_000, "7/7",
     "Over branch limit: HQ", "11 h", 0.46),
    ("LU-APP-2609-04765", "Olivia Nakku", "Esther Nakato", "EN", "MSE Business Loan", 2_500_000, "7/7",
     "Instalment 49% of free income", "15 h", 0.62),
    ("LU-APP-2609-04741", "Patrick Ochieng", "Brian Ssali", "BS", "Agri Asset Loan", 4_200_000, "5/7",
     "Payslip and LC1 letter missing", "22 h", 0.92),
    ("LU-APP-2609-04733", "Stella Akech", "Peter Kato", "PK", "School Fees Loan", 1_500_000, "7/7", None, "26 h", 1.08),
]


def w07_approvals():
    s = shell("07 Approvals queue (supervisor)", "Approvals", ["Applications", "Approvals"], user=SUPERVISOR,
              period="Week")
    page_head(s, "Approvals", "Loan applications from Kampala East agents, waiting for your decision · target: decide "
                              "within 24 hours")
    with s.g("header actions"):
        x = X1
        x -= filter_btn(s, x - 170, Y0 + 13, "Product", "All", w=170) + 12
        x -= filter_btn(s, x - 160, Y0 + 13, "Agent", "All 7", w=160) + 12
        x -= seg(s, x - seg_width(["Waiting 14", "Returned 3", "Decided today 9"]), Y0 + 13,
                 ["Waiting 14", "Returned 3", "Decided today 9"], "Waiting 14", h=38) + 12
    ky = Y0 + 84
    kw = (CW - 3 * 16) / 4
    for i, (ic, col, lab, val, sub, fr) in enumerate([
            ("listcheck", BRAND, "Waiting for a decision", "14", "UGX 71.5M requested", None),
            ("clock", RED, "Oldest waiting", "26 h", "over the 24 h target: Stella Akech", None),
            ("check", GREEN, "Approved this week", "31", "of 37 decided · 84%", 31 / 37),
            ("undo", AMBER, "Returned to agents", "3", "missing or unclear documents", None)]):
        kpi(s, X0 + i * (kw + 16), ky, kw, 140, ic, col, lab, val, sub, fr)
    ty = ky + 160
    with s.g("rule banner"):
        s.rect(X0, ty, CW, 48, fill=tint(GREEN, 0.08), rx=10, stroke=tint(GREEN, 0.35))
        s.icon("info", X0 + 16, ty + 14, 20, GREEN_D, 2)
        s.text(X0 + 46, ty + 29, "These clients already count as conversions for their agents: they applied with every "
                                 "item. Your decision is recorded separately and doesn't change the agent's conversion.",
               13.5, 600, GREEN_D)
    cols = [("Application", 200, "start"), ("Client", 210, "start"), ("Agent", 210, "start"),
            ("Product", 220, "start"), ("Amount", 150, "end"), ("KYC items", 110, "start"),
            ("Flags", 250, "start"), ("Waiting", 150, "start"), ("", 92, "end")]
    rows = []
    for (aid, cl, ag, ini, prod, amt, kyc, flag, wait, fr) in QUEUE:
        rows.append([
            (lambda a: lambda s_, x, y, w, h: s_.text(x + 16, y + h / 2 + 5, a, 13, 600, BRAND))(aid),
            cl, agent_cell(ag, ini, "Kampala East"),
            (lambda p: lambda s_, x, y, w, h: chip(s_, x + 12, y + h / 2 - 11, p, PRODUCT[p], h=22, size=11))(prod),
            ugx(amt),
            (lambda k: lambda s_, x, y, w, h: (s_.icon("check" if k == "7/7" else "alert", x + 16, y + h / 2 - 8, 16,
                                                       GREEN if k == "7/7" else AMBER_D, 2.4),
                                               s_.text(x + 38, y + h / 2 + 5, k, 13, 600,
                                                       GREEN_D if k == "7/7" else AMBER_D)))(kyc),
            (lambda f: lambda s_, x, y, w, h: s_.text(x + 16, y + h / 2 + 5, f or "—", 12.5, 600 if f else 400,
                                                      (RED if "missing" in f or "blurred" in f else AMBER_D)
                                                      if f else FAINT, maxw=w - 24))(flag),
            (lambda wt, f_: lambda s_, x, y, w, h: (s_.text(x + 16, y + h / 2 - 1, wt, 13, 600,
                                                            RED if f_ > 1 else INK),
                                                    progress(s_, x + 16, y + h / 2 + 8, 100, f_,
                                                             RED if f_ > 0.8 else (AMBER if f_ > 0.5 else GREEN),
                                                             h=5)))(wait, fr),
            (lambda: lambda s_, x, y, w, h: button(s_, x + w - 12, y + h / 2 - 16, "Review", "soft", h=32, size=12.5,
                                                   anchor="end"))(),
        ])
    tby = ty + 64
    rh = (H - 28 - tby - 40 - 40) / len(rows)
    table(s, X0, tby, cols, rows, row_h=rh, head_h=40, hl=0)
    s.link(X0, tby + 40, CW, rh, "w08")
    s.text(X0 + 16, H - 44, "Showing 8 of 14 · oldest first", 13, 400, MUTED)
    s.text(X1 - 16, H - 44, "Bulk approve is off: each loan needs its own decision", 13, 400, MUTED, anchor="end")
    return s


# =====================================================================================
def w08_review():
    c = CLIENT
    s = shell("08 Application review and decision", "Approvals", ["Applications", "Approvals", c["app_id"]],
              user=SUPERVISOR, period="Week")
    with s.g("header"):
        s.text(X0, Y0 + 30, f"{c['name']} · {c['app_id']}", 26, 700, INK)
        s.text(X0, Y0 + 56, f"{c['product']} · {ugx(c['amount'])} over {c['months']} months · submitted by Sarah "
                            "Namuli today 11:42 · converted", 14, 400, MUTED)
        x = X1
        x -= button(s, x, Y0 + 12, "Client record", "secondary", icon="user", anchor="end") + 10
        s.link(x + 10, Y0 + 12, 160, 40, "w06")
        button(s, x, Y0 + 12, "Back to queue", "ghost", icon="arrowleft", anchor="end")
        s.link(x - 170, Y0 + 12, 170, 40, "w07")
    ty = Y0 + 80
    th = H - 28 - ty
    vw = 700
    card(s, X0, ty, vw, th, "Documents", "Taken in the field app · tap to zoom")
    doc_thumb(s, X0 + 24, ty + 76, vw - 48, 470, "id_front", "NIRA National ID · front · captured 30 Sep 11:17, "
                                                             "Kiwatule (±9 m)")
    tw_ = (vw - 48 - 5 * 10) / 6
    for i, (k, lab) in enumerate([("id_front", "ID front"), ("id_back", "ID back"), ("selfie", "Selfie"),
                                  ("shop", "Premises"), ("doc", "Sales book"), ("moto", "Logbook")]):
        x = X0 + 24 + i * (tw_ + 10)
        doc_thumb(s, x, ty + 562, tw_, 104, k, lab)
        if i == 0:
            s.rect(x - 2, ty + 560, tw_ + 4, 108, fill="none", rx=9, stroke=BRAND, sw=2.5)
    with s.g("face match"):
        y = ty + 686
        s.rect(X0 + 24, y, vw - 48, th - (y - ty) - 20, fill="#F7F7FC", rx=10)
        s.icon("smile", X0 + 40, y + 18, 22, GREEN, 2)
        s.text(X0 + 72, y + 34, "Face match: selfie vs NIRA photo 96%", 14, 600, INK)
        s.text(X0 + 72, y + 56, "Liveness passed (blink + turn) · NIRA record returned name, date of birth and photo",
               12.5, 400, MUTED)

    mx = X0 + vw + 20
    mw = 480
    card(s, mx, ty, mw, th, "Summary for decision", "What the agent captured and the system checked")
    y = ty + 92
    inst = rnd_instalment(c["amount"], c["months"])
    for lab, val in [("Loan requested", ugx(c["amount"])), ("Term", f"{c['months']} months"),
                     ("Monthly instalment (est.)", ugx(inst)), ("Free monthly income", "UGX 1,250,000"),
                     ("Instalment / free income", "35%  ✓ under 50%"), ("CRB", "Clear · no active loans"),
                     ("Collateral value", "UGX 6.3M · 105% of loan"), ("Branch approval limit", "UGX 10M  ✓ no HQ step")]:
        kv(s, mx + 24, y, mw - 48, lab, val, vcolor=GREEN_D if "✓" in val else INK)
        y += 34
    s.line(mx + 24, y - 10, mx + mw - 24, y - 10, LINE)
    s.text(mx + 24, y + 18, "Required items (7 of 7)", 14, 700, INK)
    y += 50
    items = ["NIRA ID front + back", "Selfie with live check", "Proof of income: sales book", "Business premises photo",
             "Collateral photo + logbook", "CRB consent signed", "Loan application ID from the loan system"]
    for it in items:
        s.icon("check", mx + 26, y - 12, 16, GREEN, 2.6)
        s.text(mx + 50, y, it, 13, 400, INK2)
        y += 26
    with s.g("agent note"):
        y += 8
        s.rect(mx + 24, y, mw - 48, th - (y - ty) - 20, fill="#F7F7FC", rx=10)
        s.text(mx + 40, y + 26, "Sarah's note", 12.5, 700, INK2)
        para(s, mx + 40, y + 48, "Visited 3 times. Shop busy on market days; 4 school uniform contracts for Term 1. "
                                 "Husband co-signed.", mw - 80, 13, 400, INK2, lh=20)

    dx = mx + mw + 20
    dw = X1 - dx
    card(s, dx, ty, dw, th, "Your decision", "Recorded with your name and the time; the agent is told at once")
    y = ty + 96
    opts = [("Approve", "Sends to disbursement", True, GREEN), ("Return to agent", "Ask for a missing or clearer item",
                                                                  False, AMBER_D),
            ("Reject", "A reason is required", False, RED)]
    for lab, sub, on, col in opts:
        with s.g(f"option {lab}"):
            s.rect(dx + 24, y, dw - 48, 64, fill=tint(col, 0.07) if on else CARD, rx=10,
                   stroke=col if on else LINE, sw=2 if on else 1)
            radio(s, dx + 50, y + 32, on, color=col)
            s.text(dx + 72, y + 28, lab, 15, 700, INK)
            s.text(dx + 72, y + 48, sub, 12.5, 400, MUTED)
        y += 76
    y += 6
    field(s, dx + 24, y, dw - 48, "Reason (for reject or return)", "Choose a reason", placeholder=True, dropdown=True)
    y += 86
    s.text(dx + 24, y + 14, "Comment to the agent", 13, 600, INK2)
    s.rect(dx + 24, y + 22, dw - 48, 96, fill=CARD, rx=8, stroke="#CDD0DE")
    s.text(dx + 38, y + 50, "Good file. Please remind Florence that the first", 14, 400, INK)
    s.text(dx + 38, y + 72, "instalment is due on 30 October.", 14, 400, INK)
    y += 140
    button(s, dx + 24, y, "Record decision: approve", "primary", icon="check", w=dw - 48, h=48, color=GREEN)
    s.link(dx + 24, y, dw - 48, 48, "w07")
    s.text(dx + dw / 2, y + 78, "Disbursement happens in the loan system as today.", 12.5, 400, MUTED,
           anchor="middle")
    with s.g("decision history"):
        y += 110
        s.line(dx + 24, y, dx + dw - 24, y, LINE)
        s.text(dx + 24, y + 30, "History", 13, 700, INK2)
        for i, (t_, what) in enumerate([("11:42", "Submitted by Sarah Namuli (first submission)"),
                                        ("11:43", "Automatic checks passed: 6 of 6"),
                                        ("11:43", "Assigned to you · decide by tomorrow 11:42")]):
            s.circle(dx + 30, y + 52 + i * 26, 4, fill=BRAND)
            s.text(dx + 44, y + 56 + i * 26, what, 12.5, 400, INK2, maxw=dw - 110)
            s.text(dx + dw - 24, y + 56 + i * 26, t_, 12, 400, MUTED, anchor="end")
    return s


# =====================================================================================
def hbars(s, x, y, w, rows, color, bar_h=16, gap=16, label_w=250, name="bars"):
    mx = max(r[1] for r in rows)
    with s.g(name):
        for i, (lab, v) in enumerate(rows):
            yy = y + i * (bar_h + gap)
            s.text(x, yy + bar_h - 3, lab, 13, 400, INK2, maxw=label_w - 10)
            bw = (w - label_w - 50) * v / mx
            s.rect(x + label_w, yy, bw, bar_h, fill=color, rx=4, op=1 - i * 0.07)
            s.text(x + label_w + bw + 8, yy + bar_h - 3, f"{v}%", 12.5, 600, INK)


def w09_reasons():
    s = shell("09 Why clients do and don't take loans", "Why & why not", ["Applications", "Why & why not"])
    page_head(s, "Why clients do and don't take loans", f"From agents' notes at every closed visit · {QUARTER} · all "
                                                        "branches · 7,361 visits closed with a reason")
    with s.g("header actions"):
        x = X1
        x -= button(s, x, Y0 + 12, "Export", "secondary", icon="download", anchor="end") + 12
        x -= filter_btn(s, x - 190, Y0 + 13, "Branch", "All branches", w=190) + 12
        x -= filter_btn(s, x - 170, Y0 + 13, "Product", "All", w=170) + 12
    ry = Y0 + 84
    cw3 = (CW - 2 * 20) / 3
    ch = 400
    card(s, X0, ry, cw3, ch, "Why they said no", "5,126 not interested at the first visit")
    hbars(s, X0 + 24, ry + 90, cw3 - 48, [("Already has a loan elsewhere", 24), ("Interest rate / cost", 19),
                                          ("Not eligible (income, job)", 14), ("Wants to ask spouse / family", 12),
                                          ("Not now, maybe next term", 11), ("Doesn't trust lenders", 7),
                                          ("Needs a bigger amount", 6), ("Other", 7)], RED, label_w=210)
    x2 = X0 + cw3 + 20
    card(s, x2, ry, cw3, ch, "Why they took a loan", "1,051 applications")
    hbars(s, x2 + 24, ry + 90, cw3 - 48, [("School fees", 29), ("Business stock / working capital", 27),
                                          ("Home improvement", 16), ("Farm inputs / equipment", 11),
                                          ("Medical bills", 7), ("Clearing another debt", 6), ("Other", 4)], GREEN,
          label_w=210)
    x3 = x2 + cw3 + 20
    card(s, x3, ry, cw3, ch, "Why applications were rejected", "166 rejected by supervisors or HQ")
    donut(s, x3 + 120, ry + 230, 84, 26, [(38, RED, "Affordability"), (21, AMBER, "Incomplete KYC"),
                                          (17, VIOLET, "CRB"), (13, BLUE, "Collateral"), (11, TEAL, "Employer")])
    s.text(x3 + 120, ry + 228, "166", 26, 700, INK, anchor="middle")
    s.text(x3 + 120, ry + 250, "rejected", 12, 400, MUTED, anchor="middle")
    y = ry + 140
    for lab, v, col in [("Instalment too high for income", 38, RED), ("KYC incomplete or unclear", 21, AMBER),
                        ("Negative CRB record", 17, VIOLET), ("Collateral not enough", 13, BLUE),
                        ("Employer not on payroll check-off", 11, TEAL)]:
        s.rect(x3 + 232, y - 10, 12, 12, fill=col, rx=3)
        s.text(x3 + 252, y, lab, 12.5, 400, INK2, maxw=cw3 - 300)
        s.text(x3 + cw3 - 24, y, f"{v}%", 12.5, 700, INK, anchor="end")
        y += 30

    by = ry + ch + 20
    bh = H - 28 - by
    mw = 860
    card(s, X0, by, mw, bh, "Which product fits whom", "Conversion rate by client type and product · darker = "
                                                       "better · helps agents pick the right product")
    segs = ["Civil servants", "Teachers", "Market vendors", "Boda boda riders", "Smallholder farmers"]
    prods = [p[0] for p in PRODUCTS]
    grid = [[31, 6, 12, 9, 2], [27, 5, 22, 8, 3], [3, 24, 9, 4, 5], [2, 18, 4, 2, 3], [1, 7, 6, 3, 21]]
    gx, gy = X0 + 200, by + 104
    cwid = (mw - 224) / 5
    for j, p in enumerate(prods):
        s.text(gx + j * cwid + cwid / 2, gy - 12, p.replace(" Loan", ""), 12, 600, INK2, anchor="middle")
    for i, sg in enumerate(segs):
        s.text(X0 + 24, gy + i * 44 + 27, sg, 13, 600, INK2)
        for j, v in enumerate(grid[i]):
            s.rect(gx + j * cwid + 3, gy + i * 44 + 3, cwid - 6, 38, fill=BRAND, op=0.08 + 0.92 * v / 31, rx=6)
            s.text(gx + j * cwid + cwid / 2, gy + i * 44 + 27, f"{v}%", 13, 700, "#FFFFFF" if v > 15 else INK,
                   anchor="middle")
    qx = X0 + mw + 20
    qw = X1 - qx
    card(s, qx, by, qw, bh, "In the agents' words", "Recent notes, tagged automatically")
    notes = [("“Already borrowed from the SACCO for school fees; will come back in January.”", "Not now", AMBER_D,
              "Peter Kato · Kireka"),
             ("“She wants the business loan but the husband must agree first. Follow-up Friday.”", "Spouse", BLUE,
              "Ruth Achieng · Naalya"),
             ("“Teacher on payroll; chose Civil Servant loan because the deduction is automatic.”", "Took loan", GREEN,
              "Sarah Namuli · Ntinda"),
             ("“Rate compared with the bank's; asked for longer tenor to lower the instalment.”", "Cost", RED,
              "Harriet Nabirye · Jinja")]
    y = by + 88
    for q, tag, col, who in notes:
        with s.g(f"note {tag}"):
            s.rect(qx + 24, y, qw - 48, 62, fill="#F7F7FC", rx=10)
            s.text(qx + 40, y + 26, q, 13.5, 400, INK, maxw=qw - 200)
            s.text(qx + 40, y + 47, who, 12, 400, MUTED)
            chip(s, qx + qw - 40 - tw(tag, 11, 600) - 20, y + 18, tag, col, h=22, size=11)
        y += 72
    return s


# =====================================================================================
PLANS = [
    ("Kiwatule follow-ups", "Interested clients from September; take KYC where ready", "Sarah Namuli", "SN",
     "28 Sep – 2 Oct", 12, 8, "Active", "Moses Okello"),
    ("Ntinda schools: payroll teachers", "Teachers at 5 schools · Civil Servant Loan", "Sarah Namuli", "SN",
     "21 Sep – 9 Oct", 15, 6, "Active", "Moses Okello"),
    ("Kireka boda stages", "Boda riders at 4 stages · MSE Business Loan", "Peter Kato", "PK", "28 Sep – 4 Oct", 14, 9,
     "Active", "Moses Okello"),
    ("Naalya estate homes", "Home improvement leads from the estate", "Ruth Achieng", "RA", "29 Sep – 6 Oct", 10, 4,
     "Active", "Ruth Achieng (agent)"),
    ("Bukoto: finish KYC", "Clients stuck at KYC captured", "Esther Nakato", "EN", "30 Sep – 2 Oct", 6, 1, "Active",
     "Moses Okello"),
    ("Banda follow-ups", "Interested clients with no visit in 14+ days", "Brian Ssali", "BS", "28 Sep – 2 Oct", 9, 1,
     "Active", "Moses Okello"),
    ("Kyanja market prospecting", "New area: market vendors, 3 new clients a day", "Sarah Namuli", "SN",
     "1 – 31 Oct", 8, 0, "Scheduled", "Sarah Namuli (agent)"),
    ("Namugongo: meet your new clients", "Territory moved from Daniel Okumu; visit all 46", "Peter Kato", "PK",
     "1 – 9 Oct", 46, 0,
     "Scheduled", "Moses Okello"),
    ("Q3 week 1 blitz", "Every interested client from Q2", "7 agents", "7+", "1 – 7 Jul", 34, 30, "Completed",
     "Moses Okello"),
]


def w10_plans():
    s = shell("10 Journey plans", "Journey plans", ["Planning", "Journey plans"], user=SUPERVISOR, period="Week")
    page_head(s, "Journey plans", "Named lists of clients to visit, each with an agent, start and end dates and a "
                                  "goal · Kampala East")
    with s.g("header actions"):
        x = X1
        bw = button(s, x, Y0 + 12, "New journey plan", "primary", icon="plus", anchor="end")
        s.link(x - bw, Y0 + 12, bw, 40, "w10c")
        x -= bw + 12
        x -= filter_btn(s, x - 160, Y0 + 13, "Agent", "All 7", w=160) + 12
    ky = Y0 + 84
    kw = (CW - 3 * 16) / 4
    for i, (ic, col, lab, val, sub, fr) in enumerate([
            ("route", BRAND, "Active plans", "6", "2 scheduled to start · 1 completed this quarter", None),
            ("users", TEAL, "Clients in active plans", "66", "across 5 agents", None),
            ("check", GREEN, "Visited so far", "29 of 66", "44% · active plans end 2–9 Oct", 29 / 66),
            ("clock", AMBER, "Due today, not visited yet", "11", "Ivan Kasozi and 10 more", None)]):
        kpi(s, X0 + i * (kw + 16), ky, kw, 140, ic, col, lab, val, sub, fr)
    ty = ky + 160
    seg(s, X0, ty, ["All 9", "Active 6", "Scheduled 2", "Completed 1"], "All 9", h=38)
    s.text(X1, ty + 24, "A client can sit on more than one plan; each visit counts once", 12.5, 400, MUTED,
           anchor="end")
    tby = ty + 54
    cols = [("Plan", 420, "start"), ("Agent", 210, "start"), ("Dates", 170, "start"), ("Clients", 90, "end"),
            ("Visited", 240, "start"), ("Status", 150, "start"), ("Created by", 190, "start"), ("", 122, "end")]
    rows = []
    for (nm, desc, ag, ini, dates, n, v, st, by) in PLANS:
        rows.append([
            (lambda a, b: lambda s_, x, y, w, h: (s_.text(x + 16, y + h / 2 - 3, a, 14, 600, INK, maxw=w - 24),
                                                  s_.text(x + 16, y + h / 2 + 15, b, 12, 400, MUTED,
                                                          maxw=w - 24)))(nm, desc),
            agent_cell(ag, ini, "Kampala East"), dates, str(n),
            (lambda v_, n_: lambda s_, x, y, w, h: (progress(s_, x + 16, y + h / 2 - 3, 130, v_ / n_,
                                                             GREEN if v_ / n_ >= 0.5 else (AMBER if v_ else LINE), h=7),
                                                    s_.text(x + 158, y + h / 2 + 5, f"{v_} of {n_}", 12.5, 400,
                                                            INK2)))(v, n),
            chip_cell(st), by,
            (lambda: lambda s_, x, y, w, h: button(s_, x + w - 12, y + h / 2 - 16, "Open", "soft", h=32, size=12.5,
                                                   anchor="end"))(),
        ])
    rh = (H - 28 - tby - 40 - 36) / len(rows)
    table(s, X0, tby, cols, rows, row_h=rh, head_h=40, hl=0)
    s.link(X0, tby + 40, CW, rh, "w10b")
    s.text(X0 + 16, H - 44, "Supervisors create plans for their agents; agents can create their own, which the "
                            "supervisor approves", 13, 400, MUTED)
    return s


PLAN_CLIENTS = [
    ("Charles Ssempijja", "Interested", "Mon 28", "28 Sep · follow-up booked for Fri", "Visited"),
    ("Sarah Namutebi", "KYC captured", "Mon 28", "28 Sep · KYC captured, payslip pending", "Visited"),
    ("Hassan Mugerwa", "Interested", "Tue 29", "29 Sep · needs time to think", "Visited"),
    ("Annet Namubiru", "Negotiation", "Tue 29", "29 Sep · comparing with a SACCO offer", "Visited"),
    ("Doreen Kyomuhendo", "Not interested", "Tue 29", "29 Sep · not interested: interest rate", "Visited"),
    ("Kenneth Lubega", "KYC captured", "Wed 30", "30 Sep 09:05 · employer letter pending", "Visited"),
    ("Betty Nakimuli", "KYC validated", "Wed 30", "30 Sep 10:20 · KYC validated", "Visited"),
    ("Florence Nambi", "Applied", "Wed 30", "30 Sep 11:42 · application submitted", "Visited"),
    ("Ivan Kasozi", "Negotiation", "Wed 30", "Planned for 12:30", "Due today"),
    ("Aisha Nalubega", "Interested", "Thu 1", "—", "Not yet due"),
    ("Juliet Kobusingye", "Interested", "Thu 1", "—", "Not yet due"),
    ("Tom Ssebaggala", "Interested", "Fri 2", "—", "Not yet due"),
]


def w10b_plan():
    s = shell("10b Journey plan: Kiwatule follow-ups", "Journey plans",
              ["Planning", "Journey plans", "Kiwatule follow-ups"], user=SUPERVISOR, period="Week")
    with s.g("plan header"):
        s.rect(X0, Y0, CW, 124, fill=CARD, rx=12, stroke=LINE)
        s.rect(X0 + 24, Y0 + 24, 52, 52, fill=tint(BRAND, 0.1), rx=12)
        s.icon("route", X0 + 36, Y0 + 36, 28, BRAND, 2)
        s.text(X0 + 96, Y0 + 50, "Kiwatule follow-ups", 24, 700, INK)
        status_chip(s, X0 + 106 + tw("Kiwatule follow-ups", 24, 700), Y0 + 31, "Active")
        s.text(X0 + 96, Y0 + 78, "Interested clients from September; take KYC where they are ready and close "
                                 "applications before the quarter ends.", 14, 400, INK2)
        s.text(X0 + 96, Y0 + 102, "Agent Sarah Namuli · 28 Sep – 2 Oct 2026 (5 days) · goal: 4 KYCs, 2 applications "
                                  "· created by Moses Okello on 27 Sep", 13, 400, MUTED)
        x = X1 - 24
        bw = button(s, x, Y0 + 40, "Edit plan", "primary", icon="edit", anchor="end")
        s.link(x - bw, Y0 + 40, bw, 40, "w10c")
        x -= bw + 10
        bw = button(s, x, Y0 + 40, "Add clients", "secondary", icon="userplus", anchor="end")
        s.link(x - bw, Y0 + 40, bw, 40, "w10c")
        x -= bw + 10
        button(s, x, Y0 + 40, "Duplicate", "secondary", icon="copy", anchor="end")
    ky = Y0 + 140
    kw = (CW - 4 * 16) / 5
    for i, (ic, col, lab, val, sub, fr) in enumerate([
            ("users", BRAND, "Clients in plan", "12", "in visit order", None),
            ("check", GREEN, "Visited", "8 of 12", "67% · on day 3 of 5", 8 / 12),
            ("clock", AMBER, "Due today", "1", "Ivan Kasozi at 12:30", None),
            ("calendar", "#8A8DA6", "Still to come", "3", "Thu 1 and Fri 2 Oct", None),
            ("trendup", TEAL, "Moved forward", "5", "4 KYC steps · 1 application", None)]):
        kpi(s, X0 + i * (kw + 16), ky, kw, 140, ic, col, lab, val, sub, fr)
    ty = ky + 156
    th = H - 28 - ty
    lw = 980
    card(s, X0, ty, lw, th, "Clients in visit order", "What happened at each visit · the agent's phone shows the same "
                                                      "list")
    cols = [("#", 50, "start"), ("Client", 220, "start"), ("Stage now", 170, "start"), ("Due", 90, "start"),
            ("Visit", 312, "start"), ("", 136, "start")]
    rows = []
    for i, (nm, stage, due, visit, st) in enumerate(PLAN_CLIENTS):
        rows.append([str(i + 1), nm,
                     (lambda st_: lambda s_, x, y, w, h: chip(s_, x + 12, y + h / 2 - 11, st_,
                                                              STAGE.get(st_, STATUS.get(st_, MUTED)), h=22, size=11,
                                                              dot=True))(stage),
                     due, visit, chip_cell(st)])
    table(s, X0 + 1, ty + 72, cols, rows, row_h=(th - 72 - 36 - 10) / len(rows), head_h=36, size=13, hl=7)
    s.link(X0 + 1, ty + 72 + 36 + 7 * (th - 72 - 36 - 10) / len(rows), lw - 2, (th - 72 - 36 - 10) / len(rows), "w06")
    mx = X0 + lw + 20
    mw = X1 - mx
    card(s, mx, ty, mw, th, "Map", "Numbered in visit order")
    m = StreetMap(s, mx + 16, ty + 70, mw - 32, th - 140, seed=5, lake=False, dense=0.8,
                  places=[("Ntinda", 0.22, 0.2), ("Kiwatule", 0.6, 0.18), ("Kigoowa", 0.3, 0.84)])
    spots = [(0.16, 0.14), (0.3, 0.1), (0.44, 0.16), (0.58, 0.1), (0.76, 0.14), (0.82, 0.32), (0.66, 0.4),
             (0.52, 0.46), (0.36, 0.52), (0.24, 0.66), (0.44, 0.76), (0.68, 0.8)]
    pts = [m.P(*q) for q in spots]
    s.poly(pts, stroke=BRAND, sw=2.5, closed=False, dash="2 6", name="plan route")
    for i, ((qx, qy), (_, _, _, _, st)) in enumerate(zip(pts, PLAN_CLIENTS)):
        col = {"Visited": GREEN, "Due today": BRAND}.get(st, "#8A8DA6")
        map_pin(s, qx, qy, col, str(i + 1), 0.85, name=f"client {i + 1}")
    with s.g("legend"):
        lx, ly = mx + 24, ty + th - 40
        for lab, col in [("Visited", GREEN), ("Due today", BRAND), ("Still to come", "#8A8DA6")]:
            s.circle(lx + 6, ly, 6, fill=col)
            lx += s.text(lx + 18, ly + 4, lab, 12.5, 400, INK2) + 40
    return s


CANDIDATES = [("Brenda Atuhaire", "Interested", "Last visit 12 Sep · Kigoowa", True),
              ("Sam Wamala", "Interested", "Last visit 9 Sep · Kyanja", True),
              ("Rose Nakitto", "KYC captured", "Last visit 15 Sep · Kigoowa", True),
              ("Denis Kato", "Negotiation", "Last visit 18 Sep · Kyanja", True),
              ("Faith Ahimbisibwe", "Interested", "Last visit 2 Sep · Kyanja", True),
              ("Lillian Nabirye", "Interested", "Last visit 11 Sep · Kigoowa", True),
              ("Ronald Mubiru", "Interested", "Last visit 24 Sep · Kyanja", False),
              ("Irene Kansiime", "KYC validated", "Last visit 26 Sep · Kigoowa", False),
              ("Tony Kizito", "Interested", "Last visit 25 Sep · Kyanja", False)]


def w10c_new_plan():
    s = shell("10c New journey plan", "Journey plans", ["Planning", "Journey plans", "New plan"], user=SUPERVISOR,
              period="Week")
    page_head(s, "New journey plan", "Name it, give it dates, pick the clients · it goes to the agent's phone when "
                                     "you publish")
    with s.g("header actions"):
        x = X1
        bw = button(s, x, Y0 + 12, "Publish to Sarah's phone", "primary", icon="send", anchor="end")
        s.link(x - bw, Y0 + 12, bw, 40, "w10")
        x -= bw + 12
        bw = button(s, x, Y0 + 12, "Save draft", "secondary", anchor="end")
        s.link(x - bw, Y0 + 12, bw, 40, "w10")
    ty = Y0 + 84
    th = H - 28 - ty
    aw = 460
    card(s, X0, ty, aw, th, "Plan details")
    fx, fw = X0 + 24, aw - 48
    y = ty + 72
    y += field(s, fx, y, fw, "Plan name", "Kigoowa & Kyanja: October follow-ups", required=True) + 14
    s.text(fx, y + 14, "Description", 13, 600, INK2)
    s.rect(fx, y + 22, fw, 84, fill=CARD, rx=8, stroke="#CDD0DE")
    para(s, fx + 14, y + 48, "Interested clients from September who haven't done KYC. Take KYC where ready; book "
                             "the rest for a second visit.", fw - 28, 13.5, 400, INK, lh=21)
    y += 120
    y += field(s, fx, y, fw, "Agent", "Sarah Namuli · Kampala East", dropdown=True, icon="user", required=True) + 14
    hw = (fw - 12) / 2
    field(s, fx, y, hw, "Start date", "Mon 5 Oct 2026", icon="calendar", required=True)
    field(s, fx + hw + 12, y, hw, "End date", "Fri 16 Oct 2026", icon="calendar", required=True)
    y += 80
    s.text(fx, y + 14, "Visit days", 13, 600, INK2)
    x = fx
    for d, on in [("Mon", True), ("Tue", True), ("Wed", True), ("Thu", True), ("Fri", True), ("Sat", False)]:
        s.rect(x, y + 24, 60, 34, fill=BRAND if on else CARD, rx=8, stroke=None if on else "#CDD0DE")
        s.text(x + 30, y + 46, d, 13, 600, "#FFFFFF" if on else INK2, anchor="middle")
        x += 68
    y += 76
    y += field(s, fx, y, fw, "Goal (optional)", "4 KYCs · 2 applications") + 18
    for lab, on in [("Agent can change the visit order", True), ("Remind the agent the evening before", True)]:
        s.text(fx, y + 14, lab, 13.5, 400, INK2)
        toggle(s, fx + fw - 36, y, on)
        y += 36

    bx = X0 + aw + 20
    bw_ = 560
    card(s, bx, ty, bw_, th, "Add clients", "Sarah's clients, filtered · tick to add")
    with s.g("search"):
        s.rect(bx + 24, ty + 76, bw_ - 48, 40, fill="#F4F5FA", rx=8, stroke=LINE)
        s.icon("search", bx + 36, ty + 87, 18, MUTED)
        s.text(bx + 64, ty + 101, "Search name, phone or area", 13, 400, FAINT)
    x = bx + 24
    for lab, on in [("Stage: Interested +2", True), ("Area: Kigoowa, Kyanja", True), ("No visit 14+ days", False)]:
        w = chip(s, x, ty + 128, lab, BRAND if on else "#8A8DA6", h=28, size=12, icon="filter" if on else None)
        x += w + 8
    y = ty + 172
    for nm, st, sub, on in CANDIDATES:
        with s.g(f"candidate {nm}"):
            s.line(bx + 24, y, bx + bw_ - 24, y, LINE2)
            checkbox(s, bx + 28, y + 17, on)
            s.text(bx + 60, y + 24, nm, 14, 600, INK)
            s.text(bx + 60, y + 42, sub, 12, 400, MUTED)
            chip(s, bx + bw_ - 24 - tw(st, 11, 600) - 34, y + 17, st, STAGE[st], h=22, size=11, dot=True)
        y += 58
    bw2 = button(s, bx + bw_ - 24, ty + th - 64, "Add 6 selected", "primary", icon="plus", anchor="end")

    cx = bx + bw_ + 20
    cw = X1 - cx
    card(s, cx, ty, cw, th, "In this plan (6)", "Suggested order by distance · drag to change")
    m = StreetMap(s, cx + 16, ty + 72, cw - 32, 220, seed=11, lake=False, dense=0.7,
                  places=[("Kigoowa", 0.25, 0.3), ("Kyanja", 0.7, 0.7)])
    spots = [(0.15, 0.2), (0.32, 0.35), (0.48, 0.25), (0.6, 0.5), (0.78, 0.62), (0.88, 0.82)]
    pts = [m.P(*q) for q in spots]
    s.poly(pts, stroke=BRAND, sw=2.5, closed=False, dash="2 6")
    for i, (qx, qy) in enumerate(pts):
        map_pin(s, qx, qy, BRAND, str(i + 1), 0.8, name=f"client {i + 1}")
    button(s, cx + cw - 24, ty + 304, "Optimise order", "soft", icon="route", h=32, size=12.5, anchor="end")
    y = ty + 352
    days = ["Mon 5", "Mon 5", "Tue 6", "Tue 6", "Wed 7", "Wed 7"]
    for i, ((nm, st, sub, on), d) in enumerate(zip([c for c in CANDIDATES if c[3]], days)):
        with s.g(f"planned {nm}"):
            s.line(cx + 24, y, cx + cw - 24, y, LINE2)
            s.icon("menu", cx + 24, y + 17, 16, FAINT, 2)
            s.circle(cx + 62, y + 25, 12, fill=BRAND)
            s.text(cx + 62, y + 29.5, str(i + 1), 11.5, 700, "#FFFFFF", anchor="middle")
            s.text(cx + 84, y + 30, nm, 13.5, 600, INK)
            s.text(cx + cw - 56, y + 30, d, 12.5, 400, INK2, anchor="end")
            s.icon("x", cx + cw - 44, y + 17, 16, MUTED, 2)
        y += 50
    return s


# =====================================================================================
TERRITORIES = [
    ("Bukoto · Kisaasi", "Esther Nakato", "EN", 164, 4, AMBER, "Active"),
    ("Ntinda · Kiwatule", "Sarah Namuli", "SN", 212, 6, BRAND, "Active"),
    ("Kigoowa · Kyanja", "Ivan Mugabe", "IM", 141, 4, GREEN, "Active"),
    ("Naalya · Kira", "Ruth Achieng", "RA", 176, 5, VIOLET, "Active"),
    ("Nakawa · Mbuya", "Joan Auma", "JA", 120, 3, BLUE, "Active"),
    ("Banda · Kyambogo", "Brian Ssali", "BS", 133, 4, RED, "Active"),
    ("Kireka · Bweyogerere", "Peter Kato", "PK", 188, 5, TEAL, "Active"),
    ("Namugongo · Kyaliwajjala", "Daniel Okumu", "DO", 46, 4, "#D9651B", "Leaving today"),
]
_XS, _YS = [0.02, 0.27, 0.51, 0.75, 0.98], [0.03, 0.49, 0.97]
_JIT = {(1, 1): (0.02, -0.03), (2, 1): (-0.03, 0.03), (3, 1): (0.02, 0.02)}


def _territory_polys(m):
    polys = []
    for r in range(2):
        for c in range(4):
            def pt(ci, ri):
                dx, dy = _JIT.get((ci, ri), (0, 0))
                return m.P(_XS[ci] + dx, _YS[ri] + dy)
            polys.append([pt(c, r), pt(c + 1, r), pt(c + 1, r + 1), pt(c, r + 1)])
    return polys


def w11_locations():
    s = shell("11 Locations", "Locations", ["Admin", "Locations"], user=SUPERVISOR)
    page_head(s, "Locations", "Letshego's field geography · clients sit on routes · people are given locations when "
                              "their user is created")
    with s.g("header actions"):
        x = X1
        x -= button(s, x, Y0 + 12, "Add territory", "primary", icon="plus", anchor="end") + 12
        bw = button(s, x, Y0 + 12, "Add route", "secondary", icon="route", anchor="end")
        s.link(x - bw, Y0 + 12, bw, 40, "w11b")
    ty = Y0 + 84
    cw = (CW - 3 * 36) / 4
    tabs = [("globe", "Regions", "4", "Central · Eastern · Northern · Western", False),
            ("store", "Branches", "14", "e.g. Kampala East, Mbarara, Gulu", False),
            ("layers", "Territories", "64", "one agent covers each", True),
            ("route", "Routes", "251", "clients sit on a route", False)]
    for i, (ic, lab, n, sub, on) in enumerate(tabs):
        x = X0 + i * (cw + 36)
        with s.g(f"level {lab}"):
            s.rect(x, ty, cw, 88, fill=CARD, rx=14, stroke=BRAND if on else LINE, sw=2 if on else 1,
                   shadow=not on)
            s.rect(x + 18, ty + 22, 44, 44, fill=tint(BRAND, 0.1) if on else "#F4F5FA", rx=12, shadow=False)
            s.icon(ic, x + 29, ty + 33, 22, BRAND if on else INK2, 2)
            s.text(x + 78, ty + 42, n, 22, 700, INK)
            s.text(x + 84 + tw(n, 22, 700), ty + 41, lab, 14, 600, BRAND if on else INK2)
            s.text(x + 78, ty + 64, sub, 12, 400, MUTED, maxw=cw - 96)
        if i < 3:
            s.icon("chevright", x + cw + 8, ty + 34, 20, FAINT, 2)
    fy = ty + 110
    with s.g("filters"):
        x = X0
        x += filter_btn(s, x, fy, "Region", "Central", w=180) + 12
        x += filter_btn(s, x, fy, "Branch", "Kampala East", w=220) + 12
        s.rect(x, fy, 280, 38, fill=CARD, rx=8, stroke=LINE, shadow=False)
        s.icon("search", x + 12, fy + 10, 18, MUTED)
        s.text(x + 40, fy + 24, "Search territories", 13, 400, FAINT)
        s.text(X1, fy + 24, "8 territories in Kampala East", 13, 400, MUTED, anchor="end")
    tby = fy + 54
    cols = [("Territory", 300, "start"), ("Branch", 170, "start"), ("Region", 130, "start"), ("Routes", 90, "end"),
            ("Clients", 100, "end"), ("Agent", 330, "start"), ("Status", 190, "start"), ("", 282, "end")]
    rows = []
    for nm, ag, ini, n, routes, col, st in TERRITORIES:
        leaving = st != "Active"
        rows.append([
            (lambda nm_, col_: lambda s_, x, y, w, h: (s_.rect(x + 16, y + h / 2 - 12, 8, 24, fill=col_, rx=3, op=0.8),
                                                       s_.text(x + 36, y + h / 2 + 5, nm_, 14, 600, INK)))(nm, col),
            "Kampala East", "Central", str(routes), str(n),
            agent_cell(ag, ini, "leaves today, 18:00" if leaving else "Field Sales Agent", col),
            chip_cell("Needs an agent" if leaving else "Active", RED if leaving else GREEN, status=False),
            (lambda lv: lambda s_, x, y, w, h: button(s_, x + w - 16, y + h / 2 - 16,
                                                      "Assign agent" if lv else "Edit",
                                                      "primary" if lv else "secondary", h=32, size=12.5,
                                                      anchor="end"))(leaving)])
    rh = (H - 28 - tby - 40 - 40) / len(rows)
    table(s, X0, tby, cols, rows, row_h=rh, head_h=40)
    s.link(X1 - 150, tby + 40 + 7 * rh, 150, rh, "w12b")
    s.text(X0 + 16, H - 44, "Showing 8 of 64 territories · the other levels use the same list, one tab each", 13,
           400, MUTED)
    return s


def w11b_new_route():
    s = shell("11b New route", "Locations", ["Admin", "Locations", "New route"], user=SUPERVISOR)
    page_head(s, "New route", "A route groups the clients to visit inside one territory · routes added from the app "
                              "wait for a supervisor's approval")
    with s.g("header actions"):
        x = X1
        bw = button(s, x, Y0 + 12, "Save route", "primary", icon="check", anchor="end")
        s.link(x - bw, Y0 + 12, bw, 40, "w11")
        x -= bw + 12
        bw = button(s, x, Y0 + 12, "Cancel", "secondary", anchor="end")
        s.link(x - bw, Y0 + 12, bw, 40, "w11")
    ty = Y0 + 84
    th = H - 28 - ty
    lw = 540
    card(s, X0, ty, lw, th, "Where it sits", "Pick from the top down")
    fx, fw = X0 + 24, lw - 48
    y = ty + 76
    for i, (lab, val, hint) in enumerate([("Region", "Central", None), ("Branch", "Kampala East", None),
                                          ("Territory", "Ntinda · Kiwatule", "Covered by Sarah Namuli · 6 routes")]):
        with s.g(f"step {lab}"):
            s.circle(fx + 12, y + 40, 12, fill=BRAND)
            s.text(fx + 12, y + 44.5, str(i + 1), 11.5, 700, "#FFFFFF", anchor="middle")
            field(s, fx + 36, y, fw - 36, lab, val, dropdown=True, required=True, ok=hint)
        y += 96 if hint else 80
    s.line(fx, y + 4, fx + fw, y + 4, LINE)
    y += 24
    s.text(fx, y + 10, "Route details", 15, 700, INK)
    y += 24
    y += field(s, fx, y, fw, "Route name", "Kiwatule new estates", required=True) + 12
    s.text(fx, y + 14, "Description", 13, 600, INK2)
    s.rect(fx, y + 22, fw, 76, fill=CARD, rx=8, stroke="#CDD0DE", shadow=False)
    para(s, fx + 14, y + 48, "New housing estates north of Kiwatule market; mostly salaried workers and small "
                             "shops.", fw - 28, 13.5, 400, INK, lh=21)
    y += 118
    for lab, on in [("Active", True), ("Place existing clients inside the area on this route", True)]:
        s.text(fx, y + 14, lab, 13.5, 400, INK2)
        toggle(s, fx + fw - 36, y, on)
        y += 38

    mx = X0 + lw + 20
    mw = X1 - mx
    card(s, mx, ty, mw, th, "Draw the route area", "Click to add points · 23 clients fall inside")
    m = StreetMap(s, mx + 16, ty + 70, mw - 32, th - 86, seed=11, lake=False, dense=0.8,
                  places=[("Ntinda", 0.24, 0.3), ("Kiwatule", 0.66, 0.44)])
    terr = [m.P(*p) for p in [(0.06, 0.08), (0.94, 0.1), (0.9, 0.92), (0.1, 0.9)]]
    s.poly(terr, fill=BRAND, op=0.04, stroke=BRAND, sw=2, dash="7 5", name="territory boundary")
    for pts, lab in [([(0.12, 0.62), (0.3, 0.55), (0.45, 0.75)], "Ntinda stage"),
                     ([(0.5, 0.8), (0.64, 0.66), (0.82, 0.74)], "Kiwatule market"),
                     ([(0.14, 0.2), (0.28, 0.34), (0.4, 0.22)], "Ntinda schools")]:
        pp = [m.P(*p) for p in pts]
        s.poly(pp, stroke=MUTED, sw=3, closed=False, dash="2 6", name=f"route {lab}")
        s.text(pp[-1][0] + 8, pp[-1][1] + 4, lab, 11.5, 600, MUTED)
    new = [m.P(*p) for p in [(0.52, 0.14), (0.84, 0.18), (0.86, 0.46), (0.6, 0.52), (0.5, 0.34)]]
    s.poly(new, fill=YELLOW, op=0.28, stroke=YELLOW_D, sw=2.5, name="new route area")
    for px, py in new:
        s.circle(px, py, 6, fill=CARD, stroke=YELLOW_D, sw=2.5)
    import random
    rnd = random.Random(4)
    for _ in range(23):
        fx_, fy_ = rnd.uniform(0.56, 0.8), rnd.uniform(0.22, 0.46)
        s.circle(*m.P(fx_, fy_), 4, fill=BRAND, stroke="#FFFFFF", sw=1.2)
    cx, cy = m.P(0.68, 0.33)
    w = tw("Kiwatule new estates", 12.5, 700)
    s.rect(cx - w / 2 - 10, cy - 38, w + 20, 26, fill="#FFFFFF", rx=8, shadow=False)
    s.text(cx, cy - 20, "Kiwatule new estates", 12.5, 700, INK, anchor="middle")
    return s


USERS_LIST = [
    ("Patricia Nankya", "PN", "LU-0142", "Head of Sales", "All", "All", "—", "Active", "Today 09:12", BRAND),
    ("Agnes Nabwire", "AN", "LU-0310", "Regional Manager", "Central", "All 4 branches", "—", "Active", "Today 08:40",
     VIOLET),
    ("Moses Okello", "MO", "LU-0421", "Branch Supervisor", "Central", "Kampala East", "All 8", "Active", "Today 12:03",
     TEAL),
    ("Daniel Ssekandi", "DS", "LU-0198", "HQ Credit Approver", "All", "All", "Loans above UGX 10M", "Active",
     "Yesterday 17:20", AMBER),
    ("Sarah Namuli", "SN", "LU-0877", "Field Sales Agent", "Central", "Kampala East", "Ntinda · Kiwatule", "Active",
     "Today 12:01", GREEN),
    ("Peter Kato", "PK", "LU-0912", "Field Sales Agent", "Central", "Kampala East", "Kireka · Bweyogerere", "Active",
     "Today 11:39", GREEN),
    ("Ruth Achieng", "RA", "LU-0930", "Field Sales Agent", "Central", "Kampala East", "Naalya · Kira", "Active",
     "Today 11:31", GREEN),
    ("Daniel Okumu", "DO", "LU-1033", "Field Sales Agent", "Central", "Kampala East", "Namugongo · Kyaliwajjala",
     "Leaving today", "Today 10:12", RED),
    ("Robert Ouma", "RO", "LU-0655", "Field Sales Agent", "Central", "Kampala Central", "Wandegeya · Makerere",
     "Active", "Today 10:15", GREEN),
    ("Allan Tumwine", "AT", "LU-0702", "Field Sales Agent", "Western", "Mbarara", "Mbarara town · Kakoba", "Active",
     "Today 09:58", GREEN),
]


def w12_users():
    s = shell("12 Users", "Users", ["Admin", "Users"], user=SUPERVISOR)
    page_head(s, "Users", "Everyone who uses the app or the console · each user's locations decide what they see")
    with s.g("header actions"):
        x = X1
        bw = button(s, x, Y0 + 12, "Add user", "primary", icon="userplus", anchor="end")
        s.link(x - bw, Y0 + 12, bw, 40, "w12b")
        x -= bw + 12
        x -= filter_btn(s, x - 190, Y0 + 13, "Branch", "Kampala East", w=190) + 12
        x -= filter_btn(s, x - 160, Y0 + 13, "Region", "Central", w=160) + 12
        filter_btn(s, x - 150, Y0 + 13, "Role", "All", w=150)
    by = Y0 + 80
    with s.g("leaving banner"):
        s.rect(X0, by, CW, 52, fill=tint(RED, 0.07), rx=12, stroke=tint(RED, 0.35), shadow=False)
        s.icon("alert", X0 + 18, by + 15, 22, RED, 2)
        s.text(X0 + 52, by + 32, "Daniel Okumu leaves today. His territory Namugongo · Kyaliwajjala (46 clients) needs "
                                 "an agent before 18:00.", 14, 600, INK)
        bw = button(s, X1 - 16, by + 10, "Give it to someone", "primary", h=32, size=12.5, anchor="end")
        s.link(X1 - 16 - bw, by + 10, bw, 32, "w12b")
    tby = by + 70
    cols = [("User", 290, "start"), ("Role", 190, "start"), ("Region", 120, "start"), ("Branch", 170, "start"),
            ("Territories", 290, "start"), ("Status", 170, "start"), ("Last active", 170, "start"), ("", 192, "end")]
    rows = []
    for nm, ini, staff, role, reg, br, terr, st, last, col in USERS_LIST:
        rows.append([agent_cell(nm, ini, f"Staff ID {staff}", col), role, reg, br, terr, chip_cell(st), last,
                     (lambda: lambda s_, x, y, w, h: button(s_, x + w - 16, y + h / 2 - 16, "Edit", "secondary", h=32,
                                                            size=12.5, anchor="end"))()])
    rh = (H - 28 - tby - 40 - 40) / len(rows)
    table(s, X0, tby, cols, rows, row_h=rh, head_h=40, hl=5)
    s.link(X0, tby + 40 + 5 * rh, CW, rh, "w12b")
    s.text(X0 + 16, H - 44, "Showing 10 of 94 users", 13, 400, MUTED)
    return s


def w12b_edit_user():
    s = shell("12b Edit user: Peter Kato", "Users", ["Admin", "Users", "Peter Kato"], user=SUPERVISOR)
    with s.g("user header"):
        s.rect(X0, Y0, CW, 96, fill=CARD, rx=14, stroke=LINE)
        avatar(s, X0 + 52, Y0 + 48, 28, "PK", GREEN)
        s.text(X0 + 96, Y0 + 44, "Peter Kato", 22, 700, INK)
        chip(s, X0 + 106 + tw("Peter Kato", 22, 700), Y0 + 26, "Field Sales Agent", GREEN, h=24, size=11.5)
        s.text(X0 + 96, Y0 + 70, "Staff ID LU-0912 · 0701 223 ··· · joined Feb 2024 · supervisor Moses Okello", 13.5,
               400, MUTED)
        x = X1 - 24
        bw = button(s, x, Y0 + 28, "Save changes", "primary", icon="check", anchor="end")
        s.link(x - bw, Y0 + 28, bw, 40, "w12")
        x -= bw + 10
        bw = button(s, x, Y0 + 28, "Cancel", "secondary", anchor="end")
        s.link(x - bw, Y0 + 28, bw, 40, "w12")
    ty = Y0 + 112
    th = H - 28 - ty
    lw = 420
    card(s, X0, ty, lw, th, "Profile")
    fx, fw = X0 + 24, lw - 48
    y = ty + 64
    for lab, val, dd in [("Full name", "Peter Kato", False), ("Staff ID", "LU-0912", False),
                         ("Phone", "0701 223 ···", False), ("Role", "Field Sales Agent", True),
                         ("Supervisor", "Moses Okello", True)]:
        y += field(s, fx, y, fw, lab, val, dropdown=dd, required=True) + 12
    y += 6
    for lab, sub, on in [("Active", "Can sign in to the app", True), ("Phone registered", "Samsung A14 · since Feb 2024", True)]:
        s.text(fx, y + 12, lab, 13.5, 600, INK)
        s.text(fx, y + 30, sub, 12, 400, MUTED)
        toggle(s, fx + fw - 36, y + 6, on)
        y += 50

    mx = X0 + lw + 20
    mw = 620
    card(s, mx, ty, mw, th, "Where Peter works", "Region › Branch › Territories › Routes · as in the user form "
                                                 "cascade")
    fx, fw = mx + 24, mw - 48
    hw = (fw - 12) / 2
    field(s, fx, ty + 76, hw, "Region", "Central", dropdown=True, required=True)
    field(s, fx + hw + 12, ty + 76, hw, "Branch", "Kampala East", dropdown=True, required=True)
    y = ty + 168
    s.text(fx, y, "Territories", 13, 600, INK2)
    s.text(fx + fw, y, "one agent per territory", 12, 400, MUTED, anchor="end")
    y += 12
    for nm, ag, ini, n, routes, col, st in TERRITORIES:
        mine = nm in ("Kireka · Bweyogerere", "Namugongo · Kyaliwajjala")
        new = nm == "Namugongo · Kyaliwajjala"
        with s.g(f"territory {nm}"):
            if new:
                s.rect(fx - 8, y, fw + 16, 50, fill=tint(GREEN, 0.07), rx=10, stroke=tint(GREEN, 0.5), shadow=False)
            else:
                s.line(fx, y, fx + fw, y, LINE2)
            checkbox(s, fx + 2, y + 16, mine, color=GREEN if new else BRAND)
            s.text(fx + 32, y + 22, nm, 13.5, 600, INK if mine else FAINT)
            sub = ("From Daniel Okumu, who leaves today" if new else
                   ("Peter's territory" if mine else f"Covered by {ag}"))
            s.text(fx + 32, y + 39, sub, 11.5, 600 if new else 400, GREEN_D if new else MUTED)
            s.text(fx + fw, y + 30, f"{n} clients · {routes} routes", 12, 400, INK2 if mine else FAINT, anchor="end")
        y += 52
    y += 14
    s.text(fx, y, "Routes", 13, 600, INK2)
    radio(s, fx + 10, y + 24, True)
    s.text(fx + 28, y + 29, "All routes in these territories (9)", 13, 400, INK)
    radio(s, fx + 290, y + 24, False)
    s.text(fx + 308, y + 29, "Only some routes", 13, 400, INK2)

    rx = mx + mw + 20
    rw = X1 - rx
    card(s, rx, ty, rw, th, "What changes when you save")
    y = ty + 70
    for val, lab in [("+46", "clients · 188 → 234"), ("+4", "routes · 5 → 9"),
                     ("+1", "journey plan: meet your new clients")]:
        s.rect(rx + 24, y, rw - 48, 50, fill="#F7F7FC", rx=12, shadow=False)
        s.text(rx + 40, y + 32, val, 18, 700, GREEN_D)
        s.text(rx + 48 + tw(val, 18, 700), y + 31, lab, 13, 400, INK2, maxw=rw - 120)
        y += 58
    m = StreetMap(s, rx + 24, y + 6, rw - 48, 230, seed=5, lake=False, dense=0.7)
    polys = _territory_polys(m)
    for (nm, *_r, col, st), pts in zip(TERRITORIES, polys):
        on = nm in ("Kireka · Bweyogerere", "Namugongo · Kyaliwajjala")
        s.poly(pts, fill=GREEN if on else "#8A8DA6", op=0.3 if on else 0.06, stroke=GREEN if on else "#C4C7D6",
               sw=2 if on else 1, name=f"zone {nm}")
    y += 252
    for t_ in ["Daniel's 2 open applications stay credited to him",
               "Clients get an SMS introducing Peter",
               "Logged in the audit trail with the old and new agent"]:
        s.icon("check", rx + 24, y - 12, 16, GREEN, 2.6)
        s.text(rx + 48, y, t_, 12.5, 400, INK2, maxw=rw - 72)
        y += 28
    return s


# =====================================================================================
def w12c_roles():
    s = shell("12c Roles and access", "Roles & access", ["Admin", "Roles & access"])
    page_head(s, "Roles & access", "What each role can do, and how its locations are set")
    with s.g("header actions"):
        button(s, X1, Y0 + 12, "Add role", "secondary", icon="plus", anchor="end")
    ty = Y0 + 84
    rw_ = 1040
    card(s, X0, ty, rw_, 520, "Roles", "Permissions are configurable; these are the defaults we propose")
    roles = [("Field Sales Agent", "Own territories", 62), ("Branch Supervisor", "Branch", 14),
             ("Regional Manager", "Region", 4), ("HQ Credit Approver", "All · above limit", 3),
             ("Head of Sales / Management", "All branches", 5), ("System Admin", "Settings only", 2)]
    perms = ["Visits & KYC", "Approve", "Locations", "Set plans", "Dashboards", "Users"]
    matrix = [[1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 0], [0, 1, 0, 0, 1, 0], [0, 0, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 1]]
    gx = X0 + 420
    cwd = (rw_ - 420 - 24) / len(perms)
    gy = ty + 96
    s.text(X0 + 24, gy, "ROLE", 11, 600, MUTED, spacing=0.6)
    s.text(X0 + 250, gy, "SEES", 11, 600, MUTED, spacing=0.6)
    for j, p in enumerate(perms):
        s.text(gx + j * cwd + cwd / 2, gy, p.upper(), 10.5, 600, MUTED, anchor="middle", spacing=0.4)
    for i, (r, scope, n) in enumerate(roles):
        y = gy + 20 + i * 64
        s.line(X0 + 24, y, X0 + rw_ - 24, y, LINE2)
        s.text(X0 + 24, y + 30, r, 14, 600, INK)
        s.text(X0 + 24, y + 49, f"{n} users", 12, 400, MUTED)
        s.text(X0 + 250, y + 36, scope, 13, 400, INK2)
        for j, v in enumerate(matrix[i]):
            cx = gx + j * cwd + cwd / 2
            if v:
                s.circle(cx, y + 32, 12, fill=tint(GREEN, 0.15))
                s.icon("check", cx - 7, y + 25, 14, GREEN, 2.8)
            else:
                s.text(cx, y + 37, "—", 13, 400, FAINT, anchor="middle")
    card(s, X0, ty + 540, rw_, H - 28 - ty - 540, "Sign-in and devices", None)
    y = ty + 540 + 70
    for lab, sub, on in [("Two-step sign-in for the web console", "Code by SMS or authenticator app", True),
                         ("Agents' phones registered to one person", "A new phone needs supervisor approval", True),
                         ("Remote wipe when someone leaves", "Client data is removed from the phone, kept on the "
                                                             "server", True)]:
        s.text(X0 + 24, y + 14, lab, 14, 600, INK)
        s.text(X0 + 24, y + 34, sub, 12.5, 400, MUTED)
        toggle(s, X0 + rw_ - 60, y + 6, on)
        y += 56

    tx = X0 + rw_ + 20
    tw2 = X1 - tx
    card(s, tx, ty, tw2, H - 28 - ty, "How locations are set", "Chosen in the user form, from the top down")
    y = ty + 80
    for role, how in [("Field Sales Agent", "Region › Branch › one or more territories (or single routes)"),
                      ("Branch Supervisor", "Region › Branch · sees every territory in it"),
                      ("Regional Manager", "One or more regions · sees every branch in them"),
                      ("HQ Credit Approver", "All branches · loans above the branch limit"),
                      ("Head of Sales", "Everything"),
                      ("System Admin", "No field data · settings only")]:
        s.line(tx + 24, y, tx + tw2 - 24, y, LINE2)
        s.text(tx + 24, y + 28, role, 14, 600, INK)
        para(s, tx + 24, y + 50, how, tw2 - 48, 12.5, 400, INK2, lh=18)
        y += 84
    with s.g("note"):
        s.rect(tx + 24, y + 12, tw2 - 48, 80, fill=tint(BRAND, 0.06), rx=12, shadow=False)
        s.icon("info", tx + 40, y + 30, 18, BRAND, 2)
        para(s, tx + 68, y + 42, "Scope decides what each person sees on the dashboard and in the app. Change it on "
                                 "the user's page.", tw2 - 110, 12.5, 400, INK2, lh=19)
        s.link(tx + 24, y + 12, tw2 - 48, 80, "w12")
    return s


# =====================================================================================
def w13_reports():
    s = shell("13 Reports, integrations and audit trail", "Reports & audit", ["Admin", "Reports & audit"])
    page_head(s, "Reports & audit", "Scheduled reports, connections to Letshego's systems, and a record of every change")
    ty = Y0 + 84
    c1 = 620
    card(s, X0, ty, c1, 420, "Scheduled reports", "Sent automatically; no one has to remember")
    y = ty + 88
    reps = [("mail", "Daily field summary", "07:00 · supervisors · email + WhatsApp", True),
            ("alert", "Silent agents alert", "Mon 08:00 · Head of Sales", True),
            ("bars", "Weekly branch league", "Fri 17:00 · all branch managers", True),
            ("file", "Quarterly performance pack (PDF)", "Day 1 of each quarter · management", True),
            ("message", "Reasons report: why / why not", "Monthly · product team", False)]
    for ic, t, sub, on in reps:
        s.rect(X0 + 24, y, 40, 40, fill=tint(BRAND, 0.1), rx=10)
        s.icon(ic, X0 + 34, y + 10, 20, BRAND, 2)
        s.text(X0 + 78, y + 17, t, 14, 600, INK)
        s.text(X0 + 78, y + 36, sub, 12.5, 400, MUTED)
        toggle(s, X0 + c1 - 60, y + 10, on)
        y += 62
    x2 = X0 + c1 + 20
    c2 = X1 - x2
    card(s, x2, ty, c2, 420, "Connections", "Agreed at kickoff; each has a manual fallback so the rollout doesn't wait")
    conns = [("database", "Letshego loan system", "Checks the loan application ID; pulls approval and disbursement "
                                                  "status", "Proposed", BLUE),
             ("idcard", "NIRA ID verification", "NIN, name and photo match at KYC (via an approved NIRA gateway)",
              "Proposed", BLUE),
             ("shield", "Credit reference bureau (CRB)", "Credit check with the client's signed consent", "Proposed",
              BLUE),
             ("message", "SMS gateway", "OTPs, client notifications, handover messages", "Ready", GREEN),
             ("download", "Excel / CSV export", "Any table, any time, for Letshego's own analysis", "Ready", GREEN)]
    y = ty + 88
    for ic, t, sub, st, col in conns:
        s.rect(x2 + 24, y, 40, 40, fill=tint(col, 0.1), rx=10)
        s.icon(ic, x2 + 34, y + 10, 20, col, 2)
        s.text(x2 + 78, y + 17, t, 14, 600, INK)
        s.text(x2 + 78, y + 36, sub, 12.5, 400, MUTED, maxw=c2 - 230)
        chip(s, x2 + c2 - 24 - tw(st, 11, 600) - 34, y + 9, st, col, h=22, size=11, dot=True)
        y += 62

    ay = ty + 440
    card(s, X0, ay, CW, H - 28 - ay, "Audit trail", "Every change: who, when, what it was before · cannot be edited",
         action="Export audit log →")
    cols = [("When", 190, "start"), ("Who", 230, "start"), ("Action", 260, "start"), ("Record", 300, "start"),
            ("Before → after", 420, "start"), ("From", 192, "start")]
    rows = [["30 Sep 12:03", "Moses Okello", "Approved application", CLIENT["app_id"], "Applied → Approved",
             "Web · Kampala"],
            ["30 Sep 11:42", "Sarah Namuli", "Submitted application", "Florence Nambi", "Negotiation → Applied",
             "Phone · 0.3712, 32.6205"],
            ["30 Sep 10:58", "Sarah Namuli", "Checked out visit: not interested", "Joseph Kiggundu",
             "Reason: already has a SACCO loan", "Phone · Ntinda"],
            ["30 Sep 09:12", "Patricia Nankya", "Changed weekly minimum", "Kampala East", "Visits 15 → 20 a week",
             "Web · Head office"],
            ["12 Aug 17:05", "Moses Okello", "Reassigned territory", "Ntinda · Kiwatule", "John Mugisha (left) → Sarah Namuli",
             "Web · Kampala"]]
    table(s, X0 + 1, ay + 76, cols, rows, row_h=(H - 28 - ay - 76 - 16) / 5 - 8, head_h=36)
    return s


SCREENS = [w07_approvals, w08_review, w09_reasons, w10_plans, w10b_plan, w10c_new_plan, w11_locations,
           w11b_new_route, w12_users, w12b_edit_user, w12c_roles, w13_reports]
