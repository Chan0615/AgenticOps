---
name: arco-vue-dropdown
description: "When there are too many commands on the page, the alternative commands can be stored in the floating container that expands downward. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Dropdown

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

Basic usage of the drop-down menu.

```vue
<template>
  <a-space size="large">
    <a-dropdown @select="handleSelect">
      <a-button>Click Me</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption disabled>Option 2</a-doption>
        <a-doption :value="{ value: 'Option3' }">Option 3</a-doption>
      </template>
    </a-dropdown>
    <a-dropdown @select="handleSelect" disabled>
      <a-button disabled>Click Me</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption disabled>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </template>
    </a-dropdown>
    <a-dropdown @select="handleSelect" :popup-max-height="false">
      <a-button>No Max Height <icon-down/></a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption disabled>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
        <a-doption>Option 4</a-doption>
        <a-doption>Option 5</a-doption>
        <a-doption>Option 6</a-doption>
        <a-doption>Option 7</a-doption>
        <a-doption>Option 8</a-doption>
        <a-doption>Option 9</a-doption>
      </template>
    </a-dropdown>
  </a-space>
</template>

<script>
export default {
  setup() {
    const handleSelect = (v) => {
      console.log(v)
    };

    return {
      handleSelect
    }
  },
}
</script>

<style>
.arco-dropdown-open .arco-icon-down {
  transform: rotate(180deg);
}
</style>
```

## Position

Support to specify 6 pop-up orientations through `position`, which are: top: up, tl: top left, tr: top right, bottom: bottom (default), bl: bottom left, br: bottom right.

```vue
<template>
  <a-space>
    <a-dropdown position="bl">
      <a-button>Bottom Left</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </template>
    </a-dropdown>
    <a-dropdown position="bottom">
      <a-button>Bottom</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </template>
    </a-dropdown>
    <a-dropdown position="br">
      <a-button>Bottom Right</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </template>
    </a-dropdown>
    <a-dropdown position="tl">
      <a-button>Top Left</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </template>
    </a-dropdown>
    <a-dropdown position="top">
      <a-button>Top</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </template>
    </a-dropdown>
    <a-dropdown position="tr">
      <a-button>Top Right</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </template>
    </a-dropdown>
  </a-space>
</template>
```

## Trigger

Specify the trigger method by `trigger`.

```vue
<template>
  <a-space size="large">
    <a-dropdown>
      <a-button>Click Me</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </template>
    </a-dropdown>
    <a-dropdown trigger="hover">
      <a-button>Hover Me</a-button>
      <template #content>
        <a-doption>Option 1</a-doption>
        <a-doption>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </template>
    </a-dropdown>
  </a-space>
</template>
```

## Dropdown button

The `<dropdown-button>` component can be used to display a button with a menu of additional related functions on the right.
`2.16.0` version added support.

```vue
<template>
  <a-space size="large">
    <a-dropdown-button>
      Publish
      <template #content>
        <a-doption>Save now</a-doption>
        <a-doption>Save and Publish</a-doption>
      </template>
    </a-dropdown-button>
    <a-dropdown-button disabled>
      Disabled
      <template #content>
        <a-doption>Save now</a-doption>
        <a-doption>Save and Publish</a-doption>
      </template>
    </a-dropdown-button>
    <a-dropdown-button>
      Publish
      <template #icon>
        <icon-down />
      </template>
      <template #content>
        <a-doption>Save now</a-doption>
        <a-doption>Save and Publish</a-doption>
      </template>
    </a-dropdown-button>
  </a-space>

</template>

<style>
.arco-dropdown-open .arco-icon-down {
  transform: rotate(180deg);
}
</style>
```

## Group

Use the grouping option through the `<dgroup>` component.

```vue
<template>
  <a-dropdown>
    <a-button>Click Me</a-button>
    <template #content>
      <a-dgroup title="Group 1">
        <a-doption>Option 1</a-doption>
        <a-doption>Option 2</a-doption>
        <a-doption>Option 3</a-doption>
      </a-dgroup>
      <a-dgroup title="Group 2">
        <a-doption>Option 4</a-doption>
        <a-doption>Option 5</a-doption>
        <a-doption>Option 6</a-doption>
      </a-dgroup>
    </template>
  </a-dropdown>
</template>
```

## Submenu

Drop-down box with multi-level menu.

```vue
<template>
  <a-dropdown>
    <a-button>Click Me</a-button>
    <template #content>
      <a-doption>Option 1</a-doption>
      <a-dsubmenu value="option-1">
        <template #default>Option 2</template>
        <template #content>
          <a-doption>Option 2-1</a-doption>
          <a-dsubmenu value="option-2-2" trigger="hover">
            <template #default>Option 2-2</template>
            <template #content>
              <a-doption>Option 2-1</a-doption>
              <a-doption>Option 2-2</a-doption>
              <a-doption>Option 2-3</a-doption>
            </template>
            <template #footer>
              <div style="padding: 6px; text-align: center;">
                <a-button>Click</a-button>
              </div>
            </template>
          </a-dsubmenu>
          <a-doption>Option 2-3</a-doption>
        </template>
      </a-dsubmenu>
      <a-doption>Option 3</a-doption>
    </template>
  </a-dropdown>
</template>
```

