# Repo Polish Plan

## 1. Keep / move / archive / remove
- Assumption: the portfolio-process files in the current root are internal working notes, not public project docs, and should not remain in the final recruiter-facing root.

- Keep in public root/path:
  - `README.md`: keep, but fully rewrite for the final public story.
  - `.gitignore`: keep, but expand to cover OS junk, caches, test artifacts, virtualenvs, and generated uploads.
  - `backend/app.py`: keep as the supported API entry point, but clean up config handling and startup behavior.
  - `backend/models/__init__.py`: keep.
  - `backend/models/caption_generator.py`: keep, but refactor lightly for lazy model loading, safer video handling, and testability.
  - `frontend/package.json`: keep.
  - `frontend/package-lock.json`: keep for reproducible frontend installs.
  - `frontend/public/index.html`: keep.
  - `frontend/public/favicon.ico`: keep.
  - `frontend/public/manifest.json`: keep, but replace CRA branding with project branding.
  - `frontend/public/robots.txt`: keep.
  - `frontend/src/App.js`: keep.
  - `frontend/src/App.css`, `frontend/src/index.css`, `frontend/src/styles/global.css`: keep.
  - `frontend/src/components/`: keep all current UI components, but remove academic text and route API calls through config.
  - `frontend/src/index.js`: keep.
  - `frontend/src/setupTests.js`: keep.

- Move:
  - Any future course screenshots, reports, or submission PDFs: move to `docs/academic_archive/`.
  - Any polished demo screenshots/GIFs: move into `assets/screenshots/`.
  - Any curated demo input files: move into `assets/sample_inputs/`.
  - Any qualitative example tables or short evaluation notes: move into `results/`.

- Archive under `docs/academic_archive/`:
  - No current file clearly belongs here yet.
  - If you decide to preserve evidence of the original class project framing, archive that material here rather than leaving it in the app UI or public root.

- Remove:
  - `PORTFOLIO_CONTEXT.md`
  - `REPO_STANDARD.md`
  - `POLISH_WORKFLOW.md`
  - `MANUAL_REVIEW_CHECKLIST.md`
  - `caption_generator_repo_polish_audit.md`
  - `caption_generator_repo_polish_plan.md`
  - `github_portfolio_rubric.md`
  - `repo_image_and_video_caption_generator.md`
  - `frontend/README.md`
  - `frontend/src/logo.svg`
  - `frontend/src/reportWebVitals.js`
  - `frontend/.gitignore`: consolidate ignore rules in the root `.gitignore`.
  - `.DS_Store`
  - `backend/.DS_Store`
  - `backend/models/.DS_Store`
  - `backend/__pycache__/`
  - Any generated `uploads/` content if present locally.

## 2. Final target root structure
```text
image-and-video-caption-generator/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── __init__.py
│   │   └── caption_generator.py
│   └── tests/
│       └── test_api.py
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   └── src/
│       ├── App.css
│       ├── App.js
│       ├── App.test.js
│       ├── index.css
│       ├── index.js
│       ├── setupTests.js
│       ├── config.js
│       ├── components/
│       └── styles/
├── scripts/
│   └── smoke_test.py
├── assets/
│   ├── screenshots/
│   └── sample_inputs/
├── results/
│   └── qualitative_examples.md
├── docs/
│   └── academic_archive/
└── .github/
    └── workflows/
        └── ci.yml
```

## 3. README plan
1. Title and one-line summary
   Include the project name and a compact description of image captioning, video frame captioning, and optional translation.
2. Why this project matters
   Explain why this is a useful supporting MLE portfolio repo: multimodal inference, API/UI integration, and model-serving awareness.
3. Demo snapshot
   Add 1-2 screenshots or a short GIF plus a few bullets summarizing the user flow and output types.
4. Key features
   List image captioning, video frame sampling, multilingual translation, upload validation, and frontend/backend split.
