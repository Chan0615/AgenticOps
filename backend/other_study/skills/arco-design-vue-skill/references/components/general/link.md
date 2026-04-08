---
name: arco-vue-link
description: "The basic style of the link. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Link

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of link.

```vue
<template>
  <a-space>
    <a-link href="link">Link</a-link>
    <a-link href="link" disabled>Link</a-link>
  </a-space>
</template>
```

## Status

The link status is divided into four types: `normal` (default), `success`, `warning` and `danger`.

```vue
<template>
  <a-space direction="vertical">
    <a-space>
      <a-link href="link">Normal Link</a-link>
      <a-link href="link" disabled>Normal Link</a-link>
    </a-space>
    <a-space>
      <a-link href="link" status="success">Success Link</a-link>
      <a-link href="link" status="success" disabled>Success Link</a-link>
    </a-space>
    <a-space>
      <a-link href="link" status="warning">Warning Link</a-link>
      <a-link href="link" status="warning" disabled>Warning Link</a-link>
    </a-space>
    <a-space>
      <a-link href="link" status="danger">Danger Link</a-link>
      <a-link href="link" status="danger" disabled>Danger Link</a-link>
    </a-space>
  </a-space>
</template>
```

## hoverable

You can use the hoverable property to set whether to hide the background color of the Link component when it is hovering.

```vue
<template>
  <a-space>
    <a-link href="link" :hoverable="false">Link</a-link>
    <a-link href="link" status="danger" :hoverable="false">Link</a-link>
  </a-space>
</template>
```

## Icon

Customize icon node. If true, the default icon will be displayed.

```vue
<template>
  <div>
    <a-space>
      <a-link href="link" icon>Link</a-link>
      <a-link href="link" disabled icon>Link</a-link>
    </a-space>
  </div>
  <div>
    <a-space>
      <a-link href="link">
        <template #icon>
          <icon-edit />
        </template>
        Link
      </a-link>
      <a-link href="link" disabled>
        <template #icon>
          <icon-edit />
        </template>
        Link
      </a-link>
    </a-space>
  </div>
</template>

<script>
  import { IconEdit } from '@arco-design/web-vue/es/icon';

  export default {
    components: { IconEdit }
  };
</script>
```

## Loading

The link can be in the loading state by setting `loading`. The link in the loading state will not trigger the `click` event.

```vue
<template>
  <a-space>
    <a-link loading>Link</a-link>
    <a-link :loading="loading1" @click="handleClick1">Link</a-link>
    <a-link :loading="loading2" @click="handleClick2">
      <template #icon>
        <icon-edit />
      </template>
      Link
    </a-link>
  </a-space>
</template>

<script>
import { ref } from 'vue';
import { IconEdit } from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconEdit,
  },
  setup() {
    const loading1 = ref(false);
    const loading2 = ref(false);

    const handleClick1 = () => {
      loading1.value = true;
      setTimeout(() => {
        loading1.value = false;
      }, 3000);
    }
    const handleClick2 = () => {
      loading2.value = true;
      setTimeout(() => {
        loading2.value = false;
      }, 3000);
    }

    return {
      loading1,
      loading2,
      handleClick1,
      handleClick2,
    };
  }
}
</script>
```

## API

### `<link>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|href|Link address|`string`|`-`||
|status|Link status|`'normal' \| 'warning' \| 'success' \| 'danger'`|`'normal'`||
|hoverable|Whether to hide background when hover|`boolean`|`true`|2.7.0|
|icon|icon|`boolean`|`false`|2.7.0|
|loading|Whether the link is in the loading state|`boolean`|`false`|2.37.0|
|disabled|Whether the link is disabled|`boolean`|`false`||
### `<link>` Events

|Event Name|Description|Parameters|
|---|---|---|
|click|Emitted when the link is clicked|ev: `MouseEvent`|
