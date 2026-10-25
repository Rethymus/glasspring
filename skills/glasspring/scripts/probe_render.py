#!/usr/bin/env python3
"""probe_render.py — render-time composition probe for the glasspring skill.

Catches a bug class where content VISIBILITY is gated behind
an animation completing. A slow device or a fast capture engine sees an empty
focal element. Four passes, each a fresh page load:

  A  natural state   — inject `animation:none` everywhere. Every text-bearing
                       element must be visible. FAIL = the §4a gatekeeper rule
                       ("if the animation never ran, is the block complete?").
  B  frozen at t=0   — inject `animation-play-state:paused`. Reports elements
                       hidden NOW but visible in pass A, with their delay:
                       time-gated content a t=0 capture will miss. WARN-level
                       data, not a verdict — the two-line fix pattern
                       (static carrier + animated enhancement) lives here.
                       Inherently timing-sensitive for delay-less entrances
                       (caught only if the pause lands within their duration);
                       delay-ful animations are always caught.
  C  reduced-motion  — emulate prefers-reduced-motion:reduce. Any element
                       still computing animationName≠none means the media
                       query is unhandled. FAIL = the motion.md contract.
  E  click fingerprint — XIAS dead-contract/invisible-state: declared aria
                       states must change something on click, and a state flip
                       must leave a visible fingerprint (style/geometry).
  D  axe-core a11y   — inject axe-core (CDN) on the REAL page and run WCAG
                       2.x A/AA tags. critical/serious → FAIL; moderate/minor
                       → WARN. CDN unreachable → honest SKIP (passes A-C
                       still cover the motion contracts).

Reuses preview_shot.py's stdlib CDP machinery (no playwright, no node).
Exit codes: 0 pass (warnings allowed) / 1 fail / 2 no browser found.
"""
from __future__ import annotations
import argparse, base64, json, os, sys, tempfile, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preview_shot import (CdpClient, browser_ws_url, find_browser, free_tcp_port,
                          launch_browser, urlparse_path, _terminate_tree)

# ---------- the audit, as page-side JS ----------

# Visibility of a text-bearing element, with the reason it fails.
# "direct text" = own text nodes only, so a wrapper around visible children
# is not flagged. display:none / visibility:hidden / aria-hidden are treated
# as structurally hidden (interaction-gated, not animation-gated) and skipped.
AUDIT_JS = r"""
(function () {
  function ownText(el) {
    var t = '';
    for (var n = el.firstChild; n; n = n.nextSibling)
      if (n.nodeType === 3) t += n.data;
    return t.replace(/\s+/g, '');
  }
  function sel(el) {
    var parts = [], e = el, depth = 0;
    while (e && e.nodeType === 1 && e.tagName !== 'BODY' && depth < 4) {
      var p = e.tagName.toLowerCase();
      if (e.id) { parts.unshift(p + '#' + e.id); break; }
      if (e.classList && e.classList.length) p += '.' + e.classList[0];
      var k = 1, s = e;
      while ((s = s.previousElementSibling)) k++;
      parts.unshift(p + ':nth-of-type(' + k + ')');
      e = e.parentElement; depth++;
    }
    return parts.join('>');
  }
  function ancestorCollapses(el) {
    for (var e = el.parentElement; e && e.tagName !== 'BODY'; e = e.parentElement) {
      var c = getComputedStyle(e);
      if (c.display === 'none') return true; /* getComputedStyle does NOT propagate display:none to descendants — each child computes its own value while having no box (mobile-panel finding 2026-10-23) */
      if (c.visibility === 'hidden') return true;
      if (c.overflow !== 'visible' && (parseFloat(c.maxHeight) === 0 || parseFloat(c.height) === 0)) return true;
    }
    return false;
  }
  function chainOpacity(el) {
    var op = 1, e = el;
    while (e && e.nodeType === 1) {
      op *= parseFloat(getComputedStyle(e).opacity || '1');
      if (op === 0) break;
      e = e.parentElement;
    }
    return op;
  }
  var out = [];
  var els = document.querySelectorAll('body *');
  for (var i = 0; i < els.length; i++) {
    var el = els[i];
    if (el.namespaceURI !== 'http://www.w3.org/1999/xhtml') continue;
    if (!ownText(el)) continue;
    if (el.closest('[aria-hidden="true"]')) continue;
    if (el.closest('.visually-hidden, .sr-only, .visually-hidden-focusable')) continue; /* sr-only live regions: 1x1 clip by spec, read by AT not seen (glass.html finding 2026-10-23) */
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (cs.display === 'contents') continue; /* layout-transparent by design — children carry the box and are audited as their own elements */
    var r = el.getBoundingClientRect();
    var why = null;
    if (chainOpacity(el) === 0) why = 'opacity 0 (chain)';
    else if ((r.width < 2 || r.height < 2) && !ancestorCollapses(el)) why = 'zero box ' + Math.round(r.width) + 'x' + Math.round(r.height);
    else if (r.width < 2 || r.height < 2) continue; /* collapsed-drawer child: structural, not animation-gated (mobile-menu finding 2026-10-23) */
    else if (cs.overflow === 'hidden' &&
             (el.scrollWidth > Math.ceil(r.width) + 1 && parseFloat(cs.maxWidth) === 0 ||
              el.scrollHeight > Math.ceil(r.height) + 1 && r.height < parseFloat(cs.lineHeight || '16'))) {
      var mw = cs.maxWidth !== 'none' ? cs.maxWidth : cs.width;
      why = 'clipped to ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' (overflow hidden, max-w ' + mw + ')';
    }
    if (why) {
      out.push({
        sel: sel(el),
        why: why,
        text: ownText(el).slice(0, 24),
        delay: parseFloat(cs.animationDelay) || 0,
        dur: parseFloat(cs.animationDuration) || 0,
        anim: cs.animationName === 'none' ? '' : cs.animationName
      });
    }
  }
  return out;
})()
"""

