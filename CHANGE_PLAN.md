# Change & Culture Plan

## 1. What this change actually is

This is not an efficiency programme. If it were, it would not be worth doing:
the manual effort it removes is under one full-time role across a company of
1,734 people, and section 6 says so with the arithmetic attached.

What it is, is the first process in this company to be rebuilt so that the rules
are written down, the calculation is reproducible, and the reason for every
number can be shown to the person it applies to. Absence was chosen because it
is small enough to fail safely and legally consequential enough that getting it
right matters. Nobody's revenue depends on it. That is a feature.

The claim I am making to the organisation is therefore narrow and I intend to
keep it narrow:

> One task inside HR's week stops being manual. The job does not change. What
> changes is that we now know how to do this to a second process, and a third.

Two things follow from that framing, and both are constraints on everything
below.

**No promise is made that cannot be kept.** No headcount case, no "HR becomes
strategic", no transformation language. The administrators who maintain these
spreadsheets have been through systems projects before and can tell the
difference between a plan and a slide. The plan below is deliberately poorer in
promises than it could be.

**The success measure is not the absence numbers.** It is whether, six months
after the pilot, someone in HR who was not involved in building this comes and
asks for the same treatment for a different process. Section 6 makes that the
headline metric, because it is the only one that reflects what the project is
actually for.

### Who is affected, and how much

| Group | Size | What changes for them |
|---|---|---|
| HR administrators who maintain the spreadsheets | a handful, concentrated in PL and IN | The most. One recurring task shrinks to exception handling. Their role does not change; this is the group the plan is really about and the group most likely to be told a comfortable version of the truth. |
| Country HR leads and HRBPs | ~10–15 | Become the named owner of a policy file with a review date. This is new accountability, and it is real work: 1–2 days per entity in year one. |
| Works councils (NL, then DE) | 2 bodies | A consultation gate, not an audience. |
| Employees | 1,734 | Nothing, except a small number who will be told their balance was wrong. |
| Payroll | small | Nothing in v1. Gains a reliable source for encashment later. |
| Managers | all | Nothing in v1. Approvals stay where they are. |

The employee row carries the risk. A correction to a leave balance is not a
systems change to the person receiving it; it is a change to something they had
already planned their year around.

---

## 2. ADKAR across the audiences

I am using ADKAR here not as a framework to display but because it forces the
question *which specific element is missing for this specific group*, and the
answer differs sharply by group. Reading the grid honestly, the first two
columns are close to free in this organisation and the last two are where the
project actually fails.

| Audience | Awareness | Desire | Knowledge | Ability | Reinforcement |
|---|---|---|---|---|---|
| HR administrators (PL, IN) | Easy — they will hear about it | **The gap.** They own the exceptions the engine does not know about; nothing compels them to hand those over | Moderate — they must learn to read a trace and judge a discrepancy | Moderate | **The gap.** If nobody asks for the reconciliation output after month 3, they go back to the sheet |
| Country HR leads / HRBPs | Easy | Mixed — reads as headquarters taking their process | Low — most have never signed off a rule as *written text* before | **The gap.** Signing a policy file requires counsel time they do not currently have budgeted | Moderate — the review date in the file is the mechanism |
| Works councils (NL, DE) | Formal, by law | Neutral at best; their job is to test it | **The gap.** They need to understand what the system does and does not observe | n/a | The agreement itself |
| Employees | Low need | n/a | Low — most need nothing | n/a | n/a |
| HR leadership / sponsor | Easy | Present | Moderate | Moderate | **The gap.** A slow project with no employee-facing output for two quarters loses attention before it produces its result |

**Awareness and Desire are not this project's problem, and I want to be precise
about why.** Groupon's leadership has taken a public, repeated position that AI
fluency is expected of everyone here, not delegated to a function. That means I
do not have to spend the first month arguing that using AI is legitimate — a
large share of what a change plan usually spends its energy on is already done.
What it does *not* mean is that anything is settled about AI and employee data;
it is a stance on direction, not a permission slip, and section 3 treats the
works councils accordingly.

The result is that the standard playbook — town halls, a vision deck, a comms
campaign to build awareness and desire — would be aimed at the two elements that
are already fine. So the plan below spends almost nothing on them and almost
everything on Ability and Reinforcement:

