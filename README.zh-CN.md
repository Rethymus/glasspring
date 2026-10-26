# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring 是一个带有明确审美主张的项目级 Agent Skill，供编程 Agent 新建响应式网页预览、整体改版、局部 UI 修改或只读审查时使用。**它按产品类型、领域或风格包、平台和技术栈路由静态参考，并提供部分本地及浏览器检查脚本。默认材质与动效方向受 Apple 风格启发（不代表关联），玻璃效果可选；用户需求和既有设计系统优先。宿主发现和任务行为尚未完整验证，详见下文。新建独立预览采用 `tokens.css`、`preview.html` 和 `design-notes.md` 三文件约定。

参考库是静态内容。Glasspring 不会自动检查线上产品并将观察结果转成新的参考卡。

> 这是公开源码预览。第三方权利、独立效果评测、宿主行为和浏览器运行时依赖控制尚未解决，稳定版发布状态为 **BLOCKED**。详见[发布门槛](docs/RELEASE-GATES.md)。

## 咖啡售卖页示例

这个虚构售卖页是**手工按照 Glasspring 的参考和检查流程整理的示例**，依据下方自包含 README 任务制作；它不是[公开试点协议](evals/protocol.json)中的咖啡任务重放，因为该试点任务指定的配色输入没有纳入本仓库。这些图片展示的是示例页面，不是 Agent 宿主会话或效果评测结果。

页面、商品和文案均为虚构；主视觉、商品和植物素材由图像生成器为本示例生成。购物袋只在本地更新页面状态和小计，不会下单或收款。

<p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-desktop.png' alt='虚构的 Morrow Coffee 售卖页桌面全页截图。' width='100%'><br>1440px 桌面页面</p>

<p align='center'><img src='examples/coffee-storefront/interaction.gif' alt='五帧本地交互：初始页面、加入 House Blend、打开购物袋、再次加入同一商品，再移除商品。' width='100%'><br>本地购物袋交互演示</p>

<details>
  <summary>查看移动端布局和购物袋状态</summary>
  <p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-mobile.png' alt='虚构的 Morrow Coffee 售卖页移动端全页截图。' width='320'></p>
  <p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-bag-open.png' alt='已打开的购物袋，包含两件 House Blend、小计 36 美元和本地演示说明。' width='100%'></p>
</details>

在仓库根目录启动示例：

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

然后访问 http://127.0.0.1:8000/preview.html。[示例文件](examples/coffee-storefront/)包括页面、tokens 和素材来源记录；[设计说明](examples/coffee-storefront/design-notes.md)记录了手动检查及其范围限制。

## 工作流

| 请求 | 预期工作流 |
|---|---|
| 新建独立网页预览 | 选择相关参考，制作页面，并交付 `tokens.css`、`preview.html` 和 `design-notes.md` |
| 整体改版 | 在现有应用和 token 入口中修改，记录设计决定和修改前后的证据 |
| 局部 UI 修改 | 沿用现有设计系统，只检查受影响区域 |
| 只读审查 | 返回审查发现，不改文件 |

## 指令的工作方式

- **选择参考：** 核心路由最多使用三份设计参考；若选择风格包，则替代领域包。相关任务指南和平台适配文档可能增加读取文件。
- **选择设计方向：** 对新预览或整体改版，指令要求 Agent 先考虑三个不同方向，再选定一个开始制作。这是指令规定的流程，不是经独立评测验证的设计质量结论。
- **制作并检查：** 新建预览遵循三文件约定；整体改版沿用现有应用和 token 入口。辅助脚本可以检查选定的对比度组合和静态模式；输出契约检查只适用于新预览。所需浏览器工具可用时，还能捕获或探测选定页面状态。
- **了解边界：** 默认材质和动效建议受 Apple 风格启发，具体以用户需求和现有设计系统为准；玻璃效果可选。对于原生 App、游戏和小程序，当前工作流提供网页预览，除非另有已实现并测试的平台版本。检查工具不评定整体设计质量，也不认证完整符合 WCAG。可选 MCP 注册需要手动配置，生产宿主集成尚未验证。

产品边界见[架构说明](docs/ARCHITECTURE.md)；来源与授权问题见[来源说明](PROVENANCE.md)和[第三方来源声明](THIRD_PARTY_NOTICES.md)。

## 安装与试用

先克隆仓库，并预览安装到一个临时项目。将 `PATH_TO_PROJECT` 替换为本机有效路径：

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

