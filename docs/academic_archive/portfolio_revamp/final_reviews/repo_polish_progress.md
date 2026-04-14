# Repo Polish Progress

## Stages completed
- Stage 3: Restructure
- Stage 4: Reproducibility
- Stage 5: README
- Stage 6: Engineering proof

## Shared assumptions
- The portfolio-process and scoring files were treated as internal working material, not public project docs.
- Because their value was not zero but they did not belong in the recruiter-facing root, they were archived under `docs/academic_archive/portfolio_revamp/` instead of being deleted.
- The supported backend run path for this repo is from the repository root via `python -m backend.app`.
- The supported frontend run path remains from `frontend/` via `npm start`.

## Stage 3: Restructure

### What changed
- Cleaned the public root so it now centers on the project itself plus essential folders.
- Created the planned structure folders needed for later stages:
  - `assets/`
  - `results/`
  - `docs/academic_archive/`
  - `docs/academic_archive/portfolio_revamp/`
  - `backend/tests/`
  - `.github/workflows/`
  - `scripts/`
- Updated [`README.md`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/README.md) with a more professional one-line summary without attempting the full rewrite yet.
- Updated [`frontend/src/components/Header.js`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/frontend/src/components/Header.js) to remove course and instructor branding from the UI.
- Updated [`frontend/src/index.js`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/frontend/src/index.js) to remove the unused CRA `reportWebVitals` import and call.
- Updated [`frontend/public/manifest.json`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/frontend/public/manifest.json) to remove Create React App branding and unused icon references.
- Expanded [`.gitignore`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/.gitignore) to cover `.DS_Store`, `.venv`, `.pytest_cache`, and frontend build output.

### What was moved
- Moved these root-level portfolio/meta files into `docs/academic_archive/portfolio_revamp/`:
  - `PORTFOLIO_CONTEXT.md`
  - `REPO_STANDARD.md`
  - `POLISH_WORKFLOW.md`
  - `MANUAL_REVIEW_CHECKLIST.md`
  - `caption_generator_repo_polish_audit.md`
  - `caption_generator_repo_polish_plan.md`
  - `github_portfolio_rubric.md`
  - `repo_image_and_video_caption_generator.md`

### What was removed
- Removed obvious junk and generated artifacts:
  - `.DS_Store`
  - `backend/.DS_Store`
  - `backend/models/.DS_Store`
  - `backend/__pycache__/`
  - `backend/models/__pycache__/`
- Removed CRA/publication-noise files that added no value to the portfolio presentation:
  - `frontend/README.md`
  - `frontend/.gitignore`
  - `frontend/src/logo.svg`
  - `frontend/src/reportWebVitals.js`
  - `frontend/src/App.test.js`
  - `frontend/public/logo192.png`
  - `frontend/public/logo512.png`

### Verification notes
- The frontend/backend split was preserved.
- No backend model logic was refactored during Stage 3.
- No API paths were changed during Stage 3.

## Stage 4: Reproducibility

### What changed
- Added [`backend/requirements.txt`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/backend/requirements.txt) with pinned Python dependencies used by the backend runtime and smoke-test path.
- Added [`.env.example`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/.env.example) with the minimal backend and frontend environment variables needed for the supported local run path.
- Added [`frontend/src/config.js`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/frontend/src/config.js) so the frontend reads its API base URL from `REACT_APP_API_BASE_URL` instead of hardcoding fetch targets inline.
- Updated [`frontend/src/App.js`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/frontend/src/App.js) to use the new frontend config helper for both API calls.
- Added [`backend/__init__.py`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/backend/__init__.py) so the backend can be run as a module from the repo root.
- Refactored [`backend/app.py`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/backend/app.py) to:
  - support `create_app()`
  - read host, port, debug mode, and upload root from environment variables
  - use sane defaults when env vars are not set
  - support a lazy caption-service boundary so mocked tests do not import the ML stack
- Refactored [`backend/models/caption_generator.py`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/backend/models/caption_generator.py) so model weights load lazily on first inference call instead of at import time.
- Added [`scripts/smoke_test.py`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/scripts/smoke_test.py) as the supported smoke-test entry path.
- Updated [`.gitignore`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/.gitignore) to ignore `.env` alongside previously ignored generated paths.

### Reproducibility issues fixed
- The backend now has one explicit dependency manifest instead of an implied Python environment.
- The repo now has one explicit backend startup path: `python -m backend.app`.
- The frontend no longer hardcodes API URLs inside component logic.
- Backend host, port, debug mode, and upload directory are configurable instead of being baked into the code path.
- App import and smoke testing no longer trigger model downloads or require `transformers` import at startup when inference is mocked.
- The supported smoke test validates the API wiring without using network access, GPU access, or real model downloads.

### Verification
- Ran `python3 scripts/smoke_test.py` successfully from the repo root.
- The smoke test passed after the lazy caption-service boundary was added.

## Stage 5: README

### What changed
- Rewrote [`README.md`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/README.md) for a recruiter-facing skim plus technical quickstart.
- Added architecture, quickstart, smoke-test, API behavior, limitations, and repo-structure sections grounded in the current codebase.
- Added [`README_review_notes.md`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/README_review_notes.md) to capture remaining gaps and intentionally avoided claims.

## Stage 6: Engineering proof

### What was added
- Added [`backend/tests/test_api.py`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/backend/tests/test_api.py) with mocked backend API coverage.
- Added [`frontend/src/App.test.js`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/frontend/src/App.test.js) as one real frontend behavior test for the current UI.
- Added [`.github/workflows/ci.yml`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/.github/workflows/ci.yml) for lightweight backend and frontend checks in GitHub Actions.

### What testing paths now exist
- Smoke test: `python scripts/smoke_test.py`
- Backend API tests: `python -m pytest backend/tests`
- Frontend UI test: `npm test -- --watchAll=false` from `frontend/`

### What CI validates
- Backend dependency installation on GitHub Actions.
- Backend mocked API tests via `pytest backend/tests`.
- Frontend dependency installation via `npm ci`.
- Frontend test execution via `npm test -- --watchAll=false`.

### Verification
- Ran `python3 -m pytest backend/tests` successfully; 3 tests passed.
- Could not run the frontend test locally in this environment because `npm` is not installed here.

## Deferred items
- Additional backend/frontend coverage beyond the current narrow test set.
- Broader backend config cleanup and structured error-contract improvements.
- Demo artifacts, qualitative examples, and evaluation notes.
- Any packaging, deployment, Docker, or infra work beyond the supported local run/test path.

## Current top-level tree
```text
image-and-video-caption-generator/
├── .env.example
├── .github/
│   └── workflows/
├── .gitignore
├── README.md
├── assets/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── models/
│   ├── requirements.txt
│   └── tests/
│       └── test_api.py
├── docs/
│   └── academic_archive/
│       └── portfolio_revamp/
├── frontend/
│   ├── package-lock.json
│   ├── package.json
│   ├── public/
│   └── src/
│       └── App.test.js
├── repo_polish_progress.md
├── repo_restructure_summary.md
├── engineering_proof_summary.md
├── repro_check.md
├── results/
└── scripts/
    └── smoke_test.py
```
