---
name: arco-design-vue-skill
description: "Arco Design Vue and Arco Design Pro Vue UI reference for @arco-design/web-vue. Use this skill whenever the user asks to build a page, create a dashboard, write frontend code, add a route, modify src/views pages, implement forms or tables, or develop any Vue 3 admin interface, especially when they mention Arco Vue, Arco Design Pro Vue, @arco-design/web-vue, a-button, a-table, a-form, Modal, Drawer, Menu, Pinia, vue-i18n, or Vite-based Arco admin scaffolds. Covers 70 component references plus project architecture, theming, i18n, responsive patterns, forms, tables, modals, and Arco Pro Vue workflow conventions."
---

# Arco Design Vue Skill Reference

`@arco-design/web-vue` with `arco-design-pro-vue` and `arco-design-pro-vite` project conventions.

## Critical Conventions

**Always follow these rules when writing Arco Design Pro Vue code:**

- **SFC pattern**: prefer Vue 3 single-file components with `<script lang="ts" setup>`.
- **Component usage**: when the app bootstrap already calls `app.use(ArcoVue)`, use Arco tags directly in templates such as `<a-button>`, `<a-form>`, `<a-table>`, `<a-card>`.
- **Icons**: when the app bootstrap already calls `app.use(ArcoVueIcon)`, use icons directly in templates such as `<icon-search />`, `<icon-plus />`, `<icon-refresh />`.
- **Styles**: do not add manual Arco global CSS imports when the project already uses the Vite Arco style plugin.
- **Date library**: prefer `dayjs`-compatible values and the existing project date format conventions.
- **State binding**: use `v-model` or explicit `v-model:<prop>` patterns such as `v-model:visible`, `v-model:active-key`, `v-model:selected-keys`.
- **Forms**: `a-form-item` uses the `field` prop for field names.
- **Page location**: put pages under `src/views/<domain>/<page>/index.vue`.
- **Routing**: register menu pages in `src/router/routes/modules/*.ts` using `AppRouteRecordRaw` and `DEFAULT_LAYOUT`.
- **Localization**: add visible page copy to locale files when the page already uses `$t(...)`.
- **Permission model**: preserve route `meta.requiresAuth`, `meta.roles`, and any `v-permission` checks.

## Skill Index

Load the relevant file below for Vue 3 examples, Arco Pro notes, and practical usage guidance.

For real business tasks, prefer this order:

1. `overview/*` to understand project structure
2. `patterns/*` to choose the right page or interaction pattern
3. `components/*` to look up exact component props, events, slots, and examples

### Setup and Configuration

| Topic | File | When to use |
|-------|------|-------------|
| Installation and Project Entry | [getting-started.md](references/overview/getting-started.md) | Bootstrapping Arco Vue in a Vite app, understanding `main.ts`, adding a new page, or orienting non-Vue teammates |
| Global Config | [config-provider.md](references/overview/config-provider.md) | Applying global size, locale, popup container, or component defaults with `a-config-provider` |
| Theming | [theming.md](references/overview/theming.md) | Theme tokens, light and dark mode, app store theme flags, and Arco theme color customization |
| Internationalization | [internationalization.md](references/overview/internationalization.md) | Adding locale keys, wiring page text with `$t(...)`, changing app locale, and structuring page locale files |
| Architecture | [architecture.md](references/overview/architecture.md) | Understanding layouts, routes, stores, API modules, mock bootstrapping, and the Arco Pro Vue file layout |

### General Components

| Component | File | Use for |
|-----------|------|---------|
| Button | [button.md](references/components/general/button.md) | Buttons, button groups, icon actions, loading actions |
| Icon | [icon.md](references/components/general/icon.md) | Built-in icons, action icons, icon-only controls |
| Typography | [typography.md](references/components/general/typography.md) | Titles, paragraphs, descriptions, readable text blocks |
| Link | [link.md](references/components/general/link.md) | Inline links, external links, lightweight actions |
| Divider | [divider.md](references/components/general/divider.md) | Section separators and inline visual breaks |

### Layout

