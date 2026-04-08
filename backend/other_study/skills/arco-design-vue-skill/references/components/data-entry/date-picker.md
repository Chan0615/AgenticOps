---
name: arco-vue-date-picker
description: "Choose a date. Support year, month, week, day type, support range selection, etc. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# DatePicker

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

The basic usage of DatePicker.

```vue
<template>
  <a-date-picker style="width: 200px;" />
</template>
```

## MonthPicker

The basic usage of MonthPicker.

```vue
<template>
  <a-month-picker style="width: 200px;" />
</template>
```

## YearPicker

The basic usage of the YearPicker.

```vue
<template>
  <a-year-picker style="width: 200px;" />
</template>
```

## QuarterPicker

The basic usage of QuarterPicker.

```vue
<template>
  <a-quarter-picker style="width: 200px;" />
</template>
```

## WeekPicker

WeekPicker provides a simple way to select weeks. It also allows you to specify the starting day of the week.

```vue
<template>
  <a-week-picker style="width: 200px; margin: 0 24px 24px 0;" />
  <a-week-picker
    style="width: 200px; margin: 0 24px 24px 0;"
    day-start-of-week="1"
  />
</template>
```

## DatePicker showTime

Use `showTime` to select a date with time.

```vue
<template>
  <a-date-picker
    style="width: 220px; margin: 0 24px 24px 0;"
    show-time
    :time-picker-props="{ defaultValue: '09:09:06' }"
    format="YYYY-MM-DD HH:mm:ss"
    @change="onChange"
    @select="onSelect"
    @ok="onOk"
  />
  <a-date-picker
    style="width: 220px; margin: 0 24px 24px 0;"
    show-time
    format="YYYY-MM-DD hh:mm"
    @change="onChange"
    @select="onSelect"
    @ok="onOk"
  />
  <a-range-picker
    style="width: 360px; margin: 0 24px 24px 0;"
    show-time
    :time-picker-props="{ defaultValue: ['00:00:00', '09:09:06'] }"
    format="YYYY-MM-DD HH:mm"
    @change="onChange"
    @select="onSelect"
    @ok="onOk"
  />
</template>
<script>
export default {
  setup() {
    function onSelect(dateString, date) {
      console.log('onSelect', dateString, date);
    }

    function onChange(dateString, date) {
      console.log('onChange: ', dateString, date);
    }

    function onOk(dateString, date) {
      console.log('onOk: ', dateString, date);
    }
    return {
      onSelect,
      onChange,
      onOk,
    };
  }
}
</script>
```

## RangePicker

The basic usage of RangePicker.

```vue
<template>
  <a-range-picker
    @change="onChange"
    @select="onSelect"
    style="width: 254px; marginBottom: 20px;"
  />
  <br />
  <a-range-picker
    mode="week"
    @change="onChange"
    @select="onSelect"
    style="width: 254px; marginBottom: 20px;"
  />
  <br />
  <a-range-picker
    mode="month"
    @change="onChange"
    @select="onSelect"
    style="width: 254px; marginBottom: 20px;"
  />
  <br />
  <a-range-picker
    mode="year"
    @change="onChange"
    @select="onSelect"
    style="width: 254px; marginBottom: 20px;"
  />
  <br />
  <a-range-picker
    mode="quarter"
    @change="onChange"
    @select="onSelect"
    style="width: 254px; marginBottom: 20px;"
  />
  <br />
  <a-range-picker
    showTime
    :time-picker-props="{
    defaultValue:['00:00:00','00:00:00']
    }"
    @change="onChange"
    @select="onSelect"
    style=" width: 380px; "
  />
</template>
<script>
export default {
  setup() {
    return {
      onSelect(dateString, date) {
        console.log('onSelect', dateString, date);
      },
      onChange(dateString, date) {
        console.log('onChange: ', dateString, date);
      },
    };
  },
}
</script>
```

## defaultValue

DatePicker has a default value.

