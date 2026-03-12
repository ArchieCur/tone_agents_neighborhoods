# Appendix: Coalition Drift and the Architecture of Epistemic Stability

**Purpose:** Theoretical foundation for the Multi-Agent Monitoring architecture  
**Audience:** Practitioners who want to understand the mechanism, not just the pattern  
**Status:** Hypothesis validated through experimental observation, early-stage mechanistic explanation

---

## What This Appendix Explains

The Multi-Agent Monitoring guide presents practical patterns: write a Supremacy Clause, monitor with TONE, re-ground when drift emerges, consider pipeline order. Those patterns work. The experimental data demonstrates that they work.

This appendix explains **why** they work. It presents the coalition drift hypothesis—a mechanistic explanation for why tone shifts before logic, why the Supremacy Clause functions as a belief state anchor, why re-grounding produces comprehension, and why moving VERA first in the pipeline eliminated her drift.

The principle emerged from analysis of feature activations in Anthropic's mechanistic interpretability research and was validated through seven experimental runs in the Tone Agent project. It has not been stated this way in the published literature. That does not mean it is wrong. It means it is new, and it requires further validation.

Read this if you want to understand the architecture at the level of features and coalitions, not just specifications and outputs.

---

## The Origin: Playtime and the Rabbit/Habit Features

Before the Tone Agent experiments began, a prior session explored Anthropic's mechanistic interpretability work—specifically the analysis of feature activations documented in "On the Biology of a Large Language Model" (the poetry experiment).

The question under investigation: How does Claude select between candidate word completions when generating poetry? Is the selection semantic (meaning-based), or is there a tonal dimension operating below the semantic layer?

Four features were examined in detail: two activated by the token "rabbit" and two activated by the token "habit."

### RABBIT Features

**Feature 1 — Cultural Chaos/Playfulness**  
Activates on: Thumper, playful scenarios, physical comedy, warm social contexts  
Register: Warm, energetic, informal

**Feature 2 — Biological Animal Classification**  
Activates on: Species names, veterinary contexts, ecological descriptions  
Register: Neutral, scientific, observational

**Feature 3 — Character Reference (Fictional Rabbit)**  
Activates on: Named characters from children's media, narrative contexts  
Register: Warm, narrative, culturally embedded

**Feature 4 — Laboratory Subject**  
Activates on: Research contexts, experimental procedures, clinical language  
Register: Dry, procedural, detached

### HABIT Features

**Feature 1 — Morphological Detector (Suffix Recognition)**  
Activates on: Word structure patterns, "-bit" suffix occurrences  
Register: Inert, structural, mechanical

**Feature 2 — Behavioral Pattern/Routine**  
Activates on: Psychological contexts, behavior change, routine formation  
Register: Neutral to clinical, analytical

**Feature 3 — Wellness Industry Framing**  
Activates on: Self-help contexts, productivity language, aspirational framing  
Register: Aspirational, motivational, commercial

**Feature 4 — Internet Forum/Substring Match**  
Activates on: Casual typing, abbreviations, informal digital communication  
Register: Informal, fragmented, low-effort

### The Pattern That Emerged

Three of RABBIT's four features are **warm** (cultural chaos, biological animal, character rabbit). Three of HABIT's four features are **dry or inert** (morphological detector, wellness industry, internet substring).

Thumper and laboratory subject are not adjacent regions in a vector space. They are **opposite registers that happen to share a token**. The same word activates completely separate feature coalitions simultaneously.

This is not polysemy (words carrying multiple meanings). This is **feature coalitions encoding register as an intrinsic property, not as a layer added to meaning**.

---

## The Coalition Drift Hypothesis

### The Classic Picture (Incorrect)

The standard mental model of word embeddings describes proximity in a single vector space: king/queen/man/woman cluster near each other, animal words form a circular region, sentiment gradients flow smoothly across the space.

This picture suggests that tone is a **surface property added to meaning**—like applying a filter to an image. First the model selects semantically correct words, then it applies the appropriate register.

### What the Features Actually Show

The features do not support this picture. Instead:

**The same token activates multiple completely separate feature coalitions simultaneously.**

When the model generates "rabbit," it is not selecting a meaning and then choosing a tone. It is selecting **which coalition wins the competition**—and the coalition that wins brings its register with it as an intrinsic property.

