# 📋 用户收尾清单（glasspring 项目 — 全部代理工作已完成）

> 生成：2026-10-16。代理可执行的开发与验证已 100% 完成并留痕（总览见 `evals/results/n6-audit.md` 审计终版）。
> 剩余 2 项均需**你的**操作或决策。完成任意一项后回到主会话说一声，我立即处理对应收尾。

## ① 终审确认（约 5-10 分钟）

审阅以下材料后给出结论（通过 / 指出具体不满意点）：

| 看什么 | 在哪 |
|---|---|
| 跨会话触发测试总表（7 条语句 × 两轮） | `evals/trigger-cross-session.md` |
| 对照评分与单项验证结论（run6-run29，24 轮） | `evals/RESULTS-INDEX.md`（**终审导航索引**，逐轮一行带路径）或 `evals/results/` 各 `RUBRIC.md` |
| 实际产出截图 | `evals/results/` 各 run 的 `shots/` 与 `pulse-restyle/`、`miniprogram/design-preview/`、`p3-style-gallery/` |

- **通过** → 我完成 G4 终判定稿，项目全量收官。
- **不满意** → 请指出**具体产出 + 具体方面**（如"run9 配色太暗""结算页布局松散"），我定向迭代后再次请你复审。

## ~~② npm 发布~~ 【已永久关闭，2026-10-17】

用户明示：**不再询问 npm 发布，没有任何相关计划。** 此项永久关闭，后续不再提出。skill 唯一分发路径为 `scripts/install.mjs`（本地树复制），README 中的 Publishing 预案已删除。

## ② Aionis 备份节奏确认（一句话即可）

核查发现 `F:/ZCodeData/Aionis/data/backups/` 有每日 ~19:02-19:07 的 ledger 备份与 repo bundle——**如果这是你 Aionis 应用自身的定时行为，回复"是"即关闭此项**；如果不是（你不明来源），告知后我深入追查是否与其他工具有关。

## 背景速览

- skill 位置：`.agents/skills/glasspring/`（**14 领域包 + 8 风格包 + 4 类型/平台包 + 3 平台适配器** + 9 个带自测锚点的脚本（含 doctor 一键体检 / verify_output 机械契约检查） + 交互态截图 + 身份验证 + 风格画廊 + DTCG 发射 + 调色板引擎 + 安装器）
- 验证战绩：GP1 五轮回归全 14/14；GP2-GP5 对照 +6/+5/+6/+4；**领域包 GP 实测 14/14 全矩阵完成**（含 finance/devtech/social/travel/regulated/industrial/ecommerce/productivity 收官批）；风格包 GP 实测 **7 家族七连通过**（linear/notion/swiss/brutalist/editorial/dark-academia/organic）；G4 触发测试 FAIL→修复→PASS 闭环；**7 个真缺陷**由测试体系抓出修复（最新：slop_scan v2.1 规则空转 NameError，主会话独立复核发现并全量回归 0 hard）；5 轮回灌循环全部落地；slop_scan v2.1（20 条规则 + 20 命中/14 防误报双锚点）+ check_contrast --pairs 批处理 + palette --scaffold 风格起跑器 + verify_output 机械契约 + doctor 一键体检+ --expect-title/--click/--probe 交互态证据；风格画廊 8 家族目验通过
- 已封板/已关闭：**npm 发布（2026-10-17 用户明示永久关闭，不再询问）**、品牌 DNA 反推方法验证、作用域封锁硬规则（其他项目零写入已核实）
