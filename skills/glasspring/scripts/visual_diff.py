#!/usr/bin/env python3
"""visual_diff.py — pixel-level screenshot diff for the glasspring skill.

Closes the bounded fix-loop's blind spot: "fixed → re-shot" verified nothing
CHANGED. Uses:
  1. fix-loop verification — before/after a fix round MUST differ (else the
     "fix" touched nothing visible: 修图无像素变化 = 没修)
  2. restyle evidence — before/after restyle must differ meaningfully
  3. regression drift — same sample across runs should match

Pure stdlib: PNG decode is zlib + unfilter (screenshots are 8-bit RGB/RGBA/
grayscale, the only types CDP emits). PNG is lossless, so the default
per-channel tolerance is 0; --tol absorbs browser AA jitter across runs.

Usage:
  python visual_diff.py before.png after.png
  python visual_diff.py a.png b.png --max-diff 0.001   # gate: fail if MORE
  python visual_diff.py a.png b.png --min-diff 0.0005  # gate: fail if LESS
  python visual_diff.py --selftest
"""
from __future__ import annotations
import argparse, struct, sys, zlib

SIG = b"\x89PNG\r\n\x1a\n"


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else (b if pb <= pc else c)


def decode_png(path: str) -> tuple[int, int, int, bytes]:
    """-> (width, height, channels, raw pixels row-major). 8-bit types only."""
    blob = open(path, "rb").read()
    if not blob.startswith(SIG):
        raise ValueError(f"not a PNG: {path}")
    pos = 8
    w = h = 0
    bpp = channels = bitdepth = 0
    idat = bytearray()
    palette: list[tuple[int, int, int]] = []
    trns = bytearray()
    while pos < len(blob):
        ln, typ = struct.unpack(">I4s", blob[pos:pos + 8])
        data = blob[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if typ == b"IHDR":
            w, h, bitdepth, ctype = struct.unpack(">IIBB", data[:10])
            if bitdepth != 8:
                raise ValueError(f"unsupported bit depth {bitdepth} (8-bit only)")
            channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
        elif typ == b"PLTE":
            palette = [tuple(data[i:i + 3]) for i in range(0, len(data), 3)]
        elif typ == b"tRNS":
            trns = data
        elif typ == b"IDAT":
            idat.extend(data)
        elif typ == b"IEND":
            break
    if not w or not h:
        raise ValueError(f"no IHDR/IEND in {path}")
    bpp = channels  # 8-bit: bytes per pixel == channels
    raw = zlib.decompress(bytes(idat))
    stride = w * bpp
    out = bytearray(stride * h)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]
        p += 1
        line = bytearray(raw[p:p + stride])
        p += stride
        if f == 1:  # Sub
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif f == 2:  # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif f == 3:  # Average
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + (left + prev[i]) // 2) & 0xFF
        elif f == 4:  # Paeth
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                ul = prev[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + _paeth(left, prev[i], ul)) & 0xFF
        elif f != 0:
            raise ValueError(f"bad filter {f} at row {y}")
        out[y * stride:(y + 1) * stride] = line
        prev = line
    if ctype == 3:  # palette → expand to RGB
        rgb = bytearray(w * h * 3)
        for i, idx in enumerate(out):
            r, g, b = palette[idx] if idx < len(palette) else (0, 0, 0)
            rgb[i * 3:i * 3 + 3] = bytes((r, g, b))
        return w, h, 3, bytes(rgb)
    return w, h, channels, bytes(out)


def diff(path_a: str, path_b: str, tol: int = 0) -> dict:
    wa, ha, ca, pa = decode_png(path_a)
    wb, hb, cb, pb = decode_png(path_b)
    if (wa, ha) != (wb, hb):
        raise ValueError(f"size mismatch: {wa}x{ha} vs {wb}x{hb} — "
                         "align viewport/labels before diffing")
    if ca != cb:  # grayscale/RGB/RGBA mix: compare the shared prefix channels
        ca = min(ca, cb)
    total = wa * ha
    changed = 0
    min_x, min_y, max_x, max_y = wa, ha, -1, -1
    for y in range(ha):
        row_a, row_b = y * wa * ca, y * wa * ca
        for x in range(wa):
            base = row_a + x * ca
            if any(abs(pa[base + k] - pb[base + k]) > tol for k in range(ca)):
                changed += 1
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
    bbox = None if max_x < 0 else (min_x, min_y, max_x, max_y)
    return {"changed": changed, "total": total, "ratio": changed / total, "bbox": bbox}


