# Change & Culture Plan

## 1. What this change is, and the norm it is meant to establish

This is not an efficiency programme. If it were, it would not be worth doing:
the manual effort it removes is under one full-time role across a company of
1,734 people, and section 6 says so with the arithmetic attached.

What it is, is the first process in this company rebuilt so that the rules are
written down, the calculation is reproducible, and the reason for any number can
be shown to the person it applies to. Absence was chosen because it is small
enough to fail safely and legally consequential enough that getting it right
matters. No revenue depends on it. That is the point.

The claim made to the organisation is therefore narrow, and stays narrow:

> One task inside HR's week stops being manual. The job does not change. What
> changes is that we now know how to do this to a second process, and a third.

**The norm.** Every project teaches the organisation how the next one will be
judged, whether anyone intends it or not. This one is meant to teach two things:

1. **We write the rules down, and when the calculation disagrees with us we
   correct in the direction the evidence points — including when that costs us
   money.** Section 6 shows the corrections netting out as money owed to
   employees rather than recovered from them. If that is not honoured the first
   time, nothing else here means anything.
2. **AI is judged here by whether it makes the truth cheaper, not by whether it
   removes people.** The first thing this AI project does is find its own
   department's errors. That is a chosen opening move, and it sets the bar for
   what follows.

Both are cheap to state and expensive to honour, which is why they are stated
before the first finding exists rather than after.

Two constraints follow. **No promise is made that cannot be kept** — no headcount
case, no "HR becomes strategic"; the people maintaining these spreadsheets have
seen systems projects before. And **the success measure is not the absence
numbers** (section 6).

### Who is affected, and how much

| Group | Size | What changes for them |
|---|---|---|
| HR administrators maintaining the spreadsheets | a handful, in PL and IN | The most. One recurring task shrinks to exception handling. The role does not change. This is the group the plan is really about, and the group most likely to be told a comfortable version of the truth. |
| Country HR leads and HRBPs | ~10–15 | Become the named owner of a policy file with a review date. New accountability, and real work: 1–2 days per entity in year one. |
| Works councils (NL, then DE) | 2 bodies | A consultation gate, not an audience. |
| Managers | all | Approvals stay where they are. But in the pilot entity they will be asked about corrected balances, so they are briefed before their people are told (section 3). |
| Employees | 1,734 | Nothing, except a small number told their balance was wrong. |
| Payroll | small | Nothing in v1. Gains a reliable source for encashment later. |

The employee row carries the risk. A corrected leave balance is not a systems
change to the person receiving it; it is a change to something they had already
planned their year around.

---

## 2. ADKAR across the audiences

ADKAR is used here not as a framework to display but because it forces the
question *which specific element is missing for this specific group* — and the
answer differs sharply.

| Audience | Awareness | Desire | Knowledge | Ability | Reinforcement |
|---|---|---|---|---|---|
| HR administrators (PL, IN) | Easy | **Gap** — they own the exceptions the engine does not know about, and nothing compels them to hand those over | Moderate — must learn to read a trace and judge a discrepancy | Moderate | **Gap** — if nobody reads the reconciliation after month 3, they go back to the sheet |
| Country HR leads / HRBPs | Easy | Mixed — reads as headquarters taking their process | Low — few have signed off a rule as *written text* before | **Gap** — signing a policy file needs counsel time nobody has budgeted | Moderate — the `review_due` date is the mechanism |
| Managers | Easy | Neutral | Low — need one page, not training | Fine | n/a |
| Works councils (NL, DE) | Formal, by law | Neutral at best; their job is to test it | **Gap** — need to understand what the system does and does not observe | n/a | The agreement itself |
| Employees | Low need | n/a | Low | n/a | n/a |
| HR leadership / sponsor | Easy | Present | Moderate | Moderate | **Gap** — a slow project with no employee-facing output for two quarters loses attention before it produces a result |

