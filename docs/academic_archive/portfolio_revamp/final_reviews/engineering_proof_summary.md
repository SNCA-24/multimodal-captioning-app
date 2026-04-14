# Engineering Proof Summary

## 1. Backend tests added
- Added [`backend/tests/test_api.py`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/backend/tests/test_api.py).
- Added a mocked success test for `POST /api/generate-image-caption`.
- Added a mocked validation-failure test for missing image uploads.
- Added a mocked success test for `POST /api/generate-video-caption`.
- Backend tests use `create_app()` plus an injected mock caption service, so they do not require model downloads, GPU access, or network access.

## 2. Frontend test added
- Added [`frontend/src/App.test.js`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/frontend/src/App.test.js).
- The test renders the real app UI instead of checking CRA placeholder content.
- It validates visible headings/upload sections and confirms language selection updates from `en` to `fr`.

## 3. CI workflow added
- Added [`.github/workflows/ci.yml`](/Users/chaitu/Downloads/image-and-video-caption-generator-main/.github/workflows/ci.yml).
- The workflow runs backend dependency installation plus `pytest backend/tests`.
- The workflow runs frontend dependency installation plus `npm test -- --watchAll=false`.
- CI stays narrow: installability and basic behavior only.

## 4. What is now validated
- Flask app creation through the backend test path.
- Successful image-caption API wiring with mocked inference.
- Validation behavior for missing image uploads.
- Successful video-caption API wiring with mocked inference.
- Real frontend UI rendering for the current app shell.
- Real frontend language selector state changes.
- GitHub-side install-and-test checks for both backend and frontend through the CI workflow definition.

## 5. What is still not validated
- Real BLIP and MarianMT inference in automated tests.
- End-to-end browser behavior with live frontend-to-backend requests.
- Real local frontend test execution in this environment, because `npm` is not installed here.
- Performance, warm-run latency, and model download behavior.
- Broader edge cases across file validation, translation behavior, and video processing.

## 6. Risks / cautions
- The backend tests prove API wiring, not model quality or runtime performance.
- The frontend test is intentionally narrow; it improves credibility but is not comprehensive UI coverage.
- The CI workflow assumes standard GitHub-hosted runners with Python and Node setup actions available.
- Real inference still depends on heavyweight ML dependencies and local runtime conditions outside the mocked tests.
