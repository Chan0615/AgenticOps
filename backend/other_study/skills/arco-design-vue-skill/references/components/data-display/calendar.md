---
name: arco-vue-calendar
description: "Calendar Component. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Calendar

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Display and select calendars

```vue

<template>
  <a-calendar v-model="value" />
  select: {{value}}
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref(new Date('2023-01-01'));

    return {
      value
    }
  },
}
</script>
```

## API

### `<calendar>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|model-value **(v-model)**|Value|`date`|`-`|
|default-value|Default value (uncontrolled state)|`date`|`-`|
|mode|Mode|`'month' \| 'year'`|`-`|
|default-mode|Default Mode|`'month' \| 'year'`|`'month'`|
|modes|Displayed mode|`('month' \| 'year')[]`|`['month', 'year']`|
### `<calendar>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Emitted when the button is clicked|date: `Date`|
|panel-change|Emitted when the button is clicked|date: `Date`|
### `<calendar>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|header|Custom header content|year: `number`<br>month: `number`|2.53.0|
|default|Custom cell content|year: `number`<br>month: `number`<br>date: `number`|2.53.0|
