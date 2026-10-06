"""Illustrative data shared by the web and mobile screens, so numbers agree everywhere.

All names, figures and IDs are made up for the demo.

The funnel (Letshego, 2 Oct 2026): sales agents prospect on routes the branch manager gives them, turn the
prospects who want a loan into leads, and relationship officers visit the leads and complete KYC. A prospect whose KYC is
completed is a client: that is the conversion.
"""
from __future__ import annotations

from charts import BRANCHES
from kit import STAGE

TODAY = "Wed 30 Sep 2026"
QUARTER = "Q3 2026"
QUARTER_RANGE = "1 Jul – 30 Sep"

MGMT = ("Patricia Nankya", "Head of Sales", "PN")
SUPERVISOR = ("Moses Okello", "Branch Manager · Kampala East", "MO")
AGENT = ("Sarah Namuli", "Sales Agent", "SN")
RO = ("Joel Byaruhanga", "Relationship Officer", "JB")


def _spread(total, weights):
    """Split total over weights; zero weights stay zero, the rounding remainder goes to the biggest week."""
    tot = sum(weights)
    vals = [round(total * w / tot) for w in weights]
    vals[weights.index(max(weights))] += total - sum(vals)
    return vals


# The pattern the client described: busy in week 1, quiet until the last three weeks.
RHYTHM = [14, 9.5, 4.6, 3.1, 2.7, 2.5, 2.8, 3.0, 3.8, 5.6, 10.5, 15.2, 19.7]
CONV_Q = sum(b[3] for b in BRANCHES.values())          # 1,051 clients (KYC completed) = conversions
TARGET_Q = sum(b[4] for b in BRANCHES.values())        # 1,382 clients
AGENTS_N = sum(b[2] for b in BRANCHES.values())        # 62 sales agents
ROS_N = 18                                             # relationship officers
PROSPECTS_Q = 48_260
LEADS_Q = 8_412
PROSPECT_TARGET_Q = 61_400                             # sum of the route targets in branch managers' plans
LEAD_VISITS_Q = 2_964                                  # relationship officers' visits to leads
HOURS_PROSPECTING = 4.1                                # average hours a day spent prospecting on route days
WEEK_PROSPECTS = _spread(PROSPECTS_Q, RHYTHM)
WEEK_LEADS = _spread(LEADS_Q, [12, 9, 4.4, 3, 2.6, 2.4, 2.7, 3, 3.9, 5.8, 11, 16, 21])
WEEK_CONV = _spread(CONV_Q, [9, 7, 3, 1.8, 1.5, 1.4, 1.7, 2, 2.6, 4.5, 11, 18, 26])
WEEK_LABELS = [f"W{i}" for i in range(1, 14)]
WEEK_DATES = ["1 Jul", "8 Jul", "15 Jul", "22 Jul", "29 Jul", "5 Aug", "12 Aug", "19 Aug", "26 Aug", "2 Sep", "9 Sep",
              "16 Sep", "23 Sep"]

# The client journey funnel for the quarter (all branches): the three numbers Letshego asked to see everywhere.
FUNNEL = [
    ("Prospects", PROSPECTS_Q, STAGE["Prospect"]),
    ("Leads generated", LEADS_Q, STAGE["Lead"]),
    ("KYC completed", CONV_Q, STAGE["KYC completed"]),
]
APPROVED, REJECTED, PENDING = 812, 166, 73
CONV_SPLY = 874   # new clients in Q3 2025, from core banking (no field data existed before the app)


def pct(a, b, digits=0):
    return f"{a / b:.{digits}%}" if b else "—"