**Awareness is close to free here; Desire is not.** Those are different claims.
Groupon's leadership has taken a public, repeated position that AI fluency is
expected of everyone rather than delegated to a function, so I do not have to
spend the first month arguing that using AI is legitimate — which is a large
share of what a change plan usually spends its energy on. But that is a stance
on direction, not a permission slip: it settles nothing about AI and employee
data (hence section 3), and it has no bearing on whether one administrator
volunteers the exceptions she has handled by hand for six years. Her desire is
the hardest problem in this plan.

So the standard playbook — town hall, vision deck, awareness campaign — would
aim at the element that is already fine. This plan spends almost nothing there.

**Ability is budget and time, not enthusiasm.** A country HR lead cannot sign a
policy file without counsel, and counsel is not free (section 6 sizes it). Unfunded
in week 1, the files go unsigned and the engine runs on rules nobody approved —
worse than the spreadsheet it replaced.

**The instrument for Knowledge and Ability is the review page, not a deck.**
`absence dashboard` writes one self-contained HTML file: every balance, the trace
behind it, the reconciliation findings, the year-ahead list. It opens on any
laptop with no install and no server, so it can be sent to a country lead, a
lawyer or a works council member and they can click into it alone, at their own
pace, on their own colleagues' records. Nobody is onboarded into a rules engine
by a presentation; they are onboarded by opening a file, finding someone they
know, and seeing why that person's number is what it is. That is the most useful
change instrument this project has, and it is why it is a file rather than an
application.

**Reinforcement decides whether this survives me.** A reconciliation nobody reads
is a report generator. Three mechanisms: the match rate joins the monthly HR pack
from month 2, permanently; `review_due` blocks publication when overdue; and the
handover gate (section 8) does not open until someone else has run a full annual
cycle.

---

## 3. Communication

The sequencing principle: **nobody hears about their own balance from a system.
Every person whose number changes hears it from a human who can answer "why",
and that human hears it before the population does.**

| When | Audience | Message | From |
|---|---|---|---|
| Week 0 | Administrators who own the spreadsheets (PL, IN) — before the pilot entity, because they will hear about it anyway | One-to-one. What is being built, what it does to their week, what it does not do, and that they are being asked to help build it. | Their own manager, with me present for detail |
| Week 1 | Country HR leads and HRBPs | The approach, the boundary, and the ask: you own a policy file and you sign it with counsel. Including what that costs in time and budget. | HR leadership |
| Week 2 | NL works council (OR) | Formal notification, before the pilot. Entitlement does not change; what changes is how balances are calculated and verified. | NL country HR lead plus counsel |
| Week 3 | External counsel, NL first | The policy file, with a specific request: confirm or correct these rules, and say what we have missed. | Country HR lead |
| Week 5 | Managers in the pilot entity | One page, ahead of their people: some balances will be corrected, approvals do not change, here is who answers questions — and please do not answer from your own copy of the sheet. | NL country HR lead |
| Week 6 | Pilot employees whose balance is wrong | Individually, by their HRBP, before any system shows a changed number. | HRBP, one to one |
| Week 8 | Pilot entity, all employees | What we did, what we found, what changes for you (for most: nothing). The corrections stated plainly. | NL country HR lead |
| Month 3 | German works council, ahead of DE scope | As NL, plus what the NL consultation concluded. | DE country HR lead plus counsel |
| Quarter 2 | Company-wide | Only once there is a result. What we found, what we fixed, and the offer: which process is next. | CHRO |
| Monthly from month 2 | HR leadership | Match rate per entity, unresolved count, days in dispute, evidence backlog. The same four numbers every month. | Me, then my successor |

**What is deliberately not said early:** anything about capacity or efficiency.
The administrators hold the knowledge that makes the policy files correct. If the
first framing they hear is a saving, they will not sabotage anything — they will
simply not volunteer the exceptions they have handled by hand for years, and
those exceptions are exactly what the engine does not know about.

### Three conversations, in the words I would actually use

The difficult parts of this plan are three specific conversations, and a plan
that describes them abstractly has not committed to anything.

**Week 0, to the administrator who maintains the Polish sheet.**

