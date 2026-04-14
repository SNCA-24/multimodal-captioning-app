from io import BytesIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app import create_app


def _build_app():
    app = create_app()
    app.config["TESTING"] = True
    temp_dir = TemporaryDirectory()
    upload_root = Path(temp_dir.name)
    app.config.update(
        CAPTION_GENERATOR=SimpleNamespace(
            generate_caption=lambda image_path, language="en": f"mock-caption:{language}",
            generate_captions_for_video=lambda video_path, language="en": [
                {"frame": 0, "caption": f"mock-video-caption:{language}"}
            ],
        ),
        UPLOAD_ROOT=upload_root,
        IMAGE_UPLOAD_DIR=upload_root / "images",
        VIDEO_UPLOAD_DIR=upload_root / "videos",
    )
    return app, temp_dir


def run_smoke_test():
    app, temp_dir = _build_app()
    try:
        client = app.test_client()

        image_response = client.post(
            "/api/generate-image-caption",
            data={
                "language": "es",
                "file": (BytesIO(b"fake-image-bytes"), "sample.jpg"),
            },
            content_type="multipart/form-data",
        )
        assert image_response.status_code == 200, image_response.get_json()
        assert image_response.get_json() == {"caption": "mock-caption:es"}

        validation_response = client.post(
            "/api/generate-image-caption",
            data={"language": "en"},
            content_type="multipart/form-data",
        )
        assert validation_response.status_code == 400, validation_response.get_json()
        assert validation_response.get_json() == {"error": "No file part in the request."}

        video_response = client.post(
            "/api/generate-video-caption",
            data={
                "language": "fr",
                "file": (BytesIO(b"fake-video-bytes"), "sample.mp4"),
            },
            content_type="multipart/form-data",
        )
        assert video_response.status_code == 200, video_response.get_json()
        assert video_response.get_json() == {
            "captions": [{"frame": 0, "caption": "mock-video-caption:fr"}]
        }

        print("Smoke test passed.")
    finally:
        temp_dir.cleanup()


if __name__ == "__main__":
    run_smoke_test()
