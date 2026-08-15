# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses `uv` for dependency management (see `uv.lock`, `pyproject.toml`).

```bash
uv sync                    # install/sync dependencies
uv run python app.py       # run the Flask + Socket.IO dev server (http://0.0.0.0:5000)
uv run pytest              # run the full test suite
uv run pytest src/core/strategies/__tests__/test_strategy_factory.py   # run a single test file
uv run pytest src/core/strategies/__tests__/test_strategy_factory.py::test_calculation_strategy_factory  # single test
```

Tests live alongside the code they cover, in `__tests__/` directories under each `src/core/*` package (not under one top-level `tests/` folder).

`app.py` requires `DB_URI` to be set (via `.env`, loaded with `python-dotenv`) — a MongoDB connection string used by `flask_pymongo`.

## Architecture

This is a Flask backend for an arithmetic tuition app, combining a REST API (MongoDB-backed question bank) with a Socket.IO-driven live assessment session. It was split out of a monorepo (`arithmetical-tuition-api` + `arithmetical-tuition-ui`) into this standalone repo; `Dockerfile`/`docker-compose.yaml` still reference the old sibling-directory layout and are stale relative to the current single-repo structure.

**App wiring** (`app.py` → `src/flask_app_factory.py`): `create_flask_app()` builds the Flask app (serving the UI's built `dist/` as static/template folder), registers the `index` and `questions` blueprints under `/api`, and attaches the Socket.IO server from `assessment_controller`. `src/db.py` wraps `flask_pymongo.PyMongo` with `init_db(app)` / `get_db()` — always fetch the DB via `get_db()` rather than importing `mongo` directly.

**Two parallel surfaces:**
- **REST** (`src/controllers/questions_controller.py`): CRUD over the `questions` Mongo collection. Mongo `_id` (ObjectId) is translated to/from a plain `id` string field via `src/core/utils/serialize_model.py` (`_id` → `id`, outbound) and `deserialize_model.py` (`id` → `_id`, inbound), applied recursively to any nested `items` lists.
- **Socket.IO** (`src/controllers/assessment_controller.py`): drives a live quiz session with module-level global state (`assessment`, `assessment_iterator`, `assessment_item`) reset on `disconnect`. Events: `start` (builds an assessment from random number pairs), `question` (advances the iterator, emits `end` on exhaustion), `answer` (evaluates the current question). This global state means only one concurrent session is supported per process.

**Core domain logic** (`src/core/`) is a layered Strategy/Factory design, evaluated top-down:
1. `assessment/` — `IAssessment`/`Assessment` wraps a sequence of evaluable items and exposes aggregate `results`/`result`.
2. `question_evaluation/` — `QuestionEvaluation` is the `IAssessmentItem` implementation; `QuestionEvaluationFactory.create(question, operation)` picks a `QuestionType` (`calculation` / `sequence` / `quiz`) by checking which enum the `operation` string belongs to (`CalculationType`, then falls back to sequence, then `QuizType`).
3. `strategies/` — `StrategyFactory.create(question: IQuestionAdapter)` pattern-matches on `question.type` to delegate to `CalculationStrategyFactory`, `SequenceStrategyFactory`, or `QuizStrategyFactory`, each producing an `IStrategy` (`do_algorithm` + `compare`). `QuestionEvaluation._strategy()` adapts itself into an ad-hoc `IQuestionAdapter` (via `type('Test', (IQuestionAdapter,), self.to_dict())()`) to feed the factory.

Several core modules (`assessment.py`, `question_evaluation.py`, `calculation_strategies.py`, `quiz_strategies.py`, `sequence_strategies.py`) are generated from sibling `.ipynb` notebooks via `nbtopy` — the `# %%` cell markers are notebook cell boundaries. When editing this logic, prefer editing the notebook if making substantial changes so the two stay in sync; the `#!/usr/bin/env python3` + `## Built from ... by nbtopy ##` header marks these generated files.
