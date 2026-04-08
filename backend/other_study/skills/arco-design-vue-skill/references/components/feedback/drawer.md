---
name: arco-vue-drawer
description: "A drawer-like panel that slides out from the side of the screen after the command is triggered. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Drawer

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Click the trigger button to slide out the drawer from the right, click the mask area to close.

```vue
<template>
  <a-button type="primary" @click="handleClick">Open Drawer</a-button>
  <a-drawer :width="340" :visible="visible" @ok="handleOk" @cancel="handleCancel" unmountOnClose>
    <template #title>
      Title
    </template>
    <div>You can customize modal body text by the current situation. This modal will be closed immediately once you
      press the OK button.
    </div>
  </a-drawer>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const visible = ref(false);

    const handleClick = () => {
      visible.value = true;
    };
    const handleOk = () => {
      visible.value = false;
    };
    const handleCancel = () => {
      visible.value = false;
    }

    return {
      visible,
      handleClick,
      handleOk,
      handleCancel
    }
  },
};
</script>
```

## Position

Customize the position and click the trigger button to slide out the drawer from the corresponding position.

```vue
<template>
  <a-radio-group v-model="position">
    <a-radio value="top">Top</a-radio>
    <a-radio value="right">Right</a-radio>
    <a-radio value="bottom">Bottom</a-radio>
    <a-radio value="left">Left</a-radio>
  </a-radio-group>
  <div :style="{marginTop: '20px'}">
    <a-button type="primary" @click="handleClick">Open Drawer</a-button>
  </div>
  <a-drawer
    :width="340"
    :height="340"
    :visible="visible"
    :placement="position"
    @ok="handleOk"
    @cancel="handleCancel"
    unmountOnClose
  >
    <template #title>
      Title
    </template>
    <div>You can customize modal body text by the current situation. This modal will be closed immediately once you press the OK button.</div>
  </a-drawer>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const visible = ref(false);
    const position = ref('right');

    const handleClick = () => {
      visible.value = true;
    };
    const handleOk = () => {
      visible.value = false;
    };
    const handleCancel = () => {
      visible.value = false;
    }

    return {
      visible,
      position,
      handleClick,
      handleOk,
      handleCancel
    }
  },
};
</script>
```

## Custom node

Customize the content by slot, or set the appropriate properties to control whether it is shown or hidden.

```vue
<template>
  <a-checkbox-group v-model="custom" :options="['hide header', 'hide footer', 'hide cancel']"/>
  <div :style="{marginTop: '20px'}">
    <a-button type="primary" @click="handleClick">Open Drawer</a-button>
  </div>
  <a-drawer
    :width="340"
    :header="!custom.includes('hide header')"
    :footer="!custom.includes('hide footer')"
    :hide-cancel="custom.includes('hide cancel')"
    :visible="visible"
    @ok="handleOk"
    @cancel="handleCancel"
    unmountOnClose
  >
    <template #header>
      <span>Header and title</span>
    </template>
    <div>
      You can customize modal body text by the current situation. This modal will be closed immediately once you
      press the OK button.
    </div>
  </a-drawer>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const visible = ref(false);
    const custom = ref([])

    const handleClick = () => {
      visible.value = true;
    };
    const handleOk = () => {
      visible.value = false;
    };
    const handleCancel = () => {
      visible.value = false;
    }

    return {
      custom,
      visible,
      handleClick,
      handleOk,
      handleCancel
    }
  },
};
</script>
```

## Nested

Open a new drawer in the drawer.

```vue
<template>
  <a-button type="primary" @click="handleClick">Open Drawer</a-button>
  <a-drawer :visible="visible" :width="500" @ok="handleOk" @cancel="handleCancel" unmountOnClose>
    <template #title>
      Title
    </template>
    <div :style="{marginBottom: '20px'}">You can customize modal body text by the current situation. This modal will be closed immediately once you press the OK button.</div>
    <a-button type="primary" @click="handleNestedClick">Open Nested Drawer</a-button>
  </a-drawer>
  <a-drawer :visible="nestedVisible" @ok="handleNestedOk" @cancel="handleNestedCancel" unmountOnClose>
    <template #title>
      Title
    </template>
    <div>You can customize modal body text by the current situation. This modal will be closed immediately once you press the OK button.</div>
  </a-drawer>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const visible = ref(false);
    const nestedVisible = ref(false);

    const handleClick = () => {
      visible.value = true;
    };
    const handleOk = () => {
      visible.value = false;
    };
    const handleCancel = () => {
      visible.value = false;
    }
    const handleNestedClick = () => {
      nestedVisible.value = true;
    };
    const handleNestedOk = () => {
      nestedVisible.value = false;
    };
    const handleNestedCancel = () => {
      nestedVisible.value = false;
    }

    return {
      visible,
      nestedVisible,
      handleClick,
      handleOk,
      handleCancel,
      handleNestedClick,
      handleNestedOk,
      handleNestedCancel
    }
  },
};
</script>
```

