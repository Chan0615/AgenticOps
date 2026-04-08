---
name: arco-vue-list
description: "The most basic list display, which can carry text, lists, pictures, and paragraphs, and is often used in the background data display page. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# List

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of the list. Can be used to carry text, lists, pictures and paragraphs.

```vue
<template>
  <a-list>
    <template #header>
      List title
    </template>
    <a-list-item>Beijing Bytedance Technology Co., Ltd.</a-list-item>
    <a-list-item>Bytedance Technology Co., Ltd.</a-list-item>
    <a-list-item>Beijing Toutiao Technology Co., Ltd.</a-list-item>
    <a-list-item>Beijing Volcengine Technology Co., Ltd.</a-list-item>
    <a-list-item>China Beijing Bytedance Technology Co., Ltd.</a-list-item>
  </a-list>
</template>
```

## Sizes

The list component provides three sizes `small, medium, large`, which can be selected according to business needs.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-radio-group v-model="size" type="button">
      <a-radio value="small">Small</a-radio>
      <a-radio value="medium">Medium</a-radio>
      <a-radio value="large">Large</a-radio>
    </a-radio-group>
    <a-list :size="size">
      <template #header>
        List title
      </template>
      <a-list-item>Beijing Bytedance Technology Co., Ltd.</a-list-item>
      <a-list-item>Bytedance Technology Co., Ltd.</a-list-item>
      <a-list-item>Beijing Toutiao Technology Co., Ltd.</a-list-item>
      <a-list-item>Beijing Volcengine Technology Co., Ltd.</a-list-item>
      <a-list-item>China Beijing Bytedance Technology Co., Ltd.</a-list-item>
    </a-list>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const size = ref('medium');

    return {
      size
    }
  },
}
</script>
```

## List Item Meta

Use the `list-item-meta` component to quickly specify the avatar, title, and text.

```vue
<template>
  <a-list>
    <a-list-item v-for="idx in 4" :key="idx">
      <a-list-item-meta
        title="Beijing Bytedance Technology Co., Ltd."
        description="Beijing ByteDance Technology Co., Ltd. is an enterprise located in China."
      >
        <template #avatar>
          <a-avatar shape="square">
            <img
              alt="avatar"
              src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp"
            />
          </a-avatar>
        </template>
      </a-list-item-meta>
    </a-list-item>
  </a-list>
</template>
```

## With Actions

Use `actions` to add operation items to the list.

```vue
<template>
  <a-list>
    <a-list-item v-for="idx in 4" :key="idx">
      <a-list-item-meta
        title="Beijing Bytedance Technology Co., Ltd."
        description="Beijing ByteDance Technology Co., Ltd. is an enterprise located in China."
      >
        <template #avatar>
          <a-avatar shape="square">
            <img
              alt="avatar"
              src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp"
            />
          </a-avatar>
        </template>
      </a-list-item-meta>
      <template #actions>
        <icon-edit />
        <icon-delete />
      </template>
    </a-list-item>
  </a-list>
</template>
```

## Vertical List

This is an example including paging, content on the right, and list operations.

```vue
<template>
  <a-list
    class="list-demo-action-layout"
    :bordered="false"
    :data="dataSource"
    :pagination-props="paginationProps"
  >
    <template #item="{ item }">
      <a-list-item class="list-demo-item" action-layout="vertical">
        <template #actions>
          <span><icon-heart />83</span>
          <span><icon-star />{{ item.index }}</span>
          <span><icon-message />Reply</span>
        </template>
        <template #extra>
          <div class="image-area">
            <img alt="arco-design" :src="item.imageSrc" />
          </div>
        </template>
        <a-list-item-meta
          :title="item.title"
          :description="item.description"
        >
          <template #avatar>
            <a-avatar shape="square">
              <img alt="avatar" :src="item.avatar" />
            </a-avatar>
          </template>
        </a-list-item-meta>
      </a-list-item>
    </template>
  </a-list>
</template>

<script>
import { reactive } from 'vue'

const names = ['Socrates', 'Balzac', 'Plato'];
const avatarSrc = [
  '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp',
  '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/e278888093bef8910e829486fb45dd69.png~tplv-uwbnlip3yd-webp.webp',
  '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/9eeb1800d9b78349b24682c3518ac4a3.png~tplv-uwbnlip3yd-webp.webp',
];
const imageSrc = [
  '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/29c1f9d7d17c503c5d7bf4e538cb7c4f.png~tplv-uwbnlip3yd-webp.webp',
  '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/04d7bc31dd67dcdf380bc3f6aa07599f.png~tplv-uwbnlip3yd-webp.webp',
  '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/1f61854a849a076318ed527c8fca1bbf.png~tplv-uwbnlip3yd-webp.webp',
];
const dataSource = new Array(15).fill(null).map((_, index) => {
  return {
    index: index,
    avatar: avatarSrc[index % avatarSrc.length],
    title: names[index % names.length],
    description:
      'Beijing ByteDance Technology Co., Ltd. is an enterprise located in China. ByteDance has products such as TikTok, Toutiao, volcano video and Douyin (the Chinese version of TikTok).',
    imageSrc: imageSrc[index % imageSrc.length],
  };
});

