"""Web console screens (1920 x 1080): shell, sign in, overview, agents, agent profile, field map, pipeline, client."""
from __future__ import annotations

from charts import (BRANCHES, StreetMap, UgandaMap, agent_dot, donut, funnel, heat_strip, line_chart, map_pin,
                    perf_color, ring, sparkline)
from data import (AGENT, AGENTS, AGENTS_N, APPROVED, CLIENT, CONV_Q, CONV_SPLY, FUNNEL, MGMT, PENDING, QUARTER,
                  QUARTER_RANGE, REJECTED, SUPERVISOR, TARGET_Q, TEAM, VISITS_Q, WEEK_CONV, WEEK_DATES, WEEK_LABELS,
                  WEEK_VISITS, rnd_instalment, ugx)
from kit import (AMBER, AMBER_D, BG, BLUE, BRAND, BRAND_D, BRAND_M, CARD, FAINT, GREEN, GREEN_D, INK, INK2, LINE,
                 LINE2, MUTED, PRODUCT, PRODUCTS, RED, STAGE, STAGES, STATUS, SVG, TEAL, VIOLET, YELLOW, YELLOW_D,
                 avatar, button, card, checkbox, chip, field, para, progress, radio, shade, status_chip, table, tint,
                 toggle, triangle, tw, wordmark)

W, H = 1920, 1080
SB = 264
TOP = 68
X0 = SB + 32
X1 = W - 32
CW = X1 - X0
Y0 = TOP + 28

NAV = [
    ("SALES", [("Overview", "grid"), ("Agents", "users"), ("Field map", "map"), ("Client pipeline", "workflow")]),
    ("APPLICATIONS", [("Approvals", "listcheck"), ("Why & why not", "message")]),
    ("PLANNING", [("Journey plans & targets", "route"), ("Agent handover", "swap")]),
    ("ADMIN", [("Users & territories", "settings"), ("Reports & audit", "history")]),
]
NAV_TARGET = {"Overview": "w01", "Agents": "w02", "Field map": "w04", "Client pipeline": "w05", "Approvals": "w07",
              "Why & why not": "w09", "Journey plans & targets": "w10", "Agent handover": "w11",
              "Users & territories": "w12", "Reports & audit": "w13"}
BADGES = {"Agents": ("6", RED), "Approvals": ("14", YELLOW)}

SB_TEXT = "#D9D8F3"
SB_MUTED = "#9E9CD6"


def shell(title: str, active: str, crumbs: list[str], user=MGMT, period="Quarter"):
    s = SVG(W, H, title)
    s.rect(0, 0, W, H, fill=BG, name="page background")

    with s.g("sidebar"):
        s.rect(0, 0, SB, H, fill=BRAND, name="sidebar bg")
        # faint triangle watermark
        with s.g("sidebar watermark", opacity=0.07):
            s.poly([(SB - 20, H - 420), (SB + 120, H - 150), (SB - 170, H - 150)], fill="#FFFFFF")
        wordmark(s, 26, 50, 23, "#FFFFFF")
        s.text(26, 72, "Field Sales · Uganda", 12, 400, SB_MUTED, name="product sub")
        y = 110
        for group, items in NAV:
            s.text(28, y, group, 10.5, 600, SB_MUTED, spacing=1.2, name=f"nav group {group}")
            y += 14
            for label, ic in items:
                on = label == active
                with s.g(f"nav {label}"):
                    if on:
                        s.rect(14, y, SB - 28, 40, fill="#FFFFFF", op=0.12, rx=8, name="active bg")
                        s.rect(14, y + 10, 3, 20, fill=YELLOW, rx=1.5, name="active bar")
                    s.icon(ic, 30, y + 10, 20, YELLOW if on else SB_TEXT, 1.8)
                    s.text(62, y + 25, label, 14, 600 if on else 400, "#FFFFFF" if on else SB_TEXT, name="label")
                    if label in BADGES:
                        b, col = BADGES[label]
                        bw = tw(b, 11, 700) + 14
                        s.rect(SB - 30 - bw, y + 11, bw, 18, fill=col, rx=9, name="badge")
                        s.text(SB - 30 - bw / 2, y + 24, b, 11, 700, BRAND_D if col == YELLOW else "#FFFFFF",
                               anchor="middle", name="badge n")
                s.link(14, y, SB - 28, 40, NAV_TARGET.get(label))
                y += 42
            y += 12
        with s.g("field app card"):
            s.rect(16, H - 180, SB - 32, 88, fill="#FFFFFF", op=0.08, rx=10)
            s.rect(30, H - 166, 30, 30, fill=YELLOW, rx=8)
            s.icon("phone", 36, H - 160, 18, BRAND_D, 2)
            s.text(70, H - 146, "Agent field app", 13, 600, "#FFFFFF")
            s.text(30, H - 120, "Android · works offline · GPS", 12, 400, SB_TEXT)
            s.text(30, H - 102, "NIRA ID capture · open it →", 12, 400, SB_TEXT)
        s.link(16, H - 180, SB - 32, 88, "m03")
        # demo shortcut: click the name to switch between management and supervisor views
        s.link(0, H - 76, SB - 56, 76, "w07" if user == MGMT else "w01")
        s.link(SB - 52, H - 60, 40, 44, "w00")
        with s.g("sidebar user"):
            s.rect(0, H - 76, SB, 76, fill=BRAND_D, name="user bg")
            s.circle(44, H - 38, 18, fill=YELLOW)
            s.text(44, H - 32, user[2], 14, 700, BRAND_D, anchor="middle")
            s.text(72, H - 42, user[0], 14, 600, "#FFFFFF")
            s.text(72, H - 23, user[1], 11.5, 400, SB_MUTED, maxw=SB - 128)
            s.rect(SB - 50, H - 58, 38, 38, fill="#FFFFFF", op=0.1, rx=8, name="sign out button")
            s.icon("logout", SB - 41, H - 49, 20, "#FFB4B4", 2)

    with s.g("top bar"):
        s.rect(SB, 0, W - SB, TOP, fill=CARD, name="top bar bg")
        s.line(SB, TOP, W, TOP, LINE)
        x = X0
        for i, c in enumerate(crumbs):
            last = i == len(crumbs) - 1
            x += s.text(x, 40, c, 14, 600 if last else 400, INK if last else MUTED, name=f"crumb {c}")
            if not last:
                s.icon("chevright", x + 6, 29, 16, FAINT)
                x += 28
        rx = X1
        avatar(s, rx - 18, 34, 18, user[2], BRAND)
        rx -= 52
        s.line(rx, 20, rx, 48, LINE)
        rx -= 44
        with s.g("notifications"):
            s.icon("bell", rx, 23, 22, INK2)
            s.circle(rx + 19, 25, 7, fill=RED)
            s.text(rx + 19, 29, "5", 10, 700, "#FFFFFF", anchor="middle")
        rx -= 290
        with s.g("search"):
            s.rect(rx, 16, 266, 36, fill="#F4F5FA", rx=8, stroke=LINE)
            s.icon("search", rx + 12, 25, 18, MUTED)
            s.text(rx + 40, 39, "Search clients, agents, app IDs…", 13, 400, FAINT)
        # the period switch the client asked for: day, week, quarter, year
        pw = seg_width(["Day", "Week", "Quarter", "Year"])
        rx -= pw + 20
        seg(s, rx, 16, ["Day", "Week", "Quarter", "Year"], period, h=36)
        lab = {"Day": "Wed 30 Sep 2026", "Week": "W13 · 23–30 Sep", "Quarter": f"{QUARTER} · {QUARTER_RANGE}",
               "Year": "FY 2026 · Jan–Dec"}[period]
        lw = tw(lab, 13, 600) + 50
        rx -= lw + 12
        with s.g("date range"):
            s.rect(rx, 16, lw, 36, fill=CARD, rx=8, stroke=LINE)
            s.icon("calendar", rx + 12, 25, 18, BRAND)
            s.text(rx + 38, 39, lab, 13, 600, INK)
    return s


def seg_width(items, size=13):
    return sum(tw(i, size, 600) + 28 for i in items) + 8


def seg(s: SVG, x, y, items, active, h=36, size=13, name="segmented control"):
    with s.g(name):
        w = seg_width(items, size)
        s.rect(x, y, w, h, fill="#F1F2F8", rx=8, stroke=LINE)
        cx = x + 4
        for it in items:
            iw = tw(it, size, 600) + 28
            if it == active:
                s.rect(cx, y + 4, iw, h - 8, fill=BRAND, rx=6)
            s.text(cx + iw / 2, y + h / 2 + size * 0.36, it, size, 600, "#FFFFFF" if it == active else INK2,
                   anchor="middle")
            cx += iw
    return w


