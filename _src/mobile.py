"""Agent field app (Android, Flutter), 360 x 800 screens.

The walkthrough follows Sarah Namuli's visit to Florence Nambi on 30 Sep: check-in, KYC, validation, negotiation,
close. Florence was first visited by John Mugisha in July and moved to Sarah when he left.
"""
from __future__ import annotations

from charts import StreetMap, map_pin, ring
from data import CLIENT, rnd_instalment, ugx
from kit import (AMBER, AMBER_D, BG, BLUE, BRAND, BRAND_D, BRAND_M, CARD, FAINT, GREEN, GREEN_D, INK, INK2, LINE,
                 LINE2, MUTED, PRODUCT, RED, STAGE, STATUS, SVG, TEAL, VIOLET, YELLOW, YELLOW_D, avatar, button,
                 checkbox, chip, field, para, progress, radio, shade, status_chip, tint, toggle, triangle, tw,
                 wordmark)
from web import doc_thumb

MW, MH = 360, 800
PAD = 16
NAV_H = 76


def phone(title: str, bg=BG, dark=False, time="11:05"):
    s = SVG(MW, MH, title)
    s.soft = True
    s.rect(0, 0, MW, MH, fill=bg, name="screen background")
    status_bar(s, dark, time)
    return s


def status_bar(s: SVG, dark=False, time="11:05"):
    fg = "#FFFFFF" if dark else INK
    with s.g("status bar"):
        s.text(PAD, 18, time, 12.5, 600, fg)
        x = MW - PAD
        s.rect(x - 22, 8, 20, 10, fill="none", stroke=fg, sw=1.2, rx=2, name="battery")
        s.rect(x - 20, 10, 13, 6, fill=fg, rx=1)
        s.rect(x - 1.5, 11, 2, 4, fill=fg, rx=1)
        for i in range(4):
            h = 3 + i * 2.2
            s.rect(x - 52 + i * 5, 17 - h, 3, h, fill=fg, rx=0.8, op=1 if i < 3 else 0.3, name="signal bar")
        s.text(x - 60, 18, "4G", 10.5, 700, fg, anchor="end", name="network")


def app_bar(s: SVG, title, back=None, sub=None, right=None, dark=False):
    bg = BRAND if dark else CARD
    fg = "#FFFFFF" if dark else INK
    with s.g("app bar"):
        s.rect(0, 24, MW, 56, fill=bg, name="app bar bg")
        if not dark:
            s.line(0, 80, MW, 80, LINE)
        x = PAD
        if back:
            s.icon("arrowleft", x, 40, 24, fg, 2)
            x += 40
        if sub:
            s.text(x, 48, title, 16.5, 600, fg, maxw=MW - x - 50)
            s.text(x, 67, sub, 12, 400, "#C9C8EE" if dark else MUTED, maxw=MW - x - 50)
        else:
            s.text(x, 58, title, 18, 600, fg)
        if right:
            s.icon(right, MW - PAD - 24, 40, 24, fg, 2)
    if back:
        s.link(0, 24, 56, 56, back)


def bottom_nav(s: SVG, active="Home"):
    items = [("Home", "home", "m03"), ("Clients", "users", "m17"), ("Visit", None, "m05"), ("Plans", "route", "m04"),
             ("Me", "user", "m19")]
    bx, by, bw, bh = 12, MH - 84, MW - 24, 64
    w = bw / 5
    for i, (_, _, tgt) in enumerate(items):
        s.link(bx + i * w, by - (24 if i == 2 else 0), w, bh + (24 if i == 2 else 0), tgt)
    with s.g("bottom navigation"):
        s.rect(bx, by, bw, bh, fill=CARD, rx=24, shadow=True, name="nav bg")
        for i, (lab, ic, _) in enumerate(items):
            cx = bx + i * w + w / 2
            on = lab == active
            with s.g(f"tab {lab}"):
                if ic is None:
                    s.circle(cx, by + 4, 27, fill=BRAND if on else YELLOW, stroke=BG, sw=5, shadow=True,
                             name="visit button")
                    s.icon("plus", cx - 12, by - 8, 24, YELLOW if on else BRAND_D, 2.8)
                    s.text(cx, by + bh - 11, lab, 11, 700 if on else 600, BRAND if on else INK2, anchor="middle")
                    continue
                if on:
                    s.rect(cx - 24, by + 9, 48, 30, fill=tint(BRAND, 0.1), rx=15, name="indicator")
                s.icon(ic, cx - 11, by + 13, 22, BRAND if on else "#9A9CB0", 2)
                s.text(cx, by + bh - 11, lab, 11, 700 if on else 400, BRAND if on else "#8A8DA6", anchor="middle")
    s.rect(MW / 2 - 54, MH - 8, 108, 4, fill=INK, rx=2, op=0.3, name="gesture bar")


def gesture(s: SVG, dark=False):
    s.rect(MW / 2 - 54, MH - 8, 108, 4, fill="#FFFFFF" if dark else INK, rx=2, op=0.45, name="gesture bar")


def footer(s: SVG, primary, target, icon=None, secondary=None, sec_target=None, color=BRAND):
    with s.g("footer"):
        s.rect(0, MH - 84, MW, 84, fill=CARD)
        s.line(0, MH - 84, MW, MH - 84, LINE)
        if secondary:
            button(s, PAD, MH - 70, secondary, "secondary", w=100, h=48)
            s.link(PAD, MH - 70, 100, 48, sec_target)
            button(s, PAD + 112, MH - 70, primary, "primary", icon=icon, w=MW - 2 * PAD - 112, h=48, color=color)
            s.link(PAD + 112, MH - 70, MW - 2 * PAD - 112, 48, target)
        else:
            button(s, PAD, MH - 70, primary, "primary", icon=icon, w=MW - 2 * PAD, h=48, color=color)
            s.link(PAD, MH - 70, MW - 2 * PAD, 48, target)
    gesture(s)


def stepper(s: SVG, y, step, labels=("Details", "ID & photos", "Income")):
    with s.g("kyc steps"):
        n = len(labels)
        w = (MW - 2 * PAD) / n
        for i, lab in enumerate(labels):
            x = PAD + i * w
            done, cur = i < step - 1, i == step - 1
            s.rect(x + 2, y, w - 4, 4, fill=BRAND if (done or cur) else LINE, rx=2)
            s.text(x + 2, y + 20, f"{i + 1} {lab}", 11.5, 600 if cur else 400,
                   BRAND if cur else (INK2 if done else FAINT))


def m_field(s: SVG, y, label, value, placeholder=False, dropdown=False, icon=None, required=True, h=46, suffix=None,
            ok=None):
    return field(s, PAD, y, MW - 2 * PAD, label, value, h=h, placeholder=placeholder, dropdown=dropdown, icon=icon,
                 required=required, suffix=suffix, size=14.5, ok=ok)


def pills(s: SVG, x0, y, items, maxw=MW - PAD, size=12.5, h=32, gap=8):
    """Toggle chips that wrap. items: [(label, on)]. Returns the y below the last row."""
    x = x0
    for lab, on in items:
        w = tw(lab, size, 600) + (38 if on else 26)
        if x + w > maxw:
            x = x0
            y += h + gap
        with s.g(f"pill {lab}"):
            s.rect(x, y, w, h, fill=tint(BRAND, 0.1) if on else CARD, rx=h / 2, stroke=BRAND if on else "#CDD0DE")
            if on:
                s.icon("check", x + 11, y + (h - 14) / 2, 14, BRAND, 2.6)
            s.text(x + (29 if on else 13), y + h / 2 + size * 0.36, lab, size, 600, BRAND if on else INK2)
        x += w + gap
    return y + h


def check_row(s: SVG, y, title, sub, ok=True, color=GREEN):
    s.circle(PAD + 14, y + 14, 12, fill=tint(color if ok else AMBER, 0.15))
    s.icon("check" if ok else "clock", PAD + 6, y + 6, 16, color if ok else AMBER_D, 2.8 if ok else 2.2)
    s.text(PAD + 36, y + 13, title, 13.5, 600, INK, maxw=MW - 2 * PAD - 40)
    s.text(PAD + 36, y + 31, sub, 12, 400, MUTED, maxw=MW - 2 * PAD - 40)


def visit_bar(s: SVG, text):
    """Strip under the app bar while a visit is open (checked in, not yet checked out)."""
    with s.g("visit in progress"):
        s.rect(0, 80, MW, 30, fill=tint(GREEN, 0.12))
        s.circle(PAD + 6, 95, 4.5, fill=GREEN)
        s.text(PAD + 18, 99.5, text, 12, 600, GREEN_D, maxw=MW - 2 * PAD - 20)