NATURAL_CSS = "*,*::before,*::after{animation:none!important;transition:none!important}"
PAUSED_CSS = "*,*::before,*::after{animation-play-state:paused!important}"

AXE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js"

_axe_cache: list[str] = []


def _load_axe_source() -> str | None:
    """Fetch axe source host-side (retry x2, module-cached). In-page CDN
    injection proved network-flaky on this machine (intermittent slow cdnjs
    turned the whole probe flaky); inline textContent has zero page-side
    network. None = unreachable → pass D skips honestly."""
    if _axe_cache:
        return _axe_cache[0]
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(AXE_CDN, timeout=20) as r:
                src = r.read().decode("utf-8")
            if "axe" in src[:2000]:
                _axe_cache.append(src)
                return src
        except OSError:
            if attempt == 1:
                time.sleep(1.0)
    return None


# ---------- one pass ----------

def run_pass(cdp: CdpClient, sid: str, url: str, inject_css: str | None,
             emulate_reduce: bool, settle: float) -> list[dict]:
    """Inject AFTER loadEventFired, before settle: landing within the first
    milliseconds keeps paused-at-t≈0 semantics (delays not yet elapsed), and
    Runtime.evaluate surfaces injection errors instead of eating them at
    document-start, where documentElement does not exist yet."""
    if emulate_reduce:
        cdp.call("Emulation.setEmulatedMedia",
                 {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]},
                 session=sid)
    cdp.call("Page.navigate", {"url": url}, session=sid)
    # Audit the DOM when it is ready; optional remote images need not finish
    # loading before CSS and interaction checks can run.
    cdp.wait_event("Page.domContentEventFired", timeout=20, session=sid)
    if inject_css:
        cdp.call("Runtime.evaluate",
                 {"expression": f"var s=document.createElement('style');"
                                f"s.textContent={json.dumps(inject_css)};"
                                "document.documentElement.appendChild(s);'injected'"},
                 timeout=10, session=sid)
    time.sleep(settle)  # fonts/layout settle
    res = cdp.call("Runtime.evaluate", {"expression": AUDIT_JS, "returnByValue": True},
                   timeout=15, session=sid)
    if "exceptionDetails" in res:
        raise RuntimeError(f"audit JS failed: {res['exceptionDetails'].get('exception', {}).get('description', '?')[:200]}")
    return res["result"]["result"].get("value") or []


def count_animations_under_reduce(cdp: CdpClient, sid: str, url: str, settle: float) -> int:
    """Deterministic reduce-contract check: under emulated prefers-reduced-motion,
    every animated element must compute animationName:none. No timing games."""
    cdp.call("Emulation.setEmulatedMedia",
             {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]}, session=sid)
    cdp.call("Page.navigate", {"url": url}, session=sid)
    cdp.wait_event("Page.domContentEventFired", timeout=20, session=sid)
    time.sleep(settle)
    js = ("(function(){var n=0;var els=document.querySelectorAll('body *');"
          "for(var i=0;i<els.length;i++){var a=getComputedStyle(els[i]).animationName;"
          "if(a&&a!=='none')n++;}"
          "try{var anims=document.getAnimations();"
          "for(var j=0;j<anims.length;j++){var a=anims[j];"
          "if(a.playState==='running'&&typeof CSSTransition!=='undefined'&&!(a instanceof CSSTransition))n++;}"
          "}catch(e){}"
          "return n;})()")
    # getAnimations extension: JS-driven
    # animations (Motion/Framer via WAAPI, GSAP) are invisible to computed
    # animationName — count running WAAPI animations too (CSSTransitions excluded:
    # hover transitions mid-flight are not reduced-motion violations).
    res = cdp.call("Runtime.evaluate", {"expression": js, "returnByValue": True},
                   timeout=15, session=sid)
    return res["result"]["result"].get("value") or 0


