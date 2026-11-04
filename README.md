# Research Paper Reading

**I read research papers so the ideas in them don't stay locked away.** Each note takes one paper, asks it one question, checks its numbers against the source, and puts the answer in plain words that anyone can follow.

<!-- BEGIN:stats -->
| Papers read | Fields | Claims corrected against the source |
|:---:|:---:|:---:|
| **1** | **1** | **5** |
<!-- END:stats -->

## Start here

New to research papers? Open the latest note and read section 5, the two-sentence summary. If it makes you curious, read the rest.

<!-- BEGIN:latest -->
**[Agents' Last Exam](papers/2026-11-04_Agents-Last-Exam.md)** (AI agents, read 2026-11-04)

> The best AI setups finish only about a quarter of real multi-hour office jobs once a strict script checks the result.
<!-- END:latest -->

## Why read papers at all

Research papers are where new ideas show up first, often years before they reach a product or a headline. Most people never open them because they look impenetrable. They don't have to be.

You don't read a paper front to back. You ask it one question, study its main figure, and say its idea in your own words. Half an hour is enough to come away with something real.

Here's an example. In June 2026, a Berkeley-led team gave the best AI agents more than a thousand real professional tasks, the kind that take people hours or days. The top setup finished about a quarter of them. Product announcements won't tell you that. Papers will.

## Reading log

Every paper I've read, newest first.

<!-- BEGIN:log -->
| Read | Paper | Field | The idea in one line | Status |
|---|---|---|---|---|
| 2026-11-04 | [Agents' Last Exam](papers/2026-11-04_Agents-Last-Exam.md) | AI agents | The best AI setups finish only about a quarter of real multi-hour office jobs once a strict script checks the result. | Done |
<!-- END:log -->

## Threads

The questions I keep pulling on. Each one gathers the papers that answer part of it, so ideas from different fields end up side by side.

<!-- BEGIN:threads -->
- **How do you know an automation actually worked?**  
  1 paper: [Agents' Last Exam](papers/2026-11-04_Agents-Last-Exam.md)
- **Where should a person stay in the loop?**  
  1 paper: [Agents' Last Exam](papers/2026-11-04_Agents-Last-Exam.md)
<!-- END:threads -->

## How I read a paper

Two phases, about half an hour in all. The full method is in [METHOD.md](METHOD.md), and it improves with every paper: see its changelog.

```
PHASE 1  READ  (13 min)                     PHASE 2  VERIFY AND STEAL  (15 min)

1  Find it through a lab, not a search      6  Study the visuals, check every number
2  Write down the one question I'm asking   7  Open two real examples
3  Read the abstract, "Here we show"        8  Test the idea on my own work
   and the figure captions                  
4  Swap each jargon word for a toy example     Done: archive it, move on
5  Explain it in two plain sentences
```

Two rules hold for every note:

- **Plain words.** The summary can't use any word from the paper's title, so I have to understand the idea instead of repeating it.
- **Numbers come from the source.** Press releases and summaries often get figures wrong. Every number in a note is checked against the paper's own tables, and each note lists what it corrected.

## What's in this repository

```
README.md            this page, rebuilt automatically on every commit
METHOD.md            how I read a paper, step by step
papers/              one note per paper, named YYYY-MM-DD_Short-Title.md
templates/           the blank note every paper starts from
scripts/             the script that rebuilds this page from the notes
.githooks/           checks that run before anything is published
```

The tables on this page are generated from the header at the top of each note, so they're always up to date.
