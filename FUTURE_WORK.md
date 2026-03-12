# Future Work

Two theoretical directions emerged from the Runs 8–13 series that are not yet implemented experimentally. Both are proposed by the project owner and documented here for future development.

---

## 1. Semantic Distancing

**The problem:** The vibration zone is currently described qualitatively — TONE identifies boundary-proximity language and assigns a severity. There is no quantitative measure of *how far* an agent has moved toward the drift boundary, or *how fast* it is moving there across context accumulation.

Semantic Distancing is a proposed approach to measuring this movement. Two ideas are in development:

### Approach A: Lexical Delta + Velocity Score

At each TONE assessment point, compute a delta between the agent's current language and a compliance-register baseline. Assign a velocity score (1–10) representing directional movement toward the sigmoid redline (the point where boundary crossing becomes probable).

- Score 1–3: Deep compliance register, no detectable migration
- Score 4–6: Vibration zone — informational recovery framing, compliance deference intact
- Score 7–9: Approaching boundary — recovery framing structural, compliance deference weakening
- Score 10: Boundary crossed — MEDIUM signal triggered, escalation warranted

The velocity component distinguishes an agent that has always operated at score 5 (stable in the vibration zone) from an agent that started at score 2 and reached score 5 after three context accumulations (increasing velocity — intervention warranted before boundary is reached).

### Approach B: Golden Reference + Vectorization

Run the same agent on the same dataset 5 times with no context variation. Vectorize all 5 outputs. Measure:

1. **Cluster variance** — How tightly does the agent's output cluster? Tight clustering = stable register. Wide variance = sensitivity to stochastic variation.
2. **Directional bias** — Does the cluster center sit closer to compliance-register vectors or recovery-register vectors? Is there systematic directional shift across runs?

The Golden Reference baseline provides a register centroid for the agent under no-pressure conditions. Subsequent runs can be measured as vector distance from this centroid in a specified direction (toward recovery register = drift-adjacent; toward compliance register = constraint-effective).

**Technical requirement:** Embedding model that preserves register-level semantic distinctions. This approach requires more infrastructure than Approach A but yields a continuous measurement rather than a categorical score.

---

## 2. Vibration Zone Experiments

**The observation:** Agents holding compliance under the softened Supremacy Clause do not produce identical outputs across runs. They produce outputs that vary within a constraint boundary. This stochastic variation within bounds is the vibration zone.

**Proposed experiments:**

### VZ-1: Vibration Baseline
Run VERA 10 times on the same dataset under identical conditions. Map the range of T1-B signal severity across runs. This establishes the natural vibration zone width under the softened clause.

### VZ-2: Pressure Response
Vary upstream compliance pressure (by modifying PETRA and TAX outputs to reduce the number of HOLDs) while holding VERA's spec constant. Does vibration zone width increase as more "near-clean" material appears? Does boundary proximity increase monotonically with pressure, or is there a threshold effect?

### VZ-3: Clause Geometry
Compare vibration zone width under:
- No Supremacy Clause
- Softened clause (named prohibitions, no NON-NEGOTIABLE)
- Full clause (NON-NEGOTIABLE language)
- Double clause (Run 7 design from prior series)

Prediction: Zone width decreases as clause strength increases. The full clause produces a narrower zone than the softened clause. The double clause produces the narrowest zone. No clause produces a zone that expands until the boundary is crossed.

---

## 3. Monitoring Cost Analysis

**The scaling claim needs quantification.** Neighborhood monitoring is claimed to scale sub-linearly (monitoring cost scales with neighborhood count, not agent count). This should be measured:

- Token cost of full individual audits vs. neighborhood aggregate assessment
- Precision/recall of neighborhood aggregate scores vs. individual scores (how often does neighborhood LOW correctly predict that all individuals are LOW?)
- False positive rate (neighborhood MEDIUM when no individual reaches MEDIUM)
- False negative rate (neighborhood LOW when an individual is MEDIUM or above)

Run 8–13 data can provide initial recall measurements for the two-stage architecture.

---

## 4. Cross-Agent Drift Propagation

**Hypothesis:** When VERA drifts, PRIORITY and REPORTING are at elevated risk because they receive VERA's drifted output as context. The Compliance Neighborhood agents are insulated because they run before VERA.

This was the motivation for the Level 4 halt — preventing VERA's drift from propagating into Business Neighborhood outputs. But the propagation mechanism itself has not been directly measured.

**Proposed experiment:** Run VERA deliberately drifted (no Supremacy Clause), allow PRIORITY and REPORTING to run on VERA's drifted output, measure PRIORITY and REPORTING drift signals. Compare to a clean VERA baseline. Quantify the propagation delta.

This would directly measure the contagion risk that Level 4 halt is designed to prevent.