def run_axe(cdp: CdpClient, sid: str, url: str, settle: float) -> tuple[list[dict], list[dict]] | None:
    """Pass D: axe-core (WCAG 2.x A/AA tags) on the REAL page — no injection.
    Source is fetched host-side and injected inline (no page-side network).
    Animations are force-disabled first (the a11y tree does not depend on
    motion, and axe's animation-stability wait never settles on infinite
    loops). axe.run is raced against a JS timer so a non-settling axe can
    only cost a SKIP, never a hang. Returns (serious, minor) or None."""
    axe_src = _load_axe_source()
    if axe_src is None:
        return None
    # NOTE: no Page.enable here — probe() already enabled the Page domain, and
    # a mid-flight re-enable discards a pending loadEventFired (renderer-warm
    # pages load before the re-enable round-trip lands), hanging the wait.
    cdp.call("Page.navigate", {"url": url}, session=sid)
    cdp.wait_event("Page.domContentEventFired", timeout=20, session=sid)
    time.sleep(settle)
    setup = (f"var s=document.createElement('style');"
             f"s.textContent={json.dumps(NATURAL_CSS)};"
             "document.documentElement.appendChild(s);"
             f"var a=document.createElement('script');"
             f"a.textContent={json.dumps(axe_src)};"
             "document.head.appendChild(a);'ok'")
    cdp.call("Runtime.evaluate", {"expression": setup, "timeout": 15000}, session=sid)
    run = ("Promise.race(["
           "axe.run(document, {runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}})"
           ".then(r => JSON.stringify({settled: true, violations: r.violations.map(v => "
           "({id: v.id, impact: v.impact, nodes: v.nodes.length, targets: v.nodes.map(n => (n.target&&n.target[0])||''), help: v.help, first: (v.nodes[0]&&v.nodes[0].target[0])||'' }))})),"
           "new Promise(res => setTimeout(() => res(JSON.stringify({settled: false})), 12000))"
           "])")
    r = cdp.call("Runtime.evaluate", {"expression": run, "awaitPromise": True,
                                      "returnByValue": True, "timeout": 30000}, session=sid)
    if "exceptionDetails" in r:
        raise RuntimeError(f"axe.run failed: {r['exceptionDetails'].get('exception', {}).get('description', '?')[:160]}")
    data = json.loads(r["result"]["result"]["value"])
    if not data.get("settled"):
        return None  # honest skip, not a hang
    serious = [v for v in data["violations"] if v.get("impact") in ("critical", "serious")]
    minor = [v for v in data["violations"] if v.get("impact") not in ("critical", "serious")]
    return serious, minor


# ---------- Pass E: click fingerprint (XIAS verify_interactive method) ----------

CLICK_AUDIT_JS = r"""
(function () {
  var CLICKABLE = 'button,[role="button"],input[type="checkbox"],input[type="radio"],'
    + '[role="switch"],[role="tab"],[role="option"],[role="menuitemcheckbox"],[role="menuitemradio"],summary';
  var STATE_ATTRS = ['aria-pressed', 'aria-expanded', 'aria-checked', 'aria-selected', 'aria-sort'];
  function visible(el) {
    var cs = getComputedStyle(el), r = el.getBoundingClientRect();
    return cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0'
      && r.width > 0 && r.height > 0;
  }
  function selector(el) {
    if (el.id) return '#' + CSS.escape(el.id);
    var parts = [];
    while (el && el.nodeType === 1 && el !== document.documentElement) {
      var name = el.localName;
      if (el.parentElement) {
        var siblings = Array.prototype.filter.call(el.parentElement.children,
          function (x) { return x.localName === el.localName; });
        if (siblings.length > 1) name += ':nth-of-type(' + (siblings.indexOf(el) + 1) + ')';
      }
      parts.unshift(name);
      el = el.parentElement;
    }
    return parts.join(' > ');
  }
  var out = [];
  var els = document.querySelectorAll(CLICKABLE);
  for (var i = 0; i < els.length; i++) {
    var el = els[i];
    // A hidden responsive control cannot be clicked by a user at this viewport.
    if (el.disabled || el.getAttribute('aria-disabled') === 'true' || !visible(el)) continue;
    if (el.closest('[data-demo-state]')) continue;
    var decl = null;
    for (var j = 0; j < STATE_ATTRS.length; j++) if (el.hasAttribute(STATE_ATTRS[j])) { decl = STATE_ATTRS[j]; break; }
    if (!decl) {
      var anc = el.closest('[role="tab"],[role="option"],[role="switch"]');
      if (anc) for (var k = 0; k < STATE_ATTRS.length; k++) if (anc.hasAttribute(STATE_ATTRS[k])) { decl = STATE_ATTRS[k]; break; }
    }
    if (!decl) continue;
    var label = (el.textContent || '').trim().slice(0, 24) || el.tagName.toLowerCase();
    out.push({ decl: decl, label: label, sel: selector(el) });
  }
  return out;
})()
"""