# Sales agents in the tables, best first by clients:
# name, initials, branch, territory, prospects, leads, clients (KYC completed from their leads), prospect target,
# 13 weekly prospect counts, hours prospecting a day, last ping, status (prospects against target)
_SHAPES = {
    "steady": [22, 18, 15, 14, 16, 15, 17, 14, 16, 17, 16, 18, 16],
    "even": [30, 22, 14, 12, 11, 13, 14, 16, 18, 20, 22, 25, 24],
    "dip": [26, 20, 12, 10, 12, 11, 13, 12, 14, 15, 17, 18, 18],
    "slump": [30, 24, 6, 4, 3, 5, 4, 6, 8, 12, 18, 20, 22],
    "slump2": [28, 20, 8, 5, 4, 4, 5, 6, 7, 10, 16, 18, 20],
    "slump3": [26, 21, 7, 3, 2, 3, 4, 5, 6, 9, 15, 18, 20],
    "slump4": [31, 25, 5, 2, 0, 0, 2, 3, 4, 8, 14, 16, 18],
    "gap": [30, 22, 4, 0, 0, 0, 0, 2, 3, 5, 10, 12, 14],
    "gap2": [26, 24, 6, 2, 0, 0, 0, 0, 2, 4, 9, 11, 12],
    "gap3": [24, 20, 5, 0, 0, 0, 0, 0, 0, 3, 7, 7, 8],
    "silent": [22, 15, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    "silent2": [20, 14, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}
_A = [
    ("Andrew Kasule", "AK", "Kampala Central", "Wandegeya · Makerere", 1702, 312, 46, 1800, "even", 5.4,
     "Today 10:15"),
    ("Allan Tumwine", "AT", "Mbarara", "Mbarara town · Kakoba", 1588, 297, 43, 1650, "dip", 5.2, "Today 09:58"),
    ("Sarah Namuli", "SN", "Kampala East", "Ntinda · Kiwatule", 1486, 286, 41, 1650, "steady", 5.1, "Today 11:42"),
    ("Harriet Nabirye", "HN", "Jinja", "Jinja town · Walukuba", 1064, 181, 24, 1500, "slump2", 3.4, "Today 08:41"),
    ("Peter Kato", "PK", "Kampala East", "Kireka · Bweyogerere", 1120, 198, 27, 1650, "slump", 3.6, "Today 11:05"),
    ("Ruth Achieng", "RA", "Kampala East", "Naalya · Kira", 1012, 171, 22, 1650, "slump4", 3.3, "Today 10:32"),
    ("Grace Akol", "GA", "Lira", "Lira town · Adyel", 978, 160, 21, 1500, "slump3", 3.1, "Yesterday 16:20"),
    ("Samuel Wandera", "SW", "Mbale", "Mbale town · Namakwekwe", 812, 120, 14, 1500, "gap", 2.6, "Today 07:55"),
    ("Fred Opio", "FO", "Gulu", "Gulu town · Layibi", 704, 98, 11, 1500, "gap2", 2.2, "Yesterday 15:02"),
    ("Brian Ssali", "BS", "Kampala East", "Banda · Kyambogo", 560, 71, 7, 1650, "gap3", 1.8, "Today 09:10"),
    ("Denis Okiror", "DO", "Soroti", "Soroti town", 302, 34, 3, 1500, "silent", 0.6, "17 Sep 12:44"),
    ("Rose Candiru", "RC", "Arua", "Arua town · Oli", 268, 22, 1, 1350, "silent2", 0.4, "11 Sep 10:03"),
]


def _status(p, t, shape):
    if shape.startswith("silent"):
        return "Silent"
    f = p / t
    return "On track" if f >= 0.85 else ("At risk" if f >= 0.6 else "Behind")


AGENTS = [(nm, ini, br, terr, p, l, c, t, _spread(p, _SHAPES[sh]), hrs, last, _status(p, t, sh))
          for nm, ini, br, terr, p, l, c, t, sh, hrs, last in _A]
SARAH = next(a for a in AGENTS if a[0] == AGENT[0])

# Kampala East sales agents today: name, initials, status, last ping, prospects today, today's target,
# leads today, route, hours prospecting today
TEAM = [
    ("Sarah Namuli", "SN", "Prospecting", "11:42", 32, 50, 3, "Kiwatule market route", 2.6),
    ("Peter Kato", "PK", "Prospecting", "11:39", 21, 50, 2, "Kireka stage route", 2.1),
    ("Ruth Achieng", "RA", "Prospecting", "11:31", 27, 50, 4, "Naalya estates route", 2.4),
    ("Esther Nakato", "EN", "Prospecting", "11:28", 18, 40, 1, "Bukoto shops route", 1.9),
    ("Ivan Mugabe", "IM", "Idle", "09:44", 6, 40, 0, "Kyanja market route", 0.8),
    ("Brian Ssali", "BS", "Outside territory", "11:20", 3, 50, 0, "Banda stage route", 0.5),
    ("Joan Auma", "JA", "Offline", "Yesterday", 0, 40, 0, "Mbuya hill route", 0.0),
]
# Kampala East relationship officers today: name, initials, status, last ping, lead visits today, KYC completed today,
# lead journey plan, Q3 KYC completed
ROS = [
    ("Joel Byaruhanga", "JB", "At a lead", "11:42", 3, 2, "Kiwatule leads", 61),
    ("Christine Apio", "CA", "Moving", "11:36", 2, 1, "Kireka & Naalya leads", 70),
]

# The client we follow through the demo: Sarah prospected her, called her the next day (lead), Moses put her on
# Joel's lead journey plan, and Joel completed her KYC on 30 Sep.
CLIENT = {
    "name": "Florence Nambi",
    "initials": "FN",
    "id": "CL-0021457",
    "app_id": "LU-APP-2609-04817",
    "phone": "0772 418 ··· ",
    "nin": "CF84•••••••7KD",
    "business": "Nambi Tailoring & Fabrics, Kiwatule",
    "product": "MSE Business Loan",
    "amount": 6_000_000,
    "months": 18,
    "gps": "0.3712, 32.6205 · ±9 m",
    "route": "Kiwatule market route",
    "prospected": "Tue 22 Sep 10:18",
    "lead": "Wed 23 Sep 14:05",
    "plan": "Kiwatule leads",
}

# The prospect Sarah calls in the demo and turns into a lead
CALLEE = {"name": "Aisha Nalubega", "initials": "AN", "phone": "0752 664 ···", "amount": 2_000_000,
          "met": "Mon 28 Sep 15:40 · Kiwatule market route", "business": "Vegetable stall, Kiwatule market"}


def instalment(p, months, monthly_rate=0.029):
    r = monthly_rate
    return p * r / (1 - (1 + r) ** -months)


def ugx(n, short=False):
    if short:
        if n >= 1e9:
            return f"UGX {n / 1e9:.2f}B"
        if n >= 1e6:
            return f"UGX {n / 1e6:.1f}M"
        return f"UGX {n / 1e3:.0f}K"
    return f"UGX {n:,.0f}"


def rnd_instalment(p, months):
    return round(instalment(p, months) / 500) * 500
