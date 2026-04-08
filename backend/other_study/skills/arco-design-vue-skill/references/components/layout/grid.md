---
name: arco-vue-grid
description: "Grid can effectively ensure the consistency and logic of the page, strengthen teamwork and unity. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Grid

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

Demonstrated the most basic 24 equal division applications

```vue
<template>
  <div class="grid-demo-background">
    <a-space direction="vertical" :size="16" style="display: block;">
      <a-row class="grid-demo">
        <a-col :span="24">
          <div>24 - 100%</div>
        </a-col>
      </a-row>
      <a-row class="grid-demo">
        <a-col :span="12">
          <div>12 - 50%</div>
        </a-col>
        <a-col :span="12">
          <div>12 - 50%</div>
        </a-col>
      </a-row>
      <a-row class="grid-demo">
        <a-col :span="8">
          <div>8 - 33.33%</div>
        </a-col>
        <a-col :span="8">
          <div>8 - 33.33%</div>
        </a-col>
        <a-col :span="8">
          <div>8 - 33.33%</div>
        </a-col>
      </a-row>
      <a-row class="grid-demo">
        <a-col :span="6">
          <div>6 - 25%</div>
        </a-col>
        <a-col :span="6">
          <div>6 - 25%</div>
        </a-col>
        <a-col :span="6">
          <div>6 - 25%</div>
        </a-col>
        <a-col :span="6">
          <div>6 - 25%</div>
        </a-col>
      </a-row>
      <a-row class="grid-demo">
        <a-col :span="4">
          <div>4 - 16.66%</div>
        </a-col>
        <a-col :span="4">
          <div>4 - 16.66%</div>
        </a-col>
        <a-col :span="4">
          <div>4 - 16.66%</div>
        </a-col>
        <a-col :span="4">
          <div>4 - 16.66%</div>
        </a-col>
        <a-col :span="4">
          <div>4 - 16.66%</div>
        </a-col>
        <a-col :span="4">
          <div>4 - 16.66%</div>
        </a-col>
      </a-row>
    </a-space>
  </div>
</template>

<style scoped>
.grid-demo-background {
  background-image: linear-gradient(
    90deg,
    var(--color-fill-2) 4.16666667%,
    transparent 4.16666667%,
    transparent 8.33333333%,
    var(--color-fill-2) 8.33333333%,
    var(--color-fill-2) 12.5%,
    transparent 12.5%,
    transparent 16.66666667%,
    var(--color-fill-2) 16.66666667%,
    var(--color-fill-2) 20.83333333%,
    transparent 20.83333333%,
    transparent 25%,
    var(--color-fill-2) 25%,
    var(--color-fill-2) 29.16666667%,
    transparent 29.16666667%,
    transparent 33.33333333%,
    var(--color-fill-2) 33.33333333%,
    var(--color-fill-2) 37.5%,
    transparent 37.5%,
    transparent 41.66666667%,
    var(--color-fill-2) 41.66666667%,
    var(--color-fill-2) 45.83333333%,
    transparent 45.83333333%,
    transparent 50%,
    var(--color-fill-2) 50%,
    var(--color-fill-2) 54.16666667%,
    transparent 54.16666667%,
    transparent 58.33333333%,
    var(--color-fill-2) 58.33333333%,
    var(--color-fill-2) 62.5%,
    transparent 62.5%,
    transparent 66.66666667%,
    var(--color-fill-2) 66.66666667%,
    var(--color-fill-2) 70.83333333%,
    transparent 70.83333333%,
    transparent 75%,
    var(--color-fill-2) 75%,
    var(--color-fill-2) 79.16666667%,
    transparent 79.16666667%,
    transparent 83.33333333%,
    var(--color-fill-2) 83.33333333%,
    var(--color-fill-2) 87.5%,
    transparent 87.5%,
    transparent 91.66666667%,
    var(--color-fill-2) 91.66666667%,
    var(--color-fill-2) 95.83333333%,
    transparent 95.83333333%
  );
}
.grid-demo .arco-col {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}
.grid-demo .arco-col:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
.grid-demo .arco-col:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}
</style>
```

## Offset of Col

Specify `offset` to translate the grid.