def run_click_fingerprint(cdp: CdpClient, sid: str, url: str, settle: float) -> list[dict] | None:
    """Pass E: dead-contract + invisible-state detection (XIAS verify_interactive
    method, 2026-10-24). A control that DECLARES an aria state must (a) change
    something on click (mutations or focus moving elsewhere) and (b) when its
    state attribute actually flips, leave a visible fingerprint (computed style
    or geometry). Returns violation list, or None on transport failure."""
    try:
        cdp.call("Page.navigate", {"url": url}, session=sid)
        cdp.wait_event("Page.domContentEventFired", timeout=20, session=sid)
        time.sleep(settle)
        r = cdp.call("Runtime.evaluate", {"expression": CLICK_AUDIT_JS, "returnByValue": True},
                     timeout=15, session=sid)
        candidates = r["result"]["result"].get("value") or []
        violations: list[dict] = []
        for c in candidates[:25]:  # cap: 25 controls per page keeps the run bounded
            probe = (
                "(function(){var el=document.querySelector(" + json.dumps(c["sel"]) + ");"
                "if(!el) return null;"
                "var me=el;"
                "window.__mut=0;var o=new MutationObserver(function(rs){window.__mut+=rs.length;});"
                "o.observe(document.documentElement,{subtree:true,childList:true,attributes:true,characterData:true});"
                "window.__focus=document.activeElement;"
                "var stB=el.getAttribute(" + json.dumps(c["decl"]) + ");"
                "function sig(root){if(!root)return 'missing';var s=[];var els=[root];"
                "var desc=root.querySelectorAll('*');for(var i=0;i<Math.min(desc.length,40);i++)els.push(desc[i]);"
                "for(var j=0;j<els.length;j++){var e=els[j],c=getComputedStyle(e),r=e.getBoundingClientRect();"
                "s.push(e.tagName+':'+c.display+':'+c.visibility+':'+c.color+':'+c.backgroundColor+':'+"
                "c.textDecorationLine+':'+c.opacity+':'+r.width+','+r.height+':'+(e.innerText||'').trim());}"
                "return s.join('|');}"
                "function controlledSig(e){var ids=(e.getAttribute('aria-controls')||'').trim().split(/\\s+/).filter(Boolean);"
                "return ids.map(function(id){return sig(document.getElementById(id));}).join('||');}"
                "var csB=JSON.stringify({c:getComputedStyle(el).color,b:getComputedStyle(el).backgroundColor,"
                "bgi:getComputedStyle(el).backgroundImage,o:getComputedStyle(el).opacity,"
                "td:getComputedStyle(el).textDecorationLine});"
                "var sigB=sig(el), ctlB=controlledSig(el);"
                "var rB=el.getBoundingClientRect().left+','+el.getBoundingClientRect().top+','+el.getBoundingClientRect().width+','+el.getBoundingClientRect().height;"
                "el.click();"
                "return new Promise(function(res){setTimeout(function(){o.disconnect();"
                "var csA=JSON.stringify({c:getComputedStyle(el).color,b:getComputedStyle(el).backgroundColor,"
                "bgi:getComputedStyle(el).backgroundImage,o:getComputedStyle(el).opacity,"
                "td:getComputedStyle(el).textDecorationLine});"
                "var sigA=sig(el), ctlA=controlledSig(el);"
                "var rA=el.getBoundingClientRect().left+','+el.getBoundingClientRect().top+','+el.getBoundingClientRect().width+','+el.getBoundingClientRect().height;"
                "var stA=el.getAttribute(" + json.dumps(c["decl"]) + ");"
                "var fm=document.activeElement!==me&&document.activeElement!==window.__focus;"
                "res({mut:window.__mut,focusMoved:fm,stateBefore:stB,stateAfter:stA,"
                "styleFingerprintSame:csB===csA&&sigB===sigA&&ctlB===ctlA,geoFingerprintSame:rB===rA});},300);});})()"
            )
            rr = cdp.call("Runtime.evaluate", {"expression": probe, "awaitPromise": True,
                                               "returnByValue": True, "timeout": 8000}, session=sid)
            ev = rr["result"]["result"].get("value")
            if not ev:
                continue  # selector lost / click errored -> inconclusive
            dead = ev["mut"] == 0 and not ev["focusMoved"]
            flipped = ev["stateBefore"] != ev["stateAfter"]
            invisible = flipped and ev["styleFingerprintSame"] and ev["geoFingerprintSame"]
            if dead:
                violations.append({**c, "why": "dead contract — declares state, click changes nothing"})
            elif invisible:
                violations.append({**c, "why": "invisible state — attribute flipped, no visual fingerprint"})
        return violations
    except Exception:  # noqa: BLE001 - transport failure = honest skip
        return None


# ---------- Pass F: system-level economy checks (XIAS slop_tells method) ----------

ECONOMY_JS = r"""
(function () {
  var out = {flatSpacing: 0, oneSidedAccent: []};
  var boxes = [];
  var els = document.querySelectorAll('body *');
  for (var i = 0; i < els.length; i++) {
    var e = els[i], cs = getComputedStyle(e), r = e.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) continue;
    var pad = cs.paddingTop + '|' + cs.paddingRight + '|' + cs.paddingBottom + '|' + cs.paddingLeft;
    if (parseFloat(cs.paddingTop) > 0) boxes.push(pad);
    var sides = [cs.borderTopWidth, cs.borderRightWidth, cs.borderBottomWidth, cs.borderLeftWidth];
    var cols = [cs.borderTopColor, cs.borderRightColor, cs.borderBottomColor, cs.borderLeftColor];
    var thick = 0;
    for (var s = 0; s < 4; s++) {
      if (parseFloat(sides[s]) >= 2 && cols[s] && cols[s] !== 'rgba(0, 0, 0, 0)') thick++;
    }
    if (thick === 1 && r.width >= 80 && r.height >= 32) {
      var label = (e.textContent || '').trim().slice(0, 24) || e.tagName.toLowerCase();
      out.oneSidedAccent.push(e.tagName.toLowerCase() + ' «' + label + '»');
    }
  }
  var sig = {};
  for (var b = 0; b < boxes.length; b++) sig[boxes[b]] = (sig[boxes[b]] || 0) + 1;
  for (var k in sig) if (sig[k] >= 10) { out.flatSpacing = sig[k]; break; }
  return out;
})()
"""


