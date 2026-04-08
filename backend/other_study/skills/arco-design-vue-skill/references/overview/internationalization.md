---
name: arco-vue-internationalization
description: "Arco Design Pro Vue internationalization guide. Use for vue-i18n wiring, locale files, menu text localization, and multi-language project structure."
user-invocable: false
---

# Internationalization

## Globalization

Internationalization is achieved through the [ConfigProvider](config-provider.md) component.

## Basic usage

```vue
<template>
  <a-config-provider :locale="enUS">
    <a-pagination :total="50" show-total show-jumper show-page-size />
  </a-config-provider>
</template>

<script>
import enUS from '@arco-design/web-vue/es/locale/lang/en-us';

export default {
  data() {
    return {
      enUS,
    };
  },
};
</script>
```

## Supported regional languages

| Language            | Area code |
| ------------------- | --------- |
| Simple Chinese      | zh-CN     |
| English (US)        | en-US     |
| Japanese            | ja-JP     |
| Traditional Chinese | zh-TW     |
| Portuguese          | pt-PT     |
| Spanish             | es-ES     |
| Indonesian          | id-ID     |
| French, France      | fr-FR     |
| German, Germany     | de-DE     |
| Korean              | ko-KR     |
| Italian, Italy      | it-IT     |
| Thai                | th-TH     |
| Melayu (Malaysia)   | ms-MY     |
| Vietnamese          | vi-VN     |
| Khmer (Cambodia)    | km-KH     |
| Arabic (Egypt)      | ar-EG     |
| Russian (Russia)    | ru-RU     |
| Dutch (Netherlands) | nl-NL     |

## Language Pack

Internationalization is firstly the provision of language packs. In Pro, the language packs are defined in `src/locale`, and then imported into `main` to take effect.

```
locale/
  en-US.ts
  zh-CN.ts
hooks/
  locale.ts
main.ts
```

At the same time, hooks for obtaining the current language and switching the current language are provided in the hooks directory.

 ```ts
import {computed} from 'vue';
import {useI18n} from 'vue-i18n';

export default function useLocale() {
     const i18 = useI18n();
     const currentLocale = computed(() => {
         return i18.locale.value;
     });
     const changeLocale = (value: string) => {
         i18.locale.value = value;
         localStorage.setItem('arco-locale', value);
     };
     return {
         currentLocale,
         changeLocale,
     };
}
```