- **Ability** is budget and time, not enthusiasm. A country HR lead cannot sign a
  policy file without counsel, and counsel is not free. If that is not funded in
  week 1, the files go unsigned and the engine runs on rules nobody has approved,
  which is worse than the spreadsheet it replaced. Sitting with each lead while
  they read their own file, line by line, until they can say what it does — that
  is the actual work, and it is roughly a day each. I would do it in person.
- **Reinforcement** is what decides whether this survives me. A reconciliation
  nobody reads is a report generator. The mechanisms are: the match rate goes in
  the same monthly HR pack as everything else, from month 2, permanently; the
  `review_due` date in each policy file is a blocker in `annual-update` and
  blocks publication when overdue; and the handover gate in section 8 does not
  open until a named person has run one full annual cycle themselves.

---

## 3. Communication

The sequencing principle: **nobody hears about their own balance from a system.
Every person whose number changes hears it from a human who can answer "why",
and that human hears it before the population does.**

| When | Audience | Message | From |
|---|---|---|---|
| Week 0 | The administrators who own the spreadsheets today (PL, IN) — before the pilot entity, because they will hear about it anyway | One-to-one. What is being built, what it does to their week, what it does not do, and that they are being asked to help build it. | Their own manager, with me present to answer detail |
| Week 1 | Country HR leads and HRBPs | The approach, the boundary, and the ask: you own a policy file and you sign it with counsel. Includes the time and budget this costs. | HR leadership |
| Week 2 | NL works council (OR) | Formal notification, before the pilot. No change to entitlement is proposed; the change is to how balances are calculated and verified. | NL country HR lead plus counsel |
| Week 3 | External counsel, NL first | The policy file with a specific request: confirm or correct these rules, and tell us what we have missed. | Country HR lead |
| Week 6 | Pilot employees whose balance is wrong | Individually, by their HRBP, before any system shows a changed number. | HRBP, one to one |
| Week 8 | Pilot entity, all employees | What we did, what we found, what changes for you (for most: nothing). The corrections included, stated plainly. | NL country HR lead |
| Month 3 | Germany works council, ahead of DE scope | Same content as NL, plus what the NL consultation concluded. | DE country HR lead plus counsel |
| Quarter 2 | Company-wide | Only once there is a result. What we found, what we fixed, and the offer: which process is next. | CHRO |
| Monthly, from month 2 | HR leadership | Match rate per entity, unresolved count, days in dispute, evidence backlog. Same four numbers every month. | Me, then my successor |

**What is deliberately not said early:** anything about capacity or efficiency.
The administrators hold the knowledge that makes the policy files correct. If
the first framing they hear is a saving, they will not sabotage anything — they
will simply not volunteer the exceptions they have been handling by hand for
years, and those exceptions are exactly what the engine does not know about.
That is the most likely cause of a technically successful and practically
useless rollout.

**Tone, across everything:** the reconciliation output is a list of errors in
other people's work. It must be framed as *system* error, because that is what
it is — nobody applies the Dutch notice rule by hand across 70 people and gets
it right. If any artefact reads as an audit of individuals, the entities will
start defending their numbers instead of fixing them, and the data gets worse.

### Three conversations, in the words I would actually use

Because the difficult parts of this plan are three specific conversations, and a
plan that describes them abstractly has not really made a commitment.

**Week 0, to the administrator who maintains the Polish sheet.**

> I want you to hear this from me before it is announced. We are building
> something that recalculates leave balances from the rules, and the first thing
> it does is compare its answer with your sheet. I am not expecting your sheet to
> be right. It cannot be — nobody can apply the ten-year education rule by hand
> across five hundred people and get it right every time, and if this finds
> errors, that is the system's fault, not yours.
>
> What it means for your week: the recurring part — the rollover, the balance
> questions, the September expiry chase — shrinks. What is left is the part that
> needs judgement: deciding whether a discrepancy is the engine being wrong or
> the sheet being wrong. That part is not automatable and it is the part I need
> you for. Your role is not changing and there is no headcount number attached to
> this project. If that ever changes, you hear it from [named manager], not from
> a system.
>
> I need one thing from you now: the exceptions. Every case you handle by hand
> because the rule does not quite cover it. Those are invisible to me and they
> are the difference between this working and this producing confident nonsense.

**Week 6, to an employee whose balance was overstated.**

