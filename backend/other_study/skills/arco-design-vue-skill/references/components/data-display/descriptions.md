---
name: arco-vue-descriptions
description: "Generally used for the information display of the detail page. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Descriptions

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Simply display multiple read-only fields in groups, which are generally used for information on the details page.

```vue
<template>
  <a-space direction="vertical" size="large" fill>
    <a-descriptions :data="data" title="User Info" layout="inline-horizontal" />
    <a-descriptions title="User Info" :column="{xs:1, md:3, lg:4}">
      <a-descriptions-item v-for="item of data" :label="item.label" :span="item.span ?? 1">
        <a-tag>{{ item.value }}</a-tag>
      </a-descriptions-item>
    </a-descriptions>
  </a-space>
</template>

<script>
export default {
  setup() {
    const data = [{
      label: 'Name',
      value: 'Socrates',
      span: 3,
    }, {
      label: 'Mobile',
      value: '123-1234-1234',
    }, {
      label: 'Residence',
      value: 'Beijing'
    }, {
      label: 'Hometown',
      value: 'Beijing',
    }, {
      label: 'Address',
      value: 'Yingdu Building, Zhichun Road, Beijing'
    }];

    return {
      data
    }
  },
}
</script>
```

## Single Row

A single-column description list style.

```vue
<template>
  <a-radio-group type="button" v-model="size">
    <a-radio value="mini">mini</a-radio>
    <a-radio value="small">small</a-radio>
    <a-radio value="medium">medium</a-radio>
    <a-radio value="large">large</a-radio>
  </a-radio-group>
  <a-descriptions style="margin-top: 20px" :data="data" :size="size" title="User Info" :column="1"/>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const size = ref('medium');

    const data = [{
      label: 'Name',
      value: 'Socrates',
    }, {
      label: 'Mobile',
      value: '123-1234-1234',
    }, {
      label: 'Residence',
      value: 'Beijing'
    }, {
      label: 'Hometown',
      value: 'Beijing',
    }, {
      label: 'Address',
      value: 'Yingdu Building, Zhichun Road, Beijing'
    }];

    return {
      data,
      size
    }
  },
}
</script>
```

## Align Label Text

The label text can be left-aligned and right-aligned, or it can be arranged vertically.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-descriptions :data="data" title="User Info" align="right" />
    <a-descriptions :data="data" title="User Info" :align="{ label: 'right' }" />
    <a-descriptions :data="data" title="User Info" layout="inline-vertical" />
  </a-space>
</template>

<script>
export default {
  setup() {
    const data = [{
      label: 'Name',
      value: 'Socrates',
    }, {
      label: 'Mobile',
      value: '123-1234-1234',
    }, {
      label: 'Residence',
      value: 'Beijing'
    }, {
      label: 'Hometown',
      value: 'Beijing',
    }, {
      label: 'Address',
      value: 'Yingdu Building, Zhichun Road, Beijing'
    }];

    return {
      data
    }
  },
}
</script>
```

## Bordered Descriptions

List with border and background color.

```vue
<template>
  <a-descriptions :data="data" title="User Info" bordered/>
</template>

<script>
export default {
  setup() {
    const data = [{
      label: 'Name',
      value: 'Socrates',
    }, {
      label: 'Mobile',
      value: '123-1234-1234',
    }, {
      label: 'Residence',
      value: 'Beijing'
    }, {
      label: 'Hometown',
      value: 'Beijing',
    }, {
      label: 'Address',
      value: 'Yingdu Building, Zhichun Road, Beijing'
    }];

    return {
      data
    }
  },
}
</script>
```

## Layouts

There are four layout modes: horizontal arrangement, vertical arrangement, horizontal arrangement in a row, and vertical arrangement in a row.

```vue