5. Architecture overview
   Show a simple request flow: frontend upload -> Flask endpoint -> BLIP caption generation -> optional MarianMT translation -> JSON response -> UI rendering.
6. Tech stack
   List React, Flask, Transformers, BLIP, MarianMT, Pillow, OpenCV, and testing tools.
7. Quickstart
   Provide exact install and run steps for backend and frontend, plus required environment variables.
8. API behavior
   Document the two endpoints, accepted file types, expected request fields, and example JSON responses.
9. Results and qualitative examples
   Link to `results/qualitative_examples.md` and summarize representative outputs, multilingual examples, and observed latency.
10. Limitations and tradeoffs
   Explain frame sampling is simple, captions are model-dependent, translation quality varies, and cold-start downloads can be slow.
11. Repo structure
   Show the final root tree with one-line explanations for major folders.
12. Testing and CI
   State the supported smoke-test command, frontend test command, and CI coverage.
13. Future improvements
   Keep this short and honest: batching, async processing, better video summarization, and deployment hardening are enough.

## 4. Reproducibility plan
- Backend dependency setup:
  - Add `backend/requirements.txt` with pinned versions for Flask, Flask-Cors, transformers, torch, Pillow, opencv-python, pytest, and any small helper packages actually used.
  - Document the supported Python version in `README.md`.
  - Keep the backend install path simple: `python -m venv .venv`, activate, `pip install -r backend/requirements.txt`.

- Frontend dependency/setup clarity:
  - Keep `frontend/package-lock.json` as the reproducible source of truth.
  - Document the supported Node version in `README.md`.
  - Keep the frontend install path simple: `cd frontend && npm install`.
  - Replace the placeholder frontend README by documenting the supported workflow only in the root README.

- Environment/config handling:
  - Add a root `.env.example` with the minimal variables actually needed.
  - Add `REACT_APP_API_BASE_URL` for frontend API configuration.
  - Add backend env/config support for host, port, debug mode, and upload base directory with sane defaults.
  - Keep model names configurable only if this can be done with minimal code churn; otherwise document the current fixed model choices clearly.

- Supported startup path:
  - Backend supported path: run the Flask app from the repo root or via a documented module/script path that does not depend on ambiguous working directories.
  - Frontend supported path: `npm start` from `frontend/`.
  - Make the frontend read the backend base URL from config instead of hardcoding `http://127.0.0.1:5000`.
  - Lightly refactor backend initialization so heavy model loading does not block import-time tests or break CI.

- Smoke-test path:
  - Add `scripts/smoke_test.py` as the single supported smoke-test entry point.
  - The smoke test should use Flask’s test client and mock caption generation so it validates API wiring without downloading models.
  - Cover one happy-path image request and one upload-validation failure case.

## 5. Engineering proof plan
- Backend tests:
  - Add `backend/tests/test_api.py`.
  - Test `POST /api/generate-image-caption` with a mocked caption generator and an in-memory image file.
  - Test one negative case such as missing file or invalid extension.
  - If lightweight enough, add one mocked video endpoint test; if not, keep image endpoint plus validation as the minimum credible bar.

- Frontend tests:
  - Replace the CRA placeholder `App.test.js`.
  - Add one real behavior test that renders the app and verifies the actual UI elements are present, such as the project heading, language selector, and upload prompts.
  - Keep frontend testing shallow; do not build an extensive suite.

- CI workflow:
  - Add `.github/workflows/ci.yml`.
  - Run one backend install plus pytest job.
  - Run one frontend install plus test job with `npm test -- --watchAll=false`.
  - Keep CI focused on installability and basic behavior, not linting or deployment.

- Config cleanup:
  - Centralize allowed file extensions and upload directories in backend config/constants.
  - Remove hardcoded frontend fetch URLs and replace them with a small config module such as `frontend/src/config.js`.
  - Ensure backend errors return consistent JSON shapes for easier testing and clearer UI handling.

