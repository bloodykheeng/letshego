"""Charts, the Uganda branch map and a stylised street map, drawn as plain SVG shapes."""
from __future__ import annotations

import json
import math
import os
import random

from kit import (BRAND, BRAND_D, CARD, FAINT, GREEN, INK, INK2, LINE, LINE2, MUTED, RED, SVG, YELLOW, shade, tint,
                 tw)

# Uganda district boundaries (UBOS, 137 districts), copied from the SNV prototype so the repo builds on its own.
BOUNDARIES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "districts.geojson")

# Illustrative branch network: branch -> (district, region, agents, Q3 conversions, Q3 target)
BRANCHES = {
    "Kampala Central": ("Kampala", "Central", 9, 214, 240),
    "Kampala East": ("Wakiso", "Central", 7, 131, 190),
    "Mukono": ("Mukono", "Central", 5, 92, 120),
    "Masaka": ("Masaka", "Central", 4, 71, 96),
    "Jinja": ("Jinja", "Eastern", 5, 88, 110),
    "Mbale": ("Mbale", "Eastern", 4, 64, 96),
    "Soroti": ("Soroti", "Eastern", 3, 29, 72),
    "Lira": ("Lira", "Northern", 4, 58, 84),
    "Gulu": ("Gulu", "Northern", 4, 61, 84),
    "Arua": ("Arua", "Northern", 3, 22, 60),
    "Hoima": ("Hoima", "Western", 3, 39, 60),
    "Fort Portal": ("Kabarole", "Western", 3, 47, 60),
    "Mbarara": ("Mbarara", "Western", 5, 101, 110),
    "Kabale": ("Kabale", "Western", 3, 34, 60),
}
BRANCH_DISTRICTS = {v[0]: k for k, v in BRANCHES.items()}


def perf_color(frac):
    if frac >= 0.85:
        return GREEN
    if frac >= 0.6:
        return "#E39A0B"
    return RED


# ---------------------------------------------------------------- donut
def arc_path(cx, cy, r_out, r_in, a0, a1):
    large = 1 if a1 - a0 > math.pi else 0
    x0, y0 = cx + r_out * math.cos(a0), cy + r_out * math.sin(a0)
    x1, y1 = cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)
    x2, y2 = cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)
    x3, y3 = cx + r_in * math.cos(a0), cy + r_in * math.sin(a0)
    return (f"M{x0:.2f} {y0:.2f} A{r_out} {r_out} 0 {large} 1 {x1:.2f} {y1:.2f} "
            f"L{x2:.2f} {y2:.2f} A{r_in} {r_in} 0 {large} 0 {x3:.2f} {y3:.2f} Z")


def donut(s: SVG, cx, cy, r, thick, parts, gap=0.025, name="donut"):
    """parts: [(value, color, label)]"""
    tot = sum(p[0] for p in parts)
    a = -math.pi / 2
    with s.g(name):
        for v, color, label in parts:
            da = 2 * math.pi * v / tot
            s.path(arc_path(cx, cy, r, r - thick, a + gap / 2, a + da - gap / 2), fill=color, name=label)
            a += da


def ring(s: SVG, cx, cy, r, thick, frac, color, bg=LINE2, name="progress ring"):
    """Progress ring starting at 12 o'clock."""
    with s.g(name):
        s.circle(cx, cy, r - thick / 2, fill="none", stroke=bg, sw=thick)
        if frac > 0:
            a0 = -math.pi / 2
            a1 = a0 + 2 * math.pi * min(frac, 0.9999)
            rr = r - thick / 2
            x0, y0 = cx + rr * math.cos(a0), cy + rr * math.sin(a0)
            x1, y1 = cx + rr * math.cos(a1), cy + rr * math.sin(a1)
            large = 1 if a1 - a0 > math.pi else 0
            s.path(f"M{x0:.2f} {y0:.2f} A{rr} {rr} 0 {large} 1 {x1:.2f} {y1:.2f}", stroke=color, sw=thick)


