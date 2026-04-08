---
name: arco-vue-badge
description: "Badge normally appears in the upper right corner of the icon or text to prompt important information. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Badge

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage. Just specify `count` or `content slot` to display the badge.

```vue
<template>
  <a-space :size="40">
    <a-badge :count="9">
      <a-avatar shape="square" />
    </a-badge>
    <a-badge :count="9" dot :dotStyle="{ width: '10px', height: '10px' }">
      <a-avatar shape="square" />
    </a-badge>
    <a-badge :dotStyle="{ height: '16px', width: '16px', fontSize: '14px' }">
      <template #content>
        <IconClockCircle
          :style="{ verticalAlign: 'middle', color: 'var(--color-text-2)' }"
        />
      </template>
      <a-avatar shape="square" />
    </a-badge>
  </a-space>
</template>

<script>
import { IconClockCircle } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconClockCircle },
};
</script>
```

## Standalone

Used in standalone when `default slot` is empty.

```vue
<template>
  <a-space :size="40">
    <a-badge :count="2" />
    <a-badge
      :count="2"
      :dotStyle="{ background: '#E5E6EB', color: '#86909C' }"
    />
    <a-badge :count="16" />
    <a-badge :count="1000" :max-count="99" />
  </a-space>
</template>
```

## Red Badge

A red dot will be displayed instead of the count. The dot will be showed only when `count > 0`.

```vue
<template>
  <a-space :size="40">
    <a-badge :count="9" dot :offset="[6, -2]">
      <a href="#">Link</a>
    </a-badge>
    <a-badge :count="9" dot :offset="[2, -2]">
      <IconNotification
        :style="{ color: '#888', fontSize: '18px', verticalAlign: '-3px' }"
      />
    </a-badge>
  </a-space>
</template>

<script>
import { IconNotification } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconNotification },
};
</script>
```

## Text

Customize the content.

```vue
<template>
  <a-space :size="40">
    <a-badge text="NEW">
      <a-avatar shape="square">
        <span>
          <IconUser />
        </span>
      </a-avatar>
    </a-badge>
    <a-badge text="HOT">
      <a-avatar shape="square">
        <span>
          <IconUser />
        </span>
      </a-avatar>
    </a-badge>
  </a-space>
</template>

<script>
import { IconUser } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconUser },
};
</script>
```

## Max Count

If the count is larger than `max-count`, the `${max-count}+` will be displayed. The default value of `max-count` is `99`.

```vue
<template>
  <a-space :size="40">
    <a-badge :max-count="10" :count="0">
      <a-avatar shape="square">
        <span>
          <IconUser />
        </span>
      </a-avatar>
    </a-badge>
    <a-badge :max-count="10" :count="100">
      <a-avatar shape="square">
        <span>
          <IconUser />
        </span>
      </a-avatar>
    </a-badge>
    <a-badge :count="100">
      <a-avatar shape="square">
        <span>
          <IconUser />
        </span>
      </a-avatar>
    </a-badge>
    <a-badge :max-count="999" :count="1000">
      <a-avatar shape="square">
        <span>
          <IconUser />
        </span>
      </a-avatar>
    </a-badge>
  </a-space>
</template>

<script>
import { IconUser } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconUser },
};
</script>
```

## Status

Different status.

```vue
<template>
  <a-space size="large" direction="vertical">
    <a-space size="large">
      <a-badge status="normal" />
      <a-badge status="processing" />
      <a-badge status="success" />
      <a-badge status="warning" />
      <a-badge status="danger" />
    </a-space>
    <a-space size="large">
      <a-badge status="normal" text="Normal" />
      <a-badge status="processing" text="Processing" />
      <a-badge status="success" text="Success" />
      <a-badge status="warning" text="Warning" />
      <a-badge status="danger" text="Danger" />
    </a-space>
  </a-space>
</template>
```

## Color

We provide a variety of preset colors for the badge. And you can also set a custom color by the color property.

```vue
<template>
  <div>
    <a-badge
      v-for="color in colors"
      :key="color"
      :color="color"
      :text="color"
      :style="{ marginRight: '24px' }"
    />
  </div>
  <br />
  <div>
    <a-badge
      v-for="color in customColors"
      :key="color"
      :color="color"
      :text="color"
      :style="{ marginRight: '24px' }"
    />
  </div>
</template>

<script>
const COLORS = [
  'red',
  'orangered',
  'orange',
  'gold',
  'lime',
  'green',
  'cyan',
  'arcoblue',
  'purple',
  'pinkpurple',
  'magenta',
  'gray',
];

const COLORS_CUSTOM = [
  '#F53F3F',
  '#7816FF',
  '#00B42A',
  '#165DFF',
  '#FF7D00',
  '#EB0AA4',
  '#7BC616',
  '#86909C',
  '#B71DE8',
  '#0FC6C2',
  '#FFB400',
  '#168CFF',
  '#FF5722',
];
export default {
  data() {
    return {
      colors: COLORS,
      customColors: COLORS_CUSTOM,
    };
  },
};
</script>
```

## API

### `<badge>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|text|Set the display text of the status dot|`string`|`-`|
|dot|Whether to display a red dot instead of `count`|`boolean`|`false`|
|dot-style|Customize badge dot style|`object`|`-`|
|max-count|Max count to show. If count is larger than this value, it will be displayed as `${maxCount}+`|`number`|`99`|
|offset|Set offset of the badge dot|`number[]`|`[]`|
|color|Customize dot color|`ColorType \| string`|`-`|
|status|Badge status|`'normal' \| 'processing' \| 'success' \| 'warning' \| 'danger'`|`-`|
|count|Number to show in badge|`number`|`-`|
