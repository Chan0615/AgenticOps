---
name: arco-vue-tabs
description: "Organize content in the same view. You can view the content of one view at a time, and you can switch tabs to view other content. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Tabs

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of tab.

```vue
<template>
  <a-tabs default-active-key="2">
    <a-tab-pane key="1" title="Tab 1">
      Content of Tab Panel 1
    </a-tab-pane>
    <a-tab-pane key="2" title="Tab 2">
      Content of Tab Panel 2
    </a-tab-pane>
    <a-tab-pane key="3">
      <template #title>Tab 3</template>
      Content of Tab Panel 3
    </a-tab-pane>
  </a-tabs>
</template>
```

## Icon Tab

Tab page with icons.

```vue
<template>
  <a-tabs>
    <a-tab-pane key="1">
      <template #title>
        <icon-calendar/> Tab 1
      </template>
      Content of Tab Panel 1
    </a-tab-pane>
    <a-tab-pane key="2">
      <template #title>
        <icon-clock-circle/> Tab 2
      </template>
      Content of Tab Panel 2
    </a-tab-pane>
    <a-tab-pane key="3">
      <template #title>
        <icon-user/> Tab 3
      </template>
      Content of Tab Panel 3
    </a-tab-pane>
  </a-tabs>
</template>
```

## Position

The position of the tab bar can be customized through the `position` property.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-radio-group v-model="position" type="button">
      <a-radio value="top">Top</a-radio>
      <a-radio value="right">Right</a-radio>
      <a-radio value="bottom">Bottom</a-radio>
      <a-radio value="left">Left</a-radio>
    </a-radio-group>
    <a-tabs :position="position">
      <a-tab-pane key="1" title="Tab 1">
        Content of Tab Panel 1
      </a-tab-pane>
      <a-tab-pane key="2" title="Tab 2">
        Content of Tab Panel 2
      </a-tab-pane>
      <a-tab-pane key="3" title="Tab 3">
        Content of Tab Panel 3
      </a-tab-pane>
    </a-tabs>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const position = ref('top');

    return {
      position
    }
  },
}
</script>
```

## Types

The type of label can be set by `type`.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-radio-group v-model="type" type="button">
      <a-radio value="line">Line</a-radio>
      <a-radio value="card">Card</a-radio>
      <a-radio value="card-gutter">Card Gutter</a-radio>
      <a-radio value="text">Text</a-radio>
      <a-radio value="rounded">Rounded</a-radio>
      <a-radio value="capsule">Capsule</a-radio>
    </a-radio-group>
    <a-radio-group v-model="size" type="button">
      <a-radio value="mini">Mini</a-radio>
      <a-radio value="small">Small</a-radio>
      <a-radio value="medium">Medium</a-radio>
      <a-radio value="large">Large</a-radio>
    </a-radio-group>
    <a-tabs :type="type" :size="size">
      <a-tab-pane key="1" title="Tab 1">
        Content of Tab Panel 1
      </a-tab-pane>
      <a-tab-pane key="2" title="Tab 2">
        Content of Tab Panel 2
      </a-tab-pane>
      <a-tab-pane key="3" title="Tab 3">
        Content of Tab Panel 3
      </a-tab-pane>
    </a-tabs>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const type = ref('line');
    const size = ref('medium');

    return {
      type,
      size
    }
  },
}
</script>
```

## Lazy load

By setting the lazy-load property, the panel can be rendered when it is first activated.

```vue
<template>
  <a-tabs default-active-key="2" lazy-load>
    <a-tab-pane key="1" title="Tab 1">
      Content of Tab Panel 1
    </a-tab-pane>
    <a-tab-pane key="2" title="Tab 2">
      Content of Tab Panel 2
    </a-tab-pane>
    <a-tab-pane key="3" title="Tab 3">
      Content of Tab Panel 3
    </a-tab-pane>
  </a-tabs>
</template>
```

## Extra

The extra display content can be customized through the `extra` slot.

```vue
<template>
  <a-tabs>
    <template #extra>
      <a-button>Action</a-button>
    </template>
    <a-tab-pane key="1" title="Tab 1">
      Content of Tab Panel 1
    </a-tab-pane>
    <a-tab-pane key="2" title="Tab 2">
      Content of Tab Panel 2
    </a-tab-pane>
    <a-tab-pane key="3" title="Tab 3">
      Content of Tab Panel 3
    </a-tab-pane>
  </a-tabs>
</template>
```

## Editable

By setting `:editable="true"`, you can turn on the dynamic increase and decrease tabs. Only works with `line` | `card` | `card-gutter`

```vue

<template>
  <a-tabs type="card-gutter" :editable="true" @add="handleAdd" @delete="handleDelete" show-add-button auto-switch>
    <a-tab-pane v-for="(item, index) of data" :key="item.key" :title="item.title" :closable="index!==2">
      {{ item?.content }}
    </a-tab-pane>
  </a-tabs>
</template>

<script>
import { ref } from 'vue';

let count = 5;

export default {
  setup() {
    const data = ref([
      {
        key: '1',
        title: 'Tab 1',
        content: 'Content of Tab Panel 1'
      },
      {
        key: '2',
        title: 'Tab 2',
        content: 'Content of Tab Panel 2'
      },
      {
        key: '3',
        title: 'Tab 3',
        content: 'Content of Tab Panel 3'
      },
      {
        key: '4',
        title: 'Tab 4',
        content: 'Content of Tab Panel 4'
      }
    ]);

    const handleAdd = () => {
      const number = count++;
      data.value = data.value.concat({
        key: `${number}`,
        title: `New Tab ${number}`,
        content: `Content of New Tab Panel ${number}`
      })
    };
    const handleDelete = (key) => {
      data.value = data.value.filter(item => item.key !== key)
    };

    return {
      data,
      handleAdd,
      handleDelete
    }
  },
}
</script>
```

