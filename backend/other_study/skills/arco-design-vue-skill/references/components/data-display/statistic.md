---
name: arco-vue-statistic
description: "Highlight a certain number or group of numbers and statistical data with descriptions. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Statistic

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Use when you need to highlight a certain number or group of numbers or display statistical data with descriptions.

```vue
<template>
  <a-space size="large">
    <a-statistic title="Downloads" :value="125670" show-group-separator />
    <a-statistic extra="Comments" :value="40509" :precision="2" />
  </a-space>
</template>
```

## Custom prefix & suffix

The prefix and suffix can be added through the `prefix` and `suffix` slots.

```vue
<template>
  <a-space size="large">
    <a-statistic title="New Users" :value="125670" show-group-separator >
      <template #suffix>
        <icon-arrow-rise />
      </template>
    </a-statistic>
    <a-statistic title="User Growth Rate" :value="50.52" :precision="2" :value-style="{ color: '#0fbf60' }">
      <template #prefix>
        <icon-arrow-rise />
      </template>
      <template #suffix>%</template>
    </a-statistic>
  </a-space>
</template>
```

## Animation

Numerical animation can be turned on through `animation`.

```vue
<template>
  <a-statistic title="User Growth Rate" :value="50.52" :precision="2" :value-from="0" :start="start" animation>
    <template #prefix>
      <icon-arrow-rise />
    </template>
    <template #suffix>%</template>
  </a-statistic>
  <a-button @click="start=true">Start</a-button>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const start = ref(false);

    return {
      start
    }
  },
}
</script>
```

## Countdown

The basic usage of the countdown component `countdown`.

```vue
<template>
  <a-row>
    <a-col :flex="1">
      <a-countdown
        title="Countdown"
        :value="now + 1000 * 60 * 60 * 2"
        :now="now"
      />
    </a-col>
    <a-col :flex="1">
      <a-countdown
        title="Milliseconds"
        :value="now + 1000 * 60 * 60 * 2"
        :now="now"
        format="HH:mm:ss.SSS"
      />
    </a-col>
    <a-col :flex="1">
      <a-countdown
        title="Days"
        :value="now + 1000 * 60 * 60 * 24 * 4"
        :now="now"
        format="D [days] H [hours] m [minutes] s [seconds]"
      />
    </a-col>
  </a-row>
  <a-space direction="vertical" style="margin-top: 10px">
    <a-countdown
      title="Trigger on finish"
      :value="Date.now() + 5 * 1000"
      format="mm:ss.SSS"
      :now="Date.now()"
      :start="start"
      @finish="handleFinish"
    />
    <a-button @click="start = true" type="primary">Start</a-button>
  </a-space>
</template>

<script>
import { ref } from 'vue';
import { Message } from '@arco-design/web-vue';

export default {
  setup() {
    const now = Date.now();
    const start = ref(false);

    const handleFinish = () => {
      Message.info('Finish');
    };

    return {
      now,
      start,
      handleFinish,
    };
  },
};
</script>
```

## API

### `<statistic>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|title|Title of the numerical display|`string`|`-`||
|value|Numerical display value|`number \| Date`|`-`||
|format|Format of numerical display [dayjs](https://day.js.org/docs/en/display/format) (used in date mode)|`string`|`'HH:mm:ss'`||
|extra|Additional display content|`string`|`-`||
|start|Whether to start animation|`boolean`|`true`||
|precision|Decimal reserved digits (used in digital mode)|`number`|`0`||
|separator|Carry separator (used in number mode)|`string`|`-`||
|show-group-separator|Whether to display the carry separator (used in number mode)|`boolean`|`false`||
|animation|Whether to turn on animation|`boolean`|`false`||
|animation-duration|Animation's duration time|`number`|`2000`||
|value-from|The starting value of the animation|`number`|`-`||
|placeholder|Prompt text (displayed when value is undefined )|`string`|`-`|2.28.0|
|value-style|Custom value style|`CSSProperties`|`-`|2.32.0|
### `<statistic>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|title|Title|-|
|prefix|Prefix|-|
|suffix|Suffix|-|
|extra|Extra content|-|

### `<countdown>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|title|Countdown title|`string`|`-`||
|value|Countdown value|`number`|`() => Date.now() + 300000`||
|now|Used to correct the incorrect display of the initialization time|`number`|`() => Date.now()`||
|format|Countdown display format [dayjs](https://day.js.org/docs/en/display/format)|`string`|`'HH:mm:ss'`||
|start|Whether to start the countdown|`boolean`|`true`||
|value-style|Custom value style|`CSSProperties`|`-`|2.32.0|
### `<countdown>` Events

|Event Name|Description|Parameters|
|---|---|---|
|finish|Callback at the end of the countdown|-|
### `<countdown>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|title|Title|-|
