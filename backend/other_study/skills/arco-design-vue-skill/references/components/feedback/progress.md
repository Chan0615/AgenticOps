---
name: arco-vue-progress
description: "Give users feedback on the running status of tasks in the current system execution, which is mostly used in scenes that run for a period of time, effectively reducing the anxiety of users during waiting. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Progress

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Simple progress bar.

```vue
<template>
  <a-progress :percent="0.2" :style="{width:'50%'}" />
  <br/>
  <br/>
  <a-progress :percent="0.3" :style="{width:'50%'}">
    <template v-slot:text="scope" >
      Progress {{ scope.percent * 100 }}%
    </template>
  </a-progress>
</template>
```

## Progress Status

Specify the status of the progress bar through `status`

```vue
<template>
  <a-space direction="vertical" :style="{width: '50%'}">
    <a-progress :percent="percent" />
    <a-progress status='warning' :percent="percent" />
    <a-progress status='danger' :percent="percent" />
  </a-space>
  <div :style="{marginTop:'20px'}">
    <a-slider v-model="percent" :max="1" :step="0.1" :style="{width: '150px'}" />
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const percent = ref(0.2);

    return {
      percent
    }
  },
}
</script>
```

## Circle Progress

Setting `type="circle"` will show a circular progress bar.

```vue

<template>
  <a-space size="large">
    <a-progress type="circle" :percent="percent" />
    <a-progress type="circle" status='warning' :percent="percent" />
    <a-progress type="circle" status='danger' :percent="percent" />
    <a-progress type="circle" status='success' :percent="percent" />
  </a-space>
  <div :style="{marginTop:'20px'}">
    <a-slider v-model="percent" :max="1" :step="0.1" :style="{width: '150px'}" />
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const percent = ref(0.2);

    return {
      percent
    }
  },
}
</script>
```

## Mini Progress

Set `size="mini"` to display a miniature progress bar.

```vue
<template>
  <a-space size="large" :style="{width: '100%'}">
    <a-progress size="mini" :percent="percent"/>
    <a-progress size="mini" status='warning' :percent="percent"/>
    <a-progress size="mini" status='danger' :percent="percent"/>
    <a-progress size="mini" status='success' :percent="percent"/>
  </a-space>
  <a-space size="large" :style="{width: '100%', marginTop: '20px'}">
    <a-progress type="circle" size="mini" :percent="percent"/>
    <a-progress type="circle" size="mini" status='warning' :percent="percent"/>
    <a-progress type="circle" size="mini" status='danger' :percent="percent"/>
    <a-progress type="circle" size="mini" status='success' :percent="percent"/>
  </a-space>
  <div :style="{marginTop: '20px'}">
    <a-slider v-model="percent" :max="1" :step="0.1" :style="{width: '150px'}" />
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const percent = ref(0.2);

    return {
      percent
    }
  },
}
</script>
```

## Progress Size

Set the size of the progress bar through `size`

```vue
<template>
  <a-space direction="vertical" size="large" :style="{width:'50%'}">
    <a-radio-group v-model="size" type="button">
      <a-radio value="small">Small</a-radio>
      <a-radio value="medium">Medium</a-radio>
      <a-radio value="large">Large</a-radio>
    </a-radio-group>
    <a-progress :size="size" :percent="0.2"/>
    <a-progress status='warning' :size="size" :percent="0.2"/>
    <a-progress status='danger' :size="size" :percent="0.2"/>
    <a-space>
      <a-progress type="circle" :size="size" :percent="0.2"/>
      <a-progress type="circle" status='warning' :size="size" :percent="0.2"/>
      <a-progress type="circle" status='danger' :size="size" :percent="0.2"/>
    </a-space>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    return {
      size: ref('medium')
    }
  }
}
</script>
```

## linear-gradient

linear-gradient progress bar.

```vue
<template>
  <div>
    <a-progress
      :percent="0.8"
      :style="{ width: '50%' }"
      :color="{
        '0%': 'rgb(var(--primary-6))',
        '100%': 'rgb(var(--success-6))',
      }"
    />
    <br/>
    <br/>

    <a-progress
      :percent="1"
      :style="{ width: '50%' }"
      :color="{
        '0%': 'rgb(var(--primary-6))',
        '100%': 'rgb(var(--success-6))',
      }"
    />
    <br/>
    <br/>
    <a-space size="large">
      <a-progress
        type="circle"
        :percent="0.8"
        :style="{ width: '50%' }"
        :color="{
          '0%': 'rgb(var(--primary-6))',
          '100%': 'rgb(var(--success-6))',
        }"
      />

      <a-progress
        type="circle"
        :percent="1"
        :style="{ width: '50%' }"
        :color="{
          '0%': 'rgb(var(--primary-6))',
          '100%': 'rgb(var(--success-6))',
        }"
      />
    </a-space>
  </div>
</template>
```

## Steps Progress

Show the step progress bar by setting `steps`.

```vue
<template>
  <div :style="{ width: '50%' }">
    <a-progress :steps="3" :percent="0.3" />
    <a-progress :steps="5" status="warning" :percent="1" />
    <a-progress :steps="3" size="small" :percent="0.3" />
  </div>
</template>
```

## trackColor

You can use 'trackColor' to set the color of the remaining progress bar.

```vue
<template>
  <div :style="{ width: '50%' }">
    <a-progress
      :percent="0.4"
      trackColor="var(--color-primary-light-1)"
      style="margin-bottom: 20px;"
    />
    <a-progress
      :percent="0.4"
      :steps="4"
      trackColor="var(--color-primary-light-1)"
      style="margin-bottom: 20px;"
    />
    <a-progress
      :percent="0.4"
      type="circle"
      trackColor="var(--color-primary-light-1)"
      style="margin-bottom: 20px;"
    />
  </div>
</template>
```

## API

### `<progress>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|type|The type of progress bar|`'line' \| 'circle'`|`'line'`|
|size|The size of the progress bar|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`|
|percent|The current percentage of the progress bar|`number`|`0`|
|steps|Turn on the step bar mode and set the number of steps|`number`|`0`|
|animation|Whether to turn on the transition animation|`boolean`|`false`|
|stroke-width|The line width of the progress bar|`number`|`-`|
|width|The width of the progress bar|`number\|string`|`-`|
|color|The color of the progress bar|`string\|object`|`-`|
|track-color|The color of the progress track|`string`|`-`|
|show-text|Whether to display text|`boolean`|`true`|
|status|Progress bar status|`'normal' \| 'success' \| 'warning' \| 'danger'`|`-`|
