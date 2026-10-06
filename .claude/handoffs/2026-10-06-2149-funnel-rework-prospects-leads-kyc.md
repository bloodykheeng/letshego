# Handoff: funnel rework after the first demo (prospects, leads, KYC completed)
_Date: 2026-10-06 21:49 · updated 22:42 · Author: Claude_

## Goal
Rework the prototype around what Letshego asked for at the first demo (2 Oct): lead generation, the
three-stage funnel, route and lead journey plans, and two field roles. The source is the user's own notes,
which are pasted below and are the reference for every decision.

## Status
Done for the second demo: 59 screens (22 web, 37 app), light + dark, all links valid, every screen
reachable, all committed and pushed to `main`. Commits this session: 681b378 / 6efe857 (dark mode out and
back), cf11e7c (funnel rework), 5694906 (this note), 7cf07bb (docs), 2fa2f6d (client = loan disbursed,
menu order), then the docs/URL/handoff refresh.

## What changed
- **Funnel and data:** `STAGES` in [kit.py](../../_src/kit.py) is now Prospect · Lead · KYC completed;
  [data.py](../../_src/data.py) is rewritten (FUNNEL, AGENTS by prospects/leads/clients/hours, TEAM,
  ROS, CLIENT journey dates, CALLEE = Aisha).
- **App, sales agent (Sarah):** m03 Home (today's target, this week's stats, each card opens its list) ·
  m04 route journey plans list → m04a week 40 · m04b prospect map · m05 add a prospect · m06 my prospects ·
  m07 prospect (Aisha) → m07b make a lead → m07c lead created · m08 no loan: why · m17 my leads · m19 Me.
- **App, relationship officer (Joel):** m20 Home · m21 lead journey plans list → m21b Kiwatule leads ·
  m09–m09f / m18–m18d Florence's record (Overview shows lead details from Sarah; History tab) ·
  m10–m13 KYC (m13 = KYC completed, ready for the loan) · m14–m16b loan · m23 leads & clients · m22 Me.
- **Shell:** 4-tab bottom bar per role (`NAV_ITEMS`), no centre button; `add_button` floating action;
  M2 sign-in has demo buttons for Sarah / Joel.
- **Console:** w01 head office (funnel, New clients = loans disbursed with conversion %, time prospecting,
  prospects → KYC → clients by agent) · **w01b** new, Moses's "Kampala East today" · w02 sales agents · w03 where Sarah has worked (map
  layers) · w04 field map (geofence alert on Brian) · w05 pipeline · w06 Florence's journey ·
  w10 journey plans (route + lead) · **w10b–w10e** route/lead journey plan detail and new · w11/w11b
  locations without Region · w12/w12b/w12c users and roles (Regional Manager removed).
- **Client = loan disbursed** (team, late in the session): `CLIENTS_Q` = 786 and `clients()` in data.py
  (about 3 in 4 KYC-completed leads get a loan); conversion everywhere uses disbursed loans; w07 banner,
  w06 journey (ends at "Loan disbursed: client"), m13/m15/m16 and the app lists no longer call KYC a client.
- **Console menu** (`NAV` in web.py): SALES (Overview) · PLANNING (Journey plans) · FIELD (Agents, Field map,
  Client pipeline) · LOANS · ADMIN. W10 headings: "Route journey plans · sales agents".
- **Live URL is letshego.vercel.app** (Vercel project "letshego"); build.py, index.html, briefing.py,
  README, BRIEFING and the /handoff command were switched from letshego-prototype.vercel.app.
- **Docs:** README (screen table §4, rules §6, presenting §10) and BRIEFING (what changed, getting around
  the app, walkthrough, data flow, questions) are current; `briefing.html` regenerated.
- Dark mode: removed then restored the same session; branch `with-dark-mode` on GitHub is now redundant.

## Uncommitted / in-flight
- none: all committed and pushed.

