---
name: arco-vue-popconfirm
description: "Click on the element and a popconfirm will pop up. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Popconfirm

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of popconfirm.

```vue
<template>
  <a-popconfirm content="Are you sure you want to delete?">
    <a-button>Click To Delete</a-button>
  </a-popconfirm>
</template>
```

## Custom Button

Customize the text or icon of the button.

```vue
<template>
  <a-popconfirm content="Do you want to discard the draft?" okText="Discard" cancelText="No">
    <a-button>Discard</a-button>
  </a-popconfirm>
</template>
```

## Popup Position

`popconfirm` supports 12 different positions. They are: `upper left` `upper` `upper right` `lower left` `down` `lower right` `upper left` `left` `lower left` `upper right` `right` `lower right`.

```vue
<template>
  <div :style="{position: 'relative', width: '440px', height: '280px'}">
    <a-popconfirm content="This is a Popconfirm" position="tl">
      <a-button class="button" :style="{position: 'absolute',top:'0',left:'70px'}">TL</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="top">
      <a-button class="button" :style="{position: 'absolute',top:'0',left:'180px'}">TOP</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="tr">
      <a-button class="button" :style="{position: 'absolute',top:'0',left:'290px'}">TR</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="bl">
      <a-button class="button" :style="{position: 'absolute',top:'240px',left:'70px'}">BL</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="bottom">
      <a-button class="button" :style="{position: 'absolute',top:'240px',left:'180px'}">BOTTOM</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="br">
      <a-button class="button" :style="{position: 'absolute',top:'240px',left:'290px'}">BR</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="lt">
      <a-button class="button" :style="{position: 'absolute',top:'60px',left:'10px'}">LT</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="left">
      <a-button class="button" :style="{position: 'absolute',top:'120px',left:'10px'}">LEFT</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="lb">
      <a-button class="button" :style="{position: 'absolute',top:'180px',left:'10px'}">LB</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="rt">
      <a-button class="button" :style="{position: 'absolute',top:'60px',left:'350px'}">RT</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="right">
      <a-button class="button" :style="{position: 'absolute',top:'120px',left:'350px'}">RIGHT</a-button>
    </a-popconfirm>
    <a-popconfirm content="This is a Popconfirm" position="rb">
      <a-button class="button" :style="{position: 'absolute',top:'180px',left:'350px'}">RB</a-button>
    </a-popconfirm>
  </div>
</template>

<style scoped lang="less">
.button{
  width: 100px;
}
</style>
```

## Type

The type of the confirmation box can be set via the `type` property.

```vue
<template>
  <a-space>
    <a-popconfirm content="Are you sure you want to delete?" type="info">
      <a-button>Click To Delete</a-button>
    </a-popconfirm>
    <a-popconfirm content="Are you sure you want to delete?" type="success">
      <a-button>Click To Delete</a-button>
    </a-popconfirm>
    <a-popconfirm content="Are you sure you want to delete?" type="warning">
      <a-button>Click To Delete</a-button>
    </a-popconfirm>
    <a-popconfirm content="Are you sure you want to delete?" type="error">
      <a-button>Click To Delete</a-button>
    </a-popconfirm>
  </a-space>
</template>
```

`<popconfirm>` inherits all props from `<trigger>`.

## API

### `<popconfirm>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|content|Content|`string`|`-`|
|position|Popup position|`'top' \| 'tl' \| 'tr' \| 'bottom' \| 'bl' \| 'br' \| 'left' \| 'lt' \| 'lb' \| 'right' \| 'rt' \| 'rb'`|`'top'`|
|popup-visible **(v-model)**|Whether the popconfirm is visible|`boolean`|`-`|
|default-popup-visible|Whether the popconfirm is visible by default (uncontrolled mode)|`boolean`|`false`|
|type|Types of the popconfirm|`'info' \| 'success' \| 'warning' \| 'error'`|`'info'`|
|ok-text|The content of the ok button|`string`|`-`|
|cancel-text|The content of the cancel button|`string`|`-`|
|ok-loading|Whether the ok button is in the loading state|`boolean`|`false`|
|ok-button-props|Props of ok button|`ButtonProps`|`-`|
|cancel-button-props|Props of cancel button|`ButtonProps`|`-`|
|content-class|The class name of the popup content|`ClassName`|`-`|
|content-style|The style of the popup content|`CSSProperties`|`-`|
|arrow-class|The class name of the popup arrow|`ClassName`|`-`|
|arrow-style|The style of the popup arrow|`CSSProperties`|`-`|
|popup-container|Mount container for popup|`string \| HTMLElement`|`-`|
|on-before-ok|The callback function before the ok event is triggered. If false is returned, subsequent events will not be triggered, and done can also be used to close asynchronously.|`(  done: (closed: boolean) => void) => void \| boolean \| Promise<void \| boolean>`|`-`|
|on-before-cancel|The callback function before the cancel event is triggered. If it returns false, no subsequent events will be triggered.|`() => boolean`|`-`|
### `<popconfirm>` Events

|Event Name|Description|Parameters|
|---|---|---|
|popup-visible-change|Triggered when the visible or hidden state of the bubble confirmation box changes|visible: `boolean`|
|ok|Triggered when the confirm button is clicked|-|
|cancel|Triggered when the cancel button is clicked|-|
### `<popconfirm>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|icon|Icon|-|
|content|Content|-|
