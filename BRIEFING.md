# Letshego Field Sales: team briefing

> **Internal · for our team only · do not share with Letshego.**
> What you need to understand the brief, speak the client's language, and walk through the prototype with confidence.
>
> **Prototype:** https://letshego-prototype.vercel.app. The screen links below open the right screen directly.

**Contents:** [1. 30-second version](#1-the-30-second-version) · [2. What changed after the first demo](#2-what-changed-after-the-first-demo-2-oct) · [3. Words decoded](#3-the-words-they-will-use-decoded) · [4. The funnel, level by level](#4-the-funnel-level-by-level) · [5. What they asked for](#5-what-they-asked-for-and-where-it-is) · [6. Roles](#6-roles) · [7. Data flow](#7-how-data-moves) · [8. Walkthrough](#8-walkthrough-script-about-10-minutes) · [9. Questions for the client](#9-questions-to-clear-with-the-client) · [10. Likely questions](#10-likely-questions-and-short-answers) · [11. How we would build it](#11-how-we-would-build-it) · [12. Watch-outs](#12-watch-outs-before-the-demo)

---

## 1. The 30-second version

- **Letshego Uganda** is a microfinance lender (Tier IV, head office in Kololo, Kampala). It lends to civil servants through payroll deductions, to micro and small businesses, and for school fees and housing.
- **The problem:** field staff go out in the first week of the quarter, go quiet, then rush in the last three weeks. Management can't see what they do most of the quarter.
- **Their priority (2 Oct):** the **front end** of the customer journey, lead generation, not back-office work after KYC.
- **What they want to see everywhere:** one funnel, **Prospects → Leads generated → KYC completed**, and how many prospects became clients.
- **Success:** a **conversion** is a prospect who became a client: a relationship officer completed their KYC. The loan decision is tracked separately.

---

## 2. What changed after the first demo (2 Oct)

| Before (first demo) | Now |
|---|---|
| One field agent did everything: first visit, KYC, loan | **Sales agents** prospect and generate leads; **relationship officers** visit leads and complete KYC |
| Funnel: Visited → Interested → KYC → Validated → Negotiation → Applied | Funnel: **Prospects → Leads generated → KYC completed** |
| Conversion = application submitted | Conversion = **prospect became a client (KYC completed)** |
| Journey plan = a list of clients to visit | Two kinds: **route journey plans** (an agent's route per day with a prospect target) and **lead journey plans** (leads for an officer to visit) |
| "Branch Supervisor" | **Branch Manager** (Moses Okello) |
| Branch league table on the overview | **Prospects to clients by agent**, and a branch manager's own **Kampala East today** screen |
| Plans only for one kind of staff | **One role each, but work can be assigned across roles** (Moses gives Joel, an officer, a route journey plan for Friday) |

Still to come, from the meeting notes (not in the prototype yet): turnaround time at each approval stage, rejection reasons at every loan stage, the loan calculator replacing their Excel sheet as its own step, and digital authentication of National IDs and driving licences.

---

## 3. The words they will use, decoded

| Term | What it means |
|---|---|
| **Prospect** | Someone a sales agent met in the field: **name, phone number and location** (GPS). Nothing more. |
| **Lead** | A prospect who wants a loan. The agent has their number and follows up (outside the app); in the app they add the **National ID number (NIN), loan amount and location**. |
| **KYC completed** | A relationship officer visited the lead and captured **Know Your Customer** details: NIRA ID, selfie, income, collateral, CRB consent. The lead is now a **client**. |
| **Conversion** | Prospect → client. Shown as "prospect → client %" on every dashboard. |
| **Route journey plan** | The branch manager gives a sales agent **a route for each day and a prospect target** (e.g. "Kiwatule market route, 50 prospects"). |
| **Lead journey plan** | The branch manager gives a relationship officer **a list of leads to visit**, with dates and a goal. |
| **Branch › Territory › Route** | Letshego's field structure: a branch manager runs a branch, the branch has territories, each territory has routes, and routes have sales agents. Territories are **geofenced**: the app knows when someone leaves theirs. |
| **Time prospecting** | Hours on the route, from GPS. Management called this "critical". |
| **NIRA / NIN** | National Identification and Registration Authority; the NIN is on every National ID. |
| **CRB** | Credit Reference Bureau: borrowing history, checked with consent. |
| **MSE** | Micro and Small Enterprise: shops, tailors, market vendors, boda boda owners. |
| **SPLY** | Same Period Last Year: we compare new clients "vs Q3 2025". |
| **Silent** | Our word for field staff with no prospect or visit in 14+ days. Not a client term. |

---

## 4. The funnel, level by level

This follows the levels in our notes from the 2 Oct meeting.

| Level | Who | What happens | App | Console |
|---|---|---|---|---|
| 1 Planning | Branch Manager | Gives each sales agent a route per day and a prospect target | [M4 My route journey plans](https://letshego-prototype.vercel.app/prototype.html#m04) → [M4a week 40](https://letshego-prototype.vercel.app/prototype.html#m04a) | [W10](https://letshego-prototype.vercel.app/prototype.html#w10) → [W10b](https://letshego-prototype.vercel.app/prototype.html#w10b) · [W10c new](https://letshego-prototype.vercel.app/prototype.html#w10c) |
| 2 Prospecting | Sales Agent | Meets people on the route: name, phone, GPS location | [M5 Add a prospect](https://letshego-prototype.vercel.app/prototype.html#m05) · [M4b Prospect map](https://letshego-prototype.vercel.app/prototype.html#m04b) | [W04 Field map](https://letshego-prototype.vercel.app/prototype.html#w04) |
| 3 Lead | Sales Agent | Follows up the prospect on the phone (outside the app): "interested in a loan? how much?" Interested → NIN, amount, location | [M6 My prospects](https://letshego-prototype.vercel.app/prototype.html#m06) → [M7 Prospect](https://letshego-prototype.vercel.app/prototype.html#m07) → [M7b Make a lead](https://letshego-prototype.vercel.app/prototype.html#m07b) · no loan → [M8 why](https://letshego-prototype.vercel.app/prototype.html#m08) | [W05 Pipeline](https://letshego-prototype.vercel.app/prototype.html#w05) |
| 4 Lead journey plan | Branch Manager | Puts new leads on an officer's lead journey plan | [M21 My lead journey plans](https://letshego-prototype.vercel.app/prototype.html#m21) → [M21b Kiwatule leads](https://letshego-prototype.vercel.app/prototype.html#m21b) | [W10d](https://letshego-prototype.vercel.app/prototype.html#w10d) · [W10e new](https://letshego-prototype.vercel.app/prototype.html#w10e) |
| 5 KYC | Relationship Officer | Visits the lead, completes KYC: **the lead becomes a client** | [M9 record](https://letshego-prototype.vercel.app/prototype.html#m09) → [M10](https://letshego-prototype.vercel.app/prototype.html#m10)–[M13](https://letshego-prototype.vercel.app/prototype.html#m13) | [W06 Client record](https://letshego-prototype.vercel.app/prototype.html#w06) |
| After | Relationship Officer → Branch Manager / HQ | Loan application and decision (tracked, but not the conversion) | [M14](https://letshego-prototype.vercel.app/prototype.html#m14)–[M16b](https://letshego-prototype.vercel.app/prototype.html#m16b) | [W07](https://letshego-prototype.vercel.app/prototype.html#w07) → [W08](https://letshego-prototype.vercel.app/prototype.html#w08) |

**The demo story, Florence Nambi:** Sarah prospected her at Kiwatule market on Tue 22 Sep and made her a lead on Wed 23 Sep (wants UGX 6M for a sewing machine), Moses put her on Joel's "Kiwatule leads" plan, and Joel completed her KYC on 30 Sep at 11:24. She counts as a client for Sarah, for Joel and for the branch.

---

## 5. What they asked for and where it is

| They asked for | Where it is | Point to make |
|---|---|---|
| Managers plan field activity and set targets per team | [W10](https://letshego-prototype.vercel.app/prototype.html#w10), [W10c](https://letshego-prototype.vercel.app/prototype.html#w10c), [W01b](https://letshego-prototype.vercel.app/prototype.html#w01b) | A route per day, a prospect target per route. |
| Lead = as soon as name and phone are captured; then hand qualified leads to an officer | [M5](https://letshego-prototype.vercel.app/prototype.html#m05), [M7b](https://letshego-prototype.vercel.app/prototype.html#m07b), [W10e](https://letshego-prototype.vercel.app/prototype.html#w10e) | We split it, as in our notes: name + phone + GPS = prospect; + NIN, amount and location = lead. **Confirm with them** (§9). |
| A relationship manager can also act as an agent | [M22](https://letshego-prototype.vercel.app/prototype.html#m22), [W10](https://letshego-prototype.vercel.app/prototype.html#w10), [W12c](https://letshego-prototype.vercel.app/prototype.html#w12c) | Everyone keeps one role; the branch manager assigns extra work, e.g. a route journey plan for Joel on Friday. |
| GPS always captured; geofenced territories | [W04](https://letshego-prototype.vercel.app/prototype.html#w04) (Brian's alert), [M4b](https://letshego-prototype.vercel.app/prototype.html#m04b) | Prospects outside the territory still save, and the manager is told. |
| Time spent prospecting | [W01](https://letshego-prototype.vercel.app/prototype.html#w01), [W01b](https://letshego-prototype.vercel.app/prototype.html#w01b), [W02](https://letshego-prototype.vercel.app/prototype.html#w02), [W03](https://letshego-prototype.vercel.app/prototype.html#w03) | Hours on route from GPS, per agent and per day. |
| How many people each team engages | [W01b](https://letshego-prototype.vercel.app/prototype.html#w01b), [W02](https://letshego-prototype.vercel.app/prototype.html#w02) | Prospects per agent, per day, per week. |
| Where has an agent worked: prospects, leads, visits | [W03 Sarah](https://letshego-prototype.vercel.app/prototype.html#w03) | Map of everything she found this quarter, in layers. |
| Pipeline Planning → Prospecting → Conversion | [W05](https://letshego-prototype.vercel.app/prototype.html#w05), [W06](https://letshego-prototype.vercel.app/prototype.html#w06) | Florence's journey: every step with who, when and where. |
| Reasons for "no" | [M8](https://letshego-prototype.vercel.app/prototype.html#m08), [W09](https://letshego-prototype.vercel.app/prototype.html#w09) | From prospects and visits. |

---

## 6. Roles

| Role | Person in the prototype | What they do | Sees |
|---|---|---|---|
| **Sales Agent** | Sarah Namuli, Kampala East | Prospects on routes, turns prospects who want a loan into leads | Own territory and routes |
| **Relationship Officer** | Joel Byaruhanga · Christine Apio | Visits leads on lead journey plans, completes KYC, sends loan applications | Leads on their plans |
| **Branch Manager** | Moses Okello, Kampala East | Territories, routes, route journey plans for agents, lead journey plans for officers, loan approvals, branch stats | The branch |
| **HQ Credit Approver** | Daniel Ssekandi | Loans above the branch limit | All, above limit |
| **Head of Sales** | Patricia Nankya | Watches the funnel, acts on silent staff | All branches |
| **System Admin** | (not shown) | Users, devices, settings | Settings only |

**Demo shortcuts (not features):** in the console, click the name at the bottom left to switch between Patricia ([W01](https://letshego-prototype.vercel.app/prototype.html#w01)) and Moses ([W01b](https://letshego-prototype.vercel.app/prototype.html#w01b)). On the app's sign-in screen ([M2](https://letshego-prototype.vercel.app/prototype.html#m02)), pick Sarah or Joel.

---

## 7. How data moves

```
1 PLAN                 2 PROSPECT              3 LEAD                  4 LEAD PLAN            5 KYC = CLIENT
Branch manager sets →  Sales agent saves    →  Wants a loan? Agent  →  Branch manager puts →  Officer visits, completes
routes and targets     name, phone, GPS        adds NIN,               leads on an officer's  KYC (NIRA, CRB checks)
                       (works offline)         amount, location        lead journey plan              → loan application → decision
```

Everything is stored on Letshego's servers. Every change goes into the [audit trail](https://letshego-prototype.vercel.app/prototype.html#w13).

---

## 8. Walkthrough script (about 10 minutes)

1. **[W00 Sign in](https://letshego-prototype.vercel.app/prototype.html#w00):** "One sign-in for head office, branches and the field."
2. **[W01 Sales overview](https://letshego-prototype.vercel.app/prototype.html#w01)** (Patricia): "The funnel you asked for: prospects, leads, KYC completed. 1 in 46 prospects became a client this quarter. Here's the quarter rhythm, time spent prospecting, and who needs attention today."
3. **[W02 Sales agents](https://letshego-prototype.vercel.app/prototype.html#w02):** "Prospects against route targets, leads, clients, hours prospecting. Each square is a week of prospecting; red = none."
4. **[W03 Sarah](https://letshego-prototype.vercel.app/prototype.html#w03):** "Where Sarah has worked this quarter: every prospect, lead and client on the map, inside her territory."
5. **Switch to Moses** (click the name): **[W01b Kampala East today](https://letshego-prototype.vercel.app/prototype.html#w01b):** "Each agent's route and target today, live. 14 leads wait for an officer." → **[W04 Field map](https://letshego-prototype.vercel.app/prototype.html#w04):** "Brian has left his territory; Moses was told."
6. **[W10 Journey plans](https://letshego-prototype.vercel.app/prototype.html#w10):** route journey plans for agents ([W10b Sarah's week](https://letshego-prototype.vercel.app/prototype.html#w10b), [W10c new](https://letshego-prototype.vercel.app/prototype.html#w10c)) and lead journey plans for officers ([W10d](https://letshego-prototype.vercel.app/prototype.html#w10d), [W10e new](https://letshego-prototype.vercel.app/prototype.html#w10e)).
7. **The app as Sarah** ([M2](https://letshego-prototype.vercel.app/prototype.html#m02) → Sarah): [M3 Home](https://letshego-prototype.vercel.app/prototype.html#m03): today's target 32/50, this week's prospects, leads and KYC → **Add prospect** → [M5 Add a prospect](https://letshego-prototype.vercel.app/prototype.html#m05) (name, phone, location) → [M6 My prospects](https://letshego-prototype.vercel.app/prototype.html#m06) → [M7 Aisha](https://letshego-prototype.vercel.app/prototype.html#m07) → **Make a lead** → [M7b NIN, amount, location](https://letshego-prototype.vercel.app/prototype.html#m07b) → [M7c Lead created](https://letshego-prototype.vercel.app/prototype.html#m07c). Say once: "Calls happen on the phone as usual; the app records the result." Also: [M4b Prospect map](https://letshego-prototype.vercel.app/prototype.html#m04b), [M17 My leads](https://letshego-prototype.vercel.app/prototype.html#m17) (where each lead is now).
8. **The app as Joel** ([M2](https://letshego-prototype.vercel.app/prototype.html#m02) → Joel): [M20 Home](https://letshego-prototype.vercel.app/prototype.html#m20): today's lead journey plan → Florence → [M9 her record](https://letshego-prototype.vercel.app/prototype.html#m09) (lead details from Sarah) → [KYC tab](https://letshego-prototype.vercel.app/prototype.html#m09b) → [M10](https://letshego-prototype.vercel.app/prototype.html#m10)–[M12](https://letshego-prototype.vercel.app/prototype.html#m12) → [M13 KYC completed: she's a client](https://letshego-prototype.vercel.app/prototype.html#m13) → Loan tab → [M14 calculator](https://letshego-prototype.vercel.app/prototype.html#m14) → [M15](https://letshego-prototype.vercel.app/prototype.html#m15) → [M16 submitted](https://letshego-prototype.vercel.app/prototype.html#m16) → [M16b check out](https://letshego-prototype.vercel.app/prototype.html#m16b). [M22](https://letshego-prototype.vercel.app/prototype.html#m22): Joel is an officer, also assigned a route journey plan for Friday.
9. **[W06 Florence](https://letshego-prototype.vercel.app/prototype.html#w06):** "Her whole journey: prospect, lead, lead journey plan, visit, KYC, loan." → [W07](https://letshego-prototype.vercel.app/prototype.html#w07) / [W08](https://letshego-prototype.vercel.app/prototype.html#w08): "The loan decision is separate from the conversion."
10. **[W12 Users](https://letshego-prototype.vercel.app/prototype.html#w12) → [W12c Roles](https://letshego-prototype.vercel.app/prototype.html#w12c):** "Sales agents, officers and branch managers; one role each, and the branch manager can assign anyone extra work, like a route journey plan for an officer."

---

## 9. Questions to clear with the client

From our team's list (2 Oct) and the meeting. Our current assumption is in brackets.

1. **Fields when prospecting** (name, phone, GPS location; optional "where you met" and a note).
2. **Fields when generating a lead** (NIN, loan amount, location). Their meeting note says a lead exists once name and phone are captured; we call that a prospect, and make it a lead once NIN and amount are known. **Which do they mean?**
3. **Fields the relationship officer captures at the visit** (full KYC: details, NIRA ID and photos, income and collateral, CRB consent).
4. **The funnel they envisage** (Prospects → Leads generated → KYC completed; conversion = prospect became a client).
5. **The reports they envisage** (daily prospecting summary, weekly funnel, silent staff and geofence alerts, reasons report).
6. **Users:** sales agents, relationship officers and branch managers at branches; Head of Sales at HQ; a system admin. Anyone else?
7. **Branch manager's role:** create territories and routes, give agents routes, give officers leads to visit, see branch reports. Correct?
8. **Approval matrix:** committee, relationship officer, DSA, loan officer, managers at branch and/or head office. (Placeholder: branch manager up to UGX 10M, HQ above.)
9. **Roles matrix** at each approval level for prospecting, creating a lead and converting a lead to a client.
10. **Digital ID checks:** can National IDs and driving licences be authenticated through a NIRA gateway? Does Letshego have access?
11. **The loan calculator:** can we have the Excel sheet to digitise it?
12. **Targets:** prospect targets per route day (we used 40–50), and client targets per branch.

**Still open from the first demo:** real products, rates and the affordability rule; real branches, territories and routes; the loan system and its API.

---

## 10. Likely questions and short answers

**"What if there's no network?"** Everything saves on the phone, encrypted, with GPS, and syncs later. NIRA and CRB checks wait in a queue.

**"Can agents fake prospects?"** Each prospect carries GPS and time, and the phone number is checked for duplicates. Prospects far from the route or outside the territory are flagged.

**"Why split prospect and lead?"** Agents can capture a name in seconds on the street; the follow-up tells us who really wants a loan. Both numbers matter: one measures effort, the other interest.

**"Does the loan decision change the numbers?"** No. The prospect became a client when KYC was completed. Approval rates are reported separately.

**"What happens when someone leaves?"** Prospects, leads and clients belong to territories, not people. The branch manager gives the territory to someone else ([W12b](https://letshego-prototype.vercel.app/prototype.html#w12b)).

**"Is this built?"** No. It's a clickable prototype with illustrative data, to agree the workflow before building.

---

## 11. How we would build it

A proposal to discuss, not a commitment.

| Part | Proposal |
|---|---|
| Field app | Flutter, Android first. One app, screens by role (sales agent, relationship officer). Offline-first, background sync, GPS and geofencing, camera with GPS stamping, PIN/fingerprint sign-in, remote wipe, light and dark mode. |
| Web console | Dashboards, route and lead journey plans, pipeline, maps, approvals, locations, users. Access scoped by role and locations. Light and dark mode. |
| API and data | One back end; records owned by Letshego; full audit log; daily backups. |
| Integrations | Loan system, NIRA gateway, CRB, SMS. Each with a manual or file fallback. |
| Rollout | Demo → pilot at one or two branches (e.g. Kampala East) → all branches. Train branch managers first. |

---

## 12. Watch-outs before the demo

- **Say once, clearly, that all data is illustrative.** Names, figures, IDs and products are made up.
- **Lead with the funnel** (W01, then W01b): prospects, leads generated, KYC completed. That is what they asked to see.
- **Don't promise NIRA or CRB integration dates.** Access depends on Letshego's agreements.
- **Open the link while online** and wait for "✓ Offline-ready"; present full screen (**F**).
- **Light or dark:** pick one before you start (moon button, or **D**) and stay in it.
- The name switch in the console and the Sarah / Joel buttons on the app's sign-in are demo shortcuts. Don't present them as features.