```vue
<template>
  <a-date-picker
    defaultValue="2019-06-03"
    @select="onSelect"
    @change="onChange"
    :style="style"
  />
  <a-date-picker
    defaultValue="2019-06-03"
    :format="(value) => `custom format: ${dayjs(value).format('YYYY-MM-DD')}`"
    @select="onSelect"
    @change="onChange"
    :style="{ ...style, width: '240px' }"
  />
  <a-date-picker
    showTime
    defaultValue="2019-06-03 08:00:00"
    @select="onSelect"
    @change="onChange"
    :style="style"
  />
  <a-year-picker
    defaultValue="2019"
    @select="onSelect"
    @change="onChange"
    :style="style"
  />
  <a-month-picker
    defaultValue="2019-06"
    @select="onSelect"
    @change="onChange"
    :style="style"
  />
  <a-week-picker
    :defaultValue="dayjs('2019-08-02')"
    @select="onSelect"
    @change="onChange"
    :style="style"
  />
  <a-range-picker
    showTime
    :defaultValue="['2019-08-08 00:00:00', '2019-08-18 00:00:00']"
    @select="onSelect"
    @change="onChange"
    :style="{ ...style, width: '360px' }"
  />
  <a-range-picker
    mode="month"
    :defaultValue="['2019-08', '2020-06']"
    @select="onSelect"
    @change="onChange"
    style="width: 300px; marginBottom: 24px;"
  />
</template>
<script>
import dayjs from 'dayjs';

export default {
  setup() {
    return {
      dayjs,
      onSelect(dateString, date) {
        console.log('onSelect', dateString, date);
      },
      onChange(dateString, date) {
        console.log('onChange: ', dateString, date);
      },
      style: { width: '200px', marginBottom: '24px', marginRight: '24px' }
    }
  }
}
</script>
```

## disabled date

Use `disabledDate` to disable specified dates. And use `disabledTime` to disable time, which needs to be used with `showTime`.

```vue
<template>
  <div>
    <a-date-picker
      style="width: 200px; margin-right: 24px; margin-bottom: 24px;"
      :disabledDate="(current) => dayjs(current).isBefore(dayjs())"
    />
    <a-range-picker
      style="width: 360px; margin-right: 24px; margin-bottom: 24px;"
      :disabledDate="(current) => dayjs(current).isBefore(dayjs())"
    />
    <a-date-picker
      style="width: 200px; margin-right: 24px; margin-bottom: 24px;"
      show-time
      :disabledDate="(current) => dayjs(current).isBefore(dayjs())"
      :disabledTime="getDisabledTime"
    />
    <a-range-picker
      style="width: 360px; margin-bottom: 24px;"
      show-time
      :timePickerProps="{hideDisabledOptions: true}"
      :disabledDate="(current) => dayjs(current).isBefore(dayjs())"
      :disabledTime="getDisabledRangeTime"
    />
  </div>
</template>
<script>
import dayjs from 'dayjs';

function range(start, end) {
  const result = [];
  for (let i = start; i < end; i++) {
    result.push(i);
  }
  return result;
}

function getDisabledTime(date) {
  return {
    disabledHours: () => range(6, 24),
    disabledMinutes: () => range(30, 60),
    disabledSeconds: () => range(30, 60),
  };
}

function getDisabledRangeTime(date, type) {
  return {
    disabledHours: () => type === 'start' ? range(0, 6): range(6, 24),
    disabledMinutes: () => type === 'end' ? range(0, 30) : [31, 60],
    disabledSeconds: () => range(30, 60),
  };
}

export default {
  setup() {
    return {
      dayjs,
      getDisabledTime,
      getDisabledRangeTime,
    }
  }
}
</script>
```

## Shortcuts

Use `shortcuts` to preset time for quick selection.

