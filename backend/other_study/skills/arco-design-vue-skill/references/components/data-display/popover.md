---
name: arco-vue-popover
description: "When the mouse hovers, focus, or click on a component, a bubble-like card floating layer will pop up. You can manipulate the elements on the card. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Popover

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Move the mouse in or click to pop up bubbles, which can operate on the elements on the floating layer, and carry complex content and operations.

```vue
<template>
  <a-popover title="Title">
    <a-button>Hover</a-button>
    <template #content>
      <p>Here is the text content</p>
      <p>Here is the text content</p>
    </template>
  </a-popover>
</template>
```

## Trigger

By setting `trigger`, you can specify different trigger methods.

```vue
<template>
  <a-space>
    <a-popover title="Title">
      <a-button>Hover Me</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover title="Title" trigger="click">
      <a-button>Click Me</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
  </a-space>
</template>
```

## Popup Position

`Popover` supports 12 different positions. They are: `upper left` `upper` `upper right` `lower left` `down` `lower right` `upper left` `left` `lower left` `upper right` `right` `lower right`.

```vue
<template>
  <div :style="{position: 'relative', width: '440px', height: '280px'}">
    <a-popover position="tl">
      <a-button class="button" :style="{position: 'absolute',top:'0',left:'70px'}">TL</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="top">
      <a-button class="button" :style="{position: 'absolute',top:'0',left:'180px'}">TOP</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="tr">
      <a-button class="button" :style="{position: 'absolute',top:'0',left:'290px'}">TR</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="bl">
      <a-button class="button" :style="{position: 'absolute',top:'240px',left:'70px'}">BL</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="bottom">
      <a-button class="button" :style="{position: 'absolute',top:'240px',left:'180px'}">BOTTOM</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="br">
      <a-button class="button" :style="{position: 'absolute',top:'240px',left:'290px'}">BR</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="lt">
      <a-button class="button" :style="{position: 'absolute',top:'60px',left:'10px'}">LT</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="left">
      <a-button class="button" :style="{position: 'absolute',top:'120px',left:'10px'}">LEFT</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="lb">
      <a-button class="button" :style="{position: 'absolute',top:'180px',left:'10px'}">LB</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="rt">
      <a-button class="button" :style="{position: 'absolute',top:'60px',left:'350px'}">RT</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="right">
      <a-button class="button" :style="{position: 'absolute',top:'120px',left:'350px'}">RIGHT</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
    <a-popover position="rb">
      <a-button class="button" :style="{position: 'absolute',top:'180px',left:'350px'}">RB</a-button>
      <template #content>
        <p>Here is the text content</p>
        <p>Here is the text content</p>
      </template>
    </a-popover>
  </div>
</template>

<style scoped lang="less">
.button{
  width: 100px;
}
</style>
```

`<popover>` inherits all props from `<trigger>`.

## API

### `<popover>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|popup-visible **(v-model)**|Whether the popover is visible|`boolean`|`-`|
|default-popup-visible|Whether the popover is visible by default (uncontrolled mode)|`boolean`|`false`|
|title|Title|`string`|`-`|
|content|Content|`string`|`-`|
|trigger|Trigger method|`'hover' \| 'click' \| 'focus' \| 'contextMenu'`|`'hover'`|
|position|Pop-up position|`'top' \| 'tl' \| 'tr' \| 'bottom' \| 'bl' \| 'br' \| 'left' \| 'lt' \| 'lb' \| 'right' \| 'rt' \| 'rb'`|`'top'`|
|content-class|The class name of the popup content|`ClassName`|`-`|
|content-style|The style of the popup content|`CSSProperties`|`-`|
|arrow-class|The class name of the popup arrow|`ClassName`|`-`|
|arrow-style|The style of the popup arrow|`CSSProperties`|`-`|
|popup-container|Mount container for pop-up box|`string \| HTMLElement`|`-`|
### `<popover>` Events

|Event Name|Description|Parameters|
|---|---|---|
|popup-visible-change|Triggered when the text bubble display status changes|visible: `boolean`|
### `<popover>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|title|Title|-|
|content|Content|-|
