---
name: arco-vue-controlled-uncontrolled
description: "Arco Design Vue controlled vs uncontrolled guidance. Use for choosing v-model, explicit state ownership, and default-value behavior."
user-invocable: false
---

# Controlled vs Uncontrolled

In Vue admin pages, prefer controlled state when the page needs to react to changes, validate data, or synchronize filters with requests.

## Controlled pattern

Use `v-model` or `v-model:<prop>` when:

- page logic depends on the value immediately
- you need reset behavior
- value changes affect requests, charts, or other components
- the value must be stored in Pinia or route state

Common controlled examples in Arco Pro Vue:

- `v-model="formModel.status"` on `a-select`
- `v-model:visible="visible"` on `a-modal` or `a-drawer`
- `v-model:active-key="activeKey"` on `a-tabs`
- `v-model:selectedKeys="selectedKeys"` on `a-table`

## Uncontrolled or default prop pattern

Use default props only when:

- the component is locally self-contained
- page logic does not need every intermediate change
- the existing codebase already uses that style in the same feature

Common uncontrolled examples:

- `default-value` on a standalone demo or local-only component
- `default-selected-keys` on a component whose selection never needs page-level reset or synchronization
- `default-expanded-keys` when tree expansion does not affect any other page behavior

## Practical rule

For Arco Pro Vue pages, filters, forms, dialogs, and tabs are usually easier to maintain as controlled state.

If the user asks to "reset filters", "sync tab state", "persist selection", or "react immediately", controlled state is the correct default.