def option_row(s: SVG, y, icon, color, title, sub, target=None, h=54):
    with s.g(f"option {title}"):
        s.rect(PAD, y, MW - 2 * PAD, h, fill=CARD, rx=12, stroke=LINE)
        s.circle(PAD + 28, y + h / 2, 16, fill=tint(color, 0.14))
        s.icon(icon, PAD + 19, y + h / 2 - 9, 18, color, 2.2)
        s.text(PAD + 54, y + h / 2 - 3, title, 14, 600, INK)
        s.text(PAD + 54, y + h / 2 + 15, sub, 12, 400, MUTED, maxw=MW - 2 * PAD - 90)
        s.icon("chevright", MW - PAD - 28, y + h / 2 - 10, 20, FAINT)
    if target:
        s.link(PAD, y, MW - 2 * PAD, h, target)


# =====================================================================================
def m01_splash():
    s = phone("M1 Splash", bg=BRAND, dark=True, time="08:02")
    with s.g("facets", opacity=0.08):
        s.poly([(250, 470), (470, 860), (30, 860)], fill="#FFFFFF")
        s.poly([(60, 60), (200, 300), (-80, 300)], fill="#FFFFFF")
    triangle(s, MW / 2 - 48, 270, 96)
    s.text(MW / 2, 420, "Letshego", 40, 700, "#FFFFFF", anchor="middle", italic=True)
    s.text(MW / 2, 452, "Field Sales", 17, 400, "#C9C8EE", anchor="middle")
    with s.g("loader"):
        for i in range(3):
            s.circle(MW / 2 - 16 + i * 16, 560, 4, fill=YELLOW, op=1 - i * 0.3)
    s.text(MW / 2, MH - 40, "Improving lives", 13, 400, "#A9A8DC", anchor="middle")
    gesture(s, True)
    s.link(0, 0, MW, MH, "m02")
    return s


def m02_sign_in():
    s = phone("M2 Sign in", bg=BRAND, dark=True, time="08:02")
    with s.g("facets", opacity=0.08):
        s.poly([(290, 60), (420, 300), (160, 300)], fill="#FFFFFF")
    wordmark(s, PAD + 4, 96, 28, "#FFFFFF")
    s.text(PAD + 4, 124, "Field Sales · Uganda", 14, 400, "#C9C8EE")
    s.text(PAD + 4, 190, "Welcome back,", 15, 400, "#DCDBF6")
    s.text(PAD + 4, 218, "Sarah", 26, 700, "#FFFFFF")
    with s.g("sheet"):
        s.rect(0, 256, MW, MH - 256, fill=CARD, rx=24, name="sheet bg")
        s.rect(0, 290, MW, MH - 290, fill=CARD)
        y = 284
        y += m_field(s, y, "Staff ID", "LU-0877", icon="user") + 14
        s.text(PAD, y + 14, "PIN", 13, 600, INK2)
        with s.g("pin boxes"):
            bw = (MW - 2 * PAD - 5 * 8) / 6
            for i in range(6):
                x = PAD + i * (bw + 8)
                s.rect(x, y + 24, bw, 50, fill=CARD, rx=10, stroke=BRAND if i == 4 else "#CDD0DE",
                       sw=2 if i == 4 else 1)
                if i < 4:
                    s.circle(x + bw / 2, y + 49, 6, fill=INK)
        y += 96
        button(s, PAD, y, "Sign in", "primary", w=MW - 2 * PAD, h=50, size=15.5)
        s.link(PAD, y, MW - 2 * PAD, 50, "m03")
        y += 66
        with s.g("fingerprint"):
            s.icon("fingerprint", MW / 2 - 18, y, 36, BRAND, 1.8)
            s.text(MW / 2, y + 58, "Use fingerprint", 13, 600, BRAND, anchor="middle")
        s.link(MW / 2 - 70, y, 140, 70, "m03")
        with s.g("device note"):
            yy = MH - 110
            s.rect(PAD, yy, MW - 2 * PAD, 62, fill="#F5F5FB", rx=12)
            s.icon("shield", PAD + 14, yy + 18, 22, BRAND, 2)
            s.text(PAD + 46, yy + 27, "This phone is registered to you", 13, 600, INK)
            s.text(PAD + 46, yy + 46, "Sign-in works offline after the first time", 12, 400, MUTED)
    gesture(s)
    return s


HERO = "#16171F"


def m03_home():
    s = phone("M3 Home", bg=BG)
    s.raw('<defs><linearGradient id="heroGrad" x1="0" y1="0" x2="1" y2="1">'
          '<stop offset="0" stop-color="#FFE45C"/><stop offset="1" stop-color="#FBC805"/></linearGradient></defs>')
    with s.g("top"):
        s.circle(PAD + 22, 70, 22, fill=YELLOW)
        s.text(PAD + 22, 76, "SN", 15, 700, BRAND_D, anchor="middle")
        s.text(PAD + 54, 63, "Good morning", 12.5, 400, MUTED)
        s.text(PAD + 54, 84, "Sarah Namuli", 19, 700, INK)
        for i, ic in enumerate(["search", "bell"]):
            cx = MW - PAD - 20 - i * 48
            s.circle(cx, 70, 20, fill=CARD, shadow=True)
            s.icon(ic, cx - 10, 60, 20, INK, 2)
        s.circle(MW - PAD - 12, 60, 4.5, fill=RED)
    with s.g("hero"):
        y = 108
        HI, HM = "#231F0F", "#6B5A1E"
        s.rect(PAD, y, MW - 2 * PAD, 164, fill="url(#heroGrad)", rx=24, name="hero bg")
        s.poly([(MW - PAD - 128, y + 164), (MW - PAD, y + 36), (MW - PAD, y + 140), (MW - PAD - 24, y + 164)],
               fill="#FFFFFF", op=0.22, name="facet")
        s.text(PAD + 20, y + 30, "Q3 CONVERSIONS", 10.5, 700, HM, spacing=1)
        s.text(PAD + 20, y + 80, "18", 46, 700, HI)
        s.text(PAD + 22 + tw("18", 46, 700), y + 80, "/22", 20, 600, HM)
        s.text(PAD + 20, y + 104, "4 to go · quarter ends today", 12.5, 600, HM)
        with s.g("mini chart"):
            weeks = [22, 18, 15, 14, 16, 15, 17, 14, 16, 17, 16, 18, 16]
            x0, x1, base = MW - PAD - 136, MW - PAD - 20, y + 86
            bw = (x1 - x0) / 13
            s.text(x0, y + 30, "Visits / week", 10.5, 700, HM)
            for i, v in enumerate(weeks):
                h_ = 44 * v / 22
                s.rect(x0 + i * bw + 2, base - h_, bw - 4, h_, fill=HI, rx=2.5, op=1 if i == 12 else 0.22)
            s.text(x0, y + 104, "✓ no quiet weeks", 10.5, 700, "#0D5A34")
        s.rect(PAD + 20, y + 122, MW - 2 * PAD - 40, 6, fill="#FFFFFF", rx=3, op=0.55)
        s.rect(PAD + 20, y + 122, (MW - 2 * PAD - 40) * 18 / 22, 6, fill=HI, rx=3)
        s.text(PAD + 20, y + 150, "82% of target", 12, 700, HI)
        s.icon("trophy", MW - PAD - 120, y + 138, 14, HI, 2)
        s.text(MW - PAD - 20, y + 150, "Rank 3 of 62", 12, 700, HI, anchor="end")
    with s.g("stats"):
        y = 286
        cw = (MW - 2 * PAD - 16) / 3
        for i, (lab, val, sub, subcol) in enumerate([("Visits today", "3", "2 planned · 1 off", MUTED),
                                                      ("KYCs · week", "4", "▲ 2 vs last week", GREEN_D),
                                                      ("Conv. · week", "1", "Florence is next", MUTED)]):
            x = PAD + i * (cw + 8)
            s.rect(x, y, cw, 84, fill=CARD, rx=18, stroke=LINE)
            s.text(x + 14, y + 24, lab, 11, 600, MUTED, maxw=cw - 20)
            s.text(x + 14, y + 55, val, 24, 700, INK)
            s.text(x + 14, y + 73, sub, 10.5, 600 if subcol != MUTED else 400, subcol, maxw=cw - 20)
    with s.g("up next"):
        s.text(PAD, 400, "Up next", 15, 700, INK)
        s.text(MW - PAD, 400, "Kiwatule follow-ups", 12, 400, MUTED, anchor="end")
        y = 412
        s.rect(PAD, y, MW - 2 * PAD, 76, fill=CARD, rx=20, stroke=LINE)
        avatar(s, PAD + 38, y + 38, 22, "FN", GREEN)
        s.text(PAD + 70, y + 34, CLIENT["name"], 15, 700, INK)
        s.text(PAD + 70, y + 54, "Take KYC · 0.6 km · 4 min", 12, 400, MUTED)
        s.circle(MW - PAD - 38, y + 38, 22, fill=BRAND)
        s.icon("arrowright", MW - PAD - 48, y + 28, 20, "#FFFFFF", 2.4)
        s.link(PAD, y, MW - 2 * PAD, 76, "m09")
    with s.g("today"):
        s.text(PAD, 516, "Today", 15, 700, INK)
        s.text(PAD + 52, 516, "5 visits · 2 left", 12, 400, MUTED)
        y = 528
        s.rect(PAD, y, MW - 2 * PAD, 92, fill=CARD, rx=20, stroke=LINE)
        items = [("KL", "Kenneth", "09:05", "done", False), ("BN", "Betty", "10:20", "done", False),
                 ("JK", "Joseph", "off plan", "done", True), ("FN", "Florence", "Next", "next", False),
                 ("IK", "Ivan", "12:30", "later", False)]
        n = len(items)
        x0, x1 = PAD + 36, MW - PAD - 36
        cy = y + 34
        s.line(x0, cy, x1, cy, LINE2, 2)
        s.line(x0, cy, x0 + (x1 - x0) * 3 / (n - 1), cy, tint(GREEN, 0.5), 2)
        for i, (ini, nm, tm, st, off) in enumerate(items):
            cx = x0 + (x1 - x0) * i / (n - 1)
            col = {"done": "#B5B7C6" if off else GREEN, "next": BRAND}.get(st, "#D5D7E0")
            if st == "next":
                s.circle(cx, cy, 21, fill=tint(BRAND, 0.14))
            s.circle(cx, cy, 15, fill=col if st != "later" else CARD, stroke=col, sw=2)
            s.text(cx, cy + 4, ini, 10, 700, "#FFFFFF" if st != "later" else INK2, anchor="middle")
            s.text(cx, cy + 32, nm, 11, 700 if st == "next" else 400, INK if st == "next" else INK2, anchor="middle")
            s.text(cx, cy + 46, tm, 10, 600 if (off or st == "next") else 400,
                   AMBER_D if off else (BRAND if st == "next" else MUTED), anchor="middle")
        s.link(x0 + (x1 - x0) * 3 / (n - 1) - 22, cy - 22, 44, 70, "m09")
    with s.g("plans shortcut"):
        y = 634
        s.rect(PAD, y, MW - 2 * PAD, 50, fill=CARD, rx=16, stroke=LINE)
        s.rect(PAD + 10, y + 9, 32, 32, fill=tint(YELLOW, 0.3), rx=10)
        s.icon("route", PAD + 17, y + 16, 18, YELLOW_D, 2.2)
        s.text(PAD + 54, y + 22, "2 active journey plans", 13, 700, INK)
        s.text(PAD + 54, y + 39, "Kiwatule follow-ups · 7 of 12 visited", 11.5, 400, MUTED)
        s.icon("chevright", MW - PAD - 30, y + 15, 20, FAINT)
        s.link(PAD, y, MW - 2 * PAD, 50, "m04")
    bottom_nav(s, "Home")
    return s