- Scripts or commands for running:
  - Add `scripts/smoke_test.py`.
  - Prefer documented cross-platform commands in `README.md` over shell-only wrappers.
  - Only add more scripts if they reduce ambiguity; do not add a large tooling layer.

## 6. Demo / evaluation artifacts plan
- Screenshots:
  - Add 2-3 polished screenshots in `assets/screenshots/`.
  - Minimum set: landing/upload screen, image caption result, video caption result.

- Sample inputs:
  - Add 2-3 small image inputs and 1 short video clip in `assets/sample_inputs/`, only if licensing and repo size are safe.
  - If file sizes are too large, keep thumbnails/stills in git and link to hosted demo inputs instead.

- Sample outputs:
  - Add `results/qualitative_examples.md` with a small table of input type, generated caption, and brief comment.
  - Include one image example and one video example at minimum.

- Multilingual examples:
  - Include 2-3 translated caption examples, for example English to Spanish and English to French.
  - Keep this qualitative, not benchmark-style.

- Latency notes:
  - Add a short note on approximate local latency for image caption generation and for short video processing.
  - Call out first-run model download and cold-start cost explicitly.

- Failure cases:
  - Document a few known weak spots such as dense scenes, ambiguous actions, weak frame sampling for long videos, and translation phrasing drift.
  - Keep this to a short honest section, not a research error analysis.

## 7. Implementation order
1. Clean the public root: remove portfolio/meta docs from the final repo path, delete generated junk, and add `LICENSE`.
2. Add backend reproducibility basics: `backend/requirements.txt`, supported Python version guidance, and minimal config/env handling.
3. Lightly refactor backend startup and model-loading boundaries so the app can be imported and tested without real model downloads.
4. Add frontend config for API base URL and remove hardcoded localhost assumptions.
5. Remove academic/scaffold signals from the frontend UI and boilerplate files.
6. Add the backend smoke/API tests with mocked inference.
7. Replace the frontend placeholder test with one real behavior test.
8. Add the basic GitHub Actions CI workflow.
9. Add demo artifacts: screenshots, sample inputs if feasible, and `results/qualitative_examples.md`.
10. Rewrite the root README using the final working commands, final structure, and real example outputs.
11. Do a final hygiene pass on `.gitignore`, manifests, unused files, and documentation consistency.

## 8. Risks / cautions
- Do not break the current working image/video caption flow while cleaning up structure.
- Do not remove the frontend/backend split or collapse everything into one script.
- Do not overbuild configuration, packaging, or infra; this repo needs one clear local run path, not Docker, Terraform, or deployment orchestration.
- Do not turn evaluation into a benchmark project; qualitative examples plus latency/failure notes are enough.
- Do not let tests depend on real model downloads, GPU availability, or network access.
- Do not keep course framing in the UI or README, but also do not fabricate a larger production story than the code supports.
- Do not keep default CRA artifacts that add noise, but avoid churning frontend structure more than necessary.
- Do not commit generated uploads, caches, or large demo media that make the repo heavy.

## 9. Definition of done
- The public root contains only project-facing material plus essential repo files.
- The repo has one clear backend install path, one clear frontend install path, one supported run path, and one supported smoke-test path.
- Backend dependencies are pinned in `backend/requirements.txt`, and frontend API configuration is no longer hardcoded to localhost.
- The frontend no longer shows course/instructor branding or default CRA placeholder behavior.
- The repo includes at least one backend API smoke test, one real frontend behavior test, and one passing CI workflow.
- The README explains the project, architecture, quickstart, API behavior, results, and tradeoffs clearly enough for a recruiter skim and a short technical review.
- The repo includes visible demo artifacts and a lightweight qualitative results file with multilingual examples, latency notes, and failure cases.
- The final result reads as a compact, reproducible multimodal inference app with credible MLE engineering signals, not as an academic submission or thin wrapper demo.
