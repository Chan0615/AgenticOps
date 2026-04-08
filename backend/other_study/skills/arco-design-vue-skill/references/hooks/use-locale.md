---
name: arco-vue-use-locale
description: "Arco Pro Vue useLocale composable reference. Use for reading and switching the current application locale."
user-invocable: false
---

# useLocale

`useLocale()` is a small wrapper around `vue-i18n` and local storage.

Upstream shape:

```ts
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { Message } from '@arco-design/web-vue';

export default function useLocale() {
  const i18 = useI18n();
  const currentLocale = computed(() => i18.locale.value);
  const changeLocale = (value: string) => {
    if (i18.locale.value === value) return;
    i18.locale.value = value;
    localStorage.setItem('arco-locale', value);
    Message.success(i18.t('navbar.action.locale'));
  };
  return { currentLocale, changeLocale };
}
```

## Typical responsibilities

- read the current locale
- switch locale
- persist locale to local storage
- show a success message after change

## Practical rule

Reuse the existing composable rather than writing locale-switch logic directly in each page or navbar component.
