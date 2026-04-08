---
name: arco-vue-use-loading
description: "Arco Pro Vue useLoading composable reference. Use for small page-level loading state and async request coordination."
user-invocable: false
---

# useLoading

Typical upstream pattern:

```ts
const { loading, setLoading, toggle } = useLoading(true);
```

Source shape:

```ts
import { ref } from 'vue';

export default function useLoading(initValue = false) {
  const loading = ref(initValue);
  const setLoading = (value: boolean) => {
    loading.value = value;
  };
  const toggle = () => {
    loading.value = !loading.value;
  };
  return { loading, setLoading, toggle };
}
```

## When to use

- table fetch state
- submit button state
- card-level loading wrappers

## Real page pattern

```ts
const { loading, setLoading } = useLoading(true);

const fetchData = async () => {
  setLoading(true);
  try {
    // request
  } finally {
    setLoading(false);
  }
};
```

## Rule

Use it for small local loading needs. If loading state becomes cross-page or cross-feature, move that concern to a store or dedicated feature module.
