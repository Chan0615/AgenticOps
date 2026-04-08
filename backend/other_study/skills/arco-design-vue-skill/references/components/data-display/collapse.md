---
name: arco-vue-collapse
description: "The content area that can be collapsed/expanded. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Collapse

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Used to group and hide complex content areas, and can be collapsed or expanded. Multiple panels can be expanded by default.

```vue
<template>
  <a-collapse :default-active-key="['1', 2]">
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." :key="2" disabled>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="3">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
  </a-collapse>
</template>
```

## Accordion

Activate the accordion mode with `accordion`, and only one panel can be opened at the same time.

```vue
<template>
  <a-collapse :default-active-key="[1]" accordion>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="2">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="3">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
  </a-collapse>
</template>
```

## Nested panels

Panels are nested at multiple levels.

```vue
<template>
  <a-collapse :default-active-key="['1', 2]" destroy-on-hide>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1">
      <a-collapse :default-active-key="['1.1']" destroy-on-hide>
        <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1.1">
          <div>Beijing Toutiao Technology Co., Ltd.</div>
        </a-collapse-item>
        <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1.2">
          <div>Beijing Toutiao Technology Co., Ltd.</div>
        </a-collapse-item>
      </a-collapse>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." :key="2">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="3">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
  </a-collapse>
</template>
```

## Border less

Hide the border by setting `bordered="false"`.

```vue
<template>
  <a-collapse :default-active-key="['1']" :bordered="false">
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="2" disabled>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="3">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
  </a-collapse>
</template>
```

## Extra slot

The extra node on the far right can be set by `extra`. `extra` click to set `stop` modifier to prevent the current item from expanding.

```vue
<template>
  <a-collapse>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1">
      <template #extra>
        <icon-copy />
      </template>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." :key="2">
      <template #extra>
        <a-button type="primary" size="mini" @click.stop="sayHello">hello</a-button>
      </template>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="3">
      <template #extra>
        <a-tag size="small">city</a-tag>
      </template>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
  </a-collapse>
</template>

<script>
import { Message } from '@arco-design/web-vue';

export default {
  setup() {
    const sayHello = () => {
      Message.info('hello');
    };

    return {
      sayHello,
    };
  },
};
</script>
```

## Custom expand icon

Customize the expand icon for `collapse-item`

```vue
<template>
  <a-collapse :default-active-key="['1', 2]">
    <template #expand-icon="{ active }">
      <icon-face-smile-fill v-if="active"/>
      <icon-face-frown-fill v-else/>
    </template>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1">
      <template #expand-icon="{ active }">
        <icon-double-down v-if="active"/>
        <icon-double-right v-else/>
      </template>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." :key="2">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="3">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
  </a-collapse>
</template>
```

## Custom style

custom panels styles.

```vue
<template>
  <a-collapse :default-active-key="['1', 2]" :bordered="false">
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." :style="customStyle" key="1">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." :style="customStyle" :key="2">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." :style="customStyle" key="3">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
  </a-collapse>
</template>

<script>
export default {
  setup() {
    const customStyle = {
      borderRadius: '6px',
      marginBottom: '18px',
      border: 'none',
      overflow: 'hidden',
    }

    return {
      customStyle
    }
  }
}
</script>
```

## Expand icon position

Set the position of the expanded icon through the `expand-icon-position` property.

```vue
<template>
  <a-space direction="vertical" :style="{ width: '100%' }">
    <a-space>
      <a-radio-group type="button" v-model="position">
        <a-radio value="left">Left</a-radio>
        <a-radio value="right">Right</a-radio>
      </a-radio-group>
      <a-checkbox v-model="hideIcon">Hide Expand Icon</a-checkbox>
    </a-space>
    <a-collapse
      :default-active-key="['1']"
      :expand-icon-position="position"
      :show-expand-icon="!hideIcon"
    >
      <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1">
        <template #expand-icon>
          <icon-plus />
        </template>
        <template #extra>
          <a-tag size="small">city</a-tag>
        </template>
        <div>Beijing Toutiao Technology Co., Ltd.</div>
        <div>Beijing Toutiao Technology Co., Ltd.</div>
        <div>Beijing Toutiao Technology Co., Ltd.</div>
      </a-collapse-item>
      <a-collapse-item
        header="Beijing Toutiao Technology Co., Ltd."
        key="2"
        disabled
      >
        <div>Beijing Toutiao Technology Co., Ltd.</div>
        <div>Beijing Toutiao Technology Co., Ltd.</div>
        <div>Beijing Toutiao Technology Co., Ltd.</div>
      </a-collapse-item>
      <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="3">
        <div>Beijing Toutiao Technology Co., Ltd.</div>
        <div>Beijing Toutiao Technology Co., Ltd.</div>
        <div>Beijing Toutiao Technology Co., Ltd.</div>
      </a-collapse-item>
    </a-collapse>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const position = ref('left');
    const hideIcon = ref(false);

    return {
      position,
      hideIcon,
    };
  },
};
</script>
```

## Destroy On Hide

By setting `destroy-on-hide` the panel contents can be destroyed when hidden.

```vue
<template>
  <a-collapse :default-active-key="['1', 2]" destroy-on-hide>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="1">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." :key="2">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
    <a-collapse-item header="Beijing Toutiao Technology Co., Ltd." key="3" :show-expand-icon="false">
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
      <div>Beijing Toutiao Technology Co., Ltd.</div>
    </a-collapse-item>
  </a-collapse>
</template>
```

## API

### `<collapse>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|active-key **(v-model)**|The `key` of the currently expanded panel|`(string \| number)[]`|`-`||
|default-active-key|The `key` of the panel expanded by default (uncontrolled mode)|`(string \| number)[]`|`[]`||
|accordion|Whether to enable accordion mode|`boolean`|`false`||
|show-expand-icon|Whether to show the expand icon|`boolean`|`-`|2.33.0|
|expand-icon-position|The location where the expand icon is displayed|`'left' \| 'right'`|`'left'`||
|bordered|Whether to show the border|`boolean`|`true`||
|destroy-on-hide|Whether to destroy content when hidden|`boolean`|`false`|2.27.0|
### `<collapse>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Emitted when the expanded panel changes|activeKey: `(string \| number)[]`<br>ev: `Event`|

### `<collapse-item>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|header|The title of the panel|`string`|`-`||
|disabled|Whether to disable|`boolean`|`false`||
|show-expand-icon|Whether to show the expand icon|`boolean`|`true`||
|destroy-on-hide|Whether to destroy content when hidden|`boolean`|`false`|2.27.0|
### `<collapse-item>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|extra|Extra Content|-||
|expand-icon|Expand icon|active: `boolean`<br>disabled: `boolean`<br>position: `'left' \| 'right'`|2.33.0|
|header|The title of the panel|-||

## FAQ

### The `key` attribute of `<CollapseItem>` components is required
In the `<Collapse>` component, each `<CollapseItem>` needs to specify a unique `key` attribute, and the `key` corresponding to the value in `activeKey`.
