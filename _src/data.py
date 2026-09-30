"""Illustrative data shared by the web and mobile screens, so numbers agree everywhere.

All names, figures and IDs are made up for the demo.
"""
from __future__ import annotations

from charts import BRANCHES

TODAY = "Wed 30 Sep 2026"
QUARTER = "Q3 2026"
QUARTER_RANGE = "1 Jul – 30 Sep"

MGMT = ("Patricia Nankya", "Head of Sales", "PN")
SUPERVISOR = ("Moses Okello", "Branch Supervisor · Kampala East", "MO")
AGENT = ("Sarah Namuli", "Field Sales Agent", "SN")


def _spread(total, weights):
    tot = sum(weights)
    vals = [round(total * w / tot) for w in weights]
    vals[-1] += total - sum(vals)
    return vals


# The pattern the client described: busy in week 1, quiet until the last three weeks.
VISITS_Q = 8412
CONV_Q = sum(b[3] for b in BRANCHES.values())          # 1,051 applications submitted = conversions
TARGET_Q = sum(b[4] for b in BRANCHES.values())        # 1,382
AGENTS_N = sum(b[2] for b in BRANCHES.values())        # 62
WEEK_VISITS = _spread(VISITS_Q, [14, 9.5, 4.6, 3.1, 2.7, 2.5, 2.8, 3.0, 3.8, 5.6, 10.5, 15.2, 19.7])
WEEK_CONV = _spread(CONV_Q, [9, 7, 3, 1.8, 1.5, 1.4, 1.7, 2, 2.6, 4.5, 11, 18, 26])
WEEK_LABELS = [f"W{i}" for i in range(1, 14)]
WEEK_DATES = ["1 Jul", "8 Jul", "15 Jul", "22 Jul", "29 Jul", "5 Aug", "12 Aug", "19 Aug", "26 Aug", "2 Sep", "9 Sep",
              "16 Sep", "23 Sep"]

# Funnel for the quarter (all branches)
FUNNEL = [
    ("Visited", 8412),
    ("Interested", 3286),
    ("KYC captured", 1904),
    ("KYC validated", 1652),
    ("Negotiation", 1418),
    ("Applied", CONV_Q),
]
APPROVED, REJECTED, PENDING = 812, 166, 73
CONV_SPLY = 874   # applications in Q3 2025, from core banking (no field data existed before the app)

# Agents shown in the tables: name, initials, branch, territory, visits, conversions, target, 13 weekly visits,
# last check-in, status
AGENTS = [
    ("Sarah Namuli", "SN", "Kampala East", "Ntinda · Kiwatule", 214, 19, 22,
     [22, 18, 15, 14, 16, 15, 17, 14, 16, 17, 16, 18, 16], "Today 11:42", "On track"),
    ("Robert Ouma", "RO", "Kampala Central", "Wandegeya · Makerere", 241, 31, 27,
     [30, 22, 14, 12, 11, 13, 14, 16, 18, 20, 22, 25, 24], "Today 10:15", "On track"),
    ("Allan Tumwine", "AT", "Mbarara", "Mbarara town · Kakoba", 198, 23, 22,
     [26, 20, 12, 10, 12, 11, 13, 12, 14, 15, 17, 18, 18], "Today 09:58", "On track"),
    ("Peter Kato", "PK", "Kampala East", "Kireka · Bweyogerere", 162, 15, 22,
     [30, 24, 6, 4, 3, 5, 4, 6, 8, 12, 18, 20, 22], "Today 11:05", "At risk"),
    ("Harriet Nabirye", "HN", "Jinja", "Jinja town · Walukuba", 151, 14, 22,
     [28, 20, 8, 5, 4, 4, 5, 6, 7, 10, 16, 18, 20], "Today 08:41", "At risk"),
    ("Grace Akol", "GA", "Lira", "Lira town · Adyel", 139, 13, 21,
     [26, 21, 7, 3, 2, 3, 4, 5, 6, 9, 15, 18, 20], "Yesterday 16:20", "At risk"),
    ("Ruth Achieng", "RA", "Kampala East", "Naalya · Kira", 128, 11, 22,
     [31, 25, 5, 2, 0, 0, 2, 3, 4, 8, 14, 16, 18], "Today 10:32", "At risk"),
    ("Samuel Wandera", "SW", "Mbale", "Mbale town · Namakwekwe", 102, 9, 24,
     [30, 22, 4, 0, 0, 0, 0, 2, 3, 5, 10, 12, 14], "Today 07:55", "Behind"),
    ("Fred Opio", "FO", "Gulu", "Gulu town · Layibi", 96, 8, 21,
     [26, 24, 6, 2, 0, 0, 0, 0, 2, 4, 9, 11, 12], "Yesterday 15:02", "Behind"),
    ("Brian Ssali", "BS", "Kampala East", "Banda · Kyambogo", 74, 5, 22,
     [24, 20, 5, 0, 0, 0, 0, 0, 0, 3, 7, 7, 8], "Today 09:10", "Behind"),
    ("Denis Okiror", "DO", "Soroti", "Soroti town", 41, 2, 24,
     [22, 15, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], "17 Sep 12:44", "Silent"),
    ("Rose Candiru", "RC", "Arua", "Arua town · Oli", 38, 1, 20,
     [20, 14, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "11 Sep 10:03", "Silent"),
]

# Kampala East team for the field map and journey plans
TEAM = [
    ("Sarah Namuli", "SN", "At client", "11:42", 7, 1, "Ntinda · Kiwatule"),
    ("Peter Kato", "PK", "Moving", "11:39", 5, 0, "Kireka · Bweyogerere"),
    ("Ruth Achieng", "RA", "At client", "11:31", 4, 1, "Naalya · Kira"),
    ("Esther Nakato", "EN", "Moving", "11:28", 6, 0, "Bukoto · Kisaasi"),
    ("Ivan Mugabe", "IM", "Idle 2 h", "09:44", 2, 0, "Kigoowa · Kyanja"),
    ("Brian Ssali", "BS", "Idle 3 h", "09:10", 1, 0, "Banda · Kyambogo"),
    ("Joan Auma", "JA", "Offline", "Yesterday", 0, 0, "Nakawa · Mbuya"),
]

# The client we follow through the demo
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
}


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
