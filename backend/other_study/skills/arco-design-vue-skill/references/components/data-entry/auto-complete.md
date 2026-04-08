---
name: arco-vue-auto-complete
description: "The auto-complete function of the input. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# AutoComplete

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of auto-complete

```vue
<template>
  <a-auto-complete :data="data" @search="handleSearch" :style="{width:'360px'}" placeholder="please enter something"/>
</template>

<script>
export default {
  data() {
    return {
      data: []
    }
  },
  methods: {
    handleSearch(value) {
      if (value) {
        this.data = [...Array(5)].map((_, index) => `${value}-${index}`)
        console.log(this.data)
      } else {
        this.data = []
      }
    }
  }
}
</script>
```

## Strict

Use the `strict` attribute to specify that the matching is strictly case sensitive.

```vue

<template>
  <a-auto-complete :data="data" :style="{width:'360px'}" placeholder="please enter something" strict />
</template>

<script>
export default {
  data() {
    return {
      data: ['Beijing', 'Shanghai', 'Chengdu', 'WuHan']
    }
  },
}
</script>
```

## Dropdown Footer

custom popup menu footer

```vue
<template>
  <a-auto-complete :data="data" @search="handleSearch" :style="{width:'360px'}" placeholder="please enter something">
    <template #footer>
      <div style="padding: 6px 0; text-align: center;">
        <a-button>Click Me</a-button>
      </div>
    </template>
  </a-auto-complete>
</template>

<script>
export default {
  data() {
    return {
      data: []
    }
  },
  methods: {
    handleSearch(value) {
      if (value) {
        this.data = [...Array(5)].map((_, index) => `${value}-${index}`)
        console.log(this.data)
      } else {
        this.data = []
      }
    }
  }
}
</script>
```

## API

### `<auto-complete>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`string`|`-`||
|default-value|Default value (uncontrolled mode)|`string`|`''`||
|disabled|Whether to disable|`boolean`|`false`||
|data|Data used for auto-complete|`(string \| number \| SelectOptionData \| SelectOptionGroup)[]`|`[]`||
|popup-container|Mount container for popup|`string \| HTMLElement \| null \| undefined`|`-`||
|strict|Whether it is strict verification mode|`boolean`|`false`||
|filter-option|Custom option filtering method|`FilterOption`|`true`||
|trigger-props|trigger props|`TriggerProps`|`-`|2.14.0|
|allow-clear|Whether to allow the input to be cleared|`boolean`|`false`|2.23.0|
|virtual-list-props|Pass the virtual list attribute, pass in this parameter to turn on virtual scrolling [VirtualListProps](#VirtualListProps)|`VirtualListProps`|`-`|2.50.0|
### `<auto-complete>` Events

|Event Name|Description|Parameters|version|
|---|---|---|:---|
|change|Emitted when the value changes|value: `string`||
|search|Emitted when the user searches|value: `string`||
|select|Emitted when an option is selected|value: `string`||
|clear|Triggered when the user clicks the clear button|ev: `Event`|2.23.0|
|dropdown-scroll|Triggered when the drop-down scrolls|ev: `Event`|2.52.0|
|dropdown-reach-bottom|Triggered when the drop-down menu is scrolled to the bottom|ev: `Event`|2.52.0|
### `<auto-complete>` Methods

|Method|Description|Parameters|Return|version|
|---|---|---|:---:|:---|
|focus|Make the input box focus|-|-|2.40.0|
|blur|Make the input box lose focus|-|-|2.40.0|
### `<auto-complete>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|option|Display content of options|data: `OptionInfo`|2.13.0|
|footer|The footer of the popup menu box|-||
