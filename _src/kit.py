"""SVG kit for the Letshego Field Sales mockups.

Every screen is plain SVG that Adobe XD imports as editable layers: rects, paths,
circles and live text. Group ids become XD layer names. Text is always emitted
left-anchored, with widths measured against the installed Segoe UI fonts, so
right-aligned and centred text lands correctly even where an importer ignores
text-anchor.
"""
from __future__ import annotations

import re
from contextlib import contextmanager
from xml.sax.saxutils import escape

from PIL import ImageFont

FONT_FAMILY = "Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
FONT_FILES = {
    300: "C:/Windows/Fonts/segoeuisl.ttf",
    400: "C:/Windows/Fonts/segoeui.ttf",
    600: "C:/Windows/Fonts/seguisb.ttf",
    700: "C:/Windows/Fonts/segoeuib.ttf",
    800: "C:/Windows/Fonts/seguibl.ttf",
}
# Bold italic is only used for the Letshego wordmark, which is set in a heavy italic.
ITALIC_FILES = {700: "C:/Windows/Fonts/segoeuiz.ttf", 800: "C:/Windows/Fonts/seguibli.ttf",
                400: "C:/Windows/Fonts/segoeuii.ttf"}
_font_cache: dict = {}


def tw(text: str, size: float, weight: int = 400, italic: bool = False) -> float:
    key = (size, weight, italic)
    if key not in _font_cache:
        path = ITALIC_FILES[weight] if italic else FONT_FILES[weight]
        _font_cache[key] = ImageFont.truetype(path, int(round(size * 4)))
    return _font_cache[key].getlength(text) / 4


def wrap(text: str, maxw: float, size: float, weight: int = 400) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, size, weight) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- palette
# Letshego brand, sampled from the LetsGo app: deep indigo + signal yellow, faceted triangle mark.
INK = "#1B1C3A"
INK2 = "#4B4D6B"
MUTED = "#7D8099"
FAINT = "#AAACC0"
LINE = "#E4E5EF"
LINE2 = "#EFF0F6"
BG = "#F5F6FA"
CARD = "#FFFFFF"

BRAND = "#2F2E80"      # Letshego indigo
BRAND_D = "#1F1E57"
BRAND_M = "#4744A8"
YELLOW = "#FBD405"     # Letshego yellow
YELLOW_D = "#8C6A00"   # readable text on yellow tints
GREEN = "#15925A"      # success / conversion
GREEN_D = "#0E6B41"
AMBER = "#E39A0B"
AMBER_D = "#9A6300"
RED = "#D14343"
BLUE = "#2F6FDB"
VIOLET = "#7056D6"
TEAL = "#0E8C99"

# Client journey, from the whiteboard session (29 Sep 2026). Order matters.
STAGES = [
    ("Visited", "#8A8DA6"),
    ("Interested", BLUE),
    ("KYC captured", VIOLET),
    ("KYC validated", TEAL),
    ("Negotiation", AMBER),
    ("Applied", GREEN),          # = successful conversion
]
STAGE = dict(STAGES)

STATUS = {
    "Approved": "#15925A",
    "Applied": "#15925A",
    "Converted": "#15925A",
    "Submitted": BLUE,
    "Awaiting approval": "#B7791F",
    "Under review": "#B7791F",
    "Returned": "#D9651B",
    "Rejected": "#C2362F",
    "Not interested": "#C2362F",
    "Declined": "#C2362F",
    "Overdue": "#C2362F",
    "Silent": "#C2362F",
    "Draft": "#7D8099",
    "Planned": "#7D8099",
    "Synced": "#15925A",
    "Queued": "#B7791F",
    "On track": "#15925A",
    "At risk": "#B7791F",
    "Behind": "#C2362F",
    "Active": "#15925A",
    "Left": "#7D8099",
    "Leaving today": "#D9651B",
    "Scheduled": BLUE,
    "Completed": "#0E8C99",
    "Visited": "#15925A",
    "Due today": "#B7791F",
    "Not yet due": "#8A8DA6",
    "Pending approval": "#B7791F",
    "Verified": "#15925A",
    "Follow-up": BLUE,
    **STAGE,
}