def page_head(s: SVG, title, subtitle, y=Y0):
    s.text(X0, y + 30, title, 26, 700, INK, name="page title")
    s.text(X0, y + 56, subtitle, 14, 400, MUTED, name="page subtitle")


def filter_btn(s: SVG, x, y, label, value, w=None):
    lw = tw(label + ":", 13)
    vw = tw(value, 13, 600)
    bw = w or lw + vw + 54
    with s.g(f"filter {label}"):
        s.rect(x, y, bw, 38, fill=CARD, rx=8, stroke=LINE)
        s.text(x + 14, y + 24, label + ":", 13, 400, MUTED)
        s.text(x + 18 + lw, y + 24, value, 13, 600, INK, maxw=bw - lw - 50)
        s.icon("chevdown", x + bw - 28, y + 11, 16, MUTED)
    return bw


def rule_note(s: SVG, x, y, text="Conversion = application submitted with all items", icon="check", color=GREEN):
    w = tw(text, 12, 600) + 42
    with s.g("rule note"):
        s.rect(x, y, w, 28, fill=tint(color, 0.1), rx=14)
        s.icon(icon, x + 11, y + 6, 16, color, 2.4)
        s.text(x + 32, y + 18.5, text, 12, 600, shade(color, 0.2))
    return w


def kpi(s: SVG, x, y, w, h, icon, color, label, value, sub, frac=None, tag=None, delta=None, delta_bad=False):
    with s.g(f"kpi {label}"):
        s.rect(x, y, w, h, fill=CARD, rx=12, stroke=LINE, name="bg")
        s.rect(x + 20, y + 20, 38, 38, fill=tint(color, 0.13), rx=9, name="icon bg")
        s.icon(icon, x + 29, y + 29, 20, shade(color, 0.1), 2)
        s.text(x + 70, y + 36, label, 13, 600, INK2, maxw=w - 90)
        if tag:
            chip(s, x + 70, y + 43, tag, color, h=20, size=11)
        vw = s.text(x + 20, y + 98, value, 30, 700, INK, name="value")
        if delta:
            col = RED if delta_bad else GREEN
            s.icon("trenddown" if delta_bad else "trendup", x + 28 + vw, y + 80, 16, col, 2.2)
            s.text(x + 48 + vw, y + 94, delta, 12, 600, col, name="delta")
        s.text(x + 20, y + 120, sub, 12.5, 400, MUTED, name="sub", maxw=w - 40)
        if frac is not None:
            progress(s, x + 20, y + h - 14, w - 40, frac, color, h=6)


def agent_cell(name, ini, sub, color=BRAND):
    def f(s_, x, y, w, h):
        avatar(s_, x + 30, y + h / 2, 16, ini, color)
        s_.text(x + 56, y + h / 2 - 2, name, 13.5, 600, INK, maxw=w - 64)
        s_.text(x + 56, y + h / 2 + 15, sub, 12, 400, MUTED, maxw=w - 64)
    return f


def chip_cell(label, color=None, status=True):
    def f(s_, x, y, w, h):
        if status:
            status_chip(s_, x + 12, y + h / 2 - 11, label, h=22, size=11)
        else:
            chip(s_, x + 12, y + h / 2 - 11, label, color, h=22, size=11)
    return f


def kv(s: SVG, x, y, w, label, value, vcolor=INK, size=13.5, bold=True):
    s.text(x, y, label, 13, 400, MUTED, name="label")
    s.text(x + w, y, value, size, 600 if bold else 400, vcolor, anchor="end", name="value", maxw=w * 0.62)


def doc_thumb(s: SVG, x, y, w, h, kind, label, ok=True):
    """Illustrative document photo: an ID card, a face, a shop, a payslip or a logbook."""
    with s.g(f"document {label}"):
        s.rect(x, y, w, h, fill="#EEF0F6", rx=8, stroke=LINE)
        ix, iy, iw, ih = x + 8, y + 8, w - 16, h - 40
        if kind in ("id_front", "id_back"):
            s.rect(ix, iy, iw, ih, fill="#E6ECE0", rx=6, stroke="#C9D3BF")
            s.rect(ix, iy, iw, ih * 0.18, fill="#1C1C1C", rx=6, op=0.85)
            s.rect(ix + iw * 0.06, iy + ih * 0.32, iw * 0.08, ih * 0.08, fill="#D72222")
            s.rect(ix + iw * 0.14, iy + ih * 0.32, iw * 0.08, ih * 0.08, fill="#FCDC04")
            if kind == "id_front":
                s.rect(ix + iw * 0.06, iy + ih * 0.46, iw * 0.26, ih * 0.44, fill="#B9A58E", rx=3)
                s.circle(ix + iw * 0.19, iy + ih * 0.6, ih * 0.09, fill="#6B4F3A")
                for k in range(4):
                    s.rect(ix + iw * 0.38, iy + ih * (0.32 + k * 0.14), iw * (0.5 - k * 0.07), ih * 0.06,
                           fill="#8A937F", rx=2)
            else:
                for k in range(3):
                    s.rect(ix + iw * 0.06, iy + ih * (0.62 + k * 0.1), iw * 0.88, ih * 0.05, fill="#6D745F", rx=1)
                s.rect(ix + iw * 0.66, iy + ih * 0.26, iw * 0.26, iw * 0.26, fill="#FFFFFF", stroke="#6D745F")
        elif kind == "selfie":
            s.rect(ix, iy, iw, ih, fill="#C7D3E6", rx=6)
            s.circle(ix + iw / 2, iy + ih * 0.42, ih * 0.2, fill="#7A5638")
            s.path(f"M{ix + iw * 0.22:.1f} {iy + ih:.1f} C{ix + iw * 0.25:.1f} {iy + ih * 0.7:.1f} "
                   f"{ix + iw * 0.75:.1f} {iy + ih * 0.7:.1f} {ix + iw * 0.78:.1f} {iy + ih:.1f} Z", fill="#D9642E")
            s.rect(ix + iw * 0.2, iy + ih * 0.12, iw * 0.6, ih * 0.66, fill="none", rx=ih * 0.3, stroke="#FFFFFF",
                   sw=1.5, dash="4 3")
        elif kind == "shop":
            s.rect(ix, iy, iw, ih, fill="#BFD7EA", rx=6)
            s.rect(ix + iw * 0.1, iy + ih * 0.3, iw * 0.8, ih * 0.7, fill="#E9D8B4")
            s.rect(ix + iw * 0.06, iy + ih * 0.22, iw * 0.88, ih * 0.14, fill=BRAND_M)
            for k in range(4):
                s.rect(ix + iw * (0.14 + k * 0.19), iy + ih * 0.46, iw * 0.14, ih * 0.54,
                       fill=["#D84F6F", "#3F8FD2", "#F2B705", "#4BA36B"][k])
        elif kind == "doc":
            s.rect(ix + iw * 0.18, iy, iw * 0.64, ih, fill="#FFFFFF", stroke="#D5D8E4")
            for k in range(7):
                s.rect(ix + iw * 0.25, iy + ih * (0.12 + k * 0.11), iw * (0.5 if k % 3 else 0.32), ih * 0.04,
                       fill="#B5B9CC", rx=1)
        elif kind == "moto":
            s.rect(ix, iy, iw, ih, fill="#D8E4D0", rx=6)
            s.circle(ix + iw * 0.28, iy + ih * 0.72, ih * 0.16, fill="none", stroke="#333", sw=3)
            s.circle(ix + iw * 0.74, iy + ih * 0.72, ih * 0.16, fill="none", stroke="#333", sw=3)
            s.path(f"M{ix + iw * 0.28:.1f} {iy + ih * 0.72:.1f} L{ix + iw * 0.45:.1f} {iy + ih * 0.45:.1f} "
                   f"L{ix + iw * 0.66:.1f} {iy + ih * 0.45:.1f} L{ix + iw * 0.74:.1f} {iy + ih * 0.72:.1f}",
                   stroke="#C62828", sw=4)
        s.text(x + 10, y + h - 13, label, 12, 600, INK, maxw=w - 34, name="caption")
        if ok:
            s.circle(x + w - 16, y + h - 17, 8, fill=GREEN)
            s.icon("check", x + w - 21, y + h - 22, 10, "#FFFFFF", 3.4)


