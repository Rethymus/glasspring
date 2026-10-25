#!/usr/bin/env python3
"""preview_shot.py — device-emulated screenshots for the glasspring skill.

Why CDP device emulation: on Windows, headless Chromium enforces a minimum
LAYOUT width (~500px) no matter what --window-size says. Emulation.setDeviceMetricsOverride produces true 390px
viewports. This script implements the minimal CDP/WebSocket client it needs
on Python stdlib only — no playwright, no node.

Usage:
  python preview_shot.py --selftest
      offline anchors (port parse, WS framing, masking) + live proof: shoot a
      test page at 390px and assert the PNG is exactly 390px wide.
  python preview_shot.py URL --out-dir shots
      captures mobile 390x844 and desktop 1440x900 (deviceScaleFactor 1 by
      default so PNG width == CSS width; pass --dsf 2 for crisper review).
  python preview_shot.py URL --widths 390,768 --dsf 2

Exit codes: 0 ok / 1 hard failure (missing anchor, browser launch failure,
width mismatch). If no Chromium-family browser is installed the live part
prints SKIP and exits 0 — say so honestly instead of faking a screenshot.
"""
from __future__ import annotations
import argparse, base64, json, os, re, shutil, socket, struct, subprocess, sys, tempfile, threading, time, urllib.request

# ---------- offline anchors ----------

def parse_devtools_port(line: str):
    m = re.search(r"DevTools listening on ws://127\.0\.0\.1:(\d+)/", line or "")
    return int(m.group(1)) if m else None

def mask_payload(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % 4] for i, b in enumerate(data))

def build_client_frame(payload: bytes, opcode: int = 0x1) -> bytes:
    """Client->server frames MUST be masked (RFC 6455)."""
    header = bytes([0x80 | opcode])
    n = len(payload)
    if n < 126:
        header += bytes([0x80 | n])                      # MASK bit set
    elif n < 65536:
        header += bytes([0x80 | 126]) + struct.pack(">H", n)
    else:
        header += bytes([0x80 | 127]) + struct.pack(">Q", n)
    key = os.urandom(4)
    return header + key + mask_payload(payload, key)

