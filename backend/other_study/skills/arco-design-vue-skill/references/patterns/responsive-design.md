---
name: arco-vue-responsive-design
description: "Arco Design Pro Vue responsive design guide. Use for responsive grids, menu collapse behavior, card layout adaptation, and mobile-friendly admin pages."
user-invocable: false
---

# Responsive Design

## Common responsive tools in Arco Pro Vue

- `a-row` and `a-col`
- app-store menu collapse state
- responsive hooks
- mobile drawer menu behavior in the default layout

## Practical grid example

```vue
<a-row :gutter="16">
  <a-col :xs="24" :sm="24" :md="12" :lg="8">
    <a-card>Card A</a-card>
  </a-col>
  <a-col :xs="24" :sm="24" :md="12" :lg="8">
    <a-card>Card B</a-card>
  </a-col>
  <a-col :xs="24" :sm="24" :md="24" :lg="8">
    <a-card>Card C</a-card>
  </a-col>
</a-row>
```

## Good admin-page behavior

- collapse dense filter rows instead of forcing one extremely wide row
- stack cards vertically on smaller screens
- keep primary actions visible and reachable
- avoid wide fixed tables without a clear scroll strategy

## Menu and layout notes

The default Arco Pro Vue layout already contains mobile menu behavior. Extend it carefully instead of replacing it with a second menu system.

## useResponsive hook pattern

In upstream Arco Pro Vue, `useResponsive(true)` updates app-store device state and hides the menu when the viewport is narrow. Use that hook before inventing local `window.resize` logic.

## Practical rule

A responsive admin page is still primarily an information architecture problem. Reduce clutter before adding more CSS.
