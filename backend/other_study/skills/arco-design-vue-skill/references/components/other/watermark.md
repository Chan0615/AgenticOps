---
name: arco-vue-watermark
description: "Used to Add a watermark to a specified area. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Watermark

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of the watermark.

```vue
<template>
  <a-watermark content="arco.design">
    <div style="width: 100%; height: 350px;" />
  </a-watermark>
</template>
```

## Multiline Text

Multi-line text watermarks can be specified with the content set string array.

```vue
<template>
  <a-watermark :content="['arco.design',dayjs().format('YYYY-MM-DD')]">
    <div style="width: 100%; height: 300px;" />
  </a-watermark>
</template>
<script>
import dayjs from 'dayjs';

export default {
  setup() {
    return {
      dayjs,
    }
  }
}
</script>
```

## Image Watermark

Set an image watermark using the image property. It's recommended to use 2x or 3x images (supports Base64).

```vue
<template>
  <a-watermark content="acro.design" grayscale image="">
    <div style="width: 100%; height: 300px;" />
  </a-watermark>
</template>
```

## Custom

Customize the watermark.

```vue
<template>
  <a-form size="small" :model="form" auto-label-width>
    <a-row :gutter="16">
      <a-col :span="24">
        <a-form-item field="rotate" label="rotate">
          <a-slider v-model="form.rotate" :min="-180" :max="180" />
        </a-form-item>
      </a-col>
      <a-col :span="12">
        <a-form-item label="gap">
          <a-input-group>
            <a-input-number
              v-model="form.gap[0]"
              placeholder="gap[x]"
              :min="0"
            />
            <a-input-number
              v-model="form.gap[1]"
              placeholder="gap[y]"
              :min="0"
            />
          </a-input-group>
        </a-form-item>
      </a-col>
      <a-col :span="12">
        <a-form-item label="offset">
          <a-input-group>
            <a-input-number v-model="form.offset[0]" placeholder="offsetLeft" />
            <a-input-number v-model="form.offset[1]" placeholder="offsetTop" />
          </a-input-group>
        </a-form-item>
      </a-col>
      <a-col :span="12">
        <a-form-item label="fontSize">
          <a-input-number v-model="form.font.fontSize" mode="button" />
        </a-form-item>
      </a-col>
      <a-col :span="12">
        <a-form-item label="zIndex">
          <a-input-number v-model="form.zIndex" mode="button" />
        </a-form-item>
      </a-col>
      <a-col :span="6">
        <a-form-item label="repeat">
          <a-switch v-model="form.repeat" />
        </a-form-item>
      </a-col>
      <a-col :span="6">
        <a-form-item label="staggered">
          <a-switch v-model="form.staggered" />
        </a-form-item>
      </a-col>
    </a-row>
  </a-form>
  <a-watermark content="arco.design" v-bind="form">
    <div style="width: 100%; border: 1px solid #e5e6eb; box-sizing: border-box">
      <a-typography-title :heading="5"> Design system </a-typography-title>
      <a-typography>
        <a-typography-paragraph>
          A design is a plan or specification for the construction of an object
          or system or for the implementation of an activity or process, or the
          result of that plan or specification in the form of a prototype,
          product or process. The verb to design expresses the process of
          developing a design.
        </a-typography-paragraph>
        <a-typography-paragraph>
          A design is a plan or specification for the construction of an object
          or system or for the implementation of an activity or process, or the
          result of that plan or specification in the form of a prototype,
          product or process. The verb to design expresses the process of
          developing a design.
        </a-typography-paragraph>
      </a-typography>
      <img
        style="position: relative; z-index: 7"
        src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/24e0dd27418d2291b65db1b21aa62254.png~tplv-uwbnlip3yd-webp.webp"
      />
    </div>
  </a-watermark>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const form = reactive({
      rotate: 0,
      gap: [50, 50],
      offset: [],
      font: { fontSize: 16 },
      zIndex: 6,
      repeat: true,
      staggered: true,
    });
    return {
      form,
    };
  },
};
</script>
```

## API

### `<watermark>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|content|Watermark text content|`string \| string[]`|`-`|
|image|Image watermark address|`string`|`-`|
|width|Watermark width|`number`|`-`|
|height|Watermark height|`number`|`-`|
|gap|Watermark spacing|`[number, number]`|`() => [90, 90]`|
|offset|The offset from the upper left corner of the container, the default is half the watermark spacing|`[number, number]`|`[gap[0]/2, gap[1]/2]`|
|rotate|Watermark rotation angle|`number`|`-22`|
|font|Watermark font style, specific parameter configuration see [WatermarkFont](#WatermarkFont)|`WatermarkFont`|`-`|
|z-index|Watermark z-index|`number`|`6`|
|alpha|Watermark opacity|`number`|`1`|
|anti-tamper|Watermark anti-tampering|`boolean`|`true`|
|grayscale|Grayscale watermark|`boolean`|`false`|
|repeat|Whether to repeat the watermark|`boolean`|`true`|
|staggered|Whether to stagger the arrangement layout|`boolean`|`true`|

### WatermarkFont

|Name|Description|Type|Default|
|---|---|---|:---:|
|color|Font color|`string`|`rgba(0, 0, 0, 0.15)`|
|fontSize|Font size|`number`|`16`|
|fontFamily|Font family|`string`|`sans-serif`|
|fontStyle|Font style|`'none' \| 'normal' \| 'italic' \| 'oblique'`|`normal`|
|textAlign|Font align|`'start' \| 'end' \| 'left' \| 'right' \| 'center'`|`center`|
|fontWeight|Font weight|`'normal' \| 'bold' \| 'bolder' \| 'lighter' \| number`|`normal`|
