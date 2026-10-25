# Domain pack — productivity & B2B SaaS（CRM/HR/项目协作/文档 + 中后台横切）

> When to read: people operate software for work — CRM/ sales pipelines, HR/people ops, project management, docs/knowledge bases.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## Cross-domain grammar（已在中后台横切验证）

- Table is the protagonist: three row-height tiers, frozen columns, inline edit, right-aligned tabular-nums; record detail = header + tabs + related lists; batch bar appears on selection.
- Drawer for detail (not page-away); ⌘K palette; URL-synced views.
- Motion 2/5: skeleton→fade, drawer slide-in spring, everything else ≤150ms. Glass: nav/drawer/palette only — never rows/cells.
- Red lines: marketing aesthetics inside the back office; hover popovers covering the next row; hidden operations for beauty.

## Surfaces

### CRM / 销售（Salesforce/HubSpot 型）
- Pipeline kanban (WIP counts), lead→deal state machine, activity timelines; zero-friction lookup is the whole job — every extra click is tax.
- Components: record 3-part layout, global search, mass-email/sequence panels, forecast charts.

### HR / 招聘（Greenhouse/Workday 型）
- Dignity constraint: salary fields masked by default (reveal = audit-logged), no celebratory motion on rejections/layoffs, structured interviews as scorecards, candidate portal warm-toned vs admin cool.
- Components: approval inbox, interview scorecard, pipeline board per stage, audit timeline.
- Red lines: default-visible compensation of others; playful motion around terminations.

### 项目管理/协作（Asana/Linear 型）
- Multi-view same dataset (board/list/gantt/calendar), URL-synced; **the spring-heavy exception in B2B**: drag snap, cross-column drop, completion pop — physical object-ness is the domain mental model (motion 3/5).
- Detail drawer slides from the card; WIP limits visible; no reflow mid-drag.
- Red lines: >2 actions per card, view switch losing scroll position.

### 文档/知识库（Notion/Confluence/GitBook 型）
- Chrome disappears: content = interface; slash-menu block editor, breadcrumb + TOC, comments in sidebar (never modal over prose), version history always findable.
- Motion 2/5: block drag + menu spring; typing area zero motion; page switch <100ms.
- Components: infinite sidebar tree (drag to move), bidirectional links, suggested edits mode.
- Red lines: modals interrupting writing, auto-collapsing user-expanded sections, colored backgrounds in body.
