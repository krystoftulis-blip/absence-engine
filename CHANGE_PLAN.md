# Change & Culture Plan

This plan covers a change that is smaller than it sounds for most people and
much larger than it sounds for a few. Getting that asymmetry right is most of
the work.

---

## 1. Who is actually affected, and how much

| Group | Size | What changes for them |
|---|---|---|
| HR administrators who maintain the spreadsheets | a handful, concentrated in PL and IN | The most - their core task disappears and is replaced by exception handling. This is the group the plan is really about. |
| Country HR leads and HRBPs | ~10–15 | Become named owners of a policy file with a review date. New accountability, formalised. |
| Payroll | small | Gains a reliable source for encashment and final settlements - later, not in v1. |
| Works councils (DE, NL) | 2 bodies | A consultation gate, not an audience. |
| Managers | all | Nothing in v1. Approvals stay where they are. |
| Employees | 1,734 | Nothing in v1, except a small number who will be told their balance was wrong. |

The last row is the one that carries the risk. A correction to someone's leave
balance is not an IT change to them; it is a change to something they had
already planned their year around.

---

## 2. Communication

The sequencing principle: **nobody hears about their own balance from a system.
Every person whose number changes hears it from a human who can answer "why",
and that human hears it before the population does.**

| When | Audience | Message | From |
|---|---|---|---|
| Week 0 | The 2–4 administrators who own the spreadsheets today | One-to-one, before anything else. What is being built, why, what happens to their role, and that they are being asked to help build it. The honest version, including that their current task will not exist in a year. | Their direct manager, with the project sponsor available |
| Week 1 | Country HR leads and HRBPs | The approach, the boundary, and the ask: each of you owns a policy file and signs it off with counsel. This is real work, roughly 1–2 days per entity. | HR leadership |
| Week 2 | Works councils (DE), OR (NL) | Formal notification. Framed correctly: no change to entitlement is proposed; the change is to how balances are recorded and verified. Consultation opens before the pilot, not after. | Country HR lead plus counsel |
| Week 3 | External counsel per jurisdiction | The policy file, with a specific request: confirm or correct these rules, and tell us what we have missed. | Country HR lead |
| Week 6 (after pilot findings exist) | Pilot entity's employees whose balance is wrong | Individually, by their HRBP, before any system shows a changed number. "We checked, we found an error, here is what it is and what we are doing." | HRBP, one to one |
| Week 8 | Pilot entity, all employees | What happened, what it found, what changes for you (mostly nothing). Includes the corrections found - transparently. | Country HR lead |
| Quarter 2 | Company-wide | Only once there is a result worth reporting. What we found, what we fixed, what is next. | CHRO |
| Ongoing | Leadership | Reconciliation match rate per entity, unresolved count, days in dispute. Same numbers every month. | Project lead |

**What is deliberately not communicated early:** any efficiency or headcount
framing. If the first thing the administrators hear about this project is a
sentence about capacity, the project is over - they own the knowledge that makes
the policy files correct, and they will not give it to something they read as a
threat. The efficiency case is a conversation with leadership and with the
affected individuals about their own future, not a company announcement.

**Tone:** the reconciliation output is a list of errors in other people's work.
Every artefact must frame those as *system* errors, because that is what they
are - nobody can apply the Dutch notice rule by hand across 70 people and get it
right. If any communication reads as an audit of individuals, the entities will
start defending their numbers instead of fixing them, and the data will get
worse rather than better.

---

## 3. Rollout

Pilot, not big bang. The brief flags migration risk and the migration risk is
real, so the sequence is designed so that nothing is irreversible until an
entity has seen the engine agree with it for two cycles.

**Phase 0 — Read only (weeks 1–8, Poland).**
Poland first: largest population, hardest rules, and the shared services hub, so
the administrators are in one place. The engine reads the entity's existing
export, recomputes, and reports. The spreadsheet remains the system of record.
Nothing an employee sees changes.
*Gate to proceed:* the policy file is signed off by counsel; every material
difference is explained or corrected; two consecutive monthly runs are stable.

**Phase 1 — Parallel run (weeks 9–20, Poland then India).**
Both systems run. The engine's number is published to HR but not to employees.
Every disagreement is resolved before month end. Opening balances are signed off
one by one - this is the slow part and it is unavoidable.
*Gate:* match rate above an agreed threshold for two consecutive cycles, zero
unresolved records without a named owner and a date.