```vue
<template>
  <div>
    <a-row class="grid-demo" style="marginBottom: 16px; backgroundColor: var(--color-fill-2);">
      <a-col :span="8">col - 8</a-col>
      <a-col :span="8" :offset="8">
        col - 8 | offset - 8
      </a-col>
    </a-row>
    <a-row class="grid-demo" style="marginBottom: 16px; backgroundColor: var(--color-fill-2);">
      <a-col :span="6" :offset="8">
        col - 6 | offset - 8
      </a-col>
      <a-col :span="6" :offset="4">
        col - 6 | offset - 4
      </a-col>
    </a-row>
    <a-row class="grid-demo" style="backgroundColor: var(--color-fill-2)">
      <a-col :span="12" :offset="8">
        col - 12 | offset - 8
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.grid-demo .arco-col {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}
.grid-demo .arco-col:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
.grid-demo .arco-col:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}
</style>
```

## Interval of Grid

By specifying `gutter` on `Row`, the area interval of the grid can be increased

```vue
<template>
  <div>
    <p>Horizontal</p>
    <a-row class="grid-demo" :gutter="24">
      <a-col :span="12">
        <div>col - 12</div>
      </a-col>
      <a-col :span="12">
        <div>col - 12</div>
      </a-col>
    </a-row>
    <p>Responsive</p>
    <a-row class="grid-demo" :gutter="{ md: 8, lg: 24, xl: 32 }">
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
    </a-row>
    <p>Horizontal and Vertical</p>
    <a-row class="grid-demo" :gutter="[24, 12]">
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.grid-demo .arco-col {
  height: 48px;
  color: var(--color-white);
}
.grid-demo .arco-col > div {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
.grid-demo .arco-col:nth-child(2n) > div {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
.grid-demo .arco-col:nth-child(2n + 1) > div {
  background-color: var(--color-primary-light-4);
}
</style>
```

## Horizontal Layout

Use `justify` for horizontal layout

```vue
<template>
  <div>
    <p>Arrange left</p>
    <a-row class="grid-demo" justify="start">
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
    </a-row>
    <p>Arrange center</p>
    <a-row class="grid-demo" justify="center">
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
    </a-row>
    <p>Arrange right</p>
    <a-row class="grid-demo" justify="end">
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
    </a-row>
    <p>Space around</p>
    <a-row class="grid-demo" justify="space-around">
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
    </a-row>
    <p>Space between</p>
    <a-row class="grid-demo" justify="space-between">
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
      <a-col :span="4">
        <div>col - 4</div>
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.grid-demo {
  background-color: var(--color-fill-2);
  margin-bottom: 40px;
}
.grid-demo:last-child {
  margin-bottom: 0px;
}
.grid-demo .arco-col {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}
.grid-demo .arco-col:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
.grid-demo .arco-col:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}
</style>
```

## Vertical Layout

Use `align` for vertical layout.

```vue
<template>
  <div>
    <p>Arrange top</p>
    <a-row class="grid-demo" align="start">
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
    </a-row>
    <p>Arrange center</p>
    <a-row class="grid-demo" align="center">
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
    </a-row>
    <p>Arrange bottom</p>
    <a-row class="grid-demo" align="end">
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
      <a-col :span="6">
        <div>col - 6</div>
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.grid-demo {
  background-color: var(--color-fill-2);
  margin-bottom: 40px;
}
.grid-demo:last-child {
  margin-bottom: 0px;
}
.grid-demo .arco-col {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}
.grid-demo .arco-col:nth-of-type(1) {
  height: 90px;
  line-height: 90px;
}
.grid-demo .arco-col:nth-of-type(2) {
  height: 48px;
  line-height: 48px;
}
.grid-demo .arco-col:nth-of-type(3) {
  height: 120px;
  line-height: 120px;
}
.grid-demo .arco-col:nth-of-type(4) {
  height: 60px;
  line-height: 60px;
}
.grid-demo .arco-col:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
.grid-demo .arco-col:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}
</style>
```

## Order

Sort elements by `order`.