def selftest() -> int:
    import os, tempfile

    def chunk(typ: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + typ + data + struct.pack(">I", zlib.crc32(typ + data))

    def write_png(path: str, w: int, h: int, px: bytes, ctype: int = 2):
        ihdr = struct.pack(">IIBBBBB", w, h, 8, ctype, 0, 0, 0)
        stride = w * {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
        raw = b"".join(b"\x00" + px[y * stride:(y + 1) * stride] for y in range(h))
        with open(path, "wb") as f:
            f.write(SIG + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))

    ok = True

    def check(cond, msg):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
        ok = ok and cond

    with tempfile.TemporaryDirectory() as td:
        a = os.path.join(td, "a.png")
        b = os.path.join(td, "b.png")
        c = os.path.join(td, "c.png")
        # 4x4 RGB: all (10,20,30); b: one pixel at (2,1) flips; c: sub-filtered same as a
        px_a = bytes((10, 20, 30)) * 16
        px_b = bytearray(px_a)
        px_b[(1 * 4 + 2) * 3:(1 * 4 + 2) * 3 + 3] = bytes((200, 200, 200))
        write_png(a, 4, 4, px_a)
        write_png(b, 4, 4, bytes(px_b))
        # sub-filter encode of the same a-pixels (filter path coverage)
        rows_enc = []
        for y in range(4):
            row = px_a[y * 12:(y + 1) * 12]
            rows_enc.append(b"\x01" + bytes((v - (row[i - 3] if i >= 3 else 0)) & 0xFF
                                            for i, v in enumerate(row)))
        raw_sub = b"".join(rows_enc)
        with open(c, "wb") as f:
            f.write(SIG + chunk(b"IHDR", struct.pack(">IIBBBBB", 4, 4, 8, 2, 0, 0, 0))
                    + chunk(b"IDAT", zlib.compress(raw_sub)) + chunk(b"IEND", b""))
        r0 = diff(a, a)
        check(r0["changed"] == 0 and r0["ratio"] == 0.0, "identical → ratio 0")
        r1 = diff(a, b)
        check(r1["changed"] == 1 and abs(r1["ratio"] - 1 / 16) < 1e-9, f"one-pixel flip → {r1['changed']} px, ratio {r1['ratio']:.4f}")
        check(r1["bbox"] == (2, 1, 2, 1), f"bbox exact: {r1['bbox']}")
        r2 = diff(a, c)
        check(r2["changed"] == 0, "sub-filter decode roundtrips to identical")
        try:
            diff(a, os.path.join(td, "missing.png"))
            check(False, "missing file raises")
        except (OSError, FileNotFoundError):
            check(True, "missing file raises")
    print("visual_diff selftest:", "ALL PASS" if ok else "FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="pixel-level PNG diff (fix-loop / restyle / drift gates)")
    ap.add_argument("png_a", nargs="?", help="before/left PNG")
    ap.add_argument("png_b", nargs="?", help="after/right PNG")
    ap.add_argument("--tol", type=int, default=0, help="per-channel tolerance (0 = lossless-exact)")
    ap.add_argument("--max-diff", type=float, help="gate: FAIL if ratio EXCEEDS this (drift)")
    ap.add_argument("--min-diff", type=float, help="gate: FAIL if ratio is BELOW this (fix/restyle changed nothing)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.png_a or not a.png_b:
        ap.error("two PNG paths required (or --selftest)")
    try:
        r = diff(a.png_a, a.png_b, tol=a.tol)
    except (OSError, ValueError) as e:
        print(f"error: {e}")
        return 2
    bbox = "" if r["bbox"] is None else f" bbox x{r['bbox'][0]},y{r['bbox'][1]}-{r['bbox'][2]},y{r['bbox'][3]}"
    print(f"changed {r['changed']}/{r['total']} px = {r['ratio']:.5f} (tol {a.tol}){bbox}")
    if a.max_diff is not None and r["ratio"] > a.max_diff:
        print(f"FAIL: ratio {r['ratio']:.5f} > max {a.max_diff} (drift / unwanted change)")
        return 1
    if a.min_diff is not None and r["ratio"] < a.min_diff:
        print(f"FAIL: ratio {r['ratio']:.5f} < min {a.min_diff} — 修图无像素变化 = 没修 (no visible change)")
        return 1
    if a.max_diff is None and a.min_diff is None and r["changed"] == 0:
        print("identical — if these were fix-round shots, the fix changed nothing visible")
    return 0


if __name__ == "__main__":
    sys.exit(main())