MY_PLANS = [
    ("Kiwatule follow-ups", "28 Sep – 2 Oct", "Interested clients from September; take KYC where ready", 7, 12,
     "2 due today", "Moses Okello", "Active"),
    ("Ntinda schools: payroll teachers", "21 Sep – 9 Oct", "Teachers at 5 schools · Civil Servant Loan", 6, 15,
     "none due today", "Moses Okello", "Active"),
    ("Kyanja market prospecting", "1 – 31 Oct", "New area: market vendors, 3 new clients a day", 0, 8,
     "starts tomorrow", "You · approved by Moses", "Scheduled"),
]


def m04_plans():
    s = phone("M4 Journey plans", bg=BG, time="11:06")
    app_bar(s, "Journey plans", back="m03", sub="Client lists with dates · from Moses or you", right="plus")
    s.link(MW - 60, 24, 60, 56, "m04c")
    with s.g("filter chips"):
        x = PAD
        for lab, on in [("All 3", True), ("Active 2", False), ("Scheduled 1", False), ("Done 12", False)]:
            w = tw(lab, 12.5, 600) + 26
            s.rect(x, 94, w, 32, fill=BRAND if on else CARD, rx=16, stroke=None if on else "#CDD0DE")
            s.text(x + 13, 114.5, lab, 12.5, 600, "#FFFFFF" if on else INK2)
            x += w + 8
    y = 138
    for i, (nm, dates, desc, v, n, due, by, st) in enumerate(MY_PLANS):
        with s.g(f"plan {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 120, fill=CARD, rx=14, stroke=BRAND if i == 0 else LINE, sw=2 if i == 0 else 1)
            s.text(PAD + 14, y + 26, nm, 14.5, 700, INK, maxw=MW - 2 * PAD - 110)
            chip(s, MW - PAD - 14 - tw(st, 11, 600) - 34, y + 12, st, STATUS[st], h=22, size=11, dot=True)
            s.icon("calendar", PAD + 14, y + 36, 14, INK2, 2)
            s.text(PAD + 34, y + 48, f"{dates} · by {by}", 12, 600, INK2, maxw=MW - 2 * PAD - 50)
            s.text(PAD + 14, y + 68, desc, 12, 400, MUTED, maxw=MW - 2 * PAD - 28)
            progress(s, PAD + 14, y + 84, MW - 2 * PAD - 28, v / n, GREEN if v else LINE, h=6)
            s.text(PAD + 14, y + 108, f"{v} of {n} visited · {due}", 12, 600, INK2)
        if i == 0:
            s.link(PAD, y, MW - 2 * PAD, 120, "m04b")
        y += 130
    bottom_nav(s, "Plans")
    return s


def m04b_plan():
    s = phone("M4b Journey plan: Kiwatule follow-ups", bg=BG, time="11:07")
    app_bar(s, "Kiwatule follow-ups", back="m04", sub="28 Sep – 2 Oct · set by Moses Okello", right="more")
    with s.g("plan info"):
        y = 92
        s.rect(PAD, y, MW - 2 * PAD, 68, fill=CARD, rx=12, stroke=LINE)
        s.text(PAD + 14, y + 22, "Interested clients from September; take KYC", 12.5, 400, INK2, maxw=MW - 2 * PAD - 28)
        s.text(PAD + 14, y + 38, "where ready · goal: 4 KYCs, 2 applications", 12.5, 400, INK2)
        progress(s, PAD + 14, y + 50, MW - 2 * PAD - 110, 7 / 12, GREEN, h=6)
        s.text(MW - PAD - 14, y + 56, "7 of 12", 12.5, 700, INK, anchor="end")
    m = StreetMap(s, PAD, 172, MW - 2 * PAD, 196, seed=11, lake=False, dense=0.7,
                  places=[("Ntinda", 0.25, 0.2), ("Kiwatule", 0.7, 0.3)])
    s.rect(PAD, 172, MW - 2 * PAD, 196, fill="none", rx=12, stroke=LINE)
    spots = [(0.1, 0.15), (0.22, 0.3), (0.34, 0.18), (0.46, 0.34), (0.3, 0.52), (0.42, 0.66), (0.56, 0.54),
             (0.66, 0.4), (0.8, 0.52), (0.88, 0.72), (0.7, 0.84), (0.52, 0.86)]
    pts = [m.P(*q) for q in spots]
    s.poly(pts, stroke=BRAND, sw=2.5, closed=False, dash="2 6", name="plan route")
    for i, (qx, qy) in enumerate(pts):
        col = GREEN if i < 7 else (BRAND if i < 9 else "#8A8DA6")
        map_pin(s, qx, qy, col, str(i + 1), 0.72, name=f"client {i + 1}")
    s.text(PAD, 394, "Clients in visit order", 15, 700, INK)
    s.text(MW - PAD, 394, "Show visited (7)", 12.5, 600, BRAND, anchor="end")
    rows = [("6", "Kenneth Lubega", "Visited 09:05 · employer letter pending", "done"),
            ("7", "Betty Nakimuli", "Visited 10:20 · KYC validated", "done"),
            ("8", CLIENT["name"], "Due today · Interested · 0.6 km", "next"),
            ("9", "Ivan Kasozi", "Due today 12:30 · Negotiation", "due"),
            ("10", "Aisha Nalubega", "Thu 1 Oct · Interested", "later")]
    y = 408
    for n, nm, sub, st in rows:
        nxt = st == "next"
        with s.g(f"row {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 50, fill=CARD, rx=12, stroke=BRAND if nxt else LINE, sw=2 if nxt else 1)
            col = {"done": GREEN, "next": BRAND, "due": BRAND}.get(st, "#8A8DA6")
            s.circle(PAD + 24, y + 25, 12, fill=col if st != "later" else CARD, stroke=col, sw=2)
            if st == "done":
                s.icon("check", PAD + 18, y + 19, 12, "#FFFFFF", 3.2)
            else:
                s.text(PAD + 24, y + 29.5, n, 11, 700, "#FFFFFF" if st in ("next", "due") else INK2, anchor="middle")
            s.text(PAD + 46, y + 21, nm, 13.5, 600, INK)
            s.text(PAD + 46, y + 38, sub, 11.5, 400, MUTED, maxw=190 if nxt else 250)
            if nxt:
                button(s, MW - PAD - 10, y + 10, "Check in", "primary", h=30, size=12, anchor="end")
        if nxt:
            s.link(PAD, y, MW - 2 * PAD, 50, "m09")
        y += 56
    bottom_nav(s, "Plans")
    return s


def m04c_new_plan():
    s = phone("M4c New journey plan (by the agent)", bg=CARD, time="11:08")
    app_bar(s, "New journey plan", back="m04", sub="Moses approves plans you create")
    y = 96
    y += m_field(s, y, "Plan name", "Kyanja market prospecting", h=42) + 10
    s.text(PAD, y + 14, "Description", 13, 600, INK2)
    s.rect(PAD, y + 22, MW - 2 * PAD, 62, fill=CARD, rx=8, stroke="#CDD0DE")
    para(s, PAD + 12, y + 45, "New area. Market vendors and boda riders; aim for 3 new clients a day.",
         MW - 2 * PAD - 24, 13, 400, INK, lh=19)
    y += 96
    hw = (MW - 2 * PAD - 10) / 2
    field(s, PAD, y, hw, "Start", "Thu 1 Oct", h=42, icon="calendar", size=13.5, required=True)
    field(s, PAD + hw + 10, y, hw, "End", "Sat 31 Oct", h=42, icon="calendar", size=13.5, required=True)
    y += 78
    s.text(PAD, y + 14, "Clients (3)", 14, 700, INK)
    s.text(MW - PAD, y + 14, "+ Add clients", 13, 600, BRAND, anchor="end")
    y += 26
    for nm, sub in [("Tony Kizito", "Interested · Kyanja"), ("Ronald Mubiru", "Interested · Kyanja"),
                    ("Faith Ahimbisibwe", "Interested · Kyanja market")]:
        with s.g(f"client {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 44, fill="#F7F7FC", rx=10)
            s.icon("menu", PAD + 10, y + 14, 16, FAINT, 2)
            s.text(PAD + 36, y + 19, nm, 13.5, 600, INK)
            s.text(PAD + 36, y + 35, sub, 11.5, 400, MUTED)
            s.icon("x", MW - PAD - 28, y + 14, 16, MUTED, 2)
        y += 50
    with s.g("new clients slots"):
        y += 4
        s.text(PAD, y + 14, "Leave room for new clients", 13.5, 600, INK)
        s.text(PAD, y + 32, "3 a day · counted as planned visits", 12, 400, MUTED)
        toggle(s, MW - PAD - 36, y + 8, True)
    footer(s, "Send to Moses for approval", "m04", icon="send")
    return s


def m07_first_visit():
    s = phone("M7 First visit: is the client interested?", bg=BG, time="10:56")
    app_bar(s, "First visit · Joseph Kiggundu", back="m06", sub="Kiggundu Hardware · Ntinda · off plan")
    visit_bar(s, "Visit in progress · checked in 10:52 · GPS ±7 m")
    with s.g("purpose"):
        y = 122
        s.rect(PAD, y, MW - 2 * PAD, 58, fill=CARD, rx=12, stroke=LINE)
        s.text(PAD + 14, y + 22, "PURPOSE OF THIS VISIT", 10.5, 700, MUTED, spacing=0.8)
        s.text(PAD + 14, y + 43, "Introduce Letshego and find out his needs", 13.5, 600, INK)
    y = 200
    s.text(PAD, y + 4, "What would he need money for?", 13, 600, INK2)
    y = pills(s, PAD, y + 14, [("Business stock", True), ("School fees", True), ("Equipment", False),
                               ("Home", False), ("Emergency", False)], h=30) + 14
    s.text(PAD, y + 4, "Products that might suit (your notes)", 13, 600, INK2)
    y = pills(s, PAD, y + 14, [("MSE Business Loan", True), ("School Fees Loan", True), ("Home Improvement", False)],
              h=30) + 12
    with s.g("note"):
        s.rect(PAD, y, MW - 2 * PAD, 50, fill=CARD, rx=10, stroke="#CDD0DE")
        s.text(PAD + 12, y + 30, "Busy shop. Pays a SACCO loan until December.", 13, 400, INK, maxw=MW - 2 * PAD - 50)
        s.icon("mic", MW - PAD - 32, y + 15, 18, BRAND, 2)
    y += 68
    s.text(PAD, y + 4, "Is he interested in a loan?", 15, 700, INK)
    y += 16
    option_row(s, y, "check", GREEN, "Yes, interested", "Take KYC now, or book a KYC visit")
    option_row(s, y + 60, "calendar", BLUE, "Needs time to think", "Book a follow-up visit")
    option_row(s, y + 120, "x", RED, "No", "Capture why, then check out", "m08")
    gesture(s)
    return s


def m09_visit():
    s = phone("M9 Visit: Florence Nambi (returning client)", bg=BG, time="11:15")
    app_bar(s, "Visit · " + CLIENT["name"], back="m05", sub="Plan: Kiwatule follow-ups · her 3rd visit")
    visit_bar(s, "Visit in progress · checked in 11:14 · GPS ✓ 9 m")
    with s.g("client"):
        y = 122
        s.rect(PAD, y, MW - 2 * PAD, 64, fill=CARD, rx=12, stroke=LINE)
        avatar(s, PAD + 32, y + 32, 20, "FN", GREEN)
        s.text(PAD + 62, y + 28, "Nambi Tailoring & Fabrics", 14, 600, INK)
        s.text(PAD + 62, y + 47, "Kiwatule market route · your territory since 12 Aug", 11.5, 400, MUTED,
               maxw=MW - 2 * PAD - 76)
    with s.g("where she is"):
        y = 198
        s.rect(PAD, y, MW - 2 * PAD, 78, fill=CARD, rx=12, stroke=LINE)
        s.text(PAD + 14, y + 22, "WHERE SHE IS IN THE JOURNEY", 10.5, 700, MUTED, spacing=0.8)
        labels = ["Visited", "Interested", "KYC", "Validated", "Negotiate", "Applied"]
        n = len(labels)
        x0, x1 = PAD + 28, MW - PAD - 28
        cy = y + 44
        s.line(x0, cy, x1, cy, LINE, 2)
        s.line(x0, cy, x0 + (x1 - x0) / (n - 1), cy, BLUE, 2)
        for i, lab in enumerate(labels):
            cx = x0 + (x1 - x0) * i / (n - 1)
            if i <= 1:
                s.circle(cx, cy, 7, fill=BLUE)
            elif i == 2:
                s.circle(cx, cy, 8, fill=CARD, stroke=BRAND, sw=2.5)
            else:
                s.circle(cx, cy, 5, fill=LINE)
            s.text(cx, cy + 22, lab, 10.5, 700 if i in (1, 2) else 400, BRAND if i == 2 else (INK2 if i < 2 else FAINT),
                   anchor="middle")
    with s.g("why here"):
        y = 288
        s.rect(PAD, y, MW - 2 * PAD, 76, fill=tint(YELLOW, 0.2), rx=12)
        s.text(PAD + 14, y + 22, "WHY YOU'RE HERE (FROM THE PLAN)", 10.5, 700, YELLOW_D, spacing=0.8)
        s.text(PAD + 14, y + 43, "Collect her ID and sales book, take KYC", 13.5, 600, INK)
        s.text(PAD + 14, y + 62, "Last note 14 Sep: “Documents ready by month end.”", 11.5, 400, INK2,
               maxw=MW - 2 * PAD - 28)
    y = 386
    s.text(PAD, y, "What happened?", 15, 700, INK)
    with s.g("next step"):
        y += 14
        s.rect(PAD, y, MW - 2 * PAD, 70, fill=BRAND, rx=12)
        s.circle(PAD + 30, y + 35, 18, fill=YELLOW)
        s.icon("idcard", PAD + 20, y + 25, 20, BRAND_D, 2.2)
        s.text(PAD + 60, y + 30, "She's ready: take KYC now", 14.5, 700, "#FFFFFF")
        s.text(PAD + 60, y + 50, "Next stage · 3 short steps, about 15 min", 12, 400, "#C9C8EE")
        s.icon("chevright", MW - PAD - 30, y + 25, 20, YELLOW, 2.4)
        s.link(PAD, y, MW - 2 * PAD, 70, "m10")
    y += 80
    option_row(s, y, "calendar", BLUE, "Needs more time", "Book a follow-up visit and check out")
    option_row(s, y + 60, "x", RED, "No longer interested", "Capture why, then check out")
    option_row(s, y + 120, "userx", "#8A8DA6", "Client not available", "Still logged as a visit attempt")
    gesture(s)
    return s

def m08_not_interested():
    s = phone("M8 Not interested: capture why", bg=CARD, time="10:58")
    app_bar(s, "Not interested: why?", back="m07", sub="Joseph Kiggundu · first visit · 10:58")
    y = 104
    s.text(PAD, y, "Why not? Pick all that apply", 14.5, 700, INK)
    y = pills(s, PAD, y + 14, [("Has a loan elsewhere", True), ("Interest rate / cost", False),
                               ("Not eligible", False), ("Ask spouse / family", True), ("Not now", False),
                               ("Doesn't trust lenders", False), ("Needs a bigger amount", False), ("Other", False)])
    y += 26
    s.text(PAD, y, "Agent's note", 13, 600, INK2)
    with s.g("note box"):
        s.rect(PAD, y + 10, MW - 2 * PAD, 96, fill=CARD, rx=10, stroke="#CDD0DE")
        para(s, PAD + 14, y + 36, "SACCO loan ends in December. His wife co-owns the shop and must agree before any "
                                  "new loan.", MW - 2 * PAD - 60, 13.5, 400, INK, lh=20)
        s.circle(MW - PAD - 22, y + 84, 16, fill=tint(BRAND, 0.1))
        s.icon("mic", MW - PAD - 31, y + 75, 18, BRAND, 2)
    y += 126
    s.text(PAD, y, "Products that could suit later", 13, 600, INK2)
    y = pills(s, PAD, y + 12, [("MSE Business Loan", True), ("School Fees Loan", False),
                               ("Home Improvement", False)])
    y += 22
    with s.g("follow-up"):
        s.rect(PAD, y, MW - 2 * PAD, 64, fill="#F5F5FB", rx=12)
        s.icon("calendar", PAD + 14, y + 21, 22, BRAND, 2)
        s.text(PAD + 46, y + 28, "Follow up later", 14, 600, INK)
        s.text(PAD + 46, y + 47, "Mon 11 Jan 2027 · reminder on your phone", 12, 400, MUTED)
        toggle(s, MW - PAD - 50, y + 22, True)
    with s.g("reason note"):
        y += 80
        s.icon("info", PAD, y, 16, MUTED, 2)
        para(s, PAD + 24, y + 12, "Reasons feed the “why and why not” report for management.", MW - 2 * PAD - 30, 12,
             400, MUTED, lh=17)
    footer(s, "Check out", "m03", icon="check")
    return s


def m10_kyc_details():
    s = phone("M10 KYC 1: personal details", bg=CARD, time="11:16")
    app_bar(s, "KYC · " + CLIENT["name"], back="m09", sub="Step 1 of 3 · during the visit · client details", right="more")
    stepper(s, 92, 1)
    y = 128
    y += m_field(s, y, "Full name (as on National ID)", CLIENT["name"], icon="user") + 10
    y += m_field(s, y, "Phone", "0772 418 ···", icon="phone", ok="Registered to this name (MTN)") + 8
    with s.g("gender and age"):
        s.text(PAD, y + 14, "Gender", 13, 600, INK2)
        s.text(MW / 2 + 6, y + 14, "Date of birth", 13, 600, INK2)
        hw = (MW - 2 * PAD - 12) / 2
        for i, (lab, on) in enumerate([("Woman", True), ("Man", False)]):
            x = PAD + i * hw / 2
            s.rect(x, y + 22, hw / 2 - 3, 42, fill=BRAND if on else CARD, rx=8, stroke=None if on else "#CDD0DE")
            s.text(x + hw / 4 - 1.5, y + 48, lab, 13.5, 600, "#FFFFFF" if on else INK2, anchor="middle")
        s.rect(MW / 2 + 6, y + 22, hw, 42, fill=CARD, rx=8, stroke="#CDD0DE")
        s.text(MW / 2 + 18, y + 48, "12 Mar 1992 (34)", 13.5, 400, INK)
        y += 78
    hw = (MW - 2 * PAD - 12) / 2
    field(s, PAD, y, hw, "Marital status", "Married", dropdown=True, size=14)
    field(s, PAD + hw + 12, y, hw, "Dependants", "3", size=14, suffix="− +")
    y += 78
    y += m_field(s, y, "Occupation", "Self-employed · tailor (6 yrs)", dropdown=True) + 10
    y += m_field(s, y, "Education", "Secondary (S4)", dropdown=True, required=False) + 10
    y += m_field(s, y, "Home / business location", "Kiwatule, Nakawa · from GPS", icon="pin") + 8
    footer(s, "Next: ID & photos", "m11", icon="arrowright", secondary="Save", sec_target="m03")
    return s


def m11_kyc_id():
    s = phone("M11 KYC 2: NIRA ID and photos", bg=CARD, time="11:19")
    app_bar(s, "KYC · " + CLIENT["name"], back="m10", sub="Step 2 of 3 · ID & photos", right="more")
    stepper(s, 92, 2)
    y = 128
    s.text(PAD, y + 4, "National ID (NIRA)", 14.5, 700, INK)
    tw_ = (MW - 2 * PAD - 10) / 2
    doc_thumb(s, PAD, y + 16, tw_, 112, "id_front", "Front")
    doc_thumb(s, PAD + tw_ + 10, y + 16, tw_, 112, "id_back", "Back")
    y += 142
    with s.g("nin"):
        s.rect(PAD, y, MW - 2 * PAD, 70, fill=tint(GREEN, 0.07), rx=12, stroke=tint(GREEN, 0.35))
        s.icon("scan", PAD + 14, y + 12, 20, GREEN_D, 2)
        s.text(PAD + 44, y + 27, f"NIN read from the card: {CLIENT['nin']}", 12.5, 600, INK, maxw=MW - 2 * PAD - 56)
        s.icon("check", PAD + 14, y + 40, 18, GREEN, 3)
        s.text(PAD + 44, y + 53, "NIRA: name, date of birth and photo match", 12.5, 600, GREEN_D)
    y += 86
    s.text(PAD, y + 4, "Live selfie", 14.5, 700, INK)
    with s.g("selfie row"):
        doc_thumb(s, PAD, y + 16, 110, 112, "selfie", "Selfie")
        s.text(PAD + 126, y + 44, "Face match 96%", 15, 700, GREEN_D)
        s.text(PAD + 126, y + 66, "Liveness passed", 12.5, 400, INK2)
        s.text(PAD + 126, y + 86, "(blink and turn head)", 12.5, 400, MUTED)
    y += 142
    s.text(PAD, y + 4, "Other photos", 14.5, 700, INK)
    tw3 = (MW - 2 * PAD - 16) / 3
    for i, (k, lab) in enumerate([("shop", "Premises"), ("doc", "Sales book"), ("moto", "Collateral")]):
        doc_thumb(s, PAD + i * (tw3 + 8), y + 16, tw3, 96, k, lab)
    y += 124
    s.icon("pin", PAD, y - 2, 14, MUTED, 2)
    s.text(PAD + 20, y + 9, "Photos are GPS-stamped and never saved to the gallery", 11.5, 400, MUTED)
    footer(s, "Next: income", "m12", icon="arrowright", secondary="Back", sec_target="m10")
    return s


def m12_kyc_income():
    s = phone("M12 KYC 3: earnings and collateral", bg=CARD, time="11:22")
    app_bar(s, "KYC · " + CLIENT["name"], back="m11", sub="Step 3 of 3 · earnings & collateral", right="more")
    stepper(s, 92, 3)
    y = 128
    y += m_field(s, y, "Main source of income", "Business · tailoring shop", dropdown=True) + 10
    hw = (MW - 2 * PAD - 12) / 2
    field(s, PAD, y, hw, "Monthly income", "2,400,000", suffix="UGX", size=14, required=True)
    field(s, PAD + hw + 12, y, hw, "Monthly expenses", "1,150,000", suffix="UGX", size=14, required=True)
    y += 80
    s.text(PAD, y + 14, "Other loans now", 13, 600, INK2)
    y = pills(s, PAD, y + 24, [("None", True), ("Bank", False), ("SACCO", False), ("Mobile loan", False)]) + 18
    s.text(PAD, y + 4, "Collateral", 14.5, 700, INK)
    for nm, sub, val in [("Motorcycle · UBF 412K", "Photo ✓ · logbook ✓", "UGX 4.5M"),
                         ("Sewing machines (3)", "Photos ✓ · receipts ✓", "UGX 1.8M")]:
        y += 16
        with s.g(f"collateral {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 58, fill=CARD, rx=12, stroke=LINE)
            s.rect(PAD + 10, y + 9, 40, 40, fill=tint(BRAND, 0.1), rx=8)
            s.icon("briefcase", PAD + 20, y + 19, 20, BRAND, 2)
            s.text(PAD + 62, y + 25, nm, 13.5, 600, INK)
            s.text(PAD + 62, y + 43, sub, 12, 400, GREEN_D)
            s.text(MW - PAD - 14, y + 34, val, 13.5, 700, INK, anchor="end")
        y += 58
    y += 10
    s.text(PAD, y + 14, "+ Add collateral", 13.5, 600, BRAND)
    y += 34
    with s.g("consent"):
        s.rect(PAD, y, MW - 2 * PAD, 58, fill="#F5F5FB", rx=12)
        checkbox(s, PAD + 14, y + 12, True)
        s.text(PAD + 42, y + 25, "Client agreed to a CRB check", 13.5, 600, INK)
        s.text(PAD + 42, y + 43, "Signed on screen 11:23", 12, 400, MUTED)
    footer(s, "Validate KYC", "m13", icon="shield", secondary="Back", sec_target="m11")
    return s


def m13_validation():
    s = phone("M13 KYC validation", bg=BG, time="11:24")
    app_bar(s, "KYC validation", back="m12", sub=CLIENT["name"])
    with s.g("result"):
        y = 96
        s.rect(PAD, y, MW - 2 * PAD, 104, fill=CARD, rx=14, stroke=tint(GREEN, 0.5))
        ring(s, PAD + 52, y + 52, 34, 7, 1.0, GREEN)
        s.icon("check", PAD + 38, y + 38, 28, GREEN, 3)
        s.text(PAD + 102, y + 44, "KYC validated", 18, 700, INK)
        s.text(PAD + 102, y + 66, "6 of 6 checks passed", 13, 400, GREEN_D)
        s.text(PAD + 102, y + 85, "Checked online in 8 seconds", 12, 400, MUTED)
    y = 218
    s.rect(PAD, y, MW - 2 * PAD, 346, fill=CARD, rx=14, stroke=LINE)
    for title, sub in [("NIRA: ID is genuine and matches", "NIN, name, date of birth, photo"),
                       ("Phone is in her name", "MTN registration check"),
                       ("Not already a Letshego client", "Checked in the loan system"),
                       ("Location inside your territory", "Kiwatule · 0.3712, 32.6205"),
                       ("Affordable", "Can pay up to UGX 625,000 a month"),
                       ("CRB clear", "No active loans · consent signed")]:
        check_row(s, y + 14, title, sub)
        y += 55
    with s.g("offline note"):
        y = 580
        s.rect(PAD, y, MW - 2 * PAD, 58, fill=tint(AMBER, 0.12), rx=12)
        s.icon("wifioff", PAD + 14, y + 17, 22, AMBER_D, 2)
        para(s, PAD + 46, y + 25, "No network? Checks wait in the queue and run as soon as you're back online.",
             MW - 2 * PAD - 60, 12, 400, INK2, lh=17)
    footer(s, "Continue: loan options", "m14", icon="arrowright")
    return s


def m14_negotiation():
    s = phone("M14 Negotiation: pick a loan product", bg=CARD, time="11:30")
    app_bar(s, "Loan options", back="m13", sub="Negotiation · " + CLIENT["name"])
    y = 100
    s.text(PAD, y, "Suggested for Florence", 14.5, 700, INK)
    prods = [("MSE Business Loan", "Best fit: business owner, steady sales", True),
             ("School Fees Loan", "3 children in school", False)]
    y += 12
    for nm, why, on in prods:
        with s.g(f"product {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 60, fill=tint(BRAND, 0.06) if on else CARD, rx=12,
                   stroke=BRAND if on else LINE, sw=2 if on else 1)
            radio(s, PAD + 24, y + 30, on)
            s.text(PAD + 44, y + 26, nm, 14, 700, INK)
            s.text(PAD + 44, y + 45, why, 12, 400, MUTED)
            if on:
                chip(s, MW - PAD - 12 - tw("Best fit", 11, 600) - 20, y + 10, "Best fit", GREEN, h=20, size=11)
        y += 70
    with s.g("calculator"):
        y += 4
        s.text(PAD, y + 12, "Amount", 13, 600, INK2)
        s.text(MW - PAD, y + 12, ugx(CLIENT["amount"]), 16, 700, INK, anchor="end")
        s.rect(PAD, y + 26, MW - 2 * PAD, 10, fill=LINE2, rx=5)
        s.rect(PAD, y + 26, (MW - 2 * PAD) * 0.4, 10, fill=YELLOW, rx=5)
        s.circle(PAD + (MW - 2 * PAD) * 0.4, y + 31, 11, fill=CARD, stroke=YELLOW_D, sw=2)
        s.text(PAD, y + 54, "UGX 500K", 11, 400, MUTED)
        s.text(MW - PAD, y + 54, "UGX 15M", 11, 400, MUTED, anchor="end")
        y += 72
        s.text(PAD, y + 12, "Months to repay", 13, 600, INK2)
        bw = (MW - 2 * PAD - 3 * 8) / 4
        for i, m in enumerate([6, 12, 18, 24]):
            on = m == CLIENT["months"]
            s.rect(PAD + i * (bw + 8), y + 22, bw, 40, fill=YELLOW if on else CARD, rx=8,
                   stroke=None if on else "#CDD0DE")
            s.text(PAD + i * (bw + 8) + bw / 2, y + 47, str(m), 14, 700, BRAND_D if on else INK2, anchor="middle")
        y += 76
        inst = rnd_instalment(CLIENT["amount"], CLIENT["months"])
        s.rect(PAD, y, MW - 2 * PAD, 76, fill=BRAND, rx=14)
        s.text(PAD + 16, y + 26, "Monthly instalment (indicative)", 12.5, 400, "#C9C8EE")
        s.text(PAD + 16, y + 56, ugx(inst), 22, 700, "#FFFFFF")
        s.text(MW - PAD - 16, y + 56, "35% of free income ✓", 12, 600, YELLOW, anchor="end")
        y += 90
    s.text(PAD, y + 12, "Why this product (for the supervisor)", 13, 600, INK2)
    s.rect(PAD, y + 22, MW - 2 * PAD, 62, fill=CARD, rx=10, stroke="#CDD0DE")
    para(s, PAD + 12, y + 46, "Wants a 2nd industrial machine before January; uniform orders each term.",
         MW - 2 * PAD - 24, 13, 400, INK, lh=19)
    footer(s, "Client agrees: close", "m15", icon="arrowright", secondary="Back", sec_target="m13")
    return s


def m15_close():
    s = phone("M15 Close: submit the loan application", bg=CARD, time="11:41")
    app_bar(s, "Close the sale", back="m14", sub=f"{CLIENT['product']} · {ugx(CLIENT['amount'])}")
    y = 100
    s.text(PAD, y, "Does the client agree to apply?", 14.5, 700, INK)
    bw = (MW - 2 * PAD - 10) / 2
    s.rect(PAD, y + 14, bw, 44, fill=GREEN, rx=10)
    s.icon("check", PAD + bw / 2 - 30, y + 26, 20, "#FFFFFF", 2.8)
    s.text(PAD + bw / 2 + 4, y + 42, "Yes", 14.5, 700, "#FFFFFF", anchor="middle")
    s.rect(PAD + bw + 10, y + 14, bw, 44, fill=CARD, rx=10, stroke="#CDD0DE")
    s.text(PAD + bw + 10 + bw / 2, y + 42, "No, capture why", 13.5, 600, INK2, anchor="middle")
    y += 80
    s.text(PAD, y, "Required items", 14.5, 700, INK)
    s.text(MW - PAD, y, "7 of 7", 13, 700, GREEN_D, anchor="end")
    items = ["NIRA ID both sides", "Live selfie", "Proof of income", "Premises photo", "Collateral + logbook",
             "CRB consent", "Loan application ID"]
    y += 10
    for i, it in enumerate(items):
        ix = PAD + (i % 2) * ((MW - 2 * PAD) / 2)
        iy = y + 20 + (i // 2) * 26
        s.icon("check", ix, iy - 12, 15, GREEN, 3)
        s.text(ix + 22, iy, it, 12.5, 400, INK2)
    y += 20 + 4 * 26 + 6
    field(s, PAD, y, MW - 2 * PAD, "Loan application ID (from the loan system)", CLIENT["app_id"], h=46, icon="scan",
          ok="Found in the loan system · MSE · UGX 6,000,000", size=14.5, required=True)
    y += 114
    s.text(PAD, y, "Why is she taking the loan?", 13, 600, INK2)
    y = pills(s, PAD, y + 12, [("Business equipment", True), ("Stock", False), ("School fees", False),
                               ("Other", False)]) + 16
    with s.g("rule"):
        s.rect(PAD, y, MW - 2 * PAD, 52, fill=tint(GREEN, 0.08), rx=12)
        s.icon("info", PAD + 12, y + 15, 20, GREEN_D, 2)
        para(s, PAD + 42, y + 22, "Submitting with every item counts as a conversion, whatever the approval decision.",
             MW - 2 * PAD - 54, 12, 600, GREEN_D, lh=17)
    footer(s, "Submit application", "m16", icon="send", color=GREEN)
    return s


def m16_success():
    s = phone("M16 Conversion recorded", bg=CARD, time="11:42")
    with s.g("confetti"):
        for i, (x, y, k) in enumerate([(40, 120, 18), (300, 90, 14), (270, 200, 10), (70, 250, 12), (320, 300, 16),
                                       (30, 330, 9), (190, 70, 11)]):
            triangle(s, x, y, k, name=f"confetti {i + 1}")
    s.circle(MW / 2, 250, 62, fill=tint(GREEN, 0.14))
    s.circle(MW / 2, 250, 44, fill=GREEN)
    s.icon("check", MW / 2 - 24, 226, 48, "#FFFFFF", 3)
    s.text(MW / 2, 350, "Conversion recorded", 23, 700, INK, anchor="middle")
    s.text(MW / 2, 376, "Florence applied for an MSE Business Loan", 14, 400, INK2, anchor="middle")
    with s.g("summary"):
        y = 402
        s.rect(PAD, y, MW - 2 * PAD, 120, fill="#F5F5FB", rx=14)
        for i, (lab, val) in enumerate([("Application", CLIENT["app_id"]), ("Amount", ugx(CLIENT["amount"])),
                                        ("Sent to", "Moses Okello (supervisor)")]):
            s.text(PAD + 16, y + 32 + i * 34, lab, 13, 400, MUTED)
            s.text(MW - PAD - 16, y + 32 + i * 34, val, 13.5, 700, INK, anchor="end")
    with s.g("progress"):
        y = 540
        s.rect(PAD, y, MW - 2 * PAD, 70, fill=tint(YELLOW, 0.22), rx=14)
        s.text(PAD + 16, y + 28, "Q3: 19 of 22 conversions", 14.5, 700, INK)
        s.text(MW - PAD - 16, y + 28, "+1", 14.5, 700, GREEN_D, anchor="end")
        progress(s, PAD + 16, y + 44, MW - 2 * PAD - 32, 19 / 22, BRAND, h=8, bg="#FFFFFF")
    s.text(MW / 2, 640, "Checked out 11:52 · 38-minute visit · you'll be notified", 12.5, 400, MUTED, anchor="middle")
    button(s, PAD, MH - 140, "Next stop: Ivan Kasozi", "primary", icon="navigation", w=MW - 2 * PAD, h=48)
    s.link(PAD, MH - 140, MW - 2 * PAD, 48, "m04")
    button(s, PAD, MH - 82, "View Florence's record", "ghost", w=MW - 2 * PAD, h=44)
    s.link(PAD, MH - 82, MW - 2 * PAD, 44, "m18")
    gesture(s)
    return s


MY_CLIENTS = [
    (CLIENT["name"], "MSE Business Loan", "Applied", "Awaiting approval · 11:42"),
    ("Betty Nakimuli", "School Fees Loan", "KYC validated", "Offer a loan · validated today"),
    ("Ivan Kasozi", "MSE Business Loan", "Negotiation", "Visit today 12:30"),
    ("Sarah Namutebi", "MSE Business Loan", "KYC captured", "Validate · payslip pending"),
    ("Charles Ssempijja", "MSE Business Loan", "Interested", "Follow up Fri 2 Oct"),
    ("Joseph Kiggundu", "—", "Not interested", "Revisit Jan 2027"),
]


def m17_clients():
    s = phone("M17 My clients", bg=BG, time="11:44")
    app_bar(s, "My clients", sub="32 open · all stored with Letshego", right="userplus")
    s.link(MW - 60, 24, 60, 56, "m06")
    with s.g("filter chips"):
        x = PAD
        for lab, on in [("All 32", True), ("Interested 14", False), ("KYC 9", False), ("Negotiation 6", False)]:
            w = tw(lab, 12.5, 600) + 26
            s.rect(x, 94, w, 32, fill=BRAND if on else CARD, rx=16, stroke=None if on else "#CDD0DE")
            s.text(x + 13, 114.5, lab, 12.5, 600, "#FFFFFF" if on else INK2)
            x += w + 8
    y = 140
    for nm, prod, st, nxt in MY_CLIENTS:
        col = STATUS.get(st, BRAND)
        with s.g(f"client {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 84, fill=CARD, rx=12, stroke=LINE)
            s.rect(PAD, y + 12, 4, 60, fill=col, rx=2)
            s.text(PAD + 18, y + 26, nm, 14.5, 600, INK)
            chip(s, MW - PAD - 12 - tw(st, 11, 600) - 34, y + 12, st, col, h=22, size=11, dot=True)
            s.text(PAD + 18, y + 47, prod, 12, 400, MUTED)
            s.icon("clock", PAD + 18, y + 58, 14, INK2, 2)
            s.text(PAD + 38, y + 70, nxt, 12.5, 600, INK2)
        if nm == CLIENT["name"]:
            s.link(PAD, y, MW - 2 * PAD, 84, "m18")
        y += 92
    bottom_nav(s, "Clients")
    return s


def m18_client():
    s = phone("M18 Client record", bg=BG, time="11:45")
    app_bar(s, CLIENT["name"], back="m17", sub="Client " + CLIENT["id"] + " · owned by Letshego", right="more")
    with s.g("client header"):
        y = 92
        s.rect(PAD, y, MW - 2 * PAD, 150, fill=CARD, rx=14, stroke=LINE)
        avatar(s, PAD + 36, y + 36, 22, "FN", GREEN)
        s.text(PAD + 68, y + 32, "Nambi Tailoring & Fabrics", 14, 600, INK)
        s.text(PAD + 68, y + 51, "Kiwatule · 0772 418 ···", 12.5, 400, MUTED)
        x = PAD + 16
        x += chip(s, x, y + 68, "Applied", GREEN, h=24, size=11.5, dot=True) + 8
        chip(s, x, y + 68, "MSE Business Loan", PRODUCT["MSE Business Loan"], h=24, size=11.5)
        bw = (MW - 2 * PAD - 32 - 16) / 3
        for i, (ic, lab) in enumerate([("phone", "Call"), ("navigation", "Directions"), ("edit", "Note")]):
            bx = PAD + 16 + i * (bw + 8)
            s.rect(bx, y + 104, bw, 34, fill=tint(BRAND, 0.08), rx=8)
            s.icon(ic, bx + bw / 2 - tw(lab, 12.5, 600) / 2 - 12, y + 113, 16, BRAND, 2)
            s.text(bx + bw / 2 + 10, y + 126, lab, 12.5, 600, BRAND, anchor="middle")
    with s.g("tabs"):
        y = 256
        x = PAD
        for lab, on in [("Journey", True), ("Details", False), ("Documents 6", False), ("Visits 3", False)]:
            w = tw(lab, 13, 600) + 20
            s.text(x + 10, y + 18, lab, 13, 600, BRAND if on else MUTED)
            if on:
                s.rect(x + 4, y + 28, w - 8, 3, fill=BRAND, rx=1.5)
            x += w + 4
        s.line(0, y + 31, MW, y + 31, LINE)
    steps = [("Visited", "John Mugisha · 29 Jul", "Visited", True),
             ("Interested", "Moved to you 12 Aug when John left", "Interested", True),
             ("KYC captured", "Today 11:16 · 6 photos", "KYC captured", True),
             ("KYC validated", "Today 11:24 · 6 of 6 checks", "KYC validated", True),
             ("Negotiation", "UGX 6M · 18 months", "Negotiation", True),
             ("Applied: converted", "Today 11:42 · " + CLIENT["app_id"], "Applied", True),
             ("Supervisor decision", "Waiting for Moses Okello", None, False)]
    y = 318
    for i, (lab, sub, st, done) in enumerate(steps):
        col = STAGE[st] if st else "#C4C7D6"
        with s.g(f"step {lab}"):
            if i < len(steps) - 1:
                s.line(PAD + 16, y + 12, PAD + 16, y + 46, col if steps[i + 1][3] else LINE, 2,
                       dash=None if steps[i + 1][3] else "4 4")
            s.circle(PAD + 16, y, 11, fill=col if done else CARD, stroke=col, sw=2)
            if done:
                s.icon("check", PAD + 10, y - 6, 12, "#FFFFFF", 3.2)
            else:
                s.icon("clock", PAD + 9, y - 7, 14, MUTED, 2)
            s.text(PAD + 38, y - 1, lab, 13.5, 600, INK if done else MUTED)
            s.text(PAD + 38, y + 16, sub, 12, 400, MUTED, maxw=MW - 2 * PAD - 50)
        y += 48
    with s.g("next step"):
        y += 2
        s.rect(PAD, y, MW - 2 * PAD, 50, fill=tint(AMBER, 0.12), rx=12)
        s.icon("clock", PAD + 14, y + 14, 20, AMBER_D, 2)
        s.text(PAD + 44, y + 22, "Next: supervisor decision", 13, 600, INK)
        s.text(PAD + 44, y + 39, "You'll be notified · then plan the disbursement visit", 12, 400, MUTED)
    footer(s, "Start a visit with Florence", "m09", icon="pin")
    return s


def m05_start_visit():
    s = phone("M5 Start a visit: choose the client", bg=BG, time="11:12")
    app_bar(s, "Start a visit", back="m03", sub="Who are you visiting?")
    with s.g("search"):
        s.rect(PAD, 92, MW - 2 * PAD, 44, fill=CARD, rx=10, stroke="#CDD0DE")
        s.icon("search", PAD + 12, 104, 20, MUTED)
        s.text(PAD + 42, 119, "Search name, phone or NIN", 14, 400, FAINT)
    with s.g("new client"):
        y = 148
        s.rect(PAD, y, MW - 2 * PAD, 58, fill=tint(YELLOW, 0.2), rx=12, stroke=YELLOW_D, sw=1.2, dash="5 4")
        s.circle(PAD + 30, y + 29, 16, fill=YELLOW)
        s.icon("userplus", PAD + 20, y + 19, 20, BRAND_D, 2.2)
        s.text(PAD + 56, y + 25, "New client (first visit)", 14.5, 700, INK)
        s.text(PAD + 56, y + 43, "Not in Letshego's records yet", 12, 400, YELLOW_D)
        s.icon("chevright", MW - PAD - 30, y + 19, 20, YELLOW_D)
        s.link(PAD, y, MW - 2 * PAD, 58, "m06")
    y = 234
    s.text(PAD, y, "DUE TODAY IN YOUR PLANS", 11, 700, MUTED, spacing=0.8)
    s.text(MW - PAD, y, "2 left", 12, 600, BRAND, anchor="end")
    rows = [(CLIENT["name"], "Interested · ready to apply", "0.6 km", BLUE, True),
            ("Ivan Kasozi", "Negotiation · 12:30", "1.4 km", AMBER, False)]
    y += 12
    for nm, sub, dist, col, nxt in rows:
        with s.g(f"planned {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 60, fill=CARD, rx=12, stroke=BRAND if nxt else LINE, sw=2 if nxt else 1)
            s.rect(PAD, y + 12, 4, 36, fill=col, rx=2)
            s.text(PAD + 18, y + 25, nm, 14, 600, INK)
            s.text(PAD + 18, y + 44, sub, 12, 400, MUTED)
            if nxt:
                button(s, MW - PAD - 12, y + 14, "Check in", "primary", h=32, size=12.5, anchor="end")
            else:
                s.text(MW - PAD - 14, y + 35, dist, 12, 600, INK2, anchor="end")
        if nxt:
            s.link(PAD, y, MW - 2 * PAD, 60, "m09")
        y += 68
    y += 14
    s.text(PAD, y, "NEAR YOU, NOT DUE TODAY", 11, 700, MUTED, spacing=0.8)
    y += 12
    for nm, sub, dist in [("Aisha Nalubega", "Interested · due Thu in your plan", "0.7 km"),
                          ("Charles Ssempijja", "Interested · follow-up due Fri", "0.9 km"),
                          ("Sarah Namutebi", "KYC captured · payslip pending", "1.1 km")]:
        with s.g(f"nearby {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 56, fill=CARD, rx=12, stroke=LINE)
            s.text(PAD + 16, y + 23, nm, 14, 600, INK)
            s.text(PAD + 16, y + 41, sub, 12, 400, MUTED)
            s.text(MW - PAD - 14, y + 33, dist, 12, 600, INK2, anchor="end")
        y += 62
    with s.g("off-plan note"):
        s.icon("info", PAD, y + 4, 16, MUTED, 2)
        para(s, PAD + 24, y + 16, "Visits outside your plans are fine; they show as off-plan on the dashboard.",
             MW - 2 * PAD - 30, 12, 400, MUTED, lh=17)
    bottom_nav(s, "Visit")
    return s


def m06_new_client():
    s = phone("M6 New client: register", bg=CARD, time="10:52")
    app_bar(s, "New client", back="m05", sub="Register first · KYC comes later, if interested")
    with s.g("gps"):
        y = 92
        s.rect(PAD, y, MW - 2 * PAD, 36, fill=tint(GREEN, 0.08), rx=10)
        s.icon("pin", PAD + 12, y + 9, 18, GREEN_D, 2)
        s.text(PAD + 38, y + 23, "From GPS: Ntinda · Kiwatule › Ntinda stage route", 12.5, 600, GREEN_D)
    y = 138
    y += m_field(s, y, "Full name", "Joseph Kiggundu", icon="user", h=42) + 6
    y += m_field(s, y, "Phone", "0701 552 ···", icon="phone", h=42, ok="No existing Letshego client with this number") + 2
    s.text(PAD, y + 14, "Gender and age", 13, 600, INK2)
    y = pills(s, PAD, y + 22, [("Man", True), ("Woman", False), ("26–35", False), ("36–50", True), ("50+", False)],
              h=30) + 8
    s.text(PAD, y + 14, "Type of work", 13, 600, INK2)
    y = pills(s, PAD, y + 22, [("Business owner", True), ("Civil servant", False), ("Salaried", False),
                               ("Farmer", False)], h=30) + 6
    y += m_field(s, y, "Business or employer", "Kiggundu Hardware, Ntinda", icon="store", h=42) + 4
    s.text(PAD, y + 14, "How you met", 13, 600, INK2)
    pills(s, PAD, y + 22, [("Door to door", True), ("Referral", False), ("Walk-in", False)], h=30)
    footer(s, "Save & start visit", "m07", icon="pin", secondary="Save only", sec_target="m17")
    return s

def m19_me():
    s = phone("M19 Me: my performance", bg=BG, time="12:02")
    with s.g("header"):
        s.circle(PAD + 32, 88, 30, fill=YELLOW)
        s.text(PAD + 32, 97, "SN", 20, 700, BRAND_D, anchor="middle")
        s.text(PAD + 76, 82, "Sarah Namuli", 19, 700, INK)
        s.text(PAD + 76, 104, "Field Sales Agent · LU-0877", 12.5, 400, MUTED)
        s.text(PAD + 76, 124, "Supervisor: Moses Okello", 12.5, 400, MUTED)
    with s.g("theme switch"):
        s.circle(MW - PAD - 20, 60, 20, fill=CARD, shadow=True)
        s.icon("moon", MW - PAD - 30, 50, 20, INK, 2)
        s.text(MW - PAD - 20, 96, "Theme", 10.5, 600, MUTED, anchor="middle")
    s.link(MW - PAD - 44, 36, 48, 68, "!theme")
    with s.g("quarter"):
        y = 140
        s.rect(PAD, y, MW - 2 * PAD, 116, fill=CARD, rx=20, stroke=LINE)
        s.text(PAD + 16, y + 28, "Q3 2026", 14, 700, INK)
        chip(s, MW - PAD - 16 - tw("Rank 3 of 62", 11, 600) - 34, y + 12, "Rank 3 of 62", GREEN, h=22, size=11,
             icon="trophy")
        cw = (MW - 2 * PAD - 32) / 3
        for i, (v, lab) in enumerate([("19/22", "Conversions"), ("214", "Visits"), ("82%", "Plan kept")]):
            x = PAD + 16 + i * cw
            s.text(x, y + 72, v, 21, 700, INK)
            s.text(x, y + 94, lab, 12, 400, MUTED)
    y = 282
    s.text(PAD, y, "This week", 15, 700, INK)
    s.text(MW - PAD, y, "W13 · 28 Sep – 2 Oct", 12, 400, MUTED, anchor="end")
    y += 14
    s.rect(PAD, y, MW - 2 * PAD, 176, fill=CARD, rx=14, stroke=LINE)
    s.text(PAD + 16, y + 30, "Journey plan visits made", 13.5, 400, INK2)
    s.text(MW - PAD - 16, y + 30, "15 of 18", 13.5, 700, INK, anchor="end")
    progress(s, PAD + 16, y + 39, MW - 2 * PAD - 32, 15 / 18, BRAND, h=5)
    for i, (lab, v) in enumerate([("Off-plan visits (new clients, walk-ins)", "2"), ("KYCs completed", "5"),
                                  ("Conversions", "2")]):
        yy = y + 76 + i * 34
        s.text(PAD + 16, yy, lab, 13.5, 400, INK2)
        s.text(MW - PAD - 16, yy, v, 13.5, 700, INK, anchor="end")
    y += 194
    rows = [("refresh", "Sync", "All synced 12:01 · nothing waiting", GREEN),
            ("map", "Offline maps", "Kampala East downloaded", BRAND),
            ("layers", "My territory", "Ntinda · Kiwatule · 6 routes · 212 clients", BRAND)]
    for ic, t, sub, col in rows:
        with s.g(f"row {t}"):
            s.rect(PAD, y, MW - 2 * PAD, 56, fill=CARD, rx=12, stroke=LINE)
            s.icon(ic, PAD + 14, y + 17, 22, col, 2)
            s.text(PAD + 48, y + 25, t, 14, 600, INK)
            s.text(PAD + 48, y + 43, sub, 12, 400, MUTED)
            s.icon("chevright", MW - PAD - 30, y + 18, 20, FAINT)
        y += 62
    with s.g("sign out"):
        s.text(MW / 2, y + 14, "Sign out", 14, 700, RED, anchor="middle")
        s.link(MW / 2 - 60, y - 6, 120, 30, "m02")
    bottom_nav(s, "Me")
    return s


SCREENS = [m01_splash, m02_sign_in, m03_home, m04_plans, m04b_plan, m04c_new_plan,
           m05_start_visit, m06_new_client, m07_first_visit,
           m08_not_interested, m09_visit, m10_kyc_details, m11_kyc_id, m12_kyc_income, m13_validation,
           m14_negotiation, m15_close, m16_success, m17_clients, m18_client, m19_me]
