# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring 是一个有明确设计立场的项目级 Agent Skill，面向响应式网页界面工作。**它引导编程 Agent 新建预览、整体改版、局部 UI 修改或只读审查，并按任务路由到随附的设计参考和选定的本地检查。默认指导采用受 Apple 风格启发的起点；用户需求和既有设计系统优先，玻璃效果可选。

本仓库遵循开放的 [Agent Skills 格式](https://agentskills.io/specification)；格式符合规范本身不能证明宿主会发现或遵循该 Skill。

> **公开源码预览 · 稳定版 BLOCKED。** 第三方内容权利审查仍未完成。详见[发布门槛](docs/RELEASE-GATES.md)。

## 咖啡售卖页示例

这是一个按 Glasspring 指导手工整理的示例，不是全新 Agent 宿主会话的运行结果，也不能证明 Skill 会提升效果。商品均为虚构；购物袋只在页面内更新状态，不支持结账或支付。[设计说明](examples/coffee-storefront/design-notes.md)记录了已检查和仍未验证的内容。

<p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-desktop.png" alt="虚构的 Morrow Coffee 售卖页桌面全页截图。" width="100%"><br>1440px 桌面页面</p>

<p align="center"><img src="examples/coffee-storefront/interaction.gif" alt="本地交互：初始页面、加入 House Blend、打开购物袋、增加数量，再移除商品。" width="100%"><br>本地购物袋交互</p>

<details>
  <summary>移动端布局和打开的购物袋</summary>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-mobile.png" alt="虚构的 Morrow Coffee 售卖页移动端全页截图。" width="320"></p>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-bag-open.png" alt="已打开的购物袋，包含两件 House Blend、小计 36 美元和本地演示说明。" width="100%"></p>
</details>

示例包含 **390px 和 1440px** 两种视口截图。记录显示：输出契约 **6/6 PASS**、样式扫描 **0 条发现**、选定对比度 **7 组 PASS**、Playwright 交互冒烟检查 **PASS**。禁用 axe 的渲染探测结果为 **UNKNOWN**（退出码 2）；自动化 axe 检查为 **NOT_RUN**。这些结果只适用于此示例。

在仓库根目录启动页面：

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

访问 <http://127.0.0.1:8000/preview.html>。可查看[预览源码](examples/coffee-storefront/preview.html)、[设计令牌](examples/coffee-storefront/tokens.css)和[完整检查记录](examples/coffee-storefront/design-notes.md)。

## Skill 可以指导哪些工作

- **新建预览：**生成 `tokens.css`、`preview.html`、`design-notes.md`，并在 `shots/` 下保存桌面和移动端 PNG。工作流要求实现前先提出三个不同方向。
- **整体改版：**在现有应用中修改，并记录修改前后的证据。
- **局部 UI 修改：**沿用已有设计系统，只检查改动区域。
- **只读审查：**报告发现，不编辑文件。

新建预览和整体改版会按产品类型、领域或风格、平台及技术栈路由参考。仓库包含选定配色的对比度计算、启发式样式扫描、新建预览输出契约检查、浏览器截图和交互探测，以及可选的 stdio MCP 服务器。MCP 需手动配置，尚未验证其与生产宿主的集成。

设计参考用于指导原则和模式，不是复制某个产品界面或素材的指令。Glasspring 不会自动把线上产品观察转成新的参考卡片。原生 App、游戏和小程序的代码交付不在已验证范围内。

## 安装与试用

请先安装到一次性项目。将 `PATH_TO_PROJECT` 替换为项目路径。记录中的检查使用 Node.js 22.14 和 Python 3.12；这不代表最低版本要求。

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

安装到 Claude Code 项目时使用 `--host claude`。安装器会将 Skill 复制到 `.agents/skills/glasspring` 或 `.claude/skills/glasspring`。文件复制检查不能证明宿主会发现或执行 Skill。安装限制、备份和移除方法见[安装与宿主验证](INSTALL.md)。

安装后，在新的编程 Agent 会话中试试：

~~~text
使用 Glasspring 为虚构品牌 Morrow Coffee 制作响应式售卖页。配色使用暖奶油色（#f8f3eb）、浓咖啡色文字（#35221b）和陶土色按钮（#93432d）。包含主视觉、三张商品卡，以及可用键盘操作的本地购物袋；加购和移除商品时更新数量与小计，不做结账或支付。使用目标项目已有素材；若缺少商品图片，请用 CSS 或内联 SVG 绘制简单插图，不下载外部素材。交付 tokens.css、preview.html 和 design-notes.md。检查 390px 和 1440px 布局，将移动端和桌面 PNG 截图保存到 shots/，并报告无法执行的检查。
~~~

这是一条示例请求，不是已记录的宿主运行或基准评测结果。

## 检查与当前证据

在仓库根目录运行本地检查：

~~~sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
~~~

这些命令检查仓库代码，不评定 Agent 生成的设计。现有项目证据仍有明确边界：

| 范围 | 状态 |
|---|---|
| 历史完整审计 | **FAIL / INCOMPLETE**：12 项 PASS、1 项真实对比度失败、1 项预期负向对照、2 项 SKIP；对比度问题仍未解决。 |
| 隐私审查 | **PARTIAL**：目前只有启发式文本扫描；未执行专用密钥扫描，也未完整审查二进制文件和 Git 历史。 |
| Codex 宿主 | Skill 元数据可见性 **PASS**；读取安装后的文件和任务行为 **UNKNOWN**。 |
| Claude Code 宿主 | 全新会话发现和任务行为 **NOT_RUN**。 |
| 独立效果评测 | **NOT_RUN (DESIGNED_NOT_EXECUTED)**；公开试点不是隐藏留出集，咖啡任务提到的随附配色也未包含在仓库中。 |
| 浏览器依赖完整性 | **OPEN**：axe-core 从 CDN 获取，尚无固定完整性校验值或离线覆盖策略。 |
| 稳定版发布 | 仍有未解除的发布门槛，状态为 **BLOCKED**。 |

证据和解除条件见[发布门槛](docs/RELEASE-GATES.md)、[评测说明](docs/EVALUATION.md)、[来源说明](PROVENANCE.md)和[第三方声明](THIRD_PARTY_NOTICES.md)。目前不宣称该 Skill 能提升设计质量、兼容所有 Agent 宿主或完全符合 WCAG。

## 安全与许可证

工具以调用者权限运行，不是沙箱。浏览器探测可能执行目标网页代码；可选的 axe 检查会从 CDN 下载 axe-core。请仅在可信项目中运行，并阅读[安全说明](SECURITY.md)。

仓库包含 [MIT 许可证](LICENSE)，但保留的第三方文本、代码和素材仍需完成权利审查。仓库许可证不会自动解决这些来源义务。

## 项目导航

- [可安装的 Skill](skills/glasspring/)：入口说明、路由参考、脚本和模板。
- [咖啡售卖页](examples/coffee-storefront/)：手工示例和检查记录。
- [架构](docs/ARCHITECTURE.md)、[评测](docs/EVALUATION.md)和[发布门槛](docs/RELEASE-GATES.md)：产品范围与证据。
- [贡献指南](CONTRIBUTING.md)、[安全说明](SECURITY.md)、[来源说明](PROVENANCE.md)和[第三方声明](THIRD_PARTY_NOTICES.md)。
