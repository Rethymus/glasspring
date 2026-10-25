# shadcn-tailwind.md — stack bridge for shadcn/ui + Tailwind projects

> When to read: the target project contains `components.json` (shadcn/ui) or you're asked to style within a Tailwind + shadcn codebase. Before ANY styling work run `npx shadcn@latest info --json` — it reports the project's config, base (Radix/Base UI), and installed components.
> Last verified: 2026-10-17 against shadcn-ui/ui main (`skills/shadcn/SKILL.md` + `customization.md` + `rules/styling.md`). **FM-7 drift warning**: this registry evolves fast — re-check the live skill if the project pins a newer shadcn major.

## 0. Division of labor (the mental model)

shadcn distributes **components** (source code via CLI, `npx shadcn@latest add …`); glasspring supplies the **design language** (tokens, glass, motion, domain red lines). They compose: theme variables + our recipes, NOT custom markup. Never hand-roll a component that `npx shadcn@latest search` can find.

CLI scouting fallback: `npx shadcn@latest info` needs a complete project (tsconfig paths etc.); in partial checkouts or design-only engagements it may fail. Fallback: read `components.json` + the theme CSS directly, and record in design-notes that CLI scouting was unavailable. Never block the design work on the CLI.

## 1. Token mapping (our tokens.md → shadcn theme variables)

shadcn's theme model is semantic CSS variables in `:root` / `.dark` — **already OKLCH**, same as ours. Map, don't duplicate:

| glasspring token | shadcn variable | note |
|---|---|---|
| `--color-bg` / `--color-surface` | `--background` / `--surface` (or `--card`) | |
| `--color-text` / `-secondary` / `-tertiary` | `--foreground` / `--muted-foreground` | tertiary maps to muted too (their scale is coarser) |
| `--color-cta` / `--on-accent` | `--primary` / `--primary-foreground` | |
| `--color-accent` (hover/selection) | `--accent` / `--accent-foreground` | |
| `--color-danger` | `--destructive` / `--destructive-foreground` | status colors: use semantic tokens or `Badge` variants — never raw Tailwind colors (`text-red-600` is slop by their rules AND ours) |
| `--color-focus` | `--ring` | |
| `--radius-*` family | `--radius` | their single-var radius derives sm/md/lg/xl from it; collapse our family to it |
| charts | `--chart-1`…`--chart-5` | fill from our ramp (Okabe-Ito rule if science/medical) |

Emission: when restyling a shadcn project, DELIVER a `:root`/`.dark` variable block in their names (dark mode = `.dark` class toggle) + a diff of any component-level class changes — not a parallel tokens.css. Keep our naming as the source of truth in `design-notes.md`, their naming in the code.

## 2. Glass in shadcn projects

Glass is a **theme layer, not a component**: apply `backdrop-filter` + translucency to the existing component's surface variable (`bg-background/70` style translucency works — vars are OKLCH), never as a new custom markup wrapper. Same decision tree (glass.md §0) and same Tier 2 fallbacks; the fallback sets the variable back to opaque (`--background` solid). Trust-zone veto still wins: price tables, balances, legal text stay on `--card` solid even if the shell goes glass.

## 3. Their hard rules we inherit (overlapping discipline)

- `className` for layout only; **built-in variants before custom styles** (`variant="outline"`, `size="sm"`).
- Semantic colors only — mirrors our zero-hardcoded-color gate exactly.
- Composition red lines: `Dialog`/`Sheet`/`Drawer` always need a Title (a11y, matches our focus/a11y gate); `Avatar` needs `AvatarFallback`; no manual `z-index` on overlays; `Separator` not `<hr>`; `Skeleton` not `animate-pulse` divs.
- Motion: their components own their transitions — our springs apply to **page-level choreography and gesture-continuity** (spring_convert), not to overriding component internals.

### 3.1 · 2026-10-22 refresh deltas（skills/shadcn/SKILL.md 重抓）

- 间距禁 `space-x-*`/`space-y-*`——flex `gap-*`；等尺寸用 `size-10` 简写
- 表单走 `FieldGroup` + `Field` 体系（禁裸 div 排间距）；校验用 `Field` 上的 `data-invalid` + 控件 `aria-invalid` 双通道
- **第三方注册表组件 `add` 后必过检**：修硬编码导入路径/补缺失子组件/图标导入换项目 `iconLibrary`
- CLI 合并纪律：更新上游组件用 `add --dry-run --diff` 智能合并；**永不手抓 GitHub 源文件**、无用户明批永不 `--overwrite`
- **原语层迁移有官方技能**：仓库自带 `skills/migrate-radix-to-base`——Radix 老项目升 Base UI 走它（本文件 §1 token 映射与原语无关，迁移不影响 token 层）
- Follow the project's spacing scale and component APIs. When changing a surface color, check its foreground color together. Confirm the existing token format before wrapping a variable in a color function.

## 4. Brand-spec hook

If the project carries a `DESIGN.md` or brand spec, it is the brief: read it first, treat it as the seed source for `palette_from_oklch.py`, and note in design-notes that the spec outranks our default aesthetic. Their preset system (`--preset <code>`) is their own distribution channel — out of our scope unless the user asks for one.
