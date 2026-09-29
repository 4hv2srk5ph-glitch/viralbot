import os
from flask import Flask, render_template
from routes import api
from oauth import oauth

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET")
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024

app.register_blueprint(api)
app.register_blueprint(oauth)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