```vue
<template>
  <a-date-picker
    style="width: 300px; margin-bottom: 24px; margin-right: 24px;"
    :shortcuts="[
      {
        label: '2 hours later',
        value: () => dayjs().add(2, 'hour')
      },
      {
        label: 'a week later',
        value: () => dayjs().add(1, 'week'),
      },
      {
        label: 'a month later',
        value: () => dayjs().add(1, 'month'),
      },
    ]"
    show-time
  />
  <a-month-picker
    style="width: 300px; margin-bottom: 24px; margin-right: 24px;"
    :shortcuts="[
      {
        label: 'last month',
        value: () => dayjs().subtract(1, 'month'),
      },
      {
        label: 'six months later',
        value: () => dayjs().add(6, 'month'),
      },
      {
        label: 'two years later',
        value: () => dayjs().add(2, 'year'),
      },
    ]"
  />
  <a-range-picker
    style="width: 400px; margin-bottom: 24px; margin-right: 24px;"
    :shortcuts="[
      {
        label: 'next 7 days',
        value: () => [dayjs(), dayjs().add(1, 'week')],
      },
      {
        label: 'next 30 days',
        value: () => [dayjs(), dayjs().add(1, 'month')],
      },
      {
        label: 'next 365 days',
        value: () => [dayjs(), dayjs().add(1, 'year')],
      },
    ]"
  />
  <a-range-picker
    mode="month"
    style="width: 300px; margin-bottom: 24px;"
    :shortcuts="[
      {
        label: 'next 6 months',
        value: () => [dayjs(), dayjs().add(6, 'month')],
      },
      {
        label: 'next 12 months',
        value: () => [dayjs(), dayjs().add(1, 'year')],
      },
      {
        label: 'next 10 years',
        value: () => [dayjs(), dayjs().add(10, 'year')],
      },
    ]"
  />
</template>
<script>
import dayjs from 'dayjs';
export default {
  setup() {
    return {
      dayjs
    }
  }
}
</script>
```

## Custom shortcuts position

Use `shortcutsPosition` to place the shortcuts to the left, right or bottom.

```vue
<template>
  <a-date-picker
    style="width: 254px; margin-bottom: 20px; margin-right: 24px;"
    shortcuts-position="left"
    :shortcuts="shortcuts"
  />
  <a-range-picker
    style="width: 300px; margin-bottom: 20px;"
    shortcuts-position="left"
    :shortcuts="rangeShortcuts"
  />
  <br />
  <a-date-picker
    style="width: 254px; margin-right: 24px;"
    shortcuts-position="right"
    :shortcuts="shortcuts"
  />
  <a-range-picker
    style="width: 300px;"
    shortcuts-position="right"
    :shortcuts="rangeShortcuts"
  />
</template>
<script>
import dayjs from 'dayjs';
export default {
  setup() {
    return {
      dayjs,
      shortcuts: [
        {
          label: 'yesterday',
          value: () => dayjs().subtract(1, 'day')
        },
        {
          label: 'today',
          value: () => dayjs(),
        },
        {
          label: 'a week later',
          value: () => dayjs().add(1, 'week'),
        },
        {
          label: 'a month later',
          value: () => dayjs().add(1, 'month'),
        },
        {
          label: '2 months later',
          value: () => dayjs().add(2, 'month'),
        }
      ],
      rangeShortcuts: [
        {
          label: 'next 2 days',
          value: () => [dayjs(), dayjs().add(2, 'day')],
        },
        {
          label: 'next 7 days',
          value: () => [dayjs(), dayjs().add(1, 'week')],
        },
        {
          label: 'next 30 days',
          value: () => [dayjs(), dayjs().add(1, 'month')],
        },
        {
          label: 'next 6 months',
          value: () => [dayjs(), dayjs().add(6, 'month')],
        },
        {
          label: 'next 12 months',
          value: () => [dayjs(), dayjs().add(1, 'year')],
        },
        {
          label: 'next 10 years',
          value: () => [dayjs(), dayjs().add(10, 'year')],
        }
      ]
    }
  }
}
</script>
```

