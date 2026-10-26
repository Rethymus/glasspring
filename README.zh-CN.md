# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring 是一个项目级 Agent Skill，用于创建和审查响应式网页界面。**它会按任务路由到随附的设计参考，指导新页面制作或现有界面修改，并提供用于检查部分实现细节的本地工具。

该 Skill 遵循开放的 [Agent Skills 格式](https://agentskills.io/specification)；格式正确本身并不能证明某个宿主会发现或遵循它。

> **公开源码预览 · 稳定版 BLOCKED。** 第三方内容权利审查尚未解决；宿主中的任务行为和独立设计效果尚未得到验证。证据及解除条件见[发布门槛](docs/RELEASE-GATES.md)。

## 咖啡售卖页示例

下面的虚构 Morrow Coffee 售卖页是**参考 Glasspring 随附的指导和检查流程手工制作的示例**。它采用咖啡售卖页场景，但不是编程 Agent 的真实运行结果，也不是效果评测。[公开试点协议](evals/protocol.json)引用了仓库中未提供的输入，其中包括一份品牌配色，因此这个页面不是可复现的基准运行结果。购物袋只更新页面状态和小计，不会下单或收款；商品、文案和图片均为虚构。

<p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-desktop.png" alt="虚构的 Morrow Coffee 售卖页桌面全页截图。" width="100%"><br>1440px 桌面页面</p>

<p align="center"><img src="examples/coffee-storefront/interaction.gif" alt="五帧本地交互：初始页面、加入 House Blend、打开购物袋、增加数量，再移除商品。" width="100%"><br>本地购物袋交互演示</p>

<details>
  <summary>查看移动端布局和购物袋状态</summary>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-mobile.png" alt="虚构的 Morrow Coffee 售卖页移动端全页截图。" width="320"></p>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-bag-open.png" alt="已打开的购物袋，包含两件 House Blend、小计 36 美元和本地演示说明。" width="100%"></p>
</details>

在仓库根目录启动示例：

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

然后访问 http://127.0.0.1:8000/preview.html。可查看[预览源码](examples/coffee-storefront/preview.html)、[设计令牌](examples/coffee-storefront/tokens.css)和[设计说明](examples/coffee-storefront/design-notes.md)；[示例 README](examples/coffee-storefront/README.md)记录启动方式和限制。

## Glasspring 可以指导哪些工作

- **新建独立预览：**指导 Agent 生成 `tokens.css`、`preview.html` 和 `design-notes.md`，并在 `shots/` 下保存窄屏和桌面 PNG 截图。
- **整体改版：**在现有应用中修改，保留原有入口，并记录修改前后的证据。
- **局部 UI 修改：**沿用现有设计系统，只检查改动区域。
- **只读审查：**报告发现，不编辑文件。

新建预览和整体改版会按产品类型、领域或风格包、平台及技术栈路由参考。新建预览流程会要求 Agent 先提出三个不同方向，再选定一个实现；这是一条流程指令，不是效果提升的证据。随附参考的默认设计语言受 Apple 风格启发，但用户需求和既有设计系统优先，玻璃效果可选。

现有检查包括选定文字配色的对比度计算、启发式样式扫描、新建独立预览的输出契约，以及可选的浏览器截图和交互探测。浏览器工具会检查为具体任务或检查提供的 URL。可选的 stdio MCP 服务器会暴露部分检查；需要手动配置，且尚未验证其与生产宿主的集成。

设计参考是随 Skill 打包的指导资料；Glasspring 不会自动把线上产品观察转成新参考卡片。平台专用参考可以用于响应式网页预览的设计决策；当前仓库没有经过验证的原生 App、游戏或小程序代码交付流程。

## 安装与试用

请先安装到一次性项目。将 `PATH_TO_PROJECT` 替换为该项目的路径。审计使用的工具版本为 Node.js 22.14 和 Python 3.12；这是已测试版本，不代表最低版本要求。

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

安装到 Claude Code 项目时使用 `--host claude`。安装器会将 Skill 复制到项目内的 `.agents/skills/glasspring` 或 `.claude/skills/glasspring`。安装目录包含[适用于独立 Skill 的第三方声明](skills/glasspring/THIRD_PARTY_NOTICES.md)，但不会包含更完整的[仓库级权利审查](THIRD_PARTY_NOTICES.md)。通过文件复制检查不能证明宿主会发现或遵循 Skill。证据、备份/恢复和移除步骤见[安装与宿主验证](INSTALL.md)。

安装后，可在编程 Agent 会话中尝试以下任务：

~~~text
使用 Glasspring 为虚构品牌 Morrow Coffee 制作响应式售卖页。配色使用暖奶油色（#f8f3eb）、浓咖啡色文字（#35221b）和陶土色按钮（#93432d）。包含主视觉、三张商品卡，以及可用键盘操作的本地购物袋；加购和移除商品时更新数量与小计，不做下单或支付。使用目标项目已有素材；若缺少商品图片，请用 CSS 或内联 SVG 绘制简单插图，不下载外部素材。交付 tokens.css、preview.html 和 design-notes.md。检查 390px 和 1440px 布局，将窄屏和桌面 PNG 截图保存到 shots/，并报告无法执行的检查。
~~~

这是一条示例请求，不代表真实 Agent 运行，也不是复现上方手工示例的步骤。

## 检查与证据

在仓库根目录运行项目检查：

~~~sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
~~~

这些命令验证的是仓库代码，不会运行 Agent 设计任务。独立预览契约和浏览器检查需要满足相应输入及工具条件；浏览器探测需要 Chromium，可选的 axe 检查还需要网络访问。这些检查不评定整体设计质量、不证明使用 Skill 带来提升，也不代表完整符合 WCAG。

此前完整审计状态为 **FAIL / INCOMPLETE**：12 项 **PASS**、1 项真实色彩对比度失败、1 项精确预期负向对照、2 项 **SKIP**；对比度问题仍未解决。详情见[发布门槛](docs/RELEASE-GATES.md)。

当前宿主证据有限：一次全新 Codex 会话列出 Skill 元数据为 **PASS**，但读取安装后的 Skill 文件仍为 **UNKNOWN**；Claude 的发现和任务行为为 **NOT_RUN**。独立效果评测为 **NOT_RUN**。稳定版仍为 **BLOCKED**。详见[安装证据](INSTALL.md)、[评测与研究](docs/EVALUATION.md)、[发布门槛](docs/RELEASE-GATES.md)和[安全说明](SECURITY.md)。

## 安全、许可证与项目文件

工具以调用者权限运行，不是沙箱。浏览器探测可能执行目标页面代码；可选的 axe 检查会从 CDN 获取 axe-core。只对可信项目运行，并阅读[安全说明](SECURITY.md)。

仓库包含 [MIT 许可证文件](LICENSE)。保留的第三方文本、代码和素材仍未完成权利审查；许可证文件本身不代表这些内容已获授权。详见[第三方来源审查](THIRD_PARTY_NOTICES.md)。

- [可安装的 Skill](skills/glasspring/)：入口文件、路由参考、脚本和模板。
- [咖啡售卖页示例](examples/coffee-storefront/)：手工示例，不是基准评测证据。
- [架构说明](docs/ARCHITECTURE.md)、[评测说明](docs/EVALUATION.md)和[发布门槛](docs/RELEASE-GATES.md)：产品边界与证据。
- [来源说明](PROVENANCE.md)、[第三方来源声明](THIRD_PARTY_NOTICES.md)、[贡献指南](CONTRIBUTING.md)和[安全说明](SECURITY.md)。