```vue
<template>
  <div>
    <a-row class="grid-demo">
      <a-col :span="6" :order="4">
        <div>1 col-order-4</div>
      </a-col>
      <a-col :span="6" :order="3">
        <div>2 col-order-3</div>
      </a-col>
      <a-col :span="6" :order="2">
        <div>3 col-order-2</div>
      </a-col>
      <a-col :span="6" :order="1">
        <div>4 col-order-1</div>
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.grid-demo .arco-col {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}
.grid-demo .arco-col:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
.grid-demo .arco-col:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}
</style>
```

## Responsive Layout

Six preset response sizes, namely `xs`, `sm`, `md`, `lg`, `xl`, `xxl`

```vue
<template>
  <a-row class="grid-demo">
    <a-col :xs="2" :sm="4" :md="6" :lg="8" :xl="10" :xxl="8">
      Col
    </a-col>
    <a-col :xs="20" :sm="16" :md="12" :lg="8" :xl="4" :xxl="8">
      Col
    </a-col>
    <a-col :xs="2" :sm="4" :md="6" :lg="8" :xl="10" :xxl="8">
      Col
    </a-col>
  </a-row>
</template>

<style scoped>
.grid-demo .arco-col {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}
.grid-demo .arco-col:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
.grid-demo .arco-col:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}
</style>
```

## Advanced Responsive Layout

The `span`, `offset`, and `order` properties can be embedded in `xs`, `sm`, `md`, `lg`, `xl`, `xxl` objects.
For example, `:xs="8"` is equivalent to `:xs="{ span: 8 }"`

```vue
<template>
  <div>
    <a-row class="grid-demo">
      <a-col :xs="{span: 5, offset: 1}" :lg="{span: 6, offset: 2}">
        Col
      </a-col>
      <a-col :xs="{span: 11, offset: 1}" :lg="{span: 6, offset: 2}">
        Col
      </a-col>
      <a-col :xs="{span: 5, offset: 1}" :lg="{span: 6, offset: 2}">
        Col
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.grid-demo .arco-col {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}
.grid-demo .arco-col:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
.grid-demo .arco-col:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}
</style>
```

## Flex

By setting the `flex` property of the `Col` component, you can configure the flex layout arbitrarily.

```vue
<template>
  <a-row class="grid-demo" style="margin-bottom: 16px;">
    <a-col flex="100px">
      <div>100px</div>
    </a-col>
    <a-col flex="auto">
      <div>auto</div>
    </a-col>
  </a-row>
  <a-row class="grid-demo" style="margin-bottom: 16px;">
    <a-col flex="100px">
      <div>100px</div>
    </a-col>
    <a-col flex="auto">
      <div>auto</div>
    </a-col>
    <a-col flex="100px">
      <div>100px</div>
    </a-col>
  </a-row>
  <a-row class="grid-demo" style="margin-bottom: 16px;">
    <a-col :flex="3">
      <div>3 / 12</div>
    </a-col>
    <a-col :flex="4">
      <div>4 / 12</div>
    </a-col>
    <a-col :flex="5">
      <div>5 / 12</div>
    </a-col>
  </a-row>
</template>

<style scoped>
.grid-demo .arco-col {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}

.grid-demo .arco-col:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}

.grid-demo .arco-col:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
</style>
```

## Grid Layout

A layout component implemented by CSS-based Grid layout, supports folding, and can set suffix nodes, which will always be displayed at the end of a line.

```vue

<template>
  <div style="margin-bottom: 20px;">
    <a-typography-text>Collapsed:</a-typography-text>
    <a-switch :checked="collapsed" @click="collapsed = !collapsed" />
  </div>
  <a-grid :cols="3" :colGap="12" :rowGap="16" class="grid-demo-grid" :collapsed="collapsed">
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item" :offset="1">item | offset - 1</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item" :span="3">item | span - 3</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item" suffix #="{ overflow }">
      suffix | overflow: {{ overflow }}
    </a-grid-item>
  </a-grid>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const collapsed = ref(false);

    return {
      collapsed
    }
  },
}
</script>

<style scoped>
.grid-demo-grid .demo-item,
.grid-demo-grid .demo-suffix {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}

.grid-demo-grid .demo-item:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}

.grid-demo-grid .demo-item:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}
</style>
```

## Responsive Grid Layout

