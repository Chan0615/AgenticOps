---
name: arco-vue-page-header
description: "The page header is located at the top of the page container and serves as a content overview and guide page-level operations. Including breadcrumbs, titles, etc. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# PageHeader

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

The basic page header is suitable for use in scenarios that require a simple description. The default is no background color.

```vue
<template>
  <div :style="{ background: 'var(--color-fill-2)', padding: '28px' }" >
    <a-page-header
      :style="{ background: 'var(--color-bg-2)' }"
      title="ArcoDesign"
      subtitle="ArcoDesign Vue 2.0"
    >
      <template #extra>
        <a-radio-group type="button" default-value="large">
          <a-radio value="mini">Mini</a-radio>
          <a-radio value="small">Small</a-radio>
          <a-radio value="large">Large</a-radio>
        </a-radio-group>
      </template>
    </a-page-header>
  </div>
</template>
```

## Breadcrumb

Show breadcrumbs in the header.

```vue
<template>
  <div :style="{ background: 'var(--color-fill-2)', padding: '28px' }" >
    <a-page-header
      :style="{ background: 'var(--color-bg-2)' }"
      title="ArcoDesign"
      subtitle="ArcoDesign Vue 2.0"
      :show-back="false"
    >
      <template #breadcrumb>
        <a-breadcrumb>
          <a-breadcrumb-item>Home</a-breadcrumb-item>
          <a-breadcrumb-item>Channel</a-breadcrumb-item>
          <a-breadcrumb-item>News</a-breadcrumb-item>
        </a-breadcrumb>
      </template>
      <template #extra>
        <a-radio-group type="button" default-value="large">
          <a-radio value="mini">Mini</a-radio>
          <a-radio value="small">Small</a-radio>
          <a-radio value="large">Large</a-radio>
        </a-radio-group>
      </template>
    </a-page-header>
  </div>
</template>

```

## Transparent

The default is no background color, if necessary, you can set a different background color by `style` or class name.

```vue
<template>
  <div :style="{
    backgroundImage: 'radial-gradient(var(--color-fill-3) 1px, rgba(0, 0, 0, 0) 1px)',
    backgroundSize: '16px 16px',
    padding: '28px',
  }">
    <a-page-header title="ArcoDesign" subtitle="ArcoDesign Vue 2.0">
      <template #breadcrumb>
        <a-breadcrumb>
          <a-breadcrumb-item>Home</a-breadcrumb-item>
          <a-breadcrumb-item>Channel</a-breadcrumb-item>
          <a-breadcrumb-item>News</a-breadcrumb-item>
        </a-breadcrumb>
      </template>
      <template #extra>
        <a-radio-group type="button">
          <a-radio value="mini">Mini</a-radio>
          <a-radio value="small">Small</a-radio>
          <a-radio value="large">Large</a-radio>
        </a-radio-group>
      </template>
    </a-page-header>
  </div>
</template>
```

## Content

A complete example of the header.

```vue
<template>
  <div :style="{ background: 'var(--color-fill-2)', padding: '28px' }" >
    <a-page-header
      :style="{ background: 'var(--color-bg-2)' }"
      title="ArcoDesign"
    >
      <template #breadcrumb>
        <a-breadcrumb>
          <a-breadcrumb-item>Home</a-breadcrumb-item>
          <a-breadcrumb-item>Channel</a-breadcrumb-item>
          <a-breadcrumb-item>News</a-breadcrumb-item>
        </a-breadcrumb>
      </template>
      <template #subtitle>
        <a-space>
          <span>ArcoDesign Vue 2.0</span>
          <a-tag color="red" size="small">Default</a-tag>
        </a-space>
      </template>
      <template #extra>
        <a-space>
          <a-button>Cancel</a-button>
          <a-button type="primary">Save</a-button>
        </a-space>
      </template>
      <p>
        For other uses, see Design
      </p>
      <p>
        A design is a plan or specification for the construction of an object or system or for the
        implementation of an activity or process, or the result of that plan or specification in the
        form of a prototype, product or process. The verb to design expresses the process of
        developing a design. In some cases, the direct construction of an object without an explicit
        prior plan (such as in craftwork, some engineering, coding, and graphic design) may also be
        considered to be a design activity. The design usually has to satisfy certain goals and
        constraints, may take into account aesthetic, functional, economic, or socio-political
        considerations, and is expected to interact with a certain environment. Major examples of
        designs include architectural blueprints,engineering drawings, business processes, circuit
        diagrams, and sewing patterns.Major examples of designs include architectural
        blueprints,engineering drawings, business processes, circuit diagrams, and sewing patterns.
      </p>
    </a-page-header>
  </div>
</template>

<script>
export default {
}
</script>
```

## API

### `<page-header>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|title|Main title|`string`|`-`|
|subtitle|Subtitle|`string`|`-`|
|show-back|Whether to show the back button|`boolean`|`true`|
### `<page-header>` Events

|Event Name|Description|Parameters|
|---|---|---|
|back|Emitted when the back button is clicked|event: `Event`|
### `<page-header>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|breadcrumb|Breadcrumb|-||
|back-icon|Back icon|-|2.36.0|
|title|Main title|-||
|subtitle|Subtitle|-||
|extra|Extra content|-||