> I want you to hear this from me before it is announced. We are building
> something that recalculates leave balances from the rules, and the first thing
> it does is compare its answer with your sheet. I am not expecting your sheet to
> be right. It cannot be — nobody applies the ten-year education rule by hand
> across five hundred people and gets it right every time. If this finds errors,
> that is the system's fault, not yours.
>
> What it means for your week: the recurring part — the rollover, the balance
> questions, the September expiry chase — shrinks. What is left is the part that
> needs judgement: deciding whether a discrepancy is the engine being wrong or the
> sheet being wrong. That is not automatable and it is the part I need you for.
> Your role is not changing and there is no headcount number attached to this
> project. If that ever changes, you hear it from [named manager], not from a
> system.
>
> One thing I need from you now: the exceptions. Every case you handle by hand
> because the rule does not quite cover it. Those are invisible to me, and they
> are the difference between this working and this producing confident nonsense.

**Week 6, to an employee whose balance was overstated.**

> We checked how your leave balance was calculated and we got it wrong. The
> sheet showed 18 days; the correct figure under the Dutch rules is 14. The
> difference is four days that had already expired and should have come off in
> July.
>
> What happens now: you keep the 18 days for this leave year. We are not taking
> back days we told you that you had. The correction applies from the next leave
> year, and I will send you the calculation so you can see where the number comes
> from. If you have booked something on the strength of that balance, it stands.
>
> The reason this happened is that the rule is genuinely hard to apply by hand.
> That is our problem, not yours.

**Week 2, opening the works council consultation.**

> I want to be exact about what this is, because "AI" is in the description and
> it should not be where you spend your time.
>
> The calculation is deterministic: written rules — the ones in the Dutch Civil
> Code and in the local employment terms — applied in a fixed order, producing
> the same answer every time, with every step recorded. No model, no learning, no
> scoring, nothing that would produce a different answer for two employees in the
> same situation. AI was used to build it and to draft the annual rule updates
> that you would review. AI is not in the path between an employee's data and
> their leave balance, and I am willing to have that written into the agreement.
>
> What the system observes: absence records, hire date, contracted hours, work
> location. What it does not observe: hours of activity, timing of work,
> performance, or anything that would allow behaviour to be monitored. If that
> boundary moves, it is a new measure and we come back to you.
>
> What is on the table is how absence is recorded and verified. Entitlement does
> not change. And where the system finds an employee was under-granted, they are
> corrected retroactively and in full.

That third script leads with what the system does not do, rather than with "AI
is already used everywhere here". The second argument is true and useless:
co-determination rights attach per measure regardless of what the company does
elsewhere, and opening with precedent invites the answer that no precedent was
agreed with them.

**Tone, everywhere:** the reconciliation output is a list of errors in other
people's work, and every artefact must frame it as *system* error, because that
is what it is. If anything reads as an audit of individuals, the entities will
defend their numbers instead of fixing them and the data will get worse.

---

## 4. Rollout

Pilot, not big bang. Nothing becomes irreversible until an entity has seen the
engine agree with it for two cycles.

**The pilot is the Netherlands.** Not the largest population and not the biggest
saving — that is Poland. Three reasons:

1. **The smallest population that still produces a guaranteed finding.** Seventy
   people, and the two rules in the portfolio least likely to be applied
   correctly by hand: the two-clock expiry (statutory days lapsing six months
   after the accrual year, supplementary after five) and conditional forfeiture,
   where days lapse only if the employer can show it warned the employee. A pilot
   that finds nothing teaches nothing.
2. **The findings are legally meaningful.** An unenforceable forfeiture is not a
   rounding error; it is days the employee is still owed.
3. **It runs the works council conversation at small scale before Germany.** Not
   lower-stakes legally — the Dutch consultation is real — but lower-stakes in
   blast radius: getting it wrong there costs one entity, getting it wrong in
   Germany first stops the programme.

The honest cost of this choice is in section 5: the Dutch pilot proves the legal
argument and almost nothing about the administrative one.

