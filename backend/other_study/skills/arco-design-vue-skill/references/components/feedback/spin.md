---
name: arco-vue-spin
description: "Used for the loading state of pages and blocks-when a part of the page is waiting for asynchronous data or is in the rendering process, appropriate loading dynamics will effectively alleviate user anxiety. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Spin

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Used to show the status of loading.

```vue
<template>
  <a-spin />
</template>
```

## Custom Size

$END$

```vue
<template>
  <a-space size="large">
    <a-spin />
    <a-spin :size="28"/>
    <a-spin :size="32"/>
  </a-space>
</template>
```

## Dot Loading

The dot type indicator can be displayed through the `dot` attribute.

```vue

<template>
  <a-spin dot />
</template>
```

## Container

You can add a loading indicator to any content.

```vue
<template>
  <a-spin :loading="loading" tip="This may take a while...">
    <a-card title="Arco Card">
      ByteDance's core product, Toutiao ('Headlines'), is a content platform in China and around
      the world. Toutiao started out as a news recommendation engine and gradually evolved into
      a platform delivering content in various formats.
    </a-card>
  </a-spin>
</template>

<script>
export default {
  data() {
    return {
      loading: true
    }
  }
}
</script>
```

## Add tip

$END$

```vue
<template>
  <a-spin tip="This may take a while..."/>
</template>
```

## Custom Icon

$END$

```vue
<template>
  <a-spin>
    <template #icon>
      <icon-sync />
    </template>
  </a-spin>
</template>

<script>
import { IconSync } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconSync }
};
</script>
```

## API

### `<spin>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|size|Size|`number`|`-`|
|loading|Whether it is loading state (Only effective in container mode)|`boolean`|`false`|
|dot|Whether to use dot type animation|`boolean`|`false`|
|tip|Prompt content|`string`|`-`|
|hide-icon|Whether to hide the icon|`boolean`|`false`|
### `<spin>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|tip|Custom tip|-|
|element|Custom element|-|
|icon|Custom icon (auto-rotation)|-|