## popup container

You can use 'popup-container' to set the mount position of the pop-up layer node

```vue
<template>
  <div>
    <div
      id="parentNode"
      style="width: 100%; height: 300px; background-color: var(--color-fill-2); position: relative; overflow: hidden; line-height: 300px; text-align: center;"
    >
      <a-button type="primary" @click="handleClick">Open Drawer</a-button>
    </div>
  </div>
  <a-drawer
    popup-container="#parentNode"
    :visible="visible"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <template #title> Title </template>
    <div
      >You can customize modal body text by the current situation. This modal
      will be closed immediately once you press the OK button.</div
    >
  </a-drawer>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const visible = ref(false);

    const handleClick = () => {
      visible.value = true;
    };
    const handleOk = () => {
      visible.value = false;
    };
    const handleCancel = () => {
      visible.value = false;
    }

    return {
      visible,
      handleClick,
      handleOk,
      handleCancel
    }
  },
};
</script>
```

## Call By Function

Use the drawer by function.

```vue
<template>
  <a-button type="primary" @click="handleClick">Open Drawer</a-button>
</template>

<script>
import { Drawer } from '@arco-design/web-vue';

export default {
  setup() {
    const handleClick = () => {
      Drawer.open({
        title: 'Info Title',
        content: 'This is an info message',
        width: 340
      });
    };

    return {
      handleClick,
    }
  },
}
</script>
```

## API

### `<drawer>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|visible **(v-model)**|Whether the drawer is visible|`boolean`|`false`||
|default-visible|Whether the drawer is visible by default (uncontrolled mode)|`boolean`|`false`||
|placement|Where the drawer is placed|`'top' \| 'right' \| 'bottom' \| 'left'`|`'right'`||
|title|Title|`string`|`-`||
|mask|Whether to show the mask|`boolean`|`true`||
|mask-closable|Click on the mask layer to be able to close|`boolean`|`true`||
|closable|Whether to show the close button|`boolean`|`true`||
|ok-text|The content of the ok button|`string`|`-`||
|cancel-text|The content of the cancel button|`string`|`-`||
|ok-loading|Whether the ok button is in the loading state|`boolean`|`false`||
|ok-button-props|Props of confirm button|`ButtonProps`|`-`|2.9.0|
|cancel-button-props|Props of cancel button|`ButtonProps`|`-`|2.9.0|
|unmount-on-close|Whether to uninstall the node when close|`boolean`|`false`|2.12.0|
|width|The width of the drawer (only available when placement is right, left)|`number\|string`|`250`||
|height|The height of the drawer (only available when placement is top, bottom)|`number\|string`|`250`||
|popup-container|Mount container for popup|`string \| HTMLElement`|`'body'`||
|drawer-style|Drawer style|`CSSProperties`|`-`||
|body-class|The classname of the drawer body|`string \| any[]`|`-`|2.57.0|
|body-style|Drawer body style|`StyleValue`|`-`|2.57.0|
|on-before-ok|The callback function before the ok event is triggered. If false is returned, subsequent events will not be triggered, and done can also be used to close asynchronously.|`(  done: (closed: boolean) => void) => void \| boolean \| Promise<void \| boolean>`|`-`||
|on-before-cancel|The callback function before the cancel event is triggered. If it returns false, no subsequent events will be triggered.|`() => boolean`|`-`||
|esc-to-close|Whether to support the ESC key to close the dialog|`boolean`|`true`|2.15.0|
|render-to-body|Whether the drawer is mounted under the `body` element|`boolean`|`true`||
|header|Whether to display high-quality content|`boolean`|`true`|2.33.0|
|footer|Whether to display the bottom content|`boolean`|`true`|2.11.0|
|hide-cancel|Whether to hide the cancel button|`boolean`|`false`|2.19.0|
### `<drawer>` Events

