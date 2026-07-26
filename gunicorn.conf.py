"""Gunicorn configuration.

The port is read here rather than passed on the command line, so the start
command needs no shell expansion of $PORT. That keeps the app reachable no
matter how the platform invokes it.
"""

import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = int(os.environ.get("GUNICORN_THREADS", "4"))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "60"))
graceful_timeout = 30
keepalive = 5
accesslog = "-"
errorlog = "-"