# Illustrative loan products. The real catalogue is confirmed with Letshego at kickoff.
PRODUCTS = [
    ("Civil Servant Loan", "Payroll check-off", BRAND),
    ("MSE Business Loan", "Micro & small enterprise", TEAL),
    ("School Fees Loan", "Education", VIOLET),
    ("Home Improvement Loan", "Housing", AMBER),
    ("Agri Asset Loan", "Farm equipment & inputs", GREEN),
]
PRODUCT = {p[0]: p[2] for p in PRODUCTS}


def tint(hex_color: str, a: float) -> str:
    """Blend a colour over white: a=1 is the colour, a=0 is white."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(255 - (255 - c) * a) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def shade(hex_color: str, a: float) -> str:
    """Darken a colour: a=0 unchanged, a=1 black."""
    h = hex_color.lstrip("#")
    r, g, b = (round(int(h[i : i + 2], 16) * (1 - a)) for i in (0, 2, 4))
    return f"#{r:02X}{g:02X}{b:02X}"


# ---------------------------------------------------------------- icons (24px grid, stroke)
ICONS: dict[str, list[str]] = {
    "grid": ["M4 3h6a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z",
             "M14 3h6a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z",
             "M14 12h6a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-6a1 1 0 0 1-1-1v-7a1 1 0 0 1 1-1z",
             "M4 16h6a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1z"],
    "target": ["M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z", "M12 6a6 6 0 1 0 0 12 6 6 0 1 0 0-12z",
               "M12 10a2 2 0 1 0 0 4 2 2 0 1 0 0-4z"],
    "file": ["M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z", "M14 2v6h6", "M16 13H8",
             "M16 17H8", "M10 9H8"],
    "sprout": ["M7 20h10", "M10 20c5.5-2.5.8-6.4 3-10",
               "M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z",
               "M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"],
    "radar": ["M12 2l7.07 2.93L22 12l-2.93 7.07L12 22l-7.07-2.93L2 12l2.93-7.07z",
              "M12 7l3.5 1.5L17 12l-1.5 3.5L12 17l-3.5-1.5L7 12l1.5-3.5z", "M12 2v20", "M2 12h20"],
    "map": ["M14.1 5.55a2 2 0 0 0 1.8 0l3.65-1.83A1 1 0 0 1 21 4.62v12.76a1 1 0 0 1-.55.9l-4.55 2.27a2 2 0 0 1-1.8 0l-4.2-2.1a2 2 0 0 0-1.8 0l-3.65 1.83A1 1 0 0 1 3 19.38V6.62a1 1 0 0 1 .55-.9l4.55-2.27a2 2 0 0 1 1.8 0z",
            "M15 5.76v15", "M9 3.24v15"],
    "book": ["M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"],
    "users": ["M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2", "M9 3a4 4 0 1 0 0 8 4 4 0 1 0 0-8z",
              "M22 21v-2a4 4 0 0 0-3-3.87", "M16 3.13a4 4 0 0 1 0 7.75"],
    "user": ["M12 3a5 5 0 1 0 0 10 5 5 0 1 0 0-10z", "M20 21a8 8 0 0 0-16 0"],
    "sliders": ["M4 21v-7", "M4 10V3", "M12 21v-9", "M12 8V3", "M20 21v-5", "M20 12V3", "M1 14h6",
                "M9 8h6", "M17 16h6"],
    "bell": ["M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9", "M10.3 21a1.94 1.94 0 0 0 3.4 0"],
    "search": ["M11 3a8 8 0 1 0 0 16 8 8 0 1 0 0-16z", "M21 21l-4.3-4.3"],
    "upload": ["M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4", "M17 8l-5-5-5 5", "M12 3v12"],
    "download": ["M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4", "M7 10l5 5 5-5", "M12 15V3"],
    "camera": ["M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3z",
               "M12 10a3 3 0 1 0 0 6 3 3 0 1 0 0-6z"],
    "pin": ["M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z", "M12 7a3 3 0 1 0 0 6 3 3 0 1 0 0-6z"],
    "check": ["M20 6L9 17l-5-5"],
    "x": ["M18 6L6 18", "M6 6l12 12"],
    "alert": ["M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z",
              "M12 9v4", "M12 17h.01"],
    "clock": ["M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z", "M12 6v6l4 2"],
    "wifioff": ["M2 2l20 20", "M8.5 16.5a5 5 0 0 1 7 0", "M2 8.82a15 15 0 0 1 4.17-2.65",
                "M10.66 5c4.01-.36 8.14.9 11.34 3.76", "M16.85 11.25a10 10 0 0 1 2.22 1.68",
                "M5 13a10 10 0 0 1 5.24-2.76", "M12 20h.01"],
    "wifi": ["M5 12.55a11 11 0 0 1 14.08 0", "M1.42 9a16 16 0 0 1 21.16 0", "M8.53 16.11a6 6 0 0 1 6.95 0",
             "M12 20h.01"],
    "refresh": ["M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8", "M3 3v5h5",
                "M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16", "M16 16h5v5"],
    "filter": ["M22 3H2l8 9.46V19l4 2v-8.54z"],
    "chevdown": ["M6 9l6 6 6-6"],
    "chevright": ["M9 18l6-6-6-6"],
    "chevleft": ["M15 18l-6-6 6-6"],
    "plus": ["M12 5v14", "M5 12h14"],
    "link": ["M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71",
             "M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"],
    "lock": ["M5 11h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2z",
             "M7 11V7a5 5 0 0 1 10 0v4"],
    "shield": ["M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z", "M9 12l2 2 4-4"],
    "layers": ["M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z",
               "M22 17.65l-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65", "M22 12.65l-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"],
    "sun": ["M12 8a4 4 0 1 0 0 8 4 4 0 1 0 0-8z", "M12 2v2", "M12 20v2", "M4.93 4.93l1.41 1.41",
            "M17.66 17.66l1.41 1.41", "M2 12h2", "M20 12h2", "M6.34 17.66l-1.41 1.41", "M19.07 4.93l-1.41 1.41"],
    "zap": ["M13 2L3 14h9l-1 8 10-12h-9z"],
    "message": ["M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"],
    "eye": ["M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z", "M12 9a3 3 0 1 0 0 6 3 3 0 1 0 0-6z"],
    "send": ["M22 2l-7 20-4-9-9-4z", "M22 2L11 13"],
    "image": ["M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z",
              "M9 7a2 2 0 1 0 0 4 2 2 0 1 0 0-4z", "M21 15l-3.09-3.09a2 2 0 0 0-2.83 0L6 21"],
    "clip": ["M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"],
    "calendar": ["M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z", "M16 2v4",
                 "M8 2v4", "M3 10h18"],
    "bars": ["M3 3v18h18", "M18 17V9", "M13 17V5", "M8 17v-3"],
    "globe": ["M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z", "M2 12h20",
              "M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"],
    "menu": ["M4 6h16", "M4 12h16", "M4 18h16"],
    "arrowright": ["M5 12h14", "M12 5l7 7-7 7"],
    "arrowleft": ["M19 12H5", "M12 19l-7-7 7-7"],
    "arrowupright": ["M7 17L17 7", "M7 7h10v10"],
    "database": ["M12 2c5 0 9 1.34 9 3s-4 3-9 3-9-1.34-9-3 4-3 9-3z", "M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5",
                 "M3 12c0 1.66 4 3 9 3s9-1.34 9-3"],
    "home": ["M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z", "M9 22V12h6v10"],
    "listcheck": ["M3 17l2 2 4-4", "M3 7l2 2 4-4", "M13 6h8", "M13 12h8", "M13 18h8"],
    "folder": ["M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2z"],
    "flag": ["M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z", "M4 22v-7"],
    "crosshair": ["M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z", "M22 12h-4", "M6 12H2", "M12 6V2", "M12 22v-4"],
    "mic": ["M12 2a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3z", "M19 10v2a7 7 0 0 1-14 0v-2", "M12 19v3"],
    "history": ["M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8", "M3 3v5h5", "M12 7v5l4 2"],
    "coins": ["M8 2a6 6 0 1 0 0 12 6 6 0 1 0 0-12z", "M18.09 10.37A6 6 0 1 1 10.34 18", "M7 6h1v4",
              "M16.71 13.88l.7.71-2.82 2.82"],
    "workflow": ["M4 3h4a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z",
                 "M16 15h4a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1v-4a1 1 0 0 1 1-1z",
                 "M7 9v4a2 2 0 0 0 2 2h6"],
    "sparkle": ["M12 3l1.9 5.8a2 2 0 0 0 1.3 1.3L21 12l-5.8 1.9a2 2 0 0 0-1.3 1.3L12 21l-1.9-5.8a2 2 0 0 0-1.3-1.3L3 12l5.8-1.9a2 2 0 0 0 1.3-1.3z"],
    "logout": ["M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4", "M16 17l5-5-5-5", "M21 12H9"],
    "more": ["M12 12h.01", "M19 12h.01", "M5 12h.01"],
    "edit": ["M12 20h9", "M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"],
    "copy": ["M10 8h10a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2V10a2 2 0 0 1 2-2z",
             "M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"],
    "fingerprint": ["M2 12C2 6.5 6.5 2 12 2a10 10 0 0 1 8 4", "M5 19.5C5.5 18 6 15 6 12c0-.7.12-1.37.34-2",
                    "M17.29 21.02c.12-.6.43-2.3.5-3.02", "M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4",
                    "M8.65 22c.21-.66.45-1.32.57-2", "M14 13.12c0 2.38 0 6.38-1 8.88",
                    "M2 16h.01", "M21.8 16c.2-2 .131-5.354 0-6", "M9 6.8a6 6 0 0 1 9 5.2c0 .47 0 1.17-.02 2"],
    "phone": ["M7 2h10a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z", "M12 18h.01"],
    "api": ["M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5c0 1.1.9 2 2 2h1",
            "M16 21h1a2 2 0 0 0 2-2v-5c0-1.1.9-2 2-2a2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1"],
    "idcard": ["M4 5h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z",
               "M8 9a2 2 0 1 0 0 4 2 2 0 1 0 0-4z", "M5 16.5c.6-1.5 1.7-2.2 3-2.2s2.4.7 3 2.2", "M14 10h5", "M14 14h3"],
    "wallet": ["M19 7V5a2 2 0 0 0-2-2H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2",
               "M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"],
    "briefcase": ["M4 7h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2z",
                  "M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"],
    "route": ["M6 16a3 3 0 1 0 0 6 3 3 0 1 0 0-6z", "M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15",
              "M18 2a3 3 0 1 0 0 6 3 3 0 1 0 0-6z"],
    "navigation": ["M3 11l19-9-9 19-2-8z"],
    "trophy": ["M6 9H4.5a2.5 2.5 0 0 1 0-5H6", "M18 9h1.5a2.5 2.5 0 0 0 0-5H18", "M4 22h16",
               "M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22", "M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22",
               "M18 2H6v7a6 6 0 0 0 12 0V2z"],
    "handshake": ["M11 17l2 2a1 1 0 1 0 3-3", "M14 14l2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4",
                  "M21 3l1 11h-2", "M3 3L2 14l6.5 6.5a1 1 0 1 0 3-3", "M3 4h8"],
    "scan": ["M3 7V5a2 2 0 0 1 2-2h2", "M17 3h2a2 2 0 0 1 2 2v2", "M21 17v2a2 2 0 0 1-2 2h-2",
             "M7 21H5a2 2 0 0 1-2-2v-2", "M7 12h10"],
    "banknote": ["M4 6h16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2z",
                 "M12 10a2 2 0 1 0 0 4 2 2 0 1 0 0-4z", "M6 12h.01", "M18 12h.01"],
    "userx": ["M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2", "M9 3a4 4 0 1 0 0 8 4 4 0 1 0 0-8z", "M17 8l5 5", "M22 8l-5 5"],
    "usercheck": ["M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2", "M9 3a4 4 0 1 0 0 8 4 4 0 1 0 0-8z", "M16 11l2 2 4-4"],
    "userplus": ["M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2", "M9 3a4 4 0 1 0 0 8 4 4 0 1 0 0-8z", "M19 8v6", "M22 11h-6"],
    "trendup": ["M22 7l-8.5 8.5-5-5L2 17", "M16 7h6v6"],
    "trenddown": ["M22 17l-8.5-8.5-5 5L2 7", "M16 17h6v-6"],
    "activity": ["M22 12h-4l-3 9L9 3l-3 9H2"],
    "star": ["M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"],
    "swap": ["M16 3l4 4-4 4", "M20 7H4", "M8 21l-4-4 4-4", "M4 17h16"],
    "gauge": ["M12 14l4-4", "M3.34 19a10 10 0 1 1 17.32 0"],
    "store": ["M3 9l1.5-5h15L21 9", "M4 9v11h16V9", "M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0", "M10 20v-5h4v5"],
    "school": ["M22 10L12 5 2 10l10 5 10-5z", "M6 12v5c3 3 9 3 12 0v-5"],
    "tractor": ["M7 18a3 3 0 1 0 0-.01z", "M18 18a2 2 0 1 0 0-.01z", "M4 15V7h7l2 5h5a2 2 0 0 1 2 2v2", "M10 18h6", "M8 7V4"],
    "hand": ["M18 11V6a2 2 0 0 0-4 0", "M14 10V4a2 2 0 0 0-4 0v2", "M10 10.5V6a2 2 0 0 0-4 0v8",
             "M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"],
    "smile": ["M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z", "M8 14s1.5 2 4 2 4-2 4-2", "M9 9h.01", "M15 9h.01"],
    "frown": ["M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z", "M16 16s-1.5-2-4-2-4 2-4 2", "M9 9h.01", "M15 9h.01"],
    "info": ["M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z", "M12 16v-4", "M12 8h.01"],
    "undo": ["M9 14L4 9l5-5", "M4 9h10.5a5.5 5.5 0 0 1 0 11H11"],
    "mail": ["M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z", "M22 6l-10 7L2 6"],
    "settings": ["M12 9a3 3 0 1 0 0 6 3 3 0 1 0 0-6z",
                 "M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"],
}


def _slug(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_-]+", "-", s).strip("-")
    return s or "layer"


class SVG:
    def __init__(self, w: int, h: int, title: str):
        self.w, self.h, self.title = w, h, title
        self.parts: list[str] = []
        self._ids: dict[str, int] = {}
        self.links: list[tuple] = []  # (x, y, w, h, target) hotspots for the clickable prototype
        self.soft = False      # phone screens: white bordered cards become soft-shadow cards
        self._shadow = False

    def link(self, x, y, w, h, target):
        if target:
            self.links.append((round(x, 1), round(y, 1), round(w, 1), round(h, 1), target))

    # ids become XD layer names; keep them unique and readable
    def _id(self, name: str | None) -> str:
        if not name:
            return ""
        base = _slug(name)
        n = self._ids.get(base, 0)
        self._ids[base] = n + 1
        return f' id="{base if n == 0 else f"{base}-{n + 1}"}"'

    def raw(self, s: str):
        self.parts.append(s)

    @contextmanager
    def g(self, name: str | None = None, transform: str | None = None, opacity: float | None = None):
        attrs = self._id(name)
        if transform:
            attrs += f' transform="{transform}"'
        if opacity is not None:
            attrs += f' opacity="{opacity}"'
        self.parts.append(f"<g{attrs}>")
        yield
        self.parts.append("</g>")

    def rect(self, x, y, w, h, fill=CARD, rx=0, stroke=None, sw=1, name=None, op=None, dash=None, shadow=None):
        if shadow is None:
            shadow = self.soft and fill in (CARD, "#FFFFFF") and stroke == LINE and rx and rx >= 10
        if shadow:
            self._shadow = True
            stroke = None if stroke == LINE else stroke
        a = f'x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{max(h, 0):.1f}"'
        if rx:
            a += f' rx="{rx}"'
        a += f' fill="{fill}"'
        if shadow:
            a += ' filter="url(#soft)"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if op is not None:
            a += f' fill-opacity="{op}"'
        self.parts.append(f"<rect{self._id(name)} {a}/>")

    def circle(self, cx, cy, r, fill=CARD, stroke=None, sw=1, name=None, op=None, shadow=False):
        a = f'cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"'
        if shadow:
            self._shadow = True
            a += ' filter="url(#soft)"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if op is not None:
            a += f' fill-opacity="{op}"'
        self.parts.append(f"<circle{self._id(name)} {a}/>")

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1, dash=None, name=None, cap=None):
        a = f'x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if cap:
            a += f' stroke-linecap="{cap}"'
        self.parts.append(f"<line{self._id(name)} {a}/>")

    def path(self, d, fill="none", stroke=None, sw=1, name=None, op=None, sop=None, dash=None, join="round",
             cap="round"):
        a = f'd="{d}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="{join}" stroke-linecap="{cap}"'
        if op is not None:
            a += f' fill-opacity="{op}"'
        if sop is not None:
            a += f' stroke-opacity="{sop}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.parts.append(f"<path{self._id(name)} {a}/>")

    def poly(self, pts, fill="none", stroke=None, sw=1, name=None, op=None, closed=True, dash=None):
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if closed else "")
        self.path(d, fill=fill, stroke=stroke, sw=sw, name=name, op=op, dash=dash)

    def text(self, x, y, s, size=14, weight=400, fill=INK, anchor="start", name=None, op=None,
             spacing: float | None = None, maxw: float | None = None, italic: bool = False):
        s = str(s)
        if maxw and tw(s, size, weight, italic) > maxw:
            while s and tw(s + "…", size, weight, italic) > maxw:
                s = s[:-1]
            s = s.rstrip() + "…"
        w = tw(s, size, weight, italic) + (spacing or 0) * max(len(s) - 1, 0)
        if anchor == "end":
            x -= w
        elif anchor == "middle":
            x -= w / 2
        a = (f'x="{x:.1f}" y="{y:.1f}" font-family="{FONT_FAMILY}" font-size="{size}" '
             f'font-weight="{weight}" fill="{fill}"')
        if italic:
            a += ' font-style="italic"'
        if spacing:
            a += f' letter-spacing="{spacing}"'
        if op is not None:
            a += f' fill-opacity="{op}"'
        self.parts.append(f"<text{self._id(name or s[:28])} {a}>{escape(s)}</text>")
        return w

    def para(self, x, y, s, maxw, size=14, weight=400, fill=INK2, lh=None, max_lines=None, name=None):
        lh = lh or round(size * 1.5)
        lines = wrap(s, maxw, size, weight)
        if max_lines and len(lines) > max_lines:
            lines = lines[:max_lines]
            last = lines[-1]
            while last and tw(last + "…", size, weight) > maxw:
                last = last[:-1]
            lines[-1] = last.rstrip() + "…"
        with self.g(name or ("para " + s[:20])):
            for i, ln in enumerate(lines):
                self.text(x, y + i * lh, ln, size, weight, fill, name="line")
        return len(lines) * lh

    def icon(self, name, x, y, size=20, color=INK2, sw=1.8):
        s = size / 24
        with self.g(f"icon {name}", transform=f"translate({x:.1f} {y:.1f}) scale({s:.4f})"):
            for d in ICONS[name]:
                self.parts.append(
                    f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw / s:.2f}" '
                    f'stroke-linecap="round" stroke-linejoin="round"/>'
                )

    def svg(self) -> str:
        body = "\n".join(self.parts)
        defs = ('<defs><filter id="soft" x="-20%" y="-20%" width="140%" height="170%">'
                '<feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="#1B1C3A" flood-opacity="0.07"/>'
                '</filter></defs>\n') if self._shadow else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}">\n<title>{escape(self.title)}</title>\n{defs}{body}\n</svg>\n')

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.svg())


# ---------------------------------------------------------------- components
def chip(s: SVG, x, y, label, color, h=24, size=12, weight=600, solid=False, icon=None, dot=False, name=None):
    """Pill label. Returns its width."""
    pad = 10
    iw = 14 if icon else (8 if dot else 0)
    gap = 6 if (icon or dot) else 0
    w = pad * 2 + iw + gap + tw(label, size, weight)
    with s.g(name or f"chip {label}"):
        s.rect(x, y, w, h, fill=color if solid else tint(color, 0.12), rx=h / 2)
        fg = "#FFFFFF" if solid else shade(color, 0.12)
        cx = x + pad
        if icon:
            s.icon(icon, cx, y + (h - 14) / 2, 14, fg, 2)
        elif dot:
            s.circle(cx + 4, y + h / 2, 4, fill=color if not solid else "#FFFFFF")
        s.text(cx + iw + gap, y + h / 2 + size * 0.36, label, size, weight, fg)
    return w


def status_chip(s: SVG, x, y, status, h=24, size=12):
    return chip(s, x, y, status, STATUS.get(status, MUTED), h=h, size=size, dot=True)


def button(s: SVG, x, y, label, kind="primary", icon=None, h=40, size=14, w=None, anchor="start", color=BRAND):
    pad = 16
    iw = 18 if icon else 0
    gap = 8 if icon and label else 0
    bw = w or (pad * 2 + iw + gap + (tw(label, size, 600) if label else 0))
    if anchor == "end":
        x -= bw
    if kind == "primary":
        bg, fg, st = color, "#FFFFFF", None
    elif kind == "danger":
        bg, fg, st = CARD, STATUS["Returned"], tint(STATUS["Returned"], 0.5)
    elif kind == "ghost":
        bg, fg, st = "none", color, None
    elif kind == "soft":
        bg, fg, st = tint(color, 0.1), shade(color, 0.05), None
    else:
        bg, fg, st = CARD, INK, LINE
    with s.g(f"button {label or icon}"):
        s.rect(x, y, bw, h, fill=bg, rx=12 if s.soft else 8, stroke=st, shadow=False)
        content = iw + gap + (tw(label, size, 600) if label else 0)
        cx = x + (bw - content) / 2
        if icon:
            s.icon(icon, cx, y + (h - 18) / 2, 18, fg, 2)
        if label:
            s.text(cx + iw + gap, y + h / 2 + size * 0.36, label, size, 600, fg)
    return bw


def card(s: SVG, x, y, w, h, title=None, subtitle=None, name=None, action=None, fill=CARD, border=LINE):
    s.rect(x, y, w, h, fill=fill, rx=12, stroke=border, name=(name or title or "card") + " bg")
    if title:
        s.text(x + 24, y + 38, title, 17, 600, INK, name="title")
        if subtitle:
            s.text(x + 24, y + 60, subtitle, 13, 400, MUTED, name="subtitle", maxw=w - 48 - (tw(action, 13, 600) + 30 if action else 0))
        if action:
            s.text(x + w - 24, y + 38, action, 13, 600, BRAND, anchor="end", name="card action")
    return x + 24, y + (80 if subtitle else 60) if title else y + 24


def progress(s: SVG, x, y, w, frac, color=BRAND, h=8, bg=LINE2, marker=None, name="progress"):
    with s.g(name):
        s.rect(x, y, w, h, fill=bg, rx=h / 2)
        if frac > 0:
            s.rect(x, y, max(w * min(frac, 1), h), h, fill=color, rx=h / 2)
        if marker is not None:
            mx = x + w * marker
            s.rect(mx - 1.5, y - 4, 3, h + 8, fill=INK, rx=1.5)


def avatar(s: SVG, cx, cy, r, initials, color=BRAND):
    with s.g(f"avatar {initials}"):
        s.circle(cx, cy, r, fill=tint(color, 0.16))
        s.text(cx, cy + r * 0.36, initials, r * 0.8, 600, shade(color, 0.1), anchor="middle")


def checkbox(s: SVG, x, y, checked=False, size=18, color=BRAND):
    with s.g("checkbox"):
        if checked:
            s.rect(x, y, size, size, fill=color, rx=4)
            s.icon("check", x + 2, y + 2, size - 4, "#FFFFFF", 3)
        else:
            s.rect(x, y, size, size, fill=CARD, rx=4, stroke="#C4C7D6", sw=1.5)


def radio(s: SVG, cx, cy, on=False, r=9, color=BRAND):
    with s.g("radio"):
        s.circle(cx, cy, r, fill=CARD, stroke=color if on else "#C4C7D6", sw=1.8)
        if on:
            s.circle(cx, cy, r - 4.5, fill=color)


def toggle(s: SVG, x, y, on=True, color=BRAND):
    with s.g("toggle"):
        s.rect(x, y, 36, 20, fill=color if on else "#CBCEDD", rx=10)
        s.circle(x + (26 if on else 10), y + 10, 7.5, fill="#FFFFFF")


def field(s: SVG, x, y, w, label, value="", h=44, placeholder=False, icon=None, suffix=None, required=False,
          error=None, ok=None, dropdown=False, size=14, focus=False):
    """Form field with label above. Returns total height used."""
    with s.g(f"field {label}"):
        lw = s.text(x, y + 14, label, 13, 600, INK2, name="label")
        if required:
            s.text(x + lw + 4, y + 14, "*", 13, 600, STATUS["Rejected"], name="required")
        by = y + 22
        border = STATUS["Rejected"] if error else (BRAND if focus else "#CDD0DE")
        s.rect(x, by, w, h, fill=CARD, rx=12 if s.soft else 8, stroke=border, sw=1.5 if (error or focus) else 1,
               name="input", shadow=False)
        tx = x + 14
        if icon:
            s.icon(icon, x + 12, by + (h - 18) / 2, 18, MUTED)
            tx = x + 40
        rpad = 14 + (24 if dropdown else 0) + (tw(suffix, 13) + 10 if suffix else 0)
        s.text(tx, by + h / 2 + size * 0.36, value, size, 400, FAINT if placeholder else INK, name="value",
               maxw=w - (tx - x) - rpad)
        if dropdown:
            s.icon("chevdown", x + w - 32, by + (h - 18) / 2, 18, MUTED)
        if suffix:
            s.text(x + w - 14 - (24 if dropdown else 0), by + h / 2 + 4.5, suffix, 13, 400, MUTED, anchor="end",
                   name="suffix")
        total = 22 + h
        if error:
            s.icon("alert", x, by + h + 7, 14, STATUS["Rejected"], 2)
            s.text(x + 20, by + h + 19, error, 12, 400, STATUS["Rejected"], name="error")
            total += 24
        elif ok:
            s.icon("check", x, by + h + 7, 14, STATUS["Approved"], 2.4)
            s.text(x + 20, by + h + 19, ok, 12, 400, STATUS["Approved"], name="hint")
            total += 24
    return total


def table(s: SVG, x, y, cols, rows, row_h=52, head_h=40, zebra=False, name="table", size=13, hl=None):
    """cols: [(label, width, align)]. rows: list of lists; a cell is str or callable(s, x, y, w, h)."""
    with s.g(name):
        tot = sum(c[1] for c in cols)
        s.rect(x, y, tot, head_h, fill="#F7F8FB", name="header bg")
        cx = x
        for label, w, align in cols:
            if align == "end":
                s.text(cx + w - 16, y + head_h / 2 + 4, label.upper(), 11, 600, MUTED, anchor="end", spacing=0.6)
            else:
                s.text(cx + 16, y + head_h / 2 + 4, label.upper(), 11, 600, MUTED, spacing=0.6)
            cx += w
        ry = y + head_h
        for i, row in enumerate(rows):
            with s.g(f"row {i + 1}"):
                if hl is not None and i == hl:
                    s.rect(x, ry, tot, row_h, fill=tint(BRAND, 0.06))
                elif zebra and i % 2:
                    s.rect(x, ry, tot, row_h, fill="#FAFBFD")
                s.line(x, ry, x + tot, ry, LINE2)
                cx = x
                for (label, w, align), cell in zip(cols, row):
                    if callable(cell):
                        cell(s, cx, ry, w, row_h)
                    elif cell is not None:
                        if align == "end":
                            s.text(cx + w - 16, ry + row_h / 2 + 4.5, cell, size, 400, INK, anchor="end")
                        else:
                            s.text(cx + 16, ry + row_h / 2 + 4.5, cell, size, 400, INK, maxw=w - 24)
                    cx += w
                ry += row_h
        return ry


def triangle(s: SVG, x, y, size=36, name="letshego triangle"):
    """Letshego's faceted yellow triangle (apex up), drawn from three facets."""
    k = size / 36
    ax, ay = x + 19 * k, y + 2 * k          # apex
    lx, ly = x + 1 * k, y + 33 * k          # bottom left
    rx_, ry = x + 35 * k, y + 33 * k        # bottom right
    cx, cy = x + 21 * k, y + 23 * k         # inner fold
    with s.g(name):
        s.poly([(ax, ay), (lx, ly), (cx, cy)], fill="#FBD405")
        s.poly([(ax, ay), (cx, cy), (rx_, ry)], fill="#E9B800")
        s.poly([(lx, ly), (cx, cy), (rx_, ry)], fill="#FFE457")


def logo_mark(s: SVG, x, y, size=36, bg=BRAND):
    """App icon: the triangle on an indigo tile."""
    k = size / 36
    with s.g("logo mark"):
        s.rect(x, y, size, size, fill=bg, rx=9 * k)
        triangle(s, x + 7 * k, y + 6 * k, 22 * k)


def wordmark(s: SVG, x, y, size=24, color=INK, anchor="start", mark=True):
    """Triangle + 'Letshego' in heavy italic. y is the text baseline. Returns total width."""
    gap = size * 0.28
    mw = size * 1.2 if mark else 0
    w = mw + (gap if mark else 0) + tw("Letshego", size, 700, True)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    with s.g("letshego wordmark"):
        if mark:
            triangle(s, x, y - size * 1.02, mw)
        s.text(x + mw + (gap if mark else 0), y, "Letshego", size, 700, color, italic=True, name="Letshego")
    return w


def para(s: SVG, x, y, text, maxw, size=14, weight=400, fill=INK2, lh=None, max_lines=None, name=None):
    return s.para(x, y, text, maxw, size, weight, fill, lh, max_lines, name)