|Event Name|Description|Parameters|version|
|---|---|---|:---|
|ok|Triggered when the OK button is clicked|ev: `MouseEvent`||
|cancel|Triggered when the cancel or close button is clicked|ev: `MouseEvent \| KeyboardEvent`||
|open|Triggered after the drawer is opened (the animation ends)|-||
|close|Triggered when the drawer is closed (the animation ends)|-||
|before-open|Triggered before drawer is opened|-|2.43.0|
|before-close|Triggered before drawer is closed|-|2.43.0|
### `<drawer>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|header|Header|-|2.33.0|
|title|Title|-||
|footer|Footer|-||

### `<drawer>` Global methods

The global methods provided by Drawer can be used in the following three ways:

1. Called by `this.$drawer`
2. In the Composition API, call through `getCurrentInstance().appContext.config.globalProperties.$drawer`
3. Import Drawer, call through Drawer itself

When used by import, the component has no way to obtain the current Vue Context. Content injected into the AppContext such as i18n or route cannot be used internally. You need to manually pass in the AppContext when calling, or specify the AppContext globally for the component.

```ts
import { createApp } from 'vue'
import { Drawer } from '@arco-design/web-vue';

const app = createApp(App);
Drawer._context = app._context;
````

### DrawerConfig

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|placement|Where the drawer is placed|`'top' \| 'right' \| 'bottom' \| 'left'`|`'right'`||
|title|Title|`RenderContent`|`-`||
|content|Content|`RenderContent`|`-`||
|mask|Whether to show the mask|`boolean`|`true`||
|maskClosable|Click on the mask layer to be able to close|`boolean`|`true`||
|closable|Whether to show the close button|`boolean`|`true`||
|okText|The content of the ok button|`string`|`-`||
|cancelText|The content of the cancel button|`string`|`-`||
|okLoading|Whether the ok button is in the loading state|`boolean`|`false`||
|okButtonProps|Props of confirm button|`ButtonProps`|`-`|2.9.0|
|cancelButtonProps|Props of cancel button|`ButtonProps`|`-`|2.9.0|
|width|The width of the drawer (only available when placement is right, left)|`number \| string`|`250`||
|height|The height of the drawer (only available when placement is top, bottom)|`number \| string`|`250`||
|popupContainer|Mount container for popup|`string \| HTMLElement`|`'body'`||
|drawerStyle|Drawer style|`CSSProperties`|`-`||
|onOk|Triggered when the OK button is clicked|`(e?: Event) => void`|`-`||
|onCancel|Triggered when the cancel or close button is clicked|`(e?: Event) => void`|`-`||
|onBeforeOk|The callback function before the ok event is triggered. If false is returned, subsequent events will not be triggered, and done can also be used to close asynchronously.|`(    done: (closed: boolean) => void  ) => void \| boolean \| Promise<void \| boolean>`|`-`||
|onBeforeCancel|The callback function before the cancel event is triggered. If it returns false, no subsequent events will be triggered.|`() => boolean`|`-`||
|onOpen|Triggered after the drawer is opened (the animation ends)|`() => void`|`-`||
|onClose|Triggered when the drawer is closed (the animation ends)|`() => void`|`-`||
|onBeforeOpen|Triggered before drawer is opened|`() => void`|`-`|2.43.0|
|onBeforeClose|Triggered before drawer is closed|`() => void`|`-`|2.43.0|
|escToClose|Whether to support the ESC key to close the drawer|`boolean`|`true`|2.15.0|
|header|Whether to display high-quality content|`boolean \| RenderContent`|`true`|2.33.0|
|footer|Whether to display the bottom content|`boolean \| RenderContent`|`true`|2.11.0|
|hideCancel|Whether to hide the cancel button|`boolean`|`false`|2.19.0|

### DrawerReturn

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|close|Close Drawer|`() => void`|`-`||
|update|Update Drawer|`(config: DrawerUpdateConfig) => void`|`-`|2.43.2|

### DrawerMethod

|Name|Description|Type|Default|
|---|---|---|:---:|
|open|Open drawer|`(config: DrawerConfig, appContext?: AppContext) => DrawerReturn`|`-`|
