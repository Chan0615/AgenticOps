---
name: arco-vue-typography
description: "Used to display titles, paragraphs, and text content. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Typography

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

Display headings, paragraphs, and text content.

```vue
<template>
  <a-typography :style="{ marginTop: '-40px' }">
    <a-typography-title>
      Design system
    </a-typography-title>
    <a-typography-paragraph>
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design.
    </a-typography-paragraph>
    <a-typography-paragraph>
      In some cases, the direct construction of an object without an explicit prior plan (such as in craftwork, some engineering, coding, and graphic design) may also be considered <a-typography-text bold>to be a design activity.</a-typography-text>
    </a-typography-paragraph>
    <a-typography-title :heading="2">ArcoDesign</a-typography-title>
    <a-typography-paragraph>
      The ArcoDesign component library defines a set of default particle variables, and a custom theme is to <a-typography-text mark>customize</a-typography-text> and <a-typography-text underline>overwrite</a-typography-text> this variable list.
    </a-typography-paragraph>
    <a-typography-paragraph blockquote>
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a <a-typography-text code>prototype</a-typography-text>, <a-typography-text code>product</a-typography-text> or <a-typography-text code>process</a-typography-text>. The verb to design expresses the process of developing a design.
    </a-typography-paragraph>
    <a-typography-paragraph mark underline delete>A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process.</a-typography-paragraph>
    <a-typography-paragraph>
      <ul>
        <li>
          Architectural blueprints
          <ul>
            <li>Architectural blueprints</li>
          </ul>
        </li>
        <li>Engineering drawings</li>
        <li>Business processes</li>
      </ul>
    </a-typography-paragraph>
    <a-typography-paragraph>
      <ol>
        <li>Architectural blueprints</li>
        <li>Engineering drawings</li>
        <li>Business processes</li>
      </ol>
    </a-typography-paragraph>
  </a-typography>
</template>
```

## Title

Show titles of different levels.

```vue
<template>
  <a-typography>
    <a-typography-title>
      H1. The Pragmatic Romanticism
    </a-typography-title>
    <a-typography-title :heading="2">
      H2. The Pragmatic Romanticism
    </a-typography-title>
    <a-typography-title :heading="3">
      H3. The Pragmatic Romanticism
    </a-typography-title>
    <a-typography-title :heading="4">
      H4. The Pragmatic Romanticism
    </a-typography-title>
    <a-typography-title :heading="5">
      H5. The Pragmatic Romanticism
    </a-typography-title>
    <a-typography-title :heading="6">
      H6. The Pragmatic Romanticism
    </a-typography-title>
  </a-typography>
</template>
```

## Text

Different styles of text.

```vue
<template>
<a-space direction="vertical" :size="10">
    <a-typography-text>
      Arco Design
    </a-typography-text>
    <a-typography-text type="secondary">
      Secondary
    </a-typography-text>
    <a-typography-text type="primary">
      Primary
    </a-typography-text>
    <a-typography-text type="success">
      Success
    </a-typography-text>
    <a-typography-text type="warning">
      Warning
    </a-typography-text>
    <a-typography-text type="danger">
      Danger
    </a-typography-text>
    <a-typography-text bold>
      Bold
    </a-typography-text>
    <a-typography-text disabled>
      Disabled
    </a-typography-text>
    <a-typography-text mark>
      Mark
    </a-typography-text>
    <a-typography-text underline>
      Underline
    </a-typography-text>
    <a-typography-text delete>
      Line through
    </a-typography-text>
    <a-typography-text code>
      Code snippet
    </a-typography-text>
  </a-space>
</template>
```

## Paragraph

Paragraph style.

```vue
<template>
  <a-typography>
    <a-typography-title :heading="5">Default</a-typography-title>
    <a-typography-paragraph>
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. In some cases, the direct construction of an object without an explicit prior plan (such as in craftwork, some engineering, coding, and graphic design) may also be considered to be a design activity.
    </a-typography-paragraph>
    <a-typography-title :heading="5">Secondary</a-typography-title>
    <a-typography-paragraph type="secondary">
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. In some cases, the direct construction of an object without an explicit prior plan (such as in craftwork, some engineering, coding, and graphic design) may also be considered to be a design activity.
    </a-typography-paragraph>
    <a-typography-title :heading="5">Spacing default</a-typography-title>
    <a-typography-paragraph>
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. In some cases, the direct construction of an object without an explicit prior plan (such as in craftwork, some engineering, coding, and graphic design) may also be considered to be a design activity.
    </a-typography-paragraph>
    <a-typography-title :heading="5">Spacing close</a-typography-title>
    <a-typography-paragraph type="secondary" spacing="close">
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design.
    </a-typography-paragraph>
  </a-typography>
</template>
```

## Interactive

Provide functions such as copying and editing text.

