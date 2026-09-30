# Handoff: Letshego field sales mockups: first build to client-record hub
_Date: 2026-09-30 22:05 · Author: Claude_

## Goal
Build a clickable prototype of the Letshego Uganda field sales app (Android agent app + web console) from
the client brief, using the same Python → SVG → `prototype.html` method as the SNV mockups, pushed to
`bloodykheeng/letshego` for Vercel.

## Status
Done for a first demo: 49 screens (19 web, 30 app), light + dark, all links valid, all pushed to `main`.
Vercel project not yet connected by the user.

## What changed
- Whole repo created this session. Generator in [_src/](../../_src/): `kit.py` (drawing kit, soft shadows,
  icons, Letshego wordmark), `charts.py` (maps, funnel, heat strip), `data.py` (shared demo data),
  `web.py` + `web2.py` (console), `mobile.py` (agent app), `theme.py` (generated dark mode),
  `build.py` (screens + `prototype.html` viewer), `combine.py`, `briefing.py`.
- Web console: W00 sign-in · W01 sales overview · W02 agents · W03 agent profile · W04 field map ·
  W05 pipeline · W06 client record · W07–W08 approvals · W09 why / why not · W10–W10c journey plans ·
  W11–W11b locations · W12–W12c users, edit user, roles & access · W13 reports & audit.
- Agent app: M1–M3 splash, PIN sign-in, Home · M4–M4c journey plans · M5 start a visit · M6 new client ·
  M7/M7b first visit + book next visit · M8 why not · **M9–M9e client record during a visit (tabs)** ·
  M10–M13 KYC · M14–M15 loan application · M16 conversion · M16b check out · M17 my clients ·
  M18–M18d client record after the visit · M19 Me.
- Docs: [README.md](../../README.md) (how it works, rules, visual style) and
  [BRIEFING.md](../../BRIEFING.md) (team briefing, walkthrough, questions for the client).
- `.claude/commands/handoff.md` + `handoffpass.md` adapted from the SDS workspace; `.vercelignore`
  keeps `.claude/`, `_src/` and `_previews/` off the public site.

## Uncommitted / in-flight
- none: all committed and pushed (verify with `git status`).

## Next steps
1. User connects the repo on Vercel (preset "Other", no build command, output = root). If the project
   name is not `letshego-prototype`, update the URL in `build.py` (PROTO), `index.html`,
   `_src/briefing.py` and the links in `BRIEFING.md`, then rebuild (README §8).
2. Walk the demo path end to end in the browser (README §10) and fix anything the user flags.
3. W04 field map agent rows still show plain "visits · conversions"; could split planned / off-plan to
   match W01–W03.

## Decisions settled this session
- **Brand**: indigo `#2F2E80` + yellow `#FBD405` + faceted triangle, sampled from the LetsGo app on
  Google Play (letshego.com was unreachable). Rejected: flat heavy indigo blocks and the dark hero card
  ("too much blue", "dark thing doesn't look good"): now light surfaces, soft-shadow cards, indigo only
  for actions, yellow for highlights. No yellow page wash.
- **Conversion** = application submitted with every required item; approval never changes it (brief).
- **The visit is the unit**: check-in → purpose → outcome at check-out. A visit always starts by
  choosing the client (plan, search or New client); off-plan visits allowed.
- **Adding a client is light registration; KYC happens on a visit, once, only after "interested".**
  Rejected: KYC on every visit, and "Interested?" on the registration form.
- **Client record is the hub** (user's call): check in lands on the client's record; tabs Overview /
  KYC / Loan / Visits; **one bottom action per tab** (Overview: Check in / Check out · KYC: Start /
  Update KYC · Loan: Take loan application · after submit: Check out). KYC and loan are separate tabs,
  never one wizard. M16 conversion has **Close** (back to the Loan tab, visit still open), not check-out.
- **Back arrows go to a fixed parent** (record → My clients, loan form → Loan tab, KYC form → KYC tab);
  switching tabs never adds a Back step (`!tab:`). Only New client uses history (`!back:`).
- **Journey plan = a named list of clients** with agent, start/end dates, description, goal; many per
  agent; supervisor creates (W10c) or agent proposes for approval (M4c). Rejected: "today's route" and
  per-day visit counts.
- **Locations are master data**: Region › Branch › Territory › Route (NICE model, from NICE's user
  manual). Clients sit on routes (placed from GPS); people get locations in the user form (W12b).
  Agent leaving = tick their territory on another agent's user page. Rejected: client-by-client
  handover, and one all-in-one territories page ("not practical").
- **Dark mode lives in the product** (moon in the console top bar and on the app's Me screen); D key
  is only a presenter shortcut. Rejected: a Dark button in the viewer bar.
- **Wording**: short and plain on screens; no essay subtitles.

## Still open
| Question | Blocks | Recommendation |
| --- | --- | --- |
| Vercel project name | the share links in docs | Use `letshego-prototype` so nothing needs editing |
| Real products, rates, affordability rule, branch limit | nothing (placeholders labelled) | Ask Letshego at the demo (BRIEFING §9) |
| Real regions / branches / territories | nothing | Ask Letshego; data is in `charts.py` / `web2.py` |

## Gotchas & context
- Screens are generated: never hand-edit `web/`, `mobile/`, `*-dark/` or `prototype.html`.
- Renaming a screen leaves the old SVG behind in both `web/` and `web-dark/` (or mobile): `git rm` it.
- `CARD` is `#FFFFFE` on purpose so dark mode can tell cards from white text; new colours that look
  wrong in dark go in `KEEP` / `SURFACE` in `theme.py`.
- Headless Chrome won't render < ~500 px wide: check phone screens on a contact sheet, not `--png`.
- Inline Python in bash heredocs broke twice on quotes/`’`; write patch scripts to files instead.
- A wildcard `rm` was blocked by the safety check; delete generated files by exact name.

## Where the record lives
- Docs written or updated: `README.md`, `BRIEFING.md` (+ generated `briefing.html`)
- Live prototype: https://letshego-prototype.vercel.app (once connected)
- Session transcript: `~/.claude/projects/d--coding-new-wave-letshego/78bb08ae-cc07-404b-8fcf-fc6a39baf08b.jsonl`
  (~50 MB). **Grep it, never read it whole.** Last resort only, for something this note failed to capture.

## How to verify
- `cd _src && python build.py && python combine.py && python briefing.py` (all run clean;
  expect "19 web + 30 mobile")
- Link check: every hotspot target in `prototype.html` exists and every screen is reachable
  (strip `!back:` / `!tab:` prefixes; skip `!theme`)
- Open `prototype.html?show#m09` and walk: Home → Florence → KYC tab → Start KYC → … → Loan tab →
  Take loan application → submit → Close → Check out