# =====================================================================================
def w00_sign_in():
    s = SVG(W, H, "00 Sign in")
    s.rect(0, 0, W, H, fill=CARD, name="page background")
    with s.g("brand panel"):
        s.rect(0, 0, 880, H, fill=BRAND, name="brand bg")
        with s.g("facets", opacity=0.10):
            s.poly([(560, 380), (980, 1080), (180, 1080)], fill="#FFFFFF")
            s.poly([(760, 120), (1000, 560), (560, 560)], fill="#FFFFFF")
        with s.g("route illustration"):
            pts = [(140, 930), (300, 860), (420, 900), (560, 800), (700, 850)]
            s.poly(pts, stroke=YELLOW, sw=3, closed=False, dash="2 9")
            for i, (px, py) in enumerate(pts):
                map_pin(s, px, py, [GREEN, BLUE, RED, GREEN, YELLOW][i], None, 1.25, name=f"visit {i + 1}")
        wordmark(s, 80, 116, 34, "#FFFFFF")
        s.text(82, 146, "Field Sales · Uganda", 16, 400, "#C9C8EE")
        s.text(80, 290, "Every client visit,", 46, 700, "#FFFFFF", name="headline 1")
        s.text(80, 346, "every week of the quarter.", 46, 700, YELLOW, name="headline 2")
        para(s, 80, 400, "Agents record each visit, KYC and application from the phone. Supervisors approve the same "
                         "day. Management sees who is bringing in clients, and who isn't, while there is still time "
                         "to act.", 640, 17, 400, "#DCDBF6", lh=28)
        y = 540
        for ic, t in [("pin", "GPS-stamped visits and client locations"),
                      ("idcard", "KYC with NIRA ID photos, earnings and collateral"),
                      ("shield", "Client records belong to Letshego, not to the agent")]:
            s.rect(80, y - 21, 34, 34, fill="#FFFFFF", op=0.12, rx=8)
            s.icon(ic, 88, y - 13, 18, YELLOW, 2)
            s.text(128, y + 1, t, 16, 400, "#FFFFFF")
            y += 52
        s.text(80, H - 48, "Letshego Uganda · Improving lives · Prototype with illustrative data", 12.5, 400, "#A9A8DC",
               name="footer")

    fx = 880 + (W - 880 - 440) / 2
    with s.g("sign-in form"):
        s.text(fx, 250, "Sign in", 32, 700, INK)
        s.text(fx, 282, "Letshego staff: head office, branches and field.", 15, 400, MUTED)
        button(s, fx, 318, "Continue with Microsoft (Letshego staff)", "secondary", icon="sparkle", w=440, h=48)
        with s.g("divider"):
            s.line(fx, 400, fx + 190, 400, LINE)
            s.text(fx + 220, 405, "or", 13, 400, MUTED, anchor="middle")
            s.line(fx + 250, 400, fx + 440, 400, LINE)
        field(s, fx, 428, 440, "Staff ID", "LU-0142", h=48, icon="user")
        field(s, fx, 512, 440, "Password", "••••••••••••", h=48, icon="lock")
        s.text(fx + 440, 526, "Forgot password?", 13, 600, BRAND, anchor="end")
        checkbox(s, fx, 604, True)
        s.text(fx + 28, 618, "Keep me signed in on this computer", 13, 400, INK2)
        button(s, fx, 646, "Sign in", "primary", w=440, h=48, size=15)
        s.link(fx, 646, 440, 48, "w01")
        s.link(fx, 318, 440, 48, "w01")
        with s.g("2FA note"):
            s.rect(fx, 722, 440, 64, fill="#F6F7FB", rx=10, stroke=LINE)
            s.icon("fingerprint", fx + 16, 742, 22, BRAND, 1.8)
            s.text(fx + 52, 748, "Two-step verification is on", 13, 600, INK)
            s.text(fx + 52, 768, "We'll send a code to your Letshego phone next.", 12, 400, MUTED)
        with s.g("app link"):
            s.text(fx, 846, "Field agent?", 13, 400, MUTED)
            s.text(fx + tw("Field agent? ", 13), 846, "Open the Android app →", 13, 600, BRAND)
            s.link(fx, 830, 300, 24, "m01")
    s.text(880 + (W - 880) / 2, H - 48, "Client data protected under Uganda's Data Protection and Privacy Act, 2019",
           12, 400, MUTED, anchor="middle")
    return s


