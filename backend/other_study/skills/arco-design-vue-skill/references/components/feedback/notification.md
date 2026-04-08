---
name: arco-vue-notification
description: "Globally display notification reminders to convey information to users in a timely and effective manner. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Notification

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.
> Advanced `Notification.footer`, `closeIcon`, and `closeIconElement` demos use Vue JSX render content.
> If the project avoids JSX, translate those snippets to `h()` render functions or small wrapper components.

## Basic Usage

Basic usage of notification.

```vue
<template>
  <a-space>
    <a-button type="primary" @click="() => this.$notification.info({
      title:'Notification',
      content:'This is a notification!'
    })"
    >
      Open Notification
    </a-button>
    <a-button @click="handleNotification">
      Open Notification
    </a-button>
  </a-space>
</template>

<script>
import { Notification } from '@arco-design/web-vue';

export default {
  setup() {
    const handleNotification = () => {
      Notification.info({
        title: 'Notification',
        content: 'This is a notification!',
      })
    }

    return { handleNotification }
  }
}
</script>
```

## Notification Type

The message type of the notification.

```vue
<template>
  <a-space>
    <a-button
      type='primary'
      @click="() => this.$notification.info('This is an info message!')"
    >
      Info
    </a-button>
    <a-button
      type='primary'
      status="success"
      @click="() => this.$notification.success('This is a success message!')"
    >
      Success
    </a-button>
    <a-button
      type='primary'
      status="warning"
      @click="() => this.$notification.warning('This is a warning message!')"
    >
      Warning
    </a-button>
    <a-button
      type='primary'
      status="danger"
      @click="() => this.$notification.error('This is an error message!')"
    >
      Error
    </a-button>
    <a-button
      type='secondary'
      @click="() => this.$notification.info({
        content: 'This is an error message!',
        showIcon: false
      })"
    >
      Normal
    </a-button>
  </a-space>
</template>
```

## Position

Notification has 4 different positions, `Top Left`, `Top Right (default)`, `Bottom Left`, `Bottom Right`.

```vue
<template>
  <a-space>
    <a-button type="primary" @click="handleNotification"> Top Right </a-button>
    <a-button type="primary" @click="handleNotificationTopLeft"> Top Left </a-button>
    <a-button type="primary" @click="handleNotificationBottomRight"> Bottom Right </a-button>
    <a-button type="primary" @click="handleNotificationBottomLeft"> Bottom Left </a-button>
  </a-space>
</template>

<script>
import { Notification } from '@arco-design/web-vue';

export default {
  setup() {
    const handleNotification = () => {
      Notification.info({
        title: 'Title',
        content: 'This is a Notification!',
      })
    }

    const handleNotificationTopLeft = () => {
      Notification.info({
        title: 'Title',
        content: 'This is a Notification!',
        position: "topLeft"
      })
    }

    const handleNotificationBottomRight = () => {
      Notification.info({
        title: 'Title',
        content: 'This is a Notification!',
        position: 'bottomRight'
      })
    }

    const handleNotificationBottomLeft = () => {
      Notification.info({
        title: 'Title',
        content: 'This is a Notification!',
        position: "bottomLeft"
      })
    }

    return {
      handleNotification,
      handleNotificationTopLeft,
      handleNotificationBottomRight,
      handleNotificationBottomLeft
    }
  }
}
</script>
```

## Update

Specifying `id` to update the existing notification.

```vue
<template>
  <a-button type="primary" @click="handleNotification">
    Open Notification
  </a-button>
</template>

<script>
import { Notification } from '@arco-design/web-vue';

export default {
  setup() {
    const handleNotification = () => {
      Notification.warning({
        id: 'your_id',
        title: 'Ready to update',
        content: 'Will update after 2 seconds...',
      })

      setTimeout(() => {
        Notification.success({
          id: 'your_id',
          title: 'Success',
          content: 'Update success!',
        });
      }, 2000)
    }

    return { handleNotification }
  }
}
</script>
```

## Update duration

Specifying `id` to update the existing notification.

```vue
<template>
  <a-button type="primary" @click="handleNotification">
    Open Notification
  </a-button>
</template>

<script>
import { Notification } from '@arco-design/web-vue';

export default {
  setup() {
    const handleNotification = () => {
      Notification.warning({
        id: 'your_id',
        title: 'Ready to update',
        content: 'Will update after 2 seconds...',
        duration: 0,
      })

      setTimeout(() => {
        Notification.success({
          id: 'your_id',
          title: 'Success',
          content: 'Update success!',
          duration: 3000,
        });
      }, 2000)
    }

    return { handleNotification }
  }
}
</script>
```

## Custom action buttons

You can add operation buttons by specifying the `btn` field.