## Trigger

Specify the trigger method by `trigger`.

```vue
<template>
  <a-radio-group v-model="trigger">
    <a-radio value="click">click</a-radio>
    <a-radio value="hover">hover</a-radio>
  </a-radio-group>
  <a-tabs default-active-key="1" :trigger="trigger">
    <a-tab-pane key="1" title="Tab 1"> Content of Tab Panel 1 </a-tab-pane>
    <a-tab-pane key="2" title="Tab 2"> Content of Tab Panel 2 </a-tab-pane>
    <a-tab-pane key="3">
      <template #title>Tab 3</template>
      Content of Tab Panel 3
    </a-tab-pane>
  </a-tabs>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const trigger = ref('click');
    return {
      trigger,
    };
  },
};
</script>
```

## Scrollable

Support scrolling operation via scroll wheel or touch pad. And you can set the scroll position through the `scrollPosition` property.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-radio-group v-model="position" type="button">
      <a-radio value="left">Left</a-radio>
      <a-radio value="top">Top</a-radio>
      <a-radio value="right">Right</a-radio>
      <a-radio value="bottom">Bottom</a-radio>
    </a-radio-group>
    <a-radio-group v-model="scrollPosition" type="button">
      <a-radio value="auto">auto</a-radio>
      <a-radio value="start">start</a-radio>
      <a-radio value="center">center</a-radio>
      <a-radio value="end">end</a-radio>
    </a-radio-group>
    <a-button @click="changeActive"> Change: {{activeKey}}</a-button>
  </a-space>
  <a-tabs
    v-model:activeKey="activeKey"
    :position="position"
    :scrollPosition="scrollPosition"
    style="width: 100%;height: 300px;margin-top: 20px"
  >
    <a-tab-pane v-for="tab in tabs" :key="tab.key" :title="tab.title">
      {{ tab.content }}
    </a-tab-pane>
  </a-tabs>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const position = ref('top');
    const scrollPosition = ref('auto');
    const activeKey = ref('Tab1');
    const tabs = Array.from({ length: 30 }, (v, i) => {
      return {
        key: `Tab${i + 1}`,
        title: `Tab ${i + 1}`,
        content: `Content of Tab Panel ${i + 1}`
      }
    });

    const changeActive = () => {
      activeKey.value = `Tab${Math.floor(Math.random() * 30) + 1}`;
    }

    return {
      tabs,
      position,
      scrollPosition,
      activeKey,
      changeActive
    }
  },
}
</script>
```

## API

### `<tabs>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|active-key **(v-model)**|The `key` of the currently selected label|`string\|number`|`-`||
|default-active-key|The `key` of the tab selected by default (uncontrolled state, select the first tab page when it is empty)|`string\|number`|`-`||
|position|Position of the tab|`'left' \| 'right' \| 'top' \| 'bottom'`|`'top'`||
|size|The size of the tab|`'mini' \| 'small' \| 'medium' \| 'large'`|`-`||
|type|The type of tab|`'line' \| 'card' \| 'card-gutter' \| 'text' \| 'rounded' \| 'capsule'`|`'line'`||
|direction|The direction of tab|`'horizontal' \| 'vertical'`|`'horizontal'`||
|editable|Whether to enable editable mode|`boolean`|`false`||
|show-add-button|Whether to display the add button (only available in editable mode)|`boolean`|`false`||
|destroy-on-hide|Whether to destroy the content when the label is not displayed|`boolean`|`false`|2.27.0|
|lazy-load|Whether to mount the content when the label is first displayed|`boolean`|`false`||
|justify|The height of the container is fully supported, and it only takes effect in horizontal mode.|`boolean`|`false`||
|animation|Whether to enable option content transition animation|`boolean`|`false`||
|header-padding|Whether there is a horizontal margin on the header of the tab. Only valid for tabs with `type` equal to `line` and `text` type|`boolean`|`true`|2.10.0|
|auto-switch|Whether to switch to a new tab after creating a tab (the last one)|`boolean`|`false`|2.18.0|
|hide-content|Whether to hide content|`boolean`|`false`|2.25.0|
|trigger|Trigger method|`'hover' \| 'click'`|`'click'`|2.34.0|
|scroll-position|The scroll position of the selected tab, the default auto will scroll the activeTab to the visible area, but will not adjust the position intentionally|`'start' \| 'end' \| 'center' \| 'auto' \| number`|`'auto'`||
### `<tabs>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when the current tag value changes|key: ` string \| number `|
|tab-click|Triggered when the user clicks on the tab|key: ` string \| number `|
|add|Triggered when the user clicks the add button|-|
|delete|Triggered when the user clicks the delete button|key: ` string \| number `|
### `<tabs>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|extra|Additional tab content|-|

### `<tab-pane>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|title|Title of the tab|`string`|`-`||
|disabled|Whether to disable|`boolean`|`false`||
|closable|Whether to allow this tab to be closed (only effective in editable mode)|`boolean`|`true`||
|destroy-on-hide|Whether to destroy the content when the label is not displayed|`boolean`|`false`|2.27.0|
### `<tab-pane>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|title|Tab title|-|
