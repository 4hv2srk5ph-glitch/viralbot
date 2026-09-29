from flask import Blueprint, jsonify, request, session
from pathlib import Path
from job_queue import create_job, list_jobs
from youtube_service import upload_video

api = Blueprint("api", __name__)

@api.get("/api/status")
def status():
    return jsonify({
        "durum": "Çevrimiçi",
        "surum": "MVP-2",
        "youtube": "google_credentials" in session
    })

@api.get("/api/jobs")
def jobs():
    return jsonify(list_jobs())

@api.post("/api/create-job")
def new_job():
    data = request.get_json(silent=True) or {}
    return jsonify(create_job(data.get("topic", "Günün viral konusu")))

@api.post("/api/upload")
def upload():
    if "google_credentials" not in session:
        return jsonify({
            "error": "Önce YouTube hesabını bağla.",
            "connect_url": "/oauth/login"
        }), 401

    video = request.files.get("video")
    if not video:
        return jsonify({"error": "Video seçilmedi"}), 400

    title = (request.form.get("title") or "Yeni Shorts").strip()
    description = request.form.get("description") or ""
    privacy = request.form.get("privacy") or "private"

    Path("uploads").mkdir(exist_ok=True)
    filename = Path(video.filename or "video.mp4").name
    path = Path("uploads") / filename
    video.save(path)

    try:
        video_id = upload_video(
            session["google_credentials"],
            str(path),
            title,
            description,
            ["shorts"],
            privacy,
        )
        return jsonify({
            "status": "uploaded",
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        })
    except Exception as exc:
        return jsonify({"error": f"YouTube yükleme hatası: {exc}"}), 502
    finally:
        try:
            path.unlink(missing_ok=True)
        except Exception:
            pass