# =====================================================================================
def w01_overview():
    s = shell("01 Sales overview", "Overview", ["Sales", "Overview"])
    page_head(s, "Sales overview", f"All 14 branches · {AGENTS_N} field agents · {QUARTER} ({QUARTER_RANGE}) · "
                                   "week 13 of 13")
    with s.g("header actions"):
        x = X1
        x -= button(s, x, Y0 + 12, "Export", "primary", icon="download", anchor="end") + 12
        x -= filter_btn(s, x - 170, Y0 + 13, "Product", "All", w=170) + 12
        x -= filter_btn(s, x - 190, Y0 + 13, "Branch", "All branches", w=190) + 16
        rule_note(s, x - 336, Y0 + 18)

    ky = Y0 + 84
    kw = (CW - 5 * 16) / 6
    active = AGENTS_N - 6
    kpis = [
        ("pin", BRAND, "Client visits", f"{VISITS_Q:,}", "6,930 different clients", 0.90, "Plan 9,300", None, False),
        ("hand", BLUE, "Interested", f"{FUNNEL[1][1]:,}", f"{FUNNEL[1][1] / VISITS_Q:.0%} of visits", None, None,
         None, False),
        ("idcard", TEAL, "KYC validated", f"{FUNNEL[3][1]:,}", f"{FUNNEL[3][1] / FUNNEL[2][1]:.0%} of KYC captured",
         None, None, None, False),
        ("check", GREEN, "Conversions", f"{CONV_Q:,}", f"of {TARGET_Q:,} target · {CONV_Q / TARGET_Q:.0%}",
         CONV_Q / TARGET_Q, "Applications", f"+{CONV_Q / CONV_SPLY - 1:.0%} vs Q3 2025", False),
        ("shield", VIOLET, "Approval rate", f"{APPROVED / (APPROVED + REJECTED):.0%}",
         f"{APPROVED} approved · {REJECTED} rejected", None, None, None, False),
        ("users", RED, "Active agents", f"{active} / {AGENTS_N}", "6 silent: no visit in 14+ days", active / AGENTS_N,
         None, None, False),
    ]
    for i, (ic, col, lab, val, sub, fr, tag, d, bad) in enumerate(kpis):
        kpi(s, X0 + i * (kw + 16), ky, kw, 150, ic, col, lab, val, sub, fr, tag, d, bad)
    for i, tgt in enumerate(["w04", "w05", "w05", "w05", "w07", "w02"]):
        s.link(X0 + i * (kw + 16), ky, kw, 150, tgt)

    # ---- quarter rhythm
    ry = ky + 166
    rw = 1010
    card(s, X0, ry, rw, 370, "Quarter rhythm: visits and conversions by week",
         "The pattern behind the problem: busy in week 1, quiet mid-quarter, a rush in the last three weeks")
    with s.g("legend"):
        lx = X0 + rw - 330
        s.rect(lx, ry + 28, 14, 12, fill=tint(BRAND, 0.35), rx=2)
        s.text(lx + 20, ry + 39, "Visits", 12, 600, INK2)
        s.line(lx + 80, ry + 34, lx + 100, ry + 34, GREEN, 3)
        s.text(lx + 106, ry + 39, "Conversions", 12, 600, INK2)
        s.line(lx + 200, ry + 34, lx + 220, ry + 34, INK2, 2, dash="5 4")
        s.text(lx + 226, ry + 39, "Even pace to target", 12, 400, INK2)
    cx0, cy0, cw_, ch_ = X0 + 70, ry + 100, rw - 130, 210
    n = 13
    colw = cw_ / n
    vmax = 1800
    cmax = 330
    with s.g("slump band"):
        s.rect(cx0 + colw * 2, cy0 - 10, colw * 7, ch_ + 10, fill=tint(RED, 0.07), rx=6)
        s.text(cx0 + colw * 5.5, cy0 + 8, "Mid-quarter slump", 12.5, 700, shade(RED, 0.1), anchor="middle")
        drop = 1 - min(WEEK_VISITS[2:9]) / WEEK_VISITS[0]
        s.text(cx0 + colw * 5.5, cy0 + 26, f"visits down {drop:.0%} from week 1", 12, 400, shade(RED, 0.05),
               anchor="middle")
    with s.g("axes"):
        for k in range(4):
            yy = cy0 + ch_ - ch_ * k / 3
            s.line(cx0, yy, cx0 + cw_, yy, LINE2 if k else LINE)
            s.text(cx0 - 10, yy + 4, f"{int(vmax * k / 3):,}", 11, 400, MUTED, anchor="end")
            s.text(cx0 + cw_ + 10, yy + 4, f"{int(cmax * k / 3)}", 11, 400, GREEN, name="conv axis")
        s.text(cx0 - 10, cy0 - 22, "Visits", 11, 600, MUTED, anchor="end")
        s.text(cx0 + cw_ + 10, cy0 - 22, "Conv.", 11, 600, GREEN)
    with s.g("visit bars"):
        for i, v in enumerate(WEEK_VISITS):
            bh = ch_ * v / vmax
            s.rect(cx0 + i * colw + colw * 0.2, cy0 + ch_ - bh, colw * 0.6, bh, fill=tint(BRAND, 0.35), rx=3)
            s.text(cx0 + i * colw + colw / 2, cy0 + ch_ + 18, WEEK_LABELS[i], 11, 600, INK2, anchor="middle")
            if i % 2 == 0:
                s.text(cx0 + i * colw + colw / 2, cy0 + ch_ + 33, WEEK_DATES[i], 10.5, 400, MUTED, anchor="middle")
    with s.g("pace line"):
        py = cy0 + ch_ - ch_ * (TARGET_Q / 13) / cmax
        s.line(cx0, py, cx0 + cw_, py, INK2, 1.6, dash="5 4")
        s.text(cx0 + cw_ - 4, py - 6, f"{TARGET_Q / 13:.0f} / week", 11, 600, INK2, anchor="end")
    with s.g("conversion line"):
        pts = [(cx0 + i * colw + colw / 2, cy0 + ch_ - ch_ * v / cmax) for i, v in enumerate(WEEK_CONV)]
        s.poly(pts, stroke=GREEN, sw=2.6, closed=False)
        for p in pts:
            s.circle(*p, 3.5, fill=CARD, stroke=GREEN, sw=2)
    s.link(X0, ry, rw, 370, "w02")

    # ---- funnel
    fx = X0 + rw + 20
    fw = X1 - fx
    card(s, fx, ry, fw, 370, "Client journey funnel", f"{QUARTER} · all branches · a conversion = application "
                                                        "submitted", action="Pipeline →")
    rows = [(lab, v, STAGE[lab]) for lab, v in FUNNEL]
    funnel(s, fx + 24, ry + 86, fw - 48, rows, row_h=34, gap=13, label_w=118)
    s.link(fx, ry, fw, 370, "w05")

    # ---- bottom row: branches + attention
    by = ry + 386
    bh = H - 28 - by
    bw = 830
    card(s, X0, by, bw, bh, "Branches: conversions against target", f"{QUARTER} · colour = % of target reached",
         action="All branches →")
    mp = UgandaMap(X0 + 8, by + 62, 250, bh - 100)
    mp.draw_base(s)
    mp.draw_branches(s)
    with s.g("map legend"):
        lx, ly = X0 + 24, by + bh - 22
        for lab, col in [("≥85%", GREEN), ("60–84%", AMBER), ("<60%", RED)]:
            s.rect(lx, ly - 10, 12, 12, fill=col, op=0.75, rx=3)
            lx += s.text(lx + 17, ly, lab, 11, 400, INK2) + 30
    brs = sorted(BRANCHES.items(), key=lambda kv_: -kv_[1][3] / kv_[1][4])
    tx = X0 + 280
    cols = [("Branch", 170, "start"), ("Agents", 70, "end"), ("Conversions vs target", 250, "start"),
            ("%", 60, "end")]
    rws = []
    for br, (dist, reg, ag, conv, tgt) in brs[:4] + brs[-3:]:
        fr = conv / tgt
        rws.append([br, str(ag),
                    (lambda fr_, c_, t_: lambda s_, x, y, w, h: (progress(s_, x + 16, y + h / 2 - 3, 140, fr_,
                                                                            perf_color(fr_), h=7),
                                                                   s_.text(x + 166, y + h / 2 + 5, f"{c_} / {t_}", 12.5,
                                                                           400, INK2)))(fr, conv, tgt),
                    f"{fr:.0%}"])
    table(s, tx, by + 64, cols, rws, row_h=(bh - 64 - 36 - 8) / 7, head_h=34, size=13)
    s.link(X0, by, bw, bh, "w02")

    ax = X0 + bw + 20
    aw = X1 - ax
    card(s, ax, by, aw, bh, "Agents needing attention", "Flagged automatically every morning · 6 silent, 10 behind",
         action="All agents →")
    flags = [
        ("Rose Candiru", "RC", "Arua", "No visit for 19 days", "Silent", "Last check-in 11 Sep"),
        ("Denis Okiror", "DO", "Soroti", "No visit for 13 days", "Silent", "2 conversions of 24"),
        ("Brian Ssali", "BS", "Kampala East", "No visits weeks 4–9", "Behind", "5 of 22 · 23%"),
        ("Samuel Wandera", "SW", "Mbale", "Visits 4× below plan mid-quarter", "Behind", "9 of 24 · 38%"),
        ("Fred Opio", "FO", "Gulu", "KYC started, never completed (11)", "Behind", "8 of 21 · 38%"),
    ]
    rh = (bh - 80) / len(flags)
    for i, (nm, ini, br, why, st, sub) in enumerate(flags):
        yy = by + 72 + i * rh
        with s.g(f"flag {nm}"):
            if i:
                s.line(ax + 24, yy, ax + aw - 24, yy, LINE2)
            avatar(s, ax + 44, yy + rh / 2, 17, ini, RED if st == "Silent" else AMBER_D)
            s.text(ax + 72, yy + rh / 2 - 3, nm, 14, 600, INK)
            s.text(ax + 72 + tw(nm, 14, 600) + 8, yy + rh / 2 - 3, "· " + br, 12.5, 400, MUTED)
            s.text(ax + 72, yy + rh / 2 + 16, why, 12.5, 400, INK2, maxw=290)
            status_chip(s, ax + aw - 330, yy + rh / 2 - 11, st, h=22, size=11)
            s.text(ax + aw - 244, yy + rh / 2 + 5, sub, 12.5, 400, INK2, maxw=132)
            button(s, ax + aw - 24, yy + rh / 2 - 15, "Call", "soft", icon="phone", h=30, size=12, anchor="end")
    s.link(ax, by, aw, bh, "w02")
    return s


# =====================================================================================
def w02_agents():
    s = shell("02 Agents performance", "Agents", ["Sales", "Agents"])
    page_head(s, "Agents", f"{AGENTS_N} field agents · {QUARTER} · conversions against each agent's target, and "
                           "how steady their visits were week by week")
    with s.g("header actions"):
        x = X1
        x -= button(s, x, Y0 + 12, "Export", "secondary", icon="download", anchor="end") + 12
        x -= filter_btn(s, x - 200, Y0 + 13, "Sort", "Conversions ↓", w=200) + 12
        x -= filter_btn(s, x - 190, Y0 + 13, "Branch", "All branches", w=190) + 12
        with s.g("search agents"):
            s.rect(x - 250, Y0 + 13, 250, 38, fill=CARD, rx=8, stroke=LINE)
            s.icon("search", x - 238, Y0 + 23, 18, MUTED)
            s.text(x - 210, Y0 + 37, "Search agents", 13, 400, FAINT)

    sy = Y0 + 84
    sw_ = (CW - 3 * 16) / 4
    stats = [("On track", "≥ 85% of target", 21, GREEN, "trendup"),
             ("At risk", "60–84% of target", 25, AMBER, "gauge"),
             ("Behind", "under 60% of target", 10, RED, "trenddown"),
             ("Silent", "no visit in 14+ days", 6, "#8E1F1F", "userx")]
    for i, (lab, sub, n, col, ic) in enumerate(stats):
        x = X0 + i * (sw_ + 16)
        with s.g(f"stat {lab}"):
            s.rect(x, sy, sw_, 92, fill=CARD, rx=12, stroke=LINE if i < 3 else tint(RED, 0.5),
                   sw=1 if i < 3 else 1.5)
            s.rect(x + 20, sy + 24, 44, 44, fill=tint(col, 0.12), rx=10)
            s.icon(ic, x + 31, sy + 35, 22, col, 2)
            s.text(x + 80, sy + 42, lab, 14, 600, INK2)
            s.text(x + 80, sy + 64, sub, 12.5, 400, MUTED)
            s.text(x + sw_ - 24, sy + 58, str(n), 32, 700, col, anchor="end")
            progress(s, x + 80, sy + 76, sw_ - 170, n / AGENTS_N, col, h=5)

    ty = sy + 112
    with s.g("tabs"):
        seg(s, X0, ty, ["All 62", "Silent 6", "Behind 10", "At risk 25", "On track 21"], "All 62", h=38)
        s.text(X1, ty + 24, "Weekly visits: darker = more visits · red outline = no visits that week", 12.5, 400,
               MUTED, anchor="end")
    tby = ty + 54
    cols = [("Agent", 290, "start"), ("Territory", 190, "start"), ("Weekly visits W1–W13", 270, "start"),
            ("Visits", 90, "end"), ("Conv.", 80, "end"), ("Conversions vs target", 230, "start"),
            ("Conv. rate", 100, "end"), ("Last check-in", 160, "start"), ("Status", 182, "start")]
    rows = []
    for (nm, ini, br, terr, v, c, t, wk, last, st) in AGENTS:
        col = {"On track": BRAND, "At risk": AMBER_D, "Behind": RED, "Silent": "#8E1F1F"}[st]
        rows.append([
            agent_cell(nm, ini, br, col), terr,
            (lambda wk_: lambda s_, x, y, w, h: heat_strip(s_, x + 16, y + h / 2 - 8, wk_, cell=15, gap=4,
                                                            max_v=30, h=16))(wk),
            f"{v}", f"{c}",
            (lambda fr_, c_, t_: lambda s_, x, y, w, h: (progress(s_, x + 16, y + h / 2 - 3, 120, fr_,
                                                                    perf_color(fr_), h=7),
                                                           s_.text(x + 146, y + h / 2 + 5, f"{c_}/{t_} · {fr_:.0%}",
                                                                   12.5, 400, INK2)))(c / t, c, t),
            f"{c / v:.1%}", last, chip_cell(st)])
    table(s, X0, tby, cols, rows, row_h=(H - 28 - tby - 40 - 44) / len(rows), head_h=40, size=13, hl=0)
    s.link(X0, tby + 40, CW, (H - 28 - tby - 40 - 44) / len(rows), "w03")
    with s.g("table footer"):
        s.text(X0 + 16, H - 44, f"Showing 12 of {AGENTS_N} agents", 13, 400, MUTED)
        s.text(X1 - 16, H - 44, "1  2  3  4  5  6  →", 13, 600, BRAND, anchor="end")
    return s