> We checked how your leave balance was calculated and we got it wrong. The
> sheet showed 18 days; the correct figure under the Dutch rules is 14. The
> difference is four days that had already expired and should have come off in
> July.
>
> To be clear about what happens: you keep the 18 days for this leave year. We
> are not taking days back that we told you that you had. The correction applies
> from the next leave year, and I will send you the calculation so you can see
> where the number comes from. If you have booked something on the strength of
> that balance, it stands.
>
> The reason this happened is that the rule is genuinely hard to apply by hand,
> and that is our problem, not yours.

**Week 2, opening the works council consultation.**

> I want to be exact about what this is, because "AI" is in the description and
> it should not be the thing you spend your time on.
>
> The calculation is deterministic. It is a set of written rules — the ones in
> the Dutch Civil Code and in the local employment terms — applied in a fixed
> order, producing the same answer every time, with every step recorded. There is
> no model, no learning, no scoring, and nothing that would produce a different
> answer for two employees in the same situation. AI was used to build it and to
> draft the annual rule updates that you would review. AI is not in the path
> between an employee's data and their leave balance, and I am willing to have
> that written into the agreement.
>
> What the system observes is: absence records, hire date, contracted hours,
> work location. What it does not observe: hours of activity, timing of work,
> performance, or anything that would allow behaviour or performance to be
> monitored. If that boundary ever moves, it is a new measure and we come back to
> you.
>
> What is on the table for co-determination is how absence is recorded and
> verified. Entitlement itself does not change. And where the system finds that
> an employee was under-granted, they are corrected retroactively and in full.

That third script leads with what the system does not do, not with "AI is
already used everywhere here". The second argument is true and useless: works
council rights attach per measure regardless of what the company does
elsewhere, and opening with precedent invites the response that no precedent was
agreed with them.

---

## 4. Rollout

Pilot, not big bang. Nothing becomes irreversible until an entity has seen the
engine agree with it for two cycles.

**The pilot is the Netherlands.** Not the largest population and not the biggest
saving — that is Poland. The Netherlands is chosen for three reasons:

1. **Smallest population that still produces a guaranteed finding.** 70 people.
   The Dutch two-clock expiry (statutory days lapsing six months after the accrual
   year, supplementary days after five) and the conditional forfeiture rule — days
   only lapse if the employer can show it warned the employee — are the two rules
   in the whole portfolio least likely to be applied correctly by hand. The pilot
   will find something. A pilot that finds nothing teaches nothing.
2. **The findings are legally meaningful.** An unenforceable forfeiture is not a
   rounding error; it is days the employee is still owed. That makes the pilot's
   output worth acting on rather than worth filing.
3. **It rehearses the works council conversation at small scale before Germany.**
   The NL consultation is a real consultation with real consequences, and getting
   it wrong there costs one entity. Getting it wrong in Germany first stops the
   programme.

The honest cost of this choice is in section 5: the Dutch pilot proves the legal
argument and proves almost nothing about the administrative one, because the
administrative load sits in Poland and India.

**Phase 0 — read only (weeks 1–8, Netherlands).**
The engine reads the entity's existing export, recomputes, reports. The
spreadsheet stays the system of record. Nothing an employee sees changes.
*Gate:* the NL policy file is signed off by counsel; every material difference
is explained or corrected; two consecutive monthly runs stable; works council
notified and consultation open.

**Phase 1 — parallel run in NL, phase 0 opens in Poland (weeks 9–20).**
Both systems run in the Netherlands; the engine's number goes to HR, not to
employees. Every disagreement is resolved before month end. Poland enters
read-only in week 9 so its administrators are learning the method while the NL
findings are still fresh — and Poland is where the evidence backlog is, so its
start date matters more than its cut-over date.
*Gate:* match rate above the threshold agreed in week 1 for two consecutive
cycles; zero unresolved records without a named owner and a date.

**Phase 2 — cut over per entity (from month 5, NL first).**
One entity at a time. The engine becomes the record; the spreadsheet is frozen
and kept read-only for a year. Order: Netherlands, Poland, India, then Germany
once consultation has concluded, then Ireland and the US.
*Gate per entity:* consultation complete where required; opening balances
signed; a rollback that has actually been rehearsed once, not merely written
down.

**Phase 3 — the rest (from month 12).**
The nine `register_only` entities get an annual attestation, not a migration.
Any of them can be onboarded later by adding a policy file and a mapping, which
is the point of keeping rules as data. The attestation artefact does not exist
yet and is named as a gap in DECISION.md section 6.