**Phase 2 — Cut over per entity (from month 6).**
One entity at a time. The engine becomes the record; the spreadsheet is frozen,
kept read-only for a year. The order follows risk, not size: Poland, then India,
then the Netherlands and Germany once works council consultation has concluded,
then Ireland and the US.
*Gate per entity:* consultation complete where required; opening balances
signed; an agreed rollback (re-freeze the engine, unfreeze the sheet) that has
actually been rehearsed once.

**Phase 3 — The rest (from month 12).**
The nine `register_only` entities get an annual attestation, not a migration,
until there is a reason to change that. Any of them can be onboarded later by
adding a policy file and a few lines of mapping - which is the whole point of
keeping the rules as data.

**What happens to the people doing this work during the transition.** They run
the parallel process. That is not a holding pattern - during Phases 0 and 1 they
are the only people who can say whether a discrepancy is an engine error or a
spreadsheet error, and that judgement is the input the engine cannot produce.
The commitment made to them in week 0 has to be specific: *your role changes, we
will tell you what it becomes before the parallel run ends, and you are not
being managed out through a systems project.* If that commitment cannot honestly
be made, it must not be implied - and the plan should be re-scoped, because a
parallel run staffed by people who have worked out they are automating
themselves out of a job will not surface the discrepancies it needs to.

---

## 4. Critical downsides

Not a balanced SWOT. These are the ways this goes wrong.

### It goes wrong for people

**The correction problem.** Reconciliation will find employees whose balance was
overstated. Telling someone they have four fewer days than they thought - after
they have booked a holiday - is the single most damaging moment in this project.
*Mitigation:* a stated no-clawback position agreed **before** the pilot runs, not
after the first case. Overstatements found in the pilot are honoured for the
current leave year and corrected going forward. This costs money and it is worth
it; the alternative is that the first thing the new system ever does to an
employee is take something away. Understatements are corrected retroactively and
in full, immediately.

**The administrators.** Two to four people whose main task disappears. They are
also the people whose knowledge makes the policy files correct. If they conclude
the project is aimed at them, they will not sabotage it - they will simply not
volunteer the exceptions they have been handling manually for years, and those
exceptions are exactly what the engine does not know about. This is the most
likely cause of a technically successful, practically useless rollout.
*Mitigation:* named, funded destination roles agreed before week 0.

**Local autonomy.** Country HR leads currently control their own process. This
reads as headquarters taking it away. The policy files are genuinely a
counter-argument - the rules stay local and become *more* explicitly theirs - but
that argument only lands if they actually sign the files and can change them.
*Mitigation:* the sign-off is real. If a country lead's counsel disagrees with a
rule, the file changes. If the first three requests are refused, the model is
dead.

### It goes wrong legally

**Consultation.** In Germany and the Netherlands, changing how working time and
absence are recorded may trigger co-determination. Getting this wrong turns a
process improvement into a formal dispute and stops the whole programme.
*Mitigation:* consultation opens in week 2, before the pilot, and the DE and NL
cut-overs sit behind that gate regardless of technical readiness.

**Written-down entitlements.** If a policy file encodes a rule less favourably
than current local practice, the system has unilaterally reduced terms. Practice
that has run for years can itself become binding.
*Mitigation:* counsel compares each file against *current practice*, not only
against statute. Every difference is escalated, never silently adopted.

**Making a known problem documented.** Today, non-compliance is diffuse and
undocumented. After reconciliation it is a dated report naming individuals and
amounts. That is the right outcome and it is also a discovery risk. Nobody
should be surprised by it later.
*Mitigation:* legal is in the room from week 1 and agrees the remediation path
before the first report exists. Findings are acted on, not filed.

**Data protection.** A cross-entity ledger of absence, including sickness, is a
new processing activity involving health-adjacent data.
*Mitigation:* DPIA before the pilot; sickness detail stays in the local entity
and only day counts cross the boundary.

### It goes wrong for HR's credibility

**"HR built a tool that says HR was wrong."** The reconciliation's first output
is a list of errors made by HR. If it is presented as a systems achievement, the
rest of the company hears an admission.
*Mitigation:* HR states the finding first, itself, with the fix already running.
Owning it is the only version of this that builds credibility rather than
spending it.

**The efficiency claim.** If this is sold as a headcount saving and delivers
half an FTE, HR's next business case is not believed. See section 5 - the number
is genuinely small, and saying so up front is worth more than the overclaim.

**Nothing visible for six months.** Reconciliation-first means the first phases
produce a list of problems and no employee-facing improvement. In an
organisation running on stated principles of speed and simplification, that is a
hard thing to keep funded.
*Mitigation:* be explicit at the start that Phase 0 delivers a number - match
rate and days in dispute - and report it monthly from week 4. A moving metric is
what keeps a slow project alive.

### It goes wrong technically