| Component | File | Use for |
|-----------|------|---------|
| Grid | [grid.md](references/components/layout/grid.md) | Responsive row and column layout |
| Layout | [layout.md](references/components/layout/layout.md) | Header, sider, content, and footer page shells |
| Space | [space.md](references/components/layout/space.md) | Consistent spacing between controls and sections |

### Navigation

| Component | File | Use for |
|-----------|------|---------|
| Menu | [menu.md](references/components/navigation/menu.md) | Sidebar navigation, nested menus, route-driven menus |
| Tabs | [tabs.md](references/components/navigation/tabs.md) | Switchable content panels and segmented sections |
| Dropdown | [dropdown.md](references/components/navigation/dropdown.md) | Overflow actions and contextual menus |
| Breadcrumb | [breadcrumb.md](references/components/navigation/breadcrumb.md) | Navigation hierarchy and page context |
| Pagination | [pagination.md](references/components/navigation/pagination.md) | Table and list paging controls |
| Steps | [steps.md](references/components/navigation/steps.md) | Multi-step workflows |
| Affix | [affix.md](references/components/navigation/affix.md) | Sticky actions or sticky summaries |
| Anchor | [anchor.md](references/components/navigation/anchor.md) | In-page section navigation |
| PageHeader | [page-header.md](references/components/navigation/page-header.md) | Page titles, subtitles, back actions, and header extras |

### Data Entry

| Component | File | Use for |
|-----------|------|---------|
| Form | [form.md](references/components/data-entry/form.md) | Form layout, validation, and field orchestration |
| Input | [input.md](references/components/data-entry/input.md) | Text input, password input, textarea, search |
| Select | [select.md](references/components/data-entry/select.md) | Single and multiple selection, option lists, search |
| DatePicker | [date-picker.md](references/components/data-entry/date-picker.md) | Date and date-range picking |
| TimePicker | [time-picker.md](references/components/data-entry/time-picker.md) | Time and time-range picking |
| InputNumber | [input-number.md](references/components/data-entry/input-number.md) | Numeric values and bounded counters |
| Checkbox | [checkbox.md](references/components/data-entry/checkbox.md) | Multiple choices and grouped selections |
| Radio | [radio.md](references/components/data-entry/radio.md) | Single-choice groups |
| Switch | [switch.md](references/components/data-entry/switch.md) | Boolean toggles and feature flags |
| Slider | [slider.md](references/components/data-entry/slider.md) | Continuous value selection |
| Rate | [rate.md](references/components/data-entry/rate.md) | Scores and ratings |
| Cascader | [cascader.md](references/components/data-entry/cascader.md) | Hierarchical selection |
| TreeSelect | [tree-select.md](references/components/data-entry/tree-select.md) | Tree-based selection |
| Transfer | [transfer.md](references/components/data-entry/transfer.md) | Moving items between two lists |
| AutoComplete | [auto-complete.md](references/components/data-entry/auto-complete.md) | Input suggestions and type-ahead results |
| Mentions | [mentions.md](references/components/data-entry/mentions.md) | Mention insertion and suggestion lists |
| InputTag | [input-tag.md](references/components/data-entry/input-tag.md) | Tag entry and tokenized text input |
| Upload | [upload.md](references/components/data-entry/upload.md) | File and image uploads |
| ColorPicker | [color-picker.md](references/components/data-entry/color-picker.md) | Color selection |
| VerificationCode | [verification-code.md](references/components/data-entry/verification-code.md) | OTP and verification code entry |

### Data Display

