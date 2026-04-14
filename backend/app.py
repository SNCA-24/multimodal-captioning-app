import os
from pathlib import Path

from flask import Flask, current_app, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_UPLOAD_ROOT = REPO_ROOT / "uploads"


def _get_env_flag(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _has_allowed_extension(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def _get_caption_service():
    caption_service = current_app.config.get("CAPTION_GENERATOR")
    if caption_service is None:
        from backend.models import caption_generator

        caption_service = caption_generator
        current_app.config["CAPTION_GENERATOR"] = caption_service
    return caption_service


def create_app():
    app = Flask(__name__)
    CORS(app)

    upload_root = Path(os.getenv("BACKEND_UPLOAD_DIR", DEFAULT_UPLOAD_ROOT))
    app.config.update(
        HOST=os.getenv("BACKEND_HOST", "127.0.0.1"),
        PORT=int(os.getenv("BACKEND_PORT", "5000")),
        DEBUG=_get_env_flag("BACKEND_DEBUG", False),
        UPLOAD_ROOT=upload_root,
        IMAGE_UPLOAD_DIR=upload_root / "images",
        VIDEO_UPLOAD_DIR=upload_root / "videos",
        CAPTION_GENERATOR=None,
    )

    register_routes(app)
    return app


def register_routes(app):
    @app.route("/api/generate-image-caption", methods=["POST"])
    def generate_image_caption():
        language = request.form.get("language", "en")
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request."}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected."}), 400

        if not file or not _has_allowed_extension(file.filename, ALLOWED_EXTENSIONS):
            return jsonify({"error": "Invalid file type."}), 400

        filename = secure_filename(file.filename)
        image_dir = current_app.config["IMAGE_UPLOAD_DIR"]
        image_dir.mkdir(parents=True, exist_ok=True)
        filepath = image_dir / filename
        file.save(str(filepath))

        caption_service = _get_caption_service()
        caption = caption_service.generate_caption(str(filepath), language=language)
        return jsonify({"caption": caption}), 200

    @app.route("/api/generate-video-caption", methods=["POST"])
    def generate_video_caption():
        language = request.form.get("language", "en")
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request."}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected."}), 400

        if not file or not _has_allowed_extension(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            return jsonify({"error": "Invalid file type."}), 400

        filename = secure_filename(file.filename)
        video_dir = current_app.config["VIDEO_UPLOAD_DIR"]
        video_dir.mkdir(parents=True, exist_ok=True)
        filepath = video_dir / filename
        file.save(str(filepath))

        caption_service = _get_caption_service()
        captions = caption_service.generate_captions_for_video(str(filepath), language=language)
        return jsonify({"captions": captions}), 200


app = create_app()


if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"],
    )
