---
name: arco-vue-message
description: "Lightweight global feedback triggered by user actions. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Message

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of message.

```vue
<template>
  <a-button @click="handleClick">Info Message</a-button>
</template>

<script>
export default {
  methods: {
    handleClick() {
      this.$message.info('This is an info message')
    }
  }
};
</script>
```

## Message Type

There are 6 different types of global prompts, namely: `info`, `success`, `warning`, `error`, `loading`. Version 2.41.0 adds the `normal` type, which has no icon by default.

```vue

<template>
  <div>
    <a-space>
      <a-button @click="()=>this.$message.info('This is an info message!')">Info Message</a-button>
      <a-button @click="()=>this.$message.success('This is a success message!')" status="success">Success Message
      </a-button>
      <a-button @click="()=>this.$message.warning('This is a warning message!')" status="warning">Warning Message
      </a-button>
      <a-button @click="()=>this.$message.error('This is an error message!')" status="danger">Error Message</a-button>
    </a-space>
  </div>
  <div style="margin-top: 20px">
    <a-space>
      <a-button @click="()=>this.$message.normal('This is a normal message!')">Normal Message</a-button>
      <a-button @click="()=>this.$message.normal({
    content:'This is a normal message!',
    icon:renderIcon
    })">Normal Message With Icon
      </a-button>
      <a-button @click="()=>this.$message.loading('This is a loading message!')" status="primary">Loading Message
      </a-button>
    </a-space>
  </div>
</template>

<script>
import { h } from 'vue';
import { IconExclamationCircleFill } from '@arco-design/web-vue/es/icon';

export default {
  setup() {
    const renderIcon = () => h(IconExclamationCircleFill);
    return {
      renderIcon
    }
  }
};
</script>
```

## Custom icon

Set `icon` to customize the icon.

```vue
<template>
  <a-button @click="handleClick">Info Message</a-button>
</template>

<script>
import { h } from 'vue';
import { IconFaceSmileFill } from '@arco-design/web-vue/es/icon';

export default {
  methods: {
    handleClick() {
      this.$message.info({
        content: 'This is an info message!',
        icon: () => h(IconFaceSmileFill)
      });
    }
  }
}
</script>
```

## Position

The prompt has 2 different pop-up positions, namely the top and the bottom.

```vue
<template>
  <a-space>
    <a-button @click="()=>this.$message.info({content:'This is an info message!'})">Top Message</a-button>
    <a-button @click="()=>this.$message.info({content:'This is an info message!',position:'bottom'})">Bottom Message</a-button>
  </a-space>
</template>
```

## Closeable

Set `closable` to show the close button.

```vue
<template>
  <a-button @click="handleClick">Closeable Message</a-button>
</template>

<script>
export default {
  methods: {
    handleClick(){
      this.$message.info({
        content:'This is an info message!',
        closable: true
      })
    }
  }
};
</script>
```

## Update content

Update the message content and reset the timer by setting the `duration` property.

```vue
<template>
  <a-button @click="handleClick">Update Info Message</a-button>
</template>

<script>
export default {
  data() {
    return {
      index: 0
    }
  },
  methods: {
    handleClick() {
      this.$message.info({
        id: 'myInfo',
        content: `This is an info message ${this.$data.index++}`,
        duration: 2000
      })
    }
  }
};
</script>
```

### `Message` Global methods

The global methods provided by Message can be used in the following three ways:
1. Called by this.$message
2. In the Composition API, call getCurrentInstance().appContext.config.globalProperties.$message
3. Import Message and call it through Message itself

When used by import, the component has no way to obtain the current Vue Context. Content injected into the AppContext such as i18n or route cannot be used internally. You need to manually pass in the AppContext when calling, or specify the AppContext globally for the component.

```ts
import { createApp } from 'vue'
import { Message } from '@arco-design/web-vue';

const app = createApp(App);
Message._context = app._context;
````

### MessageMethod

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|info|Show info message|`(    config: string \| MessageConfig,    appContext?: AppContext  ) => MessageReturn`|`-`||
|success|Show success message|`(    config: string \| MessageConfig,    appContext?: AppContext  ) => MessageReturn`|`-`||
|warning|Show warning message|`(    config: string \| MessageConfig,    appContext?: AppContext  ) => MessageReturn`|`-`||
|error|Show error message|`(    config: string \| MessageConfig,    appContext?: AppContext  ) => MessageReturn`|`-`||
|loading|Show loading message|`(    config: string \| MessageConfig,    appContext?: AppContext  ) => MessageReturn`|`-`||
|normal|Show message|`(    config: string \| MessageConfig,    appContext?: AppContext  ) => MessageReturn`|`-`|2.41.0|
|clear|Clear all messages|`(position?: MessagePosition) => void`|`-`||

### MessageConfig

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|content|Content|`RenderContent`|`-`||
|id|Unique id|`string`|`-`||
|icon|Message icon|`RenderFunction`|`-`||
|position|Location of the message|`'top'\|'bottom'`|`-`||
|showIcon|Whether to show icon|`boolean`|`false`||
|closable|Whether to show the close button|`boolean`|`false`||
|duration|The duration of the message display|`number`|`-`||
|onClose|Callback function when closing|`(id: number \| string) => void`|`-`||
|resetOnHover|The mouse to move into the component will not automatically close|`boolean`|`false`|2.39.0|

### MessageReturn

|Name|Description|Type|Default|
|---|---|---|:---:|
|close|Close current message|`() => void`|`-`|
