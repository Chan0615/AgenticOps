---
name: arco-vue-tag
description: "Used for the selection, screening and classification of information. Users use tags for information feedback and interactive operations. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Tag

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of tags

```vue
<template>
  <a-space>
    <a-tag>Default</a-tag>
    <a-tag>Tag 1</a-tag>
    <a-tag>Tag 2</a-tag>
    <a-tag>
      <template #icon>
        <icon-check-circle-fill />
      </template>
      Complete
    </a-tag>
  </a-space>
</template>
```

## Closeable

Use the `closable` attribute to control whether the label can be closed. Closable tags can perform some post-closing operations through the `close` event, and the display or hiding of the tags can also be controlled through the `visible` property.

```vue
<template>
  <a-space>
    <a-tag closable>Tag</a-tag>
    <a-tag closable>
      <template #icon>
        <icon-star/>
      </template>
      Tag
    </a-tag>
  </a-space>
</template>
```

## Dynamically Edit

Can add and delete tags dynamically.

```vue
<template>
  <a-space wrap>
    <a-tag
      v-for="(tag, index) of tags"
      :key="tag"
      :closable="index !== 0"
      @close="handleRemove(tag)"
    >
      {{ tag }}
    </a-tag>

    <a-input
      v-if="showInput"
      ref="inputRef"
      :style="{ width: '90px'}"
      size="mini"
      v-model.trim="inputVal"
      @keyup.enter="handleAdd"
      @blur="handleAdd"
    />
    <a-tag
      v-else
      :style="{
        width: '90px',
        backgroundColor: 'var(--color-fill-2)',
        border: '1px dashed var(--color-fill-3)',
        cursor: 'pointer',
      }"
      @click="handleEdit"
    >
      <template #icon>
        <icon-plus />
      </template>
      Add Tag
    </a-tag>
  </a-space>
</template>

<script>
import { ref, nextTick } from 'vue';

export default {
  setup() {
    const tags = ref(['Tag 1', 'Tag 2', 'Tag 3']);
    const inputRef = ref(null);
    const showInput = ref(false);
    const inputVal = ref('');

    const handleEdit = () => {
      showInput.value = true;

      nextTick(() => {
        if (inputRef.value) {
          inputRef.value.focus();
        }
      });
    };

    const handleAdd = () => {
      if (inputVal.value) {
        tags.value.push(inputVal.value);
        inputVal.value = '';
      }
      showInput.value = false;
    };

    const handleRemove = (key) => {
      tags.value = tags.value.filter((tag) => tag !== key);
    };

    return {
      tags,
      inputRef,
      showInput,
      inputVal,
      handleEdit,
      handleAdd,
      handleRemove,
    };
  },
};
</script>

```

## Checkable

By setting `checkable`, the effect of selecting can be achieved.

```vue
<template>
  <a-space>
    <a-tag checkable>Awesome</a-tag>
    <a-tag checkable color="red" :default-checked="true">Toutiao</a-tag>
    <a-tag checkable color="arcoblue" :default-checked="true">Lark</a-tag>
  </a-space>
</template>
```

## Color

We provide a variety of label styles with preset colors, and set different colors through `color`. If the preset value cannot meet your needs, you can also set a custom color value in the `color` field.

```vue
<template>
  <a-space wrap>
    <a-tag v-for="(color, index) of colors" :key="index" :color="color" closable>{{ color }}</a-tag>
  </a-space>
  <h3>Custom Color:</h3>
  <a-space wrap>
    <a-tag v-for="(color, index) of custom" :key="index" :color="color" closable>{{ color }}</a-tag>
  </a-space>
</template>

<script>
export default {
  setup() {
    const colors = [
      'red',
      'orangered',
      'orange',
      'gold',
      'lime',
      'green',
      'cyan',
      'blue',
      'arcoblue',
      'purple',
      'pinkpurple',
      'magenta',
      'gray'
    ];
    const custom = [
      '#f53f3f',
      '#7816ff',
      '#00b42a',
      '#165dff',
      '#ff7d00',
      '#eb0aa4',
      '#7bc616',
      '#86909c',
      '#b71de8',
      '#0fc6c2',
      '#ffb400',
      '#168cff',
      '#ff5722'
    ];

    return {
      colors,
      custom
    }
  },
}
</script>
```

## Size

The size of the label is divided into three types: `small`, `medium`, and `large`. The appropriate button size can be selected in different scenarios. The recommended and default size is `medium`.

```vue
<template>
  <a-space>
    <a-tag size="large">Large</a-tag>
    <a-tag>Medium</a-tag>
    <a-tag size="small">Small</a-tag>
  </a-space>
</template>
```

## Loading

The loading status of the tag.

```vue
<template>
  <a-tag loading>Loading</a-tag>
</template>
```

## Icon

An icon can be added to the tag through the `icon` slot.

```vue
<template>
  <a-space>
    <a-tag color="gray">
      <template #icon>
        <icon-github/>
      </template>
      Github
    </a-tag>
    <a-tag color="orangered">
      <template #icon>
        <icon-gitlab/>
      </template>
      Gitlab
    </a-tag>
    <a-tag color="blue">
      <template #icon>
        <icon-twitter/>
      </template>
      Twitter
    </a-tag>
    <a-tag color="arcoblue">
      <template #icon>
        <icon-facebook/>
      </template>
      Facebook
    </a-tag>
  </a-space>
</template>
```

## Bordered

Through the prop `bordered` to display a bordered tag.

```vue
<template>
   <a-space wrap>
    <a-tag bordered>default</a-tag>
    <a-tag v-for="(color, index) of colors" :key="index" :color="color" bordered>{{ color }}</a-tag>
  </a-space>
</template>

<script>
export default {
  setup() {
    const colors = [
      'orangered',
      'orange',
      'gold',
      'lime',
      'green',
      'cyan',
      'blue',
      'arcoblue',
      'purple',
      'pinkpurple',
      'magenta',
      'gray'
    ];
    return {
      colors
    }
  },
}
</script>
```

## API

### `<tag>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|color|Label color|`'red' \| 'orangered' \| 'orange' \| 'gold' \| 'lime' \| 'green' \| 'cyan' \| 'blue' \| 'arcoblue' \| 'purple' \| 'pinkpurple' \| 'magenta' \| 'gray'`|`-`||
|size|Label size|`'small' \| 'medium' \| 'large'`|`'medium'`||
|bordered|Whether the tag is bordered|`boolean`|`false`|2.33.0|
|visible **(v-model)**|Whether the tag is visible|`boolean`|`-`||
|default-visible|Whether the tag is visible by default|`boolean`|`true`||
|loading|Whether the tag is loading state|`boolean`|`false`||
|closable|Whether the tag can be closed|`boolean`|`false`||
|checkable|Whether the tag can be checked|`boolean`|`false`||
|checked **(v-model)**|Whether the tag is checked (available when the tag is checkable)|`boolean`|`-`||
|default-checked|Whether the tag is checked by default (available when the tag is checkable)|`boolean`|`true`||
|nowrap|Tag content does not wrap|`boolean`|`false`|2.56.1|
### `<tag>` Events

|Event Name|Description|Parameters|
|---|---|---|
|close|Emitted when the close button is clicked|ev: `MouseEvent`|
|check|Emitted when the user check (emit only in the checkable mode)|checked: `boolean`<br>ev: `MouseEvent`|
### `<tag>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|icon|Icon|-|
|close-icon|Close button icon|-|
