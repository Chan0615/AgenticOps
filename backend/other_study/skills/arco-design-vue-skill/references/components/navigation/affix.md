---
name: arco-vue-affix
description: "Pin the page elements to the visible range. When the content area is relatively long and the page needs to be scrolled, the fixed pin can fix the content on the screen. Often used for side menus and button combinations. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Affix

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

Basic usage, when the fixed position is not set and the scrolling element of the page is not visible, the element is fixed at the top of the page.

```vue
<template>
  <a-affix>
    <a-button type="primary">Affix Top</a-button>
  </a-affix>
</template>
```

## Fixed Top

When the page scrolls or the browser window changes, the element is fixed when it scrolls up to a certain distance from the top.

```vue
<template>
  <a-affix :offsetTop="80">
    <a-button type="primary">80px to affix top</a-button>
  </a-affix>
</template>
```

## Fixed Bottom

When the page scrolls or the browser window changes, the element is fixed when it scrolls down to a certain distance from the bottom.

```vue
<template>
  <a-affix :offsetBottom="120">
    <a-button type="primary">120px to affix bottom</a-button>
  </a-affix>
</template>
```

## Callback

Callback when the fixed state changes.

```vue
<template>
  <a-affix
    :offsetBottom="80"
    @change="onChange"
  >
    <a-button type="primary">80px to affix bottom</a-button>
  </a-affix>
</template>
<script>
import { defineComponent } from 'vue';

export default defineComponent({
  setup() {
    const onChange = (fixed) => {
      console.log(`${fixed}`);
    };
    return {
      onChange
    };
  }
});
</script>
```

## Container

Use `target` to set the element whose scroll event needs to be listened to. Default is window.

When the `target` is specified as a non-window container, the outer element of the `target` may scroll, and the fixed
element may run out of the scroll container. You can pass in `targetContainer` to set the scroll element
outside `target`. `Affix` will monitor the scroll event of the element to update the position of the scroll nail element
in real time. You can also monitor the `scroll` event of the outer scroll element of the target in the business code,
and call `updatePosition` to update the position of the pin.

```vue

<template>
  <div
    style="height: 200px; overflow: auto"
    ref="containerRef"
  >
    <div style="height: 400px; background: #cccccc; overflow: hidden">
      <a-affix
        :offsetTop="20"
        :target="containerRef"
        style="margin: 40px"
      >
        <a-button type="primary">Affix in scrolling container</a-button>
      </a-affix>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const containerRef = ref();

    return {
      containerRef,
    };
  },
}
</script>
```

## API

### `<affix>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|offset-top|Triggered when the specified offset is reached from the top of the window|`number`|`0`|
|offset-bottom|Triggered when the specified offset is reached from the bottom of the window|`number`|`-`|
|target|Scroll container, default is `window`|`string \| HTMLElement \| Window`|`-`|
|target-container|The outer scroll element of `target`, the default is `window`. `Affix` will monitor the scroll event of the element and update the position of the anchor in real time. The main purpose is to solve the problem that if the outer element scrolls when the target attribute is specified as a non-window element, it may cause the nail to escape from the container.|`string \| HTMLElement \| Window`|`-`|
### `<affix>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when the fixed state changes|fixed: `boolean`|
### `<affix>` Methods

|Method|Description|Parameters|Return|
|---|---|---|:---:|
|updatePosition|Update position|-|-|