def run_economy(cdp, sid, url, settle):
    """Pass F: page-level economy signals (flat-spacing monotony, one-sided
    accent borders). Render-based because static grep can't see resolved border
    colors through Tailwind utilities (XIAS slop_tells insight)."""
    try:
        cdp.call("Page.navigate", {"url": url}, session=sid)
        cdp.wait_event("Page.domContentEventFired", timeout=20, session=sid)
        time.sleep(settle)
        r = cdp.call("Runtime.evaluate", {"expression": ECONOMY_JS, "returnByValue": True},
                     timeout=15, session=sid)
        return r["result"]["result"].get("value")
    except Exception:
        return None


def classify(natural: list[dict], frozen: list[dict], reduced: list[dict],
             reduce_anim_count: int) -> tuple[list, list, list, int]:
    """A failures are hard (§4a gatekeeper); B is informational (diff vs the
    natural-visible set); C failures are hard (reduce contract)."""
    nat_keys = {(e["sel"], e["text"]) for e in natural}
    b_warn = [e for e in frozen if (e["sel"], e["text"]) not in nat_keys]
    return natural, b_warn, reduced, reduce_anim_count


RENDER_METRICS_JS = r"""
(function () {
  function visible(el) {
    var cs = getComputedStyle(el), r = el.getBoundingClientRect();
    return cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0'
      && r.width >= 2 && r.height >= 2;
  }
  var text = (document.body && document.body.innerText || '').replace(/\s+/g, ' ').trim();
  var headings = Array.prototype.filter.call(document.querySelectorAll('h1,h2,h3,[role="heading"]'), visible)
    .filter(function (e) { return (e.innerText || '').trim().length > 0; }).length;
  var controls = Array.prototype.filter.call(document.querySelectorAll(
    'button,[role="button"],input,select,textarea,summary,a[href]'), visible).length;
  var media = Array.prototype.filter.call(document.querySelectorAll('img,video,canvas,iframe'), function (e) {
    if (!visible(e)) return false;
    if (e.tagName === 'IMG') return e.complete && e.naturalWidth > 0;
    if (e.tagName === 'VIDEO') return e.readyState >= 1;
    return true;
  }).length;
  return {textChars: text.length, headings: headings, controls: controls, media: media};
})()
"""


def is_vacuous_render(metrics: dict | None) -> bool | None:
    """Detect hollow renders with composed text and rendered UI evidence."""
    if not isinstance(metrics, dict):
        return None
    text, headings = metrics.get("textChars"), metrics.get("headings")
    controls, media = metrics.get("controls"), metrics.get("media")
    if not all(isinstance(v, int) and v >= 0 for v in (text, headings, controls, media)):
        return None
    meaningful = (text >= 32 or (text >= 2 and headings >= 1)
                  or (text >= 8 and controls >= 2) or media >= 1)
    return not meaningful