# ---------------------------------------------------------------- line / bars
def line_chart(s: SVG, x, y, w, h, series, xlabels, y_max, y_step, fmt=lambda v: f"{v:,.0f}", name="line chart",
               dots=True):
    """series: [(values, color, label, area)]"""
    with s.g(name):
        steps = int(y_max / y_step)
        for k in range(steps + 1):
            yy = y + h - h * k / steps
            s.line(x + 44, yy, x + w, yy, LINE2 if k else LINE)
            s.text(x + 36, yy + 4, fmt(k * y_step), 11, 400, MUTED, anchor="end", name="y label")
        n = len(xlabels)
        px = lambda i: x + 44 + (w - 44) * (i + 0.5) / n
        for i, lb in enumerate(xlabels):
            if lb:
                s.text(px(i), y + h + 20, lb, 11, 400, MUTED, anchor="middle", name="x label")
        for vals, color, label, area in series:
            pts = [(px(i), y + h - h * v / y_max) for i, v in enumerate(vals) if v is not None]
            with s.g(f"series {label}"):
                if area:
                    d = f"M{pts[0][0]:.1f} {y + h:.1f} " + " ".join(f"L{a:.1f} {b:.1f}" for a, b in pts) + \
                        f" L{pts[-1][0]:.1f} {y + h:.1f} Z"
                    s.path(d, fill=color, op=0.12, name="area")
                s.poly(pts, stroke=color, sw=2.4, closed=False, name="line",
                       dash=None if area or "target" not in label.lower() and "last year" not in label.lower() else "6 5")
                if area and dots:
                    for a, b in pts:
                        s.circle(a, b, 3.5, fill=CARD, stroke=color, sw=2)
    return px


def sparkline(s: SVG, x, y, w, h, vals, color=BRAND, area=True, name="sparkline"):
    mx = max(vals) or 1
    n = len(vals)
    pts = [(x + w * i / (n - 1), y + h - h * v / mx) for i, v in enumerate(vals)]
    with s.g(name):
        if area:
            d = f"M{x:.1f} {y + h:.1f} " + " ".join(f"L{a:.1f} {b:.1f}" for a, b in pts) + f" L{x + w:.1f} {y + h:.1f} Z"
            s.path(d, fill=color, op=0.12)
        s.poly(pts, stroke=color, sw=1.8, closed=False)
        s.circle(*pts[-1], 2.8, fill=color)


def heat_strip(s: SVG, x, y, vals, cell=14, gap=3, color=BRAND, max_v=None, h=None, name="weekly activity"):
    """One cell per period; 0 = empty (red outline) so silent weeks stand out."""
    mx = max_v or max(vals) or 1
    h = h or cell
    with s.g(name):
        for i, v in enumerate(vals):
            cx = x + i * (cell + gap)
            if v is None:
                s.rect(cx, y, cell, h, fill=LINE2, rx=3)
            elif v == 0:
                s.rect(cx, y, cell, h, fill="#FDECEC", rx=3, stroke="#F3B4B4")
            else:
                s.rect(cx, y, cell, h, fill=color, op=0.18 + 0.82 * min(v / mx, 1), rx=3)
    return len(vals) * (cell + gap) - gap


def funnel(s: SVG, x, y, w, rows, row_h=46, gap=10, label_w=150, name="funnel"):
    """rows: [(label, value, color)]. Bars centred, with step conversion % between them."""
    top = rows[0][1]
    bw_max = w - label_w - 120
    with s.g(name):
        for i, (label, v, col) in enumerate(rows):
            yy = y + i * (row_h + gap)
            bw = max(bw_max * v / top, 36)
            bx = x + label_w + (bw_max - bw) / 2
            s.text(x, yy + row_h / 2 + 5, label, 13.5, 600, INK2, name="stage")
            s.rect(bx, yy, bw, row_h, fill=col, rx=8, name=f"bar {label}")
            vs = min(15, row_h * 0.5)
            if tw(f"{v:,}", vs, 700) + 16 < bw:
                s.text(bx + bw / 2, yy + row_h / 2 + vs * 0.38, f"{v:,}", vs, 700, "#FFFFFF", anchor="middle",
                       name="value")
            else:
                s.text(bx + bw + 8, yy + row_h / 2 + vs * 0.38, f"{v:,}", vs, 700, shade(col, 0.2), name="value")
            s.text(x + w, yy + row_h / 2 + 1, f"{v / top:.0%}", 14, 700, INK, anchor="end", name="of visits")
            s.text(x + w, yy + row_h / 2 + 17, "of visits", 10.5, 400, MUTED, anchor="end", name="of visits label")
            if i:
                prev = rows[i - 1][1]
                s.text(x + label_w + bw_max / 2 + bw / 2 + 12, yy - 1, f"↓ {v / prev:.0%}", 11, 600, MUTED,
                       name="step conversion")


# ---------------------------------------------------------------- Uganda map
def _rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1e-9
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i]
        d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return _rdp(pts[: idx + 1], eps)[:-1] + _rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


_geo = None


