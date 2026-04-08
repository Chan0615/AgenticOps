---
name: arco-vue-use-permission
description: "Arco Pro Vue usePermission composable reference. Use for route access, action visibility, and permission-aware page logic."
user-invocable: false
---

# usePermission

Use `usePermission()` when the page or route behavior depends on roles.

Upstream shape:

```ts
import { RouteLocationNormalized, RouteRecordRaw } from 'vue-router';
import { useUserStore } from '@/store';

export default function usePermission() {
  const userStore = useUserStore();
  return {
    accessRouter(route: RouteLocationNormalized | RouteRecordRaw) {
      return (
        !route.meta?.requiresAuth ||
        !route.meta?.roles ||
        route.meta?.roles?.includes('*') ||
        route.meta?.roles?.includes(userStore.role)
      );
    },
  };
}
```

## Common responsibilities

- check whether a route is accessible
- find the first permitted route
- support route guards and menu filtering

## Template-level usage

```vue
<a-button v-permission="['admin']" status="danger">Delete</a-button>
```

## Practical rule

Prefer the existing permission system built around route meta and `v-permission` over ad hoc role checks scattered through templates.