# =====================================================================================
def w03_agent():
    nm, role, ini = AGENT
    s = shell("03 Agent profile (Sarah Namuli)", "Agents", ["Sales", "Agents", nm])
    with s.g("profile header"):
        s.rect(X0, Y0, CW, 118, fill=CARD, rx=12, stroke=LINE)
        s.circle(X0 + 64, Y0 + 59, 38, fill=tint(BRAND, 0.15))
        s.text(X0 + 64, Y0 + 70, ini, 28, 700, BRAND, anchor="middle")
        s.text(X0 + 120, Y0 + 50, nm, 24, 700, INK)
        status_chip(s, X0 + 128 + tw(nm, 24, 700), Y0 + 30, "On track")
        s.text(X0 + 120, Y0 + 76, f"{role} · Kampala East branch · territory Ntinda · Kiwatule · joined Mar 2024",
               14, 400, INK2)
        s.text(X0 + 120, Y0 + 98, "Supervisor Moses Okello · staff ID LU-0877 · device: Samsung A15 (registered)", 13,
               400, MUTED)
        x = X1 - 24
        x -= button(s, x, Y0 + 39, "Reassign clients", "secondary", icon="swap", anchor="end") + 10
        s.link(x, Y0 + 39, 170, 40, "w11")
        x -= button(s, x, Y0 + 39, "Today's route", "secondary", icon="map", anchor="end") + 10
        s.link(x, Y0 + 39, 150, 40, "w04")
        button(s, x, Y0 + 39, "Call", "primary", icon="phone", anchor="end")
    ky = Y0 + 136
    kw = (CW - 4 * 16) / 5
    k = [("pin", BRAND, "Visits this quarter", "214", "plan 240 · 89%", 214 / 240),
         ("check", GREEN, "Conversions", "19 / 22", "86% of target · rank 3 of 62", 19 / 22),
         ("activity", TEAL, "Conversion rate", "8.9%", "company average 12.5%", None),
         ("route", VIOLET, "Journey plan kept", "82%", "planned visits actually made", 0.82),
         ("clock", AMBER, "Avg. KYC time", "18 min", "from check-in to KYC validated", None)]
    for i, (ic, col, lab, val, sub, fr) in enumerate(k):
        kpi(s, X0 + i * (kw + 16), ky, kw, 140, ic, col, lab, val, sub, fr)

    ry = ky + 156
    lw_ = 1000
    card(s, X0, ry, lw_, 330, "Week by week", "Sarah's visits stayed steady all quarter; the dashed line is the branch "
                                              "average")
    px = line_chart(s, X0 + 20, ry + 90, lw_ - 50, 190, [
        ([12, 10, 5, 3, 3, 3, 3, 4, 5, 7, 12, 14, 16], INK2, "Branch average (last year style)", False),
        (AGENTS[0][7], BRAND, "Sarah visits", True),
    ], WEEK_LABELS, 30, 10)
    with s.g("legend"):
        lx = X0 + lw_ - 300
        s.line(lx, ry + 34, lx + 20, ry + 34, BRAND, 3)
        s.text(lx + 26, ry + 39, "Sarah: visits", 12, 600, INK2)
        s.line(lx + 130, ry + 34, lx + 150, ry + 34, INK2, 2, dash="5 4")
        s.text(lx + 156, ry + 39, "Branch average", 12, 400, INK2)
    # funnel
    fx = X0 + lw_ + 20
    fw = X1 - fx
    card(s, fx, ry, fw, 330, "Sarah's funnel", f"{QUARTER} · her own clients")
    funnel(s, fx + 24, ry + 82, fw - 48, [("Visited", 214, STAGE["Visited"]), ("Interested", 71, BLUE),
                                          ("KYC captured", 38, VIOLET), ("KYC validated", 33, TEAL),
                                          ("Negotiation", 27, AMBER), ("Applied", 19, GREEN)], row_h=26, gap=10,
           label_w=112)

    by = ry + 346
    bh = H - 28 - by
    mw = 640
    card(s, X0, by, mw, bh, "Today's route", "7 check-ins · 11.4 km · started 08:12", action="Open map →")
    m = StreetMap(s, X0 + 16, by + 70, mw - 32, bh - 86, seed=11, lake=False,
                  places=[("Ntinda", 0.3, 0.3), ("Kiwatule", 0.7, 0.45), ("Kigoowa", 0.2, 0.8)])
    stops = [(0.12, 0.2), (0.3, 0.42), (0.42, 0.3), (0.55, 0.55), (0.68, 0.38), (0.8, 0.62), (0.9, 0.8)]
    pts = [m.P(*p) for p in stops]
    s.poly(pts, stroke=BRAND, sw=3, closed=False, name="trail")
    for i, p in enumerate(pts):
        col = [GREEN, RED, BLUE, RED, GREEN, BLUE, BRAND][i]
        s.circle(*p, 11, fill=col, stroke="#FFFFFF", sw=2, name=f"check-in {i + 1}")
        s.text(p[0], p[1] + 4, str(i + 1), 11, 700, "#FFFFFF", anchor="middle")
    s.link(X0, by, mw, bh, "w04")

    cx = X0 + mw + 20
    cw2 = 440
    card(s, cx, by, cw2, bh, "Clients by stage", "Sarah's open clients")
    y = by + 80
    counts = [("Interested", 14), ("KYC captured", 5), ("KYC validated", 4), ("Negotiation", 6),
              ("Applied", 3)]
    for lab, n in counts:
        s.circle(cx + 32, y + 6, 6, fill=STAGE[lab])
        s.text(cx + 46, y + 11, lab, 13.5, 400, INK2)
        progress(s, cx + 180, y + 3, 170, n / 14, STAGE[lab], h=7)
        s.text(cx + cw2 - 24, y + 11, str(n), 13.5, 600, INK, anchor="end")
        y += 36
    s.text(cx + 24, y + 14, "Follow-ups due this week: 6", 13, 600, BRAND)
    s.link(cx, by, cw2, bh, "w05")

    ax = cx + cw2 + 20
    aw = X1 - ax
    card(s, ax, by, aw, bh, "Latest activity", "From the field app, synced")
    acts = [("11:42", "Application submitted", "Florence Nambi · LU-APP-2609-04817", GREEN, "check"),
            ("10:58", "Not interested", "Joseph Kiggundu · already has a SACCO loan", RED, "x"),
            ("10:20", "KYC validated", "Betty Nakimuli · NIRA ID matched", TEAL, "idcard"),
            ("09:31", "Visit · interested", "Charles Ssempijja · boda boda owner", BLUE, "hand"),
            ("08:12", "Day started", "Check-in at Ntinda stage", MUTED, "navigation")]
    y = by + 100
    for t, what, who, col, ic in acts:
        with s.g(f"activity {what}"):
            s.circle(ax + 38, y + 4, 14, fill=tint(col, 0.14))
            s.icon(ic, ax + 30, y - 4, 16, col, 2.2)
            s.text(ax + 62, y, what, 13.5, 600, INK)
            s.text(ax + aw - 24, y, t, 12, 400, MUTED, anchor="end")
            s.text(ax + 62, y + 18, who, 12, 400, MUTED, maxw=aw - 90)
        y += 44
    s.link(ax, by + 70, aw, 44, "w06")
    return s


