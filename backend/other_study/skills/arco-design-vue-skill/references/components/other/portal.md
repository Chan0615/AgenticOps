---
name: arco-vue-portal
description: "Portal guidance for Vue 3 and Arco Design Pro Vue. Use for custom out-of-tree rendering with Teleport when a page needs portal-like behavior."
user-invocable: false
---

# Portal

Arco Design Vue does not ship a standalone `Portal` component like the React package. In Vue 3, use the built-in `Teleport` mechanism when you need portal-style rendering.

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

```vue
<template>
  <Teleport to="body">
    <div class="floating-panel">Portal content</div>
  </Teleport>
</template>

<style scoped>
.floating-panel {
  position: fixed;
  right: 24px;
  bottom: 24px;
}
</style>
```

## Practical Notes

- Prefer Arco components such as `Modal`, `Drawer`, `Notification`, `Trigger`, and `Popover` before reaching for raw `Teleport`.

- Use `Teleport` when a custom floating layer must escape the current DOM stacking context.

- Keep focus management and keyboard accessibility in mind when rendering custom overlays.
