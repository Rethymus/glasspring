# type.md — typography (Western + CJK)

> When to read: with tokens.md, before writing any text styles.
> Targeted source check: Apple’s type-weight guidance was checked 2026-10-26; this is not a full claim-by-claim audit. See [Apple Typography guidance](https://developer.apple.com/design/human-interface-guidelines/typography). Platform-specific text sizing and CJK recommendations here are project guidance; confirm behavior in the target runtime.

## 1. Scale & roles

Use tokens.md §3 scale (1.25 ratio). Role rules that survive every project:
- One `display` style per page max. Titles sentence-case unless the brand voice says otherwise; avoid ALL-CAPS eyebrows and accent-colored single words in headlines (slop signals).
- **眉题反转对**（taste-skill house rules 2026-10-22）：分区缺 eyebrow 标签 = 结构性失败（强站的分区都有小引导标签）；但微型**加宽大写**眉题是禁止项——正解是小号 sentence-case 标签（12-13px，letter-spacing 0 或微正）。**风格域例外**（soft-skill/classics 交叉 2026-10-22）：soft-premium/高端视觉域内 10px tracked pill 眉题是流派正典语法——FM-6：风格包 never > 泛域默认，包内条款优先于本条
- Line length 60–75ch body; headings ≤ 2 lines — use `text-wrap: balance` on headings (~94% support). Display 大标题测宽 **~18–24ch**（防六行折行；taste/ux-ui 双源）。
- Hierarchy by **size + weight + space**, not by boxes and divider lines. If two levels need a border to be distinguished, increase the size gap instead.
- **层级三通道（HIG Layout 2026-10-18）**：对齐使条目被感知为相关（对齐即分组）；缩进使条目被感知为从属（indentation = subordination）；内容过多时用渐进披露（disclosure 控件/嵌套视图/可滚动分区）降初始密度——三者是 whitespace 之外层级语法的官方补充。
- **Light-weight guidance (Apple HIG, checked 2026-10-26)**: Apple advises generally avoiding Ultralight/Thin/Light for readability and sizing custom thin fonts above the platform's recommended size ([Typography guidance](https://developer.apple.com/design/human-interface-guidelines/typography)). This is platform guidance, not a ban on every thin style; Glasspring's CJK faux-light rule in §3 is a project-specific extension.
- **三层规则与眯眼测试**（nothing-design 竞品研读 2026-10-20）：每屏**恰三层**重要性——primary（唯一的一眼之物：数字/标题/状态）、secondary（语境：标签/描述，紧贴 primary 8–16px）、tertiary（元数据：边缘/底部，可见但永不竞争）。**眯眼测试**：眯起眼仍能说出最重要的是哪个；两物相争 = 一物缩小/变淡/挪位。警惕"全部 secondary"平底——均匀字号+均匀间距 = 视觉平坦，敢让 primary 大到夸张、tertiary 小到克制，**对比本身就是层级**。
- **字体纪律决策表**（同源）：区分两物时先选通道再动手——标题vs正文=**字号**；标签vs值=**颜色**；激活vs未激活=**颜色**；区题vs内容=**字号±字重**。"伸手要新字号时多半是间距问题"——先加距离。每屏预算：≤2 字族 / 3 字号 / 2 字重（display 密集场景可超，超了在 design-notes 记录理由）。
- **反差极端律**（官方 frontend-aesthetics cookbook 2026-10-22 量化）：字重配对用极端档——**100/200 对 800/900，不用 400 对 600**（display vs 正文）；字号跳变 **≥3x 不用 1.5x**（soft-premium 卡 ≥3 倍律的官方互证）。配对配方：display+mono（数据感）、serif+几何 sans（编辑感）；候选池 JetBrains Mono/Fira Code、Playfair/Fraunces、Bricolage Grotesque/Newsreader。
- **第二阶收敛警告（Space Grotesk 陷阱）**（同源原话："You still tend to converge on common choices (Space Grotesk, for example) across generations"）：反默认字体自己会变成新默认——选字时对照「这一代的反默认清单」（Inter→Space Grotesk→?），连"独特字体"也要查它是否已是集体的独特

## 2. Font stack (licensing-safe)

```css
--font-sans: system-ui, -apple-system, "Segoe UI", Inter, Roboto,
             "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans SC", sans-serif;
--font-mono: ui-monospace, "SF Mono", "Cascadia Code", Consolas, "JetBrains Mono", monospace;
```

- SF Pro / Segoe UI are **OS-served via stack references only** — never self-host, never convert to woff2 (Apple EA1370 / Microsoft FAQ restrictions). Inter (OFL-1.1) is the only self-hostable cross-platform substitute.
- `font-display: swap` if self-hosting Inter; prefer variable font.

## 3. CJK rules (Chinese/Japanese/Korean — apply when content is CJK)

These are craft conventions from Chinese product practice (marked 经验值; not from a single authority):
- **CJK 字体授权三级**（chinese-font-selector 80★ 竞品研读 2026-10-20）：**T0** 开源铁稳可嵌入（思源黑/宋、霞鹜文楷、得意黑、未来荧黑）｜**T1** 厂商承诺免费商用、留存授权声明（阿里普惠体、MiSans、站酷系）｜**T2** 慎用——**微软雅黑/苹方交付印刷或网页嵌入 = 侵权风险**（系统字体≠免费字体）；文泉驿系 GPL 感染争议、汉仪仅限平台内免费、**无授权声明一律视为不可用**。授权状态会变（厂商有收回先例），交付时注明检索日期。
- **中英混排显式声明英文字体**：不声明则英文被中文字体内置拉丁字形渲染，廉价感拉满；中文加 `italic` 是浏览器合成假斜体（faux-italic，同 §3 faux-light 禁令逻辑）；**全量中文字体 3–10MB 会卡死首屏**——子集化（subset）或按需加载是交付纪律。
- **Internationalized text**: allow labels and controls to expand in translation; avoid fixed widths and sentence fragments assembled from separately translated strings. Test representative languages and scripts with real content, including font coverage and line height.
- **Chinese line length and font pairing**: evaluate Chinese line length by character count instead of applying Western `ch` assumptions. Choose Latin and Chinese typefaces by visual fit and legibility, and test the pair with actual content. Use appropriate line breaking so punctuation does not strand at line edges.
- Body line-height **1.7–1.9** for Chinese (Western 1.5–1.6 is too tight — CJK glyphs fill the em box). Headings 1.3–1.4.
- Letter-spacing: keep 0 for Chinese body; add `0.02–0.05em` only for large Chinese display sizes if tracking feels dense.
- **中西文混排**: leave a thin space between CJK and Latin/digits (CSS `text-autospace` is not portable — insert hair spaces in copy or rely on the editor); numbers and Latin inside Chinese text read better in the same font's proportional glyphs.
- Weight ladder: Chinese fonts often lack true 300; use 400 body / 500-600 emphasis / 700 headings. Avoid faux-light (browser synthesizes it badly). Noto Sans SC variable is the reliable web self-host (OFL).
- Punctuation: 中文全角标点悬挂处理 at paragraph edges where possible; avoid `text-align: justify` on Chinese body text without `text-justify: inter-ideograph` control — rivers of gaps.
- Don't letter-space ALL-CAPS treatment onto Chinese (no caps exist); emphasis via weight or color, never underline (underline = link semantics).
- Numbers in Chinese text: prefer proportional Latin numerals; in tables use `tabular-nums`.

## 4. Data & code typography

- All numeric columns: `font-variant-numeric: tabular-nums`; right-aligned in tables.
- IDs, hashes, timestamps, code, log lines: mono stack, never proportional.
- Prices: show currency symbol consistently; decimals to 2 places (accounting contexts: exact, never rounded for display).

## 5. i18n guardrails

- 200% zoom without horizontal scroll (WCAG 1.4.10); never clip text containers with fixed heights.
- `lang` attribute set correctly (`zh-CN` etc.) — it changes font selection and line-breaking.
- RTL: use logical properties (`margin-inline-start`, not `margin-left`) from day one — retrofitting is painful. **段落按自身语言对齐而非上下文方向**（HIG RTL 2026-10-18：混排时 LTR 段落保持左对齐、RTL 段落保持右对齐）；**非方向性图片不翻转**（箭头/时间线图标翻转，照片/插图不翻转）。
- Minimum body 16px on mobile; secondary text ≥ 13px; never rely on color alone for emphasis.

## 5a. Microcopy rules (HIG Writing, 2026-10-18)

These rules govern the **words themselves** — complementary to the visual typography rules above (which govern how text looks, not what it says).

- **Buttons use verbs**: "Send" not "Let's do it!" — action-oriented, clear, no cute overrides.
- **Links are descriptive**: never "Click here" — screen reader users navigate by link text alone.
- **Placeholder is not a label**: placeholder disappears on input — every field needs a visible label (cross-ref product.md §4b).
- **Voice consistent, tone contextual**: app voice is stable (banking = trust vocabulary); tone shifts by situation (error = direct, achievement = congratulatory).
- **获奖 ≠ 可用**（同源研究实测）：usability 是唯一不随总分上升的评分线——顶级获奖站的 gate/preloader/小字/隐藏导航恰是反模式，别抄
- **编号装饰仅当真序列**（Anthropic 官方溯源 2026-10-20）：01/02/03 式编号只在内容真是序列（步骤/时间线）时使用——装饰性编号是把"结构装置"当贴纸
- **Capitalization**: pick one style per UI element type (e.g. sentence case for all headlines) and apply consistently across the entire deliverable.
- **类型动词与三连形容词**（taste/ux-ui 双源 2026-10-20）：unlock/unleash/supercharge/elevate/empower/streamline/seamless/effortless/robust/cutting-edge/next-generation/world-class/all-in-one/blazing fast 是类型信号；**三个抽象形容词连排（"Powerful, intuitive, and beautiful"）= 填充**——说出一个具体可验证的东西。过度对冲的微文案（"您或可考虑也许…"）直接说：动词前置。
- **微文案三律**（官方 frontend-design 2026-10-22）：①CTA 说结果不说动作（"Save changes" 非 "Submit"，动作名跨流程一致）②报错说清发生了什么+怎么修，**不道歉** ③空状态邀请行动；文风=平实动词+sentence case+零填充
- **mono 数据标签的域边界**（官方校准组⑤ precision）：等宽字体数据标签是 instrument 流派语法（linear-instrument 卡内一等公民）；在泛用模板页上它是「chrome 装扮」——mono 用在真数据上，不用在装饰性标签上。**光学尺寸修正**（kumo-design 厂商纪律 2026-10-22）：行内 mono 混排时降到 **~0.9em**——等宽字面大于同号比例字，不降则视觉抢行
- **Recreation prompts**: describe the observed layout, content, and interactions when reproducing a reference. Reserve broad style adjectives for deliberate design variations, where the goal is exploration rather than fidelity.
- **claims-first 起草**（taste-skill copy.md 竞品研读 2026-10-20）：营销页先写纯文本再写标记——每段一条 claim + 其 proof（图/数字/名字/演示）列成清单；**无 claim 的段 = filler，删**。"需要四行才能说完的标题，排版救不了它。"
- **本地化格式化与翻译保护**（Vercel web-interface-guidelines 竞品研读 2026-10-20）：日期/时间走 `Intl.DateTimeFormat`、数字/货币走 `Intl.NumberFormat`——不硬编码格式；语言检测用 `Accept-Language`/`navigator.languages` 而非 IP；品牌名/代码 token/标识符包 `translate="no"` 防机器翻译打碎。
- **Fewer words when possible**: "check each word to be sure it needs to be there" (HIG Writing). Read-aloud test.
- **Plain language for everyone**: no jargon, no gendered terminology, localization-ready. Avoid idioms that break in translation.
- **Content is not design**（Ilm-Alan/frontend-design 竞品研读 2026-10-18）: every string on screen must either name real information from the product, or be authored content that knows what it is — headline, button label, legal body, form field name, sample data that reads as sample. What's forbidden is content pretending to be something it isn't — filler labels ("Lorem ipsum"), vague microcopy ("Learn more" without context), themed replacement for standard UI copy. **工程学理由**（addyosmani frontend-ui-engineering 竞品研读 2026-10-20）：占位文本**掩盖真实内容暴露的布局问题**（长度/换行/溢出）——lorem 看着没问题恰因为它没内容。
- **画面禁出现制作过程元说明**（oil-ui 竞品研读 2026-10-20）："示例数据""按钮未接入""仅保存在本机"这类原型工序标签不进画面——mock/未接入性质在 design-notes 交付说明里交代，不在 UI 上自我注释；也不伪造业务成功、客户评价或产品指标。**仲裁注记**：science-research.md 的占位图"示意"标注不与此冲突——那是**数据诚实性**要求（统计图假装真实数据 = 学术失信），本条管的是**工序说明**（"这按钮还没接后端"之类），两者语义不同。
- **官方分平台字号表（HIG Typography, 2026-10-18）**：iOS/iPadOS 默认 17pt/最小 11pt；macOS 13/10；tvOS 29/23；visionOS 17/12；watchOS 16/12。本 skill 地板（16px 正文/13px 次级）严于官方最小值——维持。

## 5b. Image & asset discipline (2026-10-20)

These rules govern the **images themselves** — complementary to §5a (words) and to the visual rules (how images look).

- **Never invent an image URL**: fabricated stock-photo links are delivery-level defects — they 404 in front of the user. A URL you have not verified does not ship; say so in design-notes instead.
- **描边与图标语法**（make-interfaces-feel-better 竞品研读 2026-10-20）：图像加 1px 低透明度描边时，浅色模式**纯黑** `oklch(0 0 0 / .1)`、深色模式**纯白**——带色中性色会拾取底色读作脏边；图标笔画配相邻文字视觉重量（400 字重配 1.5px、600 配 2px），一套图标一个笔画粗细，`currentColor` 着色（状态靠 color/opacity 不靠换资产），outline 为默认、fill 标激活。
- **CLS 与加载纪律**（同源）：`<img>` 显式 `width`/`height`（防布局位移）；首屏关键图 `fetchpriority="high"`，折叠下 `loading="lazy"`
- **开放收藏优先 + 页面署名**（Leonxlnx/taste-skill 99617★→100.8k★，2026-10-22 升级为六级来源链）：①项目自有照片 → ②有工具则生成 → ③**真实档案图**（Wikimedia Commons / Openverse / 芝加哥艺术馆 / The Met，仅 PD/CC0/CC BY/CC BY-SA）→ ④品牌色代码绘制 → ⑤诚实泛用图 → ⑥纯字色。检索原则：**搜题材清单不搜类目**——搜它的街道/老地图/材料/行业版画，不搜"咖啡 shop 照片"；每张档案图**下载 + 页面署名 + 报告登记**（署名是许可条款不是礼貌），**绝不冒充客户自有产品/房间/人物/团队**，页面不写出处说明性文字（小字 credit 足够）。**真图 floor：≥4 张**（SVG 绘制不计入），通常 6-12
- **Real photos** (hero/lifestyle/texture): cite from stable free sources (Unsplash/Pexels/Pixabay) with the **full direct-URL pattern including size params** (`…?w=1920&q=80`), ready-to-paste `<img>` + descriptive `alt` that names the actual content (cross-ref §5a content-is-not-design — "image1" or marketing-fluff alt is filler).
- **Generative/conceptual art**: ship the prompt, not a fake link — wrap it in a marked block (`[IMAGE PROMPT START] … [IMAGE PROMPT END]`) so the user can run it through their image tool; preview renders a labeled placeholder (`示意` marker, science-research.md 占位图 rule is the domain-tight version).
- **No verified asset available** → ship an SVG/CSS placeholder that matches final layout proportions (never a broken `<img>` or a stretched gray box); record the intended art direction in design-notes.
- **Generated imagery**: match image style to the brand, content, and audience. When several generated assets need to feel like one set, keep their shared style instructions consistent and review the outputs together. Illustration, photography, and stylized 3D each suit different products; choose from the brief rather than a fixed default.
- **矢量优先资产律**（Trae 生产律 2026-10-23："MUST use SVG instead of binary formats"）：图标/插画/几何装饰一律 SVG 矢量（缩放无损+可 currentColor+体积小）；位图仅用于摄影级内容（六级链管辖）——「需要一张图」先问「它是照片吗」，不是就走 SVG
- **Every image earns a purpose**: hero = focal point, card media = information, texture = atmosphere — an image that is none of these is decoration slop (cross-ref slop_scan texture rules).
- **单族字重阶梯**（ui-ux-pro-max typography.csv 行 58 编码之法深读 2026-10-24）：单字族系统用**字重-场景映射表**编码（如 Outfit 900 uppercase tracking-tighter=hero / 700 uppercase=按钮导航）——比配对更可复制（零第二族成本），配对库按 Mood 关键词×Best For 检索（"elegant,luxury"→Playfair+Inter）；**无障碍优先配对**=Atkinson Hyperlegible 单族双用（dyslexia-friendly 档）
- **色彩命名的语域选择**（meodai color-name-lists 18 系统深读 2026-10-24）：18 命名系统各有语域——技术/工业→RAL/ISCC-NBS（"vivid yellowish green"精确）；用户随口→XKCD/HTML（"ugly yellow"人感）；文化诗意→日本传统色/中国传统色（勿忘我色）；历史博物→Werner/Ridgway（公有领域）。**命名语域须匹配受众语域**——工程师看 RAL 式、消费者看 XKCD 式；同一 hex 跨系统查证避免语域错位
- **长 token 包裹律**（ui-ux-pro-max ux-guidelines.csv 行 111-113 深读 2026-10-24）：URL/标识符/用户内容**不得强制横向溢出**——`overflow-wrap: anywhere` + flex/grid 文本子项可收缩；用户放大/字号覆盖/间距覆盖下文字必须**仍可得**（流式尺寸 + 内容驱动高度 + 无单位行高；固定盒裁字=Critical）；必须截断时 ellipsis + **可见的完整路径**（主操作只显示成无解释的省略号=Critical）——与 1fr 消失陷阱（web.md）为同族容器病
- **标点细节**（Vercel web-interface-guidelines 竞品研读 2026-10-20）：省略号用 `…` 非 `...`（加载态文案同样以 … 结尾）；弯引号 “” 非 straight ""；数字与单位、修饰键组合用不换行空格（`10&nbsp;MB`、`⌘&nbsp;K`）
- **图像即设计源管线**（image-to-code/imagegen-skills 新源 2026-10-22）：用户提供设计图时，**图像是设计源、代码是翻译层**——先逐节系统研读（节型/视觉优先级/可读文字**逐字提取**/字型关系/间距/按钮组件/主色节奏），禁氛围式扫一眼；**忠实非灵感**——"The goal is not: inspired by the image"，禁简化成默认模板/压缩留白/拉平字型/换泛用配色；**禁裁剪**——细节视图重新生成独立图，裁剪破坏间距与字阶关系；歧义消解序：保设计语言→布局间距→组件族→气质→补一张细节图→重生成该节→最后才是最忠实的可构建版，**不用泛用默认匆匆填歧义**
- **克隆伦理律**（Same.dev 生产律 2026-10-23）：克隆/参照站点时禁碰登录页（钓鱼风险——要求提供已登录截图代替）与涉黄/涉隐私/法律灰区站点；克隆产出需向用户声明参照来源
- **假系统黑话 tell**（同源）：「00 orchestration layer」式伪技术标签——编号+系统名词的装饰性命名与 lorem 同罪；系统名必须指向真实存在的模块。**Meta-Label 扩展**（gpt-taste 交叉 2026-10-22，"BANNED FOREVER"）：「SECTION 01」「QUESTION 05」式 节名+编号 组合标签——节名自己说话，编号只属于真序列
- **粗而诚实 > 精而泛**（swiftui-design-skill 竞品研读 2026-10-20 "Junior Designer Mode"）：拿不到真素材时，干净的灰盒占位**优于**蹩脚的 AI 生图；粗但诚实的版式**优于**精但 generic 的成品。绝不交付编造的 SVG 插画或 emoji 图标硬充。
