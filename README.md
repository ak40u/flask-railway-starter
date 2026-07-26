# Flask starter for Railway

A minimal Flask app that deploys on Railway without hand-holding: pinned Python,
a current gunicorn, an explicit bind, and a health check.

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/flask-railway-starter)

## What's in here

| File | Why it exists |
|------|---------------|
| `main.py` | The app: a landing page, `/api/info`, and `/health`. |
| `gunicorn.conf.py` | Binds to `0.0.0.0:$PORT` in Python, so the start command needs no shell expansion. |
| `requirements.txt` | `Flask~=3.1.3`, `gunicorn~=26.0.0` — patch updates, no surprise majors. |
| `.python-version` | Pins Python 3.13 so a platform default bump can't change the runtime under you. |
| `railway.json` | Nixpacks build, `gunicorn main:app`, health check on `/health`. |

## Why the pins matter

The widely used Flask starter on Railway pins `gunicorn==20.0.4`. That version imports
`pkg_resources`, which Python 3.12 no longer provides in a fresh virtualenv. When the
builder's default Python moved to 3.12, the container started crash-looping:

```
File "/opt/venv/lib/python3.12/site-packages/gunicorn/util.py", line 26, in <module>
    import pkg_resources
ModuleNotFoundError: No module named 'pkg_resources'
```

Two things prevent that here: gunicorn 26 (which no longer imports `pkg_resources`) and
a pinned `.python-version`, so the runtime only changes when you change it.

## Run it locally

```bash
pip install -r requirements.txt
python main.py          # http://localhost:8080
```

Or the way production runs it:

```bash
gunicorn main:app       # reads gunicorn.conf.py
```

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `PORT` | `8080` | Set by Railway. |
| `WEB_CONCURRENCY` | `2` | Gunicorn worker processes. |
| `GUNICORN_THREADS` | `4` | Threads per worker. |
| `GUNICORN_TIMEOUT` | `60` | Worker timeout, seconds. |

## License

MIT