# =====================================================================================
PLACES = [("Ntinda", 0.33, 0.3), ("Kiwatule", 0.6, 0.2), ("Naalya", 0.82, 0.12), ("Kyambogo", 0.44, 0.52),
          ("Banda", 0.55, 0.62), ("Bukoto", 0.12, 0.35), ("Kisaasi", 0.18, 0.1), ("Kireka", 0.8, 0.5),
          ("Nakawa", 0.3, 0.72), ("Mbuya", 0.2, 0.9), ("Kira", 0.93, 0.3), ("Kigoowa", 0.45, 0.08)]


def w04_field_map():
    s = shell("04 Field map (live)", "Field map", ["Sales", "Field map"], period="Day")
    page_head(s, "Field map", "Where agents are right now, and every visit today · Kampala East branch · "
                              "updated 11:42")
    with s.g("header actions"):
        x = X1
        x -= filter_btn(s, x - 220, Y0 + 13, "Branch", "Kampala East", w=220) + 12
        x -= filter_btn(s, x - 160, Y0 + 13, "Agents", "All 7", w=160) + 12
        x -= filter_btn(s, x - 150, Y0 + 13, "Date", "Today", w=150) + 16
        with s.g("toggles"):
            toggle(s, x - 150, Y0 + 22, True)
            s.text(x - 108, Y0 + 37, "Planned stops", 13, 400, INK2)
            toggle(s, x - 290, Y0 + 22, True)
            s.text(x - 248, Y0 + 37, "Agent trails", 13, 400, INK2)

    my = Y0 + 80
    mw = 1170
    mh = H - 28 - my
    s.rect(X0, my, mw, mh, fill=CARD, rx=12, stroke=LINE, name="map card")
    m = StreetMap(s, X0 + 1, my + 1, mw - 2, mh - 2, seed=5, places=PLACES)
    # visits (pins) by outcome
    rnd_pins = [
        (0.36, 0.34, GREEN), (0.4, 0.26, BLUE), (0.27, 0.4, RED), (0.52, 0.3, GREEN), (0.62, 0.36, BLUE),
        (0.6, 0.12, RED), (0.72, 0.18, AMBER), (0.84, 0.2, BLUE), (0.9, 0.36, GREEN), (0.78, 0.42, RED),
        (0.7, 0.55, AMBER), (0.58, 0.68, BLUE), (0.46, 0.6, RED), (0.36, 0.64, GREEN), (0.24, 0.62, AMBER),
        (0.14, 0.44, BLUE), (0.1, 0.24, RED), (0.22, 0.18, GREEN), (0.48, 0.14, AMBER), (0.66, 0.46, RED),
        (0.28, 0.82, BLUE), (0.16, 0.76, RED), (0.86, 0.6, AMBER),
    ]
    with s.g("visit pins"):
        for fx, fy, col in rnd_pins:
            px, py = m.P(fx, fy)
            if col == AMBER:
                s.circle(px, py, 8, fill=CARD, stroke=AMBER, sw=3, name="planned stop")
            else:
                map_pin(s, px, py, col, None, 0.9)
    # Sarah's trail, expanded
    trail = [(0.3, 0.22), (0.36, 0.34), (0.4, 0.26), (0.46, 0.4), (0.52, 0.3), (0.58, 0.4), (0.62, 0.36)]
    tp = [m.P(*p) for p in trail]
    s.poly(tp, stroke=BRAND, sw=3.5, closed=False, name="Sarah trail")
    for i, p in enumerate(tp[1:], 1):
        s.circle(*p, 10, fill=BRAND, stroke="#FFFFFF", sw=2, name=f"check-in {i}")
        s.text(p[0], p[1] + 4, str(i), 10.5, 700, "#FFFFFF", anchor="middle")
    with s.g("start flag"):
        fx_, fy_ = tp[0]
        s.line(fx_, fy_, fx_, fy_ - 26, INK, 2)
        s.path(f"M{fx_:.1f} {fy_ - 26:.1f} L{fx_ + 18:.1f} {fy_ - 20:.1f} L{fx_:.1f} {fy_ - 14:.1f} Z", fill=YELLOW,
               stroke=BRAND_D, sw=1)
    # agents live
    for (nm, ini, st, t, v, c, terr), (fx, fy) in zip(TEAM, [(0.62, 0.36), (0.78, 0.5), (0.86, 0.22), (0.14, 0.32),
                                                             (0.44, 0.1), (0.55, 0.6), (0.24, 0.86)]):
        px, py = m.P(fx, fy)
        col = {"At client": GREEN, "Moving": BRAND, "Offline": "#8A8DA6"}.get(st, AMBER_D)
        agent_dot(s, px + 18, py - 18, ini, col, live=st in ("At client", "Moving"), name=f"agent {nm}")
    # popup on the conversion
    px, py = m.P(0.62, 0.36)
    with s.g("popup"):
        bx, by_ = px + 40, py - 150
        s.rect(bx, by_, 300, 134, fill=CARD, rx=10, stroke=LINE)
        s.text(bx + 16, by_ + 28, CLIENT["name"], 15, 700, INK)
        chip(s, bx + 300 - 16 - tw("Applied", 11, 600) - 34, by_ + 12, "Applied", GREEN, h=22, size=11, dot=True)
        s.text(bx + 16, by_ + 50, "MSE Business Loan · UGX 6,000,000", 12.5, 400, INK2)
        s.text(bx + 16, by_ + 70, "Check-in 11:14 · out 11:52 · ±9 m", 12.5, 400, MUTED)
        s.text(bx + 16, by_ + 90, f"Agent Sarah Namuli · {CLIENT['app_id']}", 12.5, 400, MUTED)
        s.text(bx + 16, by_ + 118, "Open client →", 13, 600, BRAND)
        s.link(bx, by_, 300, 134, "w06")
    # legend
    with s.g("legend"):
        lx, ly = X0 + 20, my + mh - 132
        s.rect(lx, ly, 330, 112, fill=CARD, rx=10, stroke=LINE, op=0.96)
        s.text(lx + 16, ly + 24, "Legend", 13, 700, INK)
        items = [(GREEN, "Converted (application submitted)"), (BLUE, "In progress (interested, KYC, negotiation)"),
                 (RED, "Not interested (reason captured)"), (AMBER, "Planned stop, not yet visited")]
        for i, (col, lab) in enumerate(items):
            yy = ly + 44 + i * 18
            if col == AMBER:
                s.circle(lx + 24, yy - 4, 5, fill=CARD, stroke=AMBER, sw=2.5)
            else:
                s.circle(lx + 24, yy - 4, 6, fill=col)
            s.text(lx + 38, yy, lab, 12, 400, INK2)
    with s.g("map controls"):
        cx_ = X0 + mw - 56
        for i, ic in enumerate(["plus", "minus", "crosshair", "layers"]):
            y_ = my + 20 + i * 46
            s.rect(cx_, y_, 38, 38, fill=CARD, rx=8, stroke=LINE)
            if ic == "minus":
                s.line(cx_ + 11, y_ + 19, cx_ + 27, y_ + 19, INK2, 2.2, cap="round")
            else:
                s.icon(ic, cx_ + 9, y_ + 9, 20, INK2, 2)

    # right panel: agents
    px0 = X0 + mw + 20
    pw = X1 - px0
    card(s, px0, my, pw, 580, "Agents today", "Kampala East · 7 agents · tap to show a trail")
    y = my + 76
    for (nm, ini, st, t, v, c, terr) in TEAM:
        on = nm == "Sarah Namuli"
        col = {"At client": GREEN, "Moving": BRAND, "Offline": "#8A8DA6"}.get(st, AMBER_D)
        with s.g(f"agent row {nm}"):
            if on:
                s.rect(px0 + 10, y - 6, pw - 20, 64, fill=tint(BRAND, 0.07), rx=8, stroke=tint(BRAND, 0.35))
            avatar(s, px0 + 42, y + 26, 18, ini, col)
            s.text(px0 + 72, y + 20, nm, 14, 600, INK)
            s.text(px0 + 72, y + 40, f"{terr} · last ping {t}", 12, 400, MUTED, maxw=250)
            chip(s, px0 + pw - 24 - tw(st, 11, 600) - 34, y + 6, st, col, h=22, size=11, dot=True)
            s.text(px0 + pw - 24, y + 48, f"{v} visits · {c} conv.", 12, 600, INK2, anchor="end")
        y += 70
    s.link(px0 + 10, my + 70, pw - 20, 64, "w03")
    uy = my + 600
    card(s, px0, uy, pw, H - 28 - uy, "All branches", "Tap a branch to jump")
    um = UgandaMap(px0 + 16, uy + 60, pw - 32, H - 28 - uy - 70)
    um.draw_base(s)
    um.draw_branches(s)
    s.link(px0, uy, pw, H - 28 - uy, "w01")
    return s


