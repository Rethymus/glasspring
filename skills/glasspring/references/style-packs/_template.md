# 风格包模板（Style DNA Card Template）

> 用途：把任意产品/风格参照提炼为一张**可执行的 DNA 卡**。核心纪律（charter L3）：**重推导而非抄值**——视觉特征只提取定性参数（色相/明度区间/密度/圆角策略），精确值由 `palette_from_oklch.py` 从种子重推导并经 `check_contrast.py` 实测。
> Use the card structure and extraction steps below. Record sources and validation that are available to the user; do not imply that omitted research or examples were independently verified.

## 卡片结构

```markdown
# Style Pack: <名称>（<英文名>）

- **provenance**: basis=observation|official-docs|oss-design-system；借鉴层级（L1 原则/L2 结构/L3 重推导值/L4 资产禁用）；[Last verified: YYYY-MM-DD]
- **lifecycle**（ui-ux-pro-max styles.csv 治理模式 2026-10-24，可选）：status=active|superseded|deprecated；superseded/deprecated 必须写 successor 卡名（deprecated→replacement 重定向——用户点名旧名时路由到继任并声明）；卡间父子关系（如 soft-premium 三档共用家族头注）在此登记
- **observed-target**：写明观察对象及其版本语义。版本化产品需记录观察日期并在改版后重观察；设计流派则应注明其不是版本化产品，避免把历史风格误报为当前产品界面。
- **philosophy**: 核心一句话 + 3-5 个关键词
- **seed**: 主色相（deg）+ chroma 区间
- **tokens**: 引擎推导的色阶（贴 palette_from_oklch.py 输出）+ 密度/圆角策略/阴影族/动效性格
- **rules.always / rules.never**: 3-5 条可执行规则（含玻璃适配度判定）
- **accessibility_floor**: 实测通过的关键对比对（含数值）
- **validation**: 黄金 prompt 建议与已知限制
```

## measured_final（实测终值回写——必填）

对比度门禁与品牌感调整会**合法地**使最终语义色偏离种子。因此：
- 门禁通过后，将**最终采纳值**的 OKLCH（L/C/H 全量）与偏离原因回写本字段；
- 后续迭代以实测终值为基线，不再回到种子重推；若重推则更新本段并重测全部色对；
- 种子与终值都要保留：种子=设计意图，终值=交付事实。

## 提炼流程（rea 方法论落地）

1. **观察**：收集参照产品截图 ≥5 张（不同页面类型），按六维标注（材质/圆角/阴影/动效性格/排版性格/密度）。
2. **定性 DNA**：核心哲学一句话 + 关键词 + 性格轴（energy/formality/density/playfulness 0-10）；**取舍链**（taste-skill 408★ 竞品研读 2026-10-20 的 Taste DNA 字段）：3-4 条 **Trigger → Decision → Reason → Evidence**——什么触发情境下做了什么决定、为什么、证据是什么、**弃掉了哪个同样合理的替代**（"为何"与"弃了什么"才是 taste，光有特征值不是）；方向描述**禁空词**（干净/现代/高级/user-friendly），必须落到 px/hex/区间值。
3. **种子提取**：取其主色相与 chroma 区间（**不抄具体 hex**）。
4. **重推导**：`palette_from_oklch.py --hue <H> --chroma <C>` 生成色阶 → `check_contrast.py` 逐对实测 → 不合格升 L。
5. **成卡**：按上方结构写卡，provenance 注明观察 basis 与验证日期。
6. **验证**：用一个黄金 prompt 实战（GP 流程），域线索/风格线索命中 ≥3 才转正。
