---
title: Agents' Last Exam
authors: Yiyou Sun and 378 others, led by UC Berkeley RDI
published: 2026-06-03
source: https://arxiv.org/abs/2606.05405
project: https://agents-last-exam.org
field: AI agents
date_read: 2026-11-04
status: Verifying
one_line: The best AI setups finish only about a quarter of real multi-hour office jobs once a strict script checks the result.
corrections: 5
threads:
  - How do you know an automation actually worked?
  - Where should a person stay in the loop?
---

# Agents' Last Exam

## 1. Press summary punchline

Top coding agents look superhuman on coding benchmarks: Codex with GPT-5.5 scores 82% on Terminal-Bench. On 1,490 real professional tasks that take people hours or days, the best setup passes 24.0%, and almost nothing passes the hardest tier. Real jobs mix terminal work with clicking through desktop apps over hours, and the agents lose the thread.

## 2. My one question

Why do agents that pass coding tests fail on real multi-hour business workflows, and how do I wire an agent and a verification check so it actually finishes the job?

## 3. Bypass notes

- Abstract: a benchmark of long, economically valuable, real-world tasks with verifiable outcomes. 1K+ tasks in 55 subfields grouped into 13 industry clusters, built with 250+ industry experts. On the hardest tier the average full pass rate is below 1%.
- How a task is built (Section 3.1): three parts.
  1. The task spec, a `main.py` with `load()`, `start()` and `evaluate()`. `evaluate()` scores the final output from 0 to 1 and ignores how the agent got there.
  2. The agent, a harness (such as Codex, Claude Code or OpenClaw) driving a model.
  3. The environment, a remote Linux or Windows VM with `input/`, `software/`, `output/` (the only writable folder) and a hidden `reference/`.
- Grading avoids an LLM judge wherever a deterministic check exists. The usual pattern is gate and score: fail the gate check and the score is 0.
- The bridge (Section 4.1): a unified computer-use MCP bridge exposes 14 desktop-action tools, so a terminal agent can take screenshots and click as ordinary tool calls.

## 4. Jargon to toy example

| Term in the paper | Concrete toy example |
|---|---|
| Computer-use MCP bridge | Giving a terminal bot eyes (screenshots) and a mouse (clicks) as normal tools, so it can write a Python script and then click Export in an old desktop app that has no API. |
| Outcome-based, verifiable evaluation | Instead of asking another model "does this look right?", a script opens the final spreadsheet and checks that cell B14 equals 420.50. |
| Long-horizon failure | After 45 minutes and 80 tool calls the bot has forgotten a rule from step 2, loops on a small bug, and runs out the clock. |

## 5. Zero-jargon summary

People assumed AI coding bots were ready to take over real office work because they ace short, text-only programming puzzles. This study shows that hours-long jobs need the bot to switch between writing code and clicking through desktop software, and that even the best setup only finishes about a quarter of them when a strict script checks the final file.

## 6. Visuals

- Architecture: task spec, harness and VM are separate pieces, so any harness can be tested on any task. GUI apps reach the harness through the MCP bridge.
- Cost versus performance: not checked yet.
- Results by tier, full benchmark (Table 1):

| Setup | Overall | Near-Term | Full-Spectrum | Last-Exam |
|---|---|---|---|---|
| Codex, GPT-5.5 | 24.0 | 38.1 | 22.7 | 0.0 |
| ALE-Claw, GPT-5.5 | 23.0 | | | 2.6 |
| Claude Code, Fable 5 | 22.0 | | | 0.0 |
| OpenClaw, GPT-5.5 | 21.1 | | | |

  The best score on the hardest tier is 2.6%. Most setups score 0.
- Terminal-only subset (ALE-CLI, 105 Linux tasks): Codex with GPT-5.5 gets 23.3% overall (37.2 / 19.0 / 0.0), against its 82% on Terminal-Bench.

## 7. Two real examples

Not done yet. Open two tasks on https://agents-last-exam.org (one operations workflow, one engineering workflow) and read the prompt, the input files and the `evaluate()` script.

## 8. One-workflow audit

| Pattern from the paper | Question about my automation | Answer |
|---|---|---|
| CLI and GUI split | Am I making something click through a screen when an API or script could do 90% of it? Is my script breaking on the 10% that needs a screen? | |
| Short checked stages | Does the workflow run more than 10 to 15 steps without a checkpoint? Where can I split it into smaller stages I can verify? | |
| Deterministic `evaluate()` | Can I write a 20-line script today that checks the output file or database, with no model judging it? | |

What I can steal:

1. Use code and APIs for most of the work and keep screen clicking for the legacy software that has no API.
2. Break long processes into short stages with a check after each. The 10 to 15 minute limit is my own rule of thumb, not a number from the paper.
3. Write the `evaluate()` check before building the automation: the file exists, the schema matches, the totals reconcile.

## Fact check

Checked against arXiv v4 on 2026-11-04. The summary I started from got these wrong:

- Best overall pass rate is 24.0% (Codex, GPT-5.5), not 25.2%.
- 1,490 is task instances (from 960 workflows), across 55 subfields in 13 clusters.
- "Under 10% on the hardest tier" is the intro's wording. The table gives Codex 0.0% pass there, and the best is 2.6%.
- The 37.2 / 19.0 tier numbers are from the terminal-only subset, not the full benchmark.
- No SWE-bench-Pro score (59.1%) appears in the paper.
- Not yet checked: the $15.70 versus $1.33 to $3.80 per-task cost figures, the RDI blog post and the demo page.