The realistic failure is not a wrong calculation - the rules are tested and
traced. It is **stale policy files**: a jurisdiction changes a rule, nobody
updates the file, and the engine confidently produces wrong numbers at scale,
which is worse than a spreadsheet being wrong for one entity. `review_due` and
`annual-update` exist for exactly this and are load-bearing, not decoration. An
overdue review is a blocker in the report, and the rule should be that it also
blocks the balance from being published.

---

## 5. The headcount and quality argument, made honestly

### The estimate

Population in the six engine entities: ~1,550 (assumed - see DECISION.md).

*Variable work,* per employee per year: leave-year rollover and carry-forward
check (1 touch), balance queries from employees and managers (~2), corrections
and adjustments (~0.5), year-end expiry chase and reconciliation (1) ≈ **4.5
touches**, so roughly 7,000 touches a year. At 5–10 minutes each that is
**580–1,160 hours**, or **0.33–0.66 FTE** against 1,760 productive hours.

*Fixed work,* per year: policy review and rebuild across six entities (36–72 h),
holiday calendars for around ten calendars (20–40 h), audit and compliance
evidence (40–80 h) ≈ **96–192 hours**, or **0.05–0.11 FTE**.

Total manual load: **roughly 0.4–0.8 FTE.** Automation removes perhaps 60–75% of
the variable work and half of the fixed work, releasing **0.25–0.5 FTE.**

### What that honestly means

**This is not a headcount reduction.** Half an FTE across a company of 1,734
people does not justify the project on its own, and anyone presenting absence
management as a headcount case is overselling it. Saying so is not modesty; it
is the difference between an HR business case that gets believed next time and
one that does not.

The returns that do justify it:

1. **Error rate.** On the seeded dataset the reconciliation flags material
   differences on roughly a quarter of comparable records, and refuses to
   compute another 7 at all. Even if the real rate is a fraction of that, the
   exposure - understated balances that become claims, unlawful forfeitures,
   wrong final settlements - is worth more than half an FTE.
2. **Reviewability.** The annual legal review changes from *re-derive the rules*
   to *approve a diff*. That is the change that compounds: it costs the same
   whether there are six entities or sixteen.
3. **It is a template.** Policy-as-data plus reconciliation is not specific to
   absence. Working time, probation, benefits eligibility and notice periods all
   have the same shape: a global process with per-entity legal parameters. The
   second process costs a fraction of the first. **That** is the commercial case,
   and it should be made as one - not disguised as a saving on absence.

### How to verify the estimate

Do not take the numbers above on trust; they are a model, not a measurement.

- A two-week time diary with the administrators in Poland and India, logging
  absence-related tasks in 15-minute blocks.
- Twelve months of HR service-desk tickets tagged leave or absence: volume,
  handling time, and how many are "what is my balance".
- A count of manual adjustments in the current spreadsheets over one leave year.
- Measured before and after on the pilot entity - the only number that settles
  it.

If the measured figure comes in materially below 0.4 FTE, the honest response is
to say so and re-argue the project on compliance exposure alone, which it can
carry.

### What the released capacity should do

Vague on purpose is how this claim usually dies, so, specifically:

- **Clear the evidence backlog.** Every UNKNOWN is a real person whose
  entitlement cannot currently be determined. Collecting Polish service
  documentation is unglamorous, finite, and directly increases what several
  people are actually owed.
- **Use leave data as a wellbeing signal.** Once balances are trustworthy,
  unused-leave concentration and chronically deferred holiday are readable at
  team level. That is a burnout indicator and a manager-behaviour indicator, and
  it is currently invisible because the underlying numbers cannot be trusted.
- **Coach managers on approving time off**, using the data - who defers, whose
  team never takes leave in Q4, where approvals stall.
- **Own the next process.** The same person who learned policy-as-data on
  absence is the right person to apply it to working time or probation.

The quality claim in one line: **HR gets out of the business of maintaining
spreadsheets and into the business of noticing things** - which is the part that
affects culture, and the part that cannot be automated.

---

## 6. When I would stop the rollout

Stated in advance, because the point of kill criteria is that they are agreed
before anyone is invested.

- Works council consultation in DE or NL is unresolved after one quarter → those
  entities are removed from scope; the others continue.
- The pilot's match rate does not improve between cycle 1 and cycle 3 → the
  policy files are wrong, not the spreadsheets. Stop and re-derive the rules.
- Named destination roles for the administrators cannot be committed → pause
  before the parallel run, not after.
- The no-clawback position is not agreed before the pilot → do not run the
  pilot. Discovering overstatements without an agreed answer is worse than not
  looking.
