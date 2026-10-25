# glasspring

[English](README.md) · [简体中文]

**Glasspring 是一个可安装的 Agent Skill，用于创建、改版和审查响应式网页界面。**新建页面时，它会引导编码 Agent 交付 `tokens.css`、`preview.html` 和 `design-notes.md`。它按产品类型、行业领域、平台和技术栈路由随仓库分发的参考卡，并提供部分检查工具。参考卡是静态内容；仓库没有内置在线产品调研及将观察结果转为设计指导的流程。默认设计语言受 Apple 风格启发；用户需求和现有设计系统优先，玻璃质感可选。

> 当前为公开源码预览，尚未达到稳定版发布条件。详见[当前证据与发布门槛](docs/RELEASE-GATES.md)。

## 咖啡售卖页示例

这个虚构咖啡售卖页展示了本地购物袋交互，不会下单或收款。

<p align='center'><img src='examples/coffee-storefront/assets/preview-desktop.png' alt='虚构的 Morrow Coffee 售卖页桌面全页截图。' width='100%'><br>桌面页面</p>

<p align='center'><img src='examples/coffee-storefront/interaction.gif' alt='五帧本地交互：加入咖啡、打开购物袋、更新数量并移除商品。' width='100%'><br>独立示例的交互录制；不是 Glasspring 会话产物或评测结果。</p>

<details>
  <summary>查看移动端布局</summary>
  <p align='center'><img src='examples/coffee-storefront/assets/preview-mobile.png' alt='虚构的 Morrow Coffee 售卖页移动端全页截图。' width='320'></p>
</details>

在仓库根目录启动示例：

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

然后访问 http://127.0.0.1:8000/。页面源码见[index.html](examples/coffee-storefront/index.html)，虚构内容和素材来源见[示例说明](examples/coffee-storefront/README.md)。

## Skill 中的任务模式

| 请求类型 | 预期工作 |
|---|---|
| 新建网页 | 制作响应式预览，交付 tokens.css、preview.html 和 design-notes.md |
| 整体改版 | 修改现有网页界面，检查改动状态并记录设计决策 |
| 局部 UI 修改 | 沿用现有设计系统，只检查受影响区域 |
| 界面审查 | 报告发现，不修改文件 |

对于原生 App、游戏和小程序，当前 Skill 会提供网页预览；除非另有经过实现和验证的平台版本。

## 工作流程

Glasspring 由说明和工具引导，不是托管式生成器。Agent 根据任务选择相关参考卡和辅助命令；最终仍由人审查结果并决定是否交付。

~~~mermaid
flowchart LR
    A['需求和现有设计系统'] --> B['选择相关参考卡']
    B --> C['编码 Agent 构建、修改或审查界面']
    C --> D['按需运行本地检查并截图']
    D --> E['人工审查和交付']
~~~

可选的 stdio MCP 服务可提供部分辅助工具。宿主注册需要手动配置，当前尚未验证在生产宿主中的集成。

这些检查只覆盖选定规则与行为，不会认证设计质量、所有交互或完整符合 WCAG。

## 安装与试用

先克隆仓库，再安装到临时项目。在仓库根目录使用 --dry-run 预览文件复制操作：

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

安装到 Claude Code 时使用 --host claude。将 PATH_TO_PROJECT 替换为本机项目目录。备份与恢复方式见[安装和宿主验证说明](INSTALL.md)。

安装器和检查已在 Node.js 22、Python 3.12 环境运行过。浏览器探针还需要 Chromium 和网络连接，以便获取 axe-core。

安装后启动新的 Agent 宿主会话，检查它是否列出 Glasspring，并让它执行一项小任务。记录它是否读取已安装文件并遵循说明。文件复制成功本身不能证明 Skill 已被发现或实际生效。

可以用以下任务试用 Glasspring：

~~~text
使用 Glasspring 为虚构品牌 Morrow Coffee 制作响应式咖啡售卖页。配色使用暖奶油色（#f8f3eb）、浓咖啡色文字（#35221b）和陶土色按钮（#93432d）。包含主视觉、三张商品卡，以及可用键盘操作的本地购物袋面板；加购和移除商品时更新数量与小计，不做下单或支付。只使用目标项目已有素材；若没有商品图片，请用 CSS 或内联 SVG 绘制简单插图，不下载外部素材。交付 tokens.css、preview.html 和 design-notes.md。检查 390px 与 1440px 布局，并报告无法执行的检查。
~~~

## 检查和当前证据

在仓库根目录运行本地检查：

~~~sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
~~~

这些检查验证部分辅助工具逻辑和打包行为；它们不会运行模型，也不能证明 Agent 会遵循 Skill。

如果已经有生成结果目录，也可以检查产物结构和部分静态规则：

~~~sh
python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN"
~~~

该检查不评估设计质量，也不会验证所有交互。

| 范围 | 已记录状态 |
|---|---|
| 主分支 CI | 记录中的 Windows、macOS 和 Ubuntu 检查为 **PASS**；不包含 Agent 会话测试。[运行记录](https://github.com/Rethymus/glasspring/actions/runs/40198893762) |
| 最近一次完整样本套件 | **FAIL**：12 项 PASS、1 项对比度 FAIL、1 条预期负向控制、2 项网络 SKIP；退出码为 1。样本项目未公开，因此当前无法重放，标记为 **INSUFFICIENT_EVIDENCE**。 |
| 宿主行为 | **PARTIAL**：一次 Codex 会话列出 Skill 元数据（**PASS**）；是否读取已安装文件及任务行为仍为 **UNKNOWN**；Claude 发现和任务行为为 **NOT_RUN**。 |
| 独立效果评测 | **NOT_RUN**。公开[协议](evals/protocol.json)不完整，缺少提到的配色和组件库输入，也没有固定宿主、模型和预算值；重放为 **INSUFFICIENT_EVIDENCE**。 |
| 隐私审查 | **PARTIAL**；详见[安全说明](SECURITY.md)。 |
| 第三方权利 | 尚待逐文件核对来源、许可证与授权，状态为 **BLOCKED**；详见[第三方来源说明](THIRD_PARTY_NOTICES.md)。 |
| 浏览器运行时依赖 | **OPEN**：浏览器探针从 CDN 获取 axe-core，未固定完整性校验值，也没有离线策略。 |

完整证据和发布门槛见[发布门槛](docs/RELEASE-GATES.md)、[评测说明](docs/EVALUATION.md)和[宿主验证](INSTALL.md)。

## 安全与仓库导航

工具以当前用户权限运行，不是沙箱。浏览器探针可能执行目标页面代码，并在运行时获取 axe-core。只对可信项目运行，并先阅读[安全说明](SECURITY.md)。

- [Skill 入口与路由参考](skills/glasspring/)
- [设计工作流和范围](docs/ARCHITECTURE.md)
- [评测计划和基准研究](docs/EVALUATION.md)
- 来源和素材审查：[PROVENANCE.md](PROVENANCE.md)、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- 安装、贡献与安全指引：[INSTALL.md](INSTALL.md)、[CONTRIBUTING.md](CONTRIBUTING.md)、[SECURITY.md](SECURITY.md)

根目录的 [MIT 许可证](LICENSE)仅适用于贡献者有权授权的项目自有内容，不会清除第三方文本、代码或素材的权利问题。
