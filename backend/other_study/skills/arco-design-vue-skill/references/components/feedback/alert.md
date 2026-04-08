---
name: arco-vue-alert
description: "When warning information is displayed to the user, the warning prompt is used to display the information that needs attention. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Alert

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Display information that needs attention, suitable for brief warning prompts.

```vue
<template>
  <a-alert>This is an info alert.</a-alert>
</template>
```

## Alert Type

There are four types of warnings: `info`, `success`, `warning`, and `error`. Version 2.41.0 adds the `normal` type, which has no icon by default.

```vue
<template>
  <a-row :gutter="[40, 20]">
    <a-col :span="12">
      <a-alert>This is an info alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="success">This is an success alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="warning">This is an warning alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="error">This is an error alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="normal">
        <template #icon>
          <icon-exclamation-circle-fill />
        </template>
        This is an normal alert.
      </a-alert>
    </a-col>
  </a-row>
</template>

<script>
import { IconExclamationCircleFill } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconExclamationCircleFill }
};
</script>
```

## Alert Title

You can add a title to the warning prompt by setting `title`.

```vue
<template>
  <a-row :gutter="[40, 20]">
    <a-col :span="12">
      <a-alert title="Info">This is an info alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert title="Success" type="success">This is an success alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="warning">
        <template #title>
          Warning
        </template>
        This is an warning alert.
      </a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="error">
        <template #title>
          Error
        </template>
        This is an error alert.
      </a-alert>
    </a-col>
  </a-row>
</template>
```

## Closable

By setting `closable`, the close button can be turned on.

```vue
<template>
  <a-row :gutter="[40, 20]">
    <a-col :span="12">
      <a-alert closable>This is an info alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="success" closable>This is an success alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="warning" closable>
        <template #title>
          Warning
        </template>
        This is an warning alert.
      </a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="error" closable>
        <template #title>
          Error
        </template>
        This is an error alert.
      </a-alert>
    </a-col>
  </a-row>
</template>
```

## Custom close element

Specify `close-element` slot, custom close element.

```vue
<template>
  <a-row :gutter="[40, 20]">
    <a-col :span="12">
      <a-alert closable>
        <template #close-element>
          <icon-close-circle />
        </template>
        This is an info alert.
      </a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert closable>
        <template #close-element>
          Close
        </template>
        This is an info alert.
      </a-alert>
    </a-col>
  </a-row>
</template>
```

## Hide Icon

Hide the icon by setting `:show-icon="false"`.

```vue
<template>
  <a-row :gutter="[40, 20]">
    <a-col :span="12">
      <a-alert :show-icon="false">This is an info alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="success" :show-icon="false">This is an success alert.</a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="warning" :show-icon="false">
        <template #title>
          Warning
        </template>
        This is an warning alert.
      </a-alert>
    </a-col>
    <a-col :span="12">
      <a-alert type="error" :show-icon="false">
        <template #title>
          Error
        </template>
        This is an error alert.
      </a-alert>
    </a-col>
  </a-row>
</template>
```

## Action

Customize action buttons via `#action` slot

```vue
<template>
  <a-space direction="vertical" size="large" style="width: 100%;">
    <a-alert closable>
      This is an info alert.
      <template #action>
        <a-button size="small" type="primary">Detail</a-button>
      </template>
    </a-alert>
    <a-alert title="Example" closable>
      This is an info alert.
      <template #action>
        <a-button size="small" type="primary">Detail</a-button>
      </template>
    </a-alert>
  </a-space>
</template>
```

## Top Banner

By setting `banner`, the warning can be used as the top announcement (removal of borders and rounded corners).

```vue
<template>
  <a-alert banner center>This is an info alert.</a-alert>
</template>
```

## API

### `<alert>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|type|Type of the alert. 2.41.0 Added `normal` type|`info \| success \| warning \| error \| normal`|`'info'`|
|show-icon|Whether to show the icon|`boolean`|`true`|
|closable|Whether to show the close button|`boolean`|`false`|
|title|The title of the alert|`string`|`-`|
|banner|Whether to use as the top announcement (remove the border and rounded corners)|`boolean`|`false`|
|center|Whether the content is displayed in the center|`boolean`|`false`|
### `<alert>` Events

|Event Name|Description|Parameters|
|---|---|---|
|close|Triggered when the close button is clicked|ev: `MouseEvent`|
|after-close|Triggered after the close animation ends|-|
### `<alert>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|icon|Icon|-||
|title|Title|-||
|action|Actions|-||
|close-element|Close element|-|2.36.0|
