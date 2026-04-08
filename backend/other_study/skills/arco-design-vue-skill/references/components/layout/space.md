---
name: arco-vue-space
description: "Set the spacing between components. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Space

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

Basic usage of spacing components.

```vue
<template>
  <a-space>
    <a-typography-text>Space:</a-typography-text>
    <a-tag v-if="false" color='arcoblue'>Tag</a-tag>
    <a-button type="primary">Item1</a-button>
    <a-button type="primary">Item2</a-button>
    <a-switch defaultChecked />
  </a-space>
</template>
```

## Vertical

You can set the spacing in the vertical direction.

```vue
<template>
  <a-space direction="vertical" fill>
    <a-button type="primary" long>Item1</a-button>
    <a-button type="primary" long>Item2</a-button>
    <a-button type="primary" long>Item3</a-button>
  </a-space>
</template>
```

## Size

Built-in 4 sizes, `mini-4px` `small-8px (default)` `medium-16px` `large-24px`, and also support to pass numbers to customize the size.

```vue
<template>
  <div>
    <div style="marginBottom: 20px">
      <a-radio-group v-model="size" type='button'>
        <a-radio value="mini">mini</a-radio>
        <a-radio value="small">small</a-radio>
        <a-radio value="medium">medium</a-radio>
        <a-radio value="large">large</a-radio>
      </a-radio-group>
    </div>
    <a-space :size="size">
      <a-button type="primary">Item1</a-button>
      <a-button type="primary">Item2</a-button>
      <a-button type="primary">Item3</a-button>
    </a-space>
  </div>
</template>
<script>
export default {
  data() {
    return {
      size: 'medium',
    }
  }
};
</script>
```

## Align

There are 4 built-in alignment methods, namely `start` `center` `end` `baseline`, and the default is `center` in horizontal mode.

```vue
<template>
  <div>
    <div style="marginBottom: 20px">
      <a-radio-group v-model="align" type='button'>
        <a-radio value="start">start</a-radio>
        <a-radio value="center">center</a-radio>
        <a-radio value="end">end</a-radio>
        <a-radio value="baseline">baseline</a-radio>
      </a-radio-group>
    </div>
    <a-space :align="align" style="backgroundColor: var(--color-fill-2);padding: 10px;">
      <a-typography-text>Space:</a-typography-text>
      <a-button type="primary">Item2</a-button>
      <a-card title='Card'>
        Card content
      </a-card>
    </a-space>
  </div>
</template>
<script>
export default {
  data() {
    return {
      align: 'center',
    }
  }
};
</script>
```

## Wrap

Surround type spacing, there are spacing on all sides, generally used in the scene of line wrapping.

```vue
<template>
  <a-space wrap>
    <a-button type="primary">Item1</a-button>
    <a-button type="primary">Item2</a-button>
    <a-button type="primary">Item3</a-button>
    <a-button type="primary">Item4</a-button>
    <a-button type="primary">Item5</a-button>
    <a-button type="primary">Item6</a-button>
    <a-button type="primary">Item7</a-button>
    <a-button type="primary">Item8</a-button>
    <a-button type="primary">Item9</a-button>
    <a-button type="primary">Item10</a-button>
    <a-button type="primary">Item11</a-button>
    <a-button type="primary">Item12</a-button>
    <a-button type="primary">Item13</a-button>
    <a-button type="primary">Item14</a-button>
    <a-button type="primary">Item15</a-button>
    <a-button type="primary">Item16</a-button>
    <a-button type="primary">Item17</a-button>
    <a-button type="primary">Item18</a-button>
    <a-button type="primary">Item19</a-button>
    <a-button type="primary">Item20</a-button>
  </a-space>
</template>
```

## Split

Set separators for adjacent child elements.

```vue
<template>
  <a-space>
    <template #split>
      <a-divider direction="vertical" :margin="0" />
    </template>
    <a-button type="primary">Item1</a-button>
    <a-tag v-if="show" color='arcoblue'>Tag</a-tag>
    <a-button type="primary">Item2</a-button>
    <a-button type="primary">Item3</a-button>
    <a-switch v-model="show"/>
  </a-space>
  <a-divider />
  <a-space>
    <template #split>
      <a-divider direction="vertical" :margin="0" />
    </template>
    <a-link type="primary">Link1</a-link>
    <a-link type="primary">Link2</a-link>
    <a-link type="primary">Link3</a-link>
  </a-space>
</template>

<script setup>
import { ref } from 'vue'

const show = ref(false)
</script>
```

## API

### `<space>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|align|Alignment|`'start' \| 'end' \| 'center' \| 'baseline'`|`-`||
|direction|Spacing direction|`'vertical' \| 'horizontal'`|`'horizontal'`||
|size|Spacing size, support for setting horizontal and vertical spacing separately|`number \| 'mini' \| 'small' \| 'medium' \| 'large' \| [SpaceSize, SpaceSize]`|`'small'`||
|wrap|The spacing of the wrapping type, used in the scene of wrapping.|`boolean`|`false`||
|fill|fill the block|`boolean`|`false`|2.11.0|
### `<space>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|split|Set separator|-|

## Type
```ts
type SpaceSize = number | 'mini' | 'small' | 'medium' | 'large';
```
