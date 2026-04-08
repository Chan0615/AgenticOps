---
name: arco-vue-color-picker
description: "Used for select and display colors. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# ColorPicker

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage

```vue
<template>
  <a-space>
    <a-color-picker  v-model="value" />
    <a-color-picker defaultValue="#165DFF" showText disabledAlpha/>
  </a-space>
</template>

<script setup>
import { ref } from 'vue';
const value = ref('#165DFF')
</script>
```
## Size

ColorPicker defines four sizes (`mini`, `small`, `medium`, `large`), which are 24px, 28px, 32px, and 36px.

```vue
<template>
  <a-space>
    <a-color-picker defaultValue="#165DFF" size="mini" />
    <a-color-picker defaultValue="#165DFF" size="small" />
    <a-color-picker defaultValue="#165DFF" size="medium" />
    <a-color-picker defaultValue="#165DFF" size="large" />
  </a-space>
</template>
```
## Disabled

Set `disabled` to disable the selector.

```vue
<template>
  <a-space>
    <a-color-picker defaultValue="#165DFF" disabled />
    <a-color-picker defaultValue="#165DFF" showText disabled />
  </a-space>
</template>
```
## Color format

Set the format of the color value through `format`, supporting `hex` and `rgb`.

```vue
<template>
  <a-space direction="vertical">
    <a-radio-group type="button" v-model="format">
      <a-radio v-for="item in formatList" :value="item">{{item}}</a-radio>
    </a-radio-group>
    <a-color-picker defaultValue="#165DFF" :format="format" showText />
  </a-space>
</template>

<script setup>
import { ref } from 'vue';

const format = ref('hex')
const formatList = ['hex', 'rgb']
</script>
```
## Preset & History

The preset color and history color areas can be opened through `showPreset` and `showHistory`. Historical colors require users to control the display content themselves.

```vue
<template>
  <a-color-picker
    defaultValue="#165DFF"
    :historyColors="history"
    showHistory
    showPreset
    @popup-visible-change="addHistory"
  />
</template>

<script setup>
import { ref } from 'vue';

const history = ref(['#165DFF'])
const addHistory = (visible, color) => {
  if (!visible) {
    const index = history.value.indexOf(color);
    if (index !== -1) {
      history.value.splice(index, 1);
    }
    history.value.unshift(color);
  }
}
</script>
```
## Trigger

You can set the properties of the trigger through `trigger-props`.

```vue
<template>
  <a-space direction="vertical">
    <a-switch v-model="triggerProps.popupVisible">
      <template #checked> ON </template>
      <template #unchecked>OFF</template>
    </a-switch>
    <a-color-picker defaultValue="#165DFF" :trigger-props="triggerProps" />
  </a-space>
</template>

<script setup>
import { ref } from 'vue';

const triggerProps = ref({
  popupVisible: false,
  unmountOnClose: true,
  renderToBody: false,
  position: 'rt'
})
</script>
```
## Customize trigger element

Customize trigger element.

```vue
<template>
  <a-space>
    <a-color-picker v-model="value" size="mini" >
      <a-tag :color="value">
        <template #icon>
          <icon-bg-colors style="color: #fff" />
        </template>
        {{value}}
      </a-tag>
    </a-color-picker>
  </a-space>
</template>

<script setup>
import { ref } from 'vue';

const value = ref('#165DFF');
</script>
```
## Only Panel

Only use the color selection panel.

```vue
<template>
  <a-space :size="32">
    <a-color-picker defaultValue="#165DFF" hideTrigger showHistory showPreset/>
    <a-color-picker defaultValue="#12D2AC" disabled hideTrigger showPreset/>
  </a-space>
</template>
```

## API

### `<color-picker>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|model-value **(v-model)**|Value|`string`|`-`|
|default-value|Default value (uncontrolled state)|`string`|`-`|
|format|Color value format|`'hex' \| 'rgb'`|`-`|
|size|Size|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`|
|show-text|Show color value|`boolean`|`false`|
|show-history|Show history colors|`boolean`|`false`|
|show-preset|Show preset colors|`boolean`|`false`|
|disabled|disabled|`boolean`|`false`|
|disabled-alpha|Disable transparency channel|`boolean`|`false`|
|hide-trigger|There is no trigger element, only the color panel is displayed|`boolean`|`false`|
|trigger-props|Can accept Props of all [Trigger](../other/trigger.md) components|`Partial<TriggerProps>`|`-`|
|history-colors|Color array of historical colors|`string[]`|`-`|
|preset-colors|Color array of preset colors|`string[]`|`() => colors`|
### `<color-picker>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when the color value changes|value: `string`|
|popup-visible-change|Triggered when the color panel is expanded and collapsed|visible: `boolean`<br>value: `string`|
