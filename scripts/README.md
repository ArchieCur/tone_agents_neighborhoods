# Scripts

## Inheritance Chain

The scripts for Runs 8–13 form an inheritance chain. Understanding this chain is important for reading the code and for replicating experiments.

```
agents.py (Runs 1-7, prior series)
    └── agents_8.py (Runs 8-10)
            └── agents_11.py (Runs 11-12)
                    └── agents_13.py (Run 13)
```

```
run_experiment.py (Runs 1-4, prior series)
run_experiments_5_6.py (Runs 5-6, prior series)
run_experiment_7.py (Run 7, prior series)
    └── run_experiment_8.py (Run 8)
    └── run_experiment_9.py (Run 9)
    └── run_experiment_10.py (Run 10)
            └── run_experiment_11.py (Runs 11 — three extreme datasets)
                    └── run_experiment_12.py (Run 12 — two data_8 datasets)
                            └── run_experiment_13.py (Run 13 — Neighborhood-Low only)
```

## What Changed at Each Level

### agents_8.py
- 8 full agent specs: ARIA, PETRA, TAX, CUSTOMS (new), INTAKE (new), VERA, PRIORITY (new), REPORTING (new)
- All agents use full double Supremacy Clause (NON-NEGOTIABLE language)
- TONE: two-stage neighborhood monitoring (Stage 1 aggregate, Stage 2 conditional drill-down)
- VERA context line: 3 compliance agents (ARIA, PETRA, TAX)

### agents_11.py
- Imports ARIA, PETRA, TAX, CUSTOMS, INTAKE, PRIORITY, REPORTING unchanged from agents_8.py
- VERA_PROMPT_RUN11: softened Supremacy Clause (NON-NEGOTIABLE language removed, named prohibitions retained)
- VERA context line: 4 compliance agents (ARIA, PETRA, TAX, CUSTOMS) — documented difference from Run 8
- TONE_VERA_MINI_PROMPT: new two-tier mini-assessment with structured summary block for parser
- TONE_FULL_PROMPT_RUN11: updated full assessment with Tier 1/Tier 2 signal taxonomy (T1-A through T2-E)
- Adds "NOTE ON RUN 11" priming block informing TONE of softened clause before assessment

### agents_13.py
- Imports all agents from agents_11.py except VERA and TONE full assessment
- VERA_PROMPT_RUN13: three surgical corrections to VERA_PROMPT_RUN11:
  1. SHOULD section moved back to after first Supremacy Clause (restores Run 8 sandwich structure)
  2. VERIFICATION header restored: "Before delivering output, confirm:"
  3. Softened clause text unchanged — identical to Runs 11 and 12
- TONE_FULL_PROMPT_RUN13: "NOTE ON RUN 11" priming block removed
- Documents 5 unintended wording differences in the Run 13 handoff prompt that were NOT applied

## Pipeline Architecture (run_experiment_11.py onward)

```python
# Stage 1: Compliance neighborhood
intake_output = call_agent(INTAKE_PROMPT, data)
aria_output = call_agent(get_aria_prompt(), data + intake_output)
petra_output = call_agent(get_petra_prompt(), data + intake_output + aria_output)
tax_output = call_agent(get_tax_prompt(), data + intake_output + aria_output + petra_output)
customs_output = call_agent(CUSTOMS_PROMPT, data + ... + tax_output)

# Stage 2: VERA assessed before Business Neighborhood
vera_output = call_agent(VERA_PROMPT, compliance_outputs)
tone_mini = call_agent(TONE_VERA_MINI_PROMPT, vera_output)
intervention_level = _parse_tone_mini(tone_mini)

# Escalation ladder (Levels 1-4)
if intervention_level >= 2:  # re-ground
    ...
if intervention_level >= 3:  # prune
    ...
if intervention_level == 4:  # halt
    # PRIORITY and REPORTING do not run
    return

# Stage 3: Business neighborhood (only if not halted)
priority_output = call_agent(PRIORITY_PROMPT, all_outputs)
reporting_output = call_agent(REPORTING_PROMPT, all_outputs)

# Stage 4: TONE final full assessment
tone_full = call_agent(TONE_FULL_PROMPT, all_outputs)
```

## Parser Note

`run_experiment_11.py` includes `_parse_tone_mini()` — a regex parser that extracts the escalation level from TONE's mini-assessment summary block. The parser uses a name-boundary truncation to prevent false positives from the CUSTOMS/VERA scan window overlap (a bug fixed from run_experiment_9.py). The structured summary block in `TONE_VERA_MINI_PROMPT` provides a reliable parse target.

## Environment

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
```

Tested on Python 3.14. All scripts use the Anthropic Python SDK with `claude-sonnet-4-6` model.