## Dynamic control range

According to the selected value to control the selected range, use `onSelect` and `disabledDate`.

```vue
<template>
  <a-range-picker
      style="width: 300px;"
      @select="onSelect"
      @popupVisibleChange="onPopupVisibleChange"
      :disabledDate="disabledDate"
    />
</template>
<script>
export default {
  data() {
    return {
      dates: [],
    }
  },
  methods: {
    onSelect(valueString, value) {
      this.dates = value;
    },
    onPopupVisibleChange(visible) {
      if (!visible) {
        this.dates = []
      }
    },
    disabledDate(current) {
      const dates = this.dates;
      if (dates && dates.length) {
        const tooLate = dates[0] && Math.abs((new Date(current) - dates[0]) / (24 * 60 * 60 * 1000)) > 7;
        const tooEarly = dates[1] && Math.abs((new Date(current) - dates[1]) / (24 * 60 * 60 * 1000)) > 7;
        return tooEarly || tooLate;
      }
      return false;
    }
  }
}
</script>
```

## Size

Setting `size` can use four sizes (`mini` `small` `medium` `large`). The height corresponds to 24px, 28px, 32px, 36px.

```vue
<template>
  <div style="margin-bottom: 20px;">
    <a-radio-group v-model="size" type='button'>
      <a-radio value="mini">mini</a-radio>
      <a-radio value="small">small</a-radio>
      <a-radio value="medium">medium</a-radio>
      <a-radio value="large">large</a-radio>
    </a-radio-group>
  </div>
  <a-date-picker
    :size="size"
    style="width: 254px;"
  />
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

## Extra footer

Add an extra footer to meet the needs of some customized information.

```vue
<template>
  <a-date-picker style="width: 200px; margin-bottom: 20px">
    <template #extra>Extra footer</template>
  </a-date-picker>
  <br />
  <a-range-picker showTime style="width: 360px;">
    <template #extra>Extra footer</template>
  </a-range-picker>
</template>
```

## Disabled

Disabled.

```vue
<template>
  <a-date-picker
    defaultValue="2020-08-08"
    disabled
    style="width: 200px; margin-bottom: 20px;"
  />
  <br />
  <a-range-picker
    :defaultValue="['2020-08-08', '2020-08-18']"
    disabled
    style="width: 300px; margin-bottom: 20px;"
  />
  <br />
  <a-range-picker
    :defaultValue="['2020-08-08']"
    :disabled="[true, false]"
    :disabledDate="(current) => dayjs(current).isBefore(dayjs('2020-08-08'))"
    style="width: 300px; margin-bottom: 20px;"
  />
  <br />
  <a-range-picker
    showTime
    :defaultValue="['2020-08-08 02:02:02']"
    :disabled="[true, false]"
    style="width: 380px;"
  />
</template>
<script>
import dayjs from 'dayjs';
export default {
  setup() {
    return {
      dayjs
    };
  }
}
</script>
```

## Customize cell

Use the named slot `cell` to customize the date cell.

```vue
<template>
  <a-date-picker>
    <template #cell="{ date }">
      <div class="arco-picker-date">
        <div class="arco-picker-date-value" :style="getCellStyle(date)">
          {{ date.getDate() }}
        </div>
      </div>
    </template>
  </a-date-picker>
</template>
<script>
export default {
  setup() {
    const highlightDates = [6, 14, 22];
    const highlightStyle = {
      border: '1px solid rgb(var(--arcoblue-6))',
    };
    return {
      getCellStyle(date) {
        return highlightDates.includes(date.getDate()) ? highlightStyle : {}
      }
    }
  }
}
</script>
```

## Two-way binding

Support two-way binding through `v-model`

```vue
<template>
  <a-space>
    <a-date-picker v-model="value" style="width: 200px;" />
    <a-range-picker v-model="rangeValue" style="width: 300px;" />
  </a-space>
