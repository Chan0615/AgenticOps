---
name: arco-vue-use-responsive
description: "Arco Pro Vue useResponsive composable reference. Use for device-aware layout behavior and menu adaptation."
user-invocable: false
---

# useResponsive

Use `useResponsive()` when a feature needs to react to desktop vs mobile layout behavior.

Upstream shape:

```ts
import { onMounted, onBeforeMount, onBeforeUnmount } from 'vue';
import { useDebounceFn } from '@vueuse/core';
import { useAppStore } from '@/store';

const WIDTH = 992;

export default function useResponsive(immediate?: boolean) {
  const appStore = useAppStore();
  function resizeHandler() {
    const isMobile = document.body.getBoundingClientRect().width - 1 < WIDTH;
    appStore.toggleDevice(isMobile ? 'mobile' : 'desktop');
    appStore.toggleMenu(isMobile);
  }
  const debounceFn = useDebounceFn(resizeHandler, 100);
  onMounted(() => {
    if (immediate) debounceFn();
  });
}
```

## Common responsibilities

- detect current device mode
- coordinate app-store layout state
- support menu collapse or drawer transitions

## Practical usage

Call `useResponsive(true)` near the top of layout components or pages that depend on current device mode.

## Practical rule

Reuse the existing responsive hook first. Only add new viewport logic if the current hook cannot express the needed behavior.