The responsive configuration format of the Grid component is `{ xs: 1, sm: 2, md: 3, lg: 4, xl: 5, xxl: 6 }`.

```vue
<template>
  <a-grid :cols="{ xs: 1, sm: 2, md: 3, lg: 4, xl: 5, xxl: 6 }" :colGap="12" :rowGap="16" class="grid-demo-grid">
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item">item</a-grid-item>
    <a-grid-item class="demo-item" :span="{ xl: 4, xxl: 6 }" suffix>
      suffix
    </a-grid-item>
  </a-grid>
</template>

<style scoped>
.grid-demo-grid .demo-item,
.grid-demo-grid .demo-suffix {
  height: 48px;
  line-height: 48px;
  color: var(--color-white);
  text-align: center;
}
.grid-demo-grid .demo-item:nth-child(2n) {
  background-color: rgba(var(--arcoblue-6), 0.9);
}
.grid-demo-grid .demo-item:nth-child(2n + 1) {
  background-color: var(--color-primary-light-4);
}
</style>
```

## API

### `<row>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|gutter|Grid interval in `px`. Pass in the responsive object like {xs: 4, sm: 6, md: 12}. Pass in the array [horizontal spacing, vertical spacing] to set two directions.|`number\| ResponsiveValue\| [number \| ResponsiveValue, number \| ResponsiveValue]`|`0`||
|justify|Horizontal alignment (`justify-content`)|`'start' \| 'center' \| 'end' \| 'space-around' \| 'space-between'`|`'start'`||
|align|Vertical alignment (`align-items`)|`'start' \| 'center' \| 'end' \| 'stretch'`|`'start'`||
|div|Enabling this option `Row` and `Col` will be treated as divs without any Grid-related classes and styles|`boolean`|`false`||
|wrap|Whether `Col` can wrap onto multiple lines|`boolean`|`true`|2.13.0|

### `<col>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|span|Number of grid space|`number`|`24`||
|offset|The number of grids on the left side of the grid. There can be no grids in the grid.|`number`|`-`||
|order|Sort elements|`number`|`-`||
|xs|<576px responsive grid|`number \| { [key: string]: any }`|`-`||
|sm|>= 576px responsive grid|`number \| { [key: string]: any }`|`-`||
|md|>= 768px responsive grid|`number \| { [key: string]: any }`|`-`||
|lg|>= 992px responsive grid|`number \| { [key: string]: any }`|`-`||
|xl|>= 1200px responsive grid|`number \| { [key: string]: any }`|`-`||
|xxl|>= 1600px responsive grid|`number \| { [key: string]: any }`|`-`||
|flex|Set flex layout properties|`number \| string \| 'initial' \| 'auto' \| 'none'`|`-`|2.10.0|

### `<grid>` Props (2.15.0)
Responsive configuration has been supported since `2.18.0`, the specific configuration [ResponsiveValue](#responsivevalue)

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|cols|Number of columns displayed in each row|`number \| ResponsiveValue`|`24`|
|row-gap|The space in row-to-row|`number \| ResponsiveValue`|`0`|
|col-gap|The space in column-to-column|`number \| ResponsiveValue`|`0`|
|collapsed|Whether to collapsed|`boolean`|`false`|
|collapsed-rows|Number of rows displayed when collapsed|`number`|`1`|

### `<grid-item>` Props (2.15.0)
Responsive configuration has been supported since `2.18.0`, the specific configuration [ResponsiveValue](#responsivevalue)

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|span|Number of grids spanned|`number \| ResponsiveValue`|`1`|
|offset|Number of grids on the left|`number \| ResponsiveValue`|`0`|
|suffix|Is it a suffix element|`boolean`|`false`|

### ResponsiveValue

|Name|Description|Type|Default|
|---|---|---|:---:|
|xxl|>= 1600px responsive configuration|`number`|`-`|
|xl|>= 1200px responsive configuration|`number`|`-`|
|lg|>= 992px responsive configuration|`number`|`-`|
|md|>= 768px responsive configuration|`number`|`-`|
|sm|>= 576px responsive configuration|`number`|`-`|
|xs|<576px responsive configuration|`number`|`-`|
