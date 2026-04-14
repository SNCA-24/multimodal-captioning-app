from io import BytesIO
from types import SimpleNamespace

import pytest

from backend.app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app()
    app.config.update(
        TESTING=True,
        IMAGE_UPLOAD_DIR=tmp_path / "images",
        VIDEO_UPLOAD_DIR=tmp_path / "videos",
        CAPTION_GENERATOR=SimpleNamespace(
            generate_caption=lambda image_path, language="en": f"caption:{language}",
            generate_captions_for_video=lambda video_path, language="en": [
                {"frame": 0, "caption": f"video-caption:{language}"}
            ],
        ),
    )

    with app.test_client() as test_client:
        yield test_client


def test_generate_image_caption_success(client):
    response = client.post(
        "/api/generate-image-caption",
        data={
            "language": "fr",
            "file": (BytesIO(b"fake-image"), "sample.jpg"),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.get_json() == {"caption": "caption:fr"}


def test_generate_image_caption_missing_file_returns_400(client):
    response = client.post(
        "/api/generate-image-caption",
        data={"language": "en"},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "No file part in the request."}


def test_generate_video_caption_success(client):
    response = client.post(
        "/api/generate-video-caption",
        data={
            "language": "es",
            "file": (BytesIO(b"fake-video"), "clip.mp4"),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "captions": [{"frame": 0, "caption": "video-caption:es"}]
    }
