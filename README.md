# paper-review

[![CI](https://github.com/MrTarantoga/paper-review/actions/workflows/ci.yml/badge.svg)](https://github.com/MrTarantoga/paper-review/actions/workflows/ci.yml)

A [Claude Code](https://claude.com/claude-code) skill for critical review,
proofreading and meaning-preserving paraphrasing of academic writing: research
papers, exposés and research proposals, thesis chapters, abstracts. It works on
LaTeX, Markdown, plain text and pasted paragraphs.

It acts as a demanding but fair editor. It points out weaknesses honestly, keeps
the author's voice and exact meaning, and **never changes your text without your
approval of each specific change**.

## What it does

- **Paraphrase (QuillBot-style):** academic, formal, fluent, concise, simplified
  or expanded rewrites, with two or three genuinely different alternatives per
  passage and a warning wherever a rephrase could shift the meaning.
- **Grammar and style:** articles, prepositions, tense, nominal style, filler,
  inconsistent terminology. It includes specific checks for German-influenced
  English (false friends such as *actual*/*aktuell* or *eventually*/*eventuell*,
  "on the other side", sentence-initial "Also,").
- **Structural review:** checklists for exposés and proposals, research papers,
  abstracts and thesis chapters
  ([`references/review-checklist.md`](skills/paper-review/references/review-checklist.md)).
- **Citation check:** a bundled script
  ([`scripts/check_citations.py`](skills/paper-review/scripts/check_citations.py))
  reports cite keys missing from the `.bib`, unused entries, duplicate keys and
  entries lacking common fields. It follows `\input`/`\include`. The skill
  also flags uncited claims and never invents references.
- **Reviewer feedback:** a concise peer-review report covering summary,
  strengths, major and minor issues, hard-to-follow passages, questions, and an
  overall assessment.
- **Unclear passages** are marked separately, with an explanation of *why* a
  reader would stumble, and the skill asks instead of guessing what you meant.

## How it works

1. **Scope:** clarifies which mode and which part of the text you want.
2. **Analyse and report:** numbered findings, ordered by importance (meaning and
   logic first, nitpicks last).
3. **Discuss:** goes through every issue with you **one question per
   decision**, using Claude Code's multiple-choice question dialog, with a
   recommended option and the consequences of each choice.
4. **Apply:** rewrites section by section, again one question per change, with
   an `OLD:`/`NEW:` preview. It applies only what you approved, then compiles
   LaTeX into a scratch directory to check for broken references or citations,
   and re-reads the result for problems its own edits introduced.

If you say "just apply everything", it does so, except for changes that would
alter meaning or that depend on an unanswered question.

LaTeX stays intact: commands, `\cite`/`\ref`/`\label`, math, comments, `~`, and
line structure. If you prefer annotations to edits, it can insert `\todo{}`
notes (`todonotes`).

## Installation

### As a plugin (recommended)

In Claude Code:

```
/plugin marketplace add MrTarantoga/paper-review
/plugin install paper-review@paper-review
```

### Manually

Download the zip from the latest
[release](https://github.com/MrTarantoga/paper-review/releases/latest), or copy the skill folder into your personal or project skills directory:

```bash
git clone https://github.com/MrTarantoga/paper-review.git
cp -r paper-review/skills/paper-review ~/.claude/skills/        # all projects
# or
cp -r paper-review/skills/paper-review <project>/.claude/skills/ # one project
```

The citation checker needs only Python 3 (standard library).

## Usage

The skill triggers on its own for requests such as:

- "Review my exposé"
- "Can you look over section 2?"
- "Paraphrase this paragraph, more concise"
- "Check my citations"
- "Give me reviewer feedback on the introduction"
- "Is this sentence OK?"

You can also run the citation checker on its own:

```bash
python3 skills/paper-review/scripts/check_citations.py main.tex [--bib refs.bib]
```

## How it differs from similar skills

Several community skills cover academic proofreading and peer review, for
example [JakobThumm/proofreading](https://github.com/JakobThumm/proofreading),
`flonat/claude-research` (proofread), `jkitchin/skillz` (scientific-reviewer),
`K-Dense-AI/claude-scientific-writer` (peer-review) and
`bahayonghang/academic-writing-skills`. Most of them either produce a
report only or rewrite in bulk. This skill aims for the middle ground:

- an **interactive, approval-gated workflow**: one decision per question, edits
  applied only after explicit approval, section by section;
- **strict meaning and voice preservation**: no strengthened or weakened
  claims, no added facts, hedges or citations, and none of the generic
  "AI prose" vocabulary;
- review, paraphrasing, structural checklists and citation checking **in one
  skill**;
- attention to the typical errors of **German native speakers** writing in
  English.

## Development

CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs on every push
and pull request. To run the same checks locally:

```bash
python3 tests/validate_skill.py          # SKILL.md frontmatter, manifests, file references
python3 -m unittest discover -s tests -v # citation checker tests
ruff check .                             # lint
```

### Releasing

1. Bump `version` in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) and commit.
2. Tag and push: `git tag v1.0.1 && git push origin v1.0.1`.

The [release workflow](.github/workflows/release.yml) checks that the tag
matches `plugin.json`, runs validation and tests, and publishes a GitHub release
with generated notes and a zipped skill folder (`paper-review-vX.Y.Z.zip`).

## Licence

[MIT](LICENSE)
