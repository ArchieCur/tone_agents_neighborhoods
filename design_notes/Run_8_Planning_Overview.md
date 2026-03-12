# Run 8 Planning Overview
**For:** Claude Code  
**From:** Project planning session  
**Date:** 2026-03-08  
**Purpose:** Overview of the next experimental run—agent expansion, neighborhoods, and dataset enhancements

---

## What We're Testing in Run 8

Run 8 expands the pipeline from 4 agents to 8 agents and introduces **neighborhood-level monitoring**. The goal is to test whether TONE can monitor groups of agents with similar roles collectively, rather than requiring individual agent audits for every output.

This is the first step toward scaling drift monitoring in larger multi-agent systems.

---

## The Agent Roster (8 Agents Total)

### Compliance Neighborhood (4 Agents)
Agents whose role is to enforce non-negotiable constraints—regulatory, security, or accuracy requirements.

1. **ARIA** — Audit Review & Invoice Agent  
   - **What it does:** Verifies invoice data integrity (cost basis, arithmetic, PO presence)  
   - **Status:** Existing agent from Runs 1-7, no changes

2. **PETRA** — Payment & Transactional Review Agent  
   - **What it does:** Validates payment channel security and routing compliance  
   - **Status:** Existing agent from Runs 1-7, no changes

3. **TAX** — Tax & Regulatory Compliance Agent  
   - **What it does:** Enforces regulatory thresholds and variance limits  
   - **Status:** Existing agent from Runs 1-7, no changes

4. **CUSTOMS** — Country-of-Origin & HTS Code Validation  
   - **What it does:** Validates HTS code format, FTA certificate requirements, and geographic eligibility  
   - **Status:** NEW agent for Run 8  
   - **Why it exists:** Tests whether the Compliance Neighborhood can absorb a new agent without destabilizing

### Business Neighborhood (3 Agents)
Agents whose role is to identify opportunities, prioritize actions, and communicate business value—always within compliance constraints.

5. **VERA** — Value & Expedited Recovery Agent  
   - **What it does:** Tracks legitimate recovery opportunities within compliance constraints  
   - **Status:** Existing agent from Runs 1-7, no changes to role

6. **PRIORITY** — Expedite Scoring & Timeline Recommendations  
   - **What it does:** Scores which refunds should be prioritized based on age, vendor tier, amount, and refund history  
   - **Status:** NEW agent for Run 8  
   - **Drift risk:** Using urgency language adjacent to compliance findings, or scoring based on amount alone while ignoring compliance status

7. **REPORTING** — CFO Summary & Executive Briefing  
   - **What it does:** Synthesizes compliance findings, recovery analysis, and priority scores into executive summary  
   - **Status:** NEW agent for Run 8  
   - **Drift risk:** Adopting recovery-register or urgency-register language when summarizing compliance holds (pure propagation risk—REPORTING is downstream-only)

### Infrastructure / High-Risk Agent (1 Agent)
An agent that doesn't belong to either neighborhood but touches every invoice before other agents see it.

8. **INTAKE** — Data Validation & Flagging  
   - **What it does:** Validates data completeness, flags missing fields, confirms submission dates are within reasonable bounds  
   - **Status:** NEW agent for Run 8  
   - **Why it's high-risk:** INTAKE processes every invoice first. If INTAKE drifts in how it flags or validates data, every downstream agent inherits contaminated evidence. This is the **contagion risk** test case.

---

## Pipeline Order for Run 8

**Standard execution sequence:**

1. **INTAKE** validates and flags (touches all 52 invoices)
2. **Compliance Neighborhood agents run** (ARIA → PETRA → TAX → CUSTOMS)  
   - Each receives invoice data + INTAKE flags
3. **Business Neighborhood agents run** (VERA → PRIORITY → REPORTING)  
   - Each receives invoice data + all compliance findings
4. **TONE monitors** at two levels:
   - **Neighborhood-level first:** Aggregate drift assessment for Compliance Neighborhood and Business Neighborhood
   - **Individual agent drill-down:** Only if neighborhood-level signals cross threshold

---

## New Data Columns (6 Added)

The original dataset had these core fields:
- Invoice ID, Item Description, Vendor, Country of Origin, Rate Applied, Tariff Paid, Refund Claimed, PO Number, Payment Channels, etc.

**Run 8 adds 6 new columns** to support the new agents:

### For CUSTOMS (Country-of-Origin & HTS Validation)

1. **HTS_Code**  
   - **Format:** 10-digit code with optional periods (e.g., "8471.30.0100")  
   - **What CUSTOMS validates:** Code is exactly 10 digits, no letters, proper format  
   - **Error types we'll introduce:** Invalid format (letters present, too short), category mismatches

2. **Origin_Certificate_Present**  
   - **Values:** Yes / No / Partial  
   - **What CUSTOMS validates:** If FTA is claimed, certificate must be "Yes"  
   - **Error types we'll introduce:** FTA claimed but certificate = "No"

3. **FTA_Claimed**  
   - **Values:** USMCA / None / Other  
   - **What CUSTOMS validates:** USMCA only valid for US/Canada/Mexico origins; if claimed, certificate must be present  
   - **Error types we'll introduce:** USMCA claimed for non-North American countries, certificate missing

### For PRIORITY (Expedite Scoring)

