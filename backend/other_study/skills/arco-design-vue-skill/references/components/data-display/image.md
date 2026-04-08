---
name: arco-vue-image
description: "Used to show and preview pictures. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Image

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

When you need to view a picture, simply set the `src` property to get a component with preview picture function.

```vue
<template>
  <a-image
    width="200"
    src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp"
  />
</template>
```

## Show Caption

By setting title and description, the title and description of the picture can be displayed inside or at the bottom of the picture, and the display position is controlled by footerPosition.

```vue
<template>
  <a-image
    width="200px"
    :src="src"
    :title="title"
    :description="description"
  />
  <a-image
    width="200px"
    :src="src"
    :title="title"
    :description="description"
    footerPosition="outer"
    style="margin-left: 67px; vertical-align: top;"
  />
</template>

<script>
export default {
  setup() {
    return {
      src: 'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp',
      title: 'A user’s avatar',
      description: 'Present by Arco Design',
    }
  }
}
</script>
```

## Extra Operations

The component provides a named slot `extra` for users to customize additional content in the footer.

```vue
<template>
  <a-image
    src='https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp'
    title='A user’s avatar'
    description='Present by Arco Design'
    width="260"
    style="margin-right: 67px; vertical-align: top;"
    :preview-visible="visible1"
    @preview-visible-change="() => { visible1= false }"
  >
    <template #extra>
      <div class="actions">
        <span class="action" @click="() => { visible1 = true }"><icon-eye /></span>
        <span class="action" @click="onDownLoad"><icon-download /></span>
        <a-tooltip content="A user’s avatar">
          <span class="action"><icon-info-circle /></span>
        </a-tooltip>
      </div>
    </template>
  </a-image>
  <a-image
    src='https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp'
    title='A user’s avatar'
    description='Present by Arco Design'
    width="260"
    footer-position="outer"
    :preview-visible="visible2"
    @preview-visible-change="() => { visible2 = false }"
  >
    <template #extra>
      <div class="actions actions-outer">
        <span class="action" @click="() => { visible2 = true }"><icon-eye /></span>
        <span class="action" @click="onDownLoad"><icon-download /></span>
        <a-tooltip content="A user’s avatar">
          <span class="action"><icon-info-circle /></span>
        </a-tooltip>
      </div>
    </template>
  </a-image>
</template>
<script>
  import { ref } from 'vue';
  import { IconEye, IconDownload, IconInfoCircle } from '@arco-design/web-vue/es/icon';

  export default {
    components: {
      IconEye, IconDownload, IconInfoCircle
    },
    setup() {
      const visible1 = ref(false);
      const visible2 = ref(false);

      return {
        visible1,
        visible2,
        onDownLoad() {
          console.log('download');
        },
      }
    }
  }
</script>
<style scoped>
  .actions {
    display: flex;
    align-items: center;
  }
  .action {
    padding: 5px 4px;
    font-size: 14px;
    margin-left: 12px;
    border-radius: 2px;
    line-height: 1;
    cursor: pointer;
  }
  .action:first-child {
    margin-left: 0;
  }

  .action:hover {
    background: rgba(0,0,0,.5);
  }
  .actions-outer {
    .action {
      &:hover {
        color: #ffffff;
      }
    }
  }
</style>
```

## Error state

Content displayed when the image fails to load.

```vue
<template>
  <a-space :size="20">
    <a-image
      width="400"
      height="300"
      src="some-error.png"
    />
    <a-image
      width="400"
      height="300"
      src="some-error.png"
      alt="This is a picture of humans eating ice cream. The humans on the screen are very happy just now. The ice cream is green, it seems to be flavored with matcha. The gender of the human is unknown. It has very long hair and the human hair is brown."
    />
  </a-space>
</template>
```

## Loading

By default, the loading effect is not displayed, and the default loading effect can be displayed by setting `showLoader` to `true`. If the default loading effect does not meet the requirements, you can also set the loading style yourself through the named slot `loader`.

Loading

```vue
<template>
  <div>
    <a-button
      type="primary"
      @click="() => {timestamp = Date.now()}"
      style="margin-bottom: 20px;"
    >
      reload
    </a-button>
  </div>
  <a-image
    width="200"
    height="200"
    :src="`https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp?timestamp=${timestamp}`"
    show-loader
  />
  <a-image
    width="200"
    height="200"
    :src="`https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp?timestamp=${timestamp}`"
    style="marginLeft: 67px"
  >
    <template #loader>
      <div class="loader-animate"/>
    </template>
  </a-image>
</template>
<script>
  import { ref } from 'vue';
  export default {
    setup() {
      const timestamp = ref('');
      return {
        timestamp,
      }
    }
  }
</script>
<style scoped>
  .loader-animate {
    width: 100%;
    height: 100%;
    background: linear-gradient(
      -60deg,
      var(--color-fill-2) 25%,
      var(--color-neutral-3) 40%,
      var(--color-fill-3) 55%
    );
    background-size: 400% 100%;
    animation: loop-circle 1.5s cubic-bezier(0.34, 0.69, 0.1, 1) infinite;
  }

  @keyframes loop-circle {
    0% {
      background-position: 100% 50%;
    }

    100% {
      background-position: 0 50%;
    }
  }
</style>
```

