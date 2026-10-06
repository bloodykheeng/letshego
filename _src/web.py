"""Web console screens (1920 x 1080): shell, sign in, overviews (head office and branch), agents, agent profile, field
map, pipeline, client."""
from __future__ import annotations

from charts import (BRANCHES, StreetMap, UgandaMap, agent_dot, donut, funnel, heat_strip, line_chart, map_pin,
                    perf_color, ring, sparkline)
from data import (AGENT, AGENTS, AGENTS_N, APPROVED, CALLEE, CLIENT, CLIENTS_Q, CLIENTS_SPLY, CONV_Q, CONV_SPLY, FUNNEL, HOURS_PROSPECTING,
                  LEAD_VISITS_Q, LEADS_Q, MGMT, PENDING, PROSPECT_TARGET_Q, PROSPECTS_Q, QUARTER, QUARTER_RANGE,
                  REJECTED, ROS, ROS_N, SARAH, SUPERVISOR, TARGET_Q, TEAM, WEEK_CONV, WEEK_DATES, WEEK_LABELS,
                  WEEK_PROSPECTS, clients, rnd_instalment, ugx)
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
    ("SALES", [("Overview", "grid")]),
    ("PLANNING", [("Journey plans", "route")]),
    ("FIELD", [("Agents", "users"), ("Field map", "map"), ("Client pipeline", "workflow")]),
    ("LOANS", [("Approvals", "listcheck"), ("Why & why not", "message")]),
    ("ADMIN", [("Locations", "layers"), ("Users", "user"), ("Roles & access", "shield"), ("Reports & audit", "history")]),
]
NAV_TARGET = {"Overview": "w01", "Agents": "w02", "Field map": "w04", "Client pipeline": "w05", "Approvals": "w07",
              "Why & why not": "w09", "Journey plans": "w10", "Locations": "w11",
              "Users": "w12", "Roles & access": "w12c", "Reports & audit": "w13"}
BADGES = {"Agents": ("6", RED), "Approvals": ("14", YELLOW)}

SB_TEXT = "#D9D8F3"
SB_MUTED = "#9E9CD6"