**Phase 0 — read only (weeks 1–8, Netherlands).** The engine reads the entity's
existing export, recomputes, reports. The spreadsheet stays the system of record;
nothing an employee sees changes.
*Gate:* policy file signed off by counsel; every material difference explained or
corrected; two consecutive stable runs; consultation open.

**Phase 1 — parallel run in NL, phase 0 opens in Poland (weeks 9–20).** Both
systems run; the engine's number goes to HR, not to employees, and every
disagreement is resolved before month end. Poland starts read-only in week 9 so
its administrators learn the method while the NL findings are fresh — and Poland
is where the evidence backlog is, so its start date matters more than its
cut-over date.
*Gate:* match rate above the week-1 threshold for two consecutive cycles; no
unresolved record without a named owner and a date.

**Phase 2 — cut over per entity (from month 5, NL first).** One entity at a time.
The engine becomes the record; the spreadsheet is frozen and kept read-only for a
year. Order: Netherlands, Poland, India, Germany once consultation concludes, then
Ireland and the US.
*Gate per entity:* consultation complete where required; opening balances signed;
a rollback actually rehearsed once, not merely written down.

**Phase 3 — the rest (from month 12).** The ten `register_only` entities get an
annual attestation, not a migration; any can be onboarded later by adding a policy
file and a mapping. That attestation artefact does not exist yet — DECISION.md
section 6.

### What I personally do, weeks 1–4

The plan above is institutional. My own part is not, and it is the part I would
be judged on:

I sit with the Dutch country HR lead and we open the review page on her machine.
Not a demo — her entity, her people. We take one employee whose number the engine
disputes, expand the trace, and read it line by line until she can say out loud
what the rule does and where she thinks it is wrong. Then the same with her
policy file, which is those rules in the form her counsel will sign. Roughly a
day, and it solves the whole Ability problem for that person.

Then the same with the Polish and Indian administrators, in the other direction:
not me explaining the engine, but them showing me the cases it gets wrong. Each
one is either an exception to encode or a rule I have misread, and both are
findings.

No communications campaign in those four weeks. Five or six people, one at a
time, with the file open on the screen, until each can operate it without me.
Everything else in this plan depends on that working.

### What happens to the people doing this work

During phases 0 and 1 they run the parallel process, which is not a holding
pattern: they are the only people who can say whether a discrepancy is an engine
error or a sheet error, and that judgement is the input the engine cannot
produce.

The week-0 commitment — role unchanged, no headcount number attached — is the
organisation's to make, not mine. I build this and hand it over; a promise from
me expires when I move to the next process. So it is made by the person who will
still be their manager in a year, in week 0, in that same conversation. **Named
owner: the HR leader to whom the PL and IN administrators report.** If that
person will not make it, the plan is re-scoped rather than run with it implied.

### The evidence backlog, stated accurately

In the seeded population the engine refuses to produce a balance for six people
out of 58 — Polish entitlement depending on prior-employment and education
documents the company does not hold, or no signed opening balance at the ledger
cut-over. Each is a real person whose entitlement cannot currently be determined,
and closing the gap means going and getting a document.

That work is **partly one-off and partly permanent.** The backlog of existing
employees is finite and can be cleared. New joiners are not: every Polish hire,
indefinitely, brings the same evidence question, and that belongs in onboarding
from the pilot onwards rather than being discovered in year two.

---

## 5. Critical downsides

Not a balanced assessment. These are the ways this goes wrong.

**The pilot choice is itself a risk.** The Netherlands optimises for a guaranteed
legal finding and a small blast radius, and buys that by testing where the
administrative burden is smallest. Seventy people generate few balance queries;
the Dutch administrator is not drowning. So the pilot will show that the engine
finds real legal errors and almost nothing about whether it saves anyone
meaningful time — which is the question a sponsor asks at month 3. *Mitigation:*
say it in week 1, before the result exists, and state that the administrative
measurement comes from Poland in phase 1. A caveat that arrives after the
expectation has formed reads as an excuse.

