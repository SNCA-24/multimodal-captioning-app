# Reproducibility Check

## 1. Backend setup path
- Exact install steps:
  - From the repo root: `python -m venv .venv`
  - Activate on macOS/Linux: `source .venv/bin/activate`
  - Activate on Windows PowerShell: `.venv\Scripts\Activate.ps1`
  - Install dependencies: `pip install -r backend/requirements.txt`
  - Copy [`.env.example`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/.env.example) to `.env` if you want to override defaults.
- Exact run command:
  - From the repo root: `python -m backend.app`

## 2. Frontend setup path
- Exact install steps:
  - From the repo root: `cd frontend`
  - Install dependencies: `npm install`
- Exact run command:
  - From `frontend/`: `npm start`

## 3. Environment/config handling
- Variables added:
  - `BACKEND_HOST`
  - `BACKEND_PORT`
  - `BACKEND_DEBUG`
  - `BACKEND_UPLOAD_DIR`
  - `REACT_APP_API_BASE_URL`
- Defaults used:
  - `BACKEND_HOST=127.0.0.1`
  - `BACKEND_PORT=5000`
  - `BACKEND_DEBUG=false`
  - `BACKEND_UPLOAD_DIR=uploads`
  - `REACT_APP_API_BASE_URL=http://127.0.0.1:5000`
- Assumptions removed:
  - Frontend API calls are no longer hardcoded inline to one backend URL.
  - Backend startup no longer depends on `debug=True` being hardcoded in source.
  - Upload directories are no longer fixed in multiple ad hoc code paths.
  - Importing the Flask app no longer forces model downloads at startup.

## 4. Smoke-test path
- Exact command:
  - From the repo root: `python scripts/smoke_test.py`
- What it validates:
  - Flask app creation
  - image caption endpoint wiring
  - video caption endpoint wiring
  - request validation for missing file uploads
  - upload-directory handling through the configured app paths
- What is mocked:
  - caption generation
  - video caption generation
  - all model inference and model downloads

## 5. Remaining reproducibility gaps
- The README still does not contain the final polished quickstart and architecture sections.
- There is still no frontend behavior test or backend pytest suite beyond the smoke-test script.
- There is still no CI workflow to enforce install/run/test consistency automatically.
- The backend still assumes the ML stack is installed for real inference, which is correct for runtime but not yet documented in the final README.
- No pinned Node version is documented yet.
- Real inference runtime characteristics such as first-run model download time and CPU/GPU expectations are not yet surfaced in public docs.

## 6. Risks / cautions
- Actual caption generation still depends on heavyweight ML packages from `backend/requirements.txt`; the smoke test only proves API wiring, not real model execution.
- The frontend now depends on `REACT_APP_API_BASE_URL` only at build/runtime startup, so changing it requires restarting the frontend dev server.
- The supported backend path is `python -m backend.app`; running the backend some other way may reintroduce path ambiguity.
- Stage 5/6 should verify the real frontend and backend startup path end to end after dependencies are installed, then add the lightweight engineering proof and final docs.
