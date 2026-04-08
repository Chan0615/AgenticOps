---
name: arco-vue-input-tag
description: "Used to enter the label. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# InputTag

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of tag input.

```vue
<template>
  <a-input-tag :default-value="['test']" :style="{width:'320px'}" placeholder="Please Enter" allow-clear/>
</template>
```

## Status

The input box has three states: disabled, readonly and error.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-tag :default-value="['test']" :style="{width:'320px'}" placeholder="Please Enter" disabled/>
    <a-input-tag :default-value="['test']" :style="{width:'320px'}" placeholder="Please Enter" readonly/>
    <a-input-tag :default-value="['test']" :style="{width:'320px'}" placeholder="Please Enter" error/>
  </a-space>
</template>
```

## Max Tags

Set the maximum number of display labels.

```vue
<template>
  <a-input-tag :default-value="['one','two','three','four']" :style="{width:'380px'}" placeholder="Please Enter" :max-tag-count="3" allow-clear/>
</template>
```

## Input Size

The input box is divided into four sizes: `mini`, `small`, `medium`, and `large`.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-radio-group type="button" v-model="size">
      <a-radio value="mini">mini</a-radio>
      <a-radio value="small">small</a-radio>
      <a-radio value="medium">medium</a-radio>
      <a-radio value="large">large</a-radio>
    </a-radio-group>
    <a-input-tag :default-value="['one']" :style="{width:'320px'}" placeholder="Please enter something" :size="size" allow-clear />
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const size = ref('medium');

    return {
      size
    }
  },
}
</script>
```

## API

### `<input-tag>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`(string \| number \| TagData)[]`|`-`||
|default-value|Default value (uncontrolled state)|`(string \| number \| TagData)[]`|`[]`||
|input-value **(v-model)**|The value of the input|`string`|`-`||
|default-input-value|The default value of the input (uncontrolled state)|`string`|`''`||
|placeholder|Placeholder|`string`|`-`||
|disabled|Whether to disable|`boolean`|`false`||
|error|Whether it is an error state|`boolean`|`false`||
|readonly|Whether it is read-only mode|`boolean`|`false`||
|allow-clear|Whether to allow clear|`boolean`|`false`||
|size|The size of the input|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|max-tag-count|The maximum number of tags displayed, `0` means unlimited|`number`|`0`||
|retain-input-value|Whether to keep the content of the input box|`boolean \| { create?: boolean; blur?: boolean }`|`false`||
|format-tag|Format tag content|`(data: TagData) => string`|`-`||
|unique-value|Whether to create only unique values|`boolean`|`false`|2.15.0|
|field-names|Customize fields in `TagData`|`InputTagFieldNames`|`-`|2.22.0|
|tag-nowrap|Tag content does not wrap|`boolean`|`false`|2.56.1|
### `<input-tag>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when the value changes|value: `(string \| number \| TagData)[]`<br>ev: `Event`|
|input-value-change|Trigger when the input value changes|inputValue: `string`<br>ev: `Event`|
|press-enter|Triggered when the enter key is pressed|inputValue: `string`<br>ev: `KeyboardEvent`|
|remove|Triggered when the delete button of the label is clicked|removed: `string \| number`<br>ev: `Event`|
|clear|Triggered when the clear button is clicked|ev: `MouseEvent`|
|focus|Triggered when the input box gets focus|ev: `FocusEvent`|
|blur|Triggered when the input box loses focus|ev: `FocusEvent`|
### `<input-tag>` Methods

|Method|Description|Parameters|Return|
|---|---|---|:---:|
|focus|Make the input box focus|-|-|
|blur|Make the input box lose focus|-|-|
### `<input-tag>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|tag|Display content of tag|data: `TagData`|
|prefix|Prefix|-|
|suffix|Suffix|-|

### TagData

|Name|Description|Type|Default|
|---|---|---|:---:|
|value|Tag value|`string \| number`|`-`|
|label|Tag content|`string`|`-`|
|closable|Whether to close|`boolean`|`false`|
|tagProps|Tag props|`TagProps`|`-`|
