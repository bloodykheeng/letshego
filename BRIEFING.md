# Letshego Field Sales: team briefing

> **Internal · for our team only · do not share with Letshego.**
> What you need to understand the brief, speak the client's language, and walk through the prototype with confidence.
>
> **Prototype:** https://letshego-prototype.vercel.app. The screen links below open the right screen directly.

**Contents:** [1. 30-second version](#1-the-30-second-version) · [2. Words decoded](#2-the-words-they-will-use-decoded) · [3. The problem](#3-the-problem-and-how-they-define-success) · [3b. Visits & KYC](#3b-what-a-visit-is-and-when-kyc-happens) · [4. Client journey](#4-the-client-journey-and-where-each-stage-lives) · [5. What they asked for](#5-what-they-asked-for-and-where-it-is) · [6. Roles](#6-roles) · [7. Data flow](#7-how-data-moves) · [8. Walkthrough](#8-walkthrough-script-about-8-minutes) · [9. Questions for the client](#9-questions-and-assumptions-to-clear-with-the-client) · [10. Likely questions](#10-likely-questions-and-short-answers) · [11. How we would build it](#11-how-we-would-build-it) · [12. Watch-outs](#12-watch-outs-before-the-demo)

---

## 1. The 30-second version

- **Letshego Uganda** is a microfinance lender (Tier IV, head office in Kololo, Kampala). It lends to civil servants through payroll deductions, to micro and small businesses, and for school fees and housing. Its field sales agents find and sign up new borrowers.
- **The problem:** agents go out in the first week of the quarter, go quiet, then rush in the last three weeks to hit targets. Management can't see what agents do most of the quarter, which clients they visit, or why clients do or don't take a loan.
- **What they want:** an app agents use at every client visit, tracking each client from the first visit to the loan application and its approval, plus a dashboard that shows who is, and isn't, bringing in clients, by day, week, quarter or year.
- **Success, in their words:** a **conversion** is when the client agrees to apply and hands in every required item. Whether the loan is later approved doesn't change that.
- **Our ask:** propose and build a prototype for a demo (brief from Sam, Project Manager, 29 Sep 2026; agreement held by Nexa AI on the SalesCore platform).

---

## 2. The words they will use, decoded

| Term | What it means |
|---|---|
| **KYC** | **Know Your Customer.** Proving who the client is and whether they can repay: ID, photos, location, income, collateral. Required by the regulator before lending. |
| **NIRA / NIN** | **National Identification and Registration Authority**, Uganda's ID agency. Every adult has a **NIN** (National Identification Number) on their National ID card. "Take NIRA" on the whiteboard = capture the National ID. |
| **KYC validation** | Checking the KYC is true: the ID matches NIRA, the phone is in the client's name, the client isn't already a Letshego borrower, the income supports the loan. |
| **CRB** | **Credit Reference Bureau.** Holds each person's borrowing history. Lenders check it, with the client's consent, before lending. |
| **Check-off / payroll loan** | A loan repaid by deduction from the salary before it's paid out. Letshego started with civil servants this way. |
| **MSE** | **Micro and Small Enterprise**: shops, tailors, market vendors, boda boda owners. |
| **Conversion** | The success measure: client agrees and submits every required item. The **loan application ID** is captured at this point. |
| **Loan application ID** | The number Letshego's loan system gives an application. Capturing it in the app ties the field record to the real loan. |
| **Journey plan** | A **named list of clients** to visit, with an agent, start and end dates, a description and a goal (e.g. "Kiwatule follow-ups, 28 Sep – 2 Oct"). An agent can have several at once. The supervisor creates them, or the agent does and the supervisor approves. "Journey plan adherence" = planned client visits actually made; visits not on any plan count as **off-plan**. |
| **Region › Branch › Territory › Route** | Letshego's geography, as in NICE. A **territory** is a real area (e.g. Ntinda · Kiwatule) covered by one agent; it holds several **routes** (e.g. Kiwatule market). Every client sits on a route, placed automatically from GPS when registered, so each client falls under one territory and its agent. |
| **Affordability / DSR** | Whether the instalment fits the client's income. We show "instalment as a % of free income" (income minus expenses), with a 50% ceiling as a placeholder. |
| **SPLY** | **Same Period Last Year.** A comparison NICE's dashboards use; we show conversions "vs Q3 2025" on the overview. |
| **Silent agent** | Our word for an agent with no check-in for 14+ days. Not a client term. |

---

## 3. The problem and how they define success

The whiteboard session showed one pattern: **activity in week 1, a slump in the middle, a rush in weeks 11–13.** The overview's "Quarter rhythm" chart ([W01](https://letshego-prototype.vercel.app/prototype.html#w01)) draws exactly that, so management recognises their own problem in the first minute.

The fix has three parts, and each has a screen:

1. **See it:** every visit is GPS-stamped, so quiet weeks show up as empty cells on the agents table ([W02](https://letshego-prototype.vercel.app/prototype.html#w02)).
2. **Act on it early:** silent and behind agents are flagged every morning ([W01](https://letshego-prototype.vercel.app/prototype.html#w01), right-hand card).
3. **Prevent it:** supervisors plan which clients each agent visits every day, and the dashboard shows how much of the plan was kept ([W10](https://letshego-prototype.vercel.app/prototype.html#w10)).

> **The rule we must repeat:** a conversion counts when the application is submitted with every item. Approval is tracked separately. It appears on the overview, the approvals queue ([W07](https://letshego-prototype.vercel.app/prototype.html#w07)) and the close screen in the app ([M15](https://letshego-prototype.vercel.app/prototype.html#m15)).

---

## 3b. What a visit is, and when KYC happens

**A visit is what we track.** Every visit is a check-in at a client (GPS and time), a purpose, and an **outcome** recorded before check-out. That is what the dashboards count: visits, which clients, and what came of them.

**Why an agent visits depends on where the client is:**

| Client is at | Purpose of the visit | Possible outcomes |
|---|---|---|
| New (not in records) | Introduce Letshego, learn their needs, note products that might suit | Interested · needs time (follow-up) · not interested (why) |
| Interested | Collect documents and **take KYC** | KYC done · follow-up · no longer interested |
| KYC validated | Negotiate: choose the product, amount, term | Agreed · follow-up · declined (why) |
| Negotiation | Close: submit the application with every item | **Conversion** · declined (why) |
| Applied / approved | Follow up on the decision or disbursement | Relationship visit |
| Any | Client not available | Logged as a visit attempt |

**KYC is done during a visit, once per client, only after they say they're interested.** It is not part of adding a client. Adding a client ([M6](https://letshego-prototype.vercel.app/prototype.html#m06)) is light registration: name, phone, location, gender and age, type of work, how you met. That is enough to track them, plan visits and report demographics even if they say no, which most prospects do. KYC ([M10](https://letshego-prototype.vercel.app/prototype.html#m10)–[M13](https://letshego-prototype.vercel.app/prototype.html#m13)) is the heavy step: NIRA ID, selfie, income, collateral, CRB consent. It can happen on the first visit if the client is ready with documents, or on a later visit, like Florence's.

---

## 4. The client journey and where each stage lives

The stages come straight from the whiteboard (Figure 1 in the brief).

| # | Stage | In the agent app | In the web console |
|---|---|---|---|
| 1 | Agent visits client (location / territory) | Choose the client from today's plan or add a new one: [M5 Start a visit](https://letshego-prototype.vercel.app/prototype.html#m05) → [M6 New client](https://letshego-prototype.vercel.app/prototype.html#m06) → [M7 First visit](https://letshego-prototype.vercel.app/prototype.html#m07), or a returning client → [M9 Visit](https://letshego-prototype.vercel.app/prototype.html#m09) | [W10 Journey plans](https://letshego-prototype.vercel.app/prototype.html#w10) · [W04 Field map](https://letshego-prototype.vercel.app/prototype.html#w04) |
| 2 | Interested? **No → end, capture why** | Asked on the first visit: [M7](https://letshego-prototype.vercel.app/prototype.html#m07) → No → [M8 Capture why](https://letshego-prototype.vercel.app/prototype.html#m08) | [W09 Why & why not](https://letshego-prototype.vercel.app/prototype.html#w09) |
| 3 | Take KYC: coordinates, photos, NIRA ID, earnings, collateral, demographics | [M10](https://letshego-prototype.vercel.app/prototype.html#m10) · [M11](https://letshego-prototype.vercel.app/prototype.html#m11) · [M12](https://letshego-prototype.vercel.app/prototype.html#m12) | [W06 Client record](https://letshego-prototype.vercel.app/prototype.html#w06) |
| 4 | KYC validation | [M13](https://letshego-prototype.vercel.app/prototype.html#m13): 6 automatic checks | W06, validation checks |
| 5 | Negotiation: loan product(s) chosen | [M14](https://letshego-prototype.vercel.app/prototype.html#m14): suggested products, calculator, agent's note | [W05 Pipeline](https://letshego-prototype.vercel.app/prototype.html#w05) |
| 6 | Close: application ID captured = **conversion**. **No → end, capture why** | [M15](https://letshego-prototype.vercel.app/prototype.html#m15) → [M16](https://letshego-prototype.vercel.app/prototype.html#m16) | [W01 Overview](https://letshego-prototype.vercel.app/prototype.html#w01) |
| 7 | Supervisor / HQ approval → approved, or rejected with reason | [M18](https://letshego-prototype.vercel.app/prototype.html#m18) shows the status | [W07](https://letshego-prototype.vercel.app/prototype.html#w07) → [W08](https://letshego-prototype.vercel.app/prototype.html#w08) |

---

## 5. What they asked for and where it is

| The brief says | Where it is | Point to make |
|---|---|---|
| An app for field agents to use at client visits | [M1–M19](https://letshego-prototype.vercel.app/prototype.html#m01) | Android app (Flutter). Works offline, GPS, camera. |
| Track each client from first visit to application and approval | [W05](https://letshego-prototype.vercel.app/prototype.html#w05), [W06](https://letshego-prototype.vercel.app/prototype.html#w06), [M18](https://letshego-prototype.vercel.app/prototype.html#m18) | One timeline per client, every step with who, when and where. |
| KYC: coordinates, photos and IDs (NIRA), earnings, validation, collateral | [M10–M13](https://letshego-prototype.vercel.app/prototype.html#m10) | NIN read from the card; NIRA match; face match; affordability check. |
| Demographic data and agent's notes on suitable products | [M10](https://letshego-prototype.vercel.app/prototype.html#m10), [M14](https://letshego-prototype.vercel.app/prototype.html#m14), [W09](https://letshego-prototype.vercel.app/prototype.html#w09) product-fit grid | Notes feed a product-fit view by client type. |
| Loan product(s) chosen and the loan application ID | [M14](https://letshego-prototype.vercel.app/prototype.html#m14), [M15](https://letshego-prototype.vercel.app/prototype.html#m15) | The app checks the ID against the loan system (proposed). |
| Notes on why clients took a loan, and why not | [M8](https://letshego-prototype.vercel.app/prototype.html#m08), [M15](https://letshego-prototype.vercel.app/prototype.html#m15), [W09](https://letshego-prototype.vercel.app/prototype.html#w09) | Tap-to-pick reasons plus a free note (or voice note). |
| Client records stay with Letshego if an agent leaves | [W11 Locations](https://letshego-prototype.vercel.app/prototype.html#w11) → [W12 Users](https://letshego-prototype.vercel.app/prototype.html#w12) → [W12b Edit user](https://letshego-prototype.vercel.app/prototype.html#w12b) | Clients belong to routes and territories, not agents. Locations are set up once ([W11](https://letshego-prototype.vercel.app/prototype.html#w11), [W11b new route](https://letshego-prototype.vercel.app/prototype.html#w11b)) and given to people in the user form, like NICE. When an agent leaves, tick their territory on another agent's user page: every client, route and running plan moves in one step. |
| Applications go to supervisors or HQ for approval | [W07](https://letshego-prototype.vercel.app/prototype.html#w07), [W08](https://letshego-prototype.vercel.app/prototype.html#w08) | Branch limit decides whether HQ is needed (UGX 10M placeholder). |
| Dashboard by day, week, quarter or year: who isn't bringing in clients | [W01](https://letshego-prototype.vercel.app/prototype.html#w01), [W02](https://letshego-prototype.vercel.app/prototype.html#w02), [W03](https://letshego-prototype.vercel.app/prototype.html#w03) | The Day / Week / Quarter / Year switch is in the top bar of every screen. |
| Agents add new clients in the field | [M6 New client](https://letshego-prototype.vercel.app/prototype.html#m06), also from [M17 My clients](https://letshego-prototype.vercel.app/prototype.html#m17) | Duplicate check on the phone number before saving. |
| Supervisors decide which clients agents visit | Web: [W10 all plans](https://letshego-prototype.vercel.app/prototype.html#w10) → [W10b one plan](https://letshego-prototype.vercel.app/prototype.html#w10b) · [W10c new plan](https://letshego-prototype.vercel.app/prototype.html#w10c). App: [M4 my plans](https://letshego-prototype.vercel.app/prototype.html#m04) → [M4b plan](https://letshego-prototype.vercel.app/prototype.html#m04b) · [M4c agent creates a plan](https://letshego-prototype.vercel.app/prototype.html#m04c) | Named client lists with dates; Home shows what's due today across plans. Adherence on [W01](https://letshego-prototype.vercel.app/prototype.html#w01) and [W02](https://letshego-prototype.vercel.app/prototype.html#w02). |

**Extras we added (say so, don't oversell):** live field map with agent trails (idea from the NICE sell-out map), journey plan adherence (also a NICE idea), scheduled reports, audit trail.

---

## 6. Roles

| Role | Person in the prototype | What they do | Sees |
|---|---|---|---|
| **Field Sales Agent** | Sarah Namuli, Kampala East | Visits, KYC, negotiation, submits applications | Own clients only |
| **Branch Supervisor** | Moses Okello, Kampala East | Approves applications, creates journey plans, assigns territories to agents | Their branch |
| **Regional Manager** | (not shown) | Oversees several branches | Their region |
| **HQ Credit Approver** | (not shown) | Decides loans above the branch limit | All, above limit |
| **Head of Sales / Management** | Patricia Nankya | Watches performance and acts on silent agents | All branches |
| **System Admin** | (not shown) | Users, devices, settings | Settings only |

In the web console, **click the name at the bottom left** to switch between Patricia (management) and Moses (supervisor). That's a demo shortcut, not a real feature.

---

## 7. How data moves

```
1 FIELD                 2 VALIDATION              3 APPLICATION             4 DECISION              5 MANAGEMENT
Agent checks in with →  NIRA, phone, CRB,     →   Agent captures the    →   Supervisor or HQ    →   Dashboards, alerts,
GPS; captures KYC,      duplicate and             loan application ID       approves, returns       reasons, reports
photos, notes           affordability checks      = CONVERSION              or rejects (reason)
(works offline)         (queued if offline)
```

Everything is stored on Letshego's servers, not only on the phone. Every change goes into the [audit trail](https://letshego-prototype.vercel.app/prototype.html#w13).

---

## 8. Walkthrough script (about 8 minutes)

1. **[W00 Sign in](https://letshego-prototype.vercel.app/prototype.html#w00):** "One sign-in for head office, branches and the field, with two-step verification."
2. **[W01 Sales overview](https://letshego-prototype.vercel.app/prototype.html#w01):** "This is the quarter you described: week 1 busy, the middle quiet, the rush at the end. Here's the funnel from visit to application, and the agents who need a call today."
3. **[W02 Agents](https://letshego-prototype.vercel.app/prototype.html#w02):** "Each row is an agent; each little square is a week. Red outlines are weeks with no visits. You see the slump per person, not just in total."
4. **[W04 Field map](https://letshego-prototype.vercel.app/prototype.html#w04):** "Where agents are right now and every visit today, coloured by outcome." Click the popup → **[W06](https://letshego-prototype.vercel.app/prototype.html#w06)**.
5. **[W06 Client record](https://letshego-prototype.vercel.app/prototype.html#w06):** "Florence's whole story: first visited by John, who left; the record stayed with Letshego and moved to Sarah. KYC photos, checks, and the application."
6. **Switch to the app** (bottom bar, *Agent app*): [M3 Home](https://letshego-prototype.vercel.app/prototype.html#m03) shows what's due today from Sarah's [journey plans](https://letshego-prototype.vercel.app/prototype.html#m04) → yellow **Visit** button → [M5 choose the client](https://letshego-prototype.vercel.app/prototype.html#m05).
   - **New client:** [M6 register Joseph](https://letshego-prototype.vercel.app/prototype.html#m06) (light details, no KYC) → [M7 first visit](https://letshego-prototype.vercel.app/prototype.html#m07): needs and products that might suit → "No" → [M8 capture why](https://letshego-prototype.vercel.app/prototype.html#m08) → check out. "We always capture why."
   - **Returning client:** Florence → [M9 visit](https://letshego-prototype.vercel.app/prototype.html#m09): where she is in the journey, why Sarah is there, what happened. She's ready, so KYC [M10](https://letshego-prototype.vercel.app/prototype.html#m10)–[M12](https://letshego-prototype.vercel.app/prototype.html#m12) → [M13 validated](https://letshego-prototype.vercel.app/prototype.html#m13) → [M14 product](https://letshego-prototype.vercel.app/prototype.html#m14) → [M15 close](https://letshego-prototype.vercel.app/prototype.html#m15) → [M16 conversion and check-out](https://letshego-prototype.vercel.app/prototype.html#m16). Finish on [M18](https://letshego-prototype.vercel.app/prototype.html#m18), her record.
7. **Back to the web** as Moses: [W07 Approvals](https://letshego-prototype.vercel.app/prototype.html#w07) → [W08 Decision](https://letshego-prototype.vercel.app/prototype.html#w08). "Conversion already counted; the decision is separate."
8. **[W09 Why & why not](https://letshego-prototype.vercel.app/prototype.html#w09):** "What agents hear in the field, turned into numbers for product and pricing."
9. **[W10 Journey plans](https://letshego-prototype.vercel.app/prototype.html#w10):** "Every plan is a named list of clients with dates and a goal. Open one ([W10b](https://letshego-prototype.vercel.app/prototype.html#w10b)): who has been visited, what happened, what's due, on a map. Creating one ([W10c](https://letshego-prototype.vercel.app/prototype.html#w10c)) means picking clients from the pipeline. The agent sees the same plans on the phone ([M4](https://letshego-prototype.vercel.app/prototype.html#m04) → [M4b](https://letshego-prototype.vercel.app/prototype.html#m04b))."
10. **[W11 Locations](https://letshego-prototype.vercel.app/prototype.html#w11) → [W12 Users](https://letshego-prototype.vercel.app/prototype.html#w12) → [W12b Edit Peter](https://letshego-prototype.vercel.app/prototype.html#w12b):** "Letshego's geography is Region › Branch › Territory › Route, set up once. People get their locations in the user form. Daniel is leaving today, so Moses ticks Daniel's territory on Peter's page: 46 clients, 4 routes and the running plan move in one step."

---

## 9. Questions and assumptions to clear with the client

The brief asks us to bring these. Our current assumptions are in brackets; each is easy to change.

**Process**
- Does a conversion need the loan application ID at submission, or can it follow later? (We assumed at submission.)
- Who approves what: branch supervisor up to what amount, HQ above? (Placeholder: UGX 10M branch limit.)
- Can a supervisor return an application for more documents without losing the conversion? (We assumed yes.)
- How are territories drawn today: by area, by employer (for payroll loans), or both?

**Products and rules**
- The real product list, amounts, terms and rates. (We used five illustrative products and 2.9% a month only for the calculator.)
- The affordability rule. (Placeholder: instalment up to 50% of free income.)
- Which items are "required" per product? (We used 7 for an MSE loan.)

**Systems**
- Which loan system issues the application ID, and can we read from it by API? If not, a daily file works for the pilot.
- NIRA verification: does Letshego already have access through a gateway? Same for CRB.
- Is SalesCore (under the Nexa AI agreement) the platform we must build on, or can we propose the stack?

**People and devices**
- How many agents, supervisors and branches? (We showed 62 agents, 14 branches; illustrative.)
- Company phones or agents' own phones? Android only? (We assumed company Android phones.)
- Languages needed in the app. (English first; Luganda offered.)

**Data**
- Data retention and consent wording under the Data Protection and Privacy Act, 2019.
- Do they want past clients (before the app) imported?

---

## 10. Likely questions and short answers

**"What if the agent has no network?"**
The app saves everything on the phone, encrypted, including GPS and photos, and syncs when it's back online. Checks that need the internet (NIRA, CRB) wait in a queue.

**"Is KYC taken when the agent adds a client?"**
No. Adding a client is quick registration. KYC is taken on a visit once the client is interested, and only once.

**"Can agents fake visits?"**
Check-in needs GPS within a set distance of the client, and photos are taken in the app with GPS and time stamps; they can't be picked from the gallery. The map shows each agent's trail.

**"What happens to clients when an agent leaves?"**
They never belonged to the agent; they belong to a territory. The supervisor gives the territory to another agent in one step ([W11](https://letshego-prototype.vercel.app/prototype.html#w11)); the new agent sees every client with the full history, and the old phone is wiped.

**"Does approval change the agent's numbers?"**
No. The agent's conversion counts at submission, as Letshego defined it. Approval rates are reported separately.

**"Is this built?"**
No. It's a clickable prototype with illustrative data, to agree the workflow before building.

**"Can it work with our loan system?"**
Yes, by API if available, or by a scheduled file. We agree the method during kickoff.

**"Why Flutter?"**
One codebase for a real Android app with offline storage, camera and GPS; iPhone later without a rewrite.

---

## 11. How we would build it

A proposal to discuss, not a commitment.

| Part | Proposal |
|---|---|
| Agent app | Flutter, Android first. Offline-first local database, background sync, camera with GPS stamping, fingerprint/PIN sign-in, remote wipe. |
| Web console | Dashboards, approvals, pipeline, maps, plans, users. Role- and territory-based access. |
| API and data | One back end for app and web; client records owned by Letshego; full audit log; daily backups. |
| Integrations | Loan system (application ID and status), NIRA gateway, CRB, SMS. Each with a manual or file fallback. |
| Rollout | Demo → pilot at one or two branches (e.g. Kampala East) → all branches. Train supervisors first. |

---

## 12. Watch-outs before the demo

- **Say once, clearly, that all data is illustrative.** Names, figures, IDs and products are made up. The branch list is plausible but not Letshego's real network.
- **Brand colours were sampled from Letshego's LetsGo app** (indigo #2F2E80, yellow #FBD405, the triangle mark). Ask for their brand guidelines before any production design.
- **Don't promise NIRA or CRB integration dates.** Access depends on Letshego's agreements.
- **Open the link while online** and wait for "✓ Offline-ready" in the bottom bar; present full screen (**F**).
- The client asked about "who is not bringing in clients". Lead with W01 → W02; that is their pain.
