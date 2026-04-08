---
name: arco-vue-tooltip
description: "A tooltip that popup when the mouse hovers, focus, or click on a component. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Tooltip

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

When the mouse is moved in, the tooltip appears, and when the mouse is moved out, the tooltip disappears.

```vue
<template>
  <a-space>
    <a-tooltip content="This is tooltip content">
      <a-button>Mouse over to display tooltip</a-button>
    </a-tooltip>
    <a-tooltip content="This is a two-line tooltip content.This is a two-line tooltip content.">
      <a-button>Mouse over to display tooltip</a-button>
    </a-tooltip>
  </a-space>
</template>
```

## Mini Size

Suitable for small scenes or digital tooltip styles.

```vue
<template>
  <a-tooltip content="1234" position="top" mini>
    <a-button>Mouse over to display tooltip</a-button>
  </a-tooltip>
</template>
```

## Position

The tooltip supports 12 different orientations. They are: `upper left`, `upper`, `upper right`, `lower left`, `down`, `lower right`, `upper left`, `left`, `lower left`, `upper right`, `right`, `lower right`.

```vue
<template>
  <div :style="{position: 'relative', width: '440px', height: '280px'}">
    <a-tooltip content="This is a Tooltip" position="tl">
      <a-button class="button" :style="{position: 'absolute',top:'0',left:'70px'}">TL</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="top">
      <a-button class="button" :style="{position: 'absolute',top:'0',left:'180px'}">TOP</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="tr">
      <a-button class="button" :style="{position: 'absolute',top:'0',left:'290px'}">TR</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="bl">
      <a-button class="button" :style="{position: 'absolute',top:'240px',left:'70px'}">BL</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="bottom">
      <a-button class="button" :style="{position: 'absolute',top:'240px',left:'180px'}">BOTTOM</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="br">
      <a-button class="button" :style="{position: 'absolute',top:'240px',left:'290px'}">BR</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="lt">
      <a-button class="button" :style="{position: 'absolute',top:'60px',left:'10px'}">LT</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="left">
      <a-button class="button" :style="{position: 'absolute',top:'120px',left:'10px'}">LEFT</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="lb">
      <a-button class="button" :style="{position: 'absolute',top:'180px',left:'10px'}">LB</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="rt">
      <a-button class="button" :style="{position: 'absolute',top:'60px',left:'350px'}">RT</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="right">
      <a-button class="button" :style="{position: 'absolute',top:'120px',left:'350px'}">RIGHT</a-button>
    </a-tooltip>
    <a-tooltip content="This is a Tooltip" position="rb">
      <a-button class="button" :style="{position: 'absolute',top:'180px',left:'350px'}">RB</a-button>
    </a-tooltip>
  </div>
</template>

<style scoped>
.button {
  width: 100px;
}
</style>
```

## Custom Background Color

Customize the background color through the `background-color` property.

```vue
<template>
  <a-space>
    <a-tooltip content="This is tooltip content" background-color="#3491FA">
      <a-button>#3491FA</a-button>
    </a-tooltip>
    <a-tooltip content="This is tooltip content" background-color="#165DFF">
      <a-button>#165DFF</a-button>
    </a-tooltip>
    <a-tooltip content="This is tooltip content" background-color="#722ED1">
      <a-button>#722ED1</a-button>
    </a-tooltip>
  </a-space>
</template>
```

`<tooltip>` inherits all props from `<trigger>`.

## API

### `<tooltip>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|popup-visible **(v-model)**|Whether the tooltip is visible|`boolean`|`-`|
|default-popup-visible|Whether the tooltip is visible by default (uncontrolled mode)|`boolean`|`false`|
|disabled|Whether the tooltip is disabled|`boolean`|`false`|
|content|Tooltip content|`string`|`-`|
|position|Popup position|`'top' \| 'tl' \| 'tr' \| 'bottom' \| 'bl' \| 'br' \| 'left' \| 'lt' \| 'lb' \| 'right' \| 'rt' \| 'rb'`|`'top'`|
|mini|Whether to display as a mini size|`boolean`|`false`|
|background-color|Background color of the popover|`string`|`-`|
|content-class|The class name of the popup content|`ClassName`|`-`|
|content-style|The style of the popup content|`CSSProperties`|`-`|
|arrow-class|The class name of the popup arrow|`ClassName`|`-`|
|arrow-style|The style of the popup arrow|`CSSProperties`|`-`|
|popup-container|Mount container for popup|`string \| HTMLElement`|`-`|
### `<tooltip>` Events

|Event Name|Description|Parameters|
|---|---|---|
|popup-visible-change|Emitted when the tooltip display status changes|visible: `boolean`|
### `<tooltip>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|content|Content|-|
