---
name: arco-vue-empty
description: "Refers to a state in which the current scene has no corresponding data content. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Empty

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

Basic usage of empty component.

```vue
<template>
  <a-empty />
</template>
```

## Custom Image & Description

Customize icons and pictures through the `image` slot, or modify the text through the content.

```vue
<template>
  <a-empty>
    <template #image>
      <icon-exclamation-circle-fill />
    </template>
    No data, please reload!
  </a-empty>
</template>

<script>
import { IconExclamationCircleFill } from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconExclamationCircleFill
  },
}
</script>
```

## API

### `<empty>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|description|Description|`string`|`-`||
|img-src|The src of the Custom Image|`string`|`-`||
|in-config-provider|Whether to use in ConfigProvider|`boolean`|`false`|2.47.0|
### `<empty>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|image|Image/Icon|-|