**The correction problem.** Reconciliation will find overstated balances. Telling
someone they have four fewer days than they thought, after they have booked a
holiday, is the most damaging single moment in this project. *Position, agreed
before the pilot and not after the first case:* overstatements are the
organisation's risk, not the employee's — days honoured for the current leave
year, calculation corrected going forward. This costs money. The alternative is
that the first thing this system ever does to an employee is take something away,
after which nothing else it says is believed.

**Understatements are the half that gets quietly dropped.** The tempting position
is to wait for people to raise it. That is not a corrective, it is a filter: it
corrects the confident and the numerate and leaves everyone else short. So
under-granted employees are sought out actively and corrected retroactively and in
full, including where that means reconstructing entitlement from paper records
nobody wants to go looking for. If that is too expensive to commit to, the
reconciliation should not be run at all — acting on one direction of error only
is worse than not knowing.

**The administrators.** Their main recurring task shrinks, and they are also the
people whose knowledge makes the policy files correct. The failure mode is not
sabotage, it is silence: the exceptions never get volunteered, which is the most
likely cause of a technically successful and practically useless rollout.
*Mitigation:* the week-0 conversation, owned by their manager, and the exceptions
requested explicitly as a deliverable rather than hoped for.

**Local autonomy.** Country HR leads control their own process today, and this
reads as headquarters taking it away. The policy files are a real counter-argument
— the rules stay local and become more explicitly theirs — but only if they can
actually change them. *Mitigation:* the sign-off is real. If a country lead's
counsel disagrees with a rule, the file changes. If the first three such requests
are refused, the model is dead and everyone will know it.

**Three legal exposures, each with the same shape: they are cheap now and
expensive later.** *Co-determination* — changing how absence is recorded and
verified may trigger it in NL and DE, and getting it wrong turns a process
improvement into a formal dispute; NL opens week 2, DE month 3, both cut-overs
behind that gate regardless of technical readiness. *Terms* — a file that encodes
a rule less favourably than current local practice has unilaterally reduced
terms, and practice that has run for years can itself be binding; counsel
compares each file against *current practice*, not only statute, and every
difference is escalated rather than silently adopted. *Discovery* — today
non-compliance is undocumented, and after reconciliation it is a dated report
naming individuals and amounts; that is the right outcome and also a risk, so
legal is in the room from week 1 and the remediation path is agreed before the
first report exists. Separately, a cross-entity ledger including sickness is a
new processing activity: DPIA before the pilot, sickness detail stays local, only
day counts cross the boundary.

**"HR built a tool that says HR was wrong."** The first output is a list of
errors made by HR; presented as a systems achievement, the company hears an
admission. *Mitigation:* HR states the finding first, itself, with the fix
already running. The related trap is the efficiency overclaim — sell this as a
headcount saving, deliver half an FTE, and HR's next business case is not
believed.

**Nothing visible for two quarters.** Reconciliation-first produces a list of
problems and no employee-facing improvement. *Mitigation:* be explicit that phase
0's deliverable is a number, and report it from month 2.

**Stale policy files.** The realistic technical failure is not a wrong
calculation — the rules are tested and every figure carries its trace. It is a
jurisdiction changing a rule, nobody updating the file, and the engine
confidently producing wrong numbers at scale, which is worse than one spreadsheet
being wrong for one entity. Hence `review_due` blocking publication rather than
merely warning.

**The person who built it leaves it.** This is a method introduced by one person
who intends to move to the next process. If the handover is informal, the method
leaves with him and what remains is a repository nobody owns. Section 8 is the
mitigation, and it is a gate with conditions rather than an intention.

---

## 6. What it costs, what it returns

### What it costs — an estimate, and only that

None of these figures come from Groupon's data. They are the order of magnitude
I would present in week 1 so that nobody discovers the bill later, and the first
thing I would replace with real numbers.

