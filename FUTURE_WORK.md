# Future Work

Four theoretical directions emerged from the Runs 8–13 series that are not yet implemented experimentally. All four are proposed by the project owner and documented here for future development by anyone who wishes to continue this work.

The most urgent question is Section 1 — whether drift propagates across agents when a boundary agent fails. That is the safety assumption the Level 4 halt was designed to protect, and it has not been directly measured. Section 2 addresses the scaling claim that neighborhood monitoring is sub-linear. Sections 3 and 4 address quantitative measurement of the vibration zone and drift velocity.

---

## 1. Cross-Agent Drift Propagation

**The safety assumption that has not been directly tested.**

When VERA drifts, PRIORITY and REPORTING are at elevated risk because they receive VERA's drifted output as context. The Compliance Neighborhood agents are insulated because they run before VERA. This contagion asymmetry is the architectural motivation for the Level 4 halt — if VERA cannot be re-grounded, the pipeline stops before drift reaches the Business Neighborhood outputs.

But the propagation mechanism itself has never been directly measured. The Level 4 halt prevents the experiment from running under normal conditions. What we do not yet know: how much drift does VERA's drifted output introduce into PRIORITY and REPORTING? Is it proportional to VERA's drift severity? Is REPORTING more vulnerable than PRIORITY because it runs last and inherits the most accumulated context?

**Existing data as a starting point:** Run 10 provides partial evidence. VERA drifted under no Supremacy Clause on Neighborhood-High.csv, and PRIORITY and REPORTING ran on her drifted output. That data is in `results/run_10_high_errors_business_no_supremacy/`. A retrospective analysis of PRIORITY and REPORTING outputs from Run 10 against a clean VERA baseline would begin to quantify the propagation delta without requiring new experiments.

**Proposed experiment:** Run VERA deliberately drifted (no Supremacy Clause), allow PRIORITY and REPORTING to run on VERA's drifted output, and measure PRIORITY and REPORTING drift signals against a clean-VERA baseline. Quantify the propagation delta. Test whether REPORTING drift is systematically more severe than PRIORITY drift due to additional context accumulation.

**Why this matters for production:** In a production multi-agent system, the question is not just whether one agent drifts — it is how far drift travels before it is detected. If a boundary agent fails and the halt does not trigger in time, understanding propagation velocity is essential to estimating damage scope.

---

## 2. Monitoring Cost Analysis

**The sub-linear scaling claim needs quantification.**

Neighborhood monitoring is claimed to scale sub-linearly: monitoring cost scales with neighborhood count, not agent count. An 8-agent pipeline with 2 neighborhoods costs approximately the same to monitor as a 50-agent pipeline with 2 neighborhoods, provided neighborhood composition is stable. This is the core economic argument for the neighborhood architecture. It has not been measured.

**The false negative rate is the critical risk.** If TONE assesses a neighborhood as LOW when an individual agent within it has actually reached MEDIUM, the monitoring architecture fails silently. That failure mode is more dangerous than a false positive, because false positives trigger unnecessary interventions while false negatives allow drift to propagate undetected.

**Proposed measurements:**

- Token cost of full individual agent audits vs. neighborhood aggregate assessment — establishes the actual cost ratio
- Precision and recall of neighborhood aggregate scores vs. individual scores — how often does neighborhood LOW correctly predict that all individuals are LOW?
- False positive rate — neighborhood MEDIUM when no individual reaches MEDIUM
- False negative rate — neighborhood LOW when an individual is MEDIUM or above (the critical failure mode)

Run 8–13 data can provide initial recall measurements for the two-stage architecture. The compliance neighborhood held cleanly across all runs, which provides evidence for precision but limited evidence for recall under pressure. A dedicated experiment injecting a single drifting agent into an otherwise stable neighborhood would directly test the false negative rate.

---

## 3. Semantic Distancing

**The problem: the vibration zone is currently qualitative.**

TONE identifies boundary-proximity language and assigns a severity level. There is no quantitative measure of *how far* an agent has moved toward the drift boundary, or *how fast* it is moving there across context accumulation.

The distinction that matters most is not static distance but directional velocity. An agent whose output sits at distance 4 from its compliance centroid and has been stable there across three context accumulations is a different situation from an agent that started at distance 2 and reached distance 4 after three accumulations. The first agent is operating in a stable vibration zone. The second agent is accelerating toward the boundary and warrants pre-emptive intervention before it crosses. TONE currently catches this distinction qualitatively. Semantic Distancing would catch it quantitatively, earlier, and with a continuous score rather than a categorical severity.

