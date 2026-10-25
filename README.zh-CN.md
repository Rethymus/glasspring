# glasspring

[English](README.md) · [简体中文]

**面向编码 Agent 的响应式网页设计工作流 Skill。**

Glasspring 包含一个 Skill 入口、静态设计参考卡和本地辅助工具。它引导编码 Agent 根据需求与现有设计系统，制作网页预览、整体改版、局部 UI 修改或界面审查。参考资料是静态内容；项目不会自动采集或逆向在线产品。

用户需求和现有设计系统优先，玻璃质感只是可选的视觉风格。

> 当前是公开源码预览，尚未通过稳定版发布门槛。Agent 宿主中的实际行为和独立效果评测尚未验证，隐私审查仅部分完成，第三方权利仍受阻。详见[发布门槛](docs/RELEASE-GATES.md)。

## 咖啡售卖页示例

下图是仓库中的虚构独立页面，供读者查看视觉和交互状态。它不是 Glasspring Agent 会话的输出，也不是评测结果。公开[评测协议](evals/protocol.json)中的计划咖啡任务引用了一份未随仓库提供的奶油色与陶土色配色输入，因此此页面不能复现为该任务的评测产物。购物袋只改变本地页面状态，不会下单或收款。

<table>
  <tr>
    <td align='center'><img src='examples/coffee-storefront/assets/preview-desktop.png' alt='虚构的 Morrow Coffee 售卖页桌面全页截图。' width='100%'></td>
    <td align='center'><img src='examples/coffee-storefront/assets/preview-bag-open.png' alt='页面打开了本地购物袋；仅显示小计，没有结账功能。' width='100%'></td>
  </tr>
  <tr>
    <td align='center'>桌面页面</td>
    <td align='center'>本地购物袋交互状态</td>
  </tr>
</table>

<details>
  <summary>查看移动端布局</summary>
  <p align='center'><img src='examples/coffee-storefront/assets/preview-mobile.png' alt='虚构的 Morrow Coffee 售卖页移动端全页截图。' width='320'></p>
</details>

在仓库根目录启动示例：

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

然后访问 http://127.0.0.1:8000/。示例的虚构内容与素材来源见[说明](examples/coffee-storefront/README.md)。

## Skill 引导的工作

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

安装后启动新的 Agent 宿主会话，检查它是否列出 Glasspring，并让它执行一项小任务。记录它是否读取已安装文件并遵循说明。文件复制成功本身不能证明 Skill 已被发现或实际生效。

示例任务：

~~~text
制作一个面向值班工程师的响应式事故仪表盘。严重级别筛选器必须能改变可见日志；暂停操作必须停止更新；加载中和无结果状态要清楚。主要控件应支持键盘操作。
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
| 最近一次完整样本套件 | **FAIL**：12 项 PASS、1 项对比度 FAIL、1 条预期负向控制、2 项网络 SKIP。样本项目未公开，因此当前无法重放，标记为 **INSUFFICIENT_EVIDENCE**。 |
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
