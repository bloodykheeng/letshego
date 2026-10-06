"""Field app (Android, Flutter), 360 x 800 screens, for two roles (each user has one).

Sales agent (Sarah Namuli): prospects on the routes Moses gives her (name, phone, location) and turns the ones who
want a loan into leads (NIN, amount, location). Calls happen outside the app; the app records the result.
Relationship officer (Joel Byaruhanga): visits the leads on his lead journey plan and completes KYC, which makes the lead a
client. The walkthrough follows Florence Nambi: prospected by Sarah on 22 Sep, a lead on 23 Sep, KYC on 30 Sep.
"""
from __future__ import annotations

from charts import StreetMap, map_pin, ring
from data import CALLEE, CLIENT, SARAH, clients, rnd_instalment, ugx
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


def app_bar(s: SVG, title, back=None, sub=None, right=None, dark=False, history=False):
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
        s.link(0, 24, 56, 56, ("!back:" + back) if history else back)


def bottom_nav(s: SVG, active="Home", role="agent"):
    items = NAV_ITEMS[role]
    bx, by, bw, bh = 12, MH - 84, MW - 24, 64
    w = bw / len(items)
    for i, (_, _, tgt) in enumerate(items):
        s.link(bx + i * w, by, w, bh, tgt)
    with s.g("bottom navigation"):
        s.rect(bx, by, bw, bh, fill=CARD, rx=24, shadow=True, name="nav bg")
        for i, (lab, ic, _) in enumerate(items):
            cx = bx + i * w + w / 2
            on = lab == active
            with s.g(f"tab {lab}"):
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
    s = phone("M2 Sign in", bg=BG, time="08:02")
    with s.g("brand"):
        s.rect(MW / 2 - 26, 64, 52, 52, fill=BRAND, rx=16)
        triangle(s, MW / 2 - 14, 74, 28)
        s.text(MW / 2, 140, "Letshego Field Sales", 13, 600, MUTED, anchor="middle")
    with s.g("who"):
        s.circle(MW / 2, 196, 30, fill=YELLOW)
        s.text(MW / 2, 204, "SN", 20, 700, BRAND_D, anchor="middle")
        s.text(MW / 2, 254, "Welcome back, Sarah", 20, 700, INK, anchor="middle")
        s.text(MW / 2, 276, "Sales Agent · LU-0877 · Not you?", 12.5, 400, MUTED, anchor="middle")
    s.text(MW / 2, 322, "Enter your 6-digit PIN", 13.5, 600, INK2, anchor="middle")
    with s.g("pin dots"):
        for i in range(6):
            cx = MW / 2 - 70 + i * 28
            if i < 4:
                s.circle(cx, 348, 7, fill=BRAND)
            else:
                s.circle(cx, 348, 7, fill=CARD, stroke="#C4C7D6", sw=2)
    with s.g("keypad"):
        keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "fp", "0", "del"]
        kw, kh, gap = 84, 54, 14
        x0 = (MW - 3 * kw - 2 * gap) / 2
        for i, k in enumerate(keys):
            x = x0 + (i % 3) * (kw + gap)
            y = 374 + (i // 3) * (kh + 8)
            if k == "fp":
                s.icon("fingerprint", x + kw / 2 - 15, y + kh / 2 - 15, 30, BRAND, 1.9)
            elif k == "del":
                s.icon("arrowleft", x + kw / 2 - 12, y + kh / 2 - 12, 24, INK2, 2)
            else:
                s.rect(x, y, kw, kh, fill=CARD, rx=18, stroke=LINE)
                s.text(x + kw / 2, y + kh / 2 + 9, k, 24, 400, INK, anchor="middle")
        s.link(x0, 374, 3 * kw + 2 * gap, 4 * (kh + 8), "m03")
    with s.g("demo role switch"):
        y = 632
        s.text(MW / 2, y, "DEMO · SIGN IN AS", 10.5, 700, FAINT, anchor="middle", spacing=0.8)
        bw = (MW - 2 * PAD - 10) / 2
        for i, (ini, nm, role, tgt, col) in enumerate([("SN", "Sarah Namuli", "Sales Agent", "m03", BRAND),
                                                       ("JB", "Joel Byaruhanga", "Relationship Officer", "m20",
                                                        TEAL)]):
            x = PAD + i * (bw + 10)
            s.rect(x, y + 12, bw, 50, fill=CARD, rx=14, stroke=LINE)
            avatar(s, x + 24, y + 37, 15, ini, col)
            s.text(x + 46, y + 33, nm, 12.5, 700, INK, maxw=bw - 52)
            s.text(x + 46, y + 50, role, 11, 400, MUTED, maxw=bw - 52)
            s.link(x, y + 12, bw, 50, tgt)
    with s.g("offline note"):
        y = MH - 40
        s.icon("shield", MW / 2 - 118, y - 13, 16, GREEN, 2)
        s.text(MW / 2 - 96, y, "Phone registered to you · works offline", 12, 400, MUTED)
    gesture(s)
    return s


def m03_home():
    s = phone("M3 Home (sales agent)", bg=BG)
    home_top(s, "SN", "Sarah Namuli")
    hero_card(s, 108, "TODAY'S TARGET", "32", "/50", "prospects · 18 to go", 32 / 50,
              "64% of today's target", "2.6 h prospecting",
              [(52, "Mon"), (47, "Tue"), (32, "Wed")], "Prospects / day", "target 50 a day")
    s.text(PAD, 300, "This week", 15, 700, INK)
    s.text(MW - PAD, 300, "prospects · leads · KYC", 12, 400, MUTED, anchor="end")
    stat_cards(s, 312, [("Prospects", "131", "32 today", MUTED, STAGE["Prospect"]),
                        ("Leads", "14", "3 today", GREEN_D, STAGE["Lead"]),
                        ("KYC", "3", "completed", MUTED, STAGE["KYC completed"])])
    stat_links(s, 312, ["m06", "m17", "m17"])
    with s.g("route today"):
        y = 412
        s.rect(PAD, y, MW - 2 * PAD, 112, fill=CARD, rx=20, stroke=LINE)
        s.rect(PAD + 14, y + 14, 36, 36, fill=tint(BRAND, 0.1), rx=11)
        s.icon("map", PAD + 22, y + 22, 20, BRAND, 2)
        s.text(PAD + 62, y + 30, "Kiwatule market route", 14, 700, INK)
        s.text(PAD + 62, y + 48, "Today · inside your territory ✓", 12, 400, GREEN_D)
        s.link(PAD, y, MW - 2 * PAD, 60, "m04b")
        s.icon("chevright", MW - PAD - 30, y + 22, 20, FAINT)
        bw = (MW - 2 * PAD - 38) / 2
        button(s, PAD + 14, y + 64, "Add prospect", "primary", icon="plus", w=bw, h=36, size=13)
        s.link(PAD + 14, y + 64, bw, 36, "m05")
        button(s, PAD + 24 + bw, y + 64, "Prospect map", "soft", icon="map", w=bw, h=36, size=13)
        s.link(PAD + 24 + bw, y + 64, bw, 36, "m04b")
    with s.g("waiting prospects"):
        s.text(PAD, 554, "Prospects, not yet leads", 15, 700, INK)
        s.text(MW - PAD, 554, "All 6", 12.5, 600, BRAND, anchor="end")
        s.link(MW - PAD - 60, 538, 60, 24, "m06")
        y = 566
        s.rect(PAD, y, MW - 2 * PAD, 64, fill=CARD, rx=18, stroke=LINE)
        avatar(s, PAD + 34, y + 32, 19, CALLEE["initials"], VIOLET)
        s.text(PAD + 62, y + 28, CALLEE["name"], 14, 700, INK)
        s.text(PAD + 62, y + 47, "Prospect since Mon · Kiwatule market", 12, 400, MUTED)
        s.icon("chevright", MW - PAD - 30, y + 22, 20, FAINT)
        s.link(PAD, y, MW - 2 * PAD, 64, "m07")
    with s.g("plan shortcut"):
        y = 642
        s.rect(PAD, y, MW - 2 * PAD, 50, fill=CARD, rx=16, stroke=LINE)
        s.rect(PAD + 10, y + 9, 32, 32, fill=tint(YELLOW, 0.3), rx=10)
        s.icon("route", PAD + 17, y + 16, 18, YELLOW_D, 2.2)
        s.text(PAD + 54, y + 22, "Route journey plans", 13, 700, INK)
        s.text(PAD + 54, y + 39, "This week: 4 routes · 230 prospects · by Moses", 11.5, 400, MUTED)
        s.icon("chevright", MW - PAD - 30, y + 15, 20, FAINT)
        s.link(PAD, y, MW - 2 * PAD, 50, "m04")
    bottom_nav(s, "Home")
    return s


def m08_not_interested():
    s = phone("M8 No loan: capture why", bg=CARD, time="14:31")
    app_bar(s, "No loan: why?", back="m07", sub="Aisha Nalubega · prospect")
    y = 104
    s.text(PAD, y, "Why not? Pick all that apply", 14.5, 700, INK)
    y = pills(s, PAD, y + 14, [("Has a loan elsewhere", True), ("Interest rate / cost", False),
                               ("Not eligible", False), ("Ask spouse / family", False), ("Not now", False),
                               ("Other", False)])
    y += 26
    s.text(PAD, y, "Note (optional)", 13, 600, INK2)
    with s.g("note box"):
        s.rect(PAD, y + 10, MW - 2 * PAD, 72, fill=CARD, rx=10, stroke="#CDD0DE")
        para(s, PAD + 14, y + 36, "Has a SACCO loan until December.", MW - 2 * PAD - 60, 13.5, 400, INK, lh=20)
    y += 100
    with s.g("reason note"):
        s.icon("info", PAD, y, 16, MUTED, 2)
        para(s, PAD + 24, y + 12, "Reasons feed the “why and why not” report for management.", MW - 2 * PAD - 30, 12,
             400, MUTED, lh=17)
    footer(s, "Save", "m06", icon="check")
    return s


def m10_kyc_details():
    s = phone("M10 KYC 1: personal details", bg=CARD, time="11:16")
    app_bar(s, "KYC · " + CLIENT["name"], back="m09b", sub="KYC 1 of 3 · client details", right="more")
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
    footer(s, "Next: ID & photos", "m11", icon="arrowright", secondary="Save", sec_target="m09b")
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
    s = phone("M13 KYC checks", bg=BG, time="11:24")
    app_bar(s, "KYC checks", back="m12", sub=CLIENT["name"])
    with s.g("result"):
        y = 96
        s.rect(PAD, y, MW - 2 * PAD, 104, fill=CARD, rx=14, stroke=tint(GREEN, 0.5))
        ring(s, PAD + 52, y + 52, 34, 7, 1.0, GREEN)
        s.icon("check", PAD + 38, y + 38, 28, GREEN, 3)
        s.text(PAD + 102, y + 44, "KYC completed", 18, 700, INK)
        s.text(PAD + 102, y + 66, "Ready for the loan application", 13, 600, GREEN_D)
        s.text(PAD + 102, y + 85, "6 of 6 checks · online in 8 s", 12, 400, MUTED)
    y = 218
    s.rect(PAD, y, MW - 2 * PAD, 346, fill=CARD, rx=14, stroke=LINE)
    for title, sub in [("NIRA: ID is genuine and matches", "NIN, name, date of birth, photo"),
                       ("Phone is in her name", "MTN registration check"),
                       ("Not already a Letshego client", "Checked in the loan system"),
                       ("Location inside the territory", "Kiwatule · 0.3712, 32.6205"),
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
    footer(s, "Continue to loan", "m09c", icon="arrowright", secondary="Done", sec_target="m09f")
    return s


def m14_negotiation():
    s = phone("M14 Loan calculator", bg=CARD, time="11:30")
    app_bar(s, "Loan application", back="m09c", sub=CLIENT["name"])
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
    s.text(PAD, y + 12, "Why this product (for the branch manager)", 13, 600, INK2)
    s.rect(PAD, y + 22, MW - 2 * PAD, 62, fill=CARD, rx=10, stroke="#CDD0DE")
    para(s, PAD + 12, y + 46, "Wants a 2nd industrial machine before January; uniform orders each term.",
         MW - 2 * PAD - 24, 13, 400, INK, lh=19)
    footer(s, "Next: submit", "m15", icon="arrowright", secondary="Back", sec_target="m09c")
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
        para(s, PAD + 42, y + 22, "She becomes a client when the loan is disbursed, after Moses approves it.",
             MW - 2 * PAD - 54, 12, 600, GREEN_D, lh=17)
    footer(s, "Submit application", "m16", icon="send", color=GREEN)
    return s


def m16_success():
    s = phone("M16 Application submitted", bg=CARD, time="11:42")
    with s.g("confetti"):
        for i, (x, y, k) in enumerate([(40, 120, 18), (300, 90, 14), (270, 200, 10), (70, 250, 12), (320, 300, 16),
                                       (30, 330, 9), (190, 70, 11)]):
            triangle(s, x, y, k, name=f"confetti {i + 1}")
    s.circle(MW / 2, 250, 62, fill=tint(GREEN, 0.14))
    s.circle(MW / 2, 250, 44, fill=GREEN)
    s.icon("check", MW / 2 - 24, 226, 48, "#FFFFFF", 3)
    s.text(MW / 2, 350, "Application submitted", 23, 700, INK, anchor="middle")
    s.text(MW / 2, 376, "Florence applied for an MSE Business Loan", 14, 400, INK2, anchor="middle")
    with s.g("summary"):
        y = 402
        s.rect(PAD, y, MW - 2 * PAD, 120, fill="#F5F5FB", rx=14)
        for i, (lab, val) in enumerate([("Application", CLIENT["app_id"]), ("Amount", ugx(CLIENT["amount"])),
                                        ("Sent to", "Moses Okello (branch manager)")]):
            s.text(PAD + 16, y + 32 + i * 34, lab, 13, 400, MUTED)
            s.text(MW - PAD - 16, y + 32 + i * 34, val, 13.5, 700, INK, anchor="end")
    with s.g("progress"):
        y = 540
        s.rect(PAD, y, MW - 2 * PAD, 70, fill=tint(YELLOW, 0.22), rx=14)
        s.text(PAD + 16, y + 28, "Q3: 62 of 70 KYC completed", 14.5, 700, INK)
        s.text(MW - PAD - 16, y + 28, "+1", 13, 700, GREEN_D, anchor="end")
        progress(s, PAD + 16, y + 44, MW - 2 * PAD - 32, 62 / 70, BRAND, h=8, bg="#FFFFFF")
    s.text(MW / 2, 640, "You and Sarah are told when the loan is disbursed", 12.5, 400, MUTED, anchor="middle")
    button(s, PAD, MH - 140, "Close", "primary", icon="x", w=MW - 2 * PAD, h=48)
    s.link(PAD, MH - 140, MW - 2 * PAD, 48, "m09e")
    gesture(s)
    return s


MY_CLIENTS = [
    (CLIENT["name"], "UGX 6M · from Sarah", "KYC completed", "11:24 · loan sent for approval"),
    ("Betty Nakimuli", "UGX 2M · from Sarah", "Client", "Loan disbursed today 10:50"),
    ("Ivan Kasozi", "UGX 3M · from Sarah", "Lead", "Visit today 12:30"),
    ("Kenneth Lubega", "UGX 4M · from Peter", "Follow-up", "Employer letter pending"),
    ("Charles Ssempijja", "UGX 3M · from Peter", "Lead", "Visit Thu 1 Oct"),
    ("Doreen Kyomuhendo", "UGX 1.5M · from Ruth", "Not interested", "At the visit: interest rate"),
]


def m19_me():
    s = phone("M19 Me (sales agent)", bg=BG, time="14:40")
    me_header(s, "SN", "Sarah Namuli", YELLOW, "Staff ID LU-0877", [("Sales Agent", BRAND)])
    nm, ini, br, terr, p, l, c, t, wk, hrs, last, st = SARAH
    with s.g("quarter"):
        y = 146
        s.rect(PAD, y, MW - 2 * PAD, 128, fill=CARD, rx=20, stroke=LINE)
        s.text(PAD + 16, y + 26, "Q3 2026 performance", 14, 700, INK)
        chip(s, MW - PAD - 16 - tw("Rank 3 of 62", 11, 600) - 34, y + 10, "Rank 3 of 62", GREEN, h=22, size=11,
             icon="trophy")
        cw = (MW - 2 * PAD - 32) / 3
        for i, (v, lab, col) in enumerate([(f"{p:,}", "Prospects", STAGE["Prospect"]),
                                           (f"{l}", "Leads", STAGE["Lead"]),
                                           (f"{c}", "KYC completed", STAGE["KYC completed"])]):
            x = PAD + 16 + i * cw
            s.rect(x, y + 44, 4, 38, fill=col, rx=2)
            s.text(x + 12, y + 68, v, 21, 700, INK)
            s.text(x + 12, y + 84, lab, 11.5, 400, MUTED)
        s.text(PAD + 16, y + 112, f"{clients(c)} clients · {clients(c) / p:.1%} of prospects · team {786 / 48260:.1%}", 12, 600,
               GREEN_D)
    y = 296
    s.text(PAD, y, "This week", 15, 700, INK)
    s.text(MW - PAD, y, "W40 · 28 Sep – 2 Oct", 12, 400, MUTED, anchor="end")
    y += 12
    s.rect(PAD, y, MW - 2 * PAD, 120, fill=CARD, rx=16, stroke=LINE)
    s.text(PAD + 16, y + 26, "Prospects vs route target", 13, 400, INK2)
    s.text(MW - PAD - 16, y + 26, "131 of 230", 13, 700, INK, anchor="end")
    progress(s, PAD + 16, y + 35, MW - 2 * PAD - 32, 131 / 230, STAGE["Prospect"], h=5)
    for i, (lab, v) in enumerate([("Leads generated", "15"), ("Time prospecting", "12.9 h")]):
        yy = y + 70 + i * 26
        s.text(PAD + 16, yy, lab, 13, 400, INK2)
        s.text(MW - PAD - 16, yy, v, 13, 700, INK, anchor="end")
    y += 134
    y += where_card(s, y, [("store", "Branch", "Kampala East", "Manager: Moses Okello"),
                           ("layers", "Territory", "Ntinda · Kiwatule", "geofenced · 212 clients"),
                           ("route", "Routes", "6 routes", "Kiwatule market +5")], target="m04") + 10
    sign_out_row(s, y)
    bottom_nav(s, "Me")
    return s


# ------------------------------------------------------------------ client record: the hub for everything
HUB_TABS = ["Overview", "KYC", "Loan", "History"]
HUB_KEYS = {True: ["m09", "m09b", "m09c", "m09d"], False: ["m18", "m18b", "m18c", "m18d"]}


def journey_card(s, y, reached, now=None):
    """reached: index of the furthest step done (0 Prospect … 4 Submitted); now: the step in progress."""
    s.rect(PAD, y, MW - 2 * PAD, 72, fill=CARD, rx=16, stroke=LINE)
    s.text(PAD + 14, y + 22, "CLIENT JOURNEY", 10.5, 700, MUTED, spacing=0.8)
    labels = ["Prospect", "Lead", "Visit", "KYC", "Submitted"]
    n = len(labels)
    now = reached + 1 if now is None else now
    done_col = GREEN if reached >= 3 else BLUE
    x0, x1 = PAD + 28, MW - PAD - 28
    cy = y + 42
    s.line(x0, cy, x1, cy, LINE, 2)
    s.line(x0, cy, x0 + (x1 - x0) * reached / (n - 1), cy, done_col, 2)
    for i, lab in enumerate(labels):
        cx = x0 + (x1 - x0) * i / (n - 1)
        if i <= reached:
            s.circle(cx, cy, 6.5, fill=done_col)
        elif i == now:
            s.circle(cx, cy, 7.5, fill=CARD, stroke=BRAND, sw=2.5)
        else:
            s.circle(cx, cy, 5, fill=LINE)
        cur = i == now or (reached == n - 1 and i == n - 1)
        s.text(cx, cy + 20, lab, 10, 700 if cur else 400, BRAND if cur else (INK2 if i <= reached else FAINT),
               anchor="middle")


def info_row(s, y, icon, color, title, sub, target=None, h=58, fill=CARD, chev=True):
    with s.g(f"row {title}"):
        s.rect(PAD, y, MW - 2 * PAD, h, fill=fill, rx=14, stroke=LINE if fill == CARD else None)
        s.circle(PAD + 28, y + h / 2, 16, fill=tint(color, 0.14))
        s.icon(icon, PAD + 19, y + h / 2 - 9, 18, color, 2.2)
        s.text(PAD + 54, y + h / 2 - 3, title, 13.5, 600, INK, maxw=MW - 2 * PAD - 90)
        s.text(PAD + 54, y + h / 2 + 15, sub, 11.5, 400, MUTED, maxw=MW - 2 * PAD - 90)
        if chev:
            s.icon("chevright", MW - PAD - 28, y + h / 2 - 10, 20, FAINT)
    if target:
        s.link(PAD, y, MW - 2 * PAD, h, target)


def client_hub(title, tab, during, applied=None, kyc_done=None):
    keys = HUB_KEYS[during]
    applied = (not during) if applied is None else applied
    kyc_done = (applied or not during) if kyc_done is None else kyc_done
    s = phone(title, bg=BG, time=("11:43" if applied else ("11:25" if kyc_done else "11:15")) if during else "11:53")
    app_bar(s, CLIENT["name"], back="m21b" if during else "m23", sub="Lead from Sarah · Kiwatule market")
    s.icon("navigation", MW - PAD - 24, 40, 22, INK, 2)
    with s.g("client header"):
        y = 92
        s.rect(PAD, y, MW - 2 * PAD, 84, fill=CARD, rx=18, stroke=LINE)
        avatar(s, PAD + 34, y + 42, 22, "FN", GREEN if kyc_done else BLUE)
        s.text(PAD + 66, y + 32, "Nambi Tailoring & Fabrics", 14, 700, INK)
        stage = ("KYC completed", GREEN) if kyc_done else ("Lead", BLUE)
        x = PAD + 66
        x += chip(s, x, y + 44, stage[0], stage[1], h=22, size=11, dot=True) + 6
        chip(s, x, y + 44, "UGX 6M", BRAND, h=22, size=11)
    with s.g("visit bar"):
        y = 186
        if during:
            s.rect(PAD, y, MW - 2 * PAD, 44, fill=tint(GREEN, 0.1), rx=14)
            s.circle(PAD + 18, y + 22, 5, fill=GREEN)
            s.text(PAD + 32, y + 20, "Visit in progress", 13, 700, GREEN_D)
            s.text(PAD + 32, y + 36, "Checked in 11:14 · GPS ✓ 9 m", 11, 400, GREEN_D)
            s.rect(MW - PAD - 104, y + 8, 92, 28, fill=CARD, rx=10, stroke=tint(GREEN, 0.6), shadow=False)
            s.icon("logout", MW - PAD - 94, y + 14, 15, GREEN_D, 2.2)
            s.text(MW - PAD - 74, y + 26.5, "Check out", 12, 700, GREEN_D)
            s.link(MW - PAD - 104, y + 8, 92, 28, "m16b")
        else:
            s.rect(PAD, y, MW - 2 * PAD, 44, fill="#EEEFF5", rx=14)
            s.icon("history", PAD + 12, y + 12, 18, INK2, 2)
            s.text(PAD + 38, y + 20, "Last visit today 11:14–11:52", 12.5, 700, INK2)
            s.text(PAD + 38, y + 36, "Outcome: KYC completed, application sent", 11, 400, MUTED)
    with s.g("tabs"):
        y = 244
        tw_ = (MW - 2 * PAD) / 4
        for i, lab in enumerate(HUB_TABS):
            x = PAD + i * tw_
            on = lab == tab
            if on:
                s.rect(x + 2, y, tw_ - 4, 34, fill=CARD, rx=12, stroke=LINE, shadow=True)
            s.text(x + tw_ / 2, y + 22, lab, 13, 700 if on else 400, BRAND if on else INK2,
                   anchor="middle")
            if not on:
                s.link(x, y, tw_, 34, "!tab:" + keys[i])
    y = 292
    if tab == "Overview":
        journey_card(s, y, 4 if applied else (3 if kyc_done else 1), now=None if kyc_done else 2)
        y += 84
        if during:
            with s.g("why here"):
                s.rect(PAD, y, MW - 2 * PAD, 54, fill=tint(YELLOW, 0.2), rx=14)
                s.text(PAD + 14, y + 22, "WHY YOU'RE HERE · KIWATULE LEADS", 10, 700, YELLOW_D, spacing=0.6)
                s.text(PAD + 14, y + 42, "Wants UGX 6M for a sewing machine", 13.5, 600, INK)
            y += 66
            with s.g("lead details"):
                s.rect(PAD, y, MW - 2 * PAD, 118, fill=CARD, rx=14, stroke=LINE)
                s.icon("flag", PAD + 14, y + 12, 16, BLUE, 2)
                s.text(PAD + 38, y + 25, "LEAD DETAILS FROM SARAH", 10.5, 700, MUTED, spacing=0.6)
                for i, (lab, val) in enumerate([("NIN", CLIENT["nin"]), ("Loan amount", ugx(CLIENT["amount"])),
                                                ("Location", "Kiwatule market · GPS"), ("Lead since", "Wed 23 Sep")]):
                    s.text(PAD + 14, y + 50 + i * 20, lab, 12, 400, MUTED)
                    s.text(MW - PAD - 14, y + 50 + i * 20, val, 12, 600, INK, anchor="end")
            y += 128
            info_row(s, y, "idcard", GREEN, "Next: complete KYC", "3 sections + checks", "!tab:" + keys[1])
        else:
            info_row(s, y, "clock", AMBER_D, "Next: loan decision", "Waiting for Moses Okello · you'll be notified",
                     None, fill=tint(AMBER, 0.12), chev=False)
            y += 66
            info_row(s, y, "briefcase", GREEN, CLIENT["app_id"], "UGX 6,000,000 · 18 months", "!tab:" + keys[2])
            y += 66
            info_row(s, y, "route", BRAND, "Plan: Kiwatule leads", "8 of 12 visited · next: Ivan Kasozi 12:30", "m21b")
    elif tab == "KYC":
        if kyc_done:
            info_row(s, y, "shield", GREEN, "KYC completed · 11:24", "6 of 6 checks passed · ready for a loan",
                     None, fill=tint(GREEN, 0.08), chev=False)
            y += 70
        secs = [("1", "Client details", "Name, phone, age, family, work", "m10", "11:16"),
                ("2", "National ID & photos", "NIRA ID, live selfie, premises", "m11", "11:19"),
                ("3", "Earnings & collateral", "Income, other loans, collateral", "m12", "11:22"),
                ("4", "Checks", "NIRA, phone, CRB, territory", "m13", "11:24")]
        for n, t_, sub, tgt, tm in secs:
            with s.g(f"kyc {t_}"):
                s.rect(PAD, y, MW - 2 * PAD, 58, fill=CARD, rx=14, stroke=LINE)
                if not kyc_done:
                    s.circle(PAD + 26, y + 29, 13, fill=CARD, stroke="#C4C7D6", sw=2)
                    s.text(PAD + 26, y + 33.5, n, 12, 700, INK2, anchor="middle")
                    chip(s, MW - PAD - 14 - tw("To do", 11, 600) - 20, y + 18, "To do", "#8A8DA6", h=22, size=11)
                else:
                    s.circle(PAD + 26, y + 29, 13, fill=GREEN)
                    s.icon("check", PAD + 19, y + 22, 14, "#FFFFFF", 3)
                    s.text(MW - PAD - 16, y + 34, "Done " + tm, 11.5, 600, GREEN_D, anchor="end")
                s.text(PAD + 50, y + 25, t_, 13.5, 600, INK)
                s.text(PAD + 50, y + 43, sub, 11.5, 400, MUTED)
            s.link(PAD, y, MW - 2 * PAD, 58, tgt)
            y += 64
    elif tab == "Loan":
        if not applied:
            info_row(s, y, "shield", GREEN, "KYC completed", "Today 11:24 · 6 of 6 checks", None,
                     fill=tint(GREEN, 0.08), chev=False)
            y += 72
            with s.g("loan start"):
                s.rect(PAD, y, MW - 2 * PAD, 150, fill=CARD, rx=16, stroke=LINE)
                s.text(PAD + 16, y + 28, "No loan application yet", 14, 700, INK)
                s.text(PAD + 16, y + 48, "Asked for UGX 6,000,000 · suggested products", 12, 400, MUTED)
                pills(s, PAD + 16, y + 60, [("MSE Business Loan", True), ("School Fees Loan", False)],
                      maxw=MW - PAD - 16, h=30)
                s.text(PAD + 16, y + 126, "Can pay up to UGX 625,000 a month", 12, 600, GREEN_D)
        else:
            with s.g("application"):
                s.rect(PAD, y, MW - 2 * PAD, 262, fill=CARD, rx=16, stroke=LINE)
                s.text(PAD + 16, y + 26, "LOAN APPLICATION", 10.5, 700, MUTED, spacing=0.8)
                s.text(PAD + 16, y + 52, CLIENT["app_id"], 17, 700, INK)
                chip(s, MW - PAD - 16 - tw("Awaiting approval", 11, 600) - 34, y + 12, "Awaiting approval",
                     STATUS["Awaiting approval"], h=22, size=11, dot=True)
                yy = y + 84
                inst = rnd_instalment(CLIENT["amount"], CLIENT["months"])
                for lab, val in [("Product", CLIENT["product"]), ("Amount", ugx(CLIENT["amount"])),
                                 ("Term", f"{CLIENT['months']} months"), ("Instalment", ugx(inst) + " / month"),
                                 ("Submitted", "Today 11:42 · to Moses Okello"), ("Required items", "7 of 7 ✓")]:
                    s.text(PAD + 16, yy, lab, 12.5, 400, MUTED)
                    s.text(MW - PAD - 16, yy, val, 12.5, 700, GREEN_D if "✓" in val else INK, anchor="end")
                    yy += 29
    else:
        visits = [("Today 11:14" + ("" if during else "–11:52"), "Joel Byaruhanga · visit, KYC",
                   "In progress" if during else "KYC completed · application sent", GREEN),
                  ("Wed 23 Sep 14:05", "Sarah Namuli · made her a lead", "UGX 6M · NIN and location recorded", BLUE),
                  ("Tue 22 Sep 10:18", "Sarah Namuli · prospecting", "Prospect · Kiwatule market route", VIOLET)]
        for when, who, out, col in visits:
            with s.g(f"step {when}"):
                s.rect(PAD, y, MW - 2 * PAD, 72, fill=CARD, rx=14, stroke=LINE)
                s.rect(PAD, y + 14, 4, 44, fill=col, rx=2)
                s.text(PAD + 18, y + 24, when, 13.5, 700, INK)
                s.text(PAD + 18, y + 43, who, 12, 400, MUTED)
                s.text(PAD + 18, y + 61, out, 12, 600, shade(col, 0.15))
            y += 80

    # one action per tab
    actions = {
        (True, "Overview"): ("Check out", "m16b", "logout"),
        (True, "KYC"): ("Start KYC", "m10", "idcard"),
        (True, "Loan"): ("Take loan application", "m14", "briefcase"),
        (True, "History"): ("Check out", "m16b", "logout"),
        (False, "Overview"): ("Check in", "m09", "pin"),
        (False, "KYC"): ("Update KYC", "m10", "idcard"),
        (False, "History"): ("Check in", "m09", "pin"),
    }
    if during and kyc_done and tab == "KYC":
        actions[(True, "KYC")] = ("Continue to loan", "m09c", "arrowright")
    if during and applied and tab == "Loan":
        actions[(True, "Loan")] = ("Check out", "m16b", "logout")
    if (during, tab) in actions:
        lab, tgt, ic = actions[(during, tab)]
        footer(s, lab, tgt, icon=ic)
    else:
        gesture(s)
    return s


def m09_hub():
    return client_hub("M9 Florence: client record, visit in progress", "Overview", True)


def m09b_hub_kyc():
    return client_hub("M9b Florence: KYC tab (visit in progress)", "KYC", True)


def m09c_hub_loan():
    return client_hub("M9c Florence: Loan tab (visit in progress)", "Loan", True)


def m09d_hub_visits():
    return client_hub("M9d Florence: History tab (visit in progress)", "History", True)


def m09f_hub_kyc_done():
    return client_hub("M9f Florence: KYC tab, KYC validated (visit in progress)", "KYC", True, kyc_done=True)


def m09e_hub_applied():
    return client_hub("M9e Florence: Loan tab, application sent (visit in progress)", "Loan", True, applied=True)


def m18_client():
    return client_hub("M18 Florence: client record", "Overview", False)


def m18b_client_kyc():
    return client_hub("M18b Florence: KYC tab", "KYC", False)


def m18c_client_loan():
    return client_hub("M18c Florence: Loan tab", "Loan", False)


def m18d_client_visits():
    return client_hub("M18d Florence: History tab", "History", False)


def m16b_check_out():
    s = phone("M16b Check out: what happened?", bg=CARD, time="11:52")
    app_bar(s, "Check out", back="m09e", sub=f"{CLIENT['name']} · 11:14–11:52 · 38 min")
    y = 100
    s.text(PAD, y, "What happened on this visit?", 15, 700, INK)
    y += 14
    opts = [("KYC completed, application sent", "Detected: LU-APP-2609-04817 at 11:42", True, GREEN),
            ("KYC completed, loan later", "Book a visit to agree the loan", False, TEAL),
            ("Needs more time", "Book another visit", False, BLUE),
            ("No longer interested", "Capture why", False, RED),
            ("Lead not available", "Logged as a visit attempt", False, "#8A8DA6")]
    for lab, sub, on, col in opts:
        with s.g(f"outcome {lab}"):
            s.rect(PAD, y, MW - 2 * PAD, 52, fill=tint(col, 0.07) if on else CARD, rx=12,
                   stroke=col if on else LINE, sw=2 if on else 1, shadow=False)
            radio(s, PAD + 22, y + 26, on, color=col)
            s.text(PAD + 42, y + 22, lab, 13.5, 600, INK)
            s.text(PAD + 42, y + 40, sub, 11.5, 400, MUTED)
        y += 58
    y += 6
    y += m_field(s, y, "Next visit", "When the loan is decided · disbursement", dropdown=True, h=42) + 8
    s.text(PAD, y + 14, "Note (optional)", 13, 600, INK2)
    s.rect(PAD, y + 22, MW - 2 * PAD, 52, fill=CARD, rx=12, stroke="#CDD0DE", shadow=False)
    s.text(PAD + 12, y + 53, "Wants the money before the January term.", 13, 400, INK, maxw=MW - 2 * PAD - 50)
    s.icon("mic", MW - PAD - 32, y + 38, 18, BRAND, 2)
    footer(s, "Check out", "m18", icon="logout")
    return s


NAV_ITEMS = {
    "agent": [("Home", "home", "m03"), ("Prospects", "users", "m06"), ("Leads", "flag", "m17"), ("Me", "user", "m19")],
    "ro": [("Home", "home", "m20"), ("Plan", "route", "m21"), ("Clients", "users", "m23"), ("Me", "user", "m22")],
}

def hero_card(s, y, label, big, of, sub, frac, foot_l, foot_r, bars, bars_label, bars_note):
    HI, HM = "#231F0F", "#6B5A1E"
    with s.g("hero"):
        s.rect(PAD, y, MW - 2 * PAD, 164, fill="url(#heroGrad)", rx=24, name="hero bg")
        s.poly([(MW - PAD - 128, y + 164), (MW - PAD, y + 36), (MW - PAD, y + 140), (MW - PAD - 24, y + 164)],
               fill="#FFFFFF", op=0.22, name="facet")
        s.text(PAD + 20, y + 30, label, 10.5, 700, HM, spacing=1, maxw=190)
        s.text(PAD + 20, y + 80, big, 46, 700, HI)
        s.text(PAD + 22 + tw(big, 46, 700), y + 80, of, 18, 600, HM)
        s.text(PAD + 20, y + 104, sub, 12.5, 600, HM, maxw=180)
        with s.g("mini chart"):
            x0, x1, base = MW - PAD - 136, MW - PAD - 20, y + 86
            n = len(bars)
            bw = (x1 - x0) / n
            mx = max(v for v, _ in bars)
            s.text(x0, y + 30, bars_label, 10.5, 700, HM)
            for i, (v, lab) in enumerate(bars):
                h_ = 44 * v / mx
                b = min(bw - 6, 16)
                s.rect(x0 + i * bw + (bw - b) / 2, base - h_, b, h_, fill=HI, rx=2.5, op=1 if i == n - 1 else 0.22)
            s.text(x0, y + 104, bars_note, 10.5, 700, "#0D5A34")
        s.rect(PAD + 20, y + 122, MW - 2 * PAD - 40, 6, fill="#FFFFFF", rx=3, op=0.55)
        s.rect(PAD + 20, y + 122, (MW - 2 * PAD - 40) * frac, 6, fill=HI, rx=3)
        s.text(PAD + 20, y + 150, foot_l, 12, 700, HI)
        s.text(MW - PAD - 20, y + 150, foot_r, 12, 700, HI, anchor="end")

def home_top(s, ini, name, col=YELLOW):
    s.raw('<defs><linearGradient id="heroGrad" x1="0" y1="0" x2="1" y2="1">'
          '<stop offset="0" stop-color="#FFE45C"/><stop offset="1" stop-color="#FBC805"/></linearGradient></defs>')
    with s.g("top"):
        s.circle(PAD + 22, 70, 22, fill=col)
        s.text(PAD + 22, 76, ini, 15, 700, BRAND_D, anchor="middle")
        s.text(PAD + 54, 63, "Good morning", 12.5, 400, MUTED)
        s.text(PAD + 54, 84, name, 19, 700, INK)
        for i, ic in enumerate(["search", "bell"]):
            cx = MW - PAD - 20 - i * 48
            s.circle(cx, 70, 20, fill=CARD, shadow=True)
            s.icon(ic, cx - 10, 60, 20, INK, 2)
        s.circle(MW - PAD - 12, 60, 4.5, fill=RED)

def stat_links(s, y, targets):
    """Each stat card opens its own list."""
    cw = (MW - 2 * PAD - 16) / 3
    for i, t in enumerate(targets):
        s.link(PAD + i * (cw + 8), y, cw, 84, t)


def stat_cards(s, y, items):
    cw = (MW - 2 * PAD - 16) / 3
    with s.g("stats"):
        for i, (lab, val, sub, subcol, col) in enumerate(items):
            x = PAD + i * (cw + 8)
            s.rect(x, y, cw, 84, fill=CARD, rx=18, stroke=LINE)
            s.circle(x + 18, y + 20, 4, fill=col)
            s.text(x + 28, y + 24, lab, 11, 600, MUTED, maxw=cw - 34)
            s.text(x + 14, y + 55, val, 24, 700, INK)
            s.text(x + 14, y + 73, sub, 10.5, 600 if subcol != MUTED else 400, subcol, maxw=cw - 20)

ROUTE_WEEK = [("Mon 28", "Ntinda stage route", 50, 52, "done"),
              ("Tue 29", "Kiwatule market route", 50, 47, "done"),
              ("Wed 30", "Kiwatule market route", 50, 32, "today"),
              ("Thu 1", "Kigoowa estates route", 40, 0, "later"),
              ("Fri 2", "Ntinda schools route", 40, 0, "later")]

def m04a_route_plan():
    s = phone("M4a Route journey plan: week 40", bg=BG, time="11:06")
    app_bar(s, "Week 40", back="m04", sub="28 Sep – 2 Oct · set by Moses Okello", history=True)
    with s.g("week target"):
        y = 94
        s.rect(PAD, y, MW - 2 * PAD, 96, fill=CARD, rx=16, stroke=LINE)
        s.text(PAD + 16, y + 26, "WEEK TARGET", 10.5, 700, MUTED, spacing=0.8)
        s.text(PAD + 16, y + 60, "131", 28, 700, INK)
        s.text(PAD + 18 + tw("131", 28, 700), y + 60, " of 230 prospects", 14, 600, INK2)
        s.text(MW - PAD - 16, y + 26, "57%", 13, 700, AMBER_D, anchor="end")
        progress(s, PAD + 16, y + 74, MW - 2 * PAD - 32, 131 / 230, STAGE["Prospect"], h=7)
    s.text(PAD, 222, "Routes by day", 15, 700, INK)
    s.text(MW - PAD, 222, "target per route", 12, 400, MUTED, anchor="end")
    y = 234
    for day, route, tgt, done, st in ROUTE_WEEK:
        today = st == "today"
        with s.g(f"day {day}"):
            s.rect(PAD, y, MW - 2 * PAD, 70, fill=CARD, rx=14, stroke=BRAND if today else LINE, sw=2 if today else 1)
            s.rect(PAD + 12, y + 12, 46, 46, fill=BRAND if today else ("#F1F2F8" if st == "later" else
                                                                     tint(GREEN, 0.12)), rx=12, shadow=False)
            d, n = day.split()
            fg = "#FFFFFF" if today else (INK2 if st == "later" else GREEN_D)
            s.text(PAD + 35, y + 31, d, 11, 600, fg, anchor="middle")
            s.text(PAD + 35, y + 50, n, 16, 700, fg, anchor="middle")
            s.text(PAD + 70, y + 28, route, 13.5, 700, INK, maxw=180)
            if st == "later":
                s.text(PAD + 70, y + 48, f"Target {tgt} prospects", 12, 400, MUTED)
            else:
                progress(s, PAD + 70, y + 42, 150, min(done / tgt, 1), GREEN if done >= tgt else STAGE["Prospect"],
                         h=6)
                s.text(PAD + 70, y + 62, ("In progress · " if today else "") + f"{done} of {tgt}", 11.5, 600,
                       BRAND if today else (GREEN_D if done >= tgt else AMBER_D))
            if st == "done":
                s.icon("check" if done >= tgt else "clock", MW - PAD - 34, y + 25, 20, GREEN if done >= tgt else
                       AMBER_D, 2.6)
            elif today:
                button(s, MW - PAD - 12, y + 19, "Map", "soft", icon="map", h=32, size=12, anchor="end")
        if today:
            s.link(PAD, y, MW - 2 * PAD, 70, "m04b")
        y += 78
    with s.g("territory note"):
        s.icon("shield", PAD, y + 6, 16, GREEN_D, 2)
        para(s, PAD + 24, y + 18, "All routes are inside your territory, Ntinda · Kiwatule. The app tells you if you "
                                  "leave it.", MW - 2 * PAD - 30, 12, 400, MUTED, lh=17)
    bottom_nav(s, "Home")
    return s

def m04b_prospect_map():
    s = phone("M4b Prospect map: Kiwatule market route", bg=BG, time="11:08")
    app_bar(s, "Prospect map", back="m04a", sub="Kiwatule market route · today", history=True)
    with s.g("summary chips"):
        x = PAD
        for lab, col in [("32 prospects", STAGE["Prospect"]), ("3 leads", STAGE["Lead"]), ("2.6 h on route", GREEN)]:
            x += chip(s, x, 92, lab, col, h=28, size=12, dot=True) + 8
    m = StreetMap(s, PAD, 130, MW - 2 * PAD, 330, seed=11, lake=False, dense=0.75,
                  places=[("Ntinda", 0.2, 0.16), ("Kiwatule", 0.68, 0.22), ("Kiwatule market", 0.56, 0.62)])
    s.rect(PAD, 130, MW - 2 * PAD, 330, fill="none", rx=14, stroke=LINE)
    terr = [m.P(*p) for p in [(0.04, 0.05), (0.96, 0.06), (0.95, 0.94), (0.05, 0.95)]]
    s.poly(terr, stroke=GREEN, sw=2, dash="6 5", name="territory geofence")
    route = [m.P(*p) for p in [(0.2, 0.8), (0.34, 0.66), (0.48, 0.6), (0.62, 0.64), (0.74, 0.52), (0.84, 0.36)]]
    s.poly(route, stroke=tint(BRAND, 0.35), sw=4, closed=False, name="route")
    import random
    rnd = random.Random(9)
    with s.g("prospects"):
        for _ in range(32):
            t = rnd.uniform(0, 0.999) * (len(route) - 1)
            i = int(t)
            fx = route[i][0] + (route[i + 1][0] - route[i][0]) * (t - i) + rnd.uniform(-16, 16)
            fy = route[i][1] + (route[i + 1][1] - route[i][1]) * (t - i) + rnd.uniform(-14, 14)
            s.circle(fx, fy, 4.5, fill=STAGE["Prospect"], stroke="#FFFFFF", sw=1.4)
    for q in [(0.36, 0.6), (0.6, 0.7), (0.7, 0.5)]:
        map_pin(s, *m.P(*q), STAGE["Lead"], None, 0.8, name="lead")
    agent_x, agent_y = m.P(0.62, 0.62)
    s.circle(agent_x, agent_y, 16, fill=BRAND, op=0.18)
    s.circle(agent_x, agent_y, 8, fill=BRAND, stroke="#FFFFFF", sw=2.5, name="you are here")
    with s.g("legend"):
        lx, ly = PAD + 10, 470
        for lab, col in [("Prospect", STAGE["Prospect"]), ("Lead", STAGE["Lead"]), ("You", BRAND)]:
            s.circle(lx + 6, ly + 6, 5, fill=col)
            lx += s.text(lx + 16, ly + 10, lab, 11.5, 400, INK2) + 30
        s.line(lx, ly + 6, lx + 18, ly + 6, GREEN, 2, dash="4 3")
        s.text(lx + 24, ly + 10, "Territory", 11.5, 400, INK2)
    s.text(PAD, 512, "Latest prospects", 15, 700, INK)
    s.text(MW - PAD, 512, "All 32", 12.5, 600, BRAND, anchor="end")
    s.link(MW - PAD - 60, 496, 60, 24, "m06")
    y = 524
    for nm, sub in [("Joseph Kiggundu", "10:52 · 0701 552 ···"), ("Mariam Nakalema", "10:41 · 0783 120 ···")]:
        with s.g(f"prospect {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 54, fill=CARD, rx=12, stroke=LINE)
            s.circle(PAD + 22, y + 27, 5, fill=STAGE["Prospect"])
            s.text(PAD + 38, y + 23, nm, 13.5, 600, INK)
            s.text(PAD + 38, y + 41, sub, 11.5, 400, MUTED)
            s.icon("chevright", MW - PAD - 30, y + 17, 20, FAINT)
        y += 60
    add_button(s, "Add prospect", "m05")
    bottom_nav(s, "Prospects")
    return s

def m05_add_prospect():
    s = phone("M5 Add a prospect", bg=CARD, time="10:52")
    app_bar(s, "Add a prospect", back="m06", sub="Name, phone and location", history=True)
    with s.g("gps"):
        y = 92
        s.rect(PAD, y, MW - 2 * PAD, 40, fill=tint(GREEN, 0.08), rx=10)
        s.icon("pin", PAD + 12, y + 11, 18, GREEN_D, 2)
        s.text(PAD + 38, y + 25, "Kiwatule market route · inside your territory", 12.5, 600, GREEN_D)
    y = 150
    y += m_field(s, y, "Full name", "Joseph Kiggundu", icon="user") + 14
    y += m_field(s, y, "Phone number", "0701 552 ···", icon="phone", ok="New number: not yet a Letshego client") + 14
    y += m_field(s, y, "Location", "Kiwatule market · from GPS ±6 m", icon="crosshair") + 20
    with s.g("next step note"):
        s.rect(PAD, y, MW - 2 * PAD, 58, fill="#F5F5FB", rx=12)
        s.icon("flag", PAD + 14, y + 19, 20, BRAND, 2)
        para(s, PAD + 46, y + 25, "Wants a loan? Make him a lead later from My prospects.", MW - 2 * PAD - 60, 12,
             400, INK2, lh=17)
    footer(s, "Save prospect", "m06", icon="check", secondary="+ Next", sec_target="m05")
    return s

PROSPECTS = [
    (CALLEE["name"], "AN", "Mon 15:40 · Kiwatule market", "0752 664 ···", True),
    ("Tony Kizito", "TK", "Mon 16:05 · Kiwatule market", "0772 310 ···", False),
    ("Faith Ahimbisibwe", "FA", "Tue 11:20 · Kiwatule market", "0701 845 ···", False),
    ("Ronald Mubiru", "RM", "Tue 14:02 · Kiwatule market", "0756 228 ···", False),
    ("Hassan Mugerwa", "HM", "Tue 15:30 · Kiwatule market", "0783 551 ···", False),
    ("Joseph Kiggundu", "JK", "Today 10:52 · Kiwatule market", "0701 552 ···", False),
]

def m06_prospects():
    s = phone("M6 My prospects", bg=BG, time="14:18")
    app_bar(s, "My prospects", sub="1,486 this quarter · 32 today", right="map")
    s.link(MW - 60, 24, 60, 56, "m04b")
    with s.g("filter chips"):
        x = PAD
        for lab, on in [("Not yet leads 6", True), ("Leads 14", False), ("All 1,486", False)]:
            w = tw(lab, 12.5, 600) + 26
            s.rect(x, 94, w, 32, fill=BRAND if on else CARD, rx=16, stroke=None if on else "#CDD0DE")
            s.text(x + 13, 114.5, lab, 12.5, 600, "#FFFFFF" if on else INK2)
            x += w + 8
    y = 140
    for nm, ini, met, ph, hl in PROSPECTS:
        with s.g(f"prospect {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 68, fill=CARD, rx=14, stroke=BRAND if hl else LINE, sw=2 if hl else 1)
            avatar(s, PAD + 32, y + 34, 18, ini, VIOLET)
            s.text(PAD + 60, y + 28, nm, 14, 600, INK, maxw=200)
            s.text(PAD + 60, y + 47, f"{met} · {ph}", 11.5, 400, MUTED, maxw=230)
            s.icon("chevright", MW - PAD - 30, y + 24, 20, FAINT)
        if hl:
            s.link(PAD, y, MW - 2 * PAD, 68, "m07")
        y += 76
    add_button(s, "Add prospect", "m05")
    bottom_nav(s, "Prospects")
    return s


def m07b_lead():
    c = CALLEE
    s = phone("M7b Make a lead: Aisha Nalubega", bg=CARD, time="14:24")
    app_bar(s, "Make a lead", back="m07", sub=c["name"])
    with s.g("funnel step"):
        y = 92
        x = PAD
        for lab, on in [("Prospect", False), ("Lead", True), ("KYC completed", False)]:
            col = STAGE[lab]
            w = chip(s, x, y, lab, col if on or lab == "Prospect" else "#8A8DA6", h=26, size=11.5,
                     solid=on, icon="check" if lab == "Prospect" else None)
            x += w + 4
            if lab != "KYC completed":
                s.icon("chevright", x, y + 5, 16, FAINT)
                x += 20
    y = 140
    y += m_field(s, y, "National ID number (NIN)", "CM88•••••••2PL", icon="idcard") + 14
    y += m_field(s, y, "Loan amount", "2,000,000", suffix="UGX", icon="banknote") + 14
    y += m_field(s, y, "Location", "Kiwatule market · stall row C", icon="pin",
                 ok="From her prospect pin · inside your territory") + 20
    with s.g("what happens next"):
        s.rect(PAD, y, MW - 2 * PAD, 58, fill="#F5F5FB", rx=12)
        s.icon("route", PAD + 14, y + 19, 20, BRAND, 2)
        para(s, PAD + 46, y + 25, "Moses puts new leads on a lead journey plan for a relationship officer.",
             MW - 2 * PAD - 60, 12, 400, INK2, lh=17)
    footer(s, "Save lead", "m07c", icon="check", color=STAGE["Lead"])
    return s

def m07c_lead_done():
    c = CALLEE
    s = phone("M7c Lead created", bg=CARD, time="14:25")
    s.circle(MW / 2, 210, 62, fill=tint(BLUE, 0.14))
    s.circle(MW / 2, 210, 44, fill=BLUE)
    s.icon("flag", MW / 2 - 22, 188, 44, "#FFFFFF", 2.6)
    s.text(MW / 2, 310, "Lead created", 23, 700, INK, anchor="middle")
    s.text(MW / 2, 336, f"{c['name']} · {ugx(c['amount'])}", 14, 400, INK2, anchor="middle")
    with s.g("summary"):
        y = 364
        s.rect(PAD, y, MW - 2 * PAD, 120, fill="#F5F5FB", rx=14)
        for i, (lab, val) in enumerate([("Lead", "LD-2609-1182"), ("Goes to", "Moses Okello · lead journey plan"),
                                        ("Then", "A relationship officer visits")]):
            s.text(PAD + 16, y + 32 + i * 34, lab, 13, 400, MUTED)
            s.text(MW - PAD - 16, y + 32 + i * 34, val, 13.5, 700, INK, anchor="end")
    with s.g("this week"):
        y = 502
        s.rect(PAD, y, MW - 2 * PAD, 104, fill=tint(YELLOW, 0.22), rx=14)
        s.text(PAD + 16, y + 26, "THIS WEEK", 10.5, 700, YELLOW_D, spacing=0.8)
        cw = (MW - 2 * PAD - 32) / 3
        for i, (v, lab, d) in enumerate([("131", "Prospects", ""), ("15", "Leads", "+1"), ("3", "KYC completed", "")]):
            x = PAD + 16 + i * cw
            s.text(x, y + 64, v, 24, 700, INK)
            if d:
                s.text(x + tw(v, 24, 700) + 6, y + 64, d, 13, 700, GREEN_D)
            s.text(x, y + 86, lab, 12, 400, INK2)
    button(s, PAD, MH - 140, "Back to my prospects", "primary", icon="arrowleft", w=MW - 2 * PAD, h=48)
    s.link(PAD, MH - 140, MW - 2 * PAD, 48, "m06")
    s.text(MW / 2, MH - 64, "Home", 13, 600, BRAND, anchor="middle")
    s.link(MW / 2 - 70, MH - 84, 140, 32, "m03")
    gesture(s)
    return s

MY_LEADS = [
    (CALLEE["name"], 2_000_000, "Lead", "Created today 14:25 · waiting for a lead journey plan", None),
    (CLIENT["name"], 6_000_000, "KYC completed", "Joel Byaruhanga · today 11:24 · loan sent", None),
    ("Betty Nakimuli", 2_000_000, "Client", "Loan disbursed today · KYC by Joel", None),
    ("Ivan Kasozi", 3_000_000, "On a lead journey plan", "Joel · visit today 12:30", None),
    ("Charles Ssempijja", 3_000_000, "On a lead journey plan", "Joel · visit Thu 1 Oct", None),
    ("Kenneth Lubega", 4_000_000, "Follow-up", "Joel visited · employer letter pending", None),
]

def m17_leads():
    s = phone("M17 My leads: where they are now", bg=BG, time="14:26")
    app_bar(s, "My leads", sub="286 this quarter · 31 became clients")
    with s.g("filter chips"):
        x = PAD
        for lab, on in [("All 14", True), ("Waiting 3", False), ("On a plan 6", False), ("KYC 3", False)]:
            w = tw(lab, 12.5, 600) + 26
            s.rect(x, 94, w, 32, fill=BRAND if on else CARD, rx=16, stroke=None if on else "#CDD0DE")
            s.text(x + 13, 114.5, lab, 12.5, 600, "#FFFFFF" if on else INK2)
            x += w + 8
    y = 140
    for nm, amt, st, nxt, _ in MY_LEADS:
        col = STATUS.get(st, BRAND)
        with s.g(f"lead {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 80, fill=CARD, rx=12, stroke=LINE)
            s.rect(PAD, y + 12, 4, 56, fill=col, rx=2)
            s.text(PAD + 18, y + 26, nm, 14.5, 600, INK, maxw=170)
            chip(s, MW - PAD - 12 - tw(st, 11, 600) - 34, y + 12, st, col, h=22, size=11, dot=True)
            s.text(PAD + 18, y + 46, ugx(amt), 12, 600, INK2)
            s.icon("clock", PAD + 18, y + 55, 14, MUTED, 2)
            s.text(PAD + 38, y + 67, nxt, 12, 400, MUTED, maxw=MW - 2 * PAD - 50)
        y += 88
    bottom_nav(s, "Leads")
    return s


def m20_ro_home():
    s = phone("M20 Home (relationship officer)", bg=BG, time="11:05")
    home_top(s, "JB", "Joel Byaruhanga", col=tint(TEAL, 0.35))
    hero_card(s, 108, "TODAY'S LEAD PLAN", "2", "/5 leads", "visited · 2 KYCs", 2 / 5,
              "Next: Florence Nambi", "Plan by Moses",
              [(4, "Mon"), (5, "Tue"), (2, "Wed")], "Leads visited / day", "Mon–Wed")
    s.text(PAD, 300, "This week", 15, 700, INK)
    s.text(MW - PAD, 300, "leads to clients", 12, 400, MUTED, anchor="end")
    stat_cards(s, 312, [("Leads to visit", "8", "3 left today", MUTED, STAGE["Lead"]),
                        ("Visited", "11", "of 16 planned", MUTED, TEAL),
                        ("KYC", "6", "completed · ▲ 2", GREEN_D, STAGE["KYC completed"])])
    stat_links(s, 312, ["m21b", "m21b", "m23"])
    with s.g("up next"):
        s.text(PAD, 426, "Up next", 15, 700, INK)
        s.text(MW - PAD, 426, "Kiwatule leads", 12, 400, MUTED, anchor="end")
        y = 438
        s.rect(PAD, y, MW - 2 * PAD, 76, fill=CARD, rx=20, stroke=LINE)
        avatar(s, PAD + 38, y + 38, 22, "FN", BLUE)
        s.text(PAD + 70, y + 34, CLIENT["name"], 15, 700, INK)
        s.text(PAD + 70, y + 54, "Lead from Sarah · UGX 6M · 0.6 km", 12, 400, MUTED)
        s.circle(MW - PAD - 38, y + 38, 22, fill=BRAND)
        s.icon("arrowright", MW - PAD - 48, y + 28, 20, "#FFFFFF", 2.4)
        s.link(PAD, y, MW - 2 * PAD, 76, "m09")
    with s.g("today"):
        s.text(PAD, 544, "Today", 15, 700, INK)
        s.text(PAD + 52, 544, "5 leads · 3 left", 12, 400, MUTED)
        y = 556
        s.rect(PAD, y, MW - 2 * PAD, 92, fill=CARD, rx=20, stroke=LINE)
        items = [("KL", "Kenneth", "09:05", "done"), ("BN", "Betty", "10:20", "done"), ("FN", "Florence", "Next", "next"),
                 ("IK", "Ivan", "12:30", "later"), ("CS", "Charles", "15:00", "later")]
        n = len(items)
        x0, x1 = PAD + 36, MW - PAD - 36
        cy = y + 34
        s.line(x0, cy, x1, cy, LINE2, 2)
        s.line(x0, cy, x0 + (x1 - x0) * 2 / (n - 1), cy, tint(GREEN, 0.5), 2)
        for i, (ini, nm, tm, st) in enumerate(items):
            cx = x0 + (x1 - x0) * i / (n - 1)
            col = {"done": GREEN, "next": BRAND}.get(st, "#D5D7E0")
            if st == "next":
                s.circle(cx, cy, 21, fill=tint(BRAND, 0.14))
            s.circle(cx, cy, 15, fill=col if st != "later" else CARD, stroke=col, sw=2)
            s.text(cx, cy + 4, ini, 10, 700, "#FFFFFF" if st != "later" else INK2, anchor="middle")
            s.text(cx, cy + 32, nm, 11, 700 if st == "next" else 400, INK if st == "next" else INK2, anchor="middle")
            s.text(cx, cy + 46, tm, 10, 600 if st == "next" else 400, BRAND if st == "next" else MUTED,
                   anchor="middle")
        s.link(x0 + (x1 - x0) * 2 / (n - 1) - 22, cy - 22, 44, 70, "m09")
    bottom_nav(s, "Home", role="ro")
    return s

def m21b_lead_plan():
    s = phone("M21b Lead journey plan: Kiwatule leads", bg=BG, time="11:07")
    app_bar(s, "Kiwatule leads", back="m21", sub="28 Sep – 2 Oct · by Moses Okello", right="more", history=True)
    with s.g("plan info"):
        y = 92
        s.rect(PAD, y, MW - 2 * PAD, 68, fill=CARD, rx=12, stroke=LINE)
        s.text(PAD + 14, y + 22, "Leads from Sarah Namuli and Peter Kato", 12.5, 400, INK2, maxw=MW - 2 * PAD - 28)
        s.text(PAD + 14, y + 38, "Goal: complete KYC for 8 of 12", 12.5, 400, INK2)
        progress(s, PAD + 14, y + 50, MW - 2 * PAD - 110, 7 / 12, GREEN, h=6)
        s.text(MW - PAD - 14, y + 56, "7 of 12", 12.5, 700, INK, anchor="end")
    m = StreetMap(s, PAD, 172, MW - 2 * PAD, 196, seed=11, lake=False, dense=0.7,
                  places=[("Ntinda", 0.25, 0.2), ("Kiwatule", 0.7, 0.3)])
    s.rect(PAD, 172, MW - 2 * PAD, 196, fill="none", rx=12, stroke=LINE)
    spots = [(0.1, 0.15), (0.22, 0.3), (0.34, 0.18), (0.46, 0.34), (0.3, 0.52), (0.42, 0.66), (0.56, 0.54),
             (0.66, 0.4), (0.8, 0.52), (0.88, 0.72), (0.7, 0.84), (0.52, 0.86)]
    pts = [m.P(*q) for q in spots]
    s.poly(pts, stroke=BRAND, sw=2.5, closed=False, dash="2 6", name="visit order")
    for i, (qx, qy) in enumerate(pts):
        col = GREEN if i < 7 else (BRAND if i < 9 else "#8A8DA6")
        map_pin(s, qx, qy, col, str(i + 1), 0.72, name=f"lead {i + 1}")
    s.text(PAD, 394, "Leads in visit order", 15, 700, INK)
    s.text(MW - PAD, 394, "Show visited (7)", 12.5, 600, BRAND, anchor="end")
    rows = [("6", "Kenneth Lubega", "Visited 09:05 · employer letter pending", "done"),
            ("7", "Betty Nakimuli", "Visited 10:20 · KYC completed", "done"),
            ("8", CLIENT["name"], "Due now · UGX 6M · from Sarah · 0.6 km", "next"),
            ("9", "Ivan Kasozi", "Due 12:30 · UGX 3M · from Sarah", "due"),
            ("10", "Charles Ssempijja", "Thu 1 Oct · UGX 3M · from Peter", "later")]
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
    bottom_nav(s, "Plan", role="ro")
    return s

def m22_ro_me():
    s = phone("M22 Me (relationship officer)", bg=BG, time="12:02")
    me_header(s, "JB", "Joel Byaruhanga", tint(TEAL, 0.35), "Staff ID LU-0954",
              [("Relationship Officer", TEAL)])
    with s.g("also assigned"):
        y = 146
        s.rect(PAD, y, MW - 2 * PAD, 46, fill=tint(BRAND, 0.06), rx=12)
        s.icon("route", PAD + 12, y + 13, 20, BRAND, 2)
        s.text(PAD + 42, y + 20, "Also assigned: a route journey plan", 13, 700, INK)
        s.text(PAD + 42, y + 37, "Fri 2 Oct · Kigoowa estates · 30 prospects · by Moses", 11.5, 400, MUTED,
               maxw=MW - 2 * PAD - 54)
    with s.g("quarter"):
        y = 204
        s.rect(PAD, y, MW - 2 * PAD, 112, fill=CARD, rx=20, stroke=LINE)
        s.text(PAD + 16, y + 26, "Q3 2026 performance", 14, 700, INK)
        cw = (MW - 2 * PAD - 32) / 3
        for i, (v, lab) in enumerate([("214", "Leads visited"), ("61", "KYC completed"), ("46", "clients")]):
            x = PAD + 16 + i * cw
            s.text(x, y + 64, v, 21, 700, INK)
            s.text(x, y + 84, lab, 12, 400, MUTED)
        s.text(PAD + 16, y + 102, "Target 70 KYC · 87% · clients = loans disbursed", 11.5, 600, GREEN_D)
    y = 338
    s.text(PAD, y, "This week", 15, 700, INK)
    s.text(MW - PAD, y, "W40 · 28 Sep – 2 Oct", 12, 400, MUTED, anchor="end")
    y += 12
    s.rect(PAD, y, MW - 2 * PAD, 94, fill=CARD, rx=16, stroke=LINE)
    s.text(PAD + 16, y + 26, "Leads visited vs plan", 13, 400, INK2)
    s.text(MW - PAD - 16, y + 26, "11 of 16", 13, 700, INK, anchor="end")
    progress(s, PAD + 16, y + 35, MW - 2 * PAD - 32, 11 / 16, TEAL, h=5)
    s.text(PAD + 16, y + 72, "KYC completed · average time", 13, 400, INK2)
    s.text(MW - PAD - 16, y + 72, "6 · 18 min", 13, 700, INK, anchor="end")
    y += 108
    y += where_card(s, y, [("store", "Branch", "Kampala East", "Manager: Moses Okello"),
                           ("layers", "Territories", "2 territories", "Ntinda · Kigoowa"),
                           ("route", "Routes", "9 routes", "from lead plans")], target="m21") + 10
    sign_out_row(s, y)
    bottom_nav(s, "Me", role="ro")
    return s

def m23_ro_clients():
    s = phone("M23 My leads and clients (relationship officer)", bg=BG, time="11:58")
    app_bar(s, "Leads & clients", sub="61 KYC completed · 46 clients this quarter")
    with s.g("filter chips"):
        x = PAD
        for lab, on in [("All 18", True), ("Leads 9", False), ("KYC 4", False), ("Clients 2", False)]:
            w = tw(lab, 12.5, 600) + 26
            s.rect(x, 94, w, 32, fill=BRAND if on else CARD, rx=16, stroke=None if on else "#CDD0DE")
            s.text(x + 13, 114.5, lab, 12.5, 600, "#FFFFFF" if on else INK2)
            x += w + 8
    y = 140
    for nm, sub, st, nxt in MY_CLIENTS:
        col = STATUS.get(st, BRAND)
        with s.g(f"client {nm}"):
            s.rect(PAD, y, MW - 2 * PAD, 84, fill=CARD, rx=12, stroke=LINE)
            s.rect(PAD, y + 12, 4, 60, fill=col, rx=2)
            s.text(PAD + 18, y + 26, nm, 14.5, 600, INK, maxw=170)
            chip(s, MW - PAD - 12 - tw(st, 11, 600) - 34, y + 12, st, col, h=22, size=11, dot=True)
            s.text(PAD + 18, y + 47, sub, 12, 400, MUTED)
            s.icon("clock", PAD + 18, y + 58, 14, INK2, 2)
            s.text(PAD + 38, y + 70, nxt, 12.5, 600, INK2)
        if nm == CLIENT["name"]:
            s.link(PAD, y, MW - 2 * PAD, 84, "m18")
        y += 92
    bottom_nav(s, "Clients", role="ro")
    return s


def theme_button(s):
    with s.g("theme switch"):
        s.circle(MW - PAD - 20, 60, 20, fill=CARD, shadow=True)
        s.icon("moon", MW - PAD - 30, 50, 20, INK, 2)
        s.text(MW - PAD - 20, 96, "Theme", 10.5, 600, MUTED, anchor="middle")
    s.link(MW - PAD - 44, 36, 48, 68, "!theme")

def me_header(s, ini, name, avatar_fill, staff, roles):
    with s.g("header"):
        s.circle(PAD + 32, 88, 30, fill=avatar_fill)
        s.text(PAD + 32, 97, ini, 20, 700, BRAND_D, anchor="middle")
        s.text(PAD + 76, 80, name, 19, 700, INK)
        s.text(PAD + 76, 100, staff, 12.5, 400, MUTED)
        x = PAD + 76
        for lab, col in roles:
            x += chip(s, x, 110, lab, col, h=22, size=11, dot=True) + 6
    theme_button(s)

def where_card(s, y, rows, target=None):
    """The user's place in Letshego's hierarchy: one row per level, joined by a line."""
    h = 34 + 46 * len(rows)
    with s.g("where you work"):
        s.rect(PAD, y, MW - 2 * PAD, h, fill=CARD, rx=16, stroke=LINE)
        s.text(PAD + 16, y + 24, "WHERE YOU WORK", 10.5, 700, MUTED, spacing=0.8)
        for i, (ic, level, value, sub) in enumerate(rows):
            yy = y + 36 + i * 46
            if i < len(rows) - 1:
                s.line(PAD + 32, yy + 32, PAD + 32, yy + 46, LINE, 2)
            s.rect(PAD + 16, yy, 32, 32, fill=tint(BRAND, 0.08), rx=10, shadow=False)
            s.icon(ic, PAD + 23, yy + 7, 18, BRAND, 2)
            s.text(PAD + 58, yy + 13, level.upper(), 9.5, 700, FAINT, spacing=0.6)
            s.text(PAD + 58, yy + 30, value, 13.5, 700, INK, maxw=150)
            s.text(MW - PAD - 16, yy + 30, sub, 11.5, 400, MUTED, anchor="end", maxw=120)
    if target:
        s.link(PAD, y, MW - 2 * PAD, h, target)
    return h

def sign_out_row(s, y):
    with s.g("row Sign out"):
        s.rect(PAD, y, MW - 2 * PAD, 48, fill=CARD, rx=14, stroke=LINE)
        s.icon("logout", PAD + 14, y + 13, 22, RED, 2)
        s.text(PAD + 48, y + 21, "Sign out", 13.5, 600, RED)
        s.text(PAD + 48, y + 38, "All synced 14:39 · sign back in offline with your PIN", 11.5, 400, MUTED)
    s.link(PAD, y, MW - 2 * PAD, 48, "m02")


def add_button(s, label, target, y=MH - 140):
    """Floating action for the screen it sits on, bottom right above the tab bar."""
    w = tw(label, 13.5, 700) + 56
    x = MW - PAD - w
    with s.g(f"floating {label}"):
        s.rect(x, y, w, 46, fill=BRAND, rx=23, shadow=True)
        s.icon("plus", x + 16, y + 13, 20, "#FFFFFF", 2.6)
        s.text(x + 42, y + 28.5, label, 13.5, 700, "#FFFFFF")
    s.link(x, y, w, 46, target)

def m07_prospect():
    c = CALLEE
    s = phone("M7 Prospect: Aisha Nalubega", bg=BG, time="14:20")
    app_bar(s, c["name"], back="m06", sub="Prospect", history=True)
    with s.g("prospect header"):
        y = 92
        s.rect(PAD, y, MW - 2 * PAD, 84, fill=CARD, rx=18, stroke=LINE)
        avatar(s, PAD + 34, y + 42, 22, c["initials"], VIOLET)
        s.text(PAD + 66, y + 34, c["name"], 15, 700, INK)
        chip(s, PAD + 66, y + 46, "Prospect", STAGE["Prospect"], h=22, size=11, dot=True)
    with s.g("details"):
        y = 188
        s.rect(PAD, y, MW - 2 * PAD, 108, fill=CARD, rx=16, stroke=LINE)
        for i, (ic, lab, val) in enumerate([("phone", "Phone", c["phone"]),
                                            ("calendar", "Added", "Mon 28 Sep 15:40 · by you"),
                                            ("route", "Route", "Kiwatule market route")]):
            yy = y + 16 + i * 30
            s.icon(ic, PAD + 16, yy, 16, MUTED, 2)
            s.text(PAD + 42, yy + 13, lab, 12.5, 400, MUTED)
            s.text(MW - PAD - 16, yy + 13, val, 12.5, 600, INK, anchor="end")
    with s.g("location"):
        y = 308
        s.text(PAD, y + 4, "Location", 13, 700, INK)
        m = StreetMap(s, PAD, y + 16, MW - 2 * PAD, 200, seed=11, lake=False, dense=0.7,
                      places=[("Kiwatule market", 0.5, 0.7)])
        s.rect(PAD, y + 16, MW - 2 * PAD, 200, fill="none", rx=14, stroke=LINE)
        map_pin(s, *m.P(0.52, 0.5), STAGE["Prospect"], None, 1.1, name="her location")
        s.text(PAD, y + 238, "Kiwatule market, stall row C · GPS ±6 m", 12, 400, MUTED)
    footer(s, "Make a lead", "m07b", icon="flag", secondary="No loan", sec_target="m08")
    return s


def filter_chips(s, items, y=94):
    with s.g("filter chips"):
        x = PAD
        for lab, on in items:
            w = tw(lab, 12.5, 600) + 26
            s.rect(x, y, w, 32, fill=BRAND if on else CARD, rx=16, stroke=None if on else "#CDD0DE")
            s.text(x + 13, y + 20.5, lab, 12.5, 600, "#FFFFFF" if on else INK2)
            x += w + 8

def plan_card(s, y, name, dates, line, done, total, foot, status, color, target=None, hl=False):
    with s.g(f"plan {name}"):
        s.rect(PAD, y, MW - 2 * PAD, 118, fill=CARD, rx=14, stroke=BRAND if hl else LINE, sw=2 if hl else 1)
        s.text(PAD + 14, y + 26, name, 14.5, 700, INK, maxw=MW - 2 * PAD - 120)
        chip(s, MW - PAD - 14 - tw(status, 11, 600) - 34, y + 12, status, STATUS[status], h=22, size=11, dot=True)
        s.icon("calendar", PAD + 14, y + 36, 14, INK2, 2)
        s.text(PAD + 34, y + 48, dates, 12, 600, INK2, maxw=MW - 2 * PAD - 50)
        s.text(PAD + 14, y + 68, line, 12, 400, MUTED, maxw=MW - 2 * PAD - 28)
        progress(s, PAD + 14, y + 82, MW - 2 * PAD - 28, done / total if total else 0, color if done else LINE, h=6)
        s.text(PAD + 14, y + 106, foot, 12, 600, INK2, maxw=MW - 2 * PAD - 28)
    if target:
        s.link(PAD, y, MW - 2 * PAD, 118, target)

def m04_route_plans():
    s = phone("M4 My route journey plans", bg=BG, time="11:06")
    app_bar(s, "Route journey plans", back="m03", sub="Set by your branch manager, Moses Okello")
    filter_chips(s, [("All 3", True), ("Active 1", False), ("Next 1", False), ("Done 1", False)])
    y = 140
    for args in [("Week 40", "28 Sep – 2 Oct", "4 routes · Ntinda · Kiwatule", 131, 230, "131 of 230 prospects · 3 of 5 days",
                  "Active", STAGE["Prospect"], "m04a", True),
                 ("Week 41", "5 – 9 Oct", "5 routes · target 50 a day", 0, 250, "Target 250 prospects · starts Mon",
                  "Scheduled", STAGE["Prospect"], None, False),
                 ("Week 39", "21 – 25 Sep", "4 routes · Ntinda · Kiwatule", 218, 230, "218 of 230 prospects · 95%",
                  "Completed", GREEN, None, False)]:
        nm, dates, line, d, t, foot, st, col, tgt, hl = args
        plan_card(s, y, nm, dates, line, d, t, foot, st, col, tgt, hl)
        y += 128
    bottom_nav(s, "Home")
    return s

def m21_lead_plans():
    s = phone("M21 My lead journey plans", bg=BG, time="11:07")
    app_bar(s, "Lead journey plans", back="m20", sub="Set by your branch manager, Moses Okello")
    filter_chips(s, [("All 3", True), ("Active 1", False), ("Next 1", False), ("Done 1", False)])
    y = 140
    for args in [("Kiwatule leads", "28 Sep – 2 Oct", "12 leads from Sarah and Peter · goal 8 KYC", 7, 12,
                  "7 of 12 visited · 4 KYC completed", "Active", GREEN, "m21b", True),
                 ("Bukoto & Kyanja leads", "5 – 9 Oct", "8 leads from Esther and Ivan · goal 4 KYC", 0, 8,
                  "Starts Mon 5 Oct", "Scheduled", GREEN, None, False),
                 ("Ntinda leads", "21 – 25 Sep", "10 leads from Sarah · goal 5 KYC", 10, 10,
                  "10 of 10 visited · 6 KYC completed", "Completed", GREEN, None, False)]:
        nm, dates, line, d, t, foot, st, col, tgt, hl = args
        plan_card(s, y, nm, dates, line, d, t, foot, st, col, tgt, hl)
        y += 128
    with s.g("also assigned"):
        s.text(PAD, y + 12, "ALSO ASSIGNED TO YOU", 10.5, 700, MUTED, spacing=0.8)
        y += 22
        s.rect(PAD, y, MW - 2 * PAD, 52, fill=tint(BRAND, 0.06), rx=12)
        s.icon("route", PAD + 14, y + 16, 20, BRAND, 2)
        s.text(PAD + 44, y + 22, "Route journey plan · Fri 2 Oct", 13, 700, INK)
        s.text(PAD + 44, y + 39, "Kigoowa estates route · 30 prospects", 11.5, 400, MUTED)
    bottom_nav(s, "Plan", role="ro")
    return s


SCREENS = [m01_splash, m02_sign_in,
           m03_home, m04_route_plans, m04a_route_plan, m04b_prospect_map, m05_add_prospect, m06_prospects, m07_prospect, m07b_lead,
           m07c_lead_done, m08_not_interested, m17_leads, m19_me,
           m20_ro_home, m21_lead_plans, m21b_lead_plan,
           m09_hub, m09b_hub_kyc, m09c_hub_loan, m09d_hub_visits,
           m10_kyc_details, m11_kyc_id, m12_kyc_income, m13_validation, m09f_hub_kyc_done,
           m14_negotiation, m15_close, m16_success, m09e_hub_applied, m16b_check_out,
           m18_client, m18b_client_kyc, m18c_client_loan, m18d_client_visits, m23_ro_clients, m22_ro_me]
