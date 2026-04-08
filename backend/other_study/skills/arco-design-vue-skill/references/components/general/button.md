---
name: arco-vue-button
description: "Button is a command component that can initiate an instant operation. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Button

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Button is divided into five types: `primary`, `secondary`, `dashed`, `outline`, `text`.

```vue
<template>
  <a-space>
    <a-button type="primary">Primary</a-button>
    <a-button>Secondary</a-button>
    <a-button type="dashed">Dashed</a-button>
    <a-button type="outline">Outline</a-button>
    <a-button type="text">Text</a-button>
  </a-space>
</template>
```

## Icon Button

Buttons can be embedded with icons. When only icons are set, the width and height of the buttons are equal.

```vue
<template>
  <a-space>
    <a-button type="primary">
      <template #icon>
        <icon-plus />
      </template>
    </a-button>
    <a-button type="primary">
      <template #icon>
        <icon-delete />
      </template>
      <!-- Use the default slot to avoid extra spaces -->
      <template #default>Delete</template>
    </a-button>
  </a-space>
</template>

<script>
import { IconPlus, IconDelete } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconPlus, IconDelete }
};
</script>
```

## Button Shape

Button is divided into three shapes: `square` - **rectangular (default)**, `circle` - **circle**, and `round` - **full rounded corner**.

```vue
<template>
  <a-space>
    <a-button type="primary">Square</a-button>
    <a-button type="primary" shape="round">Round</a-button>
    <a-button type="primary">
      <template #icon>
        <icon-plus />
      </template>
    </a-button>
    <a-button type="primary" shape="circle">
      <icon-plus />
    </a-button>
  </a-space>
</template>
<script>
import { IconPlus } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconPlus }
};
</script>
```

## Button Size

Button is divided into four sizes: `mini`, `small`, `medium`, and `large`. The heights are: `24px`, `28px`, `32px`, `36px`. The recommended (default) size is `medium`. The suitable size can be selected in different scenarios and different business needs.

```vue
<template>
  <a-space>
    <a-button type="primary" size="mini">Mini</a-button>
    <a-button type="primary" size="small">Small</a-button>
    <a-button type="primary">Medium</a-button>
    <a-button type="primary" size="large">Large</a-button>
  </a-space>
</template>
```

## Button Status

The state of button is divided into four types: `normal` - **normal (default)**, `success` - **success**, `warning` - **warning**, `danger` - **danger**, Can be used simultaneously with the button type.

```vue
<template>
  <a-space direction="vertical">
    <a-space>
      <a-button type="primary" status="success">Primary</a-button>
      <a-button status="success">Default</a-button>
      <a-button type="dashed" status="success">Dashed</a-button>
      <a-button type="outline" status="success">Outline</a-button>
      <a-button type="text" status="success">Text</a-button>
    </a-space>
    <a-space>
      <a-button type="primary" status="warning">Primary</a-button>
      <a-button status="warning">Default</a-button>
      <a-button type="dashed" status="warning">Dashed</a-button>
      <a-button type="outline" status="warning">Outline</a-button>
      <a-button type="text" status="warning">Text</a-button>
    </a-space>
    <a-space>
      <a-button type="primary" status="danger">Primary</a-button>
      <a-button status="danger">Default</a-button>
      <a-button type="dashed" status="danger">Dashed</a-button>
      <a-button type="outline" status="danger">Outline</a-button>
      <a-button type="text" status="danger">Text</a-button>
    </a-space>
  </a-space>
</template>
```

## Disabled Status

The disabled state of the button.

```vue
<template>
  <a-space direction="vertical">
    <a-space>
      <a-button type="primary" disabled>Primary</a-button>
      <a-button disabled>Default</a-button>
      <a-button type="dashed" disabled>Dashed</a-button>
      <a-button type="outline" disabled>Outline</a-button>
      <a-button type="text" disabled>Text</a-button>
    </a-space>
    <a-space>
      <a-button type="primary" status="success" disabled>Primary</a-button>
      <a-button status="success" disabled>Default</a-button>
      <a-button type="dashed" status="success" disabled>Dashed</a-button>
      <a-button type="outline" status="success" disabled>Outline</a-button>
      <a-button type="text" status="success" disabled>Text</a-button>
    </a-space>
    <a-space>
      <a-button type="primary" status="warning" disabled>Primary</a-button>
      <a-button status="warning" disabled>Default</a-button>
      <a-button type="dashed" status="warning" disabled>Dashed</a-button>
      <a-button type="outline" status="warning" disabled>Outline</a-button>
      <a-button type="text" status="warning" disabled>Text</a-button>
    </a-space>
    <a-space>
      <a-button type="primary" status="danger" disabled>Primary</a-button>
      <a-button status="danger" disabled>Default</a-button>
      <a-button type="dashed" status="danger" disabled>Dashed</a-button>
      <a-button type="outline" status="danger" disabled>Outline</a-button>
      <a-button type="text" status="danger" disabled>Text</a-button>
    </a-space>
  </a-space>
</template>
```

