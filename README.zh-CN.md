# glasspring

[English](README.md) | [简体中文](README.zh-CN.md)

Glasspring 是用于设计和评审响应式网页界面的 Agent Skill。它会根据 brief 路由到少量产品类型、领域、平台和技术栈参考，再引导智能体通过语义化令牌、页面实现和定向本地或浏览器检查完成新预览或整体重设计。这些检查只提供特定规则的证据，不能证明整体设计质量。

> **截至 2026-10-25 的状态：公开源码预览版；稳定发行门槛为 NO-GO。** 文件复制检查已通过；隐私审查仅覆盖部分范围；全新宿主中的发现行为、独立效果评测和第三方权利清查尚未完成。详见[发布门槛](docs/RELEASE-GATES.md)。

## 工作方式

1. 先选择任务类型：新预览、整体重设计、微改动或仅评审。
2. 新预览或整体重设计只读取产品类型、领域、平台和技术栈中相关的少量参考。brief 未要求重设计时，沿用现有设计系统。
3. 实现或修改界面，检查相关视口，并运行与任务相称的检查。缺少浏览器或交互观察时要报告为覆盖缺口，不得记为 `PASS`。

## 范围与交付物

- **新建独立预览：** `tokens.css`、`preview.html` 和 `design-notes.md`。
- **整体重设计：** 修改现有应用及其令牌入口，并提供前后对比证据和设计说明；除非用户要求，否则不创建并行预览。
- **微改动或仅评审：** 保留现有系统，按任务采用适量检查。仅评审只报告发现，不改项目文件。

默认视觉指导带有受 Apple 启发的材质与动效取向。用户 brief、既有品牌系统和选定风格参考优先；玻璃效果是可选项。领域与风格参考是静态指导。仓库不包含带版本记录的真实产品采集流程，也没有经过独立验证的设计效果。原生 App、游戏和小程序等需求生成网页预览，除非相应平台另行实现并测试。

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
| 独立效果评测 | `NOT_RUN`；公开的 brief 是试点，不是隐藏留出集 |
| 全新宿主中的发现行为与任务表现 | `NOT_RUN` |
| 项目隐私审查 | `PARTIAL`：对 78 个受跟踪文本文件进行启发式扫描，未发现常见密钥或本地路径模式；未运行专用扫描器，也未完成二进制文件和 Git 历史的全面审查 |
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
