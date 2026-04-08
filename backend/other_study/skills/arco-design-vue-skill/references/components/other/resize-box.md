---
name: arco-vue-resize-box
description: "Telescopic frame components. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# ResizeBox

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

Basic usage of `ResizeBox`. By setting `directions`, you can specify which of the four sides can be stretched.

```vue
<template>
  <div>
    <a-resize-box
      :directions="['right', 'bottom']"
      :style="{ width: '500px', minWidth: '100px', maxWidth: '100%', height: '200px', textAlign: 'center' }"
    >
      <a-typography-paragraph>We are building the future of content discovery and creation.</a-typography-paragraph>
      <a-divider />
      <a-typography-paragraph>
        ByteDance's content platforms enable people to enjoy content powered by AI technology. We
        inform, entertain, and inspire people across language, culture and geography.
      </a-typography-paragraph>
      <a-divider>ByteDance</a-divider>
      <a-typography-paragraph>Yiming Zhang is the founder and CEO of ByteDance.</a-typography-paragraph>
    </a-resize-box>
  </div>
</template>
```

## two-way binding

Both `width` and `height` of `ResizeBox` support `v-model`..

```vue
<template>
<div>
  <a-resize-box
    :directions="['right', 'bottom']"
    :style="{ minWidth: '100px', maxWidth: '100%', textAlign: 'center' }"
    v-model:width="width"
    v-model:height="height"
  >
    <a-typography-paragraph>We are building the future of content discovery and creation.</a-typography-paragraph>
    <a-divider />
    <a-typography-paragraph>
      ByteDance's content platforms enable people to enjoy content powered by AI technology. We
      inform, entertain, and inspire people across language, culture and geography.
    </a-typography-paragraph>
    <a-divider>ByteDance</a-divider>
    <a-typography-paragraph>Yiming Zhang is the founder and CEO of ByteDance.</a-typography-paragraph>
  </a-resize-box>
</div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const width = ref(500);
    const height = ref(200);
    return {
      width,
      height,
    };
  }
};
</script>
```

## Use in Layout

The `ResizeBox` component is integrated in the [Layout](../layout/layout.md) component, so a scalable sidebar can be used in the layout.

```vue
<template>
<div class="layout-demo">
  <a-layout>
    <a-layout-header>Header</a-layout-header>
    <a-layout>
      <a-layout-sider :resize-directions="['right']">
        Sider
      </a-layout-sider>
      <a-layout-content>Content</a-layout-content>
    </a-layout>
    <a-layout-footer>Footer</a-layout-footer>
  </a-layout>
</div>
</template>

<style scoped>
.layout-demo :deep(.arco-layout-header),
.layout-demo :deep(.arco-layout-footer),
.layout-demo :deep(.arco-layout-sider-children),
.layout-demo :deep(.arco-layout-content) {
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: var(--color-white);
  font-size: 16px;
  font-stretch: condensed;
  text-align: center;
}

.layout-demo :deep(.arco-layout-header),
.layout-demo :deep(.arco-layout-footer) {
  height: 64px;
  background-color: var(--color-primary-light-4);
}

.layout-demo :deep(.arco-layout-sider) {
  width: 206px;
  background-color: var(--color-primary-light-3);
  min-width: 150px;
  max-width: 500px;
  height: 200px;
}

.layout-demo :deep(.arco-layout-content) {
  background-color: rgb(var(--arcoblue-6));
}
</style>
```

## Customize Trigger

The content of trigger in all directions can be customized through the slot `resize-trigger`.

```vue
<template>
  <a-resize-box
    :directions="['right', 'bottom']"
    style="width: 500px; min-width: 100px; max-width: 100%; height: 200px; text-align: center;"
  >
    <template #resize-trigger="{ direction }">
      <div
        :class="[
          `resizebox-demo`,
          `resizebox-demo-${direction === 'right' ? 'vertical' : 'horizontal'}`
        ]"
      >
        <div class="resizebox-demo-line"/>
      </div>
    </template>
    <a-typography-paragraph>We are building the future of content discovery and creation.</a-typography-paragraph>
    <a-divider />
    <a-typography-paragraph>
      ByteDance's content platforms enable people to enjoy content powered by AI technology. We
      inform, entertain, and inspire people across language, culture and geography.
    </a-typography-paragraph>
    <a-divider>ByteDance</a-divider>
    <a-typography-paragraph>Yiming Zhang is the founder and CEO of ByteDance.</a-typography-paragraph>
  </a-resize-box>
</template>

<style scoped>
  .resizebox-demo {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    background-color: var(--color-bg-2);
  }
  .resizebox-demo::before,
  .resizebox-demo::after {
    width: 6px;
    height: 6px;
    border: 1px solid rgb(var(--arcoblue-6));
    content: '';
}
  .resizebox-demo-line {
    flex: 1;
    background-color: rgb(var(--arcoblue-6));
  }
  .resizebox-demo-vertical {
    flex-direction: column;
  }
  .resizebox-demo-vertical .resizebox-demo-line {
    width: 1px;
    height: 100%;
  }
  .resizebox-demo-horizontal .resizebox-demo-line {
    height: 1px;
  }
</style>
```

## API

### `<resize-box>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|width **(v-model)**|Width|`number`|`-`|
|height **(v-model)**|Height|`number`|`-`|
|component|The html tag of the telescopic box|`string`|`'div'`|
|directions|Can be stretched side, there are up, down, left and right can be used|`('left' \| 'right' \| 'top' \| 'bottom')[]`|`['right']`|
### `<resize-box>` Events

|Event Name|Description|Parameters|
|---|---|---|
|moving-start|Triggered when dragging starts|ev: `MouseEvent`|
|moving|Triggered when dragging|size: `{ width: number; height: number; }`<br>ev: `MouseEvent`|
|moving-end|Triggered when the drag ends|ev: `MouseEvent`|
### `<resize-box>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|resize-trigger|The contents of the resize pole|direction: `'left' \| 'right' \| 'top' \| 'bottom'`|
|resize-trigger-icon|Resize pole icon|direction: `'left' \| 'right' \| 'top' \| 'bottom'`|
