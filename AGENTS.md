# Repository guidance

## Purpose and scope

This repository is a local, cross-platform knowledge base and code-practice workspace for studying Li Hang's *Machine Learning Methods*: supervised learning, unsupervised learning, deep learning, and reinforcement learning.

## Required tools and constraints

- Write notes in Markdown with LaTeX for mathematical notation. Every chapter `notes.md` begins with YAML frontmatter following the schema in the chapter template.
- Use the existing local Anaconda environment named `study4ai` for Python scripts and tests: `conda run -n study4ai python ...` and `conda run -n study4ai pytest ...`. An already activated `study4ai` environment is also acceptable.
- Do not create `.venv`, `venv`, Conda environments, or other project-local Python environments.
- Before installing a missing lightweight dependency such as PyYAML or pytest, ask the user and wait for confirmation.
- Obsidian is the only visualization layer. Use Dataview, DataviewJS, and Canvas; do not add web frameworks, backend services, or databases.
- All Markdown links, image references, and generated Canvas file references use standard relative paths. Do not use Obsidian `[[wikilinks]]` syntax.
- **Collaboration red line:** do not proactively fill in, replace, or rewrite a chapter's concrete algorithm implementation in `impl.py`. When the user asks for code practice based on supplied book material, implement only the requested formula or concept and keep it traceable to the relevant source pages; do not expand that request into a full chapter implementation.
- When the user supplies book content for a chapter, use it to update that chapter's `notes.md` with source-grounded explanations, formula derivations, and parameter interpretations, and maintain `interview_questions.md` with questions and answer outlines based on the same material.
- Cite the book edition and page numbers in notes and interview questions. Distinguish what the book states from explanations or examples added for clarity. Use standard relative Markdown links to local source files.

## Directory conventions

- `00_math_foundations/`: mathematics and shared prerequisites.
- `00_math_foundations/appendices/`: appendices A-G and their optional learning materials.
- `01_supervised/`, `02_unsupervised/`, `03_deep_learning/`, `04_reinforcement_learning/`: chapters grouped by topic.
- Each chapter is a folder containing `notes.md`, `interview_questions.md`, `impl.py`, `test_verify.py`, and `materials/` for chapter-specific excerpts, page images, or user-provided extracts.
- Store each chapter's PDF in that chapter's `materials/` directory, for example `01_supervised/01_perceptron/materials/source.pdf`. Do not place a combined part PDF or a duplicate whole-book PDF in a chapter folder.
- Record source edition and page ranges in chapter notes. Cite the printed page and PDF page index when they differ. Link chapter materials with standard relative paths.
- `scripts/`: repository maintenance and generation scripts.
- `tests/`: pytest tests for repository scripts and tooling.
- Book chapter folders use `chNN_slug/`, where `NN` is the book chapter number; `Book_TOC.md` is the cross-platform linked index.
- `scripts/scaffold_chapters.py` creates missing chapter templates from its book catalog and never overwrites existing files. Prerequisites remain empty until verified; do not invent dependency links from chapter order alone.
- Chapter `id` values are globally unique; `prereqs` lists those IDs, not paths or titles.

## Metadata schema

Required frontmatter fields: `id` (unique non-empty string), `module` (one of the five module directory names), `title` (non-empty string), `prereqs` (list of chapter IDs), `status` (mapping with `derivation`, `params`, and `code`, each an integer from 0 through 2), and `last_reviewed` (ISO date `YYYY-MM-DD` or `null`). Do not use booleans as status integers. Prerequisite links must resolve and the dependency graph must be acyclic.

Status meanings: `0` = not started, `1` = in progress, `2` = understood / completed.

## Editing and verification

- Keep generated and hand-maintained files deterministic and UTF-8.
- When changing metadata or generation behavior, run `conda run -n study4ai pytest` and validate metadata with `conda run -n study4ai python scripts/validate_metadata.py`.
- Regenerate `knowledge_graph.canvas` with `conda run -n study4ai python scripts/build_canvas.py` after changing chapter metadata.