| Component | File | Use for |
|-----------|------|---------|
| Table | [table.md](references/components/data-display/table.md) | Data tables, slot-based cells, operations, pagination |
| List | [list.md](references/components/data-display/list.md) | Simple record lists and feeds |
| Card | [card.md](references/components/data-display/card.md) | Content containers and dashboard sections |
| Tree | [tree.md](references/components/data-display/tree.md) | Hierarchical display and nested browsing |
| Tooltip | [tooltip.md](references/components/data-display/tooltip.md) | Small hover or focus hints |
| Popover | [popover.md](references/components/data-display/popover.md) | Rich floating detail panels |
| Avatar | [avatar.md](references/components/data-display/avatar.md) | User identity and avatar groups |
| Badge | [badge.md](references/components/data-display/badge.md) | Counts and status indicators |
| Tag | [tag.md](references/components/data-display/tag.md) | Status chips and category labels |
| Carousel | [carousel.md](references/components/data-display/carousel.md) | Banners and rotating content |
| Collapse | [collapse.md](references/components/data-display/collapse.md) | Expandable detail sections |
| Descriptions | [descriptions.md](references/components/data-display/descriptions.md) | Key-value detail layouts |
| Calendar | [calendar.md](references/components/data-display/calendar.md) | Calendar views |
| Comment | [comment.md](references/components/data-display/comment.md) | Comment-like records |
| Empty | [empty.md](references/components/data-display/empty.md) | Empty states |
| Image | [image.md](references/components/data-display/image.md) | Image display and preview |
| Statistic | [statistic.md](references/components/data-display/statistic.md) | KPI counters and metrics |
| Timeline | [timeline.md](references/components/data-display/timeline.md) | Chronological events and history |

### Feedback

| Component | File | Use for |
|-----------|------|---------|
| Modal | [modal.md](references/components/feedback/modal.md) | Blocking dialogs and confirmation flows |
| Message | [message.md](references/components/feedback/message.md) | Short global feedback toasts |
| Notification | [notification.md](references/components/feedback/notification.md) | Rich global notifications |
| Drawer | [drawer.md](references/components/feedback/drawer.md) | Side-panel editing and inspection flows |
| Alert | [alert.md](references/components/feedback/alert.md) | Inline warnings and notices |
| Progress | [progress.md](references/components/feedback/progress.md) | Progress indicators and completion bars |
| Popconfirm | [popconfirm.md](references/components/feedback/popconfirm.md) | Lightweight destructive-action confirmation |
| Result | [result.md](references/components/feedback/result.md) | Success, failure, or exception result pages |
| Skeleton | [skeleton.md](references/components/feedback/skeleton.md) | Loading placeholders |
| Spin | [spin.md](references/components/feedback/spin.md) | Loading wrappers around content |

### Other

| Component | File | Use for |
|-----------|------|---------|
| BackTop | [back-top.md](references/components/other/back-top.md) | Scroll-to-top controls |
| Portal | [portal.md](references/components/other/portal.md) | Rendering into alternate DOM containers |
| ResizeBox | [resize-box.md](references/components/other/resize-box.md) | Resizable panels |
| Trigger | [trigger.md](references/components/other/trigger.md) | Controlled popup positioning |
| Watermark | [watermark.md](references/components/other/watermark.md) | Text or image watermarks |

### Patterns and Best Practices

| Topic | File | When to use |
|-------|------|-------------|
| Form Patterns | [form-patterns.md](references/patterns/form-patterns.md) | Search forms, edit forms, async submit, form sections, and validation patterns |
| Table Patterns | [table-patterns.md](references/patterns/table-patterns.md) | Search tables, remote data, column slots, operations, and pagination wiring |
| Modal Patterns | [modal-patterns.md](references/patterns/modal-patterns.md) | Confirmation flows, edit dialogs, drawer vs modal choices, and close-after-success patterns |
| Controlled vs Uncontrolled | [controlled-uncontrolled.md](references/patterns/controlled-uncontrolled.md) | Choosing `v-model` vs default props and understanding controlled state in Vue pages |
| Responsive Design | [responsive-design.md](references/patterns/responsive-design.md) | Desktop/mobile layout adjustments, grid breakpoints, menu behavior, and responsive cards |

### Hooks and Composables

| Hook | File | Use for |
|------|------|---------|
| useLoading | [use-loading.md](references/hooks/use-loading.md) | Small page-level loading state handling |
| useLocale | [use-locale.md](references/hooks/use-locale.md) | Reading and switching app locale |
| usePermission | [use-permission.md](references/hooks/use-permission.md) | Route and action permission checks |
| useResponsive | [use-responsive.md](references/hooks/use-responsive.md) | Adapting layout behavior to device size |

