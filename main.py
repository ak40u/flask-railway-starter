import os
import platform

from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.get("/")
def index():
    return render_template(
        "index.html",
        python_version=platform.python_version(),
        flask_version=_flask_version(),
    )


@app.get("/api/info")
def info():
    """Small JSON endpoint, handy for checking the app from the command line."""
    return jsonify(
        service="flask-railway-starter",
        python=platform.python_version(),
        flask=_flask_version(),
    )


@app.get("/health")
def health():
    """Railway calls this before a new deployment replaces the old one."""
    return jsonify(status="ok"), 200


def _flask_version():
    from importlib.metadata import version

    return version("flask")


if __name__ == "__main__":
    # Local development only. In production gunicorn serves the app,
    # configured by gunicorn.conf.py.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
