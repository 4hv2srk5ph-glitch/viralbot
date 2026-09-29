import uuid
from datetime import datetime, timezone
from database import connect

def create_job(topic=""):
    job_id = "JOB-" + uuid.uuid4().hex[:8].upper()
    conn = connect()
    conn.execute("INSERT INTO jobs VALUES (?,?,?,?,?)",
                 (job_id, "Bekliyor", 0, topic, datetime.now(timezone.utc).isoformat()))
    conn.commit(); conn.close()
    return {"id": job_id, "status": "Bekliyor", "progress": 0, "topic": topic}

def update_job(job_id, status, progress):
    conn = connect()
    conn.execute("UPDATE jobs SET status=?, progress=? WHERE id=?",
                 (status, progress, job_id))
    conn.commit(); conn.close()

def list_jobs():
    conn = connect()
    rows = conn.execute("SELECT * FROM jobs ORDER BY created DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
