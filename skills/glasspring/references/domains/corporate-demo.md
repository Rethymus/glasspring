# Domain pack — corporate & product demo（企业介绍/产品演示）

> When to read: 企业官网（corporate introduction/about）与产品演示页（product demo/showcase）。后者是 **Apple 设计语言的主场——apple.com 产品页即本领域的教科书**，也是本 skill 的直系血缘。
> Last verified: 2026-10-16. Status: craft conventions from apple.com 产品页语法、中西方企业站惯例，标注【经验值】处为无单一权威来源的通行实践。

## 1. 企业介绍（Corporate Introduction）

### 结构语法（中西通用骨架）
Hero 宣言（一句话说清"我们是谁"）→ 业务板块（每块一图一句）→ 领导团队（照片+姓名+头衔）→ 发展历程（时间线）→ 新闻中心 → ESG/CSR → 全球网络/联系方式 → Careers。
- **应用片段须像真产品**（taste-skill 248 站研究 2026-10-20）：页面上展示的产品 UI 片段按 app-screen 规则真做——数据能对上、呈现一个具体发现、按页面版式当图处理；灰条与 lorem 数是最弱的画面， ruins 整页可信度。

- **信任靠真实**：设施/产线的真实摄影、领导团队真实照片与全名、注册实体与地址可查、认证证书展示——stock photo 人像堆是信任毒药。
- 中文企业站特有语法【经验值】：领导团队排序即组织语义（不可乱序）；发展历程大事件时间线；新闻中心按年份归档；国企/机构含党建专栏；中英双语切换一等公民。
- Motion 2/5：数字滚动（成立年份/员工数/覆盖国家）、板块淡入；克制——企业站的"稳"比"炫"值钱。
- Glass：hero 叙事层可用（企业愿景宣言之上）；领导团队/新闻列表实底。
- 红线：stock 味团队照、过期新闻置顶、领导排序随意、荣誉资质无证书编号。

## 2. 产品演示（Product Demo/Showcase）—— Apple 语法主场

apple.com 产品页的语法即本领域黄金标准，与本 skill 血缘一致：

- **Sticky scroll-telling**：一次一个特性——大标题（≤7 词）+ 一张图/一段交互，滚动逐章展开（scroll-driven animations 落地处）；章节间呼吸留白充足。
- **技术规格的克制**：完整规格收进底部可展开 "Tech Specs" 折叠区，正文只讲用户可感知的差异（"续航翻倍"而非毫安时）。
- **诚实演示**：交互 demo（颜色/尺寸选择器、live playground embed）用真实数据；**绝不伪造未发布功能的截图**，也不伪造业务指标（客户数/评分等看着像真业绩的数字须可辨为演示——或在页面语境自明、或在 design-notes 交代，FM-6 仲裁 2026-10-20：与 type.md §5a 画面禁制作元说明的分工是——**指标诚实性**须保，**工序标签**不进画面）。
- **对比模块**：型号并排对比（≤4 列），差异行高亮；规格用 tabular-nums。
- Motion 3-4/5（本领域唯一高动效豁免区）：scroll-driven reveals、参数切换交叉溶解、video 自动静音循环 ≤10s 一屏一个；reduced-motion 退化为静态序列图。
- Glass：导航 chrome Tier 1 可用（apple.com 即此用法）；产品大图区让位给内容。
- 组件语法：特性章节（chapter deep-dive）→ 规格折叠 → 对比模块 → CTA（购买/预约演示）；企业演示另加"预约 live demo"路径。

## 红线（两领域通用）

未发布功能的假截图；无规格支撑的特性宣称；自动播放有声视频；一屏堆叠 >1 个自动媒体；企业照/数据用 stock 充数。
