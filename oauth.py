from flask import Blueprint, redirect, session, request, jsonify
from google_auth_oauthlib.flow import Flow
from config import Config

oauth = Blueprint("oauth", __name__)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def client_config():
    if not Config.GOOGLE_CLIENT_ID or not Config.GOOGLE_CLIENT_SECRET:
        raise RuntimeError("GOOGLE_CLIENT_ID ve GOOGLE_CLIENT_SECRET eksik.")
    return {
        "web": {
            "client_id": Config.GOOGLE_CLIENT_ID,
            "client_secret": Config.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

def redirect_uri():
    return Config.GOOGLE_REDIRECT_URI or request.url_root.rstrip("/") + "/oauth/callback"

@oauth.get("/oauth/login")
def login():
    flow = Flow.from_client_config(
        client_config(), scopes=SCOPES, redirect_uri=redirect_uri()
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    session["oauth_state"] = state
    return redirect(authorization_url)

@oauth.get("/oauth/callback")
def callback():
    state = session.get("oauth_state")
    if not state:
        return "OAuth state bulunamadı.", 400

    flow = Flow.from_client_config(
        client_config(), scopes=SCOPES,
        state=state, redirect_uri=redirect_uri()
    )
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials

    session["google_credentials"] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes or SCOPES),
    }
    session.pop("oauth_state", None)
    return redirect("/")

@oauth.get("/oauth/status")
def oauth_status():
    return jsonify({"connected": "google_credentials" in session})

@oauth.get("/oauth/logout")
def logout():
    session.pop("google_credentials", None)
    return redirect("/")
