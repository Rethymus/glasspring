# glasspring

[English](README.md) | [简体中文](README.zh-CN.md)

glasspring 是面向编程智能体的前端设计 skill 与本地审查工具。

它引导智能体从网页设计 brief 生成响应式 HTML 预览、语义化 CSS 令牌和设计说明。配套本地工具可测量指定颜色对比度、检查输出结构、捕获截图并检查部分浏览器行为。

> **状态：公开源码预览版，尚非稳定发行版。** 部分工具有自动化检查，但目前没有独立研究证明 glasspring 能改善设计或任务结果。第三方内容的来源与授权审查仍未完成。详见[发布说明](PUBLICATION-NOTE.md)和[发布门槛](docs/RELEASE-GATES.md)。

## 项目功能

Skill 会根据产品类型、领域、平台和技术栈路由设计参考，要求智能体提出不同设计方向、构建网页预览、沿用或有意调整现有设计系统，并检查渲染结果。预期交付物为：

- `preview.html`：响应式网页预览。
- `tokens.css`：预览实际使用的语义化设计令牌。
- `design-notes.md`：brief 解读、设计选择、测量检查和限制说明。

当前主要交付是网页预览及其设计决策。本仓库不承诺为所有框架、部署环境或原生应用提供可直接上线的组件。

内置 `SKILL.md` 有鲜明的视觉取向：采用受 Apple 启发的材质与动效语言，并要求做出有辨识度的设计选择。这些内容属于设计指导，不是客观质量结论。只有在 brief 和既有设计系统允许的范围内才采用这一取向；半透明玻璃是可选效果，且不得用于高信任或数据密集区域。

## 不包含的功能

- 不会自动研究、采集、索引或逆向分析外部产品。领域卡片和风格卡片是静态设计参考，不包含完整来源记录，也不代表经过独立验证的设计发现。
- 不包含用于外部产品研究的自动化引擎、后端或部署服务；本项目不会调用 REA，也不实现其分析工作流。
- 不保证任何编程智能体都会发现或遵循此 skill。复制文件只能验证安装目录结构。
- 不声称完全符合无障碍标准，也不声称能带来可测量的设计提升。机械检查只覆盖部分条件，无法判断界面是否有用。

原定的研究到设计工作流尚未完成。目前实现没有版本化的产品采集流程，也没有把观察记录关联到设计卡片的证据记录。详见[可维护的项目范围](docs/ARCHITECTURE.md)和[评测说明](docs/EVALUATION.md)。

## 安装到测试项目

先克隆本仓库，并使用一次性或可丢弃的项目目录进行首次安装。

```sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
```

按所用终端的路径格式指定目标目录：

```sh
# macOS 或 Linux
node skills/glasspring/scripts/install.mjs --target "/path/to/project" --host codex
```

```powershell
# Windows PowerShell
node skills/glasspring/scripts/install.mjs --target "C:\work\project" --host codex
```

安装到 Claude Code 时，将 `codex` 替换为 `claude`。安装器会把 skill 复制到 Codex 的 `.agents/skills/glasspring` 或 Claude Code 的 `.claude/skills/glasspring`。目标目录不存在时会创建。除非指定 `--replace`，现有安装会保留；替换时会保留同级备份。`--dry-run` 可预览复制操作。安装器不会注册 MCP 服务，也不会修改全局配置。

安装后，在目标项目中启动新的宿主会话，确认 skill 是否可见，再尝试一个小任务。例如：

> 使用 glasspring 为值班工程师设计一个响应式事故仪表盘。保留现有品牌令牌；让严重级别筛选和暂停控制可以工作，并提供有用的加载态和空状态。

Windows、macOS 和 Linux 上的文件复制检查已在 CI 通过。全新宿主会话中的发现行为和模型执行情况尚未验证。使用未经验证的宿主或系统前，请查看[安装详情](INSTALL.md)。

## 验证工具

当前 CI 工作流使用 Python 3.12 和 Node.js 22，在 Windows、macOS 和 Linux 上运行以下检查：

```sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
```

检查实际生成的交付物时，可运行 `python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN"`，检查静态规则和输出结构。请把 `PATH_TO_RUN` 替换为输出目录，并使用当前终端支持的路径格式。该命令不验证所有交互，也不能证明设计质量。

截图和渲染探针需要 Chromium。`probe_render.py` 需要本地页面 URL；可用时会从 cdnjs 下载 axe-core 4.10.2。先在一个终端启动本地服务器，再在另一个终端运行探针：

```sh
python -m http.server 8000 --directory "PATH_TO_RUN"
```

```sh
python skills/glasspring/scripts/probe_render.py http://127.0.0.1:8000/preview.html
```

缺少浏览器、axe 或点击观察时，相关检查会标记未知或未通过，不会当作通过。这些定向探针不能证明完全符合 WCAG、交互行为完整或截图是最新的。

## 评测证据与未完成门槛

公开的[评测协议](evals/protocol.json)只有设计方案，尚未执行。协议中的 brief 已公开，因此它们只是公开试点，不是隐藏留出集。确认性比较需要一组在生成结束前未用于 skill 开发的新任务，并进行盲化的独立评审，同时记录视觉和任务结果。详见[评测说明](docs/EVALUATION.md)。

最近一次有记录的完整样本套件共 16 行：12 项 PASS、1 项真实对比度 FAIL、1 项预期负向对照，以及 2 项因网络依赖而 SKIP。样本文件没有包含在当前仓库中，因此无法从本仓库重现该次运行。其余状态见[发布门槛](docs/RELEASE-GATES.md)。

根目录 MIT 许可证只适用于贡献者有权授权的内容；它不能自动清除第三方文字、代码、截图或素材的授权问题。逐项来源审查仍未完成，详见[第三方声明](THIRD_PARTY_NOTICES.md)。

## 项目目录

| 路径 | 用途 |
|---|---|
| `skills/glasspring/SKILL.md` | 智能体工作流和文件路由入口 |
| `skills/glasspring/references/` | 静态领域、风格、平台、类型和令牌参考 |
| `skills/glasspring/scripts/` | 安装器、令牌与对比度工具、输出检查、截图和浏览器探针 |
| `skills/glasspring/assets/` | 说明模板、评审量表和视觉参考页面 |
| `tests/` | 针对部分失败边界的自动回归检查 |
| `evals/protocol.json` | 尚未执行的比较方案，不是评测结果 |
| `docs/` | 架构、评测、来源和发布状态说明 |

## 背景

[REA](https://github.com/morluto/rea) 促使项目关注证据导向的调查方式和 skill/工具分发。glasspring 不依赖 REA；比较使用的版本为提交 `41cf869949b82bd0f24d425f6557432ae3a63545`。详见[来源说明](PROVENANCE.md)。