</template>
<script>
export default {
  data() {
    return {
      value: Date.now(),
      rangeValue: [Date.now(), Date.now()],
    }
  }
}
</script>
```

## Customize trigger element

Customize trigger element.

```vue
<template>
  <a-space>
    <a-date-picker
      style="width: 268px;"
      v-model="value"
    >
      <a-button>{{ value || 'Please select a date' }}</a-button>
    </a-date-picker>
    <a-range-picker
      style="width: 268px;"
      v-model="rangeValue"
    >
      <a-button>{{ rangeValue && rangeValue.join(' - ') || 'Please select a date range' }}</a-button>
    </a-range-picker>
  </a-space>
</template>
<script>
import { ref } from 'vue';
export default {
  setup() {
    const value = ref();
    const rangeValue = ref();
    return {
      value,
      rangeValue,
    }
  }
}
</script>
```

## Panel Only

Only use panel, hide input selection.

```vue
<template>
  <div>
    <a-date-picker
      default-value="2019-06-03"
      v-model:pickerValue="pickerValue"
      hide-trigger
      style="width: 268px;"
    />
    <a-range-picker
      :default-value="['2019-08-01', '2020-06-01']"
      v-model:pickerValue="rangePickerValue"
      hide-trigger
      style="width: 560px; margin-top: 20px;"
    />
  </div>
