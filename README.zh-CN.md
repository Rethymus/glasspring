# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring 是一个安装到项目中的 Agent Skill，面向响应式网页界面工作。**它通过指引 Agent 按产品类型、业务领域、平台和技术栈选择静态设计参考，并在需要时运行可选的本地或浏览器检查。新建独立预览时，交付 `tokens.css`、`preview.html` 和 `design-notes.md` 三个文件。

> 当前为公开源码预览。第三方权利、独立效果评测、宿主行为和浏览器运行时依赖尚未解决，稳定版发布状态为 **BLOCKED**。详见[发布门槛](docs/RELEASE-GATES.md)。

## 咖啡售卖页示例

这个虚构售卖页是**手工按照 Glasspring 的参考和检查流程整理的示例**，对应下方同一条任务简报，并遵循三件预览交付约定。它不是 Agent 宿主会话记录、独立效果评测，也不是尚不完整的公开试点协议重放。

页面、商品和文案均为虚构；主视觉、商品和植物素材由图像生成器为本示例生成。购物袋只在本地更新商品数量和小计，不会下单或收款。

<p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-desktop.png' alt='虚构的 Morrow Coffee 售卖页桌面全页截图。' width='100%'><br>1440px 桌面页面</p>

<p align='center'><img src='examples/coffee-storefront/interaction.gif' alt='五帧本地交互：加入咖啡、打开购物袋、将数量增加到两件，再移除商品。' width='100%'><br>本地购物袋交互演示，不代表 Agent 发现能力或评测效果。</p>

<details>
  <summary>查看移动端布局和购物袋状态</summary>
  <p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-mobile.png' alt='虚构的 Morrow Coffee 售卖页移动端全页截图。' width='320'></p>
  <p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-bag-open.png' alt='已打开的购物袋，包含两件 House Blend、小计 36 美元和本地演示说明。' width='100%'></p>
</details>

在仓库根目录启动示例：

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

然后访问 http://127.0.0.1:8000/preview.html。[示例文件](examples/coffee-storefront/)包括页面、设计 tokens、设计说明和素材来源记录。

## Glasspring 的用途

| 请求 | 预期工作流 |
|---|---|
| 新建独立网页预览 | 选择相关参考，制作页面，并交付 `tokens.css`、`preview.html` 和 `design-notes.md` |
| 整体改版 | 修改现有应用和 token 入口，并记录修改前后的证据 |
| 局部 UI 修改 | 沿用现有设计系统，只检查受影响区域 |
| 只读审查 | 返回审查发现，不改文件 |

工作指引要求每项任务最多读取三份设计参考；平台适配文档单独计算；只有使用半透明表面时才要求读取 `glass.md`。检查工具可以测量指定的对比度组合、扫描选定静态模式、验证交付结构，并在浏览器工具可用时捕获页面和探测选定的渲染/交互行为。

参考卡是静态资料。Glasspring 不会采集线上产品，也没有把调研观察自动转成设计指导的流程。默认材质和动效建议受 Apple 风格启发，用户需求和现有设计系统优先，玻璃效果可选。“Apple 风格启发”仅描述设计方向，不代表与 Apple 有关联。检查工具不评定整体设计质量，也不认证完整符合 WCAG。

对于原生 App、游戏和小程序，当前工作流会提供网页预览；只有另有已实现并经过测试的平台版本时才会输出对应平台实现。可选的 stdio MCP 服务提供部分辅助工具；注册需要手动配置，生产宿主集成尚未验证。

## 安装与试用

先克隆仓库并预览安装到临时项目。将 `PATH_TO_PROJECT` 替换为本机有效路径：

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

安装到 Claude Code 项目目录时使用 `--host claude`。安装器会把文件复制到 Codex 的 `.agents/skills/glasspring` 或 Claude Code 的 `.claude/skills/glasspring` 项目目录。项目检查使用 Node.js 22 和 Python 3.12；浏览器检查需要 Chromium。文件复制成功不能证明宿主会发现或遵循 Skill。备份、恢复和宿主证据见[安装与宿主验证](INSTALL.md)。

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

如果已有生成结果目录，也可检查产物结构和部分静态规则：

~~~sh
python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN"
~~~

这些命令验证部分辅助工具逻辑和打包行为；它们不会运行 Agent，也不能证明宿主会发现或遵循 Skill。`probe_render.py` 的 axe 检查需要 Chromium 和网络连接来获取 axe-core；跳过 axe 时覆盖范围会缩小。

| 范围 | 已记录状态 |
|---|---|
| 公开 `main` CI | 记录中的 Windows、macOS 和 Ubuntu 检查为 **PASS**；不包含 Agent 会话测试。[运行记录](https://github.com/Rethymus/glasspring/actions/runs/40198893762) |
| 历史完整审计套件 | **FAIL**：12 项 PASS、1 项对比度 FAIL、1 条预期负向控制、2 项网络 SKIP；共 16 行，退出码为 1。对比度问题仍未解决，样本输入未包含在仓库中。 |
| 后续浏览器样本门禁 | **PASS（有限范围）**：11 个私有样本目录通过 390px 和 1440px 检查；0 FAIL、0 SKIP。由于样本未包含在仓库中，公开重放为 **INSUFFICIENT_EVIDENCE**；该结果没有解决历史对比度问题，也不能证明设计质量。 |
| 宿主行为 | **PARTIAL**：一次 Codex 会话列出 Skill 元数据（**PASS**）；读取已安装文件及任务行为仍为 **UNKNOWN**；Claude 发现和任务行为为 **NOT_RUN**。 |
| 独立效果评测 | **NOT_RUN**；公开重放为 **INSUFFICIENT_EVIDENCE**。公开试点缺少提及的配色与组件库输入、固定的宿主/模型/预算，以及留出任务集。详见[评测协议](evals/protocol.json)。 |
| 隐私 / 第三方权利 / 浏览器运行时 | 分别为 **PARTIAL / BLOCKED / OPEN**。详见[安全说明](SECURITY.md)、[第三方来源说明](THIRD_PARTY_NOTICES.md)和[发布门槛](docs/RELEASE-GATES.md)。 |

这张表把工具检查、宿主行为和独立效果评测分开记录。当前证据不能证明设计质量提升、支持全部 Agent 或完整符合 WCAG。研究背景和评测计划见[评测说明](docs/EVALUATION.md)。

## 安全与仓库导航

工具以当前用户权限运行，不是沙箱。浏览器探针可能执行目标页面代码，并在运行时获取 axe-core。只对可信项目运行，并先阅读[安全说明](SECURITY.md)。

- [Skill 入口与路由参考](skills/glasspring/)
- [设计工作流和范围](docs/ARCHITECTURE.md)
- [评测计划和研究背景](docs/EVALUATION.md)
- 来源和素材审查：[PROVENANCE.md](PROVENANCE.md)、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- 安装、贡献和安全指引：[INSTALL.md](INSTALL.md)、[CONTRIBUTING.md](CONTRIBUTING.md)、[SECURITY.md](SECURITY.md)

根目录的 [MIT 许可证](LICENSE)仅适用于贡献者有权授权的项目自有内容，不会清除第三方文本、代码或素材的权利问题。