def _load():
    global _geo
    if _geo is None:
        with open(BOUNDARIES, encoding="utf-8") as f:
            _geo = json.load(f)["features"]
    return _geo


class UgandaMap:
    LON0, LON1, LAT0, LAT1 = 29.55, 35.02, -1.50, 4.25

    def __init__(self, x, y, w, h, pad=8):
        self.x, self.y = x, y
        sx = (w - 2 * pad) / (self.LON1 - self.LON0)
        sy = (h - 2 * pad) / (self.LAT1 - self.LAT0)
        self.k = min(sx, sy)
        mw = (self.LON1 - self.LON0) * self.k
        mh = (self.LAT1 - self.LAT0) * self.k
        self.ox = x + (w - mw) / 2
        self.oy = y + (h - mh) / 2
        self.districts = {}
        for f in _load():
            ring_ = f["geometry"]["coordinates"][0]
            pts = [self.proj(lon, lat) for lon, lat in ring_]
            mid = len(pts) // 2
            simp = _rdp(pts[: mid + 1], 0.35)[:-1] + _rdp(pts[mid:], 0.35)
            self.districts[f["properties"]["name"]] = (pts, simp)

    def proj(self, lon, lat):
        return self.ox + (lon - self.LON0) * self.k, self.oy + (self.LAT1 - lat) * self.k

    def d(self, name):
        pts = self.districts[name][1]
        return "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + " Z"

    def centroid(self, name):
        pts = self.districts[name][0]
        a = cx = cy = 0.0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
            c = x0 * y1 - x1 * y0
            a += c
            cx += (x0 + x1) * c
            cy += (y0 + y1) * c
        a *= 0.5
        if abs(a) < 1e-6:
            xs, ys = zip(*pts)
            return sum(xs) / len(xs), sum(ys) / len(ys)
        return cx / (6 * a), cy / (6 * a)

    def draw_base(self, s: SVG, fill="#E8E9F1", stroke="#FFFFFF", sw=0.8, name="Uganda districts"):
        with s.g(name):
            for n in self.districts:
                s.path(self.d(n), fill=fill, stroke=stroke, sw=sw, name=n)

    def draw_branches(self, s: SVG, name="branch districts", sw=1.2):
        with s.g(name):
            for br, (dist, reg, ag, conv, tgt) in BRANCHES.items():
                s.path(self.d(dist), fill=perf_color(conv / tgt), op=0.75, stroke="#FFFFFF", sw=sw, name=br)

    def pins(self, s: SVG, size=11, labels=True, only=None):
        with s.g("branch pins"):
            for br, (dist, reg, ag, conv, tgt) in BRANCHES.items():
                if only and br not in only:
                    continue
                x, y = self.centroid(dist)
                if br == "Kampala East":
                    x, y = x + 10, y - 6
                s.circle(x, y, 5, fill=BRAND_D, stroke="#FFFFFF", sw=1.6)
                if labels:
                    w = tw(br, size, 600)
                    s.rect(x + 8, y - size + 1, w + 8, size + 6, fill="#FFFFFF", rx=4, op=0.9, name="label bg")
                    s.text(x + 12, y + 3, br, size, 600, INK, name=br)