| Line | Year one | Note |
|---|---|---|
| External counsel | **12–18 days** across six jurisdictions | The largest cash cost. 2–3 days per jurisdiction to check the file against statute *and* current practice, plus follow-up |
| Works council process (NL, DE) | 5–10 internal days plus counsel | Meetings, written materials, the agreement itself |
| DPIA | 3–5 days | Before the pilot |
| Country HR leads / HRBPs | 1–2 days each, ~10–20 days total | Reading and signing their own file. Spread over the year |
| Administrators, parallel run | ~0.5 day per entity per month while an entity is in phase 0 or 1 | Adjudicating discrepancies. This is the real overhead of running two processes |
| Evidence backlog | one-off effort per unresolved employee, plus a permanent step in onboarding | Section 4 |
| My own time | roughly half a role for two quarters, tapering | Then handover (section 8) |
| Build and tooling | near zero | It exists. Maintenance is a few days a year |

**Year one does not pay for itself, and it should not be presented as if it
does.** Against 0.25–0.5 FTE released annually (below), an outlay of roughly
15–20 counsel days and 30–50 internal person-days outside my own time is not
recovered inside twelve months. It is recovered from year two, and the case that
actually carries it is the template argument, not the saving.

### What the corrections cost, in both directions

This is the number people expect to point one way and does not.

On the seeded data the 16 material differences total 60 days in dispute, and the
**net is 18 days understated on the local sheets** — days owed to employees, not
days the company can recover. The no-clawback position on overstatements is the
visible concession; the larger half of the bill is retroactive correction of
under-granting, and that half is not a concession, it is a debt.

I expect a real run to point the same way, for a structural reason rather than a
lucky sample: hand-calculation errors lean one way. Defaulting a Polish employee
to the lower tier when the education evidence is missing under-grants. Writing
off Dutch days where the forfeiture is not enforceable under-grants. Nobody
hand-calculates generously by accident.

So the sentence for the sponsor in week 1 is: **this will find that we owe people
days, and correcting that is the point rather than a side effect.** Said before
the report exists, it is a principle. Said after, it is a negotiation.

### The manual effort released

Population in the six engine entities: ~1,550 (assumed — see DECISION.md).
*Variable work,* ~4.5 touches per employee per year (rollover, ~2 balance
queries, corrections, year-end expiry chase) ≈ 7,000 touches at 5–10 minutes:
**0.33–0.66 FTE**. *Fixed work,* policy review across six entities, ~ten holiday
calendars, audit evidence ≈ 96–192 hours: **0.05–0.11 FTE**. Total manual load
**0.4–0.8 FTE**; automation releases perhaps **0.25–0.5 FTE**.

**This is not a headcount case and must not be presented as one.** No role is
removed. The released capacity goes to work not currently being done at all —
clearing the evidence backlog, which directly increases what several named people
are owed.

The returns that do justify the project, in order of size:

1. **Error exposure.** The reconciliation flags material differences on roughly a
   quarter of comparable records and refuses to compute another seven at all.
   Even at a fraction of that rate, the exposure — understated balances that
   become claims, unenforceable forfeitures, wrong final settlements — is worth
   more than half an FTE.
2. **Reviewability.** The annual legal review changes from *re-derive the rules*
   to *approve a diff*, and that cost is the same whether there are six entities
   or sixteen.
3. **It is a template.** Any global process with local legal parameters, an
   annual renewal and an evidential burden has this shape. The second one costs a
   fraction of the first.

### The metric that actually matters

Every measure above is a measure of absence management, which is not what this is
for. So the headline metric is deliberately none of them:

> **Six months after the pilot: has someone in HR who was not involved in
> building this asked for the same treatment for a different process?**

The obvious objection is that I have defined success as being asked to do more
work. The answer is that it is the only indicator here that cannot be produced by
instruction. A match rate can be mandated; attendance at a demo can be mandated.
Nobody can be told to come and ask for this to be done to their own process. That
happens only if the people doing the work concluded, on their own work and on a
daily basis, that it made their week easier — which is what adoption actually
means, and the reason this project exists rather than a faster spreadsheet.

If the answer is no, a leave calculation was automated in six entities and that
is all that happened: modest, real, clearly insufficient — and the honest
response is to say so rather than re-describe it as a transformation.