### What happens to the people doing this work

During phases 0 and 1 they run the parallel process, and that is not a holding
pattern: they are the only people who can say whether a discrepancy is an engine
error or a sheet error. That judgement is the input the engine cannot produce.

The week-0 commitment — role unchanged, no headcount number attached — is a
commitment the organisation makes, not one I can make. I am building this and
handing it over; a promise from me expires when I move to the next process. So
it has to be made by the person who will still be their manager in a year, and
it has to be made in week 0, in the same conversation, or the parallel run will
be staffed by people who have worked out that nobody has said the thing that
matters. **Named owner of that commitment: the HR leader to whom the PL and IN
administrators report.** If that person will not make it, the plan should be
re-scoped rather than run with it implied.

### The evidence backlog, stated accurately

In the seeded population the engine refuses to produce a balance for six people
out of 58 — because Polish entitlement depends on prior-employment and education
documents the company does not hold, or because there is no signed opening
balance at the ledger cut-over. Every one of those is a real person whose
entitlement cannot currently be determined, and closing the gap means going and
getting a document. That is real work, and it is honest to say
what kind of work it is: **partly one-off and partly permanent.** The backlog of
existing employees is finite and can be cleared. New joiners are not — every
Polish hire, indefinitely, brings the same evidence question, and that belongs in
onboarding from the pilot onwards rather than being discovered as a surprise in
year two.

---

## 5. Critical downsides

Not a balanced assessment. These are the ways this goes wrong.

### The pilot choice is itself a risk

Choosing the Netherlands optimises for a guaranteed legal finding and a small
blast radius. It buys that by testing the case in the entity where the
administrative burden is smallest. Seventy people generate few balance queries;
the Dutch administrator is not drowning. So the pilot will demonstrate that the
engine finds real legal errors and will demonstrate almost nothing about whether
it saves anyone meaningful time — and the efficiency question is the one a
sponsor asks at month 3. The mitigation is to name this in week 1, before the
result exists, and to state that the administrative measurement comes from
Poland in phase 1 and not from the pilot. A finding that arrives after the
expectation has formed reads as an excuse.

### It goes wrong for people

**The correction problem.** Reconciliation will find employees whose balance was
overstated. Telling someone they have four fewer days than they thought, after
they have booked a holiday, is the single most damaging moment in this project.
*Position, agreed before the pilot runs and not after the first case:*
overstatements are the organisation's risk, not the employee's. The days are
honoured for the current leave year and the calculation is corrected going
forward. This costs money. The alternative is that the first thing this system
ever does to an employee is take something away, and then no subsequent
communication about it will be believed.

**Understatements are the other half, and they are the half that gets quietly
dropped.** The tempting position is to wait for people to raise it. That is not
a corrective, it is a filter: it corrects the confident and the numerate, and
leaves everyone else short. So under-granted employees are sought out actively
and corrected retroactively and in full, including where that means
reconstructing entitlement from paper records the company would rather not go
looking for. If that is too expensive to commit to, then the reconciliation
should not be run, because running it and acting on only one direction of error
is worse than not knowing.

**The administrators.** Their main recurring task shrinks. They are also the
people whose knowledge makes the policy files correct. The failure mode is not
sabotage, it is silence — the exceptions never get volunteered. *Mitigation:* the
week-0 conversation above, owned by their manager, plus the exceptions being
asked for explicitly as a deliverable rather than hoped for.

**Local autonomy.** Country HR leads control their own process today and this
reads as headquarters taking it away. The policy files are a genuine
counter-argument — the rules stay local and become more explicitly theirs — but
only if they can actually change them. *Mitigation:* the sign-off is real. If a
country lead's counsel disagrees with a rule, the file changes. If the first
three such requests are refused, the model is dead and everyone will know it.

### It goes wrong legally

**Consultation.** In the Netherlands and Germany, changing how absence is
recorded and verified may trigger co-determination. Getting it wrong turns a
process improvement into a formal dispute and stops the programme.
*Mitigation:* NL consultation opens in week 2, before the pilot; DE opens in
month 3, before DE is in scope; both cut-overs sit behind that gate regardless
of technical readiness.

**Written-down entitlements.** If a policy file encodes a rule less favourably
than current local practice, the system has unilaterally reduced terms —
and practice that has run for years can itself become binding.
*Mitigation:* counsel compares each file against *current practice*, not only
against statute. Every difference is escalated, never silently adopted.