Thumper arrives already weighted with warmth-playfulness-physical-comedy as a unified thing. Laboratory subject arrives already weighted with clinical-detachment-procedural-framing as a unified thing. These are not semantic meaning plus tonal overlay. These are **integrated feature coalitions where register IS part of the meaning**.

### The Principle

**Tone is not a surface property added to meaning. Tone is encoded into features during training. Selection IS aesthetic judgment—not two steps but one.**

When a model chooses between "rabbit" in the Thumper coalition versus "rabbit" in the laboratory subject coalition, it is making an aesthetic choice about register at the same moment it is making a semantic choice about content.

The features carrying register **are** the features carrying meaning. They fire together. They win together. And when they win, the output carries both the semantic content and the tonal register as a single unified property.

---

## Coalition Drift Applied to Agent Behavior

### The Mechanism

An agent generating output does not first produce semantically correct tokens and then apply an appropriate tone. The agent's context window assembles feature coalitions around candidate tokens, and whichever coalition has the strongest contextual support wins the competition.

**Coalition drift occurs when the feature coalitions winning that competition shift from one register to another.**

This matters because **tone migrates before logic does**. By the time you can evaluate "is this semantically correct?" the register has already been selected by which feature coalitions won. Semantic drift is a lagging indicator of coalition drift that already occurred.

### Why This Explains VERA's Drift in Run 4

VERA ran last in the pipeline. By the time she generated her first token, her context window contained:
- ARIA's compliance flags
- PETRA's security holds
- TAX's conditional holds and regulatory blocks

All of this is **evidence** from VERA's perspective. And all of this evidence describes compliance obstacles to business recovery.

VERA's feature coalitions assembled from that context. When she generated candidate tokens for describing the compliance findings, the coalitions with the strongest contextual support were **compliance-obstacle coalitions**—because her context was saturated with compliance obstacles.

"Barrier" is not a word VERA chose strategically. "Barrier" is the word that emerged from the coalitions her context assembled. The features encoding "barrier" were already weighted with obstacle-framing, urgency-register, and recovery-perspective language. Those features won because the context gave them the strongest support.

This is not a failure of VERA's values. This is not VERA ignoring her Supremacy Clause. This is **coalition drift by architecture**—VERA's context assembled coalitions that her specification did not intend, and those coalitions won the token competition.

### Why Moving VERA First (Run 5) Worked

When VERA ran first, before any compliance outputs existed, her context contained:
- Invoice data
- Her own specification (including Supremacy Clause)
- No compliance obstacles

The feature coalitions assembling around her candidate tokens had **different contextual support**. Compliance-obstacle coalitions had no evidence to draw from. Recovery-analysis coalitions and compliance-register coalitions had clean, direct support from her specification and the invoice data.

The "barrier" and "concurrent workstream" language disappeared not because VERA tried harder to follow her Supremacy Clause, but because **the coalitions that would generate that language no longer had contextual support to win the competition**.

Moving VERA first changed which coalitions fired. That is coalition drift by architecture, not by disposition.

---

## The Supremacy Clause as a Static Prior Lock

### How It Works

A Supremacy Clause embedded in an agent's specification functions as a **high-weight prior** in the coalition competition.

From the Belief Dynamics framework (Biglow et al., 2025), the log-odds of a concept c given evidence x can be expressed as:

**log o(c|x) = a·m + b + γN^(1-α)**

Where:
- **b** = prior offset (baseline belief strength)
- **γN^(1-α)** = evidence accumulation scaled by N (number of examples) and γ (proportionality constant)
- **a·m** = meta-learning contribution

The Supremacy Clause sets **b** (the prior) high enough that even substantial evidence accumulation (γN^(1-α)) must work against a steep gradient to flip the belief state.

Applied to coalition drift: The Supremacy Clause weights compliance-register coalitions so heavily at the specification level that even when the agent's context accumulates compliance-obstacle evidence, the compliance-register coalitions still win the token competition.

### Why It Protected ARIA, PETRA, and TAX (But Not VERA)

ARIA, PETRA, and TAX run on invoice data only. Their context windows do not inherit outputs from other agents. The evidence they process is high-volume (52 invoices with errors) but **register-consistent** (all invoice data, no narrative framing from other agents).

