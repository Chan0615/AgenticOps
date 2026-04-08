---
name: arco-vue-back-top
description: "A button to return to the top with one click. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# BackTop

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

When the container is scrolled to a certain height, a button to return to the top will appear in the lower right corner.

```vue
<template>
  <div class="wrapper">
    <ul id="basic-demo">
      <li v-for="(_, index) of Array(40)" :key="index">This is the content</li>
    </ul>
    <a-back-top target-container="#basic-demo" :style="{position:'absolute'}" />
  </div>
</template>

<style scoped lang="less">
.wrapper {
  position: relative;

  ul {
    height: 200px;
    overflow-y: auto;

    li {
      line-height: 30px;
    }
  }
}
</style>
```

## Custom Button

You can customize the back button.

```vue
<template>
  <div class="wrapper">
    <ul id="custom-demo">
      <li v-for="(_, index) of Array(40)" :key="index">This is the content</li>
    </ul>
    <a-back-top target-container="#custom-demo" :style="{position:'absolute'}" >
      <a-button>UP</a-button>
    </a-back-top>
  </div>
</template>

<style scoped lang="less">
.wrapper {
  position: relative;

  ul {
    height: 200px;
    overflow-y: auto;

    li {
      line-height: 30px;
    }
  }
}
</style>
```

## API

### `<back-top>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|visible-height|Display the trigger scroll height of the back to top button|`number`|`200`|
|target-container|Scroll event listener container|`string \| HTMLElement`|`-`|
|easing|Easing mode of scrolling animation, refer to [BTween](https://github.com/PengJiyuan/b-tween) for optional values|`string`|`'quartOut'`|
|duration|Duration of scroll animation|`number`|`200`|
