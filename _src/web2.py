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
PLAN_REASON = {"Follow-up": BLUE, "Finish KYC": VIOLET, "Offer loan": TEAL, "Negotiate": AMBER,
               "From handover": "#D9651B", "Prospecting": "#8A8DA6"}


def w10_plans():
    s = shell("10 Journey plans: which clients each agent visits", "Journey plans",
              ["Planning", "Journey plans"], user=SUPERVISOR, period="Day")
    page_head(s, "Journey plans", "Which clients each agent visits tomorrow, and in what order · published to "
                                  "agents' phones at 18:00")
    with s.g("header actions"):
        x = X1
        x -= button(s, x, Y0 + 12, "Publish plans to phones", "primary", icon="send", anchor="end") + 12
        x -= button(s, x, Y0 + 12, "Copy last Thursday", "secondary", icon="copy", anchor="end") + 12
        x -= filter_btn(s, x - 230, Y0 + 13, "Day", "Thu 1 Oct (tomorrow)", w=230) + 12

    ty = Y0 + 84
    th = H - 28 - ty
    # --- agents
    aw = 350
    card(s, X0, ty, aw, th, "Agents", "Kampala East · clients planned for Thu")
    plans = [("Sarah Namuli", "SN", 8, 21, True), ("Peter Kato", "PK", 7, 22, True), ("Ruth Achieng", "RA", 8, 24, True),
             ("Esther Nakato", "EN", 7, 22, True), ("Ivan Mugabe", "IM", 6, 18, False),
             ("Brian Ssali", "BS", 6, 19, False), ("Joan Auma", "JA", 3, 13, False)]
    y = ty + 78
    for nm, ini, n, wk, ok in plans:
        on = nm == "Sarah Namuli"
        with s.g(f"agent {nm}"):
            if on:
                s.rect(X0 + 10, y, aw - 20, 68, fill=tint(BRAND, 0.07), rx=10, stroke=tint(BRAND, 0.4))
            avatar(s, X0 + 40, y + 34, 17, ini, BRAND)
            s.text(X0 + 68, y + 29, nm, 14, 600, INK)
            s.text(X0 + 68, y + 48, f"Week: {wk} planned · min 20", 12, 400, GREEN_D if ok else RED)
            s.text(X0 + aw - 26, y + 36, str(n), 20, 700, INK if n >= 5 else RED, anchor="end")
            s.text(X0 + aw - 26, y + 53, "clients", 11, 400, MUTED, anchor="end")
        y += 74
    with s.g("warning"):
        s.rect(X0 + 16, y + 6, aw - 32, 84, fill=tint(AMBER, 0.12), rx=10)
        s.icon("alert", X0 + 30, y + 22, 20, AMBER_D, 2)
        para(s, X0 + 60, y + 34, "Joan has 3 clients planned. Add from her 9 interested clients waiting for KYC?",
             aw - 100, 12.5, 400, INK2, lh=18)

    # --- Sarah's plan, in visit order
    px = X0 + aw + 20
    pw = 620
    card(s, px, ty, pw, th, "Sarah Namuli · Thu 1 Oct", "8 clients in visit order · drag to reorder · "
                                                         "about 12.6 km")
    stops = [("08:30", "Charles Ssempijja", "Interested", "Follow-up", "Asked to come back after payday"),
             ("09:15", "Sarah Namutebi", "KYC captured", "Finish KYC", "Collect payslip, then validate"),
             ("10:00", "Betty Nakimuli", "KYC validated", "Offer loan", "School Fees Loan: 3 children"),
             ("10:45", "Juliet Kobusingye", "Interested", "From handover", "Was Daniel Okumu's client: introduce"),
             ("11:30", "Ivan Kasozi", "Negotiation", "Negotiate", "Wants 12 months; bring the new quote"),
             ("13:30", "Aisha Nalubega", "Interested", "Follow-up", "Bring National ID this time"),
             ("14:30", "Kyanja market", "Prospecting", "Prospecting", "New area · aim for 3 new clients"),
             ("16:00", "Annet Namubiru", "Negotiation", "Negotiate", "Compare with SACCO offer")]
    y = ty + 80
    rh = (th - 80 - 70) / len(stops)
    for i, (tm, nm, stage, reason, note) in enumerate(stops):
        with s.g(f"stop {i + 1} {nm}"):
            if i:
                s.line(px + 20, y, px + pw - 20, y, LINE2)
            s.icon("menu", px + 20, y + rh / 2 - 8, 16, FAINT, 2)
            s.circle(px + 60, y + rh / 2, 13, fill=BRAND)
            s.text(px + 60, y + rh / 2 + 4.5, str(i + 1), 12, 700, "#FFFFFF", anchor="middle")
            s.text(px + 86, y + rh / 2 - 4, nm, 14, 600, INK)
            s.text(px + 86, y + rh / 2 + 15, note, 12, 400, MUTED, maxw=260)
            chip(s, px + 360, y + rh / 2 - 11, reason, PLAN_REASON[reason], h=22, size=11)
            s.text(px + pw - 24, y + rh / 2 + 5, tm, 13, 600, INK2, anchor="end")
        y += rh
    with s.g("plan footer"):
        fy = ty + th - 60
        s.rect(px + 16, fy, pw - 32, 44, fill="#F5F5FB", rx=10)
        s.text(px + 32, fy + 27, "Starts 08:30 near Ntinda stage · ends about 16:40 · 21 clients this week (min 20 ✓)",
               12.5, 600, INK2)
    s.link(px, ty + 80, pw, rh, "w06")

    # --- map + suggestions
    rx = px + pw + 20
    rw = X1 - rx
    mh = 330
    card(s, rx, ty, rw, mh, "Route", "Planned order on the map")
    m = StreetMap(s, rx + 16, ty + 70, rw - 32, mh - 86, seed=5, lake=False, dense=0.8,
                  places=[("Ntinda", 0.25, 0.25), ("Kiwatule", 0.62, 0.2), ("Kyanja", 0.3, 0.8)])
    pts = [m.P(*q) for q in [(0.2, 0.3), (0.34, 0.18), (0.5, 0.26), (0.64, 0.34), (0.74, 0.52), (0.56, 0.62),
                             (0.34, 0.76), (0.18, 0.6)]]
    s.poly(pts, stroke=BRAND, sw=3, closed=False, dash="2 6", name="planned route")
    for i, (qx, qy) in enumerate(pts):
        map_pin(s, qx, qy, BRAND if i != 6 else "#8A8DA6", str(i + 1), 0.85, name=f"stop {i + 1}")
    sy = ty + mh + 16
    card(s, rx, sy, rw, H - 28 - sy, "Suggested to add", "Sarah's clients who need a visit but aren't planned")
    sugg = [("Hassan Mugerwa", "Interested 16 days, no KYC", "Follow-up"),
            ("Rehema Nakalema", "Moving from Daniel Okumu today", "From handover"),
            ("Paul Tumusiime", "Application returned: payslip", "Finish KYC"),
            ("Kigoowa stage", "No visits this quarter", "Prospecting")]
    y = sy + 80
    for nm, why, reason in sugg:
        with s.g(f"suggestion {nm}"):
            s.circle(rx + 30, y + 14, 5, fill=PLAN_REASON[reason])
            s.text(rx + 44, y + 12, nm, 13.5, 600, INK)
            s.text(rx + 44, y + 30, why, 12, 400, MUTED, maxw=rw - 150)
            button(s, rx + rw - 20, y, "Add", "soft", icon="plus", h=30, size=12, anchor="end")
        y += 50
    return s


