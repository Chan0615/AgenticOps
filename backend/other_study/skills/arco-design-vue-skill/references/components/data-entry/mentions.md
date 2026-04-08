---
name: arco-vue-mentions
description: "Used to mention someone or something in the input, often used for posting, chatting or commenting. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Mention

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Used to mention someone or something in the input, often used for posting, chatting or commenting.

```vue
<template>
  <a-space direction="vertical" size="large" style="width: 100%">
    <a-mention v-model="value" :data="['Bytedance', 'Bytedesign', 'Bytenumner']" placeholder="enter something" />
    <a-mention v-model="text" :data="['Bytedance', 'Bytedesign', 'Bytenumner']" type="textarea" placeholder="enter something" />
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref('');
    const text = ref('');

    return {
      value,
      text
    }
  }
}
</script>
```

## Custom Prefix

Specify `prefix` to customize the trigger character. The default is `@`, which can be customized to any character.

```vue
<template>
  <a-space direction="vertical" size="large" style="width: 100%">
    <a-mention :data="['Bytedance', 'Bytedesign', 'Bytenumner']" placeholder="input @" />
    <a-mention :data="['Bytedance', 'Bytedesign', 'Bytenumner']" prefix="#" placeholder="input #" />
    <a-mention :data="['Bytedance', 'Bytedesign', 'Bytenumner']" prefix="$" placeholder="input $" />
  </a-space>
</template>
```

## API

### `<mention>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`string`|`-`||
|default-value|Default value (uncontrolled state)|`string`|`''`||
|data|Data for automatic completion|`(string \| number \| SelectOptionData \| SelectOptionGroup)[]`|`[]`||
|prefix|Keywords that trigger auto-completion|`string \| string[]`|`'@'`||
|split|Before and after the selected item separator|`string`|`' '`||
|type|default input or textarea|`'input' \| 'textarea'`|`'input'`||
|disabled|Whether to disable|`boolean`|`false`||
|allow-clear|Whether to allow the input to be cleared|`boolean`|`false`|2.23.0|
### `<mention>` Events

|Event Name|Description|Parameters|version|
|---|---|---|:---|
|change|Triggered when the value changes|value: `string`||
|search|Trigger on dynamic search prefix, version 2.47.0 adds prefix param|value: `string`<br>prefix: `string`||
|select|Triggered when the drop-down option is selected|value: `string \| number \| Record<string, any> \| undefined`||
|clear|Triggered when the user clicks the clear button|-|2.23.0|
|focus|Emitted when the text box gets focus|ev: `FocusEvent`|2.42.0|
|blur|Emitted when the text box loses focus|ev: `FocusEvent`|2.42.0|
### `<mention>` Methods

|Method|Description|Parameters|Return|version|
|---|---|---|:---:|:---|
|focus|Make the input box focus|-|-|2.24.0|
|blur|Make the input box lose focus|-|-|2.24.0|
### `<mention>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|option|Display content of options|data: `OptionInfo`|2.13.0|