</template>
<script>
export default {
  data() {
    return {
      pickerValue: null,
      rangePickerValue: null,
    };
  }
};
</script>
```

## API

### `Common` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|locale|Internationalization configuration, used to cover the locale file in the `datePicker` field|`Record<string, any>`|`-`||
|hide-trigger|There is no trigger element, only the selection panel is displayed|`boolean`|`false`||
|allow-clear|Whether to allow clear|`boolean`|`true`||
|readonly|Whether it is read-only|`boolean`|`false`||
|error|Whether it is an error state|`boolean`|`false`||
|size|The size of the date picker|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|shortcuts|Quick selection of preset time range|`ShortcutType[]`|`[]`||
|shortcuts-position|The position of the preset range on the panel, which is placed at the bottom by default, and the side is generally used for scenes with a large number of preset times|`'left' \| 'bottom' \| 'right'`|`'bottom'`||
|position|The position of the pop-up box|`'top' \| 'tl' \| 'tr' \| 'bottom' \| 'bl' \| 'br'`|`'bl'`||
|popup-visible|Control the open or closed state of the pop-up box|`boolean`|`-`||
|default-popup-visible|The default pop-up box is open or closed|`boolean`|`false`||
|trigger-props|You can pass in the parameters of the `Trigger` component|`TriggerProps`|`-`||
|unmount-on-close|Whether to destroy the DOM structure when hiding|`boolean`|`false`||
|placeholder|Prompt copy|`string`|`-`||
|disabled|Whether to disable|`boolean`|`false`||
|disabled-date|Unselectable date|`(current?: Date) => boolean`|`-`||
|disabled-time|Unselectable time|`(current: Date) => DisabledTimeProps`|`-`||
|picker-value **(v-model)**|Date displayed on the panel|`Date \| string \| number`|`-`||
|default-picker-value|The date displayed on the panel by default|`Date \| string \| number`|`-`||
|popup-container|Mount container for pop-up box|`string \| HTMLElement`|`-`||
|value-format|The format of the value, valid for `value` `defaultValue` `pickerValue` `defaultPickerValue` and the return value in the event, supports setting as timestamp, Date and string (refer to [String parsing format](#string-parsing-format) ). If not specified, it will be formatted as a string, in the same format as `format`.|`'timestamp' \| 'Date' \| string`|`-`|2.16.0|
|preview-shortcut|Whether to preview the result of the shortcut|`boolean`|`true`|2.28.0|
|show-confirm-btn|Whether to show the confirm button, always show when `showTime = true`.|`boolean`|`false`|2.29.0|
|disabled-input|Whether input is disabled with the keyboard.|`boolean`|`false`|2.43.0|
|abbreviation|Whether to enable abbreviation|`boolean`|`true`|2.45.0|
### `Common` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|The component value changes|value: `Date \| string \| number \| undefined`<br>date: `Date \| undefined`<br>dateString: `string \| undefined`|
|select|The selected date has changed but the component value has not changed|value: `Date \| string \| number`<br>date: `Date`<br>dateString: `string`|
|popup-visible-change|Open or close the pop-up box|visible: `boolean`|
|ok|Click the confirm button|value: `Date \| string \| number`<br>date: `Date`<br>dateString: `string`|
|clear|Click the clear button|-|
|select-shortcut|Click on the shortcut option|shortcut: `ShortcutType`|
|picker-value-change|Panel date change|value: `Date \| string \| number`<br>date: `Date`<br>dateString: `string`|
### `Common` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|prefix|Input box prefix|-|2.41.0|
|suffix-icon|Input box suffix icon|-||
|icon-next-double|Double arrow page backward icon|-||
|icon-prev-double|Double arrow page forward icon|-||
|icon-next|Single arrow page backward icon|-||
|icon-prev|Single arrow page forward icon|-||
|cell|Customize the contents of the date cell|date: `Date`||
|extra|Extra footer|-||

### `<date-picker>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`Date \| string \| number`|`-`||
|default-value|Default value|`Date \| string \| number`|`-`||
|format|Display the format of the date, refer to [String Parsing Format](#string-parsing-format)|`string \| ((current: Date) => string)`|`-`||
|day-start-of-week|The first day of the week starts on the day of the week, 0-Sunday, 1-Monday, and so on.|`0 \| 1 \| 2 \| 3 \| 4 \| 5 \| 6`|`0`|2-6 from 2.21.0|
|show-time|Whether to increase time selection|`boolean`|`false`||
|time-picker-props|Time display parameters, refer to [TimePickerProps](time-picker.md)|`Partial<TimePickerProps>`|`-`||
|disabled|Whether to disable|`boolean`|`false`||
|disabled-date|Unselectable date|`(current?: Date) => boolean`|`-`||
|disabled-time|Unselectable time|`(current: Date) => DisabledTimeProps`|`-`||
|show-now-btn|Whether to display `showTime`, select the button of the current time|`boolean`|`true`||

### `<month-picker>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|model-value **(v-model)**|Value|`Date \| string \| number`|`-`|
|default-value|Default value|`Date \| string \| number`|`-`|
|format|Display the format of the date, refer to [String Parsing Format](#String Parsing Format)|`string`|`'YYYY-MM'`|

### `<year-picker>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|model-value **(v-model)**|Value|`Date \| string \| number`|`-`|
|default-value|Default value|`Date \| string \| number`|`-`|
|format|Display the format of the date, refer to [String Parsing Format](#String Parsing Format)|`string`|`'YYYY'`|

### `<quarter-picker>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`Date \| string \| number`|`-`||
|default-value|Default value|`Date \| string \| number`|`-`||
|format|Display the format of the date, refer to [String Parsing Format](#String Parsing Format)|`string`|`'YYYY-[Q]Q'`||
|value-format|The format of the value, valid for `value` `defaultValue` `pickerValue` `defaultPickerValue` and the return value in the event, supports setting as timestamp, Date and string (refer to [String parsing format](#string-parsing-format) ).|`string`|`'YYYY-MM'`|2.16.0|

### `<week-picker>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`Date \| string \| number`|`-`||
|default-value|Default value|`Date \| string \| number`|`-`||
|format|Display the format of the date, refer to [String Parsing Format](#String Parsing Format)|`string`|`'gggg-wo'`||
|value-format|The format of the value, valid for `value` `defaultValue` `pickerValue` `defaultPickerValue` and the return value in the event, supports setting as timestamp, Date and string (refer to [String parsing format](#string-parsing-format) ).|`string`|`'YYYY-MM-DD'`|2.16.0|
|day-start-of-week|The first day of the week starts on the day of the week, 0-Sunday, 1-Monday, and so on.|`0 \| 1 \| 2 \| 3 \| 4 \| 5 \| 6`|`0`|2-6 from 2.21.0|

### `<range-picker>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|mode|Type of range selector|`'date' \| 'year' \| 'quarter' \| 'month' \| 'week'`|`'date'`||
|model-value **(v-model)**|Value|`(Date \| string \| number)[]`|`-`||
|default-value|Default value|`(Date \| string \| number)[]`|`-`||
|picker-value|The date displayed in the default panel|`(Date \| string \| number)[]`|`-`||
|default-picker-value|Date displayed on the panel|`(Date \| string \| number)[]`|`-`||
|disabled|Whether to disable|`boolean \| boolean[]`|`false`||
|day-start-of-week|The first day of the week starts on the day of the week, 0-Sunday, 1-Monday, and so on.|`0 \| 1 \| 2 \| 3 \| 4 \| 5 \| 6`|`0`|2-6 from 2.21.0|
|format|Display the format of the date, refer to [String Parsing Format](#string-parsing-format)|`string`|`-`||
|value-format|The format of the value, valid for `value` `defaultValue` `pickerValue` `defaultPickerValue` and the return value in the event, supports setting as timestamp, Date and string (refer to [String parsing format](#string-parsing-format) ). If not specified, it will be formatted as a string, in the same format as `format`.|`'timestamp' \| 'Date' \| string`|`-`|2.16.0|
|show-time|Whether to increase time selection|`boolean`|`false`||
|time-picker-props|Time display parameters, refer to [TimePickerProps](time-picker.md)|`Partial<TimePickerProps>`|`-`||
|placeholder|Prompt copy|`string[]`|`-`||
|disabled-date|Non-selectable date|`(current: Date, type: 'start' \| 'end') => boolean`|`-`||
|disabled-time|Unselectable time|`(current: Date, type: 'start' \| 'end') => DisabledTimeProps`|`-`||
|separator|The segmentation symbol in the input box of the range selector|`string`|`-`||
|exchange-time|Whether the time will be exchanged, by default time will affect and participate in the ordering of start and end values, if you want to fix the time order, you can turn it off.|`boolean`|`true`|2.25.0|
|disabled-input|Whether input is disabled with the keyboard.|`boolean`|`false`|2.43.0|
|abbreviation|Whether to enable abbreviation|`boolean`|`true`||
### `<range-picker>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|The component value changes|value: `(Date \| string \| number \| undefined)[] \| undefined`<br>date: `(Date \| undefined)[] \| undefined`<br>dateString: `(string \| undefined)[] \| undefined`|
|select|The selected date has changed but the component value has not changed|value: `(Date \| string \| number \| undefined)[]`<br>date: `(Date \| undefined)[]`<br>dateString: `(string \| undefined)[]`|
|popup-visible-change|Open or close the pop-up box|visible: `boolean`|
|ok|Click the confirm button|value: `Date \| string \| number[]`<br>date: `Date[]`<br>dateString: `string[]`|
|clear|Click the clear button|-|
|select-shortcut|Click on the shortcut option|shortcut: `ShortcutType`|
|picker-value-change|Panel date change|value: `Date \| string \| number[]`<br>date: `Date[]`<br>dateString: `string[]`|

### ShortcutType

|Name|Description|Type|Default|
|---|---|---|:---:|
|label|the content of shortcut|`string \| number \| (() => VNode)`|`-`|
|value|the value of shortcut|`(Date \| string \| number)    \| (Date \| string \| number)[]    \| (() => (Date \| string \| number) \| (Date \| string \| number)[])`|`-`|
|format|the format use to parse value, refer to [String Parsing Format](#string-parsing-format)|`string`|`-`|

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

## FAQ

### About the `locale` field
The `locale` field can be configured using the language pack provided by the component library.
