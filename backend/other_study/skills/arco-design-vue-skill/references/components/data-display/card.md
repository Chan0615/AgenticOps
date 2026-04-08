---
name: arco-vue-card
description: "Card is generally used as a concise introduction or a large plate and entrance of information. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Card

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Conventional content containers can hold text, lists, pictures, and paragraphs, and are often used for module division and content overview

```vue
<template>
  <div :style="{ display: 'flex' }">
    <a-card :style="{ width: '360px' }" title="Arco Card">
      <template #extra>
        <a-link>More</a-link>
      </template>
      ByteDance's core product, Toutiao ("Headlines"), is a content platform in
      China and around the world. Toutiao started out as a news recommendation
      engine and gradually evolved into a platform delivering content in various
      formats.
    </a-card>
  </div>
</template>
```

## Hoverable

Set `hoverable` to add a mouse hover style to the card, and you can customize the hover style through style override.

```vue
<template>
  <div :style="{ display: 'flex' }">
    <a-card :style="{ width: '360px' }" title="Arco Card" hoverable>
      <template #extra>
        <a-link>More</a-link>
      </template>
      Card content <br />
      Card content
    </a-card>
    <a-card
      class="card-demo"
      title="Custom hover style"
      hoverable
    >
      <template #extra>
        <a-link>More</a-link>
      </template>
      Card content <br />
      Card content
    </a-card>
  </div>
</template>
<style scoped>
.card-demo {
  width: 360px;
  margin-left: 24px;
  transition-property: all;
}
.card-demo:hover {
  transform: translateY(-4px);
}
</style>
```

## No Border

Set `bordered` to `false` to use borderless cards.

```vue
<template>
  <div
    :style="{
      display: 'flex',
      width: '100%',
      boxSizing: 'border-box',
      padding: '40px',
      backgroundColor: 'var(--color-fill-2)',
    }"
  >
    <a-card :style="{ width: '360px' }" title="Arco Card" :bordered="false">
      <template #extra>
        <a-link>More</a-link>
      </template>
      Card content
      <br />
      Card content
    </a-card>
    <a-card
      :style="{ width: '360px', marginLeft: '24px' }"
      title="Hover me"
      hoverable
      :bordered="false"
    >
      <template #extra>
        <a-link>More</a-link>
      </template>
      Card content
      <br />
      Card content
    </a-card>
  </div>
</template>
```

## Only Content

A card that only has a content area.

```vue
<template>
  <a-card hoverable :style="{ width: '360px', marginBottom: '20px' }">
    <div
      :style="{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }"
    >
      <span
        :style="{ display: 'flex', alignItems: 'center', color: '#1D2129' }"
      >
        <a-avatar
          :style="{ marginRight: '8px', backgroundColor: '#165DFF' }"
          :size="28"
        >
          A
        </a-avatar>
        <a-typography-text>Username</a-typography-text>
      </span>
      <a-link>More</a-link>
    </div>
  </a-card>
</template>
```

## Meta

Use `Card.Meta` to support more flexible content (cover, avatar, title, description)

```vue
<template>
  <a-card hoverable :style="{ width: '360px' }">
    <template #cover>
      <div
        :style="{
          height: '204px',
          overflow: 'hidden',
        }"
      >
        <img
          :style="{ width: '100%', transform: 'translateY(-20px)' }"
          alt="dessert"
          src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a20012a2d4d5b9db43dfc6a01fe508c0.png~tplv-uwbnlip3yd-webp.webp"
        />
      </div>
    </template>
    <a-card-meta title="Card Title">
      <template #description>
        Card content <br />
        Card content
      </template>
    </a-card-meta>
  </a-card>
</template>
```

## With Row

The system overview page often cooperates with the grid.

```vue
<template>
  <div
    :style="{
      boxSizing: 'border-box',
      width: '100%',
      padding: '40px',
      backgroundColor: 'var(--color-fill-2)',
    }"
  >
    <a-row :gutter="20" :style="{ marginBottom: '20px' }">
      <a-col :span="8">
        <a-card title="Arco Card" :bordered="false" :style="{ width: '100%' }">
          <template #extra>
            <a-link>More</a-link>
          </template>
          Card content
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="Arco Card" :bordered="false" :style="{ width: '100%' }">
          <template #extra>
            <a-link>More</a-link>
          </template>
          Card content
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="Arco Card" :bordered="false" :style="{ width: '100%' }">
          <template #extra>
            <a-link>More</a-link>
          </template>
          Card content
        </a-card>
      </a-col>
    </a-row>
    <a-row :gutter="20">
      <a-col :span="16">
        <a-card title="Arco Card" :bordered="false" :style="{ width: '100%' }">
          <template #extra>
            <a-link>More</a-link>
          </template>
          Card content
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="Arco Card" :bordered="false" :style="{ width: '100%' }">
          <template #extra>
            <a-link>More</a-link>
          </template>
          Card content
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>
```