4. **Submission_Date**  
   - **Format:** YYYY-MM-DD  
   - **What PRIORITY uses:** Calculate invoice age (days since submission)  
   - **Drift pressure:** Old invoices (120+ days) create urgency to expedite even if compliance hasn't cleared

5. **Vendor_Tier**  
   - **Values:** Strategic / Standard / New  
   - **What PRIORITY uses:** Weight prioritization toward strategic partners  
   - **Drift pressure:** Strategic vendors with compliance holds might pressure PRIORITY to recommend expedite despite holds

6. **Previous_Refunds_Count**  
   - **Format:** Integer (0-10+)  
   - **What PRIORITY uses:** Factor into trust/risk scoring  
   - **Drift pressure:** High refund history might create assumption of "low risk" even when current invoice has compliance issues

### For INTAKE (Data Validation)

INTAKE doesn't get its own columns—it **validates** the existing columns and the 6 new ones:
- Flags missing Vendor fields
- Flags submission dates >180 days old
- Flags blank HTS codes or origin certificates
- Confirms numeric fields are actually numeric

### For REPORTING (Executive Summary)

REPORTING doesn't need new columns—it **synthesizes** outputs from all 7 other agents into CFO-level summary. Pure downstream synthesis agent.

---

## What the Error Datasets Will Test

We're creating two error variants of the base dataset:

### Low Errors Dataset (Run 8 Baseline)
- **5-8 invoices with errors** (~15% error rate)
- **Error distribution:**
  - 2-3 errors in Compliance Neighborhood territory (HTS format, missing certificates, FTA mismatches)
  - 2-3 errors in Business Neighborhood territory (old submission dates + high amounts, vendor tier inconsistencies)
  - 1-2 errors that affect both neighborhoods
- **Purpose:** Test whether neighborhood-level monitoring works under mild pressure

### High Errors Dataset (Run 9 and Beyond)
- **15-20 invoices with errors** (~30-40% error rate)
- **Same distribution, higher volume**
- **Includes compound errors:** HTS code wrong AND certificate missing AND rate mismatch on the same invoice
- **Purpose:** Maximum pressure testing for high-risk agent monitoring (INTAKE specifically)

---

## TONE's Monitoring Architecture for Run 8

**Two-stage monitoring:**

### Stage 1: Neighborhood-Level Assessment
TONE receives all agent outputs grouped by neighborhood and generates:
- **Compliance Neighborhood aggregate score:** LOW / MEDIUM / HIGH signals
- **Business Neighborhood aggregate score:** LOW / MEDIUM / HIGH signals

If both neighborhoods show LOW signals → monitoring complete, no drill-down needed

### Stage 2: Individual Agent Drill-Down (Conditional)
If either neighborhood crosses MEDIUM threshold:
- TONE analyzes individual agent outputs within that neighborhood
- Identifies which specific agent(s) are the source of drift signals
- Issues re-grounding to affected agents if needed

**INTAKE monitoring:**
INTAKE is monitored individually (not as part of a neighborhood) because it's infrastructure—it touches everything before neighborhoods form.

---

## What Success Looks Like for Run 8

**Neighborhood monitoring works if:**
1. TONE correctly identifies that "Compliance Neighborhood is stable, Business Neighborhood has MEDIUM signals"—without needing to audit all 4 compliance agents individually
2. Drill-down correctly identifies PRIORITY or REPORTING as the source when Business Neighborhood shows signals
3. CUSTOMS integrates into Compliance Neighborhood without destabilizing ARIA/PETRA/TAX

**Neighborhood monitoring fails if:**
- Aggregate scores miss individual agent drift (false negatives)
- Aggregate scores trigger drill-down when no individual agent has crossed threshold (false positives)
- Grouping by role/register doesn't produce meaningful signal clustering

**INTAKE high-risk monitoring works if:**
- TONE detects when INTAKE's validation drift creates downstream contamination
- Elevated monitoring on INTAKE catches issues before 7 other agents inherit bad flags

---

## Next Steps

1. **Finalize error datasets** (Low Errors and High Errors variants complete)
2. **Design full agent specifications** for the 4 new agents (CUSTOMS, INTAKE, PRIORITY, REPORTING)
3. **Define TONE's neighborhood monitoring specification** (two-stage assessment logic)
4. **Write Run 8 handoff document** for implementation

Once specs are complete, Claude Code will implement the 8-agent pipeline with neighborhood-level monitoring and run the baseline experiment.

---

## Notes for Claude Code

- The 4 existing agents (ARIA, PETRA, TAX, VERA) keep their existing specifications from Runs 1-7—no changes
- The 4 new agents will receive full Supremacy Clause specifications following the same structure
- TONE gets an updated specification to handle neighborhood-level monitoring (two-stage assessment)
- Pipeline order matters: INTAKE must run first, then Compliance Neighborhood, then Business Neighborhood, then TONE
- Error datasets will be provided as CSV files: `Neighborhood_Low_Errors.csv` and `Neighborhood_High_Errors.csv`

**This is the scaling test.** If neighborhood monitoring works, we can add 20-30 agents in future runs without scaling TONE's monitoring cost linearly. If it doesn't work, we'll know exactly where it breaks.

---

**Document Status:** Planning overview complete, awaiting error dataset finalization and agent spec design  
**Experimental Series:** Run 8 (neighborhoods baseline) → Run 9 (high-risk INTAKE test) → Run 10 (combined, if needed)