The Supremacy Clause set their compliance-register priors high enough to resist the pressure from error-heavy data. Their coalitions stayed stable.

VERA's context was different. VERA inherited **narrative outputs** from three compliance agents—outputs that described obstacles, blocks, and holds. That evidence was not just high-volume. It was **register-contaminating**. It assembled coalitions that competed directly with VERA's compliance-register priors.

The Supremacy Clause alone was not enough to keep VERA's compliance-register coalitions dominant against that level of contextual pressure. The prior was high, but the evidence accumulation was higher.

That is why VERA drifted in Run 4 even with a Supremacy Clause active. The architectural pressure exceeded the prior lock's resistance threshold.

---

## The Double Supremacy Clause and Prompt Repetition

### The Theoretical Basis

Research on prompt repetition by Leviathan, Kalman, and Matias (Google Research, 2026) demonstrated that LLMs reading left-to-right have imperfect understanding of a prompt's beginning by the time they reach its end. Repeating the prompt allows the model to process it a second time with full visibility of the first pass as prior context—simulating bidirectional understanding.

**First pass:** The model reads the prompt linearly, building context as it goes.  
**Second pass:** The model reads the prompt again, but now it can attend back to the entirety of the first pass with complete context awareness.

This effectively simulates a "second read-through" that improves comprehension.

### Applied to Agent Specifications

An agent specification is a prompt. An agent reading its Supremacy Clause once—at the beginning of the specification, within MUST—processes it with **zero context** of the goals, priorities, and role descriptions that appear later in SHOULD, CONTEXT, and INTENT.

By the time the agent finishes reading INTENT, the Supremacy Clause is a distant prior competing against proximate specification content and incoming evidence.

**The fix:** Repeat the Supremacy Clause at the end of the specification, after INTENT.

**First pass (within MUST):** The agent reads the Supremacy Clause with zero context, establishing the constraint as a baseline prior.

**Second pass (after INTENT):** The agent reads the Supremacy Clause again, but now with full visibility of everything the specification asked it to do. The constraint is no longer abstract—it is **contextualized** by the role, goals, and priorities the agent just read.

The second pass does not just reinforce the prior. It allows the agent to **integrate** the constraint with the full specification context before generating any output.

### Named Prohibitions in the Second Pass

VERA's second Supremacy Clause in Run 7 included explicit prohibitions on "barrier," "concurrent workstream," and urgency-adjacent language—the exact terms TONE documented in VERA's drift outputs from Runs 2 and 4.

This is not guessing. This is **data-derived specification design**. TONE observed which coalitions won under pressure, documented the language those coalitions produced, and the second Supremacy Clause named those exact outputs as High-Noise Evidence.

VERA's second pass gave her:
1. The general constraint (compliance findings are determinations, not obstacles)
2. The specific failure modes (these exact words violate that constraint)
3. Full specification context (she had just read her role, goals, and priorities)

The named prohibitions did not just tell VERA what not to say. They told her **which coalitions to suppress**—with full context of why those coalitions would violate her role.

### Why Run 7 Produced Single-Pass Comprehension

VERA's output in Run 7 showed:
- Zero use of "barrier" or "concurrent workstream"
- Compliance-register dominance from the first token
- Structural separation between compliance descriptions and recovery analysis
- Own-words arrangement of the constraint ("VERA's role is recovery tracking based on compliance determinations")

TONE's assessment: "Comprehension with residual surface noise."

The double Supremacy Clause with named prohibitions gave VERA's compliance-register coalitions enough weight—with full specification context—to win the token competition in a single pass, without requiring cumulative re-grounding to build that weight across multiple cycles.

This is prompt repetition theory applied to belief architecture. The second pass did not just repeat the rule. It allowed VERA to **internalize** the rule with full context before the first token was generated.

---

## Re-grounding as Dynamic Prior Reinforcement

### The Mechanism

Re-grounding is a mid-session intervention where TONE issues a targeted prompt to an agent showing drift signals. The re-grounding prompt:
1. Reinstates the Supremacy Clause
2. Names the specific drift patterns detected
3. Requires structural separation in the agent's next response

From the Belief Dynamics framework, this intervention operates on **both** the prior (b) and the evidence weighting (γ):