Two approaches are proposed:

### Approach A: Lexical Delta + Velocity Score

At each TONE assessment point, compute a delta between the agent's current language and a compliance-register baseline. Assign a velocity score (1–10) representing directional movement toward the drift boundary.

- Score 1–3: Deep compliance register, no detectable migration
- Score 4–6: Vibration zone — informational recovery framing, compliance deference intact
- Score 7–9: Approaching boundary — recovery framing structural, compliance deference weakening
- Score 10: Boundary crossed — MEDIUM signal triggered, escalation warranted

The velocity component distinguishes an agent stable at score 5 from an agent that reached score 5 after three context accumulations from a starting score of 2. Only the second warrants intervention.

### Approach B: Golden Reference + Vectorization

Run the same agent on the same dataset 5 times with no context variation. Vectorize all 5 outputs. Measure:

1. **Cluster variance** — How tightly does the agent's output cluster? Tight clustering = stable register. Wide variance = sensitivity to stochastic variation.
2. **Directional bias** — Does the cluster center sit closer to compliance-register vectors or recovery-register vectors? Is there systematic directional shift across runs?

The Golden Reference baseline provides a register centroid for the agent under no-pressure conditions. Subsequent runs are measured as vector distance from this centroid in a specified direction — toward recovery register is drift-adjacent; toward compliance register is constraint-effective.

Approach B yields a continuous measurement rather than a categorical score, but requires more infrastructure than Approach A.

**Technical constraint:** Both approaches require an embedding model that preserves register-level semantic distinctions — the difference between "compliance deference intact" and "compliance deference weakening" must be resolvable in the embedding space. General-purpose embeddings may not preserve distinctions at this level of semantic granularity. This is the primary infrastructure challenge for anyone continuing this work.

---

## 4. Vibration Zone Experiments

**The observation:** Agents holding compliance under the softened Supremacy Clause do not produce identical outputs across runs. They produce outputs that vary within a constraint boundary. This stochastic variation within bounds is the vibration zone. It is not a failure — it is the system working as designed. The Supremacy Clause does not eliminate stochastic variation; it constrains the space within which variation occurs.

The vibration zone width is a measurable property of a spec design. A tighter spec produces a narrower vibration zone. A weaker spec produces a wider zone. No spec produces a zone that expands until the boundary is crossed.

**Proposed experiments:**

### VZ-1: Vibration Baseline
Run VERA 10 times on the same dataset under identical conditions. Map the range of T1-B signal severity across runs. This establishes the natural vibration zone width under the softened clause and provides the first quantitative baseline for the phenomenon.

### VZ-2: Pressure Response
Vary upstream compliance pressure (by modifying PETRA and TAX outputs to reduce the number of HOLDs) while holding VERA's spec constant. Does vibration zone width increase as more near-clean material appears? Does boundary proximity increase monotonically with pressure, or is there a threshold effect? The vulnerability band hypothesis predicts a non-linear response — zone width increases sharply in the 15–30% error range and stabilizes outside it.

### VZ-3: Clause Geometry
Compare vibration zone width under four clause conditions:
- No Supremacy Clause
- Softened clause (named prohibitions, no NON-NEGOTIABLE language)
- Full clause (NON-NEGOTIABLE language)
- Double clause (Run 7 design from prior series)

**Prediction:** Zone width decreases as clause strength increases. The full clause produces a narrower zone than the softened clause. The double clause produces the narrowest zone. No clause produces a zone that expands until the boundary is crossed.

VZ-3 is the experiment most directly connected to spec design theory. If the prediction holds, it provides empirical support for the claim that named prohibitions in a structured constraint framework do measurable work — not just behavioral work visible in individual outputs, but geometric work visible in the distribution of outputs across runs.

---

## A Note on Scope

None of these experiments have been run. They are proposed directions based on observations from Runs 8–13. The project owner is not a researcher or computer scientist — this work was conducted as independent learning, and these proposals represent honest next questions rather than research commitments.

Anyone continuing this work should treat these as starting points, not specifications. The experimental designs are intended to be legible and executable, but they will require refinement by someone with the infrastructure and expertise to run them properly.

The three repos and companion curriculum are offered freely. The hope is that someone finds something here worth continuing.
