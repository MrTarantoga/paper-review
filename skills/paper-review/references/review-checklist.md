# Structural Review Checklists

Pick the checklist for the document type. Not every item applies to every text —
judge by the venue, length and purpose. Report concrete gaps, not a ticked list.

## Contents
1. Exposé / research proposal
2. Research paper (conference/journal)
3. Abstract
4. Thesis chapter
5. Cross-cutting checks (all types)

---

## 1. Exposé / research proposal

An exposé convinces a supervisor or committee that the project is worthwhile,
well-defined and feasible.

- **Title** — specific; reflects the actual research question, not just the topic.
- **Motivation / problem statement** — why does this matter, for whom? Is the
  problem concrete, or only a general field description?
- **State of the art** — key related work covered; is it synthesised (grouped,
  compared) rather than listed paper by paper? Is it current?
- **Research gap** — explicitly stated; follows logically from the state of the art.
  The most common weakness: the gap is implied but never stated in one clear sentence.
- **Research question(s) / hypotheses** — explicit, answerable, appropriately scoped
  for the time frame. Sub-questions map to the methodology.
- **Objectives & expected contributions** — what concretely will exist at the end
  (method, model, dataset, evaluation, tool)? Distinguish from the question itself.
- **Methodology** — concrete enough that a reader could judge feasibility: data
  sources, models/approaches, baselines, evaluation metrics, validation strategy.
  Every research question should have a corresponding method.
- **Data & resources** — availability, access, size, licensing, compute.
- **Evaluation plan** — how will success be measured; what are the baselines;
  what would count as a negative result?
- **Work plan / timeline** — phases with realistic durations; milestones; buffer.
- **Risks & limitations** — what could go wrong, with mitigation.
- **Expected results / outlook** — cautious and consistent with the methodology.
- **References** — consistent style; key works present; no dangling citations.
- **Figures** — referenced in text, captions self-explanatory, readable.

## 2. Research paper

- **Title & abstract** — abstract states problem, approach, main result
  (ideally quantitative), and significance, in that order.
- **Introduction** — context → problem → gap → contribution; contributions listed
  explicitly (often as bullet points); paper structure at the end.
- **Related work** — positions the paper against others; states differences.
- **Method** — reproducible; notation defined before use; assumptions explicit.
- **Experiments** — setup, datasets, baselines, metrics, hyperparameters; fair
  comparison; statistical significance / variance where relevant.
- **Results** — claims supported by the numbers shown; no over-interpretation.
- **Discussion / limitations** — honest; threats to validity.
- **Conclusion** — no new claims; matches the introduction's promises.
- **Page limits & template compliance** (e.g. LLNCS: abstract length, keywords,
  figure/table placement).

## 3. Abstract

- Problem, approach, key result, implication — all present?
- Within word limit; no citations or undefined abbreviations; standalone.

## 4. Thesis chapter

- Clear purpose stated at the start; links to previous and next chapter.
- Consistent with the thesis's research questions; summary at the end.

## 5. Cross-cutting checks (all types)

- **Golden thread** — every section serves the research question; can each
  paragraph's purpose be stated in one sentence?
- **Paragraph structure** — topic sentence first; one idea per paragraph.
- **Terminology** — each key term defined once and used consistently; acronyms
  defined at first use.
- **Claims** — every non-trivial claim is supported (citation, data, or argument).
- **Hedging** — appropriate: not overclaiming ("proves", "always") nor drowning
  in qualifiers.
- **Figures & tables** — all referenced in text, in order; captions explain what to
  see.
- **Consistency** — numbers, names and terms match across abstract, body, figures.
