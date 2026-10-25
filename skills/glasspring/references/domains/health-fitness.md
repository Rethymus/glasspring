# Domain pack — health & fitness（患者端/远程医疗/制药 ⚠/心理健康/养老/健身）

> When to read: health data, care journeys, medical content, wellness, senior-facing, fitness tracking.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## Cross-domain rules

- **Data restraint = clinical credibility**: one metric card = current value + normal range + trend; no leaderboards, no "score shaming". Abnormal values get a "discuss with your clinician" exit, never a red alarm wall.
- Apple Health posture to emulate: privacy-first messaging, device/E2E encryption stated, wellness/medical boundary labeled ("not for medical use"), research PDFs linked.
- Emergency/crisis entries (911/120, 988) permanently reachable on every screen of relevant products; Exit-this-page pattern (gov.uk) for vulnerable-user escape.

## Surfaces

### 患者端健康 App（Apple Health/MyChart 型）
- Motion 1-2/5: **never celebrate "normal"** (it shames the abnormal); trend charts soft-ease; springs only for pin/favorite.
- Glass: metric cards light; lab results & medication lists opaque.
- Red lines: diagnostic implications, health data for ads, default-share instead of default-private.

### 远程医疗/挂号（Teladoc/Zocdoc 型）
- Two certainties: who is the doctor (license/rating/specialty/slots on one card) and how long the wait ("约 X 分钟" not a spinner).
- Motion 2/5: rhythmic neutral wait pulse; connect-moment spring = "you're seeing a human now".
- Red lines: hidden paid-ranking (Zocdoc's model disclosed), vague credentials, no cancel/reschedule path.

### 制药/器械官网 ⚠（FDA/NMPA 合规）
- Risk and benefit presented with EQUAL visual weight; ISI (important safety information) box; adverse-event report entry is site-level permanent navigation (MedWatch pattern); print stylesheet first-class.
- Motion 0-1/5. Glass: hero frost at most.
- Red lines: public-facing prescription-drug promotion (illegal in China/NMPA), risk folded away, patient stories implying typical results.

### 心理健康（Headspace/Calm 型）
- Two registers that must not blend: healing aesthetics lower the start barrier; crisis responsibility design guards the floor (988-type entry constant, Exit-this-page escape).
- Motion 2/5 **but slow**: 4–6s breath cycles guide physiology; springs feel mechanical here — use for card lift only.
- Glass: meditation player/soundscape mixer = "quiet container"; crisis resources high-contrast solid.
- Red lines: streak-loss anxiety mechanics, crisis entry buried, AI chat replacing crisis intervention promises.

### 养老/适老化（叠加于一切老年触达产品）
- W3C WAI-AGE: existing WCAG covers most senior needs — practice = one notch looser everywhere (type ≥18px, targets ≥44-48px, contrast up, one cognitive action per screen, icons with labels).
- Motion 0-1/5; springs disabled; system reduce-motion respected absolutely. Ads forbidden in senior modes (CN MIIT push since 2021).
- Glass: essentially incompatible with the contrast floor — decorative layer only, never under text.

### 健身/运动（Strava/Peloton 型）— 见 consumer-lifestyle 消费侧画像
- Two-posture design: in-workout = giant data, zero chrome; post-workout = social confirmation + charts. Glass on live data floats; goals/streaks per Goal-Gradient; "clear than clever" on paywall signals (Strava misread case).