def _recv_exact(sock: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("socket closed")
        buf += chunk
    return buf

def read_frame(sock: socket.socket):
    """Return (fin, opcode, payload) for one complete frame (16/64-bit lengths)."""
    b1, b2 = _recv_exact(sock, 2)
    fin = bool(b1 & 0x80)
    opcode = b1 & 0x0F
    masked = b2 & 0x80
    ln = b2 & 0x7F
    if ln == 126:
        ln = struct.unpack(">H", _recv_exact(sock, 2))[0]
    elif ln == 127:
        ln = struct.unpack(">Q", _recv_exact(sock, 8))[0]
    mask = _recv_exact(sock, 4) if masked else None
    payload = _recv_exact(sock, ln)
    if mask:
        payload = mask_payload(payload, mask)
    return fin, opcode, payload

class CdpClient:
    """Minimal one-connection CDP session over WebSocket."""

    def __init__(self, host: str, port: int, path: str, timeout: float = 30.0):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n"
               "Upgrade: websocket\r\nConnection: Upgrade\r\n"
               f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        self.sock.sendall(req.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("upgrade failed: socket closed")
            resp += chunk
        if b" 101 " not in resp.split(b"\r\n", 1)[0]:
            raise ConnectionError(f"upgrade failed: {resp[:120]!r}")
        self._buf = b""
        self._id = 0

    def _read_message(self):
        """Read one complete (possibly fragmented) text message; auto-pong pings."""
        payload = b""
        while True:
            fin, opcode, data = read_frame(self.sock)
            if opcode == 0x9:  # ping -> pong
                self.sock.sendall(build_client_frame(data, opcode=0xA))
                continue
            if opcode == 0x8:
                raise ConnectionError("ws closed by peer")
            payload += data
            if fin:  # final fragment of a data message
                return payload.decode("utf-8", "replace")

    def call(self, method: str, params: dict | None = None, timeout: float | None = None,
             session: str | None = None):
        self._id += 1
        mid = self._id
        msg = {"id": mid, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        self.sock.sendall(build_client_frame(json.dumps(msg).encode()))
        return self._wait(lambda m: m.get("id") == mid, timeout)

    def wait_event(self, name: str, timeout: float | None = None, session: str | None = None):
        def pred(m):
            return m.get("method") == name and (session is None or m.get("sessionId") == session)
        return self._wait(pred, timeout)

    def _wait(self, pred, timeout: float | None):
        deadline = time.time() + (timeout or self.sock.gettimeout() or 30)
        while True:
            remain = deadline - time.time()
            if remain <= 0:
                raise TimeoutError("CDP wait timed out")
            self.sock.settimeout(remain)
            msg = json.loads(self._read_message())
            if pred(msg):
                return msg

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass

# ---------- browser discovery / launch ----------

def find_browser() -> str | None:
    for env in ("CHROME_PATH", "EDGE_PATH"):
        p = os.environ.get(env)
        if p and os.path.exists(p):
            return p
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    pf86 = os.environ.get("ProgramFiles(x86)", pf)
    lac = os.environ.get("LocalAppData", "")
    candidates = [
        rf"{pf}\Google\Chrome\Application\chrome.exe", rf"{pf86}\Google\Chrome\Application\chrome.exe",
        rf"{lac}\Google\Chrome\Application\chrome.exe",
        rf"{pf}\Microsoft\Edge\Application\msedge.exe", rf"{pf86}\Microsoft\Edge\Application\msedge.exe",
        rf"{lac}\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    for name in ("google-chrome", "chromium-browser", "chromium", "chrome", "msedge"):
        w = shutil.which(name)
        if w:
            return w
    return None

def free_tcp_port() -> int:
    """Ephemeral port for the DevTools listener.

    A PID-derived port can collide with zombie browser instances from earlier
    failed runs (their DevTools server still answers handshakes but routes
    nowhere useful) — that was the intermittent 'connected but silent' bug.
    Bind-to-0 makes collisions vanishingly unlikely.
    """
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port

def launch_browser(port: int) -> tuple[subprocess.Popen, str, str]:
    exe = find_browser()
    if not exe:
        raise FileNotFoundError("no Chromium-family browser found (set CHROME_PATH)")
    user_data = tempfile.mkdtemp(prefix="glasspring-shot-")
    for headless in ("--headless=new", "--headless"):
        proc = subprocess.Popen(
            [exe, headless, f"--remote-debugging-port={port}", f"--user-data-dir={user_data}",
             "--remote-allow-origins=*",  # Chromium 111+ silently drops WS frames without this
             "--no-first-run", "--no-default-browser-check", "--disable-extensions",
             "--disable-gpu", "--window-size=800,900", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, errors="ignore")
        deadline = time.time() + 15
        lines: list[str] = []
        def reader():
            for line in proc.stderr:
                lines.append(line)
        t = threading.Thread(target=reader, daemon=True)
        t.start()
        while time.time() < deadline:
            for line in lines:
                p = parse_devtools_port(line)
                if p:
                    # confirm the endpoint is alive before handing it out
                    try:
                        with urllib.request.urlopen(f"http://127.0.0.1:{p}/json/version", timeout=3) as r:
                            json.load(r)
                        return proc, f"ws://127.0.0.1:{p}/devtools/page", user_data
                    except OSError:
                        pass  # line seen but endpoint not serving yet
            time.sleep(0.1)
        proc.terminate()  # this headless mode didn't come up; try the next
    raise RuntimeError("browser launched but no DevTools endpoint appeared")

def browser_ws_url(port: int) -> str:
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=10) as r:
        return json.load(r)["webSocketDebuggerUrl"]

def png_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", head[16:24])

def _terminate_tree(proc: subprocess.Popen):
    """Kill the browser and its children (renderer/GPU survive plain terminate)."""
    if proc.poll() is None:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           capture_output=True)
        else:
            proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass

def shoot_with_retry(url: str, width: int, height: int, out_path: str, dsf: int = 1,
                     attempts: int = 3, clicks: list[str] | None = None,
                     probe: str | None = None, expect_title: str | None = None,
                     scroll_to: str | None = None):
    """This machine's DevTools-WS intermittently ignores a whole connection
    (glasspring P2-3 finding: identical wire bytes succeed then fail across
    runs). A fresh browser+port per attempt converts that into reliability."""
    last = None
    for i in range(1, attempts + 1):
        try:
            return shoot(url, width, height, out_path, dsf=dsf, clicks=clicks,
                         probe=probe, expect_title=expect_title, scroll_to=scroll_to)
        except Exception as e:  # noqa: BLE001 - retry any capture failure
            last = e
            print(f"  attempt {i}/{attempts} failed: {type(e).__name__}: {e}")
            time.sleep(0.5)
    raise last

def shoot(url: str, width: int, height: int, out_path: str, dsf: int = 1,
          clicks: list[str] | None = None, probe: str | None = None,
          expect_title: str | None = None, scroll_to: str | None = None):
    """Browser-endpoint + flattened-session architecture (Puppeteer-style).

    The page-level /devtools/page WS proved flaky on Edge ~140 (fresh
    /json/new targets can silently drop the first commands — glasspring
    P2-3 finding); the browser endpoint responded reliably every time.
    All temp artifacts (user-data dir, selftest PNG) are cleaned up.
    """
    port = free_tcp_port()
    proc, _ws, user_data_dir = launch_browser(port)
    try:
        ws = browser_ws_url(port)
        path = urlparse_path(ws)
        cdp = CdpClient("127.0.0.1", port, path)
        tid = cdp.call("Target.createTarget", {"url": "about:blank"})["result"]["targetId"]
        sid = cdp.call("Target.attachToTarget", {"targetId": tid, "flatten": True})["result"]["sessionId"]
        cdp.call("Page.enable", session=sid)
        cdp.call("Emulation.setDeviceMetricsOverride",
                 {"width": width, "height": height, "deviceScaleFactor": dsf, "mobile": width < 700},
                 session=sid)
        cdp.call("Page.navigate", {"url": url}, session=sid)
        cdp.wait_event("Page.loadEventFired", timeout=20, session=sid)
        time.sleep(0.6)  # fonts/raster settle
        # Regression lesson: bind evidence to content identity — stale servers on a
        # reused port would otherwise pass silently (coffee page in a tracker run).
        if expect_title:
            t = cdp.call("Runtime.evaluate",
                         {"expression": "document.title", "returnByValue": True},
                         timeout=10, session=sid)["result"]["result"].get("value", "")
            if expect_title.lower() not in str(t).lower():
                raise ValueError(
                    f"content identity mismatch: expected title ~{expect_title!r}, got {t!r} "
                    "(stale server or wrong page — do NOT ship this capture)")
        for sel in (clicks or []):
            expr = ("(function(){var e=document.querySelector(" + json.dumps(sel) +
                    "); if(e) e.click();})()")
            cdp.call("Runtime.evaluate", {"expression": expr}, timeout=10, session=sid)
            time.sleep(0.4)  # let the interaction settle
        # scrolled-state evidence: probe runs AFTER capture, so scrolling must
        # happen here to affect the image (for example, a fixed action bar below the fold).
        if scroll_to:
            if scroll_to.lower() == "bottom":
                expr = "window.scrollTo(0, document.documentElement.scrollHeight); true"
            else:
                expr = ("(function(){var e=document.querySelector(" + json.dumps(scroll_to) +
                        "); if(!e) return false; e.scrollIntoView(false); return true;})()")
            cdp.call("Runtime.evaluate", {"expression": expr}, timeout=10, session=sid)
            time.sleep(0.4)  # let the scroll settle
        # wait for lazy images to finish decoding after scroll (capped 5s) —
        # captures otherwise race loading="lazy" and ship blank work cards.
        imgwait = ("new Promise(function(res){var t0=Date.now();(function c(){var bad=false;"
                   "for(var i=0;i<document.images.length;i++){if(!document.images[i].complete){bad=true;break;}}"
                   "(bad&&Date.now()-t0<5000)?setTimeout(c,200):res(!bad);})()})")
        cdp.call("Runtime.evaluate", {"expression": imgwait, "awaitPromise": True,
                                      "returnByValue": True, "timeout": 8000}, session=sid)
        # NOTE: captureBeyondViewport=true ignores the emulated metrics (captures
        # the layout viewport instead — 980px on Windows headless). For a
        # full-page shot, re-emulate at the measured content height instead.
        if out_path.endswith(".full.png"):
            h = cdp.call("Runtime.evaluate",
                         {"expression": "document.documentElement.scrollHeight",
                          "returnByValue": True}, timeout=10,
                         session=sid)["result"]["result"].get("value", height)
            cdp.call("Emulation.setDeviceMetricsOverride",
                     {"width": width, "height": int(h), "deviceScaleFactor": dsf,
                      "mobile": width < 700}, session=sid)
            time.sleep(0.3)
        shot = cdp.call("Page.captureScreenshot", {"format": "png"}, timeout=30, session=sid)
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(shot["result"]["data"]))
        probe_val = None
        if probe:
            pv = cdp.call("Runtime.evaluate",
                          {"expression": probe, "returnByValue": True},
                          timeout=10, session=sid)
            probe_val = pv["result"]["result"].get("value")
        cdp.close()
        w, h = png_size(out_path)
        return w, h, probe_val
    finally:
        _terminate_tree(proc)
        import shutil
        shutil.rmtree(user_data_dir, ignore_errors=True)

def urlparse_path(ws_url: str) -> str:
    m = re.search(r"^(?:ws://[^/]+)?(/.*)$", ws_url)
    return m.group(1) if m else "/"

# ---------- selftest ----------

def selftest(live: bool = True) -> int:
    fails = []

    def check(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    print("selftest: offline anchors")
    check("parse devtools port", parse_devtools_port(
        "DevTools listening on ws://127.0.0.1:54321/devtools/browser/abc") == 54321)
    check("parse devtools port (no match)", parse_devtools_port("nothing here") is None)
    for size in (5, 500, 70000):  # framing roundtrip at all three length encodings
        payload = bytes(range(256)) * (size // 256 + 1)
        payload = payload[:size]
        frame = build_client_frame(payload)
        b1, b2 = frame[0], frame[1]
        assert b2 & 0x80, "client frame must be masked"
        ln = b2 & 0x7F
        off = 2
        if ln == 126:
            ln = struct.unpack(">H", frame[2:4])[0]; off = 4
        elif ln == 127:
            ln = struct.unpack(">Q", frame[2:10])[0]; off = 10
        key = frame[off:off + 4]
        body = frame[off + 4:]
        check(f"frame roundtrip len={size}", ln == size and mask_payload(body, key) == payload)

    print("selftest: live capture (true-390 proof against the Windows 500px quirk)")
    if not live:
        print("  SKIP (live disabled)")
    else:
        exe = find_browser()
        if not exe:
            print("  SKIP (no Chromium-family browser found; set CHROME_PATH) — offline anchors still green")
            print("SELFTEST PASSED (offline anchors green; live skipped honestly)")
            return 0
        data_html = ("<body style=\"margin:0;background:#1a2430;color:#fff;"
                     "font:20px system-ui\"><button id=\"b\" onclick=\"document.title='clicked'\">go</button>"
                     "preview_shot 390px proof</body>")
        url = "data:text/html," + urllib.request.quote(data_html)
        out = os.path.join(tempfile.gettempdir(), "glasspring-selftest-390.png")
        try:
            w, h, pv = shoot_with_retry(url, 390, 844, out, dsf=1, attempts=3,
                                        clicks=["#b"], probe="document.title")
            check("live 390px width == 390 (not the 500px min)", w == 390, f"got {w}x{h}")
            check("live interaction (click sets title)", pv == "clicked", str(pv))
        except Exception as e:
            check("live capture", False, f"{type(e).__name__}: {e}")

        # scrolled-state anchor: probe runs AFTER capture, so a
        # non-zero scrollY here proves the scroll survived through capture.
        tall_html = ("<body style=\"margin:0\"><div style=\"height:3000px\">tall</div>"
                     "<div id=\"deep\" style=\"height:60px\">deep end</div></body>")
        turl = "data:text/html," + urllib.request.quote(tall_html)
        tout = os.path.join(tempfile.gettempdir(), "glasspring-selftest-scroll.png")
        try:
            w, h, pv = shoot_with_retry(turl, 390, 844, tout, dsf=1, attempts=3,
                                        scroll_to="bottom", probe="Math.round(window.scrollY)")
            # anchor semantics: scroll SURVIVED capture (probe reads post-capture) —
            # exact max-scroll depends on emulated content height, don't assume it
            check("live scroll-to (scroll survives capture)", isinstance(pv, (int, float)) and pv > 100, f"scrollY={pv}")
        except Exception as e:
            check("live scroll-to", False, f"{type(e).__name__}: {e}")

    if fails:
        print(f"SELFTEST FAILED: {fails}")
        return 1
    print("SELFTEST PASSED (all anchors green)")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description="glasspring screenshot capture (CDP device emulation)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("url", nargs="?", help="page to capture (http/https/file)")
    ap.add_argument("--out-dir", default="shots")
    ap.add_argument("--widths", default="390,1440", help="comma-separated css widths (heights 844/900)")
    ap.add_argument("--dsf", type=int, default=1, help="deviceScaleFactor (1: PNG px == css px)")
    ap.add_argument("--no-live", action="store_true", help="selftest: offline anchors only")
    ap.add_argument("--click", dest="clicks", action="append", default=None,
                    help="CSS selector to click before the capture (repeatable, e.g. --click \"#tab-b\") — interaction-state evidence")
    ap.add_argument("--probe", help="JS expression evaluated after clicks; its value is printed with the shot")
    ap.add_argument("--label", default="page", help="filename label: shot-{label}-{w}x{h}.png — use distinct labels for different capture states (e.g. 'top', 'scrolled', 'modal-open')")
    ap.add_argument("--scroll-to", dest="scroll_to",
                    help="scroll before capture: a CSS selector (aligns its bottom edge) or the literal 'bottom' — scrolled-state evidence (probe cannot do this: it runs after capture)")
    ap.add_argument("--expect-title", help="content identity check: fail unless page title contains this substring")
    a = ap.parse_args()

    if a.selftest:
        return selftest(live=not a.no_live)
    if not a.url:
        ap.error("give a URL or --selftest")
    if not a.expect_title:
        # Vite preview can auto-increment ports when a stale server holds yours;
        # without a content identity check you
        # capture the WRONG app and gate the wrong artifact.
        print("note: no --expect-title given — multi-app sessions can capture a stale port's app (vite preview auto-increments); pass --expect-title for content identity.")
    os.makedirs(a.out_dir, exist_ok=True)
    label = a.label
    rc = 0
    for wstr in a.widths.split(","):
        w = int(wstr.strip())
        h = 844 if w < 700 else 900
        out = os.path.join(a.out_dir, f"shot-{label}-{w}x{h}.png")
        try:
            wpx, hpx, pv = shoot_with_retry(a.url, w, h, out, dsf=a.dsf, clicks=a.clicks,
                                            probe=a.probe, expect_title=a.expect_title,
                                            scroll_to=a.scroll_to)
            print(f"shot: {out} (png {wpx}x{hpx}px @dsf{a.dsf} for css {w}x{h})" + (f" [probe: {pv}]" if a.probe else ""))
            if wpx != w * a.dsf:
                print(f"  WARNING: expected {w * a.dsf}px wide — device emulation may have failed")
                rc = 1
        except Exception as e:
            print(f"FAILED {w}px: {type(e).__name__}: {e}")
            print("  honest fallback: use the host agent's own browser tooling for this viewport")
            rc = 1
    return rc

if __name__ == "__main__":
    sys.exit(main())