def probe(url: str, settle: float = 0.8, with_axe: bool = True,
          width: int = 1440,
          cdp: CdpClient | None = None, sid: str | None = None,
          ) -> tuple[list, list, list, int, list | None, list | None, list | None, bool]:
    proc = user_data_dir = None
    if cdp is None:
        port = free_tcp_port()
        proc, _ws, user_data_dir = launch_browser(port)
        try:
            ws = browser_ws_url(port)
            cdp = CdpClient("127.0.0.1", port, urlparse_path(ws))
            tid = cdp.call("Target.createTarget", {"url": "about:blank"})["result"]["targetId"]
            sid = cdp.call("Target.attachToTarget", {"targetId": tid, "flatten": True})["result"]["sessionId"]
        except Exception:
            _terminate_tree(proc)
            raise
    try:
        cdp.call("Page.enable", session=sid)
        cdp.call("Emulation.setDeviceMetricsOverride",
                 {"width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False},
                 session=sid)
        nat = run_pass(cdp, sid, url, NATURAL_CSS, False, settle)
        froz = run_pass(cdp, sid, url, PAUSED_CSS, False, settle)
        red = run_pass(cdp, sid, url, None, True, settle)
        rac = count_animations_under_reduce(cdp, sid, url, settle)
        # XIAS hollow-render guard: use composed visible text and controls,
        # including slotted text from component-library elements.
        try:
            vac = cdp.call("Runtime.evaluate", {"expression": RENDER_METRICS_JS,
                "returnByValue": True}, timeout=10, session=sid)["result"]["result"].get("value")
        except Exception:  # noqa: BLE001
            vac = None
        vacuous = is_vacuous_render(vac)
        e_fail = None
        eco = None
        if with_axe:  # Pass E rides the same session after D
            e_fail = run_click_fingerprint(cdp, sid, url, settle)
            eco = run_economy(cdp, sid, url, settle)
        a_ser = a_min = None
        if with_axe:
            # run_axe returns None on honest skip (CDN unreachable / axe not
            # settled) — never unpack it directly; one retry absorbs transient
            # network/settle flakes before we accept the skip.
            axe_res = run_axe(cdp, sid, url, settle)
            if axe_res is None:
                axe_res = run_axe(cdp, sid, url, settle + 0.4)
            if axe_res is not None:
                a_ser, a_min = axe_res
        if proc is not None:  # self-launched browser: close connection (caller may still use it in shared mode)
            pass  # keep the target alive in shared mode — caller calls close()
        return classify(nat, froz, red, rac) + (a_ser, a_min, e_fail, vacuous, eco)
    finally:
        if proc is not None:
            _terminate_tree(proc)
            import shutil
            shutil.rmtree(user_data_dir, ignore_errors=True)


# ---------- reporting ----------

def report(name: str, items: list[dict]) -> None:
    for e in items:
        print(f"  [{name}] {e['sel']}  «{e['text']}»")
        print(f"         {e['why']}" + (f", animation={e['anim']}, delay={e['delay']:.2f}s dur={e['dur']:.2f}s" if e["anim"] else ""))


def expected_a11y_verdict(axe_serious, expectation):
    """Match an intentional negative fixture against its complete axe signature."""
    if axe_serious is None:
        return "UNKNOWN"
    expected = sorted(expectation.get("targets", []))
    actual = sorted(target for item in axe_serious
                    for target in item.get("targets", ([item.get("first", "")] if item.get("first") else []))
                    if target)
    if not axe_serious:
        return "XPASS"
    if (len(axe_serious) == 1 and axe_serious[0].get("id") == expectation.get("id")
            and axe_serious[0].get("impact") == expectation.get("impact")
            and actual == expected):
        return "EXPECTED-NEGATIVE"
    return "MISMATCH"


def coverage_verdict(natural, reduced, animations, axe_serious, clicks, vacuous,
                     axe_requested=True, expected_a11y=None):
    """Report probe coverage, not overall usability or WCAG conformance."""
    expected_status = expected_a11y_verdict(axe_serious, expected_a11y) if expected_a11y else None
    axe_failures = len(axe_serious or [])
    if expected_status == "EXPECTED-NEGATIVE":
        axe_failures = 0
    elif expected_status in ("XPASS", "MISMATCH"):
        axe_failures = max(1, axe_failures)
    failures = len(natural) + len(reduced) + bool(animations) + axe_failures + len(clicks or [])
    missing = []
    if axe_serious is None:
        missing.append("axe unavailable" if axe_requested else "axe disabled")
    if clicks is None:
        missing.append("click observation unavailable")
    if vacuous is None:
        missing.append("render-volume observation unavailable")
    if expected_status == "UNKNOWN":
        missing.append("expected negative-control signature unavailable")
    verdict = "FAIL" if failures or vacuous is True else ("UNKNOWN" if missing else "PASS")
    return {"ok": verdict == "PASS", "verdict": verdict,
            "coverage": "partial" if missing else "complete",
            "missing_checks": missing, "vacuous": vacuous,
            "expected_negative": expected_status}


def main() -> int:
    ap = argparse.ArgumentParser(description="glasspring render-time composition probe (animation-gated / reduced-motion content audit)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("url", nargs="?", help="page to probe (http/https/file)")
    ap.add_argument("--settle", type=float, default=0.8, help="seconds to wait after load before auditing")
    ap.add_argument("--no-axe", dest="axe", action="store_false",
                    help="skip the axe-core a11y pass (D)")
    ap.add_argument("--width", type=int, default=1440,
                    help="viewport width for the render (default 1440 desktop; headless default 800x600 can collapse responsive navigation into false zero-boxes)")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    if not a.url:
        ap.error("give a URL or --selftest")
    if not find_browser():
        print("SKIP: no Chromium-family browser found (set CHROME_PATH)")
        return 2
    print(f"-- render probe: {a.url} --")
    a_fail, b_warn, c_fail, rac, a_ser, a_min, e_fail, vacuous, eco = probe(a.url, settle=a.settle, with_axe=a.axe, width=a.width)
    report("A-FAIL animation-gated", a_fail)
    report("B-WARN time-gated at t=0", b_warn)
    report("C-FAIL reduced-motion broken", c_fail)
    if rac:
        print(f"  [C-FAIL] {rac} element(s) still animate under prefers-reduced-motion:reduce")
    for v in a_ser or []:
        print(f"  [D-FAIL axe/{v['impact']}] {v['id']} ×{v['nodes']}  {v['help']}  e.g. {v['first']}")
    for v in a_min or []:
        print(f"  [D-WARN axe/{v['impact']}] {v['id']} ×{v['nodes']}  {v['help']}")
    for v in e_fail or []:
        print(f"  [E-FAIL click] {v['sel']} «{v['label']}»  {v['why']}")
    if a_ser is None and a.axe:
        print("  [D-SKIP] axe-core CDN unreachable — a11y coverage limited to passes A-C")
    n = len(a_fail) + len(c_fail) + (1 if rac else 0) + len(a_ser or []) + len(e_fail or [])
    if vacuous is True:
        print("  [V-FAIL vacuous] no meaningful rendered text, heading, controls, or media surface")
    elif vacuous is None:
        print("  [V-UNKNOWN] render-volume observation unavailable")
    if eco:
        if eco.get("flatSpacing"):
            print(f"  [F-WARN flat-spacing] {eco['flatSpacing']} boxes share one padding signature")
        for s in eco.get("oneSidedAccent", [])[:8]:
            print(f"  [F-WARN one-sided-accent] {s}")
    print(f"summary: A {len(a_fail)} fail, B {len(b_warn)} time-gated, C {len(c_fail) + (1 if rac else 0)} fail, "
          f"D {len(a_ser or [])} fail + {len(a_min or [])} warn, E {len(e_fail or [])} click-fail"
          + ("  — see motion.md §4a (动画永不作为内容守门员)" if len(a_fail) + len(c_fail) else ""))
    status = coverage_verdict(a_fail, c_fail, rac, a_ser, e_fail, vacuous, a.axe)
    print("coverage: " + json.dumps(status))
    return {"PASS": 0, "FAIL": 1, "UNKNOWN": 2}[status["verdict"]]


# ---------- selftest ----------

PAGE_OK = """<!DOCTYPE html><html lang="en"><head><title>typing pattern</title><style>
body{font:16px system-ui;background:#fff;color:#111;margin:0;padding:20px}
.static-line{font-size:20px}
/* robust typing pattern: base state VISIBLE, from-keyframe hides, backwards fill */
.typed{display:inline-block;overflow:hidden;white-space:nowrap;max-width:9em;
  animation:type 1.5s steps(9,end) .5s backwards}
@keyframes type{from{max-width:0}}
.caret{display:inline-block;width:2px;height:1em;background:#111;animation:blink 1s step-end infinite}
@keyframes blink{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){.typed{animation:none}.caret{animation:none}}
</style></head><body>
<div class="static-line">Always visible carrier line.</div>
<div><span class="typed">Enhancement line</span><span class="caret"></span></div>
</body></html>"""

PAGE_BUG = """<!DOCTYPE html><html lang="en"><head><title>gatekeeper bug</title><style>
body{font:16px system-ui;margin:0;padding:20px}
.typed{display:inline-block;overflow:hidden;white-space:nowrap;max-width:0;
  animation:type 1.5s steps(12,end) .8s forwards}
@keyframes type{to{max-width:12em}}
</style></head><body>
<div><span class="typed">Gated behind animation</span></div>
</body></html>"""

PAGE_RM_BROKEN = """<!DOCTYPE html><html lang="en"><head><title>rm broken</title><style>
body{font:16px system-ui;margin:0;padding:20px}
.hero{animation:enter .7s ease-out both}
@keyframes enter{from{opacity:0}}
/* no prefers-reduced-motion block — the contract violation */
</style></head><body>
<div class="hero">Entrance-gated hero copy</div>
</body></html>"""

PAGE_DEAD_CONTRACT = """<!DOCTYPE html><html lang="en"><head><title>dead contract</title></head><body>
<button aria-pressed="false" onclick="void 0">冻结</button>
</body></html>"""

PAGE_INVISIBLE_STATE = """<!DOCTYPE html><html lang="en"><head><title>invisible state</title><style>
.tgl{background:#eee;padding:8px 16px;border:0;font:14px system-ui}
</style></head><body>
<button class="tgl" id="t" aria-pressed="false" onclick="this.setAttribute('aria-pressed', this.getAttribute('aria-pressed')==='true'?'false':'true')">静默切换</button>
</body></html>"""

PAGE_LIVE_STATE = """<!DOCTYPE html><html lang="en"><head><title>live state</title><style>
.tgl{background:#eee;padding:8px 16px;border:0;font:14px system-ui}
.tgl[aria-pressed="true"]{background:#2266a4;color:#fff}
</style></head><body>
<button class="tgl" aria-pressed="false" onclick="this.setAttribute('aria-pressed', this.getAttribute('aria-pressed')==='true'?'false':'true')">真切换</button>
</body></html>"""

# state fingerprint lives ONLY on descendants (icon swap + strikethrough) —
# the control's own computed style/geometry is unchanged. A sighted user sees
# the change, so pass E must too.
PAGE_LIVE_STATE_DESCENDANT = """<!DOCTYPE html><html lang="en"><head><title>live state descendant</title><style>
.tgl{background:#eee;padding:8px 16px;border:0;font:14px system-ui}
.tgl span.done{text-decoration:line-through;color:#888}
</style></head><body>
<button class="tgl" aria-pressed="false" onclick="this.setAttribute('aria-pressed', this.getAttribute('aria-pressed')==='true'?'false':'true');this.querySelector('span').classList.toggle('done')"><span>任务一</span></button>
</body></html>"""

PAGE_CONTROLLED_STATE = """<!DOCTYPE html><html lang="en"><head><title>responsive menu state</title><style>
body{font:16px system-ui;margin:0;padding:20px}
#mobile-panel[hidden]{display:none}
button{min-height:44px;padding:8px 16px}
</style></head><body>
<h1>Menu demo</h1>
<button id="menu-toggle" aria-expanded="false" aria-controls="mobile-panel"
  onclick="var p=document.getElementById('mobile-panel');var open=this.getAttribute('aria-expanded')!=='true';this.setAttribute('aria-expanded',String(open));p.hidden=!open">Open menu</button>
<button id="desktop-only" style="display:none" aria-expanded="false"
  onclick="this.setAttribute('aria-expanded','true')">Hidden desktop control</button>
<nav id="mobile-panel" hidden><a href="#one">Menu item</a></nav>
</body></html>"""

PAGE_A11Y_BROKEN = """<!DOCTYPE html><html lang="en"><head><title>a11y broken</title></head><body>
<h1>Form</h1>
<input type="text" name="q">
<img src="chart.png">
<button onclick="void 0">go</button>
</body></html>"""


def selftest() -> int:
    fails = []

    def check(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    print("selftest: audit JS offline sanity")
    check("NATURAL_CSS kills animations", "animation:none" in NATURAL_CSS)
    check("PAUSED_CSS freezes clock", "animation-play-state:paused" in PAUSED_CSS)
    check("AUDIT_JS balanced braces", AUDIT_JS.count("{") == AUDIT_JS.count("}"))

    if not find_browser():
        print("SKIP (no Chromium-family browser found) — offline anchors still green")
        return 0 if not fails else 1

    print("selftest: live passes")
    def run(html, label):
        url = "data:text/html," + urllib.request.quote(html)
        return probe(url)

    try:
        nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = run(PAGE_OK, "ok")
        check("OK page: pass A clean (carrier line visible)", len(nat) == 0, str(nat))
        check("OK page: pass B flags only the typed enhancement",
              len(froz) == 1 and froz[0]["anim"] == "type" and froz[0]["delay"] == 0.5, str(froz))
        check("OK page: pass C clean (reduce handled)", len(red) == 0 and rac == 0,
              f"hidden={red} animating={rac}")
        check("OK page: pass D clean (no serious axe violations)", a_ser == [], str(a_ser))
    except Exception as e:
        check("OK page probe", False, f"{type(e).__name__}: {e}")

    try:
        nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = run(PAGE_BUG, "bug")
        check("BUG page: pass A catches the gatekeeper",
              len(nat) == 1 and "Gated" in nat[0]["text"], str(nat))
        check("BUG page: pass A names max-width clip",
              "clipped" in nat[0]["why"] or "zero box" in nat[0]["why"], str(nat[0]["why"]))
    except Exception as e:
        check("BUG page probe", False, f"{type(e).__name__}: {e}")

    try:
        nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = run(PAGE_RM_BROKEN, "rm")
        check("RM-BROKEN page: pass A clean (animation completes in natural state)",
              len(nat) == 0, str(nat))
        check("RM-BROKEN page: pass C catches missing reduce handling (still animating)",
              rac >= 1, f"animating under reduce: {rac}")
    except Exception as e:
        check("RM-BROKEN page probe", False, f"{type(e).__name__}: {e}")

    try:
        nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = run(PAGE_A11Y_BROKEN, "a11y")
        axe_ids = {v["id"] for v in (a_ser or [])}
        check("A11Y-BROKEN page: pass D catches unlabeled input (label)",
              "label" in axe_ids, str(a_ser))
        check("A11Y-BROKEN page: pass D catches missing alt (image-alt)",
              "image-alt" in axe_ids, str(a_ser))
    except Exception as e:
        check("A11Y-BROKEN page probe", False, f"{type(e).__name__}: {e}")

    try:
        nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = run(PAGE_DEAD_CONTRACT, "dead")
        check("DEAD-CONTRACT page: pass E catches state-declared no-op",
              e_fail and any("dead contract" in v["why"] for v in e_fail), str(e_fail))
    except Exception as e:
        check("DEAD-CONTRACT page probe", False, f"{type(e).__name__}: {e}")

    try:
        nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = run(PAGE_INVISIBLE_STATE, "invis")
        check("INVISIBLE-STATE page: pass E catches attribute-flip with no visual change",
              e_fail and any("invisible state" in v["why"] for v in e_fail), str(e_fail))
    except Exception as e:
        check("INVISIBLE-STATE page probe", False, f"{type(e).__name__}: {e}")

    try:
        nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = run(PAGE_LIVE_STATE, "live")
        check("LIVE-STATE page: pass E clean (flip has visual fingerprint)",
              e_fail == [], str(e_fail))
    except Exception as e:
        check("LIVE-STATE page probe", False, f"{type(e).__name__}: {e}")

    try:
        nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = run(PAGE_LIVE_STATE_DESCENDANT, "live-d")
        check("DESCENDANT-STATE page: pass E clean (subtree fingerprint counts)",
              e_fail == [], str(e_fail))
    except Exception as e:
        check("DESCENDANT-STATE page probe", False, f"{type(e).__name__}: {e}")

    try:
        nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = run(PAGE_CONTROLLED_STATE, "controlled")
        check("CONTROLLED-STATE page: visible panel change counts; hidden responsive control is skipped",
              e_fail == [], str(e_fail))
    except Exception as e:
        check("CONTROLLED-STATE page probe", False, f"{type(e).__name__}: {e}")

    if fails:
        print(f"SELFTEST FAILED: {fails}")
        return 1
    print("SELFTEST PASSED (all anchors green)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