# =====================================================================================
def w11_handover():
    s = shell("11 Agent handover (clients stay with Letshego)", "Agent handover", ["Planning", "Agent handover"],
              user=SUPERVISOR)
    page_head(s, "Agent handover", "When an agent leaves, their clients stay with Letshego and move to another agent "
                                   "with their full history")
    ty = Y0 + 84
    lw_ = 420
    card(s, X0, ty, lw_, H - 28 - ty, "Leaving agent", "Resigned · last day today · account locks at 18:00")
    with s.g("leaver"):
        s.circle(X0 + 70, ty + 130, 34, fill=LINE2)
        s.text(X0 + 70, ty + 140, "DO", 22, 700, MUTED, anchor="middle")
        s.text(X0 + 120, ty + 124, "Daniel Okumu", 20, 700, INK)
        status_chip(s, X0 + 120, ty + 136, "Leaving today", h=22, size=11)
        y = ty + 200
        for lab, val in [("Branch", "Kampala East"), ("Territory", "Namugongo · Kyaliwajjala"), ("Joined", "Jan 2024"),
                         ("Last check-in", "Today 10:12"), ("Clients owned", "46"),
                         ("Open applications", "2 (kept, not lost)")]:
            kv(s, X0 + 24, y, lw_ - 48, lab, val)
            y += 34
        s.text(X0 + 24, y + 20, "His 46 clients by stage", 14, 700, INK)
        y += 44
        for lab, n in [("Interested", 21), ("KYC captured", 6), ("KYC validated", 3), ("Negotiation", 4),
                       ("Applied", 2), ("Approved (active loans)", 10)]:
            col = STAGE.get(lab, BRAND_D)
            s.circle(X0 + 32, y - 4, 6, fill=col)
            s.text(X0 + 46, y, lab, 13, 400, INK2)
            s.text(X0 + lw_ - 24, y, str(n), 13, 700, INK, anchor="end")
            y += 30
        with s.g("safety note"):
            s.rect(X0 + 24, y + 6, lw_ - 48, 88, fill=tint(BRAND, 0.07), rx=10)
            s.icon("shield", X0 + 40, y + 24, 20, BRAND, 2)
            para(s, X0 + 70, y + 38, "Photos, KYC and notes were never kept only on his phone. Everything is on "
                                     "Letshego's servers; the phone is wiped at 18:00.", lw_ - 110, 12.5, 400, INK2,
                 lh=19)

    mx = X0 + lw_ + 20
    mw = 780
    card(s, mx, ty, mw, H - 28 - ty, "Reassign clients", "Suggested by territory and each agent's current load · "
                                                         "change any row")
    cols = [("", 44, "start"), ("Client", 210, "start"), ("Stage", 160, "start"), ("Location", 150, "start"),
            ("New agent", 200, "start")]
    clients = [("Moses Ssebunya", "Negotiation", "Namugongo", "Peter Kato"),
               ("Rehema Nakalema", "Interested", "Kyaliwajjala", "Ruth Achieng"),
               ("Hassan Mayanja", "KYC captured", "Namugongo", "Peter Kato"),
               ("Daniel Kiwanuka", "Approved", "Kira", "Ruth Achieng"),
               ("Scovia Adong", "Interested", "Bweyogerere", "Peter Kato"),
               ("Lydia Nyakato", "Applied", "Kyaliwajjala", "Ruth Achieng"),
               ("Emmanuel Wasike", "KYC validated", "Kireka", "Peter Kato"),
               ("Juliet Kobusingye", "Interested", "Namugongo", "Sarah Namuli"),
               ("Vincent Odongo", "Approved", "Kira", "Esther Nakato"),
               ("Grace Nakabugo", "Negotiation", "Bweyogerere", "Brian Ssali")]
    rows = []
    for nm, st, loc, new in clients:
        rows.append([(lambda: lambda s_, x, y, w, h: checkbox(s_, x + 16, y + h / 2 - 9, True))(), nm,
                     (lambda st_: lambda s_, x, y, w, h: chip(s_, x + 12, y + h / 2 - 11, st_,
                                                              STAGE.get(st_, GREEN_D), h=22, size=11, dot=True))(st),
                     loc,
                     (lambda n_: lambda s_, x, y, w, h: (s_.rect(x + 12, y + h / 2 - 16, w - 24, 32, fill=CARD, rx=6,
                                                                 stroke=LINE),
                                                         s_.text(x + 24, y + h / 2 + 5, n_, 13, 600, INK),
                                                         s_.icon("chevdown", x + w - 38, y + h / 2 - 8, 16,
                                                                 MUTED)))(new)])
    table(s, mx + 1, ty + 76, cols, rows, row_h=62, head_h=38)
    s.text(mx + 24, H - 50, "Showing 10 of 46 · all selected", 13, 400, MUTED)

    rx = mx + mw + 20
    rw = X1 - rx
    card(s, rx, ty, rw, H - 28 - ty, "Summary", "What happens when you confirm")
    y = ty + 96
    for nm, ini, n in [("Peter Kato", "PK", 17), ("Ruth Achieng", "RA", 14), ("Brian Ssali", "BS", 7),
                       ("Esther Nakato", "EN", 5), ("Sarah Namuli", "SN", 3)]:
        avatar(s, rx + 42, y, 16, ini, BRAND)
        s.text(rx + 68, y + 5, nm, 13.5, 600, INK)
        s.text(rx + rw - 24, y + 5, f"+{n} clients", 13, 600, BRAND, anchor="end")
        y += 44
    y += 6
    for t in ["Each new agent gets the full timeline, photos and notes", "Clients get an SMS introducing their new "
              "agent", "Conversions already made stay credited to Daniel", "The move is written to the audit trail"]:
        s.icon("check", rx + 24, y - 12, 16, GREEN, 2.6)
        para(s, rx + 48, y, t, rw - 80, 13, 400, INK2, lh=19)
        y += 46
    button(s, rx + 24, H - 100, "Confirm handover of 46 clients", "primary", icon="swap", w=rw - 48, h=48)
    s.link(rx + 24, H - 100, rw - 48, 48, "w06")
    return s