## Context Menu

After moving into the area, you can click the right mouse button to trigger.

```vue
<template>
  <a-dropdown trigger="contextMenu" alignPoint :style="{display:'block'}">
    <div :style="{display:'flex',alignItems:'center',justifyContent:'center', height:'300px',backgroundColor:'var(--color-fill-2)'}">
      <div>Click Me</div>
    </div>
    <template #content>
      <a-doption>Option 1</a-doption>
      <a-doption>Option 2</a-doption>
      <a-doption>Option 3</a-doption>
    </template>
  </a-dropdown>
</template>
```

## Icon Options

Add an icon in front of the option via the `icon` slot.

```vue
<template>
  <a-dropdown>
    <a-button>Click Me</a-button>
    <template #content>
      <a-doption>
        <template #icon>
          <icon-location />
        </template>
        <template #default>Option 1</template>
      </a-doption>
      <a-doption>
        <template #icon>
          <icon-location />
        </template>
        <template #default>Option 2</template>
      </a-doption>
      <a-doption>
        <template #icon>
          <icon-location />
        </template>
        <template #default>Option 3</template>
      </a-doption>
    </template>
  </a-dropdown>
</template>
```

`<dropdown>` inherits all props from `<trigger>`.

## API

### `<dropdown>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|popup-visible **(v-model)**|Whether the popup is visible|`boolean`|`-`||
|default-popup-visible|Whether the popup is visible by default (uncontrolled mode)|`boolean`|`false`||
|trigger|Trigger method|`'hover' \| 'click' \| 'focus' \| 'contextMenu'`|`'click'`||
|position|Popup position|`'top' \| 'tl' \| 'tr' \| 'bottom' \| 'bl' \| 'br'`|`'bottom'`||
|popup-container|Mount container for popup|`string \| HTMLElement`|`-`||
|popup-max-height|Maximum height of the popup|`boolean\|number`|`true`|2.29.0|
|hide-on-select|Whether to hide popup when the user selects|`boolean`|`true`|2.43.0|
### `<dropdown>` Events

|Event Name|Description|Parameters|
|---|---|---|
|popup-visible-change|Triggered when the display status of the drop-down box changes|visible: `boolean`|
|select|Triggered when the user selects|value: `string \| number \| Record<string, any> \| undefined `<br>ev: `Event`|
### `<dropdown>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|content|Content|-||
|footer|Footer|-|2.10.0|

### `<doption>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|value|Value|`string\|number\|object`|`-`|
|disabled|Whether to disable|`boolean`|`false`|
### `<doption>` Events

|Event Name|Description|Parameters|
|---|---|---|
|click|Emitted when the button is clicked|ev: `MouseEvent`|
### `<doption>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|icon|Icon|-|

### `<dgroup>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|title|Group title|`string`|`-`|
### `<dgroup>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|title|Group title|-|2.10.0|

### `<dsubmenu>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|value|Value (Not useful after version 2.16.0)|`string\|number`|`-`||
|disabled|Whether to disable|`boolean`|`false`|2.10.0|
|trigger|Trigger method|`'hover' \| 'click'`|`'click'`|2.10.0|
|position|Popup position|`'rt' \| 'lt'`|`'rt'`|2.10.0|
|popup-visible **(v-model)**|Whether the popup is visible|`boolean`|`-`||
|default-popup-visible|Whether the popup is visible by default (uncontrolled mode)|`boolean`|`false`||
|option-props|Custom option properties|`object`|`-`|2.29.0|
### `<dsubmenu>` Events

|Event Name|Description|Parameters|
|---|---|---|
|popup-visible-change|Triggered when the display status of the drop-down box changes|visible: `boolean`|
### `<dsubmenu>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|icon|Icon|-|2.29.0|
|content|Submenu content|-||
|footer|Footer|-|2.10.0|

### `<dropdown-button>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|popup-visible **(v-model)**|Whether the popup is visible|`boolean`|`-`|
|default-popup-visible|Whether the popup is visible by default (uncontrolled mode)|`boolean`|`false`|
|trigger|Trigger method|`'hover' \| 'click' \| 'focus' \| 'contextMenu'`|`'click'`|
|position|Popup position|`'top' \| 'tl' \| 'tr' \| 'bottom' \| 'bl' \| 'br'`|`'br'`|
|popup-container|Mount container for popup|`string \| HTMLElement`|`-`|
|disabled|Whether to disable|`boolean`|`false`|
|type|Button type|`string`|`-`|
|size|Button size|`string`|`-`|
|button-props|Button props|`ButtonProps`|`-`|
|hide-on-select|Whether to hide popup when the user selects|`boolean`|`true`|
### `<dropdown-button>` Events

|Event Name|Description|Parameters|
|---|---|---|
|popup-visible-change|Triggered when the display status of the drop-down box changes|visible: `boolean`|
|click|Emitted when the button is clicked|ev: `MouseEvent`|
|select|Triggered when the user selects|value: `string \| number \| Record<string, any> \| undefined`<br>ev: `Event`|
### `<dropdown-button>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|icon|Button icon|popupVisible: `boolean`|
|content|Content|-|
