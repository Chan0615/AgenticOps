---
name: arco-vue-time-picker
description: "Select the time on the pop-up panel to conveniently complete the time input control. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# TimePicker

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

The basic usage of TimePicker.

```vue
<template>
  <a-time-picker style="width: 194px;" />
</template>
```

## RangePicker

Select time range.

```vue
<template>
  <a-time-picker
    type="time-range"
    @select="(valueString, value) => print('onSelect:', valueString, value)"
    @change="(valueString, value) => print('onChange:', valueString, value)"
    style="width: 252px;" />
</template>
<script>
  export default {
    methods: {
      print(...arg) {
        console.log(...arg);
      }
    }
  }
</script>
```

## Two-way binding

Support `v-model` for two-way data binding.

```vue
<template>
  <a-time-picker
    style="width: 194px"
    v-model="value"
  />
</template>
<script>
  export default {
    data() {
      return {
        value: null
      }
    }
  }
</script>
```

## defaultValue

The default value can be passed through `defaultValue`

```vue
<template>
  <a-time-picker
    defaultValue="18:24:23"
    style="width: 194px; marginRight: 24px; marginBottom: 24px"
  />
  <a-time-picker
    type="time-range"
    :defaultValue="['09:24:53', '18:44:33']"
    style="width: 252px; marginBottom: 24px"
  />
</template>
```

## Size

There are four sizes.

```vue
<template>
  <div style="marginBottom: 20px">
    <a-radio-group v-model="size" type='button'>
      <a-radio value="mini">mini</a-radio>
      <a-radio value="small">small</a-radio>
      <a-radio value="medium">medium</a-radio>
      <a-radio value="large">large</a-radio>
    </a-radio-group>
  </div>
  <a-time-picker style="width: 194px;" :size="size" />
</template>
<script>
  export default {
    data() {
      return {
        size: 'small'
      }
    }
  }
</script>
```

## Disabled

Disabled.

```vue
<template>
  <a-time-picker disabled style="margin: 0 24px 24px 0;" />
  <a-time-picker type="time-range" disabled style="width: 252px; margin: 0 24px 24px 0;" />
</template>
```

## Disable partial time option

By setting `disabledHours` `disabledMinutes` `disabledSeconds`, you can disable some options of hour/minute/second.

```vue
<template>
  <a-time-picker
    style="width: 194px; margin: 0 24px 24px 0;"
    :disabledHours="() => [1, 2, 4, 14]"
    :disabledMinutes="() => [1, 2, 3, 4, 14, 15, 16, 20, 50]"
    :disabledSeconds="() => [1, 2, 3, 4, 5, 6, 7, 10, 14, 60]"
  />
  <a-time-picker
    type="time-range"
    style="width: 252px; margin: 0 24px 24px 0;"
    :disabledHours="() => [1, 2, 4, 14]"
    :disabledMinutes="() => [1, 2, 3, 4, 14, 15, 16, 20, 50]"
    :disabledSeconds="() => [1, 2, 3, 4, 5, 6, 7, 10, 14, 60]"
  />
</template>
```

## Skip confirmation

Skip the confirm step and click directly to select time.

```vue
<template>
  <a-time-picker
    disableConfirm
    style="width: 194px; margin: 0 24px 24px 0;"
  />
  <a-time-picker
    type="time-range"
    disableConfirm
    style="width: 252px; margin: 0 24px 24px 0;"
  />
</template>
```

## Custom format

By setting `format`, you can customize the hour, minute, and second.

```vue
<template>
  <a-time-picker format="HH:mm" :defaultValue="defaultValue" style="width: 130px;" />
</template>
<script>
export default {
  data() {
    return {
      defaultValue: '09:24'
    }
  }
}
</script>
```

## Step

By setting `step`, you can customize the step length of the hour, minute, and second.

```vue
<template>
  <a-time-picker
    defaultValue="10:25:30"
    :step="{
      hour: 2,
      minute: 5,
      second: 10,
    }"
    style="width: 194px;" />
</template>
```

## Extra content

Show extra content.

```vue
<template>
  <a-time-picker style="width: 194px;">
    <template #extra>
      Extra Footer
    </template>
  </a-time-picker>
</template>
```

## 12 hours

By setting `use12Hours`, you can customize the hours, minutes, and seconds.