## Progressive Loading

When you need to display a large image, you can pass a smaller image to `loader` to display it when the original image is not successfully loaded to simulate progressive loading.

```vue
<template>
  <div>
    <a-button
      type="primary"
      @click="() => {timestamp = Date.now()}"
      style="margin-bottom: 20px;"
    >
      reload
    </a-button>
  </div>
  <a-image
    width="200"
    height="200"
    :src="`https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp?timestamp=${timestamp}`"
  >
    <template #loader>
      <img
        width="200"
        src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp"
        style="filter: blur(5px);"
      />
    </template>
  </a-image>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const timestamp = ref('');
    return {
      timestamp,
    }
  }
}
</script>
```

## Preview action bar

The function buttons on the control preview control bar can be sorted and filtered through `actionLayout`.
In addition, starting from `2.17.0`, the preview component `a-image-preview` provides the `actions` slot to support custom additional action items, and also provides the action item component `a-image-preview-action` .

```vue
<template>
  <a-image
    width="200"
    src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp"
    :preview-props="{
      actionsLayout: ['rotateRight', 'zoomIn', 'zoomOut'],
    }"
  >
    <template #preview-actions>
      <a-image-preview-action name="download" @click="download"><icon-download /></a-image-preview-action>
    </template>
  </a-image>
</template>

<script>
export default {
  setup() {
    const download = () => {
      console.log('download image')
    };

    return {
      download
    }
  },
}
</script>
```

## Multi-image preview

Use `<a-image-preview-group>` to wrap the `<a-image>` component to preview multiple images.

```vue
<template>
  <a-image-preview-group infinite>
    <a-space>
      <a-image src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp" width="200" />
      <a-image src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp" width="200" />
      <a-image src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp" width="200" />
      <a-image src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/24e0dd27418d2291b65db1b21aa62254.png~tplv-uwbnlip3yd-webp.webp" width="200" />
    </a-space>
  </a-image-preview-group>
</template>
```

## Use Preview alone

`a-image-preview` can be used alone, you need to control `visible`.

```vue
<template>
  <a-button type="primary" @click="onClick">Click me to preview image</a-button>
  <a-image-preview
    src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp"
    v-model:visible="visible"
  />
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const visible = ref(false)
    const onClick = () => {
      visible.value = true;
    };

    return {
      visible,
      onClick,
    };
  },
};
</script>
```

## Use PreviewGroup alone

`<a-image-preview-group>` can be used alone, you need to control `visible` by yourself. The image display is divided into two scenes: First, the first image to be displayed can be specified by `defaultCurrent`. Second, to control which image is currently displayed by `current`.

```vue
<template>
  <a-button type="primary" @click="onClick">Click me to preview multiple image</a-button>
  <a-image-preview-group
    v-model:visible="visible"
    v-model:current="current"
    infinite
    :srcList="[
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
      'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/24e0dd27418d2291b65db1b21aa62254.png~tplv-uwbnlip3yd-webp.webp',
    ]"
  />
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const visible = ref(false)
    const current = ref(3);
    const onClick = () => {
      visible.value = true;
    };

    return {
      visible,
      current,
      onClick,
    };
  },
}
</script>
```

## Popup Container

You can specify the parent node of the preview mounted by `popupContainer`.

```vue
<template>
  <div
    id="image-demo-preview-popup-container"
    :style="{
      width: '100%',
      height: '400px',
      backgroundColor: 'var(--color-fill-2)',
      position: 'relative',
      overflow: 'hidden',
      lineHeight: '400px',
      textAlign: 'center',
    }"
  >
    <a-image
      width="200"
      src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp"
      :preview-props="{
        popupContainer: '#image-demo-preview-popup-container',
        closable: false,
      }"
    />
  </div>
</template>
```

## API

