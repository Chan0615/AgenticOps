---
name: arco-vue-pagination
description: "Use paging to control the amount of information in a single page, and page jumps can also be performed. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Pagination

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of pagination, `total` attribute is required.

```vue
<template>
  <a-pagination :total="50"/>
</template>
```

## Ellipsis Pager

When the page number is larger, the pagination style with more page numbers will be used.

```vue
<template>
  <a-pagination :total="200"/>
</template>
```

## PageSize Options

By setting `show-page-size`, the number of items per page selector is displayed.

```vue
<template>
  <a-pagination :total="200" show-page-size/>
</template>
```

## Page Jumper

By setting `show-jumper`, the page number jump input box is displayed.

```vue
<template>
  <a-pagination :total="50" show-jumper/>
</template>
```

## Pagination Size

The pagination is divided into four sizes: `mini`, `small`, `medium`, and `large`.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-radio-group type="button" v-model="size">
      <a-radio value="mini">Mini</a-radio>
      <a-radio value="small">Small</a-radio>
      <a-radio value="medium">Medium</a-radio>
      <a-radio value="large">Large</a-radio>
    </a-radio-group>
    <a-pagination :total="50" :size="size" show-total show-jumper show-page-size />
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const size = ref('medium');

    return {
      size
    }
  },
}
</script>
```

## Simple

Open the simple mode by setting the `simple` property.

```vue
<template>
  <a-pagination :total="200" simple/>
</template>
```

## Total

Display the total number of data by setting the `show-total` property.

```vue
<template>
  <a-pagination :total="200" show-total/>
</template>
```

## Show All

Show all configuration.

```vue
<template>
  <a-pagination :total="50" show-total show-jumper show-page-size/>
</template>
```

## Custom Page Item

The content of the paging button can be customized through the slot

```vue
<template>
  <a-pagination :total="200">
    <template #page-item="{ page }">
      - {{page}} -
    </template>
    <template #page-item-step="{ type }">
      <icon-send :style="type==='previous' ? {transform:`rotate(180deg)`} : undefined" />
    </template>
    <template #page-item-ellipsis>
      <icon-sun-fill />
    </template>
  </a-pagination>
</template>
```

## API

### `<pagination>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|total **(required)**|Total number of data|`number`|`-`||
|current **(v-model)**|Current page number|`number`|`-`||
|default-current|The default number of pages (uncontrolled state)|`number`|`1`||
|page-size **(v-model)**|Number of data items displayed per page|`number`|`-`||
|default-page-size|The number of data items displayed per page by default (uncontrolled state)|`number`|`10`||
|disabled|Whether to disable|`boolean`|`false`||
|hide-on-single-page|Whether to hide pagination when single page|`boolean`|`false`||
|simple|Whether it is simple mode|`boolean`|`false`||
|show-total|Whether to display the total number of data|`boolean`|`false`||
|show-more|Whether to show more buttons|`boolean`|`false`||
|show-jumper|Whether to show jump|`boolean`|`false`||
|show-page-size|Whether to display the data number selector|`boolean`|`false`||
|page-size-options|Selection list of data number selector|`number[]`|`[10, 20, 30, 40, 50]`||
|page-size-props|Props of data number selector|`SelectProps`|`-`||
|size|The size of the page selector|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|page-item-style|The style of the paging button|`CSSProperties`|`-`||
|active-page-item-style|The style of the current paging button|`CSSProperties`|`-`||
|base-size|Calculate and display the number of omitted bases. Display the omitted number as `baseSize + 2 * bufferSize`|`number`|`6`||
|buffer-size|When the ellipsis is displayed, the number of page numbers displayed on the left and right of the current page number|`number`|`2`||
|auto-adjust|Whether to adjust the page number when changing the number of data|`boolean`|`true`|2.34.0|
### `<pagination>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when page number changes|current: `number`|
|page-size-change|Triggered when the number of data items changes|pageSize: `number`|
### `<pagination>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|total|Total|total: `number`|2.9.0|
|page-item-ellipsis|Page item (ellipsis)|-|2.9.0|
|page-item-step|Page item (step)|type: `'previous'\|'next'`The type of page item step|2.9.0|
|page-item|Page item|page: `number`The page number of the paging button|2.9.0|
