"""
logger.py — Output File Writing Utilities
==========================================
This file handles:
  - Creating the results folder structure
  - Writing each agent's output to a text file
  - Writing TONE's observation log
  - Writing a run summary
"""

import os
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# FOLDER SETUP
# ─────────────────────────────────────────────────────────────────────────────

def create_run_folder(run_name: str) -> Path:
    """
    Create and return the output folder for a single experiment run.
    Example: results/run_1_no_supremacy_gentle/
    """
    folder = Path("results") / run_name
    folder.mkdir(parents=True, exist_ok=True)
    return folder


# ─────────────────────────────────────────────────────────────────────────────
# AGENT OUTPUT FILES
# ─────────────────────────────────────────────────────────────────────────────

def write_agent_output(folder: Path, agent_name: str, output: str,
                       run_description: str, dataset_name: str) -> None:
    """
    Write a single agent's output to a text file.

    File name example: aria_output.txt
    """
    filename = folder / f"{agent_name.lower()}_output.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    header = (
        f"{'=' * 60}\n"
        f"AGENT: {agent_name}\n"
        f"RUN:   {run_description}\n"
        f"DATA:  {dataset_name}\n"
        f"TIME:  {timestamp}\n"
        f"{'=' * 60}\n\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(output)
        f.write("\n")

    print(f"      Saved: {filename}")


# ─────────────────────────────────────────────────────────────────────────────
# TONE LOG FILE
# ─────────────────────────────────────────────────────────────────────────────

def write_tone_log(folder: Path, tone_output: str,
                   run_description: str, dataset_name: str) -> None:
    """
    Write TONE's observation log to a clearly labeled file.

    TONE's log is kept separate from the other agent outputs
    because it is the primary audit trail for drift detection.
    """
    filename = folder / "tone_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    header = (
        f"{'=' * 60}\n"
        f"TONE OBSERVATION LOG\n"
        f"{'=' * 60}\n"
        f"RUN:   {run_description}\n"
        f"DATA:  {dataset_name}\n"
        f"TIME:  {timestamp}\n"
        f"NOTE:  TONE observed agent outputs only. TONE did not\n"
        f"       receive invoice data. This log is the drift audit trail.\n"
        f"{'=' * 60}\n\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(tone_output)
        f.write("\n")

    print(f"      Saved: {filename}")


# ─────────────────────────────────────────────────────────────────────────────
# RE-GROUNDING OUTPUT FILE (Run 6 only)
# ─────────────────────────────────────────────────────────────────────────────

def write_regrounding_output(folder: Path, after_agent: str, output: str,
                             run_description: str) -> None:
    """
    Write one of VERA's re-grounding responses to a clearly labeled file.

    Called three times in Run 6:
      after_agent = "ARIA"   → vera_regrounding_after_aria.txt
      after_agent = "PETRA"  → vera_regrounding_after_petra.txt
      after_agent = "TAX"    → vera_regrounding_after_tax.txt

    These files are part of the audit trail and will be read by the
    project owner to assess whether re-grounding corrected VERA's drift.
    """
    filename = folder / f"vera_regrounding_after_{after_agent.lower()}.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    header = (
        f"{'=' * 60}\n"
        f"VERA RE-GROUNDING RESPONSE\n"
        f"{'=' * 60}\n"
        f"Triggered by: {after_agent} compliance output\n"
        f"Run:          {run_description}\n"
        f"Time:         {timestamp}\n"
        f"Note:         This is VERA's response to a Level 2 re-grounding\n"
        f"              prompt issued by TONE after {after_agent} completed.\n"
        f"{'=' * 60}\n\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(output)
        f.write("\n")

    print(f"      Saved: {filename}")


# ─────────────────────────────────────────────────────────────────────────────
# RUN SUMMARY FILE
# ─────────────────────────────────────────────────────────────────────────────

def write_run_summary(folder: Path, run_description: str, dataset_name: str,
                      supremacy_active: bool, agent_names: list,
                      errors: list) -> None:
    """
    Write a brief summary file for the run — useful for quick review.
    """
    filename = folder / "run_summary.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    supremacy_status = "ACTIVE (Runs 3 & 4)" if supremacy_active else "REMOVED (Runs 1 & 2)"

    summary = (
        f"{'=' * 60}\n"
        f"RUN SUMMARY\n"
        f"{'=' * 60}\n"
        f"Run:              {run_description}\n"
        f"Dataset:          {dataset_name}\n"
        f"Supremacy Clause: {supremacy_status}\n"
        f"Completed:        {timestamp}\n"
        f"{'=' * 60}\n\n"
        f"AGENTS RUN:\n"
    )

    for name in agent_names:
        summary += f"  ✓ {name}\n"

    if errors:
        summary += f"\nERRORS ENCOUNTERED:\n"
        for err in errors:
            summary += f"  ✗ {err}\n"
    else:
        summary += f"\nNo errors encountered.\n"

    summary += (
        f"\nOUTPUT FILES:\n"
        f"  aria_output.txt    — ARIA's invoice review\n"
        f"  petra_output.txt   — PETRA's payment compliance review\n"
        f"  tax_output.txt     — TAX's regulatory review\n"
        f"  vera_output.txt    — VERA's business recovery response\n"
        f"  tone_log.txt       — TONE's drift observation log (primary audit trail)\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"      Saved: {filename}")
