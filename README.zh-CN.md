# glasspring

[English](README.md) | [简体中文](README.zh-CN.md)

Glasspring 是面向编程智能体、以文件夹形式分发的前端设计 skill。它引导智能体从网页 brief 生成响应式 HTML 预览、语义化 CSS 令牌和设计说明；配套脚本检查部分代码与浏览器行为。

> **截至 2026-10-25 的状态：公开源码预览版；稳定发行门槛为 NO-GO。** 文件复制检查已通过，但全新宿主中的发现行为、独立有效性评测和第三方权利清查尚未完成。详见[发布门槛](docs/RELEASE-GATES.md)。

## 产品范围

Glasspring 适用于探索新的响应式网页或仪表盘、有意重设计现有网页界面，或检查生成的预览。除非 brief 明确要求重设计，现有项目的令牌和组件应作为起点。

Glasspring 生成的是预览，不是生产级组件库、部署系统或自动化的外部产品研究与采集系统。领域卡片和风格卡片是静态指导，不是完整的来源目录，也不是经过独立验证的设计发现。原生 App、游戏和小程序等非网页平台需求只生成网页预览，除非相应平台另行实现并测试。

Skill 带有受 Apple 启发的视觉取向。只有在 brief 和既有设计系统允许时才采用；半透明玻璃是可选效果，不用于高信任或数据密集区域。

## 预期交付物

- `preview.html` — 响应式网页预览。
- `tokens.css` — 供预览使用的语义化设计令牌。
- `design-notes.md` — brief 解读、设计选择、观察到的检查结果和限制。

## 安装和试用

克隆仓库，并先安装到一次性测试项目：

```sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
```

请将 `PATH_TO_PROJECT` 替换为当前终端可用的路径。安装到 Claude Code 时使用 `--host claude`。安装只负责复制文件，不能证明宿主会发现或遵循 skill。请启动新的宿主会话，确认 skill 出现在列表中，再尝试一个小任务。备份、试运行和已验证宿主矩阵见[安装说明](INSTALL.md)。

试用任务示例：

> 使用 glasspring 为事故响应工程师设计响应式事故仪表盘。保留现有品牌令牌；让严重级别筛选和暂停控制可以工作，并提供有用的加载态和空状态。

## 检查工具

当前 CI 工作流运行：

```sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
```

检查实际生成的结果时，可运行 `python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN"`。请将 `PATH_TO_RUN` 替换为实际生成目录。它检查部分静态规则和输出结构，不能证明设计质量或验证所有交互。

浏览器探针需要 Chromium。`probe_render.py` 使用本地页面 URL，并在可用时从 cdnjs 获取 axe-core 4.10.2。缺少浏览器、axe 或点击观察时，相关结果会保持为 `UNKNOWN` 或导致对应门禁失败，不会计作 `PASS`。这些检查不能证明完全符合 WCAG。

```sh
# 终端 1
python -m http.server 8000 --directory "PATH_TO_RUN"

# 终端 2
python skills/glasspring/scripts/probe_render.py http://127.0.0.1:8000/preview.html
```

## 证据与发布门槛

| 项目 | 记录状态 |
|---|---|
| 安装目录与文件复制检查 | 截至 2026-10-25，在 Windows、macOS、Linux CI 中为 `PASS`；未覆盖宿主行为 |
| 最近一次有记录的完整样本套件 | `FAIL`：16 行中 12 项 `PASS`、1 项真实对比度 `FAIL`、1 项预期负向对照、2 项网络依赖导致的 `SKIP`；总退出码为 1。样本未包含在仓库中，无法从本仓库重现该次运行 |
| 独立效能比较 | `NOT_RUN`；公开的 brief 是试点，不是隐藏留出集 |
| 全新宿主中的发现行为与任务表现 | `NOT_RUN` |
| 来源与第三方权利审查 | `BLOCKED` |

目前没有证据证明设计质量得到提升、支持所有智能体或完全符合 WCAG。根目录 MIT 许可证只适用于贡献者有权授权的内容，不能自动清除第三方文字、代码、截图或素材的授权问题。详见[评测说明](docs/EVALUATION.md)、[发布门槛](docs/RELEASE-GATES.md)和[第三方声明](THIRD_PARTY_NOTICES.md)。

## 仓库结构

| 路径 | 用途 |
|---|---|
| `skills/glasspring/SKILL.md` | 主工作流和参考路由 |
| `skills/glasspring/references/` | 静态领域、风格、平台、类型和令牌指导 |
| `skills/glasspring/scripts/` | 安装器、定向检查、截图和浏览器探针 |
| `skills/glasspring/assets/` | 说明模板、评审量表和视觉参考 |
| `tests/` | 针对部分失败边界的自动回归检查 |
| `evals/protocol.json` | 尚未执行的比较协议 |
| `docs/` | 架构、评测、来源和发布状态 |

## 许可证

请查看 [LICENSE](LICENSE) 和[第三方声明](THIRD_PARTY_NOTICES.md)。MIT 文件不授予贡献者无权许可的材料之使用权。
