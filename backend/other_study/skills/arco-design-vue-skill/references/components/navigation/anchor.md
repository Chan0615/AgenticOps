---
name: arco-vue-anchor
description: "Through the anchor point, you can quickly find the position of the information content on the current page. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Anchor

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of anchors

```vue
<template>
  <a-anchor>
    <a-anchor-link href="#basic">Basic</a-anchor-link>
    <a-anchor-link href="#line-less">LineLess Mode</a-anchor-link>
    <a-anchor-link href="#affix">
      Affix
      <template #sublist>
        <a-anchor-link href="#boundary">Scroll Boundary</a-anchor-link>
        <a-anchor-link href="#hash">Hash mode</a-anchor-link>
      </template>
    </a-anchor-link>
  </a-anchor>
</template>
```

## Line Less

When setting `line-less`, you can use an anchor style without a left axis.

```vue
<template>
  <a-anchor line-less>
    <a-anchor-link href="#basic">Basic</a-anchor-link>
    <a-anchor-link href="#line-less">LineLess Mode</a-anchor-link>
    <a-anchor-link href="#affix">
      Affix
      <template #sublist>
        <a-anchor-link href="#boundary">Scroll Boundary</a-anchor-link>
        <a-anchor-link href="#hash">Hash mode</a-anchor-link>
      </template>
    </a-anchor-link>
  </a-anchor>
</template>
```

## Affix Position

Use the `affix` component to fix the anchor point within the page.

```vue
<template>
  <a-affix :offsetTop="80">
    <a-anchor :style="{backgroundColor: 'var(--color-bg-1)'}">
      <a-anchor-link href="#basic">Basic</a-anchor-link>
      <a-anchor-link href="#line-less">LineLess Mode</a-anchor-link>
      <a-anchor-link href="#affix">
        Affix
        <template #sublist>
          <a-anchor-link href="#boundary">Scroll Boundary</a-anchor-link>
          <a-anchor-link href="#hash">Hash mode</a-anchor-link>
        </template>
      </a-anchor-link>
    </a-anchor>
  </a-affix>
</template>
```

## boundary

You can set `boundary` to customize the anchor point scroll offset.

```vue
<template>
  <a-anchor boundary="center">
    <a-anchor-link href="#basic">Basic</a-anchor-link>
    <a-anchor-link href="#line-less">LineLess Mode</a-anchor-link>
    <a-anchor-link href="#affix">
      Affix
      <template #sublist>
        <a-anchor-link href="#boundary">Scroll Boundary</a-anchor-link>
        <a-anchor-link href="#hash">Hash mode</a-anchor-link>
      </template>
    </a-anchor-link>
  </a-anchor>
</template>
```

## Hash

You can set the click anchor without changing the browser history.

```vue
<template>
  <a-anchor :change-hash="false">
    <a-anchor-link href="#basic">Basic</a-anchor-link>
    <a-anchor-link href="#line-less">LineLess Mode</a-anchor-link>
    <a-anchor-link href="#affix">
      Affix
      <template #sublist>
        <a-anchor-link href="#boundary">Scroll Boundary</a-anchor-link>
        <a-anchor-link href="#hash">Hash mode</a-anchor-link>
      </template>
    </a-anchor-link>
  </a-anchor>
</template>
```

## API

### `<anchor>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|boundary|Scrolling boundary value. After setting the value to a number, it will stop scrolling when the distance is `boundary` from the scrolling container.|`'start' \| 'end' \| 'center' \| 'nearest' \| number`|`'start'`|
|line-less|Whether to show the left axis|`boolean`|`false`|
|scroll-container|Scroll container|`string \| HTMLElement \| Window`|`-`|
|change-hash|Whether to change the hash. When set to `false`, clicking on the anchor will not change the hash of the page|`boolean`|`true`|
|smooth|Whether to use smooth scrolling|`boolean`|`true`|
### `<anchor>` Events

|Event Name|Description|Parameters|
|---|---|---|
|select|Triggered when the user clicks on the link|hash: ` string \| undefined `<br>preHash: `string`|
|change|Triggered when the link changes|hash: `string`|

### `<anchor-link>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|title|The text content of the anchor link|`string`|`-`|
|href|The address of the anchor link|`string`|`-`|