```vue
<template>
  <a-typography>
    <a-typography-paragraph copyable>
      Click the icon to copy this text.
    </a-typography-paragraph>
    <a-typography-paragraph
      editable
      v-model:editText="str"
    >
      {{str}}
    </a-typography-paragraph>
  </a-typography>
</template>
<script>
import { defineComponent, ref } from 'vue';
export default defineComponent({
  setup() {
    const str = ref('Click the icon to edit this text.');
    return {
      str,
    }
  }
});
</script>
```

## Ellipsis

Omit multiple lines of text when there is insufficient space.

```vue
<template>
  <div>
    <a-typography-title :heading="4" ellipsis>
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process.
    </a-typography-title>
    <a-typography-paragraph
      :ellipsis="{
        rows: 2,
        showTooltip: true,
      }"
    >
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. The verb to design expresses the process of developing a design.A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. The verb to design expresses the process of developing a design.
    </a-typography-paragraph>
    <a-typography-paragraph
      :ellipsis="{
        rows: 2,
        showTooltip: true,
        css: true
      }"
    >
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. The verb to design expresses the process of developing a design.A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. The verb to design expresses the process of developing a design.
    </a-typography-paragraph>
    <a-typography-paragraph
      :ellipsis="{
        suffix: '--Arco Design',
        rows: 2,
        expandable: true,
        showTooltip: {
          type: 'popover',
          props: {
            style: { maxWidth: `500px` }
          }
        },
      }"
    >
      <template #expand-node="{expanded}">
        {{ expanded ? '' : 'More' }}
      </template>
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. The verb to design expresses the process of developing a design.A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. The verb to design expresses the process of developing a design.
    </a-typography-paragraph>
    <a-typography-paragraph
      :ellipsis="{
        suffix: '--Arco Design',
        rows: 3,
        expandable: true,
      }"
    >
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. The verb to design expresses the process of developing a design.
      A design is a plan or specification for the construction of an object or system or for the implementation of an activity or process, or the result of that plan or specification in the form of a prototype, product or process. The verb to design expresses the process of developing a design. The verb to design expresses the process of developing a design.
    </a-typography-paragraph>
  </div>
</template>
```

## API

### `Common` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|type|Text type|`'primary' \| 'secondary' \| 'success' \| 'danger' \| 'warning'`|`-`||
|bold|Whether enable bold style|`boolean`|`false`||
|mark|Mark style|`boolean \| { color: string }`|`false`||
|underline|Whether enable underline style|`boolean`|`false`||
|delete|Whether enable delete style|`boolean`|`false`||
|code|Whether enable code style|`boolean`|`false`||
|disabled|Whether disabled|`boolean`|`false`||
|editable|Whether it's editable|`boolean`|`false`||
|editing **(v-model)**|Whether it's editing|`boolean`|`-`||
|default-editing|Default editing state|`boolean`|`false`||
|edit-text **(v-model)**|Edit text|`string`|`-`||
|copyable|Whether turn on copy functionality|`boolean`|`false`||
|copy-text|Copied text|`string`|`-`||
|copy-delay|After the copy is successful, the delay time for the copy button to return to the clickable state, in milliseconds|`number`|`3000`|2.16.0|
|ellipsis|Automatic overflow omission, refer to [EllipsisConfig](#EllipsisConfig) for more information.|`boolean \| EllipsisConfig`|`false`||
|edit-tooltip-props|Edit button question prompt configuration|`object`|`-`|2.32.0|
|copy-tooltip-props|Copy button question prompt configuration|`object`|`-`|2.32.0|
### `Common` Events

|Event Name|Description|Parameters|
|---|---|---|
|edit-start|Edit start|-|
|change|Edit content change|text: `string`|
|edit-end|Edit end|-|
|copy|Copy|text: `string`|
|ellipsis|Ellipsis change|isEllipsis: `boolean`|
|expand|Expand collapse event|expanded: `boolean`|
### `Common` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|expand-node|Custom expand button|expanded: `boolean`|
|copy-icon|Custom copy button icon|copied: `boolean`|
|copy-tooltip|Customize the tooltip content of the copy button|copied: `boolean`|

### `<typography-title>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|heading|Heading level, equivalent to `h1` `h2` `h3` `h4` `h5` `h6`|`'1' \| '2' \| '3' \| '4' \| '5' \| '6'`|`1`|

### `<typography-paragraph>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|blockquote|Whether enable blockquote|`boolean`|`false`|
|spacing|The line height of the paragraph, the default line height is recommended for long text (more than 5 lines). `close` line height is recommended for short text (less than or equal to 3 lines).|`'default' \| 'close'`|`'default'`|

### EllipsisConfig

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|rows|The number of omitted lines|`number`|`1`||
|expandable|Whether expandable|`boolean`|`false`||
|ellipsisStr|Ellipsis string|`string`|`'...'`||
|suffix|Suffix|`string`|`-`||
|showTooltip|Pop-up box when configuration is omitted|`boolean    \| { type: 'tooltip' \| 'popover'; props: Record<string, any> }`|`false`||
|css|Whether to use CSS ellipsis (expansion, custom ellipsis and suffix are not supported in this mode)|`boolean`|`false`|2.37.0|
