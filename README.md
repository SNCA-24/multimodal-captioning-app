# Multimodal Caption Generator

Compact multimodal inference app that captions uploaded images and sampled video frames through a React frontend, a Flask API, and pretrained Hugging Face models.

## Tech Stack Snapshot

- **Frontend:** React, Create React App, react-spinners
- **Backend / API:** Python, Flask, Flask-CORS
- **ML / AI:** Hugging Face Transformers, BLIP (`Salesforce/blip-image-captioning-base`), MarianMT
- **Media Processing:** Pillow, OpenCV
- **Verification / Engineering:** pytest, React Testing Library, GitHub Actions

## Why This Project Exists

Image captioning demos often stop at notebooks or single-script inference. This project packages that workflow into a small end-to-end application with a visible user flow, API boundaries, reproducible local setup, and lightweight test coverage.

The practical problem it addresses is straightforward: take user-uploaded visual media, generate text descriptions, and optionally translate those descriptions into another language. The non-trivial part is turning pretrained model inference into a usable app shape rather than a one-off experiment.

## What This Project Builds

This project builds:

- a React UI for uploading images and videos
- a Flask API for caption generation requests
- a BLIP-based image captioning path
- a simple video captioning path based on frame sampling
- an optional translation path for generated captions
- local test, smoke-test, and CI checks for API/UI behavior

This repo demonstrates a local prototype / academic-style application. It does not claim production deployment, real-user adoption, or benchmark leadership.

## Architecture / Workflow

```text
Browser UI
  -> upload image or video + choose target language
  -> POST multipart form data to Flask API
  -> backend saves file to local upload directory
  -> caption service runs BLIP caption generation
     -> for videos: sample frames based on FPS and caption sampled frames
     -> for non-English output: translate generated caption with MarianMT
  -> JSON response
  -> UI renders caption text or frame/caption pairs
```

| Component | Purpose |
|---|---|
| `frontend/src/App.js` | Coordinates image/video upload, loading state, error state, and caption rendering |
| `frontend/src/config.js` | Builds API URLs from `REACT_APP_API_BASE_URL` |
| `backend/app.py` | Defines the Flask app, upload handling, validation, and API routes |
| `backend/models/caption_generator.py` | Loads models, captions images, samples video frames, and translates output |
| `backend/tests/test_api.py` | Verifies endpoint behavior with mocked inference |
| `scripts/smoke_test.py` | Provides a fast repo-root smoke test without model downloads |

## Key Features

### System Features

- Separate upload flows for images and videos
- Configurable backend host, port, debug mode, upload root, and frontend API base URL
- Local upload persistence under configured image/video directories
- JSON API responses for both single-caption and multi-caption outputs

### ML / AI Features

- BLIP-based image caption generation
- Video caption generation from sampled frames
- Optional translation from English into supported target languages
- Lazy model loading so importing the Flask app does not immediately download models

### Engineering Features

- Backend endpoint tests with injected mock caption services
- Standalone smoke test for endpoint wiring and validation behavior
- Frontend UI test for rendering and language selection
- GitHub Actions workflow running backend and frontend test jobs

## Technical Implementation

### Core Components

- **API layer:** `backend/app.py` defines `create_app()`, CORS setup, allowed file types, environment-driven config, and the two public routes:
  - `POST /api/generate-image-caption`
  - `POST /api/generate-video-caption`
- **Model layer:** `backend/models/caption_generator.py` loads BLIP and MarianMT models, generates captions, and translates when `language != "en"`.
- **Frontend layer:** `frontend/src/App.js` manages upload events, loading state, error handling, and separate rendering for image captions versus video caption lists.

### Execution Flow

1. The UI collects a file and target language.
2. The frontend sends multipart form data to the backend.
3. The backend validates file presence and extension, then writes the upload to the configured local directory.
4. The caption service generates a caption:
   - images go directly through BLIP
   - videos are opened with OpenCV and sampled at roughly one frame per second based on FPS
5. If the target language is not English, the generated English caption is translated with MarianMT.
6. The backend returns JSON and the frontend renders caption text or frame/caption pairs.

