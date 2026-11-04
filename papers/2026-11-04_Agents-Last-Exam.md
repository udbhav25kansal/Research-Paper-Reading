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

Read in the PDF. The HTML version draws some figures over the text.

- Figure 6, how a task runs: each task runs on its own virtual computer set up with the files and software the job needs. The AI gets only the written instructions, works through the task by clicking, typing and running commands, and when it's done, a script scores what it produced against an expert's reference answer or a marking rubric.
- Figure 8, how the AI works: in a loop. It gathers what it knows so far, asks the language model what to do next, picks an action and carries it out with its tools (the terminal, files and, through a connector, the screen's mouse and keyboard), then looks at the result and goes round again until it decides the job is done.
- Figure 13, cost: each bubble is one setup, plotted as score against total cost and against time. Top-left means more done for less.

Table 1, pass rates in %, on 160 tasks (67 Near-Term, 55 Full-Spectrum, 38 Last-Exam). Per-task cost is the three tier totals divided by 160.

| Setup | Overall pass | Near-Term | Full-Spectrum | Last-Exam | Total cost | Per task |
|---|---|---|---|---|---|---|
| Codex, GPT-5.5 | 24.0 | 38.1 | 22.7 | 0.0 | $570 | ~$3.56 |
| ALE-Claw, GPT-5.5 | 23.0 | 32.8 | 23.6 | 2.6 | $326 | ~$2.04 |
| Claude Code, Fable 5 | 22.0 | 34.3 | 20.9 | 0.0 | $2,402 | ~$15.01 |
| OpenClaw, GPT-5.5 | 21.1 | 35.8 | 18.2 | 0.0 | $477 | ~$2.98 |
| Cursor, GPT-5.5 | 20.7 | 32.1 | 20.0 | 2.6 | $180 | ~$1.12 |
| Cursor, Composer 2.5 | 20.4 | 34.3 | 18.2 | 0.0 | $87 | ~$0.54 |
| Cursor, Opus 4.7 | 20.4 | 29.9 | 20.0 | 2.6 | $2,012 | ~$12.57 |
| Droid, GPT-5.5 | 19.1 | 29.9 | 16.4 | 2.6 | $251 | ~$1.57 |

What the table says:

1. Almost nothing passes the hardest tier. Four setups score 2.6%, which is one task out of 38. Everyone else scores 0.
2. Spending more doesn't buy a higher score. The best setup (Codex, GPT-5.5) costs about $3.60 a task. Claude Code with Fable 5 costs about $15 a task and scores lower.
3. The wrapper matters as much as the model. With GPT-5.5 fixed, changing only the tool around it moves the overall score from 24.0 to 19.1.
4. The headline says 1,500 tasks, but these results cover 160.

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

## Sources

Read and relied on:

1. The paper, arXiv 2606.05405, version 4 (25 Oct 2026): https://arxiv.org/abs/2606.05405 (PDF https://arxiv.org/pdf/2606.05405, HTML https://arxiv.org/html/2606.05405). Abstract, Introduction, Sections 3.1, 3.2 and 4.1, Table 1, captions for Figures 6, 8 and 13.
2. Berkeley RDI blog post, June 2026: https://rdi.berkeley.edu/blog/agents-last-exam/. Punchline, cost per task, the 0% and 1,500+ task claims.
3. ALE demo page: https://agents-last-exam.org/demo. Step 7 examples.

Seen but not relied on:

4. An AI-written summary I started from. Several of its numbers were wrong (see Fact check).
5. Hugging Face paper page, https://huggingface.co/papers/2606.05405, and news write-ups found by search. One gave conflicting pass rates.

Linked from the blog, not opened yet: the leaderboard (https://agents-last-exam.org/leaderboard), the dataset (https://huggingface.co/datasets/agents-last-exam/agents-last-exam) and the code (https://github.com/rdi-berkeley/agents-last-exam).

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
- The blog says the agents were tested on more than 1,500 tasks. The results table covers 160 of them.
- The paper says one task costs "$3 to 10 on average" (section 4.1). From Table 1, Claude Code with Fable 5 costs about $15 a task, close to the blog's $15.70 and well above that range.
