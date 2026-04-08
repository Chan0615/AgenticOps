---
name: arco-vue-switch
description: "Mutually exclusive operation controls, users can turn on or turn off a certain function. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Switch

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of switch.

```vue
<template>
  <a-switch />
</template>
```

## Switch Type

There are three types of switches: `circle`, `round` and `line`.

```vue
<template>
  <a-space size="large">
    <a-switch />
    <a-switch type="round"/>
    <a-switch type="line"/>
  </a-space>
</template>
```

## Switch Size

The switch is divided into two sizes, `small` and `medium`.

```vue
<template>
  <a-space size="large">
    <a-switch />
    <a-switch size="small"/>
  </a-space>
</template>
```

## Disabled

Disable the switch.

```vue
<template>
  <a-space size="large">
    <a-switch disabled/>
    <a-switch :default-checked="true" disabled/>
    <a-switch type="round" disabled/>
    <a-switch :default-checked="true" type="round" disabled/>
    <a-switch type="line" disabled/>
    <a-switch :default-checked="true" type="line" disabled/>
  </a-space>
</template>
```

## Button Color

The color of the switch can be customized through `checked-color` and `unchecked-color`.

```vue
<template>
  <a-switch checked-color="#F53F3F" unchecked-color="#14C9C9" />
</template>
```

## Custom Value

The value of the switch can be customized through `checked-value` and `unchecked-value`.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-switch v-model="value" checked-value="yes" unchecked-value="no" />
    <div>Current Value: {{ value }}</div>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref('');

    return {
      value
    }
  },
}
</script>
```

## Switch intercept

Set the `beforeChange` function, and the return value of the function will be used to determine whether to block the switch.

```vue
<template>
  <a-space size="large">
    <a-switch :beforeChange="handleChangeIntercept"/>
    <a-switch type="round" :beforeChange="handleChangeIntercept2"/>
    <a-switch type="line" :beforeChange="handleChangeIntercept3"/>
  </a-space>
</template>

<script>
import { Message } from '@arco-design/web-vue';

export default {
  setup() {
    const handleChangeIntercept = async (newValue) => {
      await new Promise((resolve) => setTimeout(resolve, 1000))
      return true
    }

    const handleChangeIntercept2 = async (newValue) => {
      await new Promise((resolve) => setTimeout(resolve, 500))
      if (!newValue) {
        Message.error("OH, You can't change")
        return false
      }
      return true
    }

    const handleChangeIntercept3 = async (newValue) => {
      await new Promise((_, reject) => setTimeout(() => {
        Message.error("OH, Something went wrong")
        reject()
      }, 1000))
      return true
    }

    return {
      handleChangeIntercept,
      handleChangeIntercept2,
      handleChangeIntercept3
    }
  }
}
</script>
```

## Loading

The switch is in the loading state by setting `loading`, and the switch cannot be clicked at this time.

```vue
<template>
  <a-space size="large">
    <a-switch loading />
    <a-switch type="round" loading />
    <a-switch type="line" loading />
  </a-space>
</template>
```

## Custom Text

Customize the text of the on/off state of the switch.

```vue
<template>
  <a-space size="large">
    <a-switch>
      <template #checked>
        ON
      </template>
      <template #unchecked>
        OFF
      </template>
    </a-switch>
    <a-switch type="round">
      <template #checked>
        ON
      </template>
      <template #unchecked>
        OFF
      </template>
    </a-switch>
  </a-space>
</template>
```

## Custom Icon

Customize the icon displayed on the switch button.

```vue
<template>
  <a-space size="large">
    <a-switch>
      <template #checked-icon>
        <icon-check/>
      </template>
      <template #unchecked-icon>
        <icon-close/>
      </template>
    </a-switch>
    <a-switch type="round">
      <template #checked-icon>
        <icon-check/>
      </template>
      <template #unchecked-icon>
        <icon-close/>
      </template>
    </a-switch>
    <a-switch type="line">
      <template #checked-icon>
        <icon-check/>
      </template>
      <template #unchecked-icon>
        <icon-close/>
      </template>
    </a-switch>
  </a-space>
</template>
```

## API

### `<switch>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`string\|number\|boolean`|`-`||
|default-checked|Default selected state (uncontrolled state)|`boolean`|`false`||
|disabled|Whether to disable|`boolean`|`false`||
|loading|Whether it is loading state|`boolean`|`false`||
|type|Type of switch|`'circle' \| 'round' \| 'line'`|`'circle'`||
|size|Size of switch|`'small' \| 'medium'`|`'medium'`||
|checked-value|Value when checked|`string\|number\|boolean`|`true`|2.12.0|
|unchecked-value|Value when unchecked|`string\|number\|boolean`|`false`|2.12.0|
|checked-color|The color of the switch when checked|`string`|`-`|2.12.0|
|unchecked-color|The color of the switch when unchecked|`string`|`-`|2.12.0|
|before-change|before-change hook before the switch state changes. If false is returned or a Promise is returned and then is rejected, will stop switching|`(  newValue: string \| number \| boolean) => Promise<boolean \| void> \| boolean \| void`|`-`|2.37.0|
|checked-text|Copywriting when opened (not effective when `type='line'` and `size='small'`)|`string`|`-`|2.45.0|
|unchecked-text|Copywriting when closed (not effective when `type='line'` and `size='small'`)|`string`|`-`|2.45.0|
### `<switch>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Trigger when the value changes|value: ` boolean \| string \| number `<br>ev: `Event`|
|focus|Triggered when the component gets focus|ev: `FocusEvent`|
|blur|Fired when the component loses focus|ev: `FocusEvent`|
### `<switch>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|checked-icon|The icon on the button when opened|-|
|unchecked-icon|The icon on the button when closed|-|
|checked|Copywriting when opened (not effective when `type='line'` and `size='small'`)|-|
|unchecked|Copywriting when closed (not effective when `type='line'` and `size='small'`)|-|
