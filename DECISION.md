# Decision and reasoning

## The decision

**Unify the engine and the data. Do not unify the rules. Deploy reconciliation
before migration.**

Concretely: one canonical absence record, one balance calculation, one audit
trail and one employee experience across every entity that matters. The accrual
formulas, entitlement tiers, leave-year definitions, expiry deadlines, holiday
calendars and sick-pay bands stay local - but they move out of spreadsheets and
local knowledge into versioned, dated, human-reviewable policy files that the
shared engine reads.

And the first thing that ships is not a migration. It is a recomputation that
runs *alongside* each entity's existing process and reports where the two
disagree.

---

## 1. What the numbers actually say

Two findings shaped everything that follows.

**Entity count is not the problem; employee concentration is.** Groupon's
Exhibit 21.1 lists around 40 subsidiaries, but the company operates consumer
sites in 13 countries and employed 1,734 people at the end of FY2025 - 421 in
North America and 1,313 in International. The 10-K names Poland as a shared
services hub, and Exhibit 21.1 shows a dedicated Indian shared services entity.
So the population is concentrated in a handful of entities while the long tail
is holding companies, IP entities and wound-down trading entities with no
payroll at all.

Treating "absence management across our legal entities" as a 40-entity problem
would mean forty policy sets, forty annual legal reviews and forty migrations
to serve a few hundred people. `policies/registry.yaml` classifies all of them
instead: **six entities carry roughly 88% of employees**, and those six are what
the engine covers in v1.

**The differences between jurisdictions are real, but they are parametric.**
They are not forty bespoke systems; they are the same small set of dimensions
with different values:

| dimension | how much it varies |
|---|---|
| entitlement amount | PL 20 or 26; IN 12–21 by state; DE 20; NL 4 x weekly hours; US none |
| what drives the amount | tenure, tenure *plus education*, hours worked, state of work, contract |
| leave year | calendar (PL, DE, NL), April–March (IE), anniversary |
| unit | working days, calendar days, weeks, hours |
| carry-forward | unlimited, capped, forbidden |
| expiry | 30 Sep (PL), 31 Mar (DE), 6 months (NL statutory), 5 years (NL supplementary), never (US-CA) |
| forfeiture conditions | automatic, or only if the employer proved it warned the employee (NL, DE post-*Max-Planck*) |
| holiday calendar | national, or sub-national (DE Bundesland, ES región, CH canton, IN state) |
| sick pay | employer-funded 33 days in PL, 14 if the employee is 50 or over |

That table is the entire argument for the architecture. If the variation were
arbitrary, you would need one system per country. Because the variation lives
on a fixed set of axes, one engine can serve all of them provided the axes are
data rather than code.

Three specifics that a "just harmonise it" plan would break on:

- **Poland.** The 10-year threshold that moves entitlement from 20 to 26 days
  counts previous employers *and completed education* - a master's degree is
  worth eight years. None of that is derivable from Groupon's own records. It
  depends on documents the employee hands in.
- **India.** Entitlement follows the state Shops & Establishments Act of the
  place of work, not the place of incorporation. One legal entity, four regimes.
  Earned leave above the carry cap must be *paid out*, not forfeited.
- **Netherlands.** Statutory days lapse six months after the year they accrued;
  contractual days five years later. And the statutory forfeiture only bites if
  the employer can show it told the employee. "No record of a warning" has to
  mean the days survive.

Sources for all of the above are listed at the end.

---

## 2. Where I drew the unification boundary

**Global - one version for the whole company:**
the absence event model and taxonomy; the balance engine; the audit trail and
the explanation of how each number was derived; the reconciliation and reporting
layer; the approval workflow and the employee-facing experience.

**Local - but as versioned data, not as spreadsheets or local knowledge:**
accrual method and amounts; entitlement tiers and what counts towards them;
leave-year definition; carry-forward and expiry rules; rounding; sub-national
holiday calendars; sick-pay bands; payout-on-termination rules.

**Explicitly excluded from v1:**

- *A big-bang migration into one HRIS.* This is the risk the brief itself names.
  It also does not remove any work: whichever system you buy, someone still has
  to encode Poland's education credit and India's state variants, and you would
  be doing it inside a vendor's configuration language rather than in a file a
  lawyer can read.
- *Harmonising entitlements upward to a global standard.* Attractive on a slide,
  irreversible in practice. It is a permanent cost increase, and in Germany,
  France, Italy and the Netherlands it is a change to terms that requires works
  council or union consultation. If it is ever done, it should be done as a
  benefits decision with its own business case - not smuggled in as a side
  effect of a systems project.
- *Payroll integration.* Absence balances feed payroll for encashment and final
  settlements. Wiring that up before the balances themselves are trusted would
  propagate today's errors into people's pay.
- *The 26 dormant entities and the 9 small ones.* Named, owned and attested
  annually, but not configured. A stale, unreviewed policy file is more
  dangerous than a small entity continuing under an accountable human.

**The single sentence version:** the decision is not "which system do we buy",
it is "what is the one true record, who owns each rule, and how does a rule
change get reviewed".

---