**Making a diffuse problem documented.** Today non-compliance is undocumented.
After reconciliation it is a dated report naming individuals and amounts. That
is the right outcome and it is also a discovery risk.
*Mitigation:* legal is in the room from week 1 and the remediation path is agreed
before the first report exists. Findings are acted on, not filed.

**Data protection.** A cross-entity absence ledger including sickness is a new
processing activity touching health-adjacent data.
*Mitigation:* DPIA before the pilot; sickness detail stays in the local entity
and only day counts cross the boundary.

### It goes wrong for HR's credibility

**"HR built a tool that says HR was wrong."** The first output is a list of
errors made by HR. Presented as a systems achievement, the company hears an
admission. *Mitigation:* HR states the finding first, itself, with the fix
already running. That is the only version that builds credibility instead of
spending it.

**The efficiency overclaim.** If this is sold as a headcount saving and delivers
half an FTE, HR's next business case is not believed. Section 6 states the number
and states that it is small.

**Nothing visible for two quarters.** Reconciliation-first means the early phases
produce a list of problems and no employee-facing improvement. In an organisation
that prizes speed, that is hard to keep funded. *Mitigation:* be explicit at the
start that phase 0's deliverable is a number, and report it from month 2. A
moving metric is what keeps a slow project alive.

### It goes wrong technically

The realistic failure is not a wrong calculation — the rules are tested and every
figure carries its trace. It is **stale policy files**: a jurisdiction changes a
rule, nobody updates the file, and the engine confidently produces wrong numbers
at scale, which is worse than one spreadsheet being wrong for one entity.
`review_due` and `annual-update` exist for this and are load-bearing. An overdue
review blocks publication of the balance, not just a warning in a report.

### It goes wrong because the person who built it leaves it

This is a method being introduced by one person who intends to move to the next
process. If the handover is informal, the method leaves with him and what remains
is a Python repository nobody owns. Section 8 is the mitigation, and it is a gate
with conditions, not an intention.

---

## 6. The benefit argument, made honestly

### The manual effort, measured as best I can without the data

Population in the six engine entities: ~1,550 (assumed — see DECISION.md).

*Variable work,* per employee per year: leave-year rollover and carry-forward
check (1 touch), balance queries from employees and managers (~2), corrections
and adjustments (~0.5), year-end expiry chase and reconciliation (1) ≈ **4.5
touches**, so roughly 7,000 touches a year. At 5–10 minutes each: **580–1,160
hours**, or **0.33–0.66 FTE** against 1,760 productive hours.

*Fixed work,* per year: policy review and rebuild across six entities (36–72 h),
holiday calendars for around ten calendars (20–40 h), audit and compliance
evidence (40–80 h) ≈ **96–192 hours**, or **0.05–0.11 FTE**.

Total manual load: **roughly 0.4–0.8 FTE.** Automation removes perhaps 60–75% of
the variable work and half of the fixed work, releasing **0.25–0.5 FTE.**

### What that means, and what it does not

**This is not a headcount case and it must not be presented as one.** Half an FTE
across 1,734 people does not justify a project, and no role is being removed. The
released capacity goes to work that is currently not being done at all: clearing
the evidence backlog, which directly increases what several named people are
actually owed.

Saying this plainly is not modesty. It is the difference between an HR business
case that is believed next time and one that is not — and there will be a next
time, which is the whole point.

The returns that do justify it, in order of size:

1. **Error exposure.** On the seeded dataset the reconciliation flags material
   differences on roughly a quarter of comparable records and refuses to compute
   another seven at all. Even at a fraction of that rate, the exposure —
   understated balances that become claims, unenforceable forfeitures, wrong
   final settlements — is worth more than half an FTE.
2. **Reviewability.** The annual legal review changes from *re-derive the rules*
   to *approve a diff*. That cost is the same whether there are six entities or
   sixteen, which is what makes it compound.
3. **It is a template.** Policy-as-data plus reconciliation is not specific to
   absence. Any global process with local legal parameters, an annual renewal and
   an evidential burden has the same shape. The second one costs a fraction of
   the first.

### The metric that actually matters

Every measure above is a measure of absence management, and absence management
is not what this is for. So the headline metric is deliberately not one of them:

> **Six months after the pilot: has someone in HR who was not involved in
> building this asked for the same treatment for a different process?**

