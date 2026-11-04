# How we read a paper: Feynman-to-Frontier

About 13 minutes for phase 1, then 15 minutes for phase 2.

```
Source from elite lab feeds
  -> Read the press summary first
  -> Decode Figure 1 only
  -> Replace jargon with toy examples (Feynman trick)
  -> Extract the one-sentence mechanism
```

## 1. Source via lab-first filtering (2 minutes)

Never search raw databases. Skip PubMed and Google Scholar and go straight to curated hubs:

- MIT Picower Institute and McGovern Institute news
- Harvard Brain Science Initiative (HBI)
- Cosyne (Computational and Systems Neuroscience) top papers
- Nature Neuroscience "News & Views"

Pick a paper only after reading its two-paragraph university press release. That gives you the punchline before you face the jargon. If the post is long, read only its opening paragraphs; the charts and comparisons wait for step 6.

The punchline is the main finding, said plainly. It has two halves:

```
What people believed   ->   what this study actually found
```

It commits to the result. "We tested how good they really are" is not a punchline. "They're useful on easy tasks but fail on the hardest" is.

**Step 1 passes when** you can say the punchline in one sentence of your own and you've decided the paper is worth the next 25 minutes.

## 2. Set your mercenary intent (30 seconds, before opening the PDF)

Don't read a paper outside your field to learn the whole paper. Write down one question you're trying to steal an answer for, for example "How does the visual cortex compress data compared to a camera?" or "What is the core input-to-output rule here?". Ignore every paragraph that doesn't answer it.

Check that this kind of paper can answer your question. A benchmark or exam paper tells you where things break and how success is measured, not how to build the thing. **Step 2 passes when** the question is specific, is tied to something you'd do with the answer, and is one this paper can answer.

## 3. Run the Figure 1 and last-paragraph bypass (3 minutes)

In Nature, Science and Cell papers, Figure 1 is usually the conceptual architecture of the discovery, and the last paragraph of the Introduction ("Here we show...") states the breakthrough. Read only:

- the Abstract
- that one Introduction paragraph
- the figure captions

Skip the Methods and Results text completely.

"Here we show" is a role, not a phrase to search for. Many papers never use those words. Look for the paragraph that says what the paper introduces and the sentence that states what it found, usually in the last two or three paragraphs of the Introduction.

**Step 3 passes when** you can answer your step 2 question in one line per part, or say which part these three pieces don't answer.

## 4. Apply the concrete cat translation (5 minutes)

When Feynman read biology papers at Caltech and hit an abstract term like "retrograde cortical feedback modulation", he stopped and forced a concrete toy example: "Neuron A sends a slow-down signal back to Neuron B when the eye moves". When you hit a word you don't know, swap it for a simple mechanical action: input X triggers switch Y.

## 5. Zero-jargon output test (2 minutes)

Close the PDF and write a two-sentence summary that uses no words from the paper's title.

- Sentence 1, the old bottleneck: "Scientists used to think the brain did X..."
- Sentence 2, the new mechanism: "...but this experiment shows it actually works like [simple mechanical system] by doing Y."

If you get stuck on part of a sentence, go back to the paper only to fill that one gap.

# Phase 2: Verify and steal (15 minutes)

Don't read the paper cover to cover. Phase 1 already got most of the conceptual value. Phase 2 turns it into something usable at work.

```
Look at three visuals (3 min)
  -> Click through two real examples (5 min)
  -> Audit one of my own workflows against the pattern (7 min)
  -> Done: archive it
```

## 6. Look at the visuals, not the text (3 minutes)

Open the HTML version on arXiv or the lab's blog post and look at three things only:

- the architecture diagram, traced end to end
- any cost versus performance chart
- the main results table, read by difficulty tier

Before a number goes into a note, check it against the paper's own table. Press releases, summaries and AI write-ups get numbers wrong or mix up tables.

## 7. Click through two real examples (5 minutes)

If the paper has a demo, a dataset viewer or released code, open two real examples instead of reading descriptions of them. Pick one close to my work and one outside it. Look at the input, the messy material the system is handed, and how success is checked.

## 8. Run a one-workflow audit on my own job (7 minutes)

Close the tabs. Take one automation I'm building now and ask three questions the paper's core pattern raises. Write the answers down.

## Done when

The visuals are read, two examples are inspected and one of my workflows is mapped to the pattern. Archive the paper and move on.

# Filing a note

1. Copy `templates/paper-note.md` to `papers/YYYY-MM-DD_Short-Title.md`.
2. Fill in the header first: field, status, the one-line idea, and the threads it feeds. Reuse the exact wording of an existing field or thread so papers group together.
3. Move the status from Reading to Verifying to Done as the phases finish.
4. Commit. The README rebuilds itself from the headers.

# How this method changes

The method improves with every paper. Each step of each paper ends by noting what it taught, and the change lands here.

| Date | Change | Learned from |
|---|---|---|
| 2026-11-04 | Step 1: read only the opening of a long post, define the punchline as belief versus finding, add a pass test | Agents' Last Exam, step 1 |
| 2026-11-04 | Step 2: check that the paper's type can answer the question, add a pass test | Agents' Last Exam, step 2 |
| 2026-11-04 | Step 3: "Here we show" is a role, not a literal phrase; find the paragraph that states the contribution and the finding | Agents' Last Exam, step 3 |
| 2026-11-04 | Step 3: add a pass test, answering the step 2 question in one line per part | Agents' Last Exam, step 3 |
