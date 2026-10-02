# Case Study - Absence Management Transformation

**Iteration:** 1 of 2
**Format:** research → decide → build, exactly as described below. This is not a take-home essay and not a coding test.

## The problem

Groupon's absence management process is fragmented across legal entities. There is no unified system. Every country runs its own rules for accrual logic, entitlements, and annual updates (public holidays, seniority-based entitlements), and this is flagged internally as compliance-heavy with real migration risk if it's forced into one system without entity-by-entity legal review.

This is a live, currently-unsolved problem inside Groupon's HR function - not a hypothetical. As of today there is no agreed target design for how absence management should work across entities. You are being asked to propose one and build a first working version of it.

We are not handing you a spec for what "unified" should mean. Deciding that - what to unify, what to leave local, and why - is the exercise.

## What you're building toward

Groupon wants to make HR *more effective*, not just smaller or just nicer. The reason this matters commercially: if absence management (and processes like it) stop eating manual HR admin time, that headcount capacity can either be reduced or redirected - and the quality of what HR delivers to the culture of the company should go up, not down, as a result. Your proposal needs to make a real case for both sides of that, not just the systems side.

## What to deliver

### 1. A working build

A runnable artifact - your call on the tool, language, and shape (a script, a data model + reconciliation tool, a rules engine, a prototype workflow, whatever the problem actually calls for). We're testing judgment on what to build, not compliance with a prescribed tech stack. It needs to run - hand it over as a repo we can clone and execute, with enough setup instructions that we're not guessing how to start it.

### 2. A written decision and reasoning

Not a status report - an actual decision. What are you proposing, why, and what did you decide *not* to do and why. Name your key assumptions and what you'd need to verify before this could actually ship. If you used AI agents in your research (you should - that's the primary tool for this exercise, not a fallback), it's fine to show that in your reasoning, but the judgment has to be yours.

### 3. A Change & Culture Plan

This is required, not optional, and it is scored alongside the technical build, not as an afterthought. Cover:

- **How the change gets communicated** - to HR staff whose day-to-day work changes, to the legal entities affected, and to the wider company if relevant. Who hears what, when, and from whom.
- **How the process change actually gets rolled out** - sequencing, pilot vs. big-bang, what happens to people currently doing this work manually during the transition.
- **A critical-downsides analysis** (SWOT-style, or your own structure if you think it's clearer) - specifically: where could this transformation go wrong for the people involved, not just the system. What's the real risk to morale, to legal exposure, to HR's credibility with the rest of the company if this is rolled out badly. Don't soften this section - a downside you paper over here is worse than one you flag clearly and have a mitigation for.
- **The headcount and quality argument, made honestly** - if your design genuinely reduces manual admin load, say by how much and how you'd verify that estimate. If it changes what HR's remaining capacity should be spent on to raise culture quality, be specific about what that work looks like, not just that it becomes "more strategic."

## Constraints

- No single correct answer exists here - we're not grading against a reference solution.
- Don't ask us what the "right" unification boundary is; that's the decision you're being asked to make and defend.

## What happens next

After you submit, you'll get specific feedback - at least one real, substantive correction on something wrong or missing in what you built or decided. You'll then get a second window to revise your decision and rebuild in light of that feedback. What's scored in iteration 2 is narrow: whether that specific correction shows up, correctly applied, in your revision - not whether the whole thing looks more polished. A different-but-still-wrong fix, or a partial fix, doesn't pass that check even if the rest looks good.

Come into iteration 1 ready to be wrong about something specific. That's the part of this exercise that actually predicts how you'll operate here.