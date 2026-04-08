---
name: arco-vue-slider
description: "Sliding input device, showing current value and selectable range. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Slider

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of sliding input bar.

```vue
<template>
  <a-slider :default-value="50" :style="{ width: '200px' }" />
</template>
```

## Disabled

Disable the slider.

```vue
<template>
  <a-slider :default-value="50" :style="{ width: '200px' }" disabled/>
</template>
```

## Step

Set the step size by `step`, the default step size is 1. It is recommended to set a value that can be divisible by `max-min`, otherwise, the optional maximum value will be less than `max`. When `show-ticks` is set, the step ticks are displayed.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-form :model="data" layout="inline">
      <a-form-item label="Step" field="step">
        <a-input-number :style="{ width: '100px' }" v-model="data.step" />
      </a-form-item>
      <a-form-item label="Show steps" field="showTicks">
        <a-switch v-model="data.showTicks" />
      </a-form-item>
    </a-form>
    <a-slider :default-value="20" :style="{ width: '300px' }" :step="data.step" :show-ticks="data.showTicks" />
  </a-space>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const data = reactive({
      step: 5,
      showTicks: true
    });

    return {
      data
    }
  },
}
</script>
```

## Marks

You can add text labels by setting `marks`.

```vue
<template>
  <a-slider :default-value="5" :style="{ width: '300px' }" :max="15" :marks="marks" />
</template>

<script>
export default {
  setup() {
    const marks = {
      0: '0km',
      5: '5km',
      10: '10km',
      15: '15km'
    };
    return {
      marks
    }
  },
}
</script>
```

## Range Slider

Range selection can be turned on by setting `range`, at this time `modelValue` is an array.

```vue
<template>
  <a-slider v-model="value" :style="{ width: '300px' }" range />
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref([5, 10]);

    return {
      value
    }

  }
}
</script>
```

## Show Input

When `show-input` is set, the input will be displayed.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-slider :default-value="10" :style="{ width: '300px' }" show-input />
    <a-slider :default-value="[10,20]" :style="{ width: '380px' }" range show-input />
  </a-space>
</template>
```

## Vertical Slider

Set `direction="vertical"` and a vertical slider will be displayed.

```vue
<template>
  <a-space align="start">
    <a-slider
      :default-value="50"
      direction="vertical"
    />

    <a-slider
      direction="vertical"
      :default-value="5"
      :style="{ width: '300px' }"
      :max="15"
      :marks="{
        5: '5km',
        10: '10km',
      }"
    />
  </a-space>
</template>
```

## Custom Tooltip

You can customize the prompt text by setting `format-tooltip`.

```vue
<template>
  <a-slider :min="0" :max="50" :style="{ width: '200px' }" :format-tooltip="formatter" />
</template>

<script>
export default {
  setup() {
    const formatter = (value) => {
      return `${Math.round((value / 50) * 100)}%`
    };

    return {
      formatter
    }
  },
}
</script>
```

## API

### `<slider>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`number \| [number, number]`|`-`||
|default-value|Default value (uncontrolled state)|`number \| [number, number]`|`0`||
|step|Sliding step|`number`|`1`||
|min|Minimum sliding range|`number`|`0`||
|marks|Set the displayed label|`Record<number, string>`|`-`||
|max|Maximum sliding range|`number`|`100`||
|direction|The direction of the slider|`Direction`|`'horizontal'`||
|disabled|Whether to disable|`boolean`|`false`||
|show-ticks|Whether to show ticks|`boolean`|`false`||
|show-input|Whether to show the input|`boolean`|`false`||
|range|Whether to use range selection|`boolean`|`false`||
|show-tooltip|Whether to show tooltip|`boolean`|`true`|2.42.0|
### `<slider>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Trigger when the value changes|value: `number \| [number, number]`|
