# Setup Guide (no computer knowledge needed)

Goal: let WeCom's AI (which lives on the internet) read our private data
(which lives only on this laptop).

How it works:

```
WeCom Cloud  ->  https://xxxx.trycloudflare.com  ->  this laptop  ->  FastAPI server  ->  private data
```

## Part 1 — Test on this laptop only

1. Double-click **`start_server.bat`**.
   A black window opens. Wait until it says `Application startup complete`.
   **Leave this window open.**
2. Open a second window: press the Windows key, type `powershell`, press Enter.
3. In PowerShell, copy-paste these two lines and press Enter after each:
   ```
   cd "C:\Users\Zachary\Desktop\Projects\wecom\ai_agent_mvp"
   .venv\Scripts\python.exe test_local.py
   ```
4. You should see **ALL TESTS PASSED**. That proves data can be fetched
   from this machine through an IP address — exactly what WeCom will do.

If a LAN test fails but the 127.0.0.1 tests pass, that's just the Windows
Firewall; the tunnel in Part 2 still works.

## Part 2 — Make it reachable by WeCom (Cloudflare Tunnel)

1. Keep the server window from Part 1 open.
2. Double-click **`start_tunnel.bat`**.
   - If it says cloudflared is not installed, follow the instructions it
     prints (one command: `winget install Cloudflare.cloudflared`), then
     double-click it again.
3. In the tunnel window, find the line that looks like:
   ```
   https://lucky-purple-words.trycloudflare.com
   ```
   That is the **public address** of our private database. **Leave this
   window open too.**
4. To prove it works from the internet: open any browser (even on your
   phone, with Wi-Fi off) and visit that address. You should see
   `"status": "ok"`.
5. Give that address to WeCom as the callback / tool URL. The useful
   endpoints are:
   - `https://<tunnel-address>/` — is the server alive?
   - `https://<tunnel-address>/search?q=orca` — search the private data
   - `https://<tunnel-address>/chunks` — get all the private data

Note: the free `trycloudflare.com` address **changes every time** you restart
the tunnel, so re-copy it after each restart.

## Watching what happens

Every request is written in plain English in the server window and saved to
`logs/gateway.log`. Example:

```
2026-06-10 14:02:11 | [REQUEST]  A computer at address 127.0.0.1 is asking for: GET /search
2026-06-10 14:02:11 | [SEARCH]   Looked for the word 'orca' in 1 chunks and found 1 match(es).
2026-06-10 14:02:11 | [SUCCESS]  The request worked. Data was sent back to the caller.
```

## Optional: lock the door

Anyone who knows the tunnel address can read the data. To require a password,
start the server from PowerShell like this instead of using the .bat file:

```
$env:GATEWAY_API_KEY = "choose-a-secret"
.venv\Scripts\python.exe -m uvicorn gateway:app --host 0.0.0.0 --port 8000
```

Then every caller (including WeCom's tool configuration) must send the HTTP
header `X-API-Key: choose-a-secret`.

## Something went wrong?

| What you see | What it means | Fix |
|---|---|---|
| `could not reach the server at all` | The server isn't running | Do Part 1 step 1 first |
| `chunks_available: 0` | The database file is empty/missing | Run `python ingest.py` |
| Tunnel window shows errors | No internet, or cloudflared missing | Check Wi-Fi; reinstall cloudflared |
| Browser says site can't be reached | Tunnel window was closed | Re-run `start_tunnel.bat` (new address!) |
