# Image and Video Caption Generator
Compact multimodal inference app with a React frontend and Flask backend for image captioning, video frame captioning, and optional translation.

## Why this project matters
This repo is a useful supporting MLE portfolio project because it shows more than a notebook demo:
- a user-facing frontend/backend split
- model inference behind HTTP endpoints
- multimodal handling for images and videos
- lightweight reproducibility work for local setup and smoke testing

It is intentionally small. The value is in the end-to-end inference flow and the repo discipline around it, not in a large platform or training pipeline.

## What it does
- Generates a caption for an uploaded image.
- Samples frames from an uploaded video and generates captions for those frames.
- Optionally translates captions from English into supported target languages.
- Uses a React UI for uploads and result display, with a Flask API handling inference requests.

## Architecture / workflow
High-level flow:

```text
React frontend
  -> POST image/video + language
  -> Flask API
  -> caption service
     -> BLIP image captioning
     -> optional MarianMT translation
  -> JSON response
  -> rendered caption(s) in the UI
```

Current backend endpoints:
- `/api/generate-image-caption`
- `/api/generate-video-caption`

Current inference path:
- Images are captioned directly with BLIP.
- Videos are sampled at roughly one frame per second based on FPS, and each sampled frame is captioned individually.
- Translation is only applied when the requested language is not English.

## Tech stack
- Frontend: React, Create React App runtime, `react-spinners`
- Backend: Flask, Flask-CORS
- Model layer: Hugging Face Transformers, `Salesforce/blip-image-captioning-base`, MarianMT translation models
- Media handling: Pillow, OpenCV
- Reproducibility/testing: pinned Python dependencies, standalone smoke test, Flask test client via the smoke-test path

## Quickstart
### Backend setup
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

### Frontend setup
From the repo root:

```bash
cd frontend
npm install
```

### Environment variables
Minimal environment variables are listed in [`.env.example`](./.env.example).

Current variables:
- `BACKEND_HOST`
- `BACKEND_PORT`
- `BACKEND_DEBUG`
- `BACKEND_UPLOAD_DIR`
- `REACT_APP_API_BASE_URL`

Defaults:
- backend host: `127.0.0.1`
- backend port: `5000`
- backend debug: `false`
- upload directory: `uploads`
- frontend API base URL: `http://127.0.0.1:5000`

### Supported run commands
Backend, from the repo root:

```bash
python -m backend.app
```

Frontend, from `frontend/`:

```bash
npm start
```

First real inference note:
- On a fresh machine, the first real caption request may trigger Hugging Face model downloads and local model loading before a response is returned.

## Smoke test
Supported smoke-test command, from the repo root:

```bash
python scripts/smoke_test.py
```

What it validates:
- Flask app creation
- image endpoint wiring
- video endpoint wiring
- missing-file validation behavior
- upload-path handling through app config

What it does not validate:
- real BLIP or MarianMT inference
- model downloads
- frontend rendering
- end-to-end browser behavior

The smoke test uses mocked inference so it can run without network-dependent model downloads.

## API behavior
### `POST /api/generate-image-caption`
- Input: multipart form with `file` and optional `language`
- Accepted file types: `png`, `jpg`, `jpeg`, `gif`
- Success response: JSON with a single `caption` field
- Validation failures return `400` with an `error` message

### `POST /api/generate-video-caption`
- Input: multipart form with `file` and optional `language`
- Accepted file types: `mp4`, `avi`, `mov`, `mkv`
- Success response: JSON with a `captions` list containing frame/caption pairs
- Validation failures return `400` with an `error` message

## Results / qualitative examples
Current checked-in examples are documented in [`results/qualitative_examples.md`](./results/qualitative_examples.md).

Important note:
- The current file is intentionally lightweight and honest.
- It records checked-in API response examples and known weak spots.
- It is not a benchmark report and it is not presented as full evaluation.

This repo is not presented as a benchmark project. The right bar here is clear qualitative examples and honest limitations, not fabricated metrics.

## Limitations and tradeoffs
- Video handling is simple: frames are sampled at roughly one frame per second, so this is not a full video-understanding system.
- Caption quality is model-dependent and may be weak on dense scenes, ambiguous actions, or unusual inputs.
- Translation quality is also model-dependent and may drift from the original caption wording.
- First-run inference can be slow because model weights may need to be downloaded and loaded locally.
- Real inference depends on the local machine and installed ML stack. The smoke test avoids those requirements by mocking inference.
- CPU execution is supported by the current code path; faster inference may depend on the local environment, but GPU-specific runtime behavior is not documented in this repo yet.

## Repo structure
```text
image-and-video-caption-generator/
├── README.md                  # Project overview and run path
├── .env.example               # Minimal local configuration variables
├── .github/workflows/         # Lightweight CI for backend and frontend checks
├── backend/                   # Flask API and caption generation logic
├── frontend/                  # React UI for uploads and results
├── scripts/                   # Standalone smoke-test entry path
├── assets/                    # Public demo assets such as screenshots
└── results/                   # Lightweight qualitative examples
```

## Testing and reproducibility
Current state:
- backend dependencies are pinned in [`backend/requirements.txt`](./backend/requirements.txt)
- frontend API configuration is no longer hardcoded inside the component logic
- the supported backend run path is `python -m backend.app`
- the supported smoke-test path is `python scripts/smoke_test.py`
- backend API coverage exists in [`backend/tests/test_api.py`](./backend/tests/test_api.py) with mocked inference
- frontend UI coverage exists in [`frontend/src/App.test.js`](./frontend/src/App.test.js)
- a basic GitHub Actions workflow exists in [`.github/workflows/ci.yml`](./.github/workflows/ci.yml)

Still missing:
- checked-in screenshots or a short demo GIF
- broader backend/frontend test coverage beyond the current narrow checks
- local verification notes for real frontend execution and warm-run inference latency

## Future improvements
- Add a small set of qualitative examples in `results/`
- Add a few more narrow endpoint/UI tests only where they improve confidence materially
- Improve video summarization beyond simple frame sampling
- Document real local latency and first-run model download behavior