export default {
  setup() {
    return {
      dataSource,
      paginationProps: reactive({
        defaultPageSize: 3,
        total: dataSource.length
      })
    }
  },
}
</script>

<style scoped>
.list-demo-action-layout .image-area {
  width: 183px;
  height: 119px;
  border-radius: 2px;
  overflow: hidden;
}

.list-demo-action-layout .list-demo-item {
  padding: 20px 0;
  border-bottom: 1px solid var(--color-fill-3);
}

.list-demo-action-layout .image-area img {
  width: 100%;
}

.list-demo-action-layout .arco-list-item-action .arco-icon {
  margin: 0 4px;
}
</style>
```

## Grid

Configure the grid list through the `grid` property.

```vue
<template>
  <a-list :gridProps="{ gutter: 0, span: 6 }" :bordered="false">
    <a-list-item>
      <a-list>
        <template #header>Platform</template>
        <a-list-item>iOS</a-list-item>
        <a-list-item>Android</a-list-item>
        <a-list-item>Web</a-list-item>
      </a-list>
    </a-list-item>
    <a-list-item>
      <a-list>
        <template #header>Framework</template>
        <a-list-item>Angular</a-list-item>
        <a-list-item>Vue</a-list-item>
        <a-list-item>React</a-list-item>
      </a-list>
    </a-list-item>
    <a-list-item>
      <a-list>
        <template #header>Language</template>
        <a-list-item>C++</a-list-item>
        <a-list-item>JavaScript</a-list-item>
        <a-list-item>Python</a-list-item>
      </a-list>
    </a-list-item>
    <a-list-item>
      <a-list>
        <template #header>Component</template>
        <a-list-item>Button</a-list-item>
        <a-list-item>Breadcrumb</a-list-item>
        <a-list-item>Transfer</a-list-item>
      </a-list>
    </a-list-item>
  </a-list>
</template>
```

## Responsive List Grid

Dynamically set the number of columns occupied by each item through parameters such as `grid.sm`. Be careful not to set `grid.span` at this time.

```vue
<template>
  <a-list
    :grid-props="{ gutter: [20, 20], sm: 24, md: 12, lg: 8, xl: 6 }"
    :data="dataSource"
    :bordered="false"
  >
    <template #item="{ item }">
      <a-list :data="item.data">
        <template #header>{{ item.title }}</template>
        <template #item="{ item: subItem }">
          <a-list-item>{{ subItem }}</a-list-item>
        </template>
      </a-list>
    </template>
  </a-list>
</template>

<script>
const dataSource = [
  {
    title: 'Platform',
    data: ['iOS', 'Android', 'Web'],
  },
  {
    title: 'Framework',
    data: ['Angular', 'Vue', 'React'],
  },
  {
    title: 'Language',
    data: ['C++', 'JavaScript', 'Python'],
  },
  {
    title: 'Component',
    data: ['Button', 'Breadcrumb', 'Transfer'],
  },
  {
    title: 'Design',
    data: ['Figma', 'Sketch', 'Adobe XD'],
  },
  {
    title: 'Plugin',
    data: ['Edu Tools', 'BashSupport', 'GitToolBox'],
  },
  {
    title: 'Platform',
    data: ['iOS', 'Android', 'Web'],
  },
  {
    title: 'Framework',
    data: ['Angular', 'Vue', 'React'],
  },
  {
    title: 'Language',
    data: ['C++', 'JavaScript', 'Python'],
  },
];

export default {
  setup() {
    return {
      dataSource
    }
  }
}
</script>
```

## Scroll

Limit the maximum height of the list by setting the `max-height` property. Through the `reach-bottom` event, you can
listen to the event of the bottom of the list.

```vue
<template>
  <div style="margin-bottom: 10px">
    <a-switch v-model="scrollbar" />
    Virtual Scrollbar
  </div>
  <a-list :max-height="240" @reach-bottom="fetchData" :scrollbar="scrollbar">
    <template #header>
      List title
    </template>
    <template #scroll-loading>
      <div v-if="bottom">No more data</div>
      <a-spin v-else />
    </template>
    <a-list-item v-for="item of data">{{item}}</a-list-item>
  </a-list>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const current = ref(1);
    const bottom = ref(false);
    const data = reactive([]);
    const scrollbar = ref(true);

    const fetchData = () => {
      console.log('reach bottom!');
      if (current.value <= 5) {
        window.setTimeout(() => {
          const index = data.length;
          data.push(
            `Beijing Bytedance Technology Co., Ltd. ${index + 1}`,
            `Bytedance Technology Co., Ltd. ${index + 2}`,
            `Beijing Toutiao Technology Co., Ltd. ${index + 3}`,
            `Beijing Volcengine Technology Co., Ltd. ${index + 4}`,
            `China Beijing Bytedance Technology Co., Ltd. ${index + 5}`
          );
          current.value += 1
        }, 2000)
      } else {
        bottom.value = true
      }
    }

    return {
      current,
      bottom,
      data,
      fetchData,
      scrollbar
    }
  },
}
</script>
```

## Infinite List

By specifying `virtualListProps` to turn on the virtual list, high performance can be obtained when a large amount of data is used.
When using a virtual list, if the height of the list items varies greatly, it may cause blank space in the viewport when scrolling, which can be solved by setting `virtualListProps.buffer`, see the Arco Vue FAQ entry about virtual lists.

```vue