## Card Grid

Use `Card.Grid` to use the card content segmentation mode.

```vue
<template>
  <a-card :bordered="false" :style="{ width: '100%' }">
    <a-card-grid
      v-for="(_, index) in new Array(7)"
      :key="index"
      :hoverable="index % 2 === 0"
      :style="{ width: '25%' }"
    >
      <a-card
        class="card-demo"
        title="Arco Card"
        :bordered="false"
      >
        <template #extra>
          <a-link>More</a-link>
        </template>
        <p :style="{ margin: 0 }">
          {{ index % 2 === 0 ? 'Card allow to hover' : 'Card content' }}
        </p>
      </a-card>
    </a-card-grid>
  </a-card>
</template>
<style scoped>
.card-demo {
  width: 100%;
}
.card-demo :deep(.arco-card-header) {
  border: none;
}
</style>
```

## Inner Card

Other card components can be nested in the card.

```vue
<template>
  <a-card title="Arco Card">
    <a-card :style="{ marginBottom: '20px' }" title="Inner Card Title">
      <template #extra>
        <a-link>More</a-link>
      </template>
      Inner Card Content
    </a-card>
    <a-card title="Inner Card Title">
      <template #extra>
        <a-link>More</a-link>
      </template>
      Inner Card Content
    </a-card>
  </a-card>
</template>
```

## With Actions

The `actions` slot can be used to display the bottom button group.

```vue
<template>
  <a-card :style="{ width: '360px' }">
    <template #actions>
      <span class="icon-hover"> <IconThumbUp /> </span>
      <span class="icon-hover"> <IconShareInternal /> </span>
      <span class="icon-hover"> <IconMore /> </span>
    </template>
    <template #cover>
      <div
        :style="{
          height: '204px',
          overflow: 'hidden',
        }"
      >
        <img
          :style="{ width: '100%', transform: 'translateY(-20px)' }"
          alt="dessert"
          src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a20012a2d4d5b9db43dfc6a01fe508c0.png~tplv-uwbnlip3yd-webp.webp"
        />
      </div>
    </template>
    <a-card-meta title="Card Title" description="This is the description">
      <template #avatar>
        <div
          :style="{ display: 'flex', alignItems: 'center', color: '#1D2129' }"
        >
          <a-avatar :size="24" :style="{ marginRight: '8px' }">
            A
          </a-avatar>
          <a-typography-text>Username</a-typography-text>
        </div>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script>
import {
  IconThumbUp,
  IconShareInternal,
  IconMore,
} from '@arco-design/web-vue/es/icon';

export default {
  components: { IconThumbUp, IconShareInternal, IconMore },
};
</script>
<style scoped>
.icon-hover {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  transition: all 0.1s;
}
.icon-hover:hover {
  background-color: rgb(var(--gray-2));
}
</style>
```

## API

### `<card>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|bordered|Whether to render the border|`boolean`|`true`|
|loading|Loading status|`boolean`|`false`|
|hoverable|Can be hovered|`boolean`|`false`|
|size|Size of card|`'medium' \| 'small'`|`'medium'`|
|header-style|The additional css style to apply to card head|`CSSProperties`|`() => ({})`|
|body-style|The additional css style to apply to card content|`CSSProperties`|`() => ({})`|
|title|Title of card|`string`|`-`|
|extra|Content to render in the top-right corner of the card|`string`|`-`|
### `<card>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|actions|The action list which shows at the bottom of the Card|-|
|cover|Cover of card|-|
|extra|Content to render in the top-right corner of the card|-|
|title|Title of card|-|

### `<card-meta>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|title|Title of card|`string`|`-`|
|description|Description of card|`string`|`-`|
### `<card-meta>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|description|Description of card|-|
|title|Title of card|-|
|avatar|Avatar of card|-|

### `<card-grid>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|hoverable|Whether to hover|`boolean`|`false`|
