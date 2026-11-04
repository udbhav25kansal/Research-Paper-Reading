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
corrections: 4
threads:
  - How do you know an automation actually worked?
  - Where should a person stay in the loop?
---

# Agents' Last Exam

## 1. Press summary punchline

People think AI agents are about to be job-ready. This study shows they're useful on easier tasks but fail completely on the hardest real ones.

Source: the Berkeley RDI blog post, https://rdi.berkeley.edu/blog/agents-last-exam/ (June 2026). Its own line: "The age of useful agents is here. The age of truly job-ready agents is not."

## 2. My one question

Where do agents break on real jobs, and how do I check that mine actually finished?

## 3. Bypass notes

My answers to my question:

1. Where they break: on long, real jobs that mix command-line and on-screen work, and they get worse as the jobs get harder.
2. How finishing is checked: graded against expert references and rubrics, either on the final deliverable or at milestones along the way, mostly by automatic scripts rather than a human or AI judge.

Notes:

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
| Generalist Computer-Use Agent (GCUA) | A robot intern sitting at your computer. Give it any errand (your taxes, a meeting, a flight to Paris) and it does what you would: types commands in the terminal, opens booking.com, scrolls, clicks Book. One intern, any errand. |
| Long-horizon task | Doing your taxes, not typing one number. Read the rules, pick the deductions, find the right form, fill it in, answer the accountant's email. Forty steps over an afternoon, and the deduction chosen at step 1 still has to be there at step 40. That's where agents drop the ball. |
| Milestone-based check | A checkpoint that inspects a result on the way, not an action. Before paying for the Paris ticket: is the flight in the basket the 12 March one? If not, stop there instead of waiting for the receipt. "Did it open the website?" is an action; "is the right flight in the basket?" is a milestone. |
| Verifiable outcome | A yes-or-no question about the final result that a script can settle without opinion. "Is the booked ticket the cheapest one on that site for 12 March?" Compare it with the cheapest fare an expert found: same price, pass. Not "does the booking look right?" |

Earlier toy examples from the AI summary I started with, kept because they're still useful:

| Term | Toy example |
|---|---|
| Computer-use MCP bridge | Giving a terminal bot eyes (screenshots) and a mouse (clicks) as normal tools, so it can write a script and then click Export in an old desktop app that has no API. |

## 5. Zero-jargon summary

People assumed AI bots that ace coding tests were ready to take over whole jobs. This study shows they're like a bright intern who handles short errands well but loses the thread on a long project: on real work that mixes typing and clicking for hours, they almost never pass the hardest jobs once an automatic check compares the result with an expert's.

## 6. Visuals

- Architecture: task spec, harness and VM are separate pieces, so any harness can be tested on any task. GUI apps reach the harness through the MCP bridge.
- Cost versus performance: per the blog, Fable 5 about $15.70 per task, GPT-5.5 about $3.80, Composer 2.5 about $1.33, for similar performance.
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

Checked on 2026-11-04 against the paper (arXiv v4) and the RDI blog post.

The AI summary I started from got these wrong:

- It gave 25.2% as the best overall pass rate on all tasks. The blog's 25.2% is for the terminal-only subset (ALE-CLI). On the full benchmark the best is 24.0% (Codex, GPT-5.5).
- It called 1,490 "workflows across 55 domains". The paper has 960 workflows, split into 1,490 task instances, across 55 subfields in 13 clusters.
- "Under 10% on the hardest tier" is the intro's wording. The table gives Codex 0.0% there, and the best of any setup is 2.6%.
- It presented 37.2% and 19.0% as full-benchmark tier scores. They're from the terminal-only subset.

The blog and the paper also differ from each other:

- The blog (June) says the best agent passes 25.2% on ALE-CLI. The paper (v4, October) gives Codex with GPT-5.5 23.3% there.
- The 59.1% on SWE-bench-Pro and the cost figures (Fable 5 about $15.70, GPT-5.5 about $3.80, Composer 2.5 about $1.33 per task) are in the blog, not the paper text I checked.
- The blog says every agent scored 0% on the hardest tier. The paper's table shows four setups at 2.6%, with the average below 1%.