<template>
  <h3 :style="{ color: 'var(--color-text-2)' }">10000 items</h3>
  <a-list
    :style="{ width: `600px` }"
    :virtualListProps="{
      height: 560,
    }"
    :data="list"
  >
    <template #item="{ item, index }">
      <a-list-item :key="index">
        <a-list-item-meta
          :title="item.title"
          :description="item.description"
        >
          <template #avatar>
            <a-avatar shape="square">
              A
            </a-avatar>
          </template>
        </a-list-item-meta>
      </a-list-item>
    </template>
  </a-list>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const list = reactive(Array(10000).fill(null).map((_, index) => {
      const prefix = `0000${index}`.slice(-5);
      return {
        title: 'Beijing Bytedance Technology Co., Ltd.',
        description: `(${prefix}) Beijing ByteDance Technology Co., Ltd. is an enterprise located in China.`,
      };
    }))

    return {
      list
    }
  },
}
</script>
```

## API

### `<list>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|data|List data, need to be used with `item` slot at the same time|`any[]`|`-`||
|size|List size|`'small' \| 'medium' \| 'large'`|`'medium'`||
|bordered|Whether to show the border|`boolean`|`true`||
|split|Whether to show the dividing line|`boolean`|`true`||
|loading|Whether it is loading state|`boolean`|`false`||
|hoverable|Whether to display the selected style|`boolean`|`false`||
|pagination-props|List pagination configuration|`PaginationProps`|`-`||
|grid-props|List grid configuration|`object`|`-`||
|max-height|Maximum height of the list|`string \| number`|`0`||
|bottom-offset|Trigger the distance threshold to reach the bottom|`number`|`0`||
|virtual-list-props|Pass virtual list properties, pass in this parameter to turn on virtual scrolling [VirtualListProps](#VirtualListProps)|`VirtualListProps`|`-`||
|scrollbar|Whether to enable virtual scroll bar|`boolean \| ScrollbarProps`|`true`|2.38.0|
### `<list>` Events

|Event Name|Description|Parameters|
|---|---|---|
|scroll|Triggered when the list scrolls|-|
|reach-bottom|Triggered when the list reaches the bottom|-|
|page-change|Triggered when the table pagination changes|page: `number`|
|page-size-change|Triggered when the number of data per page of the table changes|pageSize: `number`|
### `<list>` Methods

|Method|Description|Parameters|Return|
|---|---|---|:---:|
|scrollIntoView|Virtual scroll to an element|options: `{ index?: number; key?: number \| string; align: 'auto' \| 'top' \| 'bottom'}`|-|
### `<list>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|scroll-loading|When scrolling loading state, scroll to the bottom tip|-|2.20.0|
|item|List Item|index: `number`<br>item: `any`||
|empty|Empty|-||
|footer|Footer|-||
|header|Header|-||

### `<list-item>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|action-layout|Operation group arrangement direction|`Direction`|`'horizontal'`|
### `<list-item>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|meta|Meta data|-|
|extra|Extra content|-|
|actions|Actions|-|

### `<list-item-meta>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|title|Title|`string`|`-`|
|description|Description|`string`|`-`|
### `<list-item-meta>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|avatar|Avatar|-|
|title|Title|-|
|description|Description|-|

### VirtualListProps

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|height|Viewable area height|`number \| string`|`-`||
|threshold|The threshold of the number of elements to enable virtual scrolling. When the number of data is less than the threshold, virtual scrolling will not be enabled.|`number`|`-`||
|isStaticItemHeight|(Repealed) Is the element height fixed. Version 2.18.0 deprecated, please use `fixedSize`|`boolean`|`false`||
|fixedSize|Is the element height fixed.|`boolean`|`false`|2.34.1|
|estimatedSize|Is the element height fixed.|`number`|`-`|2.34.1|
|buffer|The number of elements mounted in advance outside the boundary of the viewport.|`number`|`10`|2.34.1|
