---
name: arco-vue-skeleton
description: "Use gray to place the data being loaded. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Skeleton

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

The skeleton screen component provides two components: `<a-skeleton-line>` and `<a-skeleton-shape>`, users can combine them according to their needs.

```vue
<template>
  <a-skeleton>
    <a-space direction="vertical" :style="{width:'100%'}" size="large">
      <a-skeleton-line :rows="3" />
      <a-skeleton-shape />
    </a-space>
  </a-skeleton>
</template>
```

## Shape Skeleton

The graphic skeleton screen is divided into two shapes: `square`, `circle`, and provides three sizes of `small`, `medium`, and `large`.

```vue
<template>
  <a-skeleton>
    <a-space size="large">
      <a-skeleton-shape size="small" />
      <a-skeleton-shape />
      <a-skeleton-shape size="large" />
      <a-skeleton-shape shape="circle" size="small" />
      <a-skeleton-shape shape="circle" />
      <a-skeleton-shape shape="circle" size="large" />
    </a-space>
  </a-skeleton>
</template>
```

## Animation

By setting the `animation` property, the skeleton screen can display the animation effect.

```vue
<template>
  <a-space direction="vertical" size="large" :style="{width:'100%'}">
    <a-space>
      <span>Animation</span>
      <a-switch v-model="animation" />
    </a-space>
    <a-skeleton :animation="animation">
      <a-space direction="vertical" :style="{width:'100%'}" size="large">
        <a-skeleton-line :rows="3" />
        <a-skeleton-shape />
      </a-space>
    </a-skeleton>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const animation = ref(true);

    return {
      animation
    }
  },
}
</script>
```

## API

### `<skeleton>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|loading|Whether to display the skeleton screen (loading state)|`boolean`|`true`|
|animation|Whether to enable skeleton screen animation|`boolean`|`false`|

### `<skeleton-line>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|rows|Number of rows displayed|`number`|`1`|
|widths|The width of the line skeleton|`Array<number \| string>`|`[]`|
|line-height|Line height of the line skeleton|`number`|`20`|
|line-spacing|Line spacing of line skeleton|`number`|`15`|

### `<skeleton-shape>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|shape|The shape of the shape skeleton|`'square' \| 'circle'`|`'square'`|
|size|The size of the shape skeleton|`'small' \| 'medium' \| 'large'`|`'medium'`|
