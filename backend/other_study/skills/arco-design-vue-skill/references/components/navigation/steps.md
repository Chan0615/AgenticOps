---
name: arco-vue-steps
description: "Clearly indicate the task flow and the current degree of completion, and guide the user to follow the steps to complete the task. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Steps

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of the step bar.

```vue
<template>
  <div>
    <a-steps :current="2">
      <a-step>Succeeded</a-step>
      <a-step>Processing</a-step>
      <a-step>Pending</a-step>
    </a-steps>
    <a-divider/>
    <div style="line-height: 140px; text-align: center; color: #C9CDD4; ">
      Step 2 Content
    </div>
  </div>
</template>
```

## Description

Descriptive information can be added by setting `description`.

```vue
<template>
  <a-steps>
    <a-step description="This is a description">Succeeded</a-step>
    <a-step description="This is a description">Processing</a-step>
    <a-step description="This is a description">Pending</a-step>
  </a-steps>
</template>
```

## Label Placement

The placement of label description text can be changed by setting `label-placement`. There are two types of placement: `horizontal` - **placed on the right side of the icon (default)** and `vertical` - **placed below the icon**.

```vue
<template>
  <a-steps label-placement="vertical">
    <a-step description="This is a description">Succeeded</a-step>
    <a-step description="This is a description">Processing</a-step>
    <a-step description="This is a description">Pending</a-step>
  </a-steps>
</template>
```

## Error Status

Display the error status by setting `status="error"`.

```vue
<template>
  <a-steps :current="2" status="error">
    <a-step description="This is a description">Succeeded</a-step>
    <a-step description="This is a description">Error</a-step>
    <a-step description="This is a description">Pending</a-step>
  </a-steps>
</template>
```

## Custom Icon

The node icon can be customized through the `#icon` slot.

```vue
<template>
  <a-steps>
    <a-step description="This is a description">
      Succeeded
      <template #icon>
        <icon-home/>
      </template>
    </a-step>
    <a-step description="This is a description">
      Processing
      <template #icon>
        <icon-loading/>
      </template>
    </a-step>
    <a-step description="This is a description">
      Pending
      <template #icon>
        <icon-thumb-up/>
      </template>
    </a-step>
  </a-steps>
</template>
```

## Line Less

You can use the connectionless mode by setting `line-less`.

```vue
<template>
  <a-steps :current="2" line-less>
    <a-step description="This is a description">Succeeded</a-step>
    <a-step description="This is a description">Processing</a-step>
    <a-step description="This is a description">Pending</a-step>
  </a-steps>
</template>
```

## Vertical Steps

Vertical step bar.

```vue
<template>
  <div class="frame-bg">
    <div class="frame-body">
      <div class="frame-aside">
        <a-steps :current="current" direction="vertical">
          <a-step>Succeeded</a-step>
          <a-step>Processing</a-step>
          <a-step>Pending</a-step>
        </a-steps>
      </div>
      <div class="frame-main">
        <div class="main-content">The content of this step.</div>
        <div class="main-bottom">
          <a-button :disabled="current===1" @click="onPrev">
            <icon-left />
            Back
          </a-button>
          <a-button :disabled="current===3" @click="onNext">
            Next
            <icon-right />
          </a-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const current = ref(1);

    const onPrev = () => {
      current.value = Math.max(1, current.value - 1);
    };

    const onNext = () => {
      current.value = Math.min(3, current.value + 1);
    };

    return {
      current,
      onPrev,
      onNext,
    }
  },
};
</script>

<style scoped lang="less">
.frame-bg {
  max-width: 780px;
  padding: 40px;
  background: var(--color-fill-2);
}

.frame-body {
  display: flex;
  background: var(--color-bg-2);
}

.frame-aside {
  padding: 24px;
  height: 272px;
  border-right: 1px solid var(--color-border);
}

.frame-main {
  width: 100%;
}

.main-content {
  text-align: center;
  line-height: 200px;
}

.main-bottom {
  display: flex;
  justify-content: center;

  button {
    margin: 0 20px;
  }
}
</style>
```

## Arrow Steps

By setting `type="arrow"`, you can use the arrow type step bar. **Note**: Only horizontal step bars are supported.

```vue
<template>
  <a-steps type="arrow" :current="2">
    <a-step description="This is a description">Succeeded</a-step>
    <a-step description="This is a description">Processing</a-step>
    <a-step description="This is a description">Pending</a-step>
  </a-steps>
</template>
```

## Dot Steps

By setting `type="dot"`, you can use a dotted step bar. There is no small size for this mode.

```vue
<template>
  <a-steps type="dot">
    <a-step>Succeeded</a-step>
    <a-step>Processing</a-step>
    <a-step>Pending</a-step>
  </a-steps>
</template>
```

## Navigation Steps

Display the step bar of navigation type by setting `type="navigation"`.

```vue
<template>
  <a-steps type="navigation">
    <a-step>Succeeded</a-step>
    <a-step>Processing</a-step>
    <a-step>Pending</a-step>
  </a-steps>
</template>
```

## Changeable

Set `changeable` to enable the click switch step.

```vue
<template>
  <div>
    <a-steps changeable :current="current" @change="setCurrent">
      <a-step description="This is a description">Succeeded</a-step>
      <a-step description="This is a description">Processing</a-step>
      <a-step description="This is a description">Pending</a-step>
    </a-steps>
    <div :style="{
          width: '100%',
          height: '200px',
          textAlign: 'center',
          background: 'var(--color-bg-2)',
          color: '#C2C7CC',
        }">
      <div style="line-height: 160px;">Step{{current}} Content</div>
      <a-space size="large">
        <a-button type="secondary" :disabled="current <= 1" @click="onPrev">
          <IconLeft/> Back
        </a-button>
        <a-button type="primary" :disabled="current >= 3" @click="onNext">
          Next <IconRight/>
        </a-button>
      </a-space>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      current: 1,
    };
  },
  methods: {
    onPrev() {
      this.current = Math.max(1, this.current - 1)
    },

    onNext() {
      this.current = Math.min(3, this.current + 1)
    },

    setCurrent(current) {
      this.current = current
    }
  }
};
</script>
```

## API

### `<steps>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|type|The type of the steps|`'default' \| 'arrow' \| 'dot' \| 'navigation'`|`'default'`|
|direction|The direction of the steps|`'horizontal' \| 'vertical'`|`'horizontal'`|
|label-placement|The location where the label description is placed.|`'horizontal' \| 'vertical'`|`'horizontal'`|
|current **(v-model)**|Number of current step|`number`|`-`|
|default-current|The default number of step (uncontrolled state)|`number`|`1`|
|status|The status of the current step|`'wait' \| 'process' \| 'finish' \| 'error'`|`'process'`|
|line-less|Whether to use the connectionless style|`boolean`|`false`|
|small|Whether to use a small step bar|`boolean`|`false`|
|changeable|Whether you can click to switch|`boolean`|`false`|
### `<steps>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when the number of steps changes|step: `number`<br>ev: `Event`|

### `<step>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|title|Title of the step|`string`|`-`|
|description|Description of the step|`string`|`-`|
|status|Status of the step|`'wait' \| 'process' \| 'finish' \| 'error'`|`-`|
|disabled|Whether to disable|`boolean`|`false`|
### `<step>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|node|Node|step: `number`<br>status: `string`|
|icon|Icon|step: `number`<br>status: `string`|
|description|Description|-|
