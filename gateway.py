"""
WeCom AI Gateway
================
Exposes the private database (transformed-data/chunks.json) over HTTP so that
WeCom's cloud servers can reach it through a Cloudflare Tunnel:

    WeCom Cloud -> https://xxxx.trycloudflare.com -> this machine -> this server -> chunks.json

Start it with start_server.bat, or manually:
    uvicorn gateway:app --host 0.0.0.0 --port 8000

Optional security: set the environment variable GATEWAY_API_KEY before starting.
If set, every request must include the header  X-API-Key: <that value>.
If not set, the server is open (fine for local testing, NOT for a real tunnel).
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# ---------------------------------------------------------------------------
# Logging: every message is written to the screen AND to logs/gateway.log
# ---------------------------------------------------------------------------
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/gateway.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("gateway")

DATA_FILE = Path("transformed-data/chunks.json")
API_KEY = os.environ.get("GATEWAY_API_KEY")  # optional

app = FastAPI(title="WeCom AI Gateway")


def load_chunks() -> list:
    """Read the private database fresh from disk on every request,
    so re-running ingest.py is picked up without restarting the server."""
    if not DATA_FILE.exists():
        log.error("[PROBLEM] The database file %s is missing. "
                  "Run 'python ingest.py' first to create it.", DATA_FILE)
        return []
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


@app.middleware("http")
async def log_every_request(request: Request, call_next):
    """Logs who called us, what they asked for, and whether it worked."""
    caller = request.client.host if request.client else "unknown"
    log.info("[REQUEST]  A computer at address %s is asking for: %s %s",
             caller, request.method, request.url.path)

    if API_KEY and request.headers.get("X-API-Key") != API_KEY:
        log.info("[BLOCKED]  The caller did not provide the correct API key. Request denied.")
        return JSONResponse(status_code=401, content={"error": "Missing or wrong X-API-Key header."})

    response = await call_next(request)
    if response.status_code == 200:
        log.info("[SUCCESS]  The request worked. Data was sent back to the caller.")
    else:
        log.info("[PROBLEM]  The request failed with code %s.", response.status_code)
    return response


@app.get("/")
def health():
    """Health check: lets anyone confirm the server is alive."""
    chunks = load_chunks()
    return {
        "status": "ok",
        "message": "The WeCom AI Gateway is running and can see the private database.",
        "database_file": str(DATA_FILE),
        "chunks_available": len(chunks),
        "server_time": datetime.now().isoformat(timespec="seconds"),
    }


@app.get("/chunks")
def all_chunks():
    """Return the entire private database."""
    chunks = load_chunks()
    log.info("[DATABASE] Sending all %d chunks from the private database.", len(chunks))
    return {"count": len(chunks), "chunks": chunks}


@app.get("/search")
def search(q: str = ""):
    """Keyword search. Example: /search?q=orca
    This is the endpoint the WeCom AI agent should call as its 'tool'."""
    chunks = load_chunks()
    if not q:
        log.info("[SEARCH]   The caller searched with an empty query, returning nothing.")
        return {"query": q, "count": 0, "results": []}

    results = [c for c in chunks if q.lower() in c["content"].lower()]
    log.info("[SEARCH]   Looked for the word '%s' in %d chunks and found %d match(es).",
             q, len(chunks), len(results))
    return {"query": q, "count": len(results), "results": results}


log.info("=" * 60)
log.info("Gateway code loaded. Waiting for the server to start...")
if API_KEY:
    log.info("Security is ON: callers must send the X-API-Key header.")
else:
    log.info("Security is OFF: anyone with the URL can read the data "
             "(set GATEWAY_API_KEY to turn security on).")
log.info("=" * 60)