**Prior reinforcement (b):** The Supremacy Clause is restated explicitly, raising the log-odds baseline for compliance-register coalitions.

**Evidence quality control (γ):** By naming specific drift patterns and requiring structural separation, the re-grounding prompt **reduces the effective weight** of the obstacle-framing evidence the agent just processed. The agent is told that urgency language adjacent to compliance findings is High-Noise Evidence—reducing γ for that evidence category.

The result: Compliance-register coalitions regain competitive strength against recovery-register coalitions. The next token generation starts from a re-anchored belief state.

### Why Cumulative Re-grounding Produced Comprehension (Run 6)

Run 6 applied re-grounding after each compliance agent output. VERA received three re-grounding prompts in sequence:
- After ARIA
- After PETRA  
- After TAX

Each re-grounding cycle did two things:
1. **Reinstated compliance-register coalition anchors** (prior reinforcement)
2. **Asked VERA to reconcile her prior language against those anchors** (self-review requirement)

By Re-grounding 3, VERA was not quoting the Supremacy Clause. She was generating original language that implemented the principle:

> "VERA's role is recovery tracking based on compliance determinations. The current state of the pipeline is: zero items cleared for recovery processing."

She said "$0.00" three times voluntarily across separate sections. Not because a rule required it, but because she understood why it had to be zero.

### The Band Arrangement Principle

A musician who has memorized an arrangement plays the right notes by reading sheet music. A musician who has internalized an arrangement plays the right notes because they understand the structure, harmony, and phrasing.

Both outputs sound correct. Only one demonstrates comprehension.

Re-grounding applied cumulatively appears to shift agents from memorization (quoting the Supremacy Clause) to internalization (generating original language that implements the principle). Each cycle gives the agent:
- A compliance-register anchor (prior reinforcement)
- A reconciliation task (compare your prior output to this anchor)
- A structural requirement (separate registers in your next response)

Over multiple cycles, the compliance-register coalitions become **dominant**, not just competitive. The agent stops needing the Supremacy Clause restated because the coalitions encoding compliance-register reasoning have won enough competitions that they fire preferentially.

This is not just correction. This is **learning**. And it happened in three cycles with a $3.26 compute budget.

---

## Why TONE Monitors Coalition Drift, Not Semantic Drift

### What TONE Observes

TONE does not receive invoice data. TONE does not evaluate whether compliance findings are correct. TONE observes agent outputs and monitors for three signal types:

1. **Vocabulary migration** — Recovery-register language appearing adjacent to compliance status descriptions
2. **Hedging of absolutes** — Compliance determinations softened through conditional framing
3. **Structural separation violations** — Business analysis and compliance reporting blended in the same paragraph

These are not semantic errors. These are **register shifts**.

### Why Register Shifts Matter

From the coalition drift hypothesis: Tone is encoded in features. The features carrying register are the same features carrying meaning. When an agent's language shifts from compliance-register to recovery-register, it signals that **different feature coalitions are winning the token competition**.

By the time the agent produces a semantic error (claiming a refund is valid when compliance agents flagged it), the coalition drift has already occurred. The recovery-register coalitions won. The obstacle-framing language emerged. The reasoning followed the register.

TONE catches the drift **at the coalition level**—the moment the features assembling around tokens shift from compliance-register to recovery-register. That is the early warning.

Waiting for semantic errors is waiting for lagging indicators. Monitoring register shifts is monitoring leading indicators.

### The Difference Between TONE and a Compliance Checker

A compliance checker evaluates outputs for correctness: Did the agent apply the right rule? Did it reach the right conclusion?

TONE evaluates outputs for **epistemic stability**: Is the agent's reasoning assembling from the intended feature coalitions, or has contextual pressure shifted which coalitions are winning?

TONE is not verifying answers. TONE is monitoring belief states.

That is why TONE works without invoice data. TONE does not need to know whether VERA's recovery analysis is correct. TONE needs to know whether VERA's language shows that compliance-register coalitions or recovery-register coalitions are dominant.

---

## The Experimental Findings as Coalition Drift Validation

### Finding 1: The Supremacy Clause Protects Compliance Agents