# ---------------------------------------------------------------- street map (illustrative)
class StreetMap:
    """A stylised street map (roads, lake, parks) in a box, like a light map tile.

    Everything is generated inside the box, so no clipping is needed. Seeded, so it is stable between builds.
    """

    def __init__(self, s: SVG, x, y, w, h, seed=7, lake=True, places=None, dense=1.0):
        self.s, self.x, self.y, self.w, self.h = s, x, y, w, h
        rnd = random.Random(seed)
        P = lambda fx, fy: (x + fx * w, y + fy * h)
        with s.g("street map"):
            s.rect(x, y, w, h, fill="#F2F1EC", name="land")
            # parks / wetlands
            for i in range(int(7 * dense)):
                cx, cy = rnd.uniform(0.05, 0.95), rnd.uniform(0.05, 0.85)
                rw, rh = rnd.uniform(0.05, 0.12), rnd.uniform(0.04, 0.1)
                pts = []
                for k in range(9):
                    a = k / 9 * 2 * math.pi
                    rr = rnd.uniform(0.7, 1.0)
                    px = min(max(cx + math.cos(a) * rw * rr, 0.005), 0.995)
                    py = min(max(cy + math.sin(a) * rh * rr, 0.005), 0.995)
                    pts.append(P(px, py))
                s.poly(pts, fill="#DDEBD3", name="park")
            if lake:
                pts = [P(1.0, 0.62), P(0.9, 0.7), P(0.82, 0.8), P(0.74, 0.86), P(0.66, 0.95), P(0.62, 1.0), P(1.0, 1.0)]
                s.poly(pts, fill="#C9DDF0", name="Lake Victoria")
                s.text(x + w * 0.86, y + h * 0.93, "Lake Victoria", 12, 400, "#6C8FB5", anchor="middle",
                       italic=True, name="lake label")
            # minor streets: short wiggly segments in a loose grid
            with s.g("minor streets"):
                step = 46 / dense
                gx = x + 8
                while gx < x + w - 8:
                    gy = y + rnd.uniform(0, step)
                    while gy < y + h - 8:
                        if rnd.random() < 0.55:
                            ang = rnd.choice([0, 90]) + rnd.uniform(-18, 18)
                            ln = rnd.uniform(24, 60)
                            ex = gx + math.cos(math.radians(ang)) * ln
                            ey = gy + math.sin(math.radians(ang)) * ln
                            if x + 4 < ex < x + w - 4 and y + 4 < ey < y + h - 4 and not self._in_lake(ex, ey, lake) \
                                    and not self._in_lake(gx, gy, lake):
                                s.line(gx, gy, ex, ey, "#FFFFFF", 3, cap="round")
                        gy += step
                    gx += step
            # arterial roads (edge to edge)
            self.roads = [
                [(0.0, 0.22), (0.3, 0.3), (0.55, 0.18), (1.0, 0.28)],
                [(0.0, 0.62), (0.28, 0.55), (0.5, 0.6), (0.62, 0.84)],
                [(0.18, 0.0), (0.26, 0.35), (0.2, 0.7), (0.3, 1.0)],
                [(0.58, 0.0), (0.52, 0.3), (0.66, 0.5), (0.95, 0.6)],
                [(0.78, 0.0), (0.8, 0.2), (0.9, 0.35), (1.0, 0.4)],
            ]
            for r in self.roads:
                (ax, ay), (b1x, b1y), (b2x, b2y), (ex, ey) = [P(*p) for p in r]
                d = f"M{ax:.1f} {ay:.1f} C{b1x:.1f} {b1y:.1f} {b2x:.1f} {b2y:.1f} {ex:.1f} {ey:.1f}"
                s.path(d, stroke="#E7D7B4", sw=9, name="main road casing")
                s.path(d, stroke="#FBF3DE", sw=6, name="main road")
            if places:
                with s.g("place names"):
                    for name, fx, fy in places:
                        px, py = P(fx, fy)
                        s.text(px, py, name, 12, 600, "#8A8C9E", anchor="middle", name=name)

    def _in_lake(self, px, py, lake):
        if not lake:
            return False
        fx, fy = (px - self.x) / self.w, (py - self.y) / self.h
        return fy > 0.6 and fx > 0.6 and fy > 0.6 + (1 - fx) * 1.1

    def P(self, fx, fy):
        return self.x + fx * self.w, self.y + fy * self.h


def map_pin(s: SVG, x, y, color, label=None, size=1.0, name="pin"):
    """Tear-drop pin whose point is at (x, y)."""
    k = size
    with s.g(name):
        s.path(f"M{x:.1f} {y:.1f} C{x - 4 * k:.1f} {y - 8 * k:.1f} {x - 12 * k:.1f} {y - 12 * k:.1f} {x - 12 * k:.1f} "
               f"{y - 21 * k:.1f} A{12 * k:.1f} {12 * k:.1f} 0 1 1 {x + 12 * k:.1f} {y - 21 * k:.1f} "
               f"C{x + 12 * k:.1f} {y - 12 * k:.1f} {x + 4 * k:.1f} {y - 8 * k:.1f} {x:.1f} {y:.1f} Z",
               fill=color, stroke="#FFFFFF", sw=1.6)
        if label is not None:
            s.text(x, y - 16.5 * k, str(label), 11 * k, 700, "#FFFFFF", anchor="middle", name="pin label")
        else:
            s.circle(x, y - 21 * k, 4.2 * k, fill="#FFFFFF")


def agent_dot(s: SVG, x, y, initials, color=BRAND, live=True, name="agent"):
    with s.g(name):
        if live:
            s.circle(x, y, 20, fill=color, op=0.15)
        s.circle(x, y, 14, fill=color, stroke="#FFFFFF", sw=2.5)
        s.text(x, y + 4, initials, 10.5, 700, "#FFFFFF", anchor="middle")
