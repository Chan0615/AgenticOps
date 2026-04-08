---
name: arco-vue-avatar
description: "Used as an avatar, it can be displayed in the form of pictures, icons or characters. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Avatar

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

The basic use of avatars. If the avatar is text, the font size will be automatically adjusted to fit the avatar.

```vue
<template>
  <a-space size="large">
    <a-avatar>A</a-avatar>
    <a-avatar :style="{ backgroundColor: '#3370ff' }">
      <IconUser />
    </a-avatar>
    <a-avatar :style="{ backgroundColor: '#14a9f8' }">Arco</a-avatar>
    <a-avatar :style="{ backgroundColor: '#00d0b6' }">Design</a-avatar>
    <a-avatar>
      <img
        alt="avatar"
        src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp"
      />
    </a-avatar>
  </a-space>
</template>

<script>
import { IconUser } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconUser },
};
</script>
```

## Size

The size of the avatar can be adjusted by setting the `size` field. The default size is `40px`. Set the `shape` field, you can set whether the profile picture is a circle or a square.

```vue
<template>
  <a-space size="large" direction="vertical">
    <a-space size="large">
      <a-avatar :size="64">Arco</a-avatar>
      <a-avatar :size="40">Arco</a-avatar>
      <a-avatar :size="32">Arco</a-avatar>
      <a-avatar :size="24">Arco</a-avatar>
    </a-space>
    <a-space size="large">
      <a-avatar :size="64" shape="square">Arco</a-avatar>
      <a-avatar :size="40" shape="square">Arco</a-avatar>
      <a-avatar :size="32" shape="square">Arco</a-avatar>
      <a-avatar :size="24" shape="square">Arco</a-avatar>
    </a-space>
  </a-space>
</template>
```

## Group

Use `Avatar.Group` to group a list of avatars. `size` can be used to specify the size of each avatar..

```vue
<template>
  <a-space :size="32">
    <a-avatar-group>
      <a-avatar :style="{ backgroundColor: '#7BC616' }">A</a-avatar>
      <a-avatar :style="{ backgroundColor: '#14C9C9' }">B</a-avatar>
      <a-avatar :style="{ backgroundColor: '#168CFF' }">C</a-avatar>
      <a-avatar :style="{ backgroundColor: '#FF7D00' }">Arco</a-avatar>
      <a-avatar :style="{ backgroundColor: '#FFC72E' }">Design</a-avatar>
    </a-avatar-group>

    <a-avatar-group :size="24">
      <a-avatar :style="{ backgroundColor: '#7BC616' }">A</a-avatar>
      <a-avatar :style="{ backgroundColor: '#14C9C9' }">B</a-avatar>
      <a-avatar :style="{ backgroundColor: '#168CFF' }">C</a-avatar>
      <a-avatar :style="{ backgroundColor: '#FF7D00' }">Arco</a-avatar>
      <a-avatar :style="{ backgroundColor: '#FFC72E' }">Design</a-avatar>
    </a-avatar-group>

    <a-avatar-group :size="24" :max-count="3">
      <a-avatar :style="{ backgroundColor: '#7BC616' }">A</a-avatar>
      <a-avatar :style="{ backgroundColor: '#14C9C9' }">B</a-avatar>
      <a-avatar :style="{ backgroundColor: '#168CFF' }">C</a-avatar>
      <a-avatar :style="{ backgroundColor: '#FF7D00' }">Arco</a-avatar>
      <a-avatar :style="{ backgroundColor: '#FFC72E' }">Design</a-avatar>
    </a-avatar-group>
  </a-space>
</template>
```

## Trigger Icon

You can customize the interactive button through `trigger-icon` and `trigger-type`. There are two types: `mask` and `button`.

