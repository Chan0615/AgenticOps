---
name: arco-vue-carousel
description: "Carousel is used to display multiple pictures, videos, or embedded frames and other content in a loop, and supports automatic playback or manual switching by the user. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Carousel

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage

```vue
<template>
  <a-carousel
    :style="{
      width: '600px',
      height: '240px',
    }"
    :default-current="2"
    @change="handleChange"
  >
    <a-carousel-item v-for="image in images">
      <img
        :src="image"
        :style="{
          width: '100%',
        }"
      />
    </a-carousel-item>
  </a-carousel>
</template>

<script>
export default {
  setup() {
    const images = [
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
    ];
    const handleChange=(value)=>{
      console.log(value)
    }
    return {
      images,
      handleChange
    }
  },
};
</script>
```

## Auto

You can set whether to switch automatically through `autoPlay`.
You can set `moveSpeed`, `timingFunc` to achieve different switching slide effects.

```vue
<template>
  <a-carousel
    :style="{
      width: '600px',
      height: '240px',
    }"
    :auto-play="true"
    indicator-type="dot"
    show-arrow="hover"
  >
    <a-carousel-item v-for="image in images">
      <img
        :src="image"
        :style="{
          width: '100%',
        }"
      />
    </a-carousel-item>
  </a-carousel>
</template>

<script>
export default {
  setup() {
    const images = [
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
    ];
    return {
      images
    }
  },
};
</script>
```

## Indicator

You can specify the indicator type: `dot` | `line` | `slider` and position `left` | `right` | `top` | `bottom` | `outer`.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-radio-group
      type="button"
      @change="updateType"
      style="{ marginBottom: '10px' }"
      :modelValue="indicatorType"
    >
      <a-radio value="dot">dot</a-radio>
      <a-radio value="line">line</a-radio>
      <a-radio value="slider">slider</a-radio>
    </a-radio-group>
    <a-radio-group
      type="button"
      @change="updatePosition"
      :style="{ marginBottom: '20px' }"
      :modelValue="indicatorPosition"
    >
      <a-radio value="left">left</a-radio>
      <a-radio value="right">right</a-radio>
      <a-radio value="top">top</a-radio>
      <a-radio value="bottom">bottom</a-radio>
      <a-radio value="outer">outer</a-radio>
    </a-radio-group>
    <a-carousel
      :indicator-type="indicatorType"
      :indicator-position="indicatorPosition"
      show-arrow="never"
      :style="{
      width: '600px',
      height: '240px',
    }"
    >
      <a-carousel-item v-for="image in images">
        <img
          :src="image"
          :style="{
          width: '100%',
        }"
        />
      </a-carousel-item>
    </a-carousel>
  </a-space>
</template>

<script>
export default {
  data() {
    return {
      images: [
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
      ],
      indicatorType: 'dot',
      indicatorPosition: 'bottom',
    };
  },
  methods: {
    updateType(type) {
      this.indicatorType = type;
    },
    updatePosition(position) {
      this.indicatorPosition = position;
    },
  },
};
</script>
```

## Vertical

By default, the `direction` is `horizontal`. Use the vertical direction switch by setting the `direction` to `vertical`.

```vue
<template>
  <a-carousel
    :style="{
      width: '600px',
      height: '240px',
    }"
    show-arrow="never"
    direction="vertical"
    indicator-position="right"
  >
    <a-carousel-item v-for="image in images">
      <img
        :src="image"
        :style="{
          width: '100%',
        }"
      />
    </a-carousel-item>
  </a-carousel>
</template>

<script>
export default {
  setup() {
    const images = [
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
    ];
    return {
      images
    }
  },
};
</script>
```

## Animation Card

When the space in the width direction of the page is vacant, but the space in the height direction is surplus, you can specify `animation` as `card` to use card style.

```vue
<template>
  <a-carousel
    :autoPlay="true"
    animation-name="card"
    show-arrow="never"
    indicator-position="outer"
    :style="{
      width: '100%',
      height: '240px',
    }"
  >
    <a-carousel-item v-for="image in images" :style="{ width: '60%' }">
      <img
        :src="image"
        :style="{
          width: '100%',
        }"
      />
    </a-carousel-item>
  </a-carousel>
</template>

<script>
export default {
  setup() {
    const images = [
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/24e0dd27418d2291b65db1b21aa62254.png~tplv-uwbnlip3yd-webp.webp',
    ];
    return {
      images
    }
  },
};
</script>
```

## Animation Fade

Set `animation=fade` to use fade transition effect.

```vue
<template>
  <a-carousel
    :style="{
      width: '600px',
      height: '240px',
    }"
    :auto-play="true"
    animation-name="fade"
    show-arrow="never"
  >
    <a-carousel-item v-for="image in images">
      <img
        :src="image"
        :style="{
          width: '100%',
        }"
      />
    </a-carousel-item>
  </a-carousel>
</template>

<script>
export default {
  setup() {
    const images = [
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
    ];
    return {
      images
    }
  },
};
</script>
```

## API

### `<carousel>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|current **(v-model)**|The index of current slide which starts from 1|`number`|`-`|
|default-current|Default index of current slide|`number`|`1`|
|auto-play|@en* Whether to automatically loop the display, or pass in `{ interval: the time interval for switching (default: 3000),<br>hoverToPause: whether to pause switching while hover (default: true) }` for configuration (object is supported from `2.14.0`)|`boolean \| CarouselAutoPlayConfig`|`false`|
|move-speed|The duration of the slide movement(ms)|`number`|`500`|
|animation-name|The animation of the slide movement|`'slide' \| 'fade' \| 'card'`|`'slide'`|
|trigger|How to trigger the slide switch, click/hover the indicator|`'click' \| 'hover'`|`'click'`|
|direction|The direction of the slide movement|`'horizontal' \| 'vertical'`|`'horizontal'`|
|show-arrow|When to show the arrow used to switch|`'always' \| 'hover' \| 'never'`|`'always'`|
|arrow-class|The additional css class to arrow used to switch|`string`|`''`|
|indicator-type|Type of indicator|`'line' \| 'dot' \| 'slider' \| 'never'`|`'dot'`|
|indicator-position|Position of indication|`'bottom' \| 'top' \| 'left' \| 'right' \| 'outer'`|`'bottom'`|
|indicator-class|The additional css class to indicator|`string`|`''`|
|transition-timing-function|How intermediate values are calculated for CSS properties being affected by a transition effect.<br>[transition-timing-function](https://developer.mozilla.org/zh-CN/docs/Web/CSS/transition-timing-function)|`string`|`'cubic-bezier(0.34, 0.69, 0.1, 1)'`|
### `<carousel>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Callback when slide changes|index: `number`<br>prevIndex: `number`<br>isManual: `boolean`|