If yes, the project returned what it was for, whatever the match rate says. If
no, then a leave calculation was automated in six entities and that is all that
happened — which is a modest, real, and clearly insufficient result, and the
honest response is to say so rather than to re-describe it as a transformation.

Supporting indicators, reported monthly from month 2 and unchanged thereafter:
match rate per entity, unresolved findings without an owner, days in dispute,
evidence backlog remaining. Four numbers, same four every month.

### The second process, and why it is that one

The intended second instance is **knowledge distribution and mandatory training
compliance** — who must complete what, by when, under which jurisdiction's rules,
with what evidence retained.

It is structurally the same problem: a global process, per-country legal
parameters, an annual renewal cycle, an evidential burden, and a current state
held in spreadsheets that nobody can reconstruct after the fact. Everything in
this repository that is not absence-specific — versioned policy files with an
effective date, `unknown` as a valid answer, reconciliation against the existing
record before any migration, the diff-not-apply annual update — transfers
directly.

The second reason is less architectural and more practical: it is the domain I
know. I spent **two and a half years** implementing and running an LMS, which
means I can tell the difference between a real requirement and a vendor's version
of one, and I will not need six weeks to learn what the process is before I can
model it. That is a reason to pick it second, not a reason to claim expertise
beyond it.

### How to verify the effort estimate

The numbers above are a model, not a measurement, and should not be taken on
trust.

- A two-week time diary with the administrators in Poland and India, in
  15-minute blocks.
- Twelve months of HR service-desk tickets tagged leave or absence: volume,
  handling time, share that are "what is my balance".
- A count of manual adjustments in the current sheets over one leave year.
- Measured before and after in Poland during phase 1 — the only number that
  settles it, and not obtainable from the Dutch pilot.

If the measured figure comes in materially below 0.4 FTE, the honest response is
to say so and re-argue the project on compliance exposure and on the template,
which it can carry without the efficiency claim at all.

---

## 7. When I would stop

Stated in advance, because kill criteria are only worth anything if they are
agreed before anyone is invested.

- **Works council consultation in NL is unresolved after one quarter** → the
  Netherlands leaves scope and the pilot moves to Poland with the legal findings
  unproven. If it is unresolved in Germany, Germany leaves scope and the rest
  continues.
- **The pilot's match rate does not improve between cycle 1 and cycle 3** → the
  policy files are wrong, not the spreadsheets. Stop and re-derive the rules with
  counsel before touching anything else.
- **The no-clawback position is not agreed before the pilot runs** → do not run
  the pilot. Discovering overstatements without an agreed answer is worse than
  not looking.
- **The commitment to the administrators cannot be made by their own manager** →
  pause before the parallel run, not after. A parallel run staffed by people who
  suspect otherwise will not surface the discrepancies it exists to surface.
- **Counsel time for policy sign-off is not funded by week 4** → stop at the end
  of phase 0. An engine running on unapproved rules is a liability with a
  dashboard.

---

## 8. Handover

I own the method through two instances: absence, and the second process in
section 6. After that it belongs to the organisation, and the point of writing
the conditions down now is that "after that" otherwise means "indefinitely".

**What handover means concretely.** A named owner per policy file, already in
`registry.yaml` as `owner_role`; a named owner of the engine itself; a runbook
covering the monthly reconciliation, the annual update and the evidence process;
and the four monthly numbers going to HR leadership from someone who is not me.

**The gate opens when all four are true:**

1. A named person has run **one complete annual cycle** end to end themselves —
   the year-end expiry, the `annual-update` diff, counsel sign-off on at least
   one changed file — with me available but not doing it.
2. Every engine entity has a signed policy file with a `review_due` date in the
   future and a named owner who can say what their file does.
3. The monthly report has been produced by that person, not by me, for two
   consecutive months.
4. There is a written escalation path for the case the runbook does not cover.

**What I keep afterwards, and for how long.** Answering questions, yes.
Running the monthly reconciliation, no — that is the thing that quietly becomes
permanent. The boundary is: after the gate opens, I am available for questions
for one further quarter and I do not touch the process. If the gate has not
opened within six months of the second entity going live, that is a finding about
the plan, not a reason to extend my involvement, and it goes to the sponsor as
such.

The reason for stating this so precisely is that the failure mode is not
dramatic. It is that the person who built it stays useful, so nobody learns it,
so it never becomes the organisation's — and then the second process never
happens, which was the entire point.
