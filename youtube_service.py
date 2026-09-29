from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def credentials_from_session(data):
    if not data:
        raise RuntimeError("YouTube hesabı bağlı değil.")
    return Credentials(
        token=data["token"],
        refresh_token=data.get("refresh_token"),
        token_uri=data["token_uri"],
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        scopes=data.get("scopes"),
    )

def upload_video(credentials_data, video_path, title, description="", tags=None,
                 privacy="private"):
    creds = credentials_from_session(credentials_data)
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": (tags or [])[:500],
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": privacy,
        },
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(video_path, mimetype="video/*", resumable=True),
    )

    response = None
    while response is None:
        _, response = request.next_chunk()

    return response["id"]