```vue
<template>
  <a-time-picker
    use12Hours
    defaultValue="12:20:20 AM"
    format="hh:mm:ss A"
    style="width: 194px; margin: 0 24px 24px 0;"
  />
  <a-time-picker
    use12Hours
    defaultValue="09:20:20 pm"
    format="hh:mm:ss a"
    style="width: 194px; margin: 0 24px 24px 0;"
  />
  <a-time-picker
    use12Hours
    defaultValue="2:20 AM"
    format="h:mm A"
    style="width: 194px; margin: 0 24px 24px 0;"
  />
  <a-time-picker
    type="time-range"
    use12Hours
    :defaultValue="['12:20:20 AM', '08:30:30 PM']"
    format="hh:mm:ss A"
    style="width: 300px; margin: 0 24px 24px 0;"
  />
</template>
```

## API

### `<time-picker>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|type|Selector type|`'time' \| 'time-range'`|`'time'`|
|model-value **(v-model)**|Value|`string \| number \| Date \| Array<string \| number \| Date>`|`-`|
|default-value|Default value|`string \| number \| Date \| Array<string \| number \| Date>`|`-`|
|disabled|Whether to disable|`boolean`|`false`|
|allow-clear|Whether to allow clear|`boolean`|`true`|
|readonly|Whether it is read-only mode|`boolean`|`false`|
|error|Whether it is an error state|`boolean`|`false`|
|format|Display the format of the date, refer to [String Parsing Format](#String Parsing Format)|`string`|`'HH:mm:ss'`|
|placeholder|Prompt copy|`string \| string[]`|`-`|
|size|Input box size|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`|
|popup-container|Mount container for pop-up box|`string \| HTMLElement`|`-`|
|use12-hours|12 hour clock|`boolean`|`false`|
|step|Set the hour/minute/second selection interval|`{  hour?: number;  minute?: number;  second?: number;}`|`-`|
|disabled-hours|Disabled partial hour options|`() => number[]`|`-`|
|disabled-minutes|Disabled some minutes options|`(selectedHour?: number) => number[]`|`-`|
|disabled-seconds|Disabled partial seconds option|`(selectedHour?: number, selectedMinute?: number) => number[]`|`-`|
|hide-disabled-options|Hide prohibited options|`boolean`|`false`|
|disable-confirm|Disable the confirmation step, click the time directly after opening, without clicking the confirmation button|`boolean`|`false`|
|position|Pop-up position|`'top' \| 'tl' \| 'tr' \| 'bottom' \| 'bl' \| 'br'`|`'bl'`|
|popup-visible **(v-model)**|Control the pop-up box to open or close|`boolean`|`-`|
|default-popup-visible|The pop-up box is opened or closed by default|`boolean`|`false`|
|trigger-props|You can pass in the parameters of the `Trigger` component|`TriggerProps`|`-`|
|unmount-on-close|Whether to destroy the dom structure after closing|`boolean`|`false`|
### `<time-picker>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|The component value changes|timeString: `string \| Array<string \| undefined> \| undefined`<br>time: `date \| Array<date \| undefined> \| undefined`|
|select|Select time but do not trigger component value change|timeString: `string \| Array<string \| undefined>`<br>time: `Date \| Array<Date \| undefined>`|
|clear|Click the clear button|-|
|popup-visible-change|Pop-up box expand and collapse|visible: `boolean`|
### `<time-picker>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|prefix|Input box prefix|-|2.41.0|
|suffix-icon|Input box suffix icon|-||
|extra|Extra footer|-||

### String parsing format

Format|Output|Description
---|---|---:
`YY`|21|Two-digit year
`YYYY`|2021|Four-digit year
`M`|1-12|Month, starting from 1
`MM`|01-12|Month, two digits
`MMM`|Jan-Dec|Abbreviated month name
`MMMM`|January-December|Full month name
`D`|1-31|Day of the month
`DD`|01-31|Day of the month, two digits
`d`|0-6|Day of the week, Sunday is 0
`dd`|Su-Sa|The shortest name of the day of the week
`ddd`|Sun-Sat|Abbreviated name of the day of the week
`dddd`|Sunday-Saturday|The name of the day of the week
`H`|0-23|Hour
`HH`|00-23|Hour, two digits
`h`|1-12|Hour, 12-hour clock
`hh`|01-12|Hour, 12-hour clock, two digits
`m`|0-59|Minute
`mm`|00-59|Minute, two digits
`s`|0-59|Second
`ss`|00-59|Second, two digits
`S`|0-9|Hundreds of milliseconds, one digits
`SS`|00-99|Tens of milliseconds, two digits
`SSS`|000-999|Millisecond, three digits
`Z`|-5:00|UTC offset
`ZZ`|-0500|UTC offset, add 0 in front of the number
`A`|AM PM|-
`a`|am pm|-
`Do`|1st... 3st|Day of month with serial number
`X`|1410715640.579|Unix timestamp
`x`|1410715640579|Unix millisecond timestamp
