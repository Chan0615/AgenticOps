---
name: arco-vue-rate
description: "The component used for scoring or starring. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Rate

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of rate component.

```vue
<template>
  <a-rate/>
</template>
```

## Half

Specify `allow-half` to enable half selection.

```vue
<template>
  <a-rate :default-value="2.5" allow-half/>
</template>
```

## Custom Color

Color can be customized through color. In addition, you can customize the color of different score values through object form.

```vue
<template>
  <a-space direction="vertical">
    <a-rate color="red" />
    <a-rate :color="color" />
  </a-space>
</template>

<script>
export default {
  setup() {
    const color = {
      2: 'red',
      4: 'green',
      5: 'blue'
    }
    return {
      color
    }
  },
}
</script>
```

## Readonly

Make the scoring component readonly by setting the `readonly` property.

```vue
<template>
  <a-rate :default-value="4" readonly />
</template>
```

## Allow Clear

Allow the score to be cleared by setting `allow-clear`.

```vue
<template>
  <a-rate :default-value="3" allow-clear/>
</template>
```

## Custom Character

You can replace the stars with other characters, such as emoticons, letters, numbers, font icons and even Chinese.

```vue
<template>
  <a-rate :default-value="2">
    <template #character="{ index }">
      <icon-check v-if="index < 3"/>
      <icon-close v-else/>
    </template>
  </a-rate>
</template>
```

## Rate Count

Specify a rate component of any length by specifying `count`.

```vue
<template>
  <a-rate :count="10"/>
</template>
```

## Grading

Use `grading` to use the smiley grading.

```vue
<template>
  <a-rate grading/>
</template>
```

## API

### `<rate>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|count|Total number of rate|`number`|`5`||
|model-value **(v-model)**|Value|`number`|`-`||
|default-value|Default Value|`number`|`0`||
|allow-half|Whether to allow half selection|`boolean`|`false`||
|allow-clear|Whether to allow clear|`boolean`|`false`||
|grading|Whether to enable smile grading|`boolean`|`false`||
|readonly|Whether it is readonly|`boolean`|`false`||
|disabled|Whether to disable|`boolean`|`false`||
|color|Color|`string \| Record<string, string>`|`-`|2.18.0|
### `<rate>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Trigger when the value changes|value: `number`|
|hover-change|Triggered when the mouse moves over the value|value: `number`|
### `<rate>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|character|Character|index: `number`|