<template>
  <a-radio-group type="button" v-model="size">
    <a-radio value="mini">mini</a-radio>
    <a-radio value="small">small</a-radio>
    <a-radio value="medium">medium</a-radio>
    <a-radio value="large">large</a-radio>
  </a-radio-group>
  <div style="margin-top: 20px">
    <a-descriptions :data="data" :size="size" title="User Info (horizontal)" bordered />
    <a-descriptions :data="data" :size="size" title="User Info (inline-horizontal)" layout="inline-horizontal" bordered />
    <a-descriptions :data="data" :size="size" title="User Info (vertical)" layout="vertical" bordered />
    <a-descriptions :data="data" :size="size" title="User Info (inline-vertical)" layout="inline-vertical" bordered />
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const size = ref('medium');

    const data = [{
      label: 'Name',
      value: 'Socrates',
    }, {
      label: 'Mobile',
      value: '123-1234-1234',
    }, {
      label: 'Residence',
      value: 'Beijing'
    }, {
      label: 'Hometown',
      value: 'Beijing',
    }, {
      label: 'Address',
      value: 'Yingdu Building, Zhichun Road, Beijing'
    }];

    return {
      data,
      size
    }
  },
}
</script>
```

## Layout Example

When the number of columns occupied by `span` is greater than the number of data that can be placed in `column`, `span` will be set to the value of `column`. When the remaining columns in the row are not enough to place the next column, it will automatically wrap, and the last column of each row will automatically fill the remaining amount.

```vue
<template>
  <a-form :model="form" auto-label-width>
    <a-form-item label="size">
      <a-radio-group v-model="form.size" type="button" :options="sizeOptions" />
    </a-form-item>

    <a-form-item label="layout">
      <a-radio-group
        v-model="form.layout"
        type="button"
        :options="layoutOptions"
      />
    </a-form-item>

    <a-form-item label="table-layout">
      <a-radio-group
        v-model="form.tableLayout"
        type="button"
        :options="['auto', 'fixed']"
      />
    </a-form-item>

    <a-form-item label="column">
      <a-radio-group
        v-model="form.column"
        type="button"
        :options="columnOptions"
      />
    </a-form-item>

    <a-form-item label="firstSpan">
      <a-radio-group
        v-model="form.firstSpan"
        type="button"
        :options="firstSpanOptions"
      />
    </a-form-item>
  </a-form>
  <div style="margin-top: 20px">
    <a-descriptions
      title="Layout Example"
      :size="form.size"
      :column="form.column"
      :layout="form.layout"
      :table-layout="form.tableLayout"
      bordered
    >
      <a-descriptions-item label="Item1" :span="form.firstSpan">
        <div>Span: {{form.firstSpan}}
          <span v-if="form.firstSpan > form.column" style="color: red;">
            Exceeds Column, set to Column size
          </span>
        </div>
      </a-descriptions-item>
      <a-descriptions-item label="Item2" :span="2">Span: 2</a-descriptions-item>
      <a-descriptions-item label="Item3" :span="3">Span: 3</a-descriptions-item>
      <a-descriptions-item label="Item4" :span="2">Span: 2</a-descriptions-item>
      <a-descriptions-item label="Item5" :span="1">Span: 1</a-descriptions-item>
      <a-descriptions-item label="Item6" :span="1">Span: 1</a-descriptions-item>
    </a-descriptions>
  </div>
</template>

<script setup>
import { reactive } from 'vue';

const form = reactive({
  size: 'medium',
  layout: 'horizontal',
  column: 4,
  tableLayout: 'auto',
  firstSpan: 2
});

const layoutOptions = [
  'horizontal',
  'inline-horizontal',
  'vertical',
  'inline-vertical',
];
const columnOptions = [1, 2, 3, 4, 5];
const firstSpanOptions = [1, 2, 3, 4, 5];
const sizeOptions = ['mini', 'small', 'medium', 'large'];
</script>
```

## API

### `<descriptions>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|data|Data for descriptions|`DescData[]`|`[]`||
|column|The number of data placed in each row. Version 2.20.0 supports reactive configuration, the configuration can refer to Grid|`number \| ResponsiveValue`|`3`||
|title|Title of descriptions|`string`|`-`||
|layout|Arrangement of descriptions|`'horizontal' \| 'vertical' \| 'inline-horizontal' \| 'inline-vertical'`|`'horizontal'`||
|align|Alignment position of text|`TextAlign \| { label?: TextAlign; value?: TextAlign }`|`'left'`||
|size|The size of the descriptions|`'mini' \| 'small' \| 'medium' \| 'large'`|`-`||
|bordered|Whether to show the border|`boolean`|`false`||
|label-style|Data label style|`CSSProperties`|`-`||
|value-style|Data content style|`CSSProperties`|`-`||
|table-layout|The `layout-fixed` of the table style in the description. The width will be evenly distributed when it's set to `fixed`.|`'auto' \| 'fixed'`|`'auto'`|2.38.0|
### `<descriptions>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|value|Data value|value: `string`<br>index: `number`<br>data: `DescData`|
|label|Data label|label: `string`<br>index: `number`<br>data: `DescData`|
|title|Title|-|

### `<descriptions-item>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|span|number of columns|`number`|`1`|2.18.0|
|label|Label|`string`|`-`|2.18.0|
### `<descriptions-item>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|label|Label|-|2.18.0|

### DescData

|Name|Description|Type|Default|
|---|---|---|:---:|
|label|Label|`string \| RenderFunction`|`-`|
|value|Data|`string \| RenderFunction`|`-`|
|span|number of columns|`number`|`1`|