# =====================================================================================
PIPE = {
    "Interested": [("Charles Ssempijja", "MSE Business Loan", 3_000_000, "Sarah Namuli", "SN", "1 day", None),
                   ("Aisha Nalubega", "School Fees Loan", 2_500_000, "Esther Nakato", "EN", "2 days", None),
                   ("Moses Opolot", "Civil Servant Loan", 8_000_000, "Peter Kato", "PK", "6 days", "Follow-up due"),
                   ("Doreen Atuhaire", "Home Improvement Loan", 5_000_000, "Ruth Achieng", "RA", "9 days",
                    "Stuck 7+ days")],
    "KYC captured": [("Paul Tumusiime", "Civil Servant Loan", 10_000_000, "Ivan Mugabe", "IM", "1 day",
                      "Payslip missing"),
                     ("Sarah Namutebi", "MSE Business Loan", 4_000_000, "Sarah Namuli", "SN", "2 days", None),
                     ("Henry Mukasa", "Agri Asset Loan", 3_500_000, "Brian Ssali", "BS", "12 days", "Stuck 7+ days")],
    "KYC validated": [("Betty Nakimuli", "School Fees Loan", 2_000_000, "Sarah Namuli", "SN", "today", None),
                      ("Robert Kizza", "MSE Business Loan", 7_000_000, "Esther Nakato", "EN", "3 days", None),
                      ("Susan Akello", "Civil Servant Loan", 12_000_000, "Peter Kato", "PK", "4 days", None)],
    "Negotiation": [("James Okello", "Civil Servant Loan", 9_000_000, "Joan Auma", "JA", "2 days", None),
                    ("Mary Nansubuga", "Home Improvement Loan", 6_500_000, "Ruth Achieng", "RA", "5 days",
                     "Wants lower instalment"),
                    ("Ivan Kasozi", "MSE Business Loan", 3_000_000, "Sarah Namuli", "SN", "1 day", None)],
    "Applied": [(CLIENT["name"], CLIENT["product"], CLIENT["amount"], "Sarah Namuli", "SN", "today", "Awaiting approval"),
                ("Agnes Babirye", "School Fees Loan", 1_800_000, "Esther Nakato", "EN", "1 day", "Awaiting approval"),
                ("Tom Wasswa", "Civil Servant Loan", 15_000_000, "Peter Kato", "PK", "2 days", "Sent to HQ")],
    "Decided": [("Janet Kyomugisha", "MSE Business Loan", 4_000_000, "Ruth Achieng", "RA", "Approved", None),
                ("Ronald Byamugisha", "Civil Servant Loan", 6_000_000, "Ivan Mugabe", "IM", "Approved", None),
                ("Prossy Namara", "Agri Asset Loan", 5_000_000, "Brian Ssali", "BS", "Rejected", "Affordability")],
}
PIPE_TOTALS = {"Interested": (1204, "UGX 6.8B"), "KYC captured": (212, "UGX 1.3B"), "KYC validated": (96, "UGX 0.7B"),
               "Negotiation": (131, "UGX 0.9B"), "Applied": (73, "UGX 0.5B"), "Decided": (978, "812 approved")}


def w05_pipeline():
    s = shell("05 Client pipeline", "Client pipeline", ["Sales", "Client pipeline"])
    page_head(s, "Client pipeline", "1,716 open clients, first visit to approval · every record belongs to Letshego")
    with s.g("header actions"):
        x = X1
        x -= button(s, x, Y0 + 12, "Add client", "primary", icon="userplus", anchor="end") + 12
        x -= seg(s, x - seg_width(["Board", "List", "Map"]), Y0 + 13, ["Board", "List", "Map"], "Board", h=38) + 12
        x -= filter_btn(s, x - 150, Y0 + 13, "Agent", "All", w=150) + 12
        x -= filter_btn(s, x - 170, Y0 + 13, "Product", "All", w=170) + 12
        x -= filter_btn(s, x - 210, Y0 + 13, "Branch", "Kampala East", w=210) + 12
    with s.g("lost summary"):
        y = Y0 + 72
        s.rect(X0, y, CW, 40, fill=CARD, rx=10, stroke=LINE)
        s.icon("info", X0 + 14, y + 10, 20, BRAND, 2)
        s.text(X0 + 44, y + 25, "Closed without a loan this quarter:", 13, 600, INK)
        x = X0 + 48 + tw("Closed without a loan this quarter:", 13, 600)
        for lab, n, col in [("Not interested at first visit", "5,126", RED),
                            ("Dropped after KYC", "486", AMBER_D), ("Declined to apply", "367", AMBER_D)]:
            x += s.text(x + 8, y + 25, f"{lab} ", 13, 400, INK2) + 8
            x += s.text(x, y + 25, n, 13, 700, col) + 18
        s.text(X1 - 16, y + 25, "See the reasons →", 13, 600, BRAND, anchor="end")
        s.link(X1 - 180, y, 180, 40, "w09")

    cy = Y0 + 128
    ncol = 6
    cwid = (CW - (ncol - 1) * 14) / ncol
    for i, (col_name, cards) in enumerate(PIPE.items()):
        x = X0 + i * (cwid + 14)
        color = STAGE.get(col_name, BRAND_D)
        n, total = PIPE_TOTALS[col_name]
        with s.g(f"column {col_name}"):
            s.rect(x, cy, cwid, H - 28 - cy, fill="#ECEDF4", rx=12, name="column bg")
            s.rect(x, cy, cwid, 4, fill=color, rx=2)
            label = "Approved / rejected" if col_name == "Decided" else (
                "Applied = converted" if col_name == "Applied" else col_name)
            s.text(x + 16, cy + 32, label, 14, 700, INK)
            s.text(x + cwid - 16, cy + 32, f"{n:,}", 13, 700, color if col_name != "Decided" else INK2, anchor="end")
            s.text(x + 16, cy + 52, total, 12, 400, MUTED)
            y = cy + 68
            for (nm, prod, amt, ag, ini, age, flag) in cards:
                hl = nm == CLIENT["name"]
                ch = 128
                with s.g(f"card {nm}"):
                    s.rect(x + 10, y, cwid - 20, ch, fill=CARD, rx=10,
                           stroke=BRAND if hl else LINE, sw=2 if hl else 1)
                    s.text(x + 24, y + 26, nm, 14, 600, INK, maxw=cwid - 60)
                    chip(s, x + 24, y + 36, prod, PRODUCT[prod], h=20, size=10.5)
                    s.text(x + 24, y + 76, ugx(amt), 13, 600, INK2)
                    if col_name == "Decided":
                        status_chip(s, x + cwid - 20 - tw(age, 11, 600) - 34, y + 62, age, h=20, size=11)
                    else:
                        s.text(x + cwid - 24, y + 76, age, 12, 400, MUTED, anchor="end")
                    s.line(x + 24, y + 90, x + cwid - 24, y + 90, LINE2)
                    avatar(s, x + 36, y + 109, 11, ini, BRAND)
                    s.text(x + 54, y + 113, ag, 12, 400, INK2, maxw=cwid - 80 - (tw(flag, 11, 600) if flag else 0))
                    if flag:
                        fcol = RED if "Stuck" in flag or "missing" in flag or flag == "Affordability" else (
                            AMBER_D if "Awaiting" in flag or "HQ" in flag else BLUE)
                        s.text(x + cwid - 24, y + 113, flag, 11, 600, fcol, anchor="end")
                if hl:
                    s.link(x + 10, y, cwid - 20, ch, "w06")
                y += ch + 10
            s.text(x + cwid / 2, H - 48, f"+ {n - len(cards):,} more", 12.5, 600, BRAND, anchor="middle")
    return s