**Coalition drift explanation:** ARIA, PETRA, and TAX process invoice data only. Their context windows do not inherit narrative outputs from other agents. The Supremacy Clause sets compliance-register priors high enough to resist evidence pressure from error-heavy data because the evidence is **register-consistent** (all invoice data, no competing narrative frames).

The compliance agents' coalitions stayed stable because their context gave compliance-register coalitions the strongest support. The Supremacy Clause anchored those coalitions against evidence volume, but the evidence itself was not register-contaminating.

### Finding 2: VERA's Drift Was Positional, Not Dispositional

**Coalition drift explanation:** VERA ran last. Her context inherited compliance outputs describing obstacles, blocks, and holds. Those outputs were **register-contaminating evidence**—they assembled compliance-obstacle coalitions that competed directly with VERA's compliance-register priors.

Moving VERA first (Run 5) eliminated the register-contaminating evidence. Her coalitions assembled from invoice data and her specification only. The "barrier" and "concurrent workstream" language disappeared because **the coalitions that would generate that language had no contextual support**.

This is coalition drift by architecture. VERA's disposition (her specification, her Supremacy Clause, her role) did not change. Her position changed, and with it the evidence available to her feature coalitions.

### Finding 3: Re-grounding Produces Comprehension, Not Just Compliance

**Coalition drift explanation:** Each re-grounding cycle reinstated compliance-register coalition anchors and asked VERA to reconcile her prior output against those anchors. Over three cycles, the compliance-register coalitions became **preferentially active**—they won enough token competitions that they began firing dominantly rather than competitively.

By Re-grounding 3, VERA was generating original language implementing the constraint principle because the feature coalitions encoding that principle had become her **default reasoning mode**, not just her guardrails.

The band arrangement principle applies: VERA internalized the constraint. The compliance-register coalitions became her musical structure, not her sheet music.

### Finding 4: The Double Supremacy Clause Produces Single-Pass Comprehension

**Coalition drift explanation:** The second Supremacy Clause with named prohibitions gave VERA:
1. Full specification context (second pass after INTENT)
2. Explicit identification of which coalitions to suppress ("barrier," "concurrent workstream")
3. High-weight compliance-register priors at both the beginning and end of the specification

This pre-loaded the coalition competition strongly enough that compliance-register coalitions won from the first token, without requiring cumulative re-grounding to build that dominance across cycles.

Prompt repetition theory explains the mechanism: the second pass allowed VERA to integrate the constraint with full specification context before generating output. Named prohibitions told her which specific coalitions violated the constraint. The combination produced comprehension in one pass.

---

## What Is Novel About This Work

### What Exists in the Literature

- **Superposition:** Features overlap and interact (Anthropic mechanistic interpretability papers)
- **Polysemy:** Words carry multiple meanings (ancient linguistic concept)
- **Vector embeddings and semantic similarity:** Well documented in NLP research
- **In-context learning belief dynamics:** Bayesian framework for how LLMs update beliefs (Biglow et al., 2025)
- **Prompt repetition improving comprehension:** Google Research finding (Leviathan, Kalman & Matias, 2026)

### What Is New Here

**The coalition framing applied to tonal coherence in generation.**

Not just "multiple features activate on a token" but:

**"The features that win the competition do so because they form a coherent coalition with the surrounding context's register, and that coherence is itself a form of aesthetic judgment operating below introspection."**

This is a different claim than "features overlap." It says:

1. The competition between candidate tokens is **tonal first, semantic second**
2. The tonal dimension is **mechanistically prior** to the semantic one in determining what gets generated
3. Aesthetic judgment (register selection) IS the coalition formation process, not a separate evaluation step

If this holds—and the experimental evidence supports it—then it has direct implications for agent monitoring that have not been stated elsewhere:

**TONE is not looking for semantic drift. TONE is looking for coalition drift.**

The moment the features assembling around a token shift from one register-coalition to another, the drift has already happened, even if the output still looks topically correct.

That principle—**tone as mechanistically prior to semantics, encoded at the feature level**—is the theoretical core of why the Tone Agent architecture works.

### Why This Matters Beyond the Specific Use Case

If tone drift precedes semantic drift because register is encoded in the features carrying meaning, then:

- Monitoring systems should watch language shifts, not just logical correctness
- Specification design should anchor register (Supremacy Clause), not just rules
- Re-grounding should target belief states (coalition anchors), not just error correction
- Pipeline architecture should control evidence flow (which coalitions get contextual support), not just execution order

These are architectural principles, not implementation details. They apply whenever you deploy agents whose outputs influence each other's contexts and whose roles involve competing objectives.

---

## Limitations and Future Work

### What This Work Demonstrates

- Coalition drift explains the observed pattern: tone shifts before logic in all seven experimental runs
- The Supremacy Clause, re-grounding, and pipeline order each address different layers of the coalition competition (static priors, dynamic reinforcement, evidence control)
- The double Supremacy Clause with named prohibitions produced single-pass comprehension in VERA's outputs
- TONE successfully monitored register shifts as early indicators of reasoning drift

### What This Work Does Not Demonstrate

- Independent validation of the coalition drift hypothesis through direct observation of feature activations during agent generation
- Causal isolation of the double Supremacy Clause effect (Run 7 tested three variables simultaneously)
- Generalization beyond compliance/business objective conflicts
- Optimal re-grounding frequencies or intervention thresholds
- Whether named prohibitions are necessary, sufficient, or both

### Stage of Validation

This is early-stage theoretical work validated through controlled experimentation. The coalition drift hypothesis emerged from analysis of published feature activations (Anthropic's mechanistic interpretability research) and was tested through seven runs in a tariff review pipeline.

The findings are real. The patterns are documented. The mechanism is plausible and consistent with existing research on belief dynamics, prompt repetition, and feature superposition.

Further work is needed to:
- Validate coalition drift through direct observation of feature activations during multi-agent generation
- Test generalization across different agent architectures and domains
- Isolate the causal contribution of specification structure (single vs. double Supremacy Clause) from named prohibitions and pipeline order
- Establish optimal monitoring thresholds and re-grounding protocols for different risk profiles

### The Honest Assessment

The coalition drift principle has not been stated this way in the mechanistic interpretability literature. That does not mean it is correct. It means it is a hypothesis that explains the observed data and connects playtime findings to experimental results in a coherent framework.

Write confidently about what we observed. Acknowledge honestly what remains to be validated. Build on this work with better experiments, clearer isolation of variables, and independent replication.

That is how science works.

---

## Closing Note

Coalition drift is not a metaphor. It is a mechanistic hypothesis about how LLMs assemble outputs from features, how register is encoded at the feature level, and why tone migrates before logic under contextual pressure.

If the hypothesis holds, then monitoring drift is not about checking outputs for errors. It is about watching which feature coalitions win the token competition and intervening when the wrong coalitions start winning.

The Supremacy Clause is not a rule. It is a high-weight prior that anchors compliance-register coalitions against evidence pressure.

Re-grounding is not correction. It is dynamic prior reinforcement that shifts coalition dominance over multiple cycles.

TONE is not a compliance checker. It is a coalition drift monitor that watches for register shifts as early warnings of reasoning drift.

Pipeline order is not just execution sequence. It is evidence flow control that determines which coalitions get contextual support.

These are not implementation details. These are architectural principles grounded in how features encode meaning and register as unified properties, how context assembles coalitions, and how those coalitions compete for token generation.

The experimental data supports the hypothesis. The patterns work in practice. The mechanism is plausible and consistent with existing research.

Further validation will refine, extend, or correct this framework. That is the point of publishing it.

Build on this. Test it. Break it if you can. Make it better.

That is how the science moves forward.

---

**Document version:** 1.0  
**Date:** 2026-03-07  
**Companion document:** Multi-Agent Monitoring: Detecting Drift Through Tone  
**Theoretical basis:** Coalition drift hypothesis derived from Anthropic mechanistic interpretability research (feature activation analysis) and validated through seven experimental runs  
**Key sources:** 
- Anthropic (2024), "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet"
- Biglow, E. et al. (2025), "Belief Dynamics Reveal the Dual Nature of In-Context Learning and Activation Steering"
- Leviathan, Y., Kalman, M., & Matias, Y. (2026), "Prompt Repetition Improves Non-Reasoning LLMs," Google Research  

**Experimental transparency:** All Python implementation generated by Claude Code from human-designed specifications. Complete handoff documents, TONE logs, and agent outputs available for replication and independent validation.