### Important Modules

- `backend/app.py`: request validation, upload path management, route registration, environment config
- `backend/models/caption_generator.py`: BLIP inference, MarianMT translation, OpenCV frame sampling
- `frontend/src/components/ImageUpload.js`: image selection and preview
- `frontend/src/components/VideoUpload.js`: video selection and preview
- `frontend/src/components/CaptionDisplay.js`: renders either a string caption or a list of video frame captions
- `.github/workflows/ci.yml`: backend/frontend CI jobs

### Outputs / Artifacts

- Image caption response: `{"caption": "<text>"}`
- Video caption response: `{"captions": [{"frame": <index>, "caption": "<text>"}]}`
- Local uploads written under `uploads/images` and `uploads/videos` by default

### Verification Hooks

- `python -m pytest backend/tests`
- `python scripts/smoke_test.py`
- `cd frontend && CI=true npm test -- --watchAll=false`

## Data / Inputs / Assumptions

- Inputs are user-uploaded local image or video files sent through the web UI or API.
- Supported image extensions: `png`, `jpg`, `jpeg`, `gif`
- Supported video extensions: `mp4`, `avi`, `mov`, `mkv`
- No training dataset is committed in this repository.
- No benchmark dataset or evaluation corpus is committed in this repository.
- The repo assumes models can be downloaded locally from Hugging Face on first real inference.
- Generated uploads are local artifacts; they are not treated as durable storage.
- The visible UI supports `en`, `es`, `fr`, `de`, and `zh` as target languages.

## Methodology / Approach

The implementation uses pretrained components rather than model training:

- BLIP generates the initial caption from an RGB image.
- Videos are reduced to sampled frames instead of processed with a dedicated temporal video-captioning model.
- Translation is applied after caption generation rather than using a multilingual captioning model end to end.
- Tests and smoke checks mock inference so API behavior can be verified without heavyweight downloads or GPU requirements.

This keeps the project focused on end-to-end inference application design rather than research benchmarking.

## Evaluation / Results

- Real inference latency depends on the local machine, model download state, and whether inference runs on CPU or GPU.
- This repo does not currently publish benchmarked latency numbers.

What is available:

- backend API tests for successful image/video requests and missing-file validation
- a smoke test that verifies Flask app creation and mocked endpoint wiring
- a frontend test that verifies the app shell renders and the language selector updates from `en` to `fr`
- checked-in qualitative examples in [`results/qualitative_examples.md`](./results/qualitative_examples.md)

Interpretation:

- The current evidence is strongest on application wiring, API behavior, local reproducibility, and CI-backed checks.
- Model-quality evaluation is intentionally limited in this repo because the project focuses on wrapping pretrained captioning models into a usable local inference app rather than benchmarking model accuracy.

## Demo / Example Outputs

The current repo includes a lightweight qualitative examples file in `results/` that documents API response shapes, representative mocked outputs, and known limitations.

The repository does include example response shapes from the tested API paths:

```json
{
  "caption": "caption:fr"
}
```

```json
{
  "captions": [
    {
      "frame": 0,
      "caption": "video-caption:es"
    }
  ]
}
```

`results/qualitative_examples.md` documents the current qualitative evidence available in the repo. It is intentionally scoped to app behavior and API output format rather than model-quality benchmarking.

## Quickstart

### 1. Backend setup

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Frontend setup

From the repo root:

```bash
cd frontend
npm install
```

### 3. Environment variables

Minimal local configuration is documented in [`.env.example`](./.env.example):

```env
BACKEND_HOST=127.0.0.1
BACKEND_PORT=5000
BACKEND_DEBUG=false
BACKEND_UPLOAD_DIR=uploads
REACT_APP_API_BASE_URL=http://127.0.0.1:5000
```

### 4. Run the app

Backend, from the repo root:

```bash
python -m backend.app
```

Frontend, from `frontend/`:

```bash
npm start
```

First real inference note:

- The first real caption request can trigger model downloads and local model initialization.

### 5. Run tests

Backend tests, from the repo root:

```bash
python -m pytest backend/tests
```

Backend smoke test, from the repo root:

```bash
python scripts/smoke_test.py
```

Frontend test, from `frontend/`:

```bash
CI=true npm test -- --watchAll=false
```

## Repository Structure

```text
image-and-video-caption-generator-main/
├── backend/                  # Flask API, model integration, backend tests
├── docs/                     # README standard and portfolio/supporting notes
├── frontend/                 # React application and frontend tests
├── results/                  # Lightweight qualitative examples
├── scripts/                  # Standalone smoke-test entry point
├── assets/                   # Public demo assets such as screenshots or GIFs
├── .github/workflows/        # GitHub Actions CI
├── .env.example              # Minimal local configuration
├── README.md                 # Public project overview
└── LICENSE
```

## What This Repository Shows / Ownership

This repository is presented as project-owned work visible in this repo, with claims limited to the checked-in implementation and documentation.

The visible work includes:

- React UI for image/video uploads, previews, loading state, and caption display
- Flask API routes for image and video caption generation
- BLIP and MarianMT integration for captioning and translation
- environment-based local configuration
- mocked backend tests, a smoke test, frontend UI test, and CI wiring

This project uses pretrained open-source model families through Hugging Face. The repository does not claim ownership of the underlying BLIP or MarianMT models.

The focus of this repo is the end-to-end application flow: frontend upload, API request handling, model-backed caption generation, optional translation, smoke testing, and lightweight CI.

## Design Decisions and Tradeoffs

| Decision | Why | Tradeoff / Alternative |
|---|---|---|
| Flask + React split | Makes the frontend/API boundary explicit and easier to discuss in interviews | More local setup than a single-script demo |
| Lazy model loading | Keeps imports and tests lightweight until real inference is needed | First request can be slower |
| Frame sampling for video | Simple way to extend image captioning logic to video inputs | Not full temporal video understanding |
| MarianMT post-translation | Reuses English captioning path with optional multilingual output | Translation quality can drift from original wording |
| Mocked tests and smoke path | Makes CI and local verification realistic without model downloads | Does not validate real caption quality or performance |
| Local upload directories | Keeps the app self-contained and easy to run | No durable storage, cleanup policy, or hosted file handling |

## Limitations / Honest Scope

- This is a local prototype, not a verified production deployment.
- The repo does not include benchmark metrics, evaluation datasets, or latency measurements.
- Video support is frame-sampling-based and does not model temporal context deeply.
- Real caption quality depends on the pretrained models and local runtime environment.
- The checked-in qualitative examples document API response shapes and mocked outputs from test paths; they are not presented as model-quality evaluation.
- There is no dedicated health-check endpoint, authentication layer, persistent database, or observability stack.

Claim boundary:

This project demonstrates a small end-to-end multimodal inference app with local reproducibility and lightweight verification, but it does not claim production readiness, real-user adoption, or measured model-performance gains.

## Future Improvements

- Add verified UI screenshots or a short demo GIF in `assets/`
- Add a small set of real caption examples from a verified local inference run
- Expand backend validation coverage for invalid file types and error paths
- Add broader frontend interaction tests around request success and failure states
- Document real local latency and first-run model download behavior
- Explore stronger video summarization or temporal modeling beyond frame sampling

## Skills Demonstrated

### AI / ML

- integrating pretrained multimodal inference models into an application workflow
- image caption generation with BLIP
- post-generation translation with MarianMT
- simple video frame sampling as a pragmatic approximation for video captioning

### Engineering / Systems

- API design through Flask routes and JSON responses
- environment-driven local configuration
- file upload validation and local artifact handling
- testable service boundaries via injected mock caption services
- CI setup with separate backend and frontend jobs

### Product / Application Design

- translating model inference into a user-facing workflow
- handling image and video flows separately in the UI
- exposing limitations and scope boundaries clearly for reviewers and interview discussion

### Verification / Developer Experience

- backend endpoint testing with pytest
- frontend UI testing with React Testing Library
- smoke-test scripting for fast local verification
- reproducible setup instructions for a two-part frontend/backend app