def shell(title: str, active: str, crumbs: list[str], user=MGMT, period="Quarter"):
    s = SVG(W, H, title)
    s.soft = True
    s.rect(0, 0, W, H, fill="#F6F7F9", name="page background")

    with s.g("sidebar"):
        s.rect(0, 0, SB, H, fill=CARD, name="sidebar bg")
        s.line(SB, 0, SB, H, LINE)
        wordmark(s, 26, 50, 23, INK)
        s.text(26, 72, "Field Sales · Uganda", 12, 400, MUTED, name="product sub")
        y = 110
        for group, items in NAV:
            s.text(28, y, group, 10.5, 600, FAINT, spacing=1.2, name=f"nav group {group}")
            y += 14
            for label, ic in items:
                on = label == active
                with s.g(f"nav {label}"):
                    if on:
                        s.rect(14, y, SB - 28, 40, fill=tint(BRAND, 0.08), rx=10, name="active bg", shadow=False)
                    s.icon(ic, 30, y + 10, 20, BRAND if on else "#8A8DA6", 1.9)
                    s.text(62, y + 25, label, 14, 600 if on else 400, BRAND if on else INK2,
                           name="label")
                    if label in BADGES:
                        b, col = BADGES[label]
                        bw = tw(b, 11, 700) + 14
                        s.rect(SB - 30 - bw, y + 11, bw, 18, fill=col, rx=9, name="badge")
                        s.text(SB - 30 - bw / 2, y + 24, b, 11, 700, BRAND_D if col == YELLOW else "#FFFFFF",
                               anchor="middle", name="badge n")
                tgt = NAV_TARGET.get(label)
                if label == "Overview" and user == SUPERVISOR:
                    tgt = "w01b"
                s.link(14, y, SB - 28, 40, tgt)
                y += 42
            y += 12
        with s.g("field app card"):
            s.rect(16, H - 180, SB - 32, 88, fill=tint(YELLOW, 0.2), rx=14, name="app card", shadow=False)
            s.rect(30, H - 166, 30, 30, fill=YELLOW, rx=9)
            s.icon("phone", 36, H - 160, 18, BRAND_D, 2)
            s.text(70, H - 146, "Field app", 13, 700, INK)
            s.text(30, H - 120, "Sales agents · relationship officers", 12, 400, INK2)
            s.text(30, H - 102, "Android · offline · GPS · open it →", 12, 600, YELLOW_D)
        s.link(16, H - 180, SB - 32, 88, "m02")
        # demo shortcut: click the name to switch between head office and the branch manager's view
        s.link(0, H - 76, SB - 56, 76, "w01b" if user == MGMT else "w01")
        s.link(SB - 52, H - 60, 40, 44, "w00")
        with s.g("sidebar user"):
            s.line(16, H - 76, SB - 16, H - 76, LINE)
            s.circle(44, H - 38, 18, fill=YELLOW)
            s.text(44, H - 32, user[2], 14, 700, BRAND_D, anchor="middle")
            s.text(72, H - 42, user[0], 14, 600, INK)
            s.text(72, H - 23, user[1], 11.5, 400, MUTED, maxw=SB - 128)
            s.rect(SB - 50, H - 58, 38, 38, fill="#FDECEC", rx=10, name="sign out button", shadow=False)
            s.icon("logout", SB - 41, H - 49, 20, RED, 2)

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
        rx -= 48
        with s.g("theme switch"):
            s.circle(rx + 11, 34, 18, fill="#F4F5FA", shadow=False)
            s.icon("moon", rx + 1, 24, 20, INK2, 2)
        s.link(rx - 8, 14, 38, 40, "!theme")
        rx -= 290
        with s.g("search"):
            s.rect(rx, 16, 266, 36, fill="#F4F5FA", rx=8, stroke=LINE)
            s.icon("search", rx + 12, 25, 18, MUTED)
            s.text(rx + 40, 39, "Search prospects, leads, agents…", 13, 400, FAINT)
        pw = seg_width(["Day", "Week", "Quarter", "Year"])
        rx -= pw + 20
        seg(s, rx, 16, ["Day", "Week", "Quarter", "Year"], period, h=36)
        lab = {"Day": "Wed 30 Sep 2026", "Week": "W40 · 28 Sep – 2 Oct", "Quarter": f"{QUARTER} · {QUARTER_RANGE}",
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


def rule_note(s: SVG, x, y, text="Client = loan disbursed · conversion = prospect → client", icon="check", color=GREEN):
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
    s.soft = True
    s.rect(0, 0, W, H, fill="#F6F7F9", name="page background")
    s.raw('<defs>'
          '<radialGradient id="glowY"><stop offset="0" stop-color="#FFE45C" stop-opacity="0.3"/>'
          '<stop offset="1" stop-color="#FFE45C" stop-opacity="0"/></radialGradient>'
          '<radialGradient id="glowI"><stop offset="0" stop-color="#8E8CF0" stop-opacity="0.35"/>'
          '<stop offset="1" stop-color="#8E8CF0" stop-opacity="0"/></radialGradient></defs>')
    s.circle(260, 180, 520, fill="url(#glowY)", name="yellow glow")
    s.circle(1700, 940, 560, fill="url(#glowI)", name="indigo glow")
    with s.g("faint mark", opacity=0.05):
        triangle(s, 1380, 60, 420)

    wordmark(s, 64, 78, 26, INK)
    s.text(66, 102, "Field Sales · Uganda", 13, 400, MUTED)
    with s.g("theme switch"):
        s.circle(W - 84, 66, 22, fill=CARD, shadow=True)
        s.icon("moon", W - 95, 55, 22, INK, 2)
    s.link(W - 108, 42, 48, 48, "!theme")

    # ---- floating product previews
    with s.g("preview conversions", transform="rotate(-3 470 360)"):
        x, y = 320, 290
        s.rect(x, y, 300, 136, fill=CARD, rx=20, stroke=LINE)
        s.text(x + 22, y + 32, "Q3 new clients (loans disbursed)", 13, 600, MUTED)
        s.text(x + 22, y + 76, "786", 34, 700, INK)
        s.icon("trendup", x + 130, y + 56, 18, GREEN, 2.4)
        s.text(x + 152, y + 72, "+20%", 14, 700, GREEN_D)
        sparkline(s, x + 22, y + 92, 256, 28, [9, 7, 3, 2, 2, 2, 2, 2, 3, 5, 11, 18, 26], GREEN)
    with s.g("preview notification", transform="rotate(2 420 600)"):
        x, y = 250, 540
        s.rect(x, y, 350, 84, fill=CARD, rx=20, stroke=LINE)
        s.circle(x + 40, y + 42, 20, fill=tint(GREEN, 0.15))
        s.icon("check", x + 30, y + 32, 20, GREEN, 2.8)
        s.text(x + 72, y + 36, "Lead created", 14.5, 700, INK)
        s.text(x + 72, y + 58, "Aisha Nalubega · UGX 2M · by Sarah · 14:25", 12.5, 400, MUTED)
    with s.g("preview plan kept", transform="rotate(3 1450 330)"):
        x, y = 1310, 250
        s.rect(x, y, 290, 150, fill=CARD, rx=20, stroke=LINE)
        ring(s, x + 70, y + 75, 44, 10, 0.79, BRAND)
        s.text(x + 70, y + 82, "79%", 18, 700, INK, anchor="middle")
        s.text(x + 136, y + 64, "Route targets", 13, 600, MUTED)
        s.text(x + 136, y + 88, "met this", 15, 700, INK)
        s.text(x + 136, y + 108, "quarter", 15, 700, INK)
    with s.g("preview live map", transform="rotate(-2 1500 640)"):
        x, y = 1340, 540
        s.rect(x, y, 320, 190, fill=CARD, rx=20, stroke=LINE)
        m = StreetMap(s, x + 12, y + 12, 296, 118, seed=11, lake=False, dense=0.6)
        for fx, fy, col in [(0.25, 0.4, GREEN), (0.5, 0.62, RED), (0.72, 0.35, BLUE)]:
            map_pin(s, *m.P(fx, fy), col, None, 0.8)
        agent_dot(s, *m.P(0.6, 0.3), "SN", GREEN)
        s.text(x + 18, y + 158, "Sarah Namuli", 14, 700, INK)
        s.text(x + 18, y + 177, "Prospecting · Kiwatule market · 32/50", 12, 400, MUTED)

    # ---- the card
    cw, ch = 480, 640
    cx, cy = (W - cw) / 2, 200
    s.rect(cx, cy, cw, ch, fill=CARD, rx=28, stroke=LINE, name="sign-in card")
    fx, fw = cx + 48, cw - 96
    with s.g("sign-in form"):
        s.rect(fx, cy + 48, 52, 52, fill=BRAND, rx=16)
        triangle(s, fx + 12, cy + 58, 28)
        s.text(fx, cy + 150, "Welcome back", 30, 700, INK)
        s.text(fx, cy + 180, "Sign in with your Letshego staff account.", 15, 400, MUTED)
        button(s, fx, cy + 212, "Continue with Microsoft", "secondary", icon="sparkle", w=fw, h=50)
        s.link(fx, cy + 212, fw, 50, "w01")
        s.line(fx, cy + 296, fx + fw / 2 - 70, cy + 296, LINE)
        s.text(fx + fw / 2, cy + 300, "or use your staff ID", 12.5, 400, MUTED, anchor="middle")
        s.line(fx + fw / 2 + 70, cy + 296, fx + fw, cy + 296, LINE)
        field(s, fx, cy + 322, fw, "Staff ID", "LU-0142", h=48, icon="user")
        field(s, fx, cy + 404, fw, "Password", "••••••••••••", h=48, icon="lock")
        s.text(fx + fw, cy + 418, "Forgot?", 13, 600, BRAND, anchor="end")
        checkbox(s, fx, cy + 492, True)
        s.text(fx + 28, cy + 506, "Keep me signed in on this computer", 13, 400, INK2)
        button(s, fx, cy + 530, "Sign in", "primary", icon="arrowright", w=fw, h=52, size=15)
        s.link(fx, cy + 530, fw, 52, "w01")
        s.icon("fingerprint", fx, cy + 598, 16, GREEN, 2)
        s.text(fx + 24, cy + 611, "Two-step verification is on for your account", 12.5, 400, MUTED)
    with s.g("agent app link"):
        s.rect(cx, cy + ch + 20, cw, 56, fill=CARD, rx=18, stroke=LINE)
        s.rect(cx + 16, cy + ch + 32, 32, 32, fill=YELLOW, rx=10, shadow=False)
        s.icon("phone", cx + 23, cy + ch + 39, 18, BRAND_D, 2)
        s.text(cx + 62, cy + ch + 54, "In the field? Use the Android app", 14, 600, INK)
        s.text(cx + cw - 20, cy + ch + 54, "Open →", 13, 700, BRAND, anchor="end")
        s.link(cx, cy + ch + 20, cw, 56, "m02")
    s.text(W / 2, H - 28, "Letshego Uganda · Improving lives · client data protected under the Data Protection and "
                         "Privacy Act, 2019", 12, 400, MUTED, anchor="middle")
    return s


# =====================================================================================
def w01_overview():
    s = shell("01 Sales overview", "Overview", ["Sales", "Overview"])
    page_head(s, "Sales overview", f"All 14 branches · {AGENTS_N} sales agents · {ROS_N} relationship officers · "
                                   f"{QUARTER} ({QUARTER_RANGE})")
    with s.g("header actions"):
        x = X1
        x -= button(s, x, Y0 + 12, "Export", "primary", icon="download", anchor="end") + 12
        x -= filter_btn(s, x - 190, Y0 + 13, "Branch", "All branches", w=190) + 16
        rule_note(s, x - 372, Y0 + 18)

    ky = Y0 + 84
    kw = (CW - 5 * 16) / 6
    kpis = [
        ("userplus", STAGE["Prospect"], "Prospects", f"{PROSPECTS_Q:,}",
         f"of {PROSPECT_TARGET_Q:,} planned · {PROSPECTS_Q / PROSPECT_TARGET_Q:.0%}",
         PROSPECTS_Q / PROSPECT_TARGET_Q, None, None, False),
        ("flag", STAGE["Lead"], "Leads generated", f"{LEADS_Q:,}", f"{LEADS_Q / PROSPECTS_Q:.0%} of prospects",
         None, None, None, False),
        ("idcard", STAGE["KYC completed"], "KYC completed", f"{CONV_Q:,}",
         f"{CONV_Q / LEADS_Q:.0%} of leads · loan applications sent", None, None, None, False),
        ("banknote", GREEN, "New clients", f"{CLIENTS_Q:,}",
         f"loans disbursed · {CLIENTS_Q / PROSPECTS_Q:.1%} of prospects", None, "Conversion",
         f"+{CLIENTS_Q / CLIENTS_SPLY - 1:.0%} vs Q3 2025", False),
        ("clock", AMBER, "Time prospecting", f"{HOURS_PROSPECTING} h", "a day on route days · from GPS", None,
         None, None, False),
        ("users", RED, "Active field staff", f"{AGENTS_N + ROS_N - 6} / {AGENTS_N + ROS_N}",
         "6 silent: no prospect in 14+ days", (AGENTS_N + ROS_N - 6) / (AGENTS_N + ROS_N), None, None, False),
    ]
    for i, (ic, col, lab, val, sub, fr, tag, d, bad) in enumerate(kpis):
        kpi(s, X0 + i * (kw + 16), ky, kw, 150, ic, col, lab, val, sub, fr, tag, d, bad)
    for i, tgt in enumerate(["w04", "w05", "w05", "w02", "w02", "w02"]):
        s.link(X0 + i * (kw + 16), ky, kw, 150, tgt)

    # ---- quarter rhythm
    ry = ky + 166
    rw = 1010
    card(s, X0, ry, rw, 370, "Quarter rhythm: prospects and KYC completed by week",
         "Busy in week 1, quiet mid-quarter, a rush at the end: route journey plans with daily targets even it out")
    with s.g("legend"):
        lx = X0 + rw - 330
        s.rect(lx, ry + 28, 14, 12, fill=tint(STAGE["Prospect"], 0.4), rx=2)
        s.text(lx + 20, ry + 39, "Prospects", 12, 600, INK2)
        s.line(lx + 100, ry + 34, lx + 120, ry + 34, GREEN, 3)
        s.text(lx + 126, ry + 39, "KYC completed", 12, 600, INK2)
        s.line(lx + 226, ry + 34, lx + 246, ry + 34, INK2, 2, dash="5 4")
        s.text(lx + 252, ry + 39, "Pace", 12, 400, INK2)
    cx0, cy0, cw_, ch_ = X0 + 70, ry + 100, rw - 130, 210
    n = 13
    colw = cw_ / n
    vmax = 9000
    cmax = 330
    with s.g("slump band"):
        s.rect(cx0 + colw * 2, cy0 - 10, colw * 7, ch_ + 10, fill=tint(RED, 0.07), rx=6)
        s.text(cx0 + colw * 5.5, cy0 + 8, "Mid-quarter slump", 12.5, 700, shade(RED, 0.1), anchor="middle")
        drop = 1 - min(WEEK_PROSPECTS[2:9]) / WEEK_PROSPECTS[0]
        s.text(cx0 + colw * 5.5, cy0 + 26, f"prospecting down {drop:.0%} from week 1", 12, 400, shade(RED, 0.05),
               anchor="middle")
    with s.g("axes"):
        for k in range(4):
            yy = cy0 + ch_ - ch_ * k / 3
            s.line(cx0, yy, cx0 + cw_, yy, LINE2 if k else LINE)
            s.text(cx0 - 10, yy + 4, f"{int(vmax * k / 3):,}", 11, 400, MUTED, anchor="end")
            s.text(cx0 + cw_ + 10, yy + 4, f"{int(cmax * k / 3)}", 11, 400, GREEN, name="client axis")
        s.text(cx0 - 10, cy0 - 22, "Prospects", 11, 600, MUTED, anchor="end")
        s.text(cx0 + cw_ + 10, cy0 - 22, "KYC", 11, 600, GREEN)
    with s.g("prospect bars"):
        for i, v in enumerate(WEEK_PROSPECTS):
            bh = ch_ * v / vmax
            s.rect(cx0 + i * colw + colw * 0.2, cy0 + ch_ - bh, colw * 0.6, bh, fill=tint(STAGE["Prospect"], 0.4),
                   rx=3)
            s.text(cx0 + i * colw + colw / 2, cy0 + ch_ + 18, WEEK_LABELS[i], 11, 600, INK2, anchor="middle")
            if i % 2 == 0:
                s.text(cx0 + i * colw + colw / 2, cy0 + ch_ + 33, WEEK_DATES[i], 10.5, 400, MUTED, anchor="middle")
    with s.g("pace line"):
        py = cy0 + ch_ - ch_ * (TARGET_Q / 13) / cmax
        s.line(cx0, py, cx0 + cw_, py, INK2, 1.6, dash="5 4")
        s.text(cx0 + cw_ - 4, py - 6, f"{TARGET_Q / 13:.0f} KYC / week", 11, 600, INK2, anchor="end")
    with s.g("client line"):
        pts = [(cx0 + i * colw + colw / 2, cy0 + ch_ - ch_ * v / cmax) for i, v in enumerate(WEEK_CONV)]
        s.poly(pts, stroke=GREEN, sw=2.6, closed=False)
        for p in pts:
            s.circle(*p, 3.5, fill=CARD, stroke=GREEN, sw=2)
    s.link(X0, ry, rw, 370, "w02")

    # ---- funnel
    fx = X0 + rw + 20
    fw = X1 - fx
    card(s, fx, ry, fw, 370, "Client journey funnel", f"{QUARTER} · all branches · then {CLIENTS_Q} loans disbursed = clients",
         action="Pipeline →")
    funnel(s, fx + 24, ry + 90, fw - 48, FUNNEL, row_h=48, gap=26, label_w=130)
    with s.g("funnel note"):
        s.rect(fx + 24, ry + 318, fw - 48, 36, fill="#F7F7FC", rx=10, shadow=False)
        s.text(fx + 40, ry + 341, f"Sales agents prospect and make leads · relationship officers visit leads and "
                                  "complete KYC", 12, 400, INK2, maxw=fw - 80)
    s.link(fx, ry, fw, 370, "w05")

    # ---- bottom row: agents' conversion, plans kept, attention
    by = ry + 386
    bh = H - 28 - by
    bw = 600
    card(s, X0, by, bw, bh, "Prospects to clients, by sales agent", f"{QUARTER} · best and weakest",
         action="All →")
    cols = [("Agent", 200, "start"), ("Prospects", 95, "end"), ("Leads", 70, "end"), ("KYC", 70, "end"),
            ("Clients", 75, "end"), ("Conv.", 88, "end")]
    rws = []
    for nm, ini, br, terr, p, l, c, t, wk, hrs, last, st in AGENTS[:3] + AGENTS[-2:]:
        rws.append([agent_cell(nm, ini, br, BRAND if st == "On track" else (AMBER_D if st == "At risk" else RED)),
                    f"{p:,}", f"{l}", f"{c}", f"{clients(c)}",
                    (lambda c_, p_: lambda s_, x, y, w, h: s_.text(x + w - 16, y + h / 2 + 5, f"{c_ / p_:.1%}", 13,
                                                                 700, GREEN_D if c_ / p_ >= 0.016 else RED,
                                                                 anchor="end"))(clients(c), p)])
    table(s, X0 + 1, by + 64, cols, rws, row_h=(bh - 64 - 36 - 8) / 5, head_h=34, size=13)
    s.link(X0, by, bw, bh, "w02")

    jx = X0 + bw + 20
    jw = 420
    card(s, jx, by, jw, bh, "Plans kept", "Route and lead journey plans", action="Plans →")
    with s.g("plan kept"):
        f = PROSPECTS_Q / PROSPECT_TARGET_Q
        ring(s, jx + 70, by + 124, 44, 10, f, STAGE["Prospect"])
        s.text(jx + 70, by + 131, f"{f:.0%}", 19, 700, INK, anchor="middle")
        s.text(jx + 132, by + 116, "Route targets met", 14, 700, INK)
        s.text(jx + 132, by + 136, f"{PROSPECTS_Q:,} of {PROSPECT_TARGET_Q:,} prospects", 12.5, 400, MUTED)
        s.text(jx + 132, by + 154, "that branch managers planned", 12.5, 400, MUTED)
    y = by + 196
    for lab, v, tot, col in [("Prospects on route journey plans", PROSPECT_TARGET_Q, PROSPECT_TARGET_Q, "#8A8DA6"),
                             ("Prospects made", PROSPECTS_Q, PROSPECT_TARGET_Q, STAGE["Prospect"]),
                             ("Leads put on lead journey plans", 3_410, LEADS_Q, STAGE["Lead"]),
                             ("Leads visited by officers", LEAD_VISITS_Q, LEADS_Q, TEAL)]:
        s.text(jx + 24, y, lab, 13, 400, INK2)
        s.text(jx + jw - 24, y, f"{v:,}", 13, 700, INK, anchor="end")
        progress(s, jx + 24, y + 9, jw - 48, v / tot, col, h=6)
        y += 32
    s.link(jx, by, jw, bh, "w10")

    ax = jx + jw + 20
    aw = X1 - ax
    card(s, ax, by, aw, bh, "Field staff needing attention", "Flagged every morning · 6 silent, 10 behind",
         action="All →")
    flags = [
        ("Rose Candiru", "RC", "Arua", "No prospect for 19 days", "Silent"),
        ("Denis Okiror", "DO", "Soroti", "No prospect for 13 days", "Silent"),
        ("Brian Ssali", "BS", "Kampala East", "Outside his territory 3 times this week", "Behind"),
        ("Samuel Wandera", "SW", "Mbale", "54% of route targets · weeks 4–7 empty", "Behind"),
        ("Fred Opio", "FO", "Gulu", "41 prospects with no follow-up", "Behind"),
    ]
    rh = (bh - 80) / len(flags)
    for i, (nm, ini, br, why, st) in enumerate(flags):
        yy = by + 72 + i * rh
        with s.g(f"flag {nm}"):
            if i:
                s.line(ax + 24, yy, ax + aw - 24, yy, LINE2)
            avatar(s, ax + 44, yy + rh / 2, 17, ini, RED if st == "Silent" else AMBER_D)
            s.text(ax + 72, yy + rh / 2 - 3, nm, 14, 600, INK)
            s.text(ax + 72 + tw(nm, 14, 600) + 6, yy + rh / 2 - 3, "· " + br, 12, 400, MUTED)
            s.text(ax + 72, yy + rh / 2 + 16, why, 12.5, 400, INK2, maxw=aw - 250)
            status_chip(s, ax + aw - 172, yy + rh / 2 - 11, st, h=22, size=11)
            button(s, ax + aw - 24, yy + rh / 2 - 15, "Open", "soft", h=30, size=12, anchor="end")
    s.link(ax, by, aw, bh, "w02")
    return s


# =====================================================================================
def w02_agents():
    s = shell("02 Agents performance", "Agents", ["Sales", "Agents"])
    page_head(s, "Sales agents", f"{AGENTS_N} sales agents · {QUARTER} · prospects against route targets, leads, and "
                                 "how many of their prospects became clients")
    with s.g("header actions"):
        x = X1
        x -= button(s, x, Y0 + 12, "Export", "secondary", icon="download", anchor="end") + 12
        x -= filter_btn(s, x - 220, Y0 + 13, "Sort", "KYC completed ↓", w=220) + 12
        x -= filter_btn(s, x - 190, Y0 + 13, "Branch", "All branches", w=190) + 12
        x -= seg(s, x - seg_width(["Sales agents 62", "Relationship officers 18"]), Y0 + 13,
                 ["Sales agents 62", "Relationship officers 18"], "Sales agents 62", h=38) + 12

    sy = Y0 + 84
    sw_ = (CW - 3 * 16) / 4
    stats = [("On track", "≥ 85% of route targets", 21, GREEN, "trendup"),
             ("At risk", "60–84% of route targets", 25, AMBER, "gauge"),
             ("Behind", "under 60% of route targets", 10, RED, "trenddown"),
             ("Silent", "no prospect in 14+ days", 6, "#8E1F1F", "userx")]
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
        s.text(X1, ty + 24, "Weekly prospects: darker = more · red outline = none that week", 12.5, 400, MUTED,
               anchor="end")
    tby = ty + 54
    cols = [("Agent", 260, "start"), ("Territory", 150, "start"), ("Weekly prospects W1–W13", 270, "start"),
            ("Prospects", 100, "end"), ("Vs route target", 170, "start"), ("Leads", 80, "end"),
            ("KYC completed", 120, "end"), ("Conv.", 90, "end"), ("Hours / day", 110, "end"),
            ("Last ping", 120, "start"), ("Status", 122, "start")]
    rows = []
    for (nm, ini, br, terr, p, l, c, t, wk, hrs, last, st) in AGENTS:
        col = {"On track": BRAND, "At risk": AMBER_D, "Behind": RED, "Silent": "#8E1F1F"}[st]
        rows.append([
            agent_cell(nm, ini, br, col), terr,
            (lambda wk_: lambda s_, x, y, w, h: heat_strip(s_, x + 16, y + h / 2 - 8, wk_, cell=15, gap=4,
                                                            max_v=230, h=16, color=STAGE["Prospect"]))(wk),
            f"{p:,}",
            (lambda fr_: lambda s_, x, y, w, h: (progress(s_, x + 16, y + h / 2 - 3, 90, fr_, perf_color(fr_), h=7),
                                                 s_.text(x + 116, y + h / 2 + 5, f"{fr_:.0%}", 12.5, 600,
                                                         INK2)))(p / t),
            f"{l}", f"{c}",
            (lambda c_, p_: lambda s_, x, y, w, h: s_.text(x + w - 16, y + h / 2 + 5, f"{c_ / p_:.1%}", 13, 700,
                                                         GREEN_D if c_ / p_ >= 0.016 else RED, anchor="end"))(clients(c), p),
            f"{hrs:.1f} h", last, chip_cell(st)])
    rh = (H - 28 - tby - 40 - 44) / len(rows)
    table(s, X0, tby, cols, rows, row_h=rh, head_h=40, size=13, hl=2)
    s.link(X0, tby + 40 + 2 * rh, CW, rh, "w03")
    with s.g("table footer"):
        s.text(X0 + 16, H - 44, f"Showing 12 of {AGENTS_N} sales agents · conversion = their prospects who became clients "
                                "(loan disbursed)", 13, 400, MUTED)
        s.text(X1 - 16, H - 44, "1  2  3  4  5  6  →", 13, 600, BRAND, anchor="end")
    return s


# =====================================================================================
def w03_agent():
    nm, ini, br, terr, p, l, c, t, wk, hrs, last, st = SARAH
    s = shell("03 Agent profile (Sarah Namuli)", "Agents", ["Sales", "Agents", nm])
    with s.g("profile header"):
        s.rect(X0, Y0, CW, 118, fill=CARD, rx=12, stroke=LINE)
        s.circle(X0 + 64, Y0 + 59, 38, fill=tint(BRAND, 0.15))
        s.text(X0 + 64, Y0 + 70, ini, 28, 700, BRAND, anchor="middle")
        s.text(X0 + 120, Y0 + 50, nm, 24, 700, INK)
        status_chip(s, X0 + 128 + tw(nm, 24, 700), Y0 + 30, st)
        s.text(X0 + 120, Y0 + 76, f"Sales Agent · Kampala East branch · territory {terr} · joined Mar 2024", 14, 400,
               INK2)
        s.text(X0 + 120, Y0 + 98, "Branch manager Moses Okello · staff ID LU-0877 · device: Samsung A15 (registered)",
               13, 400, MUTED)
        x = X1 - 24
        x -= button(s, x, Y0 + 39, "Her territory", "secondary", icon="layers", anchor="end") + 10
        s.link(x, Y0 + 39, 170, 40, "w11")
        button(s, x, Y0 + 39, "Route journey plan", "primary", icon="route", anchor="end")
        s.link(x - 210, Y0 + 39, 210, 40, "w10b")
    ky = Y0 + 136
    kw = (CW - 4 * 16) / 5
    k = [("userplus", STAGE["Prospect"], "Prospects", f"{p:,}", f"of {t:,} on her route journey plans · {p / t:.0%}", p / t),
         ("flag", STAGE["Lead"], "Leads generated", f"{l}", f"{l / p:.0%} of her prospects · team {LEADS_Q / PROSPECTS_Q:.0%}",
          None),
         ("idcard", STAGE["KYC completed"], "KYC completed", f"{c}", f"{c / l:.0%} of her leads · rank 3 of {AGENTS_N}",
          None),
         ("banknote", GREEN, "Clients · conversion", f"{clients(c)} · {clients(c) / p:.1%}", f"loans disbursed · company {CLIENTS_Q / PROSPECTS_Q:.1%}", None),
         ("clock", AMBER, "Time prospecting", f"{hrs} h", f"a day on route days · company {HOURS_PROSPECTING} h", None)]
    for i, (ic, col, lab, val, sub, fr) in enumerate(k):
        kpi(s, X0 + i * (kw + 16), ky, kw, 140, ic, col, lab, val, sub, fr)

    ry = ky + 156
    lw_ = 1100
    rh_ = H - 28 - ry
    card(s, X0, ry, lw_, rh_, "Where Sarah has worked: Q3 to date",
         "Every prospect, lead and client she found, from the GPS on her phone")
    with s.g("layer toggles"):
        x = X0 + lw_ - 24
        for lab, col, on in reversed([("Prospects 1,486", STAGE["Prospect"], True), ("Leads 286", STAGE["Lead"], True),
                                      ("KYC 41", GREEN, True), ("Routes", BRAND, True)]):
            w = tw(lab, 12, 600) + 44
            x -= w
            s.rect(x, ry + 24, w, 30, fill=tint(col, 0.1), rx=15, shadow=False)
            checkbox(s, x + 9, ry + 31, on, size=16, color=col)
            s.text(x + 32, ry + 44, lab, 12, 600, shade(col, 0.15))
            x -= 8
    mx, my, mw, mh = X0 + 16, ry + 72, lw_ - 32, rh_ - 88
    m = StreetMap(s, mx, my, mw, mh, seed=5, places=PLACES, lake=False)
    terr_poly = [m.P(*q) for q in [(0.2, 0.08), (0.72, 0.04), (0.78, 0.5), (0.5, 0.62), (0.22, 0.5)]]
    s.poly(terr_poly, fill=BRAND, op=0.05, stroke=BRAND, sw=2, dash="7 5", name="her territory")
    import random
    rnd = random.Random(21)
    routes = {"Kiwatule market": [(0.5, 0.16), (0.58, 0.24), (0.64, 0.34)],
              "Ntinda stage": [(0.3, 0.26), (0.36, 0.34), (0.42, 0.42)],
              "Kigoowa estates": [(0.42, 0.1), (0.5, 0.08), (0.56, 0.12)],
              "Ntinda schools": [(0.26, 0.4), (0.32, 0.48), (0.4, 0.52)]}
    for rname, pts in routes.items():
        pp = [m.P(*q) for q in pts]
        s.poly(pp, stroke=BRAND, sw=4, closed=False, name=f"route {rname}")
        s.text(pp[-1][0] + 10, pp[-1][1] + 4, rname, 11.5, 700, BRAND_D)
    with s.g("prospects"):
        for _ in range(420):
            rname = rnd.choice(list(routes))
            q = rnd.choice(routes[rname])
            px, py = m.P(q[0] + rnd.gauss(0, 0.035), q[1] + rnd.gauss(0, 0.04))
            s.circle(px, py, 3, fill=STAGE["Prospect"], op=0.55)
    with s.g("leads"):
        for _ in range(60):
            rname = rnd.choice(list(routes))
            q = rnd.choice(routes[rname])
            px, py = m.P(q[0] + rnd.gauss(0, 0.03), q[1] + rnd.gauss(0, 0.035))
            s.circle(px, py, 5, fill=STAGE["Lead"], stroke="#FFFFFF", sw=1.4)
    with s.g("clients"):
        for _ in range(16):
            rname = rnd.choice(list(routes))
            q = rnd.choice(routes[rname])
            map_pin(s, *m.P(q[0] + rnd.gauss(0, 0.025), q[1] + rnd.gauss(0, 0.03)), GREEN, None, 0.7)
    with s.g("legend"):
        lx, ly = mx + 16, my + mh - 104
        s.rect(lx, ly, 320, 88, fill=CARD, rx=10, stroke=LINE, op=0.96)
        items = [(STAGE["Prospect"], "Prospect: name, phone, location"), (STAGE["Lead"], "Lead: wants a loan · NIN, amount"),
                 (GREEN, "KYC completed by an officer")]
        for i, (col, lab) in enumerate(items):
            yy = ly + 26 + i * 22
            s.circle(lx + 22, yy - 4, 6, fill=col)
            s.text(lx + 38, yy, lab, 12, 400, INK2)
    with s.g("outside note"):
        s.rect(mx + mw - 300, my + mh - 64, 284, 48, fill=CARD, rx=10, stroke=LINE, op=0.96)
        s.icon("shield", mx + mw - 286, my + mh - 50, 18, GREEN_D, 2)
        s.text(mx + mw - 260, my + mh - 36, "98% of her prospects inside", 12.5, 700, INK)
        s.text(mx + mw - 260, my + mh - 20, "her territory · 4 outside, all 14 Aug", 11.5, 400, MUTED)

    fx = X0 + lw_ + 20
    fw = X1 - fx
    fh = 300
    card(s, fx, ry, fw, fh, "Client journey funnel", f"{QUARTER} · Sarah's own prospects")
    funnel(s, fx + 24, ry + 84, fw - 48, [("Prospects", p, STAGE["Prospect"]), ("Leads", l, STAGE["Lead"]),
                                          ("KYC completed", c, STAGE["KYC completed"])], row_h=40, gap=24, label_w=110)
    ay = ry + fh + 20
    card(s, fx, ay, fw, H - 28 - ay, "Today", "Kiwatule market route · 32 of 50 prospects · 2.6 h")
    acts = [("14:25", "Lead created", "Aisha Nalubega · UGX 2M for stock", STAGE["Lead"], "flag"),
            ("11:24", "KYC completed on her lead", "Florence Nambi · by Joel Byaruhanga", GREEN, "idcard"),
            ("10:52", "Prospect added", "Joseph Kiggundu · hardware shop", STAGE["Prospect"], "userplus"),
            ("09:02", "Started her route", "Kiwatule market · inside territory", MUTED, "navigation")]
    y = ay + 100
    for t_, what, who, col, ic in acts:
        with s.g(f"activity {what}"):
            s.circle(fx + 38, y + 4, 14, fill=tint(col, 0.14))
            s.icon(ic, fx + 30, y - 4, 16, col, 2.2)
            s.text(fx + 62, y, what, 13.5, 600, INK)
            s.text(fx + fw - 24, y, t_, 12, 400, MUTED, anchor="end")
            s.text(fx + 62, y + 18, who, 12, 400, MUTED, maxw=fw - 90)
        y += 50
    s.link(fx, ay + 100 + 50 - 20, fw, 44, "w06")
    return s


# =====================================================================================
PLACES = [("Ntinda", 0.33, 0.3), ("Kiwatule", 0.6, 0.2), ("Naalya", 0.82, 0.12), ("Kyambogo", 0.44, 0.52),
          ("Banda", 0.55, 0.62), ("Bukoto", 0.12, 0.35), ("Kisaasi", 0.18, 0.1), ("Kireka", 0.8, 0.5),
          ("Nakawa", 0.3, 0.72), ("Mbuya", 0.2, 0.9), ("Kira", 0.93, 0.3), ("Kigoowa", 0.45, 0.08)]


def w04_field_map():
    s = shell("04 Field map (live)", "Field map", ["Sales", "Field map"], user=SUPERVISOR, period="Day")
    page_head(s, "Field map", "Where the team is now, and every prospect, lead and visit today · Kampala East · "
                              "updated 11:42")
    with s.g("header actions"):
        x = X1
        x -= filter_btn(s, x - 220, Y0 + 13, "Branch", "Kampala East", w=220) + 12
        x -= filter_btn(s, x - 150, Y0 + 13, "Date", "Today", w=150) + 16
        for lab, col in reversed([("Prospects", STAGE["Prospect"]), ("Leads", STAGE["Lead"]),
                                  ("Officer visits", GREEN), ("Territories", BRAND)]):
            w = tw(lab, 13, 400) + 56
            x -= w
            toggle(s, x, Y0 + 22, True, color=col)
            s.text(x + 44, Y0 + 37, lab, 13, 400, INK2)

    my = Y0 + 80
    mw = 1170
    mh = H - 28 - my
    s.rect(X0, my, mw, mh, fill=CARD, rx=12, stroke=LINE, name="map card")
    m = StreetMap(s, X0 + 1, my + 1, mw - 2, mh - 2, seed=5, places=PLACES)
    from web2 import TERRITORIES, _territory_polys
    for (tn, ag, ini, n, routes, col, st), pts in zip(TERRITORIES, _territory_polys(m)):
        s.poly(pts, fill=col, op=0.05, stroke=col, sw=1.5, dash="7 5", name=f"territory {tn}")
    import random
    rnd = random.Random(3)
    centres = [(0.36, 0.3), (0.62, 0.3), (0.86, 0.26), (0.14, 0.34), (0.44, 0.12), (0.84, 0.66), (0.62, 0.66)]
    with s.g("prospects today"):
        for (cx_, cy_), (_, _, _, _, p, *_r) in zip(centres, TEAM):
            for _ in range(p):
                s.circle(*m.P(cx_ + rnd.gauss(0, 0.035), cy_ + rnd.gauss(0, 0.04)), 3.6, fill=STAGE["Prospect"],
                         op=0.7)
    with s.g("leads today"):
        for q in [(0.38, 0.26), (0.34, 0.36), (0.6, 0.34), (0.66, 0.26), (0.84, 0.3), (0.88, 0.2), (0.12, 0.3),
                  (0.16, 0.4), (0.58, 0.7), (0.4, 0.3)]:
            map_pin(s, *m.P(*q), STAGE["Lead"], None, 0.75)
    with s.g("officer visits"):
        for q, done in [((0.62, 0.4), True), ((0.56, 0.36), True), ((0.66, 0.44), True), ((0.7, 0.4), False),
                        ((0.82, 0.58), True), ((0.86, 0.5), False)]:
            if done:
                map_pin(s, *m.P(*q), GREEN, None, 0.9)
            else:
                s.circle(*m.P(*q), 8, fill=CARD, stroke=AMBER, sw=3, name="planned lead visit")
    for (nm, ini, st, t, p, tg, l, route, hrs), (fx, fy) in zip(TEAM, [(0.38, 0.32), (0.64, 0.32), (0.86, 0.22),
                                                                     (0.14, 0.32), (0.44, 0.1), (0.6, 0.8),
                                                                     (0.62, 0.62)]):
        px, py = m.P(fx, fy)
        col = {"Prospecting": GREEN, "Outside territory": RED, "Offline": "#8A8DA6"}.get(st, AMBER_D)
        agent_dot(s, px + 18, py - 18, ini, col, live=st in ("Prospecting", "Outside territory"), name=f"agent {nm}")
    for (nm, ini, *_r), (fx, fy) in zip(ROS, [(0.62, 0.4), (0.84, 0.52)]):
        px, py = m.P(fx, fy)
        agent_dot(s, px + 18, py - 18, ini, TEAL, live=True, name=f"officer {nm}")
    # alert popup on Brian, who is outside his territory
    px, py = m.P(0.6, 0.8)
    with s.g("alert popup"):
        bx, by_ = px + 44, py - 160
        s.rect(bx, by_, 320, 138, fill=CARD, rx=10, stroke=tint(RED, 0.6), sw=1.5)
        s.icon("alert", bx + 16, by_ + 14, 20, RED, 2)
        s.text(bx + 44, by_ + 30, "Brian Ssali left his territory", 14.5, 700, INK)
        s.text(bx + 16, by_ + 56, "Since 11:20 · 1.4 km outside Banda · Kyambogo", 12.5, 400, INK2)
        s.text(bx + 16, by_ + 76, "Route journey plan: Banda stage route · 3 of 50 prospects", 12.5, 400, MUTED)
        s.text(bx + 16, by_ + 96, "He and Moses were told at 11:25", 12.5, 400, MUTED)
        s.text(bx + 16, by_ + 124, "Open Brian's day →", 13, 600, BRAND)
    with s.g("legend"):
        lx, ly = X0 + 20, my + mh - 150
        s.rect(lx, ly, 330, 130, fill=CARD, rx=10, stroke=LINE, op=0.96)
        s.text(lx + 16, ly + 24, "Today", 13, 700, INK)
        items = [(STAGE["Prospect"], f"Prospect ({sum(t[4] for t in TEAM)} today)"),
                 (STAGE["Lead"], "Lead (wants a loan)"), (GREEN, "Officer visit: KYC completed"),
                 (AMBER, "Lead visit planned, not yet made")]
        for i, (col, lab) in enumerate(items):
            yy = ly + 46 + i * 20
            if col == AMBER:
                s.circle(lx + 24, yy - 4, 5, fill=CARD, stroke=AMBER, sw=2.5)
            else:
                s.circle(lx + 24, yy - 4, 6 if col != STAGE["Prospect"] else 4, fill=col)
            s.text(lx + 38, yy, lab, 12, 400, INK2)
        s.line(lx + 16, ly + 118, lx + 34, ly + 118, BRAND, 1.5, dash="5 4")
        s.text(lx + 40, ly + 122, "Territory boundary (geofence)", 12, 400, INK2)
    with s.g("map controls"):
        cx_ = X0 + mw - 56
        for i, ic in enumerate(["plus", "minus", "crosshair", "layers"]):
            y_ = my + 20 + i * 46
            s.rect(cx_, y_, 38, 38, fill=CARD, rx=8, stroke=LINE)
            if ic == "minus":
                s.line(cx_ + 11, y_ + 19, cx_ + 27, y_ + 19, INK2, 2.2, cap="round")
            else:
                s.icon(ic, cx_ + 9, y_ + 9, 20, INK2, 2)

    px0 = X0 + mw + 20
    pw = X1 - px0
    ph = 640
    card(s, px0, my, pw, ph, "Sales agents today", "Prospects against today's route target")
    y = my + 76
    for (nm, ini, st, t, p, tg, l, route, hrs) in TEAM:
        on = nm == "Sarah Namuli"
        col = {"Prospecting": GREEN, "Outside territory": RED, "Offline": "#8A8DA6"}.get(st, AMBER_D)
        with s.g(f"agent row {nm}"):
            if on:
                s.rect(px0 + 10, y - 6, pw - 20, 74, fill=tint(BRAND, 0.07), rx=8, stroke=tint(BRAND, 0.35))
            avatar(s, px0 + 42, y + 26, 18, ini, col)
            s.text(px0 + 72, y + 18, nm, 14, 600, INK)
            s.text(px0 + 72, y + 37, f"{route} · ping {t}", 12, 400, MUTED, maxw=250)
            chip(s, px0 + pw - 24 - tw(st, 11, 600) - 34, y + 4, st, col, h=22, size=11, dot=True)
            progress(s, px0 + 72, y + 50, 150, p / tg, perf_color(p / tg * 1.4), h=5)
            s.text(px0 + 232, y + 56, f"{p}/{tg} · {l} leads · {hrs:.1f} h", 11.5, 600, INK2)
        y += 80
    s.link(px0 + 10, my + 70, pw - 20, 74, "w03")
    uy = my + ph + 20
    card(s, px0, uy, pw, H - 28 - uy, "Relationship officers", "On lead journey plans today")
    y = uy + 74
    for nm, ini, st, last, v, k, plan, q in ROS:
        avatar(s, px0 + 42, y + 20, 18, ini, TEAL)
        s.text(px0 + 72, y + 16, nm, 14, 600, INK)
        s.text(px0 + 72, y + 35, f"{plan} · {v} visits · {k} KYC", 12, 400, MUTED)
        chip(s, px0 + pw - 24 - tw(st, 11, 600) - 34, y + 6, st, GREEN if st == "At a lead" else BRAND, h=22,
             size=11, dot=True)
        y += 58
    return s


# =====================================================================================
PIPE = {
    "Prospects": [("Joseph Kiggundu", None, "Met today · hardware shop", "Sarah Namuli", "SN", "today", None),
                          ("Tony Kizito", None, "Met Mon · phone kiosk", "Sarah Namuli", "SN", "2 days", None),
                          ("Moses Opolot", None, "Met 22 Sep · school", "Peter Kato", "PK", "8 days", "No follow-up"),
                          ("Doreen Atuhaire", None, "Met 21 Sep · salon", "Ruth Achieng", "RA", "9 days",
                           "No follow-up")],
    "Leads waiting for a plan": [(CALLEE["name"], CALLEE["amount"], "Lead today 14:25", "Sarah Namuli", "SN",
                                  "today", None),
                                 ("Paul Tumusiime", 10_000_000, "Lead since Mon", "Ivan Mugabe", "IM", "2 days", None),
                                 ("Henry Mukasa", 3_500_000, "Lead since 22 Sep", "Brian Ssali", "BS", "8 days",
                                  "Waiting 7+ days")],
    "On a lead journey plan": [("Ivan Kasozi", 3_000_000, "Joel · today 12:30", "Sarah Namuli", "SN", "1 day", None),
                       ("Robert Kizza", 7_000_000, "Christine · Thu 1 Oct", "Esther Nakato", "EN", "3 days", None),
                       ("Mary Nansubuga", 6_500_000, "Christine · Fri 2 Oct", "Ruth Achieng", "RA", "4 days", None)],
    "KYC completed": [(CLIENT["name"], CLIENT["amount"], "Joel · today 11:24", "Sarah Namuli", "SN", "today",
                               "Loan sent"),
                              ("Betty Nakimuli", 2_000_000, "Joel · today 10:20", "Sarah Namuli", "SN", "today", None),
                              ("Agnes Babirye", 1_800_000, "Christine · yesterday", "Esther Nakato", "EN", "1 day",
                               "Loan sent")],
    "Loan decision": [("Janet Kyomugisha", 4_000_000, "Approved 29 Sep", "Ruth Achieng", "RA", "Approved", None),
                      ("Ronald Byamugisha", 6_000_000, "Approved 28 Sep", "Ivan Mugabe", "IM", "Approved", None),
                      ("Prossy Namara", 5_000_000, "Rejected 28 Sep", "Brian Ssali", "BS", "Rejected",
                       "Affordability")],
}
PIPE_TOTALS = {"Prospects": (912, "not yet leads"), "Leads waiting for a plan": (64, "UGX 0.3B asked"),
               "On a lead journey plan": (118, "UGX 0.6B asked"), "KYC completed": (131, "this quarter"),
               "Loan decision": (96, "81 approved · 74 disbursed = clients")}


def w05_pipeline():
    s = shell("05 Client pipeline", "Client pipeline", ["Sales", "Client pipeline"], user=SUPERVISOR)
    page_head(s, "Client pipeline", "Kampala East · from a name on the street to a disbursed loan · every record belongs "
                                    "to Letshego")
    with s.g("header actions"):
        x = X1
        x -= seg(s, x - seg_width(["Board", "List", "Map"]), Y0 + 13, ["Board", "List", "Map"], "Board", h=38) + 12
        x -= filter_btn(s, x - 190, Y0 + 13, "Sales agent", "All 7", w=190) + 12
        x -= filter_btn(s, x - 210, Y0 + 13, "Branch", "Kampala East", w=210) + 12
    with s.g("lost summary"):
        y = Y0 + 72
        s.rect(X0, y, CW, 40, fill=CARD, rx=10, stroke=LINE)
        s.icon("info", X0 + 14, y + 10, 20, BRAND, 2)
        s.text(X0 + 44, y + 25, "Lost this quarter:", 13, 600, INK)
        x = X0 + 48 + tw("Lost this quarter:", 13, 600)
        for lab, n, col in [("Prospects who didn't want a loan", "3,826", RED),
                            ("Leads who said no at the visit", "214", AMBER_D), ("Prospects with no follow-up", "402",
                                                                                 AMBER_D)]:
            x += s.text(x + 8, y + 25, f"{lab} ", 13, 400, INK2) + 8
            x += s.text(x, y + 25, n, 13, 700, col) + 18
        s.text(X1 - 16, y + 25, "See the reasons →", 13, 600, BRAND, anchor="end")
        s.link(X1 - 180, y, 180, 40, "w09")

    cy = Y0 + 128
    ncol = len(PIPE)
    cwid = (CW - (ncol - 1) * 14) / ncol
    for i, (col_name, cards) in enumerate(PIPE.items()):
        x = X0 + i * (cwid + 14)
        color = PIPE_COLOR[col_name]
        n, total = PIPE_TOTALS[col_name]
        with s.g(f"column {col_name}"):
            s.rect(x, cy, cwid, H - 28 - cy, fill="#ECEDF4", rx=12, name="column bg")
            s.rect(x, cy, cwid, 4, fill=color, rx=2)
            s.text(x + 16, cy + 32, col_name, 14, 700, INK)
            s.text(x + cwid - 16, cy + 32, f"{n:,}", 13, 700, color, anchor="end")
            s.text(x + 16, cy + 52, total, 12, 400, MUTED)
            y = cy + 68
            for (nm, amt, sub, ag, ini, age, flag) in cards:
                hl = nm == CLIENT["name"]
                ch = 128
                with s.g(f"card {nm}"):
                    s.rect(x + 10, y, cwid - 20, ch, fill=CARD, rx=10,
                           stroke=BRAND if hl else LINE, sw=2 if hl else 1)
                    s.text(x + 24, y + 26, nm, 14, 600, INK, maxw=cwid - 60)
                    s.text(x + 24, y + 48, sub, 12.5, 400, INK2, maxw=cwid - 48)
                    s.text(x + 24, y + 74, ugx(amt) if amt else "No amount yet", 13, 600, INK if amt else FAINT)
                    if col_name == "Loan decision":
                        status_chip(s, x + cwid - 20 - tw(age, 11, 600) - 34, y + 60, age, h=20, size=11)
                    else:
                        s.text(x + cwid - 24, y + 74, age, 12, 400, MUTED, anchor="end")
                    s.line(x + 24, y + 90, x + cwid - 24, y + 90, LINE2)
                    avatar(s, x + 36, y + 109, 11, ini, BRAND)
                    s.text(x + 54, y + 113, ag, 12, 400, INK2, maxw=cwid - 80 - (tw(flag, 11, 600) if flag else 0))
                    if flag:
                        fcol = RED if flag in ("No follow-up", "Affordability") or "7+" in flag else GREEN_D
                        s.text(x + cwid - 24, y + 113, flag, 11, 600, fcol, anchor="end")
                if hl:
                    s.link(x + 10, y, cwid - 20, ch, "w06")
                y += ch + 10
            s.text(x + cwid / 2, H - 48, f"+ {n - len(cards):,} more", 12.5, 600, BRAND, anchor="middle")
    return s


# =====================================================================================
def w06_client():
    c = CLIENT
    s = shell("06 Client record (Florence Nambi)", "Client pipeline", ["Sales", "Client pipeline", c["name"]],
              user=SUPERVISOR)
    with s.g("client header"):
        s.rect(X0, Y0, CW, 110, fill=CARD, rx=12, stroke=LINE)
        s.circle(X0 + 60, Y0 + 55, 34, fill=tint(GREEN, 0.15))
        s.text(X0 + 60, Y0 + 65, c["initials"], 24, 700, GREEN_D, anchor="middle")
        s.text(X0 + 112, Y0 + 46, c["name"], 24, 700, INK)
        x = X0 + 124 + tw(c["name"], 24, 700)
        x += chip(s, x, Y0 + 27, "KYC completed", GREEN, dot=True) + 8
        chip(s, x, Y0 + 27, "Loan: awaiting approval", STATUS["Awaiting approval"])
        s.text(X0 + 112, Y0 + 74, f"Client {c['id']} · {c['business']} · 0772 418 ··· · NIN {c['nin']}", 14, 400,
               INK2)
        s.icon("shield", X0 + 112, Y0 + 83, 16, BRAND, 2)
        s.text(X0 + 134, Y0 + 96, "Kampala East › Ntinda · Kiwatule › Kiwatule market route · prospect and "
                                  "lead by Sarah Namuli · KYC by Joel Byaruhanga", 13, 600, BRAND)
        x = X1 - 24
        x -= button(s, x, Y0 + 35, "Open approval", "primary", icon="listcheck", anchor="end") + 10
        s.link(x + 10, Y0 + 35, 170, 40, "w08")
        button(s, x, Y0 + 35, "Territory", "secondary", icon="layers", anchor="end")
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
    with s.g("lead note"):
        s.rect(X0 + 24, y + 4, c1 - 48, 124, fill="#F7F7FC", rx=10)
        s.text(X0 + 40, y + 30, "From Sarah's lead", 12.5, 700, INK2)
        para(s, X0 + 40, y + 52, "Wants UGX 6M for a second industrial sewing machine before January. Uniform orders "
                                 "from 4 schools each term.", c1 - 80, 13, 400, INK2, lh=20)

    c2x = X0 + c1 + 20
    c2 = 560
    card(s, c2x, ty, c2, th, "KYC documents & checks", "Captured by Joel Byaruhanga · all GPS-stamped at the client")
    tw_ = (c2 - 48 - 2 * 12) / 3
    docs = [("id_front", "NIRA ID · front"), ("id_back", "NIRA ID · back"), ("selfie", "Selfie · live check"),
            ("shop", "Business premises"), ("doc", "Sales book (3 mo)"), ("moto", "Collateral · logbook")]
    for i, (k, lab) in enumerate(docs):
        doc_thumb(s, c2x + 24 + (i % 3) * (tw_ + 12), ty + 78 + (i // 3) * 142, tw_, 130, k, lab)
    y = ty + 378
    s.text(c2x + 24, y, "Checks", 15, 700, INK)
    y += 16
    checks = [("NIRA: NIN, name and photo match", "Verified 30 Sep 11:21 · same NIN as the lead", True),
              ("Phone registered to this name (MTN)", "Verified", True),
              ("Not already a Letshego client", "No match in core banking", True),
              ("Location inside the territory", "Kiwatule · 0.3712, 32.6205", True),
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
    steps = [("1", "Prospect", f"Sarah Namuli · {c['prospected']} · Kiwatule market · GPS ±6 m", STAGE["Prospect"]),
             ("2", "Lead", f"Sarah, {c['lead']} · wants UGX 6M · NIN and location", STAGE["Lead"]),
             ("3", "On a lead journey plan", "Moses Okello · Kiwatule leads · Joel Byaruhanga · 28 Sep", TEAL),
             ("4", "Visited", "Joel Byaruhanga · 30 Sep 11:14 · GPS ±9 m", TEAL),
             ("5", "KYC completed", "30 Sep 11:24 · 6 checks passed", GREEN),
             ("6", "Loan application sent", f"30 Sep 11:42 · {c['app_id']}", GREEN),
             ("7", "Loan disbursed: client", "After Moses Okello approves · waiting 18 min", None)]
    y = ty + 88
    for i, (n, lab, sub, col) in enumerate(steps):
        col_ = col or "#C4C7D6"
        with s.g(f"step {lab}"):
            if i < len(steps) - 1:
                nxt = steps[i + 1][3]
                s.line(c3x + 38, y + 14, c3x + 38, y + 58, nxt or LINE, 2, dash=None if nxt else "4 4")
            s.circle(c3x + 38, y, 14, fill=col_ if col else CARD, stroke=col_, sw=2)
            s.text(c3x + 38, y + 4.5, n, 12, 700, "#FFFFFF" if col else MUTED, anchor="middle")
            s.text(c3x + 64, y - 2, lab, 14, 600, INK if col else MUTED)
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
        s.text(c3x + 40, ly + 132, "When the loan is disbursed, she counts for", 12.5, 700, GREEN_D)
        for i, (who, why) in enumerate([("Sarah Namuli", "her prospect and lead"), ("Joel Byaruhanga", "his KYC"),
                                        ("Kampala East", "Q3: 98 clients so far")]):
            s.icon("check", c3x + 40, ly + 150 + i * 26, 14, GREEN, 2.8)
            s.text(c3x + 60, ly + 162 + i * 26, f"{who} · {why}", 12.5, 400, INK2)
        s.text(c3x + 40, ly + 266, "Client = loan disbursed: that is the conversion", 12.5, 600, GREEN_D)
    return s


BRANCH_FUNNEL = [("Prospects", 6_240, STAGE["Prospect"]), ("Leads generated", 1_090, STAGE["Lead"]),
                 ("KYC completed", 131, STAGE["KYC completed"])]

def w01b_branch():
    s = shell("01b Branch overview (Kampala East, today)", "Overview", ["Sales", "Kampala East today"],
              user=SUPERVISOR, period="Day")
    tp = sum(t[4] for t in TEAM)
    tt = sum(t[5] for t in TEAM)
    tl = sum(t[6] for t in TEAM)
    page_head(s, "Kampala East today", f"{len(TEAM)} sales agents on their routes · {len(ROS)} relationship officers "
                                       "on lead journey plans · updated 11:42")
    with s.g("header actions"):
        x = X1
        bw = button(s, x, Y0 + 12, "Plan tomorrow's routes", "primary", icon="route", anchor="end")
        s.link(x - bw, Y0 + 12, bw, 40, "w10c")
        x -= bw + 12
        bw = button(s, x, Y0 + 12, "Live map", "secondary", icon="map", anchor="end")
        s.link(x - bw, Y0 + 12, bw, 40, "w04")
        x -= bw + 16
        rule_note(s, x - 372, Y0 + 18)
    ky = Y0 + 84
    kw = (CW - 4 * 16) / 5
    kpis = [("userplus", STAGE["Prospect"], "Prospects today", f"{tp}", f"of {tt} on today's route journey plans · "
                                                                         f"{tp / tt:.0%}", tp / tt),
            ("flag", STAGE["Lead"], "Leads today", f"{tl}", "from earlier prospects", None),
            ("idcard", STAGE["KYC completed"], "KYC completed today", "3", "Joel 2, Christine 1 · applications sent", None),
            ("clock", AMBER, "Time prospecting", f"{sum(t[8] for t in TEAM):.1f} h",
             "across the team today · from GPS", None),
            ("alert", RED, "Alerts", "2", "Brian outside territory · Ivan idle 2 h", None)]
    for i, (ic, col, lab, val, sub, fr) in enumerate(kpis):
        kpi(s, X0 + i * (kw + 16), ky, kw, 140, ic, col, lab, val, sub, fr)
    s.link(X0 + 4 * (kw + 16), ky, kw, 140, "w04")

    ty = ky + 156
    th = H - 28 - ty
    lw = 1090
    card(s, X0, ty, lw, th, "Route journey plans today", "Each agent's route and target, set by you · live from their phones",
         action="Plans →")
    s.link(X0 + lw - 110, ty + 20, 110, 30, "w10")
    cols = [("Sales agent", 250, "start"), ("Route", 230, "start"), ("Prospects vs target", 250, "start"),
            ("Leads", 80, "end"), ("Hours", 90, "end"), ("Status", 188, "start")]
    rows = []
    for nm, ini, st, last, p, t, l, route, hrs in TEAM:
        col = {"Prospecting": GREEN, "Outside territory": RED, "Offline": "#8A8DA6"}.get(st, AMBER_D)
        rows.append([agent_cell(nm, ini, f"last ping {last}", col), route,
                     (lambda p_, t_: lambda s_, x, y, w, h: (progress(s_, x + 16, y + h / 2 - 3, 140, p_ / t_,
                                                                      perf_color(p_ / t_ * 1.4), h=7),
                                                             s_.text(x + 168, y + h / 2 + 5, f"{p_} / {t_}", 13, 600,
                                                                     INK2)))(p, t),
                     str(l), f"{hrs:.1f} h", chip_cell(st)])
    table(s, X0 + 1, ty + 72, cols, rows, row_h=(th - 72 - 36 - 70) / len(rows), head_h=36, size=13, hl=0)
    s.link(X0 + 1, ty + 108, lw - 2, (th - 72 - 36 - 70) / len(rows), "w03")
    with s.g("targets note"):
        y = ty + th - 54
        s.rect(X0 + 24, y, lw - 48, 38, fill="#F7F7FC", rx=10, shadow=False)
        s.icon("info", X0 + 38, y + 10, 18, BRAND, 2)
        s.text(X0 + 66, y + 24, "Targets are set per route in your route journey plans. Hours count only time on the route, "
                                "inside the agent's territory.", 12.5, 400, INK2)

    rx = X0 + lw + 20
    rw = X1 - rx
    fh = 330
    card(s, rx, ty, rw, fh, "Client journey funnel", f"Kampala East · {QUARTER}", action="Pipeline →")
    funnel(s, rx + 24, ty + 88, rw - 48, BRANCH_FUNNEL, row_h=44, gap=26, label_w=124)
    s.text(rx + 24, ty + fh - 22, f"98 clients (loans disbursed) · {98 / 6240:.1%} of prospects · company {CLIENTS_Q / PROSPECTS_Q:.1%}",
           12.5, 600, GREEN_D)
    s.link(rx, ty, rw, fh, "w05")
    oy = ty + fh + 20
    oh = H - 28 - oy
    card(s, rx, oy, rw, oh, "Lead journey plans today", "Relationship officers visiting leads", action="Plans →")
    y = oy + 76
    for nm, ini, st, last, v, k, plan, q in ROS:
        with s.g(f"officer {nm}"):
            avatar(s, rx + 44, y + 22, 18, ini, TEAL)
            s.text(rx + 72, y + 18, nm, 14, 600, INK)
            s.text(rx + 72, y + 37, f"{plan} · {v} visits · {k} KYC today", 12, 400, MUTED)
            chip(s, rx + rw - 24 - tw(st, 11, 600) - 34, y + 8, st, GREEN if st == "At a lead" else BRAND, h=22,
                 size=11, dot=True)
        y += 62
    s.link(rx, oy + 76, rw, 62, "w10d")
    with s.g("waiting leads"):
        y = oy + oh - 76
        s.rect(rx + 24, y, rw - 48, 56, fill=tint(BLUE, 0.07), rx=12, stroke=tint(BLUE, 0.3), shadow=False)
        s.text(rx + 40, y + 24, "14 new leads wait for a plan", 13.5, 700, INK)
        s.text(rx + 40, y + 43, "Oldest from Mon · put them on an officer's plan", 12, 400, MUTED)
        bw = button(s, rx + rw - 36, y + 12, "Make a plan", "primary", h=32, size=12.5, anchor="end")
        s.link(rx + rw - 36 - bw, y + 12, bw, 32, "w10e")
    return s

PIPE_COLOR = {"Prospects": STAGE["Prospect"], "Leads waiting for a plan": STAGE["Lead"],
              "On a lead journey plan": TEAL, "KYC completed": GREEN, "Loan decision": BRAND_D}


SCREENS = [w00_sign_in, w01_overview, w01b_branch, w02_agents, w03_agent, w04_field_map, w05_pipeline, w06_client]
