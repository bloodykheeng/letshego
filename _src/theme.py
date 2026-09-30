"""Dark mode: derive a dark version of any generated screen by remapping its colours.

Light surfaces (page, cards, tints, borders) become dark surfaces; dark foregrounds (text, icons, chart
lines) become light. Saturated brand and status colours stay as they are, and a few colours are pinned in
KEEP because they sit on yellow or are already meant to be white.
"""
from __future__ import annotations

import colorsys
import re

KEEP = {
    "#FFFFFF",                                       # white text on coloured buttons
    "#1F1E57",                                       # BRAND_D: text and icons on yellow
    "#FFE45C", "#FBC805", "#FBD405", "#E9B800", "#FFE457",   # Letshego yellows
    "#231F0F", "#6B5A1E", "#0D5A34",                 # ink colours used on the yellow hero card
}
SURFACE = {
    "#FFFFFE": "#1D1E27",   # CARD: cards sit a step above the page
    "#F5F6FA": "#121319",   # BG (app)
    "#F6F7F9": "#121319",   # web page
    "#2F2E80": "#4F4CC9",   # BRAND as a fill: lift it so buttons read on dark
    "#FEF4BE": "#121319",   # the warm wash at the top of Home: no wash in dark mode
}

_TAG = re.compile(r"<(text|rect|circle|path|line|stop)\b[^>]*>")
_ATTR = re.compile(r'(fill|stroke|stop-color)="(#[0-9A-Fa-f]{6})"')


def _rgb(c):
    return tuple(int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))


def _hex(rgb):
    return "#%02X%02X%02X" % tuple(round(max(0.0, min(1.0, v)) * 255) for v in rgb)


def surface(c: str) -> str:
    c = c.upper()
    if c in KEEP:
        return c
    if c in SURFACE:
        return SURFACE[c]
    h, l, s = colorsys.rgb_to_hls(*_rgb(c))
    if l > 0.8:
        return _hex(colorsys.hls_to_rgb(h, 0.10 + (1 - l) * 0.9, s * 0.45))
    if l > 0.6 and s < 0.35:
        return _hex(colorsys.hls_to_rgb(h, 0.30, s * 0.5))
    return c


def foreground(c: str) -> str:
    c = c.upper()
    if c in KEEP:
        return c
    h, l, s = colorsys.rgb_to_hls(*_rgb(c))
    if l < 0.6:
        return _hex(colorsys.hls_to_rgb(h, min(0.92, 0.95 - l * 0.6), min(s, 0.75)))
    return c


def dark_svg(svg: str) -> str:
    def element(m):
        tag, src = m.group(1), m.group(0)

        def attr(a):
            name, col = a.group(1), a.group(2)
            if tag == "text" and name == "fill":
                new = foreground(col)
            elif name == "stroke":
                light = colorsys.rgb_to_hls(*_rgb(col.upper()))[1] > 0.8
                new = surface(col) if light else foreground(col)
            else:
                new = surface(col)
            return f'{name}="{new}"'

        return _ATTR.sub(attr, src)

    return _TAG.sub(element, svg)