# =====================================================================================
def w12_users():
    s = shell("12 Users, roles and territories", "Users & territories", ["Admin", "Users & territories"])
    page_head(s, "Users, roles & territories", "Who can see and do what · scope limits each person to their "
                                               "territory, branch or region")
    with s.g("header actions"):
        button(s, X1, Y0 + 12, "Invite user", "primary", icon="userplus", anchor="end")
    ty = Y0 + 84
    rw_ = 1040
    card(s, X0, ty, rw_, 520, "Roles", "Permissions are configurable; these are the defaults we propose")
    roles = [("Field Sales Agent", "Own clients", 62), ("Branch Supervisor", "Branch", 14),
             ("Regional Manager", "Region", 4), ("HQ Credit Approver", "All · above limit", 3),
             ("Head of Sales / Management", "All branches", 5), ("System Admin", "Settings only", 2)]
    perms = ["Visits & KYC", "Approve", "Reassign", "Set plans", "Dashboards", "Users"]
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
    card(s, tx, ty, tw2, H - 28 - ty, "Territories: Kampala East", "Every client pin belongs to one territory and one agent")
    from charts import StreetMap
    m = StreetMap(s, tx + 16, ty + 76, tw2 - 32, 380, seed=5, dense=0.8,
                  places=[("Ntinda", 0.33, 0.3), ("Kiwatule", 0.6, 0.2), ("Kyambogo", 0.44, 0.52),
                          ("Kireka", 0.8, 0.5), ("Nakawa", 0.3, 0.72), ("Bukoto", 0.12, 0.35)])
    zones = [([(0.22, 0.12), (0.48, 0.1), (0.5, 0.38), (0.26, 0.42)], BRAND),
             ([(0.5, 0.05), (0.8, 0.08), (0.78, 0.36), (0.52, 0.38)], TEAL),
             ([(0.02, 0.2), (0.22, 0.12), (0.26, 0.42), (0.04, 0.5)], VIOLET),
             ([(0.26, 0.42), (0.5, 0.38), (0.56, 0.66), (0.3, 0.64)], AMBER),
             ([(0.52, 0.38), (0.78, 0.36), (0.96, 0.6), (0.6, 0.64)], GREEN),
             ([(0.04, 0.5), (0.3, 0.64), (0.34, 0.92), (0.06, 0.94)], RED)]
    for pts, col in zones:
        s.poly([m.P(*p) for p in pts], fill=col, op=0.14, stroke=col, name="territory")
    y = ty + 480
    for (nm, ini, st, t, v, c, terr), col in zip(TEAM[:6], [BRAND, TEAL, VIOLET, AMBER, GREEN, RED]):
        s.rect(tx + 24, y - 11, 14, 14, fill=col, op=0.5, rx=3)
        s.text(tx + 48, y, terr, 13, 600, INK)
        s.text(tx + tw2 - 24, y, nm, 13, 400, INK2, anchor="end")
        y += 32
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
            ["30 Sep 10:58", "Sarah Namuli", "Closed visit: not interested", "Joseph Kiggundu",
             "Reason: already has a SACCO loan", "Phone · Ntinda"],
            ["30 Sep 09:12", "Patricia Nankya", "Changed weekly minimum", "Kampala East", "Visits 15 → 20 a week",
             "Web · Head office"],
            ["12 Aug 17:05", "Moses Okello", "Reassigned 46 clients", "John Mugisha (left)", "→ 5 agents",
             "Web · Kampala"]]
    table(s, X0 + 1, ay + 76, cols, rows, row_h=(H - 28 - ay - 76 - 16) / 5 - 8, head_h=36)
    return s


SCREENS = [w07_approvals, w08_review, w09_reasons, w10_plans, w11_handover, w12_users, w13_reports]