Supporting indicators, monthly from month 2: match rate per entity, unresolved
findings without an owner, days in dispute, evidence backlog remaining.

### The second process, and why it is that one

The intended second instance is **knowledge distribution and mandatory training
compliance** — who must complete what, by when, under which jurisdiction's rules,
with what evidence retained.

Structurally the same problem: a global process, per-country legal parameters, an
annual renewal cycle, an evidential burden, and a current state held in
spreadsheets nobody can reconstruct after the fact. Everything here that is not
absence-specific — versioned policy files with an effective date, `unknown` as a
valid answer, reconciliation before migration, diff-not-apply annual updates —
transfers directly.

The second reason is practical: it is the domain I know. I spent **two and a half
years** implementing and running an LMS, so I can tell a real requirement from a
vendor's version of one and will not need six weeks to learn the process before I
can model it. That is a reason to pick it second, not a claim of expertise beyond
it.

### How to verify the effort estimate

The numbers above are a model, not a measurement: a two-week time diary with the
administrators in Poland and India, twelve months of leave-tagged service-desk
tickets, and a count of manual adjustments over one leave year would replace
them — measured before and after in Poland during phase 1, which is the only
number that settles it and is not obtainable from the Dutch pilot.

If the measured figure comes in materially below 0.4 FTE, the honest response is
to say so and re-argue the project on compliance exposure and on the template,
which it carries without the efficiency claim at all.

---

## 7. When I would stop

Kill criteria are only worth anything agreed before anyone is invested.

- **NL works council consultation unresolved after one quarter** → the
  Netherlands leaves scope and the pilot moves to Poland with the legal findings
  unproven. Unresolved in Germany → Germany leaves scope, the rest continues.
- **The pilot's match rate does not improve between cycle 1 and cycle 3** → the
  policy files are wrong, not the spreadsheets. Stop and re-derive the rules with
  counsel before touching anything else.
- **The no-clawback position is not agreed before the pilot runs** → do not run
  the pilot. Discovering overstatements without an agreed answer is worse than
  not looking.
- **The commitment to the administrators cannot be made by their own manager** →
  pause before the parallel run, not after.
- **Counsel time for policy sign-off is not funded by week 4** → stop at the end
  of phase 0. An engine running on unapproved rules is a liability with a
  dashboard.
- **The pilot's first cycle agrees almost perfectly** → do not celebrate. Either
  the Dutch process is genuinely correct, in which case move to Poland
  immediately and stop spending time here, or the mapping is not testing what it
  claims to. Check which before reporting anything.

---

## 8. Handover

I own the method through two instances: absence, and the second process in
section 6. After that it belongs to the organisation — and the point of writing
the conditions now is that "after that" otherwise means "indefinitely".

**What handover means concretely.** A named owner per policy file, already in
`registry.yaml` as `owner_role`; a named owner of the engine itself; a runbook
covering the monthly reconciliation, the annual update and the evidence process;
and the four monthly numbers going to HR leadership from someone who is not me.

**The gate opens when all four are true:**

1. A named person has run **one complete annual cycle** end to end themselves —
   year-end expiry, the `annual-update` diff, counsel sign-off on at least one
   changed file — with me available but not doing it.
2. Every engine entity has a signed policy file with a `review_due` date in the
   future and a named owner who can say what their file does.
3. The monthly report has been produced by that person, not by me, for two
   consecutive months.
4. There is a written escalation path for the case the runbook does not cover.

**What I keep afterwards, and for how long.** Answering questions, yes. Running
the monthly reconciliation, no — that is the thing that quietly becomes
permanent. After the gate opens I am available for questions for one further
quarter and I do not touch the process. If the gate has not opened within six
months of the second entity going live, that is a finding about the plan, not a
reason to extend my involvement, and it goes to the sponsor as such.

The failure mode here is not dramatic. It is that the person who built it stays
useful, so nobody learns it, so it never becomes the organisation's — and then
the second process never happens, which was the entire point.
