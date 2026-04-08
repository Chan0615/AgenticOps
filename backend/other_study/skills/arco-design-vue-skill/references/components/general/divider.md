---
name: arco-vue-divider
description: "Divide the content area and separate the modules. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Divider

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

It divides the text paragraphs of different chapters, the default is a horizontal dividing line, you can add text in the middle.

```vue
<template>
  <div class="divider-demo">
    <p>A design is a plan or specification for the construction of an object.</p>
    <a-divider />
    <p>A design is a plan or specification for the construction of an object.</p>
    <a-divider dashed />
    <p>A design is a plan or specification for the construction of an object.</p>
    <a-divider :size="2" style="border-bottom-style: dotted" />
    <p>A design is a plan or specification for the construction of an object.</p>
  </div>
  <div class="divider-demo" style="marginTop: 48px">
    <div class="flex-box">
      <span class="avatar"><IconImage /></span>
      <div class="content">
        <a-typography-title :heading="6">Image</a-typography-title>
        May 4, 2010
      </div>
    </div>
    <a-divider class="half-divider" />
    <div class="flex-box">
      <span class="avatar"><IconUser /></span>
      <div class="content">
        <a-typography-title :heading="6">Avatar</a-typography-title>
        May 4, 2010
      </div>
    </div>
    <a-divider class="half-divider" />
    <div class="flex-box">
      <span class="avatar"><IconPen /></span>
      <div class="content">
        <a-typography-title :heading="6">Icon</a-typography-title>
        May 4, 2010
      </div>
    </div>
  </div>
</template>

<script>
import {
  IconImage,
  IconUser,
  IconPen,
} from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconImage,
    IconUser,
    IconPen,
  },
};
</script>

<style scoped>
.divider-demo {
  box-sizing: border-box;
  width: 560px;
  padding: 24px;
  border: 30px solid rgb(var(--gray-2));
}
.half-divider {
  left: 55px;
  width: calc(100% - 55px);
  min-width: auto;
  margin: 16px 0;
}
.flex-box {
  display: flex;
  align-items: center;
  justify-content: center;
}
.flex-box .avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  margin-right: 16px;
  color: var(--color-text-2);
  font-size: 16px;
  background-color: var(--color-fill-3);
  border-radius: 50%;
}
.flex-box .content {
  flex: 1;
  color: var(--color-text-2);
  font-size: 12px;
  line-height: 20px;
}
</style>
```

## With Text

Use `orientation` to add descriptive text to Divider.

```vue
<template>
  <div class="divider-demo">
    <p>A design is a plan or specification for the construction of an object.</p>
    <a-divider orientation="left">Text</a-divider>
    <p>A design is a plan or specification for the construction of an object.</p>
    <a-divider orientation="center">Text</a-divider>
    <p>A design is a plan or specification for the construction of an object.</p>
    <a-divider orientation="right">Text</a-divider>
    <a-divider :margin="10"><icon-star /></a-divider>
  </div>
</template>

<style scoped>
.divider-demo {
  box-sizing: border-box;
  width: 560px;
  padding: 24px;
  border: 30px solid rgb(var(--gray-2));
}
</style>
```

## Vertical Divider

Specify the `direction` as `vertical` to use the vertical Divider which cannot contain text.

```vue
<template>
  <div class="divider-demo">
    <span>Item 1</span>
    <a-divider direction="vertical" />
    <span>Item 2</span>
    <a-divider direction="vertical" />
    <span>Item 3</span>
  </div>
</template>

<style scoped>
.divider-demo {
  box-sizing: border-box;
  width: 560px;
  padding: 24px;
  border: 30px solid rgb(var(--gray-2));
}
</style>
```

## API

### `<divider>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|direction|The direction of the dividing line. Can be horizontal or vertical|`'horizontal' \| 'vertical'`|`'horizontal'`||
|orientation|The position of the dividing line text|`'left' \| 'center' \| 'right'`|`'center'`||
|type|Dividing line style type|`'solid' \| 'dashed' \| 'dotted' \| 'double'`|`-`|2.35.0|
|size|The wide/height of the dividing line|`number`|`-`|2.35.0|
|margin|Margin up and down the split line (left and right margin in vertical direction)|`number \| string`|`-`|2.35.0|