## 3. Why the build has the shape it has

The obvious build is a rules engine. That is necessary but not sufficient,
because a rules engine on its own is a proposal - it produces numbers nobody has
a reason to trust yet, and it only becomes useful after a migration.

So the centre of this build is **reconciliation**. It reads each entity's
current file, in whatever shape that entity keeps it, recomputes the same
population from the canonical ledger and the entity's own policy, and reports
where they disagree and what most likely caused it.

That inverts the usual sequence, deliberately:

- A migration that starts by moving balances moves the errors with them, and
  the new system gets blamed for numbers it inherited.
- Running the recomputation alongside the live process surfaces the errors while
  the old process is still the system of record - the only point at which they
  are cheap to fix and nobody's pay is at stake.
- It gives the entities a reason to trust the engine before they are asked to
  depend on it. They can see it agree with them on the easy cases first.

On the shipped synthetic data, across three entities and 38 employees, the
reconciliation produces 68 findings: 61 comparable records at a 74% match rate,
16 material differences totalling 60 days in dispute (net 18 days *under-stated*
on the local sheets), and 7 records where the engine refuses to produce a number
at all. Those figures describe the seeded dataset, not Groupon - the deliverable
is the method, not the number.

Four design choices inside the build are worth defending explicitly.

**Rules as YAML, not as code or database rows.** A policy change is a legal
change and needs sign-off from someone who is not an engineer. A YAML diff is
readable by a lawyer; a code diff or an `UPDATE` statement is not. Every version
carries `effective_from`, so any balance can be recomputed exactly as it stood
on any past date - which is what makes an audit survivable after the rules have
moved.

**`unknown` is a first-class answer.** Where the law makes entitlement depend on
evidence the employer does not hold, the engine reports UNKNOWN and refuses to
guess. Silently defaulting a Polish graduate to 20 days under-grants six days a
year, compounds, and surfaces as a claim at termination. The same rule applies
to opening balances: an employee who predates the ledger cut-over with no
signed-off starting balance is UNKNOWN, not zero. This deliberately makes the
first report look worse. That is the point - the alternative is a clean-looking
report that is wrong.

**Balances are tracked as dated lots, not as one number.** Expiry attaches to
the year the days were earned in. The Netherlands alone makes a single running
total unworkable: two pots, six months and five years. A system that stores one
number cannot answer "how many days does this person actually lose on 1 July",
which is the only question worth asking.

**The review page is a file, not an application.** `absence dashboard` writes
one self-contained HTML file with the figures, the calculation trace and the
reconciliation findings baked in. That shape follows from who has to open it: a
country HR lead on a call, a works council member, a lawyer checking a rule.
None of them will install anything, and a server running on somebody's laptop
is not a thing you can send to a works council. Opened inside a Claude artifact
viewer the same file also offers a panel that puts the calculation trace into
plain language - it reads the trace the engine produced and never computes
anything, which is the same line section 8 draws. The page renders identically
without it.

**The annual update produces a diff, never an applied change.** The brief names
annual updates as a specific pain. `annual-update` finds what has changed -
missing or unconfirmed holiday calendars, people crossing a seniority threshold
and when, policies past their review date, missing opening balances - assigns
each to a named owner, and applies nothing. The mechanical part (finding out
what changed) is automated; the judgement (approving it) is not.

---

## 4. Assumptions

These are assumptions, not findings. Each one is falsifiable and several are
probably wrong.

1. **Per-entity headcount.** The 10-K gives only a North America / International
   split. The figures in `registry.yaml` are working assumptions. They drive the
   engine/register/dormant classification, so if they are wrong the boundary
   moves.
2. **The dormant classification.** I inferred it from entity names and Groupon's
   market exits. Some "dormant" entities may still employ people.
3. **There is a payroll system of record per entity** that can produce an
   employee extract. Without that there is no ledger and nothing to reconcile.
4. **No existing global HRIS.** If Groupon already runs Workday or similar, this
   should be a layer beside it - the policy files and the reconciliation stay,
   the ledger becomes a read from that system. See section 6.
5. **Working patterns are Monday–Friday**, with part-time modelled as a fraction
   of a five-day week. Real schedules change deductions for part-timers.
6. **Ireland uses contracted hours as a proxy** for hours actually worked in the
   8% calculation. Correct for salaried staff, wrong for irregular hours - every
   affected balance carries a flag saying so.
7. **A Polish employee reaching 10 years mid-year gets the higher tier for that
   whole leave year.** Defensible, arguably generous, needs counsel's view.
8. **The cut-over date is 1 January 2024.** Everything before it is a signed-off
   opening balance, not a recomputation, because that history does not reliably
   exist.

## 5. What must be verified before this could ship