安装到 Claude Code 项目目录时使用 `--host claude`。安装器会将文件复制到 Codex 的 `.agents/skills/glasspring` 或 Claude Code 的 `.claude/skills/glasspring`。文件复制检查不能证明宿主会发现或遵循 Skill。当前证据和备份/恢复说明见[安装与宿主验证](INSTALL.md)。

记录中的项目检查使用 Node.js 22 和 Python 3.12。浏览器探测需要 Chromium；axe 检查还会从 CDN 获取 axe-core。

安装后，在编程 Agent 会话中尝试以下任务：

~~~text
使用 Glasspring 为虚构品牌 Morrow Coffee 制作响应式咖啡售卖页。配色使用暖奶油色（#f8f3eb）、浓咖啡色文字（#35221b）和陶土色按钮（#93432d）。包含主视觉、三张商品卡，以及可用键盘操作的本地购物袋面板；加购和移除商品时更新数量与小计，不做下单或支付。只使用目标项目已有素材；若没有商品图片，请用 CSS 或内联 SVG 绘制简单插图，不下载外部素材。交付 tokens.css、preview.html 和 design-notes.md。检查 390px 与 1440px 布局，并报告无法执行的检查。
~~~

## 检查和当前证据

在仓库根目录运行工具和打包检查：

~~~sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
~~~

对新建预览的运行目录，可检查产物结构和部分静态规则：

~~~sh
python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN" --skip-selftest
~~~

此命令运行静态扫描和新预览输出契约，不会重复执行辅助脚本自检。该契约不适用于沿用现有文件路径的整体改版；改版应保留应用结构并提供修改前后的证据。检查包或工具链时再运行上方的自检命令。这些检查不会运行编程 Agent，也不能证明 Skill 能提升设计效果。`probe_render.py` 的 axe 检查需要 Chromium 和网络连接来获取 axe-core；若该覆盖不可用或被跳过，且没有其他已观测失败项，结果为 `UNKNOWN`（若其他检查失败则为 `FAIL`）。

| 范围 | 已记录状态 |
|---|---|
| 已发布的 `main` 快照 CI（`2ce478c`） | Windows、macOS 和 Ubuntu 检查为 **PASS**；CI 检查仓库工具，不运行 Agent 会话。[运行记录](https://github.com/Rethymus/glasspring/actions/runs/40198893762) |
| 历史完整审计套件 | **FAIL**：12 项 PASS、1 项对比度 FAIL、1 条预期负向控制、2 项网络 SKIP；共 16 行，退出码为 1。对比度问题仍未解决，样本输入为私有内容。 |
| 后续浏览器样本门禁 | **PASS（有限范围）**：11 个私有样本目录通过 390px 和 1440px 检查；0 FAIL、0 SKIP。样本未包含在仓库中，公开重放为 **INSUFFICIENT_EVIDENCE**。该结果没有解决历史对比度问题，也不能证明设计质量。 |
| 宿主行为 | **PARTIAL**：一次 Codex 会话列出 Skill 元数据（**PASS**）；读取已安装文件及任务行为仍为 **UNKNOWN**；Claude 发现和任务行为为 **NOT_RUN**。 |
| 独立效果评测 | **NOT_RUN**；公开试点不是留出集，且任务引用的配色和组件库输入缺失。详见[试点协议](evals/protocol.json)和[评测说明](docs/EVALUATION.md)。 |
| 隐私 / 第三方权利 / 浏览器运行时 | 分别为 **PARTIAL / BLOCKED / OPEN**。详见[安全说明](SECURITY.md)、[第三方来源声明](THIRD_PARTY_NOTICES.md)和[发布门槛](docs/RELEASE-GATES.md)。 |

这些结果不能证明支持所有 Agent、提升设计质量或完整符合 WCAG。[评测说明](docs/EVALUATION.md)记录了研究背景和后续评测计划。

## 安全与项目文档

工具以调用者权限运行，不是沙箱。浏览器探测可能执行目标页面代码，并在运行时下载 axe-core。只对可信项目运行，并先阅读[安全说明](SECURITY.md)。

- [Skill 入口和路由参考](skills/glasspring/)
- [设计工作流与边界](docs/ARCHITECTURE.md)
- [评测计划与基准研究背景](docs/EVALUATION.md)
- 来源与素材审查：[PROVENANCE.md](PROVENANCE.md)、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- 安装、贡献和安全说明：[INSTALL.md](INSTALL.md)、[CONTRIBUTING.md](CONTRIBUTING.md)、[SECURITY.md](SECURITY.md)

仓库根目录的 [MIT 许可证](LICENSE)仅适用于贡献者有权许可的项目原创内容，不代表第三方文本、代码或素材已获授权。