```vue
<template>
  <a-button type="primary" @click="handleNotification">
    Open Notification
  </a-button>
</template>

<script lang="jsx">
import { Notification, Space, Button } from '@arco-design/web-vue';

export default {
  setup() {
    const handleNotification = () => {
      const id = `${Date.now()}`;
      const closeNotification =  Notification.info({
        id,
        title:'Notification',
        content:'This is a notification!',
        duration: 0,
        footer: <Space>
          <Button
            type="secondary"
            size="small"
            onClick={() => Notification.remove(id)}
          >
            Cancel
          </Button>
          <Button type="primary" size="small" onClick={closeNotification}>
            Ok
          </Button>
        </Space>
      })
    }

    return { handleNotification }
  }
}
</script>
```

## Custom close button

Need to set up `closable: true`, Custom elements use the `closeIconElement`, only icon use the `closeIcon` (There will be a `hover` style).

```vue
<template>
  <a-space>
    <a-button type="primary" @click="handleNotification">
      Open Notification
    </a-button>
    <a-button type="primary" status="danger" @click="handleNotification2">
      Open Notification
    </a-button>
  </a-space>
</template>

<script lang="jsx">
import { Notification, Button } from '@arco-design/web-vue';
import { IconCloseCircle } from '@arco-design/web-vue/es/icon';

export default {
  setup() {
    const handleNotification = () => {
      Notification.info({
        title:'Notification',
        content:'This is a notification!',
        closable: true,
        closeIcon: <IconCloseCircle />
      })
    }

    const handleNotification2 = () => {
      Notification.error({
        title:'Notification',
        content:'This is a notification!',
        closable: true,
        closeIconElement: <Button size="mini">Close</Button>
      })
    }

    return { handleNotification, handleNotification2 }
  }
}
</script>
```

## Customize style

You can set `style` and `class` to customize the style.

```vue
<template>
  <a-button type="primary" @click="handleNotification">
    Open Notification
  </a-button>
</template>

<script>
import { Notification } from '@arco-design/web-vue';

export default {
  setup() {
    const handleNotification = () => {
      Notification.info({
        title: 'Notification',
        content: 'This is a notification!',
        closable: true,
        style: { width: '500px' }
      })
    }

    return { handleNotification }
  }
}
</script>
```

## API

### `Notification` Global methods

The global methods provided by `Notification` can be used in the following three ways:
1. Called by `this.$notification`
2. In the Composition API, call `getCurrentInstance().appContext.config.globalProperties.$notification`
3. Import `Notification`, call through `Notification` itself

When used by import, the component has no way to obtain the current Vue Context. Content injected into the AppContext such as i18n or route cannot be used internally. You need to manually pass in the AppContext when calling, or specify the AppContext globally for the component.

```ts
import { createApp } from 'vue'
import { Notification } from '@arco-design/web-vue';

const app = createApp(App);
Notification._context = app._context;
````

### NotificationMethod

|Name|Description|Type|Default|
|---|---|---|:---:|
|info|Show info notification|`(    config: string \| NotificationConfig,    appContext?: AppContext  ) => NotificationReturn`|`-`|
|success|Show success notification|`(    config: string \| NotificationConfig,    appContext?: AppContext  ) => NotificationReturn`|`-`|
|warning|Show warning notification|`(    config: string \| NotificationConfig,    appContext?: AppContext  ) => NotificationReturn`|`-`|
|error|Show error notification|`(    config: string \| NotificationConfig,    appContext?: AppContext  ) => NotificationReturn`|`-`|
|remove|remove the notification for the corresponding `id`|`(id: string) => void`|`-`|
|clear|Clear all notifications|`(position?: NotificationPosition) => void`|`-`|

### NotificationConfig

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|content|Content|`RenderContent`|`-`||
|title|Title|`RenderContent`|`-`||
|icon|Icon|`RenderFunction`|`-`||
|id|Unique id|`string`|`-`||
|style|Style|`CSSProperties`|`-`||
|class|Style class name|`ClassName`|`-`||
|position|Position|`'topLeft'\|'topRight'\|'bottomLeft'\|'bottomRight'`|`-`||
|showIcon|Whether to show icon|`boolean`|`true`||
|closable|Whether it can be closed|`boolean`|`false`||
|duration|Display duration, the unit is `ms`|`number`|`3000`||
|footer|Footer Content|`RenderFunction`|`-`|2.25.0|
|closeIcon|Close button icon|`RenderFunction`|`-`||
|closeIconElement|Close button element|`RenderFunction`|`-`||
|onClose|Callback function when closing|`(id: number \| string) => void`|`-`||

### NotificationReturn

|Name|Description|Type|Default|
|---|---|---|:---:|
|close|Close the current notification|`() => void`|`-`|