## Loading Status

The button can be in the loading state by setting `loading`. The button in the loading state will not trigger the `click` event.

```vue
<template>
  <a-space>
    <a-button type="primary" loading>Primary</a-button>
    <a-button loading>Default</a-button>
    <a-button type="dashed" loading>Dashed</a-button>
    <a-button type="primary" :loading="loading1" @click="handleClick1">Click Me</a-button>
    <a-button type="primary" :loading="loading2" @click="handleClick2">
      <template #icon>
        <icon-plus />
      </template>
      Click Me
    </a-button>
  </a-space>
</template>

<script>
import { ref } from 'vue';
import { IconPlus } from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconPlus
  },
  setup() {
    const loading1 = ref(false);
    const loading2 = ref(false);

    const handleClick1 = () => {
      loading1.value = !loading1.value
    }
    const handleClick2 = () => {
      loading2.value = !loading2.value
    }

    return {
      loading1,
      loading2,
      handleClick1,
      handleClick2
    }
  }
}
</script>
```

## Long Button

By setting the `long` property, the width of the button follows the width of the container.

```vue
<template>
  <a-space class="wrapper" direction="vertical">
    <a-button type="primary" long>Primary</a-button>
    <a-button long>Default</a-button>
    <a-button type="dashed" long>Dashed</a-button>
    <a-button type="outline" long>Outline</a-button>
    <a-button type="text" long>Text</a-button>
  </a-space>
</template>

<style scoped lang="less">
.wrapper{
  width: 400px;
  padding: 20px;
  border: 1px solid var(~'--color-border');
  border-radius: 4px;
}
</style>
```

## Button Group

Use the `<a-button-group>` component to make the buttons appear as a group. Can be used in multiple operations at the same level.

```vue
<template>
  <a-space direction="vertical">
    <a-button-group>
      <a-button>Publish</a-button>
      <a-button>
        <template #icon>
          <icon-down />
        </template>
      </a-button>
    </a-button-group>
    <a-button-group>
      <a-button>Publish</a-button>
      <a-button>
        <template #icon>
          <icon-more />
        </template>
      </a-button>
    </a-button-group>
    <a-button-group>
      <a-button type="primary">
        <icon-left />
        Prev
      </a-button>
      <a-button type="primary">
        Next
        <icon-right />
      </a-button>
    </a-button-group>
    <a-space size="large">
      <a-button-group type="primary">
        <a-button> copy </a-button>
        <a-button> cut </a-button>
        <a-button> find </a-button>
      </a-button-group>
      <a-button-group type="primary" status="warning">
        <a-button> <template #icon><icon-heart-fill /></template> </a-button>
        <a-button> <template #icon><icon-star-fill /></template> </a-button>
        <a-button> <template #icon><icon-thumb-up-fill /></template> </a-button>
      </a-button-group>
      <a-button-group size="small" disabled>
        <a-button> prev </a-button>
        <a-button> next </a-button>
      </a-button-group>
    </a-space>
  </a-space>
</template>
```

## API

### `<button>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|type|Button types are divided into five types: secondary, primary, dashed, outline and text.|`ButtonTypes`|`'secondary'`|
|shape|Button shape|`BorderShape`|`-`|
|status|Button state|`'normal' \| 'warning' \| 'success' \| 'danger'`|`'normal'`|
|size|Button size|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`|
|long|Whether the width of the button adapts to the container.|`boolean`|`false`|
|loading|Whether the button is in the loading state|`boolean`|`false`|
|disabled|Whether the button is disabled|`boolean`|`false`|
|html-type|Set the native `type` attribute of `button`, optional values refer to [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#attr-type "_blank")|`HTMLButtonElement['type']`|`'button'`|
|autofocus|Set the native `autofocus` attribute of `button`, optional values refer to [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#attr-type "_blank")|`boolean`|`false`|
|href|Set up a jump link. When this property is set, the button is rendered as `<a>`|`string`|`-`|
### `<button>` Events

|Event Name|Description|Parameters|
|---|---|---|
|click|Emitted when the button is clicked|ev: `MouseEvent`|
### `<button>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|icon|Icon|-|

### `<button-group>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|type|Children button types are divided into five types: secondary, primary, dashed, outline and text.|`ButtonTypes`|`-`|
|status|Children button state|`'normal' \| 'warning' \| 'success' \| 'danger'`|`-`|
|shape|Button shape|`BorderShape`|`-`|
|size|Children button size|`'mini' \| 'small' \| 'medium' \| 'large'`|`-`|
|disabled|All children whether the button is disabled|`boolean`|`false`|