### `<image>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|src|Image src|`string`|`-`||
|width|Image width|`string \| number`|`-`||
|height|Image height|`string \| number`|`-`||
|title|Title|`string`|`-`||
|description|Description, will be displayed at the bottom. if alt has no value, it will be set to alt|`string`|`-`||
|fit|indicate how the image should be resized to fit its container|`'contain' \| 'cover' \| 'fill' \| 'none' \| 'scale-down'`|`-`||
|alt|Text description of the image|`string`|`-`||
|hide-footer|Whether to hide footer (Version 2.36.0 supports the 'never' parameter, which supports displaying bottom content when loading errors)|`boolean \| 'never'`|`false`||
|footer-position|The position shown at the bottom|`'inner' \| 'outer'`|`'inner'`||
|show-loader|Whether to show the loading effect|`boolean`|`false`||
|preview|Whether to enable preview|`boolean`|`true`||
|preview-visible **(v-model)**|Control the open state of the preview, can be used in conjunction with previewVisibleChange|`boolean`|`-`||
|default-preview-visible|The default open state of the preview|`boolean`|`false`||
|preview-props|Preview configuration items (all options are optional) [ImagePreviewProps](#image-preview%20Props)|`ImagePreviewProps`|`-`||
|footer-class|The class name of the bottom display area|`string\|array\|object`|`-`|2.23.0|
### `<image>` Events

|Event Name|Description|Parameters|
|---|---|---|
|preview-visible-change|Preview opening and closing events|visible: `boolean`|
### `<image>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|error|Customize error content.|-|
|error-icon|Customize the icon of error content.|-|
|loader|Customize loading effect.|-|
|extra|Extra content at the bottom|-|

### `<image-preview>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|src|Image src|`string`|`-`|
|visible **(v-model)**|Whether is visible|`boolean`|`-`|
|default-visible|Default visibility|`boolean`|`false`|
|mask-closable|Whether to close the modal when mask is clicked|`boolean`|`true`|
|closable|Whether to show close button|`boolean`|`true`|
|actions-layout|Layout of action list|`string[]`|`[  'fullScreen',  'rotateRight',  'rotateLeft',  'zoomIn',  'zoomOut',  'originalSize',]`|
|popup-container|Set the mount point of the pop-up box, the same as the `to` of `teleport`, the default value is document.body|`HTMLElement \| string`|`-`|
|esc-to-close|Whether to support the ESC key to close the preview|`boolean`|`true`|
|wheel-zoom|Whether to enable wheel zoom|`boolean`|`true`|
|keyboard|Whether to enable keyboard shortcuts|`boolean`|`true`|
|default-scale|Default scale|`number`|`1`|
|zoom-rate|Zoom rate, only for scroll zoom|`number`|`1.1`|
### `<image-preview>` Events

|Event Name|Description|Parameters|
|---|---|---|
|close|Close event|-|
### `<image-preview>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|actions|Customize additional action items|-|2.17.0|

### `<image-preview-group>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|src-list|Picture list (after setting this property, the picture information of a-image subcomponent will no longer be collected)|`string[]`|`-`|
|current **(v-model)**|The index of the currently displayed image|`number`|`-`|
|default-current|The index of the first image shown|`number`|`0`|
|infinite|Whether to loop infinitely|`boolean`|`false`|
|visible **(v-model)**|Whether is visible|`boolean`|`-`|
|default-visible|Default visibility|`boolean`|`false`|
|mask-closable|Whether to close the modal when mask is clicked|`boolean`|`true`|
|closable|Whether to show close button|`boolean`|`true`|
|actions-layout|Layout of action list|`string[]`|`[  'fullScreen',  'rotateRight',  'rotateLeft',  'zoomIn',  'zoomOut',  'originalSize',]`|
|popup-container|Set the mount point of the pop-up box, the same as the `to` of `teleport`, the default value is document.body|`string \| HTMLElement`|`-`|
### `<image-preview-group>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Image switch|index: `number`|
|visible-change|Preview visibility change|visible: `boolean`|
### `<image-preview-group>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|actions|Customize additional action items|-|2.46.0|

### `<image-preview-action>` Props (2.17.0)

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|name|the name of the action|`string`|`-`|
|disabled|Whether to disable the action|`boolean`|`false`|

## FAQ

### Property Description for `image-preview`

**1. Keyboard Shortcuts - `keyboard`**
Setting this property to `true` enables corresponding keyboard shortcuts based on the `actions-layout` settings.

- `esc`: Close preview
- `left`: Switch to the previous image
- `right`: Switch to the next image
- `up`: Zoom in on the image
- `down`: Zoom out on the image
- `space`: Restore to original size

**2. Default Scaling - `defaultScale`**
This property defines the default scaling factor for images. For instance, when set to 1.5, images will be enlarged by 1.5 times their original size by default.

**3. Scroll Zoom Rate - `zoomSate`**
The `zoomSate` property controls the scaling rate of images during scrolling. Taking 1.3 as an example, each scrolling action will result in an image zoom-in or zoom-out by a factor of 1.3.
