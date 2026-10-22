# Handoff: funnel rework after the first demo + delivery timeline to 7 Dec
_Date: 2026-10-06 21:49 · updated 2026-10-06, 2026-10-15 and 2026-10-23 · Author: Claude_

## Goal
Rework the prototype around what Letshego asked for at the first demo (2 Oct): lead generation, the
three-stage funnel, route and lead journey plans, and two field roles. The source is the user's own notes,
which are pasted below and are the reference for every decision.
Then (15 Oct), after the 14 Oct meeting ("we shall start building app phase 1 and two"): a delivery timeline
from 15 Oct to 7 Dec for the real build (Flutter app, Next.js dashboard, Laravel API, test and production).

## Status
Done for the second demo: 59 screens (22 web, 37 app), light + dark, all links valid, every screen
reachable, all committed and pushed to `main`. Commits this session: 681b378 / 6efe857 (dark mode out and
back), cf11e7c (funnel rework), 5694906 (this note), 7cf07bb (docs), 2fa2f6d (client = loan disbursed,
menu order), aa2f51a (docs/URL/handoff refresh). Prototype work is finished; the build is now planned.
Delivery timeline written on 15 Oct (Markdown + Word, in the letshego folder, outside this repo).

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
- **Delivery timeline (15 Oct)**, in `d:\coding\new wave\letshego\` (not in git):
  - `letshego-delivery-timeline.md`: phases, milestones, Mermaid gantt, week-by-week table per workstream
    (Laravel API · Next.js dashboard · Flutter app · environments), environments, what Letshego owes us by
    date, risks, assumptions.
  - `Letshego Delivery Timeline.docx`: the same content for sharing and team editing (landscape A4, 6 pages;
    gantt as a shaded week grid; Owner/Status columns on milestones and on Letshego's items). The Word file
    is now the copy the team edits; the two are not linked.
  - Key dates: Fri 16 Oct kickoff · Fri 23 Oct foundations · **Fri 6 Nov Phase 1 on test** · Fri 13 Nov Phase 1
    dashboards tested · **Fri 27 Nov Phase 2 on test** · Fri 4 Dec production live · **Mon 7 Dec handover for UAT**.
- **Prospect targets (23 Oct):** "route journey plans" renamed **Prospect targets** and given their own menu
  entry under Planning. Screens: w10 Prospect targets (every agent this week) · w10b one agent's week ·
  w10c Set prospect targets. **Journey plans** are now lead journey plans only: w10d list (new) · w10e
  Kiwatule leads (was w10d) · w10f new lead journey plan (was w10e). App: m04 "Prospect targets" → m04a week.
  "Route targets" wording also became "prospect targets". README, BRIEFING and both timeline files updated.

## Uncommitted / in-flight
- none: all committed and pushed.

## Next steps
1. Get the user to confirm the phase split in the timeline (see Still open), then share the Word file.
2. Send Letshego the "what we need" list (timeline §5): phase confirmation by 16 Oct, branches/territories/
   routes by 23 Oct, users and targets by 30 Oct, products/calculator/approval matrix/NIRA-CRB by 13 Nov.
3. Ask Letshego the questions in BRIEFING §9 (is a lead "name + phone" or "+ NIN and amount"?).
4. Keep the prototype as the reference design for the build; update it only if the user asks.
5. Optionally delete the `with-dark-mode` branch on GitHub (ask first).

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
- **Prospect targets** (level 1): branch manager gives a sales agent a route and a prospect target per day.
  Its own section, not a journey plan (user, 23 Oct: "this is like prospect targets"). Rejected: "route
  journey plan" (the user's 2 Oct term, misleading) and my "prospecting targets"; the user chose
  "Prospect targets" (matches the funnel word). **Journey plans** = lead journey plans only (level 5):
  leads for a relationship officer to visit. Both open from a **list first**, then one week / one plan.
- **Console menu:** SALES (Overview) · PLANNING (Prospect targets, Journey plans) · FIELD · LOANS · ADMIN.
  Planning sits right under Overview (team: it looked misplaced after Loans).
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
| What is in Phase 1 vs Phase 2? The 14 Oct note only says "phase 1 and two" | the timeline's content | Assumed: Phase 1 = lead generation (plans, prospects, leads, GPS, dashboards); Phase 2 = officer visit, KYC, loan, approval, disbursement. User to confirm |
| Is 7 Dec the start or end of user testing? | the release dates | Assumed start: production live 4 Dec, UAT from 7 Dec, go-live after |

## Gotchas & context
- Patch big edits with Python scripts written to files; inline bash heredocs with quotes break.
- Scripts written on Windows produce CRLF lists: strip `\r` before reading file names in bash.
- Renamed screen titles leave old SVGs in `web/`, `mobile/` and both `-dark` folders: delete them
  (tracked: `git rm -f`; untracked: `rm`) or `combine.py` picks them up.
- Mermaid gantt breaks on a colon inside a task name or title (that was the "Syntax error in text").
- The Word file was generated by a throwaway docx-js script in the session scratchpad (gone now). Edit the
  .docx in Word; regenerate only if asked, from the Markdown.
- Keys after the 23 Oct split: w10 targets list, w10b/w10c targets, w10d journey plans list, w10e/w10f
  lead plans. Function names `w10b_route_plan` / `w10c_new_route_plan` / `ROUTE_PLANS` kept their old names.
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
- Docs written or updated: `README.md` (rules §6, screen table §4), `BRIEFING.md` (+ `briefing.html`);
  outside the repo: `../letshego-delivery-timeline.md` and `../Letshego Delivery Timeline.docx`
- Meeting notes in `..`: `letshego meeting oct 14.txt`, `letshego changes.txt` (the user's notes),
  `eisah letshego notes.txt` (team questions); brief in `../resources/`
- Previous handoff: `2026-09-30-2205-letshego-field-sales-mockups-first-build.md` (its funnel and role
  decisions are superseded by this note)
- Live prototype: https://letshego.vercel.app (if the Vercel project is renamed, see README §8)
- Session transcript: `~/.claude/projects/d--coding-new-wave-letshego/942a1a9b-c475-4f20-a7cd-4780062a47ef.jsonl`
  (~32 MB). **Grep it, never read it whole.** Last resort only, for something this note failed to capture.

## How to verify
- `cd _src && python build.py && python combine.py && python briefing.py` (expect "22 web + 37 mobile")
- Link check: every hotspot target in `prototype.html` exists and every screen is reachable
  (targets may be prefixed `!back:` / `!tab:`; `!theme` is the light/dark switch)
- Phone screens need a contact sheet (headless Chrome won't render narrower than ~500 px)
- Walk: `prototype.html#m02` → Sarah → Add prospect → My prospects → Aisha → Make a lead; then
  `#m02` → Joel → Plan → Kiwatule leads → Check in → KYC tab → … → Check out
