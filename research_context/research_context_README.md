# research_context/

## Purpose

This folder contextualizes the Tone Agents Neighborhoods experimental series against a parallel body of work from the broader AI research community. The primary reference point is the Google DeepMind paper *Towards the Science of Scaling Agents* (Kim, Gu, Park, et al.), which provides an empirical and theoretical framework for understanding how multi-agent systems behave as complexity increases.

The materials here serve two functions:

1. **Positioning** — documenting where this project's findings converge with and diverge from production-scale monitoring approaches
2. **Extension** — providing prototype implementations of measurement techniques (semantic entropy, NLI-based clustering) that could formalize drift quantification beyond qualitative assessment

---

## Contents

### `Towards a Science of Scaling Agent Systems.pdf`
The anchor document for this folder. This Google DeepMind paper examines scaling dynamics, agent architecture, and benchmarking frameworks across tasks including code generation, web navigation, mathematical reasoning, and multi-step planning. It provides the external framework against which the Tone Agents findings are positioned.

**Recommended starting point** for newcomers to this folder.

---

### `Positioning_This_Work.md`
The core comparative analysis. This document maps the Tone Agents experimental series against 2025/2026 production monitoring systems and the DeepMind scaling research, identifying where the two bodies of work converge and where they represent fundamentally different approaches.

**Key thesis:**
> *"The field converged on surveillance. This work converged on constitution. Both are necessary. Neither is sufficient alone."*

Key comparisons documented:
- **Scaling metrics**: message density, redundancy rates, and error amplification patterns in the DeepMind work map to neighborhood-level drift signals identified in Runs 8–13
- **Semantic entropy detection**: vocabulary migration signals in production systems parallel the vibration zone behavior observed in constrained agents
- **Circuit breakers**: the Level 4 Halt mechanism in production frameworks and the "Drunk Walking" circuit breaking pattern correspond to the Supremacy Clause's role as an inference-time posture constraint

The document draws a precise distinction between the two approaches: production systems apply a **Pre-Inference Membrane** that validates evidence before reasoning begins, while the Supremacy Clause constrains **reasoning posture during inference**—a different intervention point with different failure modes and different cost profiles.

Limitations of the current work are also documented here: LLM variance prevents single-run reliability claims, vibration zone quantification remains incomplete, and context pruning has not been systematically benchmarked.

---

### `semantic_entropy_logic.py`
A prototype implementation of Shannon Entropy-based drift measurement for model response consistency.

**Core concept:** If a constrained agent produces ten responses that cluster semantically together, entropy is low (stable). If responses diverge across multiple semantic clusters, entropy is high (drifting). This operationalizes the qualitative drift classifications used in the TONE monitoring assessments into a quantifiable score.

```
SE = -sum(P(C) * log(P(C)))
```

Where `P(C)` is the proportion of samples falling into each semantic cluster. Example calibration points:
- 90% of samples in one cluster → entropy ≈ 0.33 (stable/constrained behavior)
- 50/50 split across two clusters → entropy ≈ 0.69 (maximum uncertainty/drift)

This addresses one of the open research questions in `FUTURE_WORK.md`: how to move from qualitative Tier 1/Tier 2 drift classification to quantitative semantic distance measurement.

---

### `Automated_Clustering_NLI.py`
A prototype implementation of statement clustering using Natural Language Inference (NLI) via the `cross-encoder/nli-deberta-v3-small` transformer model.

The clustering logic compares each new agent output against existing cluster heads using entailment detection. Semantically equivalent statements join existing clusters; statements that fail entailment thresholds form new clusters. The output feeds directly into the entropy calculation in `semantic_entropy_logic.py`.

**Example behavior:**
- "The capital of France is Paris" and "Paris is the capital of France" → same cluster (entailment detected, semantically equivalent)
- "Lyon is the capital of France" → new cluster (contradiction detected, semantic drift flagged)

This prototype is designed to complement the neighborhood monitoring architecture: rather than requiring human evaluation of TONE's aggregate drift scores, NLI clustering could automate the detection of semantic divergence across agent outputs within a neighborhood.

---

### `evidence_validator_spec.md`
A production-ready agent specification for a pre-inference evidence validation layer. This document extends the Supremacy Clause architecture by specifying what a formal **Pre-Inference Membrane** would look like as a deployable agent component.

Core functions:
- Source verification and temporal relevance checking (data currency within 24 hours)
- Logical contradiction detection via NLI (zero tolerance)
- Context efficiency optimization (substantive content >60% of tokens)
- Trust scoring with circuit breakers (source blacklisting after 3 failures)

**Output format:** JSON certification including evidence IDs, integrity scores, and trust thresholds (>0.85 required for passage).

This specification addresses the "context poisoning" failure mode—where contaminated or stale evidence corrupts agent reasoning before any constraint structure can act—and represents a complementary layer to the inference-time constraints tested in Runs 8–13.

---

## Reading Order

For collaborators continuing from the main experimental series:

1. `Positioning_This_Work.md` — orient against the external research landscape
2. `Towards the Science of Scaling Agents.pdf` — review the DeepMind framework directly
3. `semantic_entropy_logic.py` + `Automated_Clustering_NLI.py` — evaluate prototype implementations against the open quantification questions in `FUTURE_WORK.md`
4. `evidence_validator_spec.md` — consider the pre-inference membrane as a complement to the Supremacy Clause architecture

For newcomers: start with the root `README.md` and `FINDINGS.md` in the main repository before reading this folder.

---

## Relationship to Open Research Questions

The materials in this folder directly address items documented in `FUTURE_WORK.md`:

| Open Question | Relevant File |
|---|---|
| Semantic drift quantification beyond qualitative assessment | `semantic_entropy_logic.py`, `Automated_Clustering_NLI.py` |
| Vibration zone characterization and measurement | `semantic_entropy_logic.py` |
| Monitoring cost false-negative analysis | `Positioning_This_Work.md` |
| Context pruning benchmarking | `evidence_validator_spec.md`, `Positioning_This_Work.md` |

---

## Provenance

The materials in this folder emerged from a structured research journey conducted 
in March 2026, after the completion of Runs 8–13. The journey began with the 
Kim et al. scaling paper and moved through DeepMind's Golden Rule, Inference 
Time Scaling, Google's Pre-Inference Governance framework, Inference-Time 
Intervention research, and the 2025/2026 Semantic Entropy literature before 
arriving at the production monitoring landscape represented by ADK LoopAgent 
and Maxim AI.

The research was conducted by the project owner in collaboration with Claude 
Sonnet 4.6 (Anthropic). The comparison document (`Positioning_This_Work.md`) 
was written at the end of that journey — not during it — to ensure the full 
landscape was understood before any positioning claims were made.

The prototype implementations (`semantic_entropy_logic.py`, 
`Automated_Clustering_NLI.py`) and the evidence validator specification 
(`evidence_validator_spec.md`) were sourced from Gemini (Google, March 2026) 
in response to specific research questions about how production systems 
implement the measurement techniques described in the literature. They are 
included here as reference implementations, not as original contributions of 
this project.

The central finding that emerged from this journey — that the field converged 
on surveillance while this work converged on constitution — was not a 
hypothesis going in. It was a discovery coming out.

---

## Note on Scope

The implementations in this folder (`semantic_entropy_logic.py`, `Automated_Clustering_NLI.py`) are prototypes intended to demonstrate measurement approaches, not production-ready tools. They have not been run against the existing experimental datasets. Integration with the pipeline architecture used in Runs 8–13 would require adaptation to the logging and output formats documented in `/scripts/`.