| # | To verify | How |
|---|---|---|
| 1 | Real headcount by legal entity and by work location | Payroll extract per entity; India needs state of work, Germany needs Bundesland |
| 2 | Every policy file, rule by rule | Local counsel per jurisdiction signs the file; the `reviewed_by` and `review_due` fields exist to be filled in, and `annual-update` flags them as blockers until they are |
| 3 | Which entities actually employ people | Company secretarial confirmation against Exhibit 21.1 |
| 4 | Opening balances | Each entity signs off the balance at cut-over; unsigned means UNKNOWN, and that backlog is real work |
| 5 | The admin-effort estimate | Two-week time diary in two entities plus 12 months of leave-related service-desk tickets (see CHANGE_PLAN.md) |
| 6 | Works council position in DE and NL | Before, not after, any process change is announced |
| 7 | Whether the reconciliation's error classes are the real ones | Run it against one entity's live file in read-only mode for one cycle |

## 6. Known gaps in v1

- No approval workflow and no employee self-service. `absence dashboard`
  produces a read-only review page for the phase-0 audience - the HR analyst,
  the country lead, the lawyer checking a rule - but requesting and approving
  leave is still wherever it is today. The employee-facing interface belongs in
  phase 2, after the balances are trusted; building it earlier would be a
  window onto figures this project has just demonstrated are wrong.
- No payroll write-back.
- Poland's three-year limitation period is not modelled (it only matters in
  disputes). India's per-state festival calendars are national holidays only,
  and are flagged as unconfirmed rather than quietly incomplete.
- Parental, unpaid and special leave exist in the taxonomy but have no accrual
  rules; only annual leave, casual/sick quotas and Polish sick pay are computed.
- Absences are attributed to the leave year containing their start date. A
  spell that straddles a year boundary should be split.
- The engine assumes an absence event carries a day count. Deriving days from
  dates and a working pattern exists (`working_days_between`) but is not yet
  wired into ingestion.

## 7. Where I think I am most likely wrong

The brief asks for a specific correction, so here is where I would look first.

1. **The systems assumption.** If a global HRIS already exists, building a
   standalone ledger is the wrong shape. The policy-as-data layer and the
   reconciliation survive that; the ledger does not. This is the assumption I
   would most like corrected, and I did not ask about it because it did not feel
   like a question I could ask without also asking you to make my decision.
2. **The boundary may be drawn too tight.** Nine entities with roughly 200 people
   sit in `register_only`. If several share a jurisdiction with an engine entity,
   configuring them costs almost nothing and my "small entities are cheaper left
   alone" reasoning is just wrong for them.
3. **Sick leave may be the bigger prize.** I made annual leave the centre. In an
   organisation with large populations in Poland and India, employer-funded sick
   pay bands and state-level sick quotas may consume more admin time and carry
   more cost exposure than annual leave does.
4. **Reconciliation-first may be too slow for the sponsor.** It is the right
   engineering sequence and the right risk sequence. It is also a plan whose
   first visible output is a list of problems, which is a hard thing to fund.

## 8. How AI was used

Research: mapping Groupon's legal entity structure from SEC filings (Exhibit
21.1 and the FY2024/FY2025 10-Ks), and assembling the jurisdictional comparison
- Polish seniority and sick-pay bands, Indian state entitlements, Dutch dual
expiry, German and Irish specifics. That work would have taken most of a week by
hand and took about an hour. Drafting: the code, the policy schema and these
documents were written with an AI agent in the loop throughout.

What I did not delegate: the unification boundary, the decision to make
reconciliation rather than migration the first deliverable, the choice to let
the engine return `unknown`, and the judgement about which entities matter. Nor
would I put AI in the calculation path of a compliance-bearing number - the
engine is deterministic, its output is fully traced, and every figure can be
explained rule by rule.

The genuine leverage is elsewhere, and it is the reason policy-as-data pays for
itself: it turns the annual legal review from *re-implement the rules* into
*approve a diff*. An agent can draft next year's change from published
legislative sources; a lawyer approves or rejects it. That is a defensible use
of AI in a compliance process, and it is the part that scales to the other
entities later.

---

## Sources

- Groupon, Inc. Form 10-K for FY2025 (filed March 2026) - country count,
  employee numbers by segment, human capital section, Poland shared services.
- Groupon, Inc. Form 10-K for FY2024 and **Exhibit 21.1, Subsidiaries of
  Groupon, Inc.** - the legal entity list used in `policies/registry.yaml`.
- Groupon Q4 and FY2025 earnings release - revenue, headcount at year end.
- Polish Labour Code (Kodeks pracy) arts. 152–173 and 92 - entitlement tiers,
  service including education, 30 September carry-over, employer-funded sick pay
  of 33 days (14 from age 50).
- State Shops & Establishments Acts (Karnataka, Maharashtra, Delhi, Tamil Nadu)
  and Factories Act 1948 s.79 - Indian earned, casual and sick leave.
- Dutch Civil Code arts. 7:634–7:645 - four times weekly hours, six-month
  statutory expiry conditional on employer notice, five-year supplementary.
- Bundesurlaubsgesetz ss.3 and 7; ECJ C-684/16 (*Max-Planck*) - German minimum,
  31 March carry-over, the duty to inform before leave can lapse.
- Organisation of Working Time Act 1997 s.19 (Ireland) - 8% of hours worked
  capped at four weeks, April–March leave year.
- California Labor Code s.227.3 - accrued vacation as earned wages.
