---
name: arco-vue-input-number
description: "Only input boxes in numeric format are allowed. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# InputNumber

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Use the mouse or keyboard to enter the standard value within the range.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-number v-model="value" :style="{width:'320px'}" placeholder="Please Enter" class="input-demo" :min="10" :max="100"/>
    <a-input-number :style="{width:'320px'}" placeholder="Please Enter" class="input-demo" :min="10" :max="100"/>
    <a-input-number :style="{width:'320px'}" placeholder="Please Enter" :default-value="500" class="input-demo" disabled/>
  </a-space>
</template>

<script>
export default {
  data(){
    return {
      value:15
    }

  }
}
</script>
```

## Button Mode

Specify `mode` as `button` to use a numeric input box with buttons.

```vue
<template>
  <a-input-number :style="{width:'320px'}" placeholder="Please Enter" :default-value="500" mode="button" class="input-demo" />
</template>
```

## Size

Setting `size` can use four sizes (`mini`, `small`, `medium`, `large`) number input box. The corresponding heights are `24px`, `28px`, `32px`, and `36px` respectively.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-number :style="{width:'320px'}" placeholder="Please Enter" size="large" class="input-demo" />
    <a-input-number :style="{width:'320px'}" placeholder="Please Enter" mode="button" size="large" class="input-demo" />
  </a-space>
</template>
```

## Precision & Step

Use `precision` to set the number precision. When `precision` is less than the decimal place of `step`, the precision is taken as the number of decimal places of `step`.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-number :style="{width:'320px'}" placeholder="Please Enter" :default-value="3.6" :step="1.2" :precision="2" class="input-demo" />
    <a-input-number :style="{width:'320px'}" placeholder="Please Enter" :default-value="1.22" :step="1.22" :precision="1" class="input-demo" />
  </a-space>
</template>
```

## Prefix & Suffix

Add prefix and suffix in the input box by specifying the `prefix` and `suffix` slots.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-number :style="{width:'320px'}" placeholder="Please enter something" allow-clear>
      <template #prefix>
        <icon-user />
      </template>
    </a-input-number>
    <a-input-number :style="{width:'320px'}" placeholder="Please enter something" allow-clear hide-button>
      <template #suffix>
        <icon-info-circle />
      </template>
    </a-input-number>
  </a-space>
</template>
```

## Step Icon

To Add the icons for the increment and decrement operations by specifying the `plus` and `minus` slots.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-input-number :style="{width:'320px'}" placeholder="Please enter something" allow-clear>
       <template #plus>
        <icon-plus />
      </template>
      <template #minus>
        <icon-minus />
      </template>
    </a-input-number>
  </a-space>
</template>
```

## Format

Use `formatter` and `parser` together to define the display value of the input box.

```vue
<template>
  <a-input-number :style="{width:'320px'}" placeholder="Please Enter" class="input-demo" :default-value="12000" :min="0" :formatter="formatter" :parser="parser"/>
</template>

<script>
export default {
  setup(){
    const formatter = (value) => {
      const values = value.split('.');
      values[0]=values[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');

      return values.join('.')
    };

    const parser = (value) => {
      return value.replace(/,/g, '')
    };

    return {
      formatter,
      parser
    }
  },
}
</script>
```

## Trigger event of v-model

By default, the number input box will modify the bound value when blur or press Enter. By setting the attribute model-event="input", the component can modify the bound value during input.
Note: In this mode, the input value will exceed the set min/max, and the component will correct the value when it is out of focus.

```vue
<template>
  <a-input-number v-model="value" :style="{width:'320px'}" placeholder="Please Enter" class="input-demo" :min="10" :max="100" model-event="input"/>
  <div>value: {{value}}</div>
</template>

<script>
export default {
  data(){
    return {
      value:15
    }

  }
}
</script>
```

## API

### `<input-number>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`number`|`-`||
|default-value|Default value (uncontrolled mode)|`number`|`-`||
|mode|Mode (`embed`: button embedded mode, `button`: left and right button mode)|`'embed' \| 'button'`|`'embed'`||
|precision|Precision|`number`|`-`||
|step|Number change step|`number`|`1`||
|disabled|Whether to disable|`boolean`|`false`||
|error|Whether it is an error state|`boolean`|`false`||
|max|Max|`number`|`Infinity`||
|min|Min|`number`|`-Infinity`||
|formatter|Define the display value of the input|`func`|`-`||
|parser|Convert from `formatter` to number, and use with `formatter`|`func`|`-`||
|placeholder|Input prompt text|`string`|`-`||
|hide-button|Whether to hide the button|`boolean`|`false`||
|size|Input size|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|allow-clear|Whether to allow the input to be cleared|`boolean`|`false`||
|model-event|Trigger event for `v-model`|`'change' \| 'input'`|`'change'`||
|read-only|Readonly|`boolean`|`false`|2.33.1|
|input-attrs|Attributes of inner input elements|`object`|`-`|2.52.0|
### `<input-number>` Events

|Event Name|Description|Parameters|version|
|---|---|---|:---|
|change|Triggered when the value changes|value: ` number \| undefined `<br>ev: `Event`||
|focus|Triggered when the input gets focus|ev: `FocusEvent`||
|blur|Triggered when the input box loses focus|ev: `FocusEvent`||
|clear|Triggered when the user clicks the clear button|ev: `Event`|2.23.0|
|input|Triggered on input|value: ` number \| undefined `<br>inputValue: `string`<br>ev: `Event`|2.27.0|
|keydown|Triggered on keydown|ev: `MouseEvent`|2.56.0|
### `<input-number>` Methods

|Method|Description|Parameters|Return|
|---|---|---|:---:|
|focus|Make the input box focus|-|-|
|blur|Make the input box lose focus|-|-|
### `<input-number>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|minus|Minus|-|
|plus|Plus|-|
|append|Append|-|
|prepend|Prepend|-|
|suffix|Suffix|-|
|prefix|Prefix|-|