## Next steps
1. Walk the demo path in the browser (BRIEFING §8) and fix whatever the user flags.
2. Ask Letshego the questions in BRIEFING §9, especially: is a lead "name + phone" (their meeting note) or
   "name + phone, then NIN + amount" (the user's notes, what we built)?
3. Later, from Richard's meeting notes, only when the user asks: turnaround time per approval stage,
   rejection reasons at every loan stage, the loan calculator from their Excel sheet, digital ID checks.
4. Optionally delete the `with-dark-mode` branch on GitHub (ask first).

## Decisions settled this session
- **The user's notes are the reference** ("my notes were better"). Don't add features beyond them;
  the user called out over-building twice ("don't over-exaggerate").
- **Hierarchy is Branch › Territory › Route**, three levels only. Routes have sales agents; the branch
  manager runs the branch. Rejected: Region level and the Regional Manager role.
- **Funnel: Prospects → Leads generated → KYC completed**, shown on cards everywhere, including Moses's side.
  "KYC captured" was renamed because it "feels weird"; small cards say "KYC" + "completed".
- **Client = loan disbursed; conversion = prospect → client** (team correction after this note was first
  written: "Clients are when a loan is disbursed"). KYC completed is a funnel stage, not a client.
  Rejected: "KYC completed = client" (my earlier assumption) and branch conversion league tables.
- **Prospect = name, phone number, location. Lead = + NIN, loan amount, location.** Nothing else on those
  forms. Rejected: "where you met", notes, "what for", "best day to visit".
- **No calling in the app** ("this is not a dialer app"): agents call from their own phone; the app only
  records the result. Rejected: call screen, call buttons, "calls to make".
- **Route journey plan** (level 1): branch manager gives a sales agent a route per day + a prospect target.
  **Lead journey plan** (level 5): branch manager gives a relationship officer leads to visit. Use these
  exact names. Plans open from a **list first**, then the plan.
- **Console menu:** Journey plans sits right under Overview (team: it looked misplaced after Loans);
  route journey plans are headed "sales agents", not "prospecting".
- **One role per user**; a branch manager can *assign* other work (Joel, an officer, gets a route plan for
  Friday). Rejected: one user holding two roles.
- **Navigation:** plain 4-tab bar; actions sit on the screen they belong to (+ Add prospect). Summary
  cards (yellow "today" card) are not clickable; stat cards open their own list. Back returns to where you
  came from (`history=True`); Florence's record goes back to the lead plan during a visit, to Clients after.
- **Wording:** professional, short ("Q3 2026 performance", not "your funnel").
- **Dark mode stays** (generated by `theme.py`, costs nothing).

## Still open
| Question | Blocks | Recommendation |
| --- | --- | --- |
| Lead = name + phone (meeting note) or + NIN/amount (user's notes)? | nothing; easy to change | Keep the user's notes; confirm at the demo |
| "He selects on the leads": does the officer pick leads himself? | nothing | Currently Moses picks (w10e); add officer self-pick only if confirmed |
| Approval matrix and roles per approval level | approvals screens detail | Ask Letshego (BRIEFING §9 items 8–9) |
| Keep the "No loan: why" button (m08)? | nothing | Kept: the original brief asked for why/why not |
| Per-agent client counts | nothing; illustrative | Estimated as 3 in 4 KYC-completed leads; replace with Letshego's real numbers |
| "FIELD" as the menu heading for Agents / Field map / Client pipeline | nothing | My name for the group; rename if the user prefers |

## Gotchas & context
- Patch big edits with Python scripts written to files; inline bash heredocs with quotes break.
- Scripts written on Windows produce CRLF lists: strip `\r` before reading file names in bash.
- Renamed screen titles leave old SVGs in `web/`, `mobile/` and both `-dark` folders: delete them
  (tracked: `git rm -f`; untracked: `rm`) or `combine.py` picks them up.
- `"m04"` / `"m21"` are the plan **lists**; `m04a` / `m21b` are the plans. Hub back depends on `during`.
- "Client" now means loan disbursed: when adding numbers, KYC counts use `CONV_Q`/`c`, client counts use
  `CLIENTS_Q`/`clients(c)`. Don't put "client" on a KYC-completed lead.
- The user's notes (2 Oct), verbatim, for reference:

```
Branch / Territories / Routes · routes have sales agent · branch manager manages a branch
level 1: Moses creates journey plans; branch has territories; each territory has routes; he assigns sales
  agents routes daily, then a target, e.g. this route make 50 prospects → route journey plans
level 2: sales agents prospect in the field: name and phone number, location · prospect map
level 3: agent has the number, can call: interested in a loan? how much? e.g. 2M → generating a lead:
  national ID, loan amount, location
level 5: branch manager does a lead journey plan for the relationship officer; the officer visits and
  closes the lead, selects on the leads, captures KYC on the visit, submits details for the loan
they want to know where e.g. Farouk worked to date: leads he generated, prospects, visits
client journey funnel: prospects · leads generated · KYC captured (now "KYC completed"), in cards,
  even on Okello's side · don't show branches conversion, show prospects conversion to clients
```

## Where the record lives
- Docs written or updated: `README.md` (rules §6, screen table §4), `BRIEFING.md` (+ `briefing.html`)
- Previous handoff: `2026-09-30-2205-letshego-field-sales-mockups-first-build.md` (its funnel and role
  decisions are superseded by this note)
- Live prototype: https://letshego.vercel.app (if the Vercel project is renamed, see README §8)
- Session transcript: `~/.claude/projects/d--coding-new-wave-letshego/942a1a9b-c475-4f20-a7cd-4780062a47ef.jsonl`
  (~22 MB). **Grep it, never read it whole.** Last resort only, for something this note failed to capture.

## How to verify
- `cd _src && python build.py && python combine.py && python briefing.py` (expect "22 web + 37 mobile")
- Link check: every hotspot target in `prototype.html` exists and every screen is reachable
  (targets may be prefixed `!back:` / `!tab:`; `!theme` is the light/dark switch)
- Phone screens need a contact sheet (headless Chrome won't render narrower than ~500 px)
- Walk: `prototype.html#m02` → Sarah → Add prospect → My prospects → Aisha → Make a lead; then
  `#m02` → Joel → Plan → Kiwatule leads → Check in → KYC tab → … → Check out
