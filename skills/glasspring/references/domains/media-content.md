# Domain pack — media & content（新闻/长文/视频/短视频/音乐/播客）

> When to read: the product's core content is media — news portals, long-form reading, video streaming, short-video feeds, music/audio, podcasts.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## Cross-domain rules

- **Dark default for playback surfaces** (video/music): content is the interface; near-black `#0A0A0A–#141414`, never pure black behind detail-rich posters.
- F-pattern governs scanning surfaces (news, logs, scores): key info in the first two paragraphs/lines, bold the informative words.
- Right-rail/banner blindness: 25% of layout there earns 0.8% of fixations — never put must-see content in ad-shaped positions; **ads poison adjacent content**.
- Infinite scroll fits "no particular task" browsing (social/feeds) but must keep a way back (integrated pagination/landmarks).

## Surfaces

### 新闻/门户
- Metered paywall over hard wall (NYT metered: 224k subs in 3 months; hard walls shed ~90% of traffic). Reading progress indicator. Breaking-news bar is a distinct component, visually isolated from articles.
- Motion 1/5. Glass: floating nav only; **body text never translucent**.
- Red lines: styling content like ads; flattened heading hierarchy (wall of text).

### 长文/博客/Newsletter
- The immersion chamber: single column 60–75ch, 1.6+ line-height, whitespace IS the product; dark mode offered and switchable mid-read (NN/g: light reads better small, dark kinder to low-vision).
- Motion 0.5/5: progress bar + TOC highlight; one gentle spring on subscribe success max.
- Components: sticky progress, subscribe cards at 1/3 + end, hover quote-share, focus/reader mode.
- Red lines: floating subscribe popups mid-paragraph, >90ch lines, hover-only critical functions.

### 视频流媒体（Netflix/YouTube 型）
- Poster-wall (horizontal rails + vertical scroll), 5-6 focusable items/screen; hover/focus scale 1.02–1.08 (spring out, decay in); controls auto-hide 2–3s.
- Motion 2.5/5. **Glass: player control layer only** — the canonical glass surface; posters/details avoid it (fights artwork texture).
- Continue-Watching progress embedded in poster; TV: XY-focus, ≤6 clicks cross-screen, focus ring unmistakable.
- Red lines: pure #000 detail pages (crushes shadow detail), controls that never hide, nested clickable elements on TV.

### 短视频 UGC（TikTok/抖音型）
- Content IS the interface: full-bleed vertical feed, swipe-up snap; UI = white text + local drop shadow over any footage; right-side action rail; bottom meta. Single-digit text per screen.
- Motion 4/5 **interaction-only**: double-tap heart burst (big spring), page-snap springs, scrub preview; the feed scroll itself never parallax.
- Glass: comment half-sheet and side panels OK; persistent overlays over video need gradient scrims first (contrast on moving footage is unownable).
- Red lines: anything interrupting the swipe gesture; missing sound-on-first-play disclosure.

### 音乐/音频流媒体（Spotify/Apple Music 型）
- Album art drives identity: dominant-color extraction → dynamic accent theme (gradient hero settling to stable base); **text always uses the extraction-safe white/black pair** with WCAG fallback.
- Now Playing = the signature glass surface: tinted glass (blur the artwork), mini-player persistent, tap to expand (shared-element spring).
- Motion 3/5. Wrapped/year-recap share cards are the brand moment.
- Red lines: fixed brand color overriding artwork mood; contrast failing on any album; heavy transitions during background listening.

### 播客
- Time management is the product: 0.5x–3x speed dial, chapter-marked progress, skip 15/30, sleep timer, "18 min left" remaining-time framing.
- Motion 1.5/5: instant (≤0.1s) speed feedback, no springs on functional controls.
- Glass: speed/sleep floating panels and chapter drawer; progress bar itself stays solid (precision).
- Red lines: speed buried in menus, resume position off by even 10s, auto-skip without an off switch.