```vue
<template>
  <a-space size="large">
    <a-avatar
      :trigger-icon-style="{ color: '#3491FA' }"
      :auto-fix-font-size="false"
      @click="toast"
      :style="{ backgroundColor: '#168CFF' }"
    >
      A
      <template #trigger-icon>
        <IconCamera />
      </template>
    </a-avatar>
    <a-avatar @click="toast" :style="{ backgroundColor: '#14C9C9' }">
      <IconUser />
      <template #trigger-icon>
        <IconEdit />
      </template>
    </a-avatar>
    <a-avatar
      @click="toast"
      shape="square"
      :style="{ backgroundColor: '#FFC72E' }"
    >
      <IconUser />
      <template #trigger-icon>
        <IconEdit />
      </template>
    </a-avatar>
    <a-avatar trigger-type="mask">
      <img
        alt="avatar"
        src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp"
      />
      <template #trigger-icon>
        <IconEdit />
      </template>
    </a-avatar>
  </a-space>
</template>

<script>
import { IconCamera, IconEdit, IconUser } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconCamera, IconEdit },
  methods: {
    toast() {
      this.$message.info('Uploading...');
    },
  },
};
</script>
```

## Auto Fix Font Size

If the avatar content is text, the font size will be automatically adjusted to fit the content in the avatar.

```vue

<template>
  <a-avatar
    :style="{
      marginRight: '24px',
      verticalAlign: 'middle',
      backgroundColor: '#14a9f8',
    }"
  >
    {{ text }}
  </a-avatar>
  <a-button
    type="secondary"
    @click="onClick"
    :style="{ verticalAlign: 'middle' }"
  >
    Change
  </a-button>
</template>

<script>
import { computed, ref } from 'vue';

const list = ['B', 'Arco', 'Design', 'Tom', 'AD'];
export default {
  setup() {
    const index = ref(0);
    const text = computed(() => list[index.value])

    const onClick = () => {
      index.value = index.value >= list.length - 1 ? 0 : index.value + 1;
    };

    return {
      text,
      onClick
    }
  },
};
</script>
```

## Custom Avatar Path

Custom Avatar Path

```vue
<template>
  <a-space size="large">
    <a-avatar
      imageUrl="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp"
    >
    </a-avatar>
    Load failed:
    <a-avatar
      imageUrl="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9123.png~tplv-uwbnlip3yd-webp.webp"
    >
    </a-avatar>
  </a-space>
</template>
```

## API

### `<avatar>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|shape|The shape of the avatar, there are two kinds of circle (circle) and square (square)|`'circle' \| 'square'`|`'circle'`||
|image-url|Custom avatar image address. If this attribute is passed in, the img tag will be rendered by default|`string`|`-`|2.40.0|
|size|The size of the avatar, the unit is `px`. Use size `40px` in styles when not filled|`number`|`-`||
|auto-fix-font-size|Whether to automatically adjust the font size according to the size of the avatar.|`boolean`|`true`||
|trigger-type|Clickable avatar interaction type|`'mask' \| 'button'`|`'button'`||
|trigger-icon-style|Interactive icon style|`CSSProperties`|`-`||
|object-fit|Object-fit type of the image in the container|`ObjectFit`|`-`|2.52.0|
### `<avatar>` Events

|Event Name|Description|Parameters|
|---|---|---|
|click|Callback when clicked|ev: `MouseEvent`|
|error|image load error|-|
|load|image load success|-|
### `<avatar>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|trigger-icon|Clickable avatar interaction icon|-|

### `<avatar-group>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|shape|The shape of the avatar in the group, there are two kinds of circle (circle) and square (square)|`'circle' \| 'square'`|`'circle'`||
|size|The size of the avatar in the group, the unit is `px`|`number`|`-`||
|auto-fix-font-size|Whether to automatically adjust the font size according to the size of the avatar.|`boolean`|`true`||
|max-count|The maximum number of avatars displayed in the avatar group. The excess avatars will be displayed in the form of `+x`.|`number`|`0`||
|z-index-ascend|The avatar `z-index` in the avatar group increases, and the default is decreasing.|`boolean`|`false`||
|max-style|Style for +x.|`CSSProperties`|`-`|2.7.0|
|max-popover-trigger-props|TriggerProps for popover around +x.|`TriggerProps`|`-`|2.7.0|