# =====================================================================================
def w06_client():
    c = CLIENT
    s = shell("06 Client record (Florence Nambi)", "Client pipeline", ["Sales", "Client pipeline", c["name"]])
    with s.g("client header"):
        s.rect(X0, Y0, CW, 110, fill=CARD, rx=12, stroke=LINE)
        s.circle(X0 + 60, Y0 + 55, 34, fill=tint(GREEN, 0.15))
        s.text(X0 + 60, Y0 + 65, c["initials"], 24, 700, GREEN_D, anchor="middle")
        s.text(X0 + 112, Y0 + 46, c["name"], 24, 700, INK)
        x = X0 + 124 + tw(c["name"], 24, 700)
        x += chip(s, x, Y0 + 27, "Applied · awaiting approval", GREEN, dot=True) + 8
        chip(s, x, Y0 + 27, c["product"], PRODUCT[c["product"]])
        s.text(X0 + 112, Y0 + 74, f"Client {c['id']} · {c['business']} · 0772 418 ··· · NIN {c['nin']}", 14, 400,
               INK2)
        s.icon("shield", X0 + 112, Y0 + 83, 16, BRAND, 2)
        s.text(X0 + 134, Y0 + 96, "Owned by Letshego Uganda · assigned to Sarah Namuli since 12 Aug 2026 (handed over "
                                  "from John Mugisha, who left)", 13, 600, BRAND)
        x = X1 - 24
        x -= button(s, x, Y0 + 35, "Open approval", "primary", icon="listcheck", anchor="end") + 10
        s.link(x + 10, Y0 + 35, 170, 40, "w08")
        button(s, x, Y0 + 35, "Reassign", "secondary", icon="swap", anchor="end")
        s.link(x - 120, Y0 + 35, 120, 40, "w11")

    ty = Y0 + 128
    th = H - 28 - ty
    c1 = 470
    card(s, X0, ty, c1, th, "Profile & demographics", "Captured at KYC · 30 Sep 2026")
    y = ty + 92
    for lab, val in [("Gender · age", "Woman · 34"), ("Marital status", "Married · 3 dependants"),
                     ("Education", "Secondary (S4)"), ("Occupation", "Tailor, own business (6 yrs)"),
                     ("Location", "Kiwatule, Nakawa Division, Kampala"), ("Phone", "MTN 0772 418 ··· · verified"),
                     ("Next of kin", "Joseph Mukiibi (husband)")]:
        kv(s, X0 + 24, y, c1 - 48, lab, val)
        y += 32
    s.line(X0 + 24, y - 8, X0 + c1 - 24, y - 8, LINE)
    s.text(X0 + 24, y + 20, "Earnings & collateral", 15, 700, INK)
    y += 50
    for lab, val in [("Monthly business income", "UGX 2,400,000"), ("Monthly expenses", "UGX 1,150,000"),
                     ("Other loans", "None (CRB clear)"), ("Collateral", "Motorcycle UBF 412K · UGX 4.5M"),
                     ("Second collateral", "Sewing machines (3) · UGX 1.8M")]:
        kv(s, X0 + 24, y, c1 - 48, lab, val)
        y += 32
    with s.g("agent note"):
        s.rect(X0 + 24, y + 4, c1 - 48, 124, fill="#F7F7FC", rx=10)
        s.text(X0 + 40, y + 30, "Agent's note on product fit", 12.5, 700, INK2)
        para(s, X0 + 40, y + 52, "Steady walk-in customers and school-uniform orders each term. MSE loan fits better "
                                 "than school fees loan: she wants a second industrial machine before January.",
             c1 - 80, 13, 400, INK2, lh=20)
    y += 156
    s.text(X0 + 24, y, "Visits (3)", 15, 700, INK)
    y += 12
    for d, what, who in [("30 Sep 11:14", "KYC, negotiation and application · 38 min", "Sarah Namuli"),
                         ("14 Sep 09:40", "Follow-up: asked her to prepare ID and sales book", "Sarah Namuli"),
                         ("29 Jul 10:05", "First visit (John Mugisha) · interested", "John Mugisha")]:
        s.icon("pin", X0 + 24, y + 10, 16, BRAND, 2)
        s.text(X0 + 48, y + 23, what, 13, 600, INK)
        s.text(X0 + c1 - 24, y + 23, d, 12, 400, MUTED, anchor="end")
        y += 30

    c2x = X0 + c1 + 20
    c2 = 560
    card(s, c2x, ty, c2, th, "KYC documents & checks", "Photos taken in the app · all GPS-stamped at the client")
    tw_ = (c2 - 48 - 2 * 12) / 3
    docs = [("id_front", "NIRA ID · front"), ("id_back", "NIRA ID · back"), ("selfie", "Selfie · live check"),
            ("shop", "Business premises"), ("doc", "Sales book (3 mo)"), ("moto", "Collateral · logbook")]
    for i, (k, lab) in enumerate(docs):
        doc_thumb(s, c2x + 24 + (i % 3) * (tw_ + 12), ty + 78 + (i // 3) * 142, tw_, 130, k, lab)
    y = ty + 378
    s.text(c2x + 24, y, "Validation checks", 15, 700, INK)
    y += 16
    checks = [("NIRA: NIN, name and photo match", "Verified 30 Sep 11:21", True),
              ("Phone registered to this name (MTN)", "Verified", True),
              ("Not already a Letshego client", "No match in core banking", True),
              ("Location inside Sarah's territory", "Kiwatule · 0.3712, 32.6205", True),
              ("Affordability: instalment ≤ 50% of free income", "Instalment 36% of free income", True),
              ("CRB consent signed on the phone", "Signed 30 Sep 11:23", True)]
    for lab, sub, ok in checks:
        s.circle(c2x + 34, y + 20, 10, fill=tint(GREEN, 0.15))
        s.icon("check", c2x + 27, y + 13, 14, GREEN, 3)
        s.text(c2x + 54, y + 19, lab, 13.5, 600, INK)
        s.text(c2x + 54, y + 36, sub, 12, 400, MUTED)
        y += 44

    c3x = c2x + c2 + 20
    c3 = X1 - c3x
    card(s, c3x, ty, c3, th, "Client journey", "Every step with who, when and where")
    steps = [("1", "Visited", "John Mugisha · 29 Jul 10:05 · GPS ±8 m", "Visited"),
             ("2", "Interested", "Wants to expand the shop · moved to Sarah 12 Aug", "Interested"),
             ("3", "KYC captured", "Sarah Namuli · 30 Sep 11:16 · 6 photos · NIRA ID", "KYC captured"),
             ("4", "KYC validated", "30 Sep 11:24 · all 6 checks passed", "KYC validated"),
             ("5", "Negotiation", "MSE Business Loan · UGX 6M · 18 months", "Negotiation"),
             ("6", "Applied: converted", f"30 Sep 11:42 · {c['app_id']}", "Applied"),
             ("7", "Supervisor approval", "Waiting for Moses Okello · 18 min", None)]
    y = ty + 88
    for i, (n, lab, sub, st) in enumerate(steps):
        col = STAGE[st] if st else "#C4C7D6"
        with s.g(f"step {lab}"):
            if i < len(steps) - 1:
                s.line(c3x + 38, y + 14, c3x + 38, y + 58, col if steps[i + 1][3] else LINE, 2,
                       dash=None if steps[i + 1][3] else "4 4")
            s.circle(c3x + 38, y, 14, fill=col if st else CARD, stroke=col, sw=2)
            s.text(c3x + 38, y + 4.5, n, 12, 700, "#FFFFFF" if st else MUTED, anchor="middle")
            s.text(c3x + 64, y - 2, lab, 14, 600, INK if st else MUTED)
            s.text(c3x + 64, y + 16, sub, 12, 400, MUTED, maxw=c3 - 90)
        y += 58
    with s.g("loan application"):
        ly = y + 6
        s.rect(c3x + 24, ly, c3 - 48, th - (ly - ty) - 20, fill=tint(GREEN, 0.07), rx=10, stroke=tint(GREEN, 0.35))
        s.text(c3x + 40, ly + 28, "Loan application", 13, 700, GREEN_D)
        s.text(c3x + 40, ly + 54, c["app_id"], 18, 700, INK)
        inst = rnd_instalment(c["amount"], c["months"])
        s.text(c3x + 40, ly + 78, f"{ugx(c['amount'])} · {c['months']} months · ≈ {ugx(inst)} a month", 12.5,
               400, INK2)
        s.text(c3x + 40, ly + 98, "Reason for the loan: second industrial sewing machine", 12.5, 400, INK2,
               maxw=c3 - 80)
        s.text(c3x + 40, ly + 132, "Required items submitted", 12.5, 700, GREEN_D)
        items = ["NIRA ID both sides", "Live selfie", "Proof of income", "Premises photo", "Collateral + logbook",
                 "CRB consent", "Loan application ID"]
        for i, it in enumerate(items):
            ix = c3x + 40 + (i % 2) * ((c3 - 80) / 2)
            iy = ly + 158 + (i // 2) * 24
            s.icon("check", ix, iy - 12, 14, GREEN, 2.8)
            s.text(ix + 20, iy, it, 12.5, 400, INK2)
        s.text(c3x + 40, ly + 266, "Counts as a conversion for Sarah (Q3: 19 of 22)", 12.5, 600, GREEN_D)
    return s


SCREENS = [w00_sign_in, w01_overview, w02_agents, w03_agent, w04_field_map, w05_pipeline, w06_client]
