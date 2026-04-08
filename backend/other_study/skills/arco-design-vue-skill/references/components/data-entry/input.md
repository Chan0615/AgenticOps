---
name: arco-vue-input
description: "Basic form components have been expanded on the basis of native controls and can be used in combination. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Input

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

The basic usage of input

```vue
<template>
  <a-space>
    <a-input :style="{width:'320px'}" placeholder="Please enter something" allow-clear />
    <a-input :style="{width:'320px'}" default-value="content" placeholder="Please enter something" allow-clear />
  </a-space>
</template>
```

## Status

The input box can be set to disable and error status.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input :style="{width:'320px'}" placeholder="Disabled status" disabled/>
    <a-input :style="{width:'320px'}" default-value="Disabled" placeholder="Disabled status" disabled/>
    <a-input :style="{width:'320px'}" placeholder="Error status" error/>
  </a-space>
</template>
```

## Input Size

The input box defines four default sizes `mini, small, medium, large`, which are `24px, 28px, 32px, 36px` respectively.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-radio-group type="button" v-model="size">
      <a-radio value="mini">mini</a-radio>
      <a-radio value="small">small</a-radio>
      <a-radio value="medium">medium</a-radio>
      <a-radio value="large">large</a-radio>
    </a-radio-group>
    <a-input :style="{width:'320px'}" placeholder="Please enter something" :size="size" allow-clear />
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

## Prefix & Suffix

Add prefix and suffix in the input box by specifying the `prefix` and `suffix` slots.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input :style="{width:'320px'}" placeholder="Please enter something" allow-clear>
      <template #prefix>
        <icon-user />
      </template>
    </a-input>
    <a-input :style="{width:'320px'}" placeholder="Please enter something" allow-clear>
      <template #suffix>
        <icon-info-circle />
      </template>
    </a-input>
  </a-space>
</template>
```

## Prepend & Append

Add elements before and after the input box by specifying the `prepend` and `append` slots.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input :style="{width:'320px'}" placeholder="Please enter something" allow-clear>
      <template #prepend>
        +86
      </template>
    </a-input>
    <a-input :style="{width:'320px'}" placeholder="Please enter something" allow-clear>
      <template #append>
        RMB
      </template>
    </a-input>

    <a-input :style="{width:'320px'}" placeholder="Please enter something" allow-clear prepend="+86">
    </a-input>
    <a-input :style="{width:'320px'}" placeholder="Please enter something" allow-clear append="RMB">
    </a-input>
  </a-space>
</template>
```

## Word Limit

Set `max-length` to limit the maximum number of words, and use `show-word-limit` to display word count statistics.

```vue
<template>
  <a-space direction="vertical" size="large" fill>
    <a-input :style="{width:'320px'}" placeholder="Please enter something" :max-length="10" allow-clear show-word-limit />
    <a-input :style="{width:'320px'}" placeholder="Please enter something" :max-length="{length:10,errorOnly:true}" allow-clear show-word-limit />
  </a-space>
</template>
```

## Input group

Input boxes can be combined by `input-group`.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-group>
      <a-input :style="{width:'160px'}" placeholder="first" />
      <a-input :style="{width:'160px'}" placeholder="second" />
    </a-input-group>
    <a-input-group>
      <a-select :options="['Option1','Option2','Option3']" :style="{width:'160px'}" placeholder="first" />
      <a-input :style="{width:'160px'}" placeholder="second" />
    </a-input-group>
  </a-space>
</template>
```

## Search Input

An input box with a search button for content retrieval.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-search :style="{width:'320px'}" placeholder="Please enter something"/>
    <a-input-search :style="{width:'320px'}" placeholder="Please enter something" search-button/>
  </a-space>
</template>
```

## Custom search button

Customize the content of the search button

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-search :style="{width:'320px'}" placeholder="Please enter something" button-text="Search" search-button/>
    <a-input-search :style="{width:'320px'}" placeholder="Please enter something" search-button>
      <template #button-icon>
        <icon-search/>
      </template>
      <template #button-default>
        Search
      </template>
    </a-input-search>
  </a-space>
</template>
```

## Search Input (Loading)

The `loading` property allows the search box to display the loading status.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-search :style="{width:'320px'}" placeholder="Please enter something" loading />
    <a-input-search :style="{width:'320px'}" placeholder="Please enter something" search-button loading />
  </a-space>
</template>
```

## Password Input

Used to enter a password.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-switch v-model="visibility" />
    <a-input-password
      v-model:visibility="visibility"
      placeholder="Please enter something"
      :style="{width:'320px'}"
      :defaultVisibility="false"
      allow-clear
    />
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const visibility = ref(true);

    return {
      visibility
    }
  },
}
</script>
```

## API

### `<input>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`string`|`-`||
|default-value|Default value (uncontrolled state)|`string`|`''`||
|size|Input size|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|allow-clear|Whether to allow the input to be cleared|`boolean`|`false`||
|disabled|Whether to disable|`boolean`|`false`||
|readonly|Whether it is read-only|`boolean`|`false`||
|error|Whether it is an error state|`boolean`|`false`||
|placeholder|Prompt text|`string`|`-`||
|max-length|Enter the maximum length of the value, the errorOnly attribute was added in version 2.12.0|`number \| { length: number; errorOnly?: boolean }`|`0`||
|show-word-limit|Whether to display word count|`boolean`|`false`||
|word-length|Calculation method of word length|`(value: string) => number`|`-`||
|word-slice|Character interception method, used together with wordLength|`(value: string, maxLength: number) => string`|`-`|2.12.0|
|input-attrs|Attributes of inner input elements|`object`|`-`|2.27.0|
|prepend|Prepend|`string`|`-`|2.57.0|
|append|Append|`string`|`-`|2.57.0|
### `<input>` Events

|Event Name|Description|Parameters|
|---|---|---|
|input|Triggered when the user enters|value: `string`<br>ev: `Event`|
|change|Only triggered when the input box is out of focus or when you press Enter|value: `string`<br>ev: `Event`|
|press-enter|Triggered when the user presses enter|ev: `KeyboardEvent`|
|clear|Triggered when the user clicks the clear button|ev: `MouseEvent`|
|focus|Triggered when the input box gets focus|ev: `FocusEvent`|
|blur|Triggered when the input box loses focus|ev: `FocusEvent`|
### `<input>` Methods

|Method|Description|Parameters|Return|
|---|---|---|:---:|
|focus|Make the input box focus|-|-|
|blur|Make the input box lose focus|-|-|
### `<input>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|append|Append|-|
|prepend|Prepend|-|
|suffix|Suffix|-|
|prefix|Prefix|-|

### `<input-password>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|visibility **(v-model)**|Whether is visible|`boolean`|`-`|
|default-visibility|Default visibility|`boolean`|`true`|
|invisible-button|Whether to show visible buttons|`boolean`|`true`|
### `<input-password>` Events

|Event Name|Description|Parameters|
|---|---|---|
|visibility-change|Callback when visibility changes|visible: `boolean`|

### `<input-search>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|search-button|Whether it is the rear button mode|`boolean`|`false`||
|loading|Whether it is loading state|`boolean`|`false`||
|disabled|Whether to disable|`boolean`|`false`||
|size|Input size|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|button-text|The text of the search button will replace the original icon after use|`string`|`-`|2.16.0|
|button-props|Button props|`ButtonProps`|`-`||
### `<input-search>` Events

|Event Name|Description|Parameters|
|---|---|---|
|search|Triggered when the search button is clicked|value: `string`<br>ev: `MouseEvent`|
