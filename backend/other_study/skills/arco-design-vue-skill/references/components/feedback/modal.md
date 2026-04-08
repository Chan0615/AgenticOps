---
name: arco-vue-modal
description: "Open a floating layer on the current page to carry related operations. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Modal

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

The basic usage of the modal.

```vue
<template>
  <a-button @click="handleClick">Open Modal</a-button>
  <a-modal v-model:visible="visible" @ok="handleOk" @cancel="handleCancel">
    <template #title>
      Title
    </template>
    <div>You can customize modal body text by the current situation. This modal will be closed immediately once you press the OK button.</div>
  </a-modal>
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
}
</script>
```

## Async Close

Asynchronous shutdown can be implemented more concisely through on-before-ok

```vue

<template>
  <a-button @click="handleClick">Open Modal</a-button>
  <a-modal v-model:visible="visible" @cancel="handleCancel" :on-before-ok="handleBeforeOk" unmountOnClose>
    <template #title>
      Title
    </template>
    <div>You can customize modal body text by the current situation. This modal will be closed immediately once you
      press the OK button.
    </div>
  </a-modal>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const visible = ref(false);

    const handleClick = () => {
      visible.value = true;
    };
    const handleBeforeOk = async () => {
      await new Promise(resolve => setTimeout(resolve, 3000));
      return true;
      // prevent close
      // return false;
    };
    const handleCancel = () => {
      visible.value = false;
    }

    return {
      visible,
      handleClick,
      handleBeforeOk,
      handleCancel
    }
  },
}
</script>
```

## Call By Function

Use the modal by function.

```vue
<template>
  <a-button @click="handleClick">Open Modal</a-button>
</template>

<script>
import { h } from 'vue';
import { Modal, Button } from '@arco-design/web-vue';

const ModalContent = {
  setup() {
    const onClick = () => {
      Modal.info({
        title: 'Info Title',
        content: 'This is an nest info message'
      });
    };

    return () => h('div', {class: 'info-modal-content'}, [
      h('span', {style: 'margin-bottom: 10px;'}, 'This is an info message'),
      h(Button, {size: 'mini', onClick}, 'Open Nest Modal')
    ])
  },
}

export default {
  setup() {
    const handleClick = () => {
      Modal.info({
        title: 'Info Title',
        content: () => h(ModalContent)
      });
    };

    return {
      handleClick
    }
  },
}
</script>

<style>
.info-modal-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
```

## Notice

There are four types of notice: **info**, **success**, **warning**, **error**, and only a confirmation button is provided to close the notice.
The message defaults to enable `simple` and `hideCancel` by default, if you want to cancel, you can set it again.

```vue
<template>
  <a-space>
    <a-button @click="handleClickInfo">Info</a-button>
    <a-button @click="handleClickSuccess" status="success">Success</a-button>
    <a-button @click="handleClickWarning" status="warning">Warning</a-button>
    <a-button @click="handleClickError" status="danger">Error</a-button>
  </a-space>
</template>

<script>
import { Modal } from '@arco-design/web-vue';

export default {
  setup() {
    const handleClickInfo = () => {
      Modal.info({
        title: 'Info Notification',
        content: 'This is an info description which directly indicates a neutral informative change or action.'
      });
    };
    const handleClickSuccess = () => {
      Modal.success({
        title: 'Success Notification',
        content: 'This is a success notification'
      });
    };
    const handleClickWarning = () => {
      Modal.warning({
        title: 'Warning Notification',
        content: 'This is a warning description which directly indicates a warning that might need attention.'
      });
    };
    const handleClickError = () => {
      Modal.error({
        title: 'Error Notification',
        content: 'This is an error description which directly indicates a dangerous or potentially negative action.'
      });
    };

    return {
      handleClickInfo,
      handleClickSuccess,
      handleClickWarning,
      handleClickError
    }
  },
}
</script>
```

## Modal width

Set `width="auto"` to make the dialog box adapt to the width

```vue
<template>
  <a-button @click="handleClick">Open Modal</a-button>
  <a-modal width="auto" v-model:visible="visible" @ok="handleOk" @cancel="handleCancel">
    <template #title>
      Title
    </template>
    <div>You can customize modal body text by the current situation. This modal will be closed immediately once you press the OK button.</div>
  </a-modal>
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
}
</script>
```

## Custom Button Text

Set `okText` and `cancelText` to customize the button text.

```vue
<template>
  <a-button @click="handleClick">Open Modal</a-button>
  <a-modal :visible="visible" @ok="handleOk" @cancel="handleCancel" okText="Confirm" cancelText="Exit" unmountOnClose>
    <template #title>
      Title
    </template>
    <div>You can customize modal body text by the current situation. This modal will be closed immediately once you press the OK button.</div>
  </a-modal>
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
}
</script>
```

## Modal Form

Using Form in Modal

```vue

<template>
  <a-button @click="handleClick">Open Form Modal</a-button>
  <a-modal v-model:visible="visible" title="Modal Form" @cancel="handleCancel" @before-ok="handleBeforeOk">
    <a-form :model="form">
      <a-form-item field="name" label="Name">
        <a-input v-model="form.name" />
      </a-form-item>
      <a-form-item field="post" label="Post">
        <a-select v-model="form.post">
          <a-option value="post1">Post1</a-option>
          <a-option value="post2">Post2</a-option>
          <a-option value="post3">Post3</a-option>
          <a-option value="post4">Post4</a-option>
        </a-select>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const visible = ref(false);
    const form = reactive({
      name: '',
      post: ''
    });

    const handleClick = () => {
      visible.value = true;
    };
    const handleBeforeOk = (done) => {
      console.log(form)
      window.setTimeout(() => {
        done()
        // prevent close
        // done(false)
      }, 3000)
    };
    const handleCancel = () => {
      visible.value = false;
    }

    return {
      visible,
      form,
      handleClick,
      handleBeforeOk,
      handleCancel
    }
  },
}
</script>
```

## Draggable

Enables the `draggable` property, which allows the user to drag the dialog.

```vue
<template>
  <a-button @click="handleClick">Open Draggable Modal</a-button>
  <a-modal v-model:visible="visible" @ok="handleOk" @cancel="handleCancel" draggable>
    <template #title>
      Title
    </template>
    <div>You can customize modal body text by the current situation. This modal will be closed immediately once you press the OK button.</div>
  </a-modal>
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
}
</script>
```

## Fullscreen

Enable the `fullscreen` property to make the dialog fill the entire container.

```vue
<template>
  <a-button @click="handleClick">Open Modal</a-button>
  <a-modal v-model:visible="visible" @ok="handleOk" @cancel="handleCancel" fullscreen>
    <template #title>
      Title
    </template>
    <div>You can customize modal body text by the current situation. This modal will be closed immediately once you press the OK button.</div>
  </a-modal>
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
}
</script>
```

## API

### `<modal>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|visible **(v-model)**|Whether the modal is visible|`boolean`|`-`||
|default-visible|Whether the modal is visible by default (uncontrolled state)|`boolean`|`false`||
|width|The width of the dialog box, if not set, the width value in the style will be used|`number\|string`|`-`|2.12.0|
|top|The height from the top of the dialog box. It does not take effect when the center display is turned on.|`number\|string`|`-`|2.12.0|
|mask|Whether to show the mask|`boolean`|`true`||
|title|Title|`string`|`-`||
|title-align|horizontal alignment of the title|`'start' \| 'center'`|`'center'`|2.17.0|
|align-center|Whether the dialog box is displayed in the center|`boolean`|`true`||
|unmount-on-close|Whether to uninstall the node when close|`boolean`|`false`||
|mask-closable|Whether to close the modal when click the mask|`boolean`|`true`||
|hide-cancel|Whether to hide the cancel button|`boolean`|`false`||
|simple|Whether to enable simple mode|`boolean`|`(props: any) => {  return props.notice;}`||
|closable|Whether to show the close button|`boolean`|`true`||
|ok-text|The content of the confirm button|`string`|`-`||
|cancel-text|The content of the cancel button|`string`|`-`||
|ok-loading|Whether the confirm button is in the loading state|`boolean`|`false`||
|ok-button-props|Props of confirm button|`ButtonProps`|`-`||
|cancel-button-props|Props of cancel button|`ButtonProps`|`-`||
|footer|Whether to show the footer|`boolean`|`true`||
|render-to-body|Whether the modal is mounted under the `body` element|`boolean`|`true`||
|popup-container|Mount container for modal|`string \| HTMLElement`|`'body'`||
|mask-style|Mask style|`CSSProperties`|`-`||
|modal-class|The classname of the modal|`string \| any[]`|`-`||
|modal-style|Modal style|`CSSProperties`|`-`||
|on-before-ok|The callback function before the ok event is triggered. If false is returned, subsequent events will not be triggered, and done can also be used to close asynchronously.|`(  done: (closed: boolean) => void) => void \| boolean \| Promise<void \| boolean>`|`-`|2.7.0|
|on-before-cancel|The callback function before the cancel event is triggered. If it returns false, no subsequent events will be triggered.|`() => boolean`|`-`|2.7.0|
|esc-to-close|Whether to support the ESC key to close the dialog|`boolean`|`true`|2.15.0|
|draggable|Whether to support drag|`boolean`|`false`|2.19.0|
|fullscreen|Whether to enable full screen|`boolean`|`false`|2.19.0|
|mask-animation-name|Mask layer animation name|`string`|`-`|2.24.0|
|modal-animation-name|Modal animation name|`string`|`-`|2.24.0|
|body-class|The classname of the modal|`string \| any[]`|`-`|2.31.0|
|body-style|Modal style|`StyleValue`|`-`|2.31.0|
|hide-title|Whether to hide the title|`boolean`|`false`|2.50.0|
### `<modal>` Events

|Event Name|Description|Parameters|version|
|---|---|---|:---|
|ok|Triggered when the OK button is clicked|ev: `MouseEvent`||
|cancel|Triggered when the cancel/close button is clicked|ev: `MouseEvent \| KeyboardEvent`||
|open|Triggered after the modal is opened (the animation ends)|-||
|close|Triggered after the modal is closed (the animation ends)|-||
|before-open|Triggered before dialog is opened|-|2.16.0|
|before-close|Triggered before dialog is closed|-|2.16.0|
### `<modal>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|title|Title|-|
|footer|Footer|-|

### `<modal>` Global methods

The global methods provided by Modal can be used in the following three ways:

1. Called by this.$modal
2. In the Composition API, call through getCurrentInstance().appContext.config.globalProperties.$modal
3. Import Modal, call through Modal itself

When used by import, the component has no way to obtain the current Vue Context. Content injected into the AppContext such as i18n or route cannot be used internally. You need to manually pass in the AppContext when calling, or specify the AppContext globally for the component.

```ts
import { createApp } from 'vue'
import { Modal } from '@arco-design/web-vue';

const app = createApp(App);
Modal._context = app._context;
````

### ModalConfig

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|title|Title|`RenderContent`|`-`||
|content|Content|`RenderContent`|`-`||
|footer|Footer|`boolean \| RenderContent`|`true`||
|closable|Whether to show the close button|`boolean`|`true`||
|okText|The content of the confirm button|`string`|`-`||
|cancelText|The content of the cancel button|`string`|`-`||
|okButtonProps|Props of confirm button|`ButtonProps`|`-`||
|cancelButtonProps|Props of cancel button|`ButtonProps`|`-`||
|okLoading|Whether the confirm button is in the loading state|`boolean`|`false`||
|hideCancel|Whether to hide the cancel button|`boolean`|`false`||
|mask|Whether to show the mask|`boolean`|`true`||
|simple|Whether to enable simple mode|`boolean`|`false`||
|maskClosable|Whether to close the modal when click the mask|`boolean`|`true`||
|maskStyle|Mask style|`CSSProperties`|`-`||
|alignCenter|Whether the dialog box is displayed in the center|`boolean`|`true`||
|escToClose|Whether to support the ESC key to close the dialog|`boolean`|`true`|2.15.0|
|draggable|Whether to support drag|`boolean`|`false`|2.19.0|
|fullscreen|Whether to enable full screen|`boolean`|`false`|2.19.0|
|onOk|Callback function for clicking the OK button|`(e?: Event) => void`|`-`||
|onCancel|Callback function for clicking the Cancel button|`(e?: Event) => void`|`-`||
|onBeforeOk|The callback function before the ok event is triggered. If false is returned, subsequent events will not be triggered, and done can also be used to close asynchronously.|`(    done: (closed: boolean) => void  ) => void \| boolean \| Promise<void \| boolean>`|`-`|2.7.0|
|onBeforeCancel|The callback function before the cancel event is triggered. If it returns false, no subsequent events will be triggered.|`() => boolean`|`-`|2.7.0|
|onOpen|Triggered after the modal is opened (the animation ends)|`() => void`|`-`||
|onClose|Triggered after the modal is closed (the animation ends)|`() => void`|`-`||
|onBeforeOpen|Triggered before dialog is opened|`() => void`|`-`|2.16.0|
|onBeforeClose|Triggered before dialog is closed|`() => void`|`-`|2.16.0|
|width|The width of the dialog box, if not set, the width value in the style will be used|`number \| string`|`-`|2.12.0|
|top|The height from the top of the dialog box. It does not take effect when the center display is turned on.|`number \| string`|`-`|2.12.0|
|titleAlign|horizontal alignment of the title|`'start' \| 'center'`|`'center'`|2.17.0|
|renderToBody|Whether the modal is mounted under the `body` element|`boolean`|`true`||
|popupContainer|Mount container for modal|`string \| HTMLElement`|`'body'`||
|modalClass|The classname of the modal|`string \| any[]`|`-`||
|modalStyle|Modal style|`CSSProperties`|`-`||
|maskAnimationName|Mask layer animation name|`string`|`-`|2.24.0|
|modalAnimationName|Modal animation name|`string`|`-`|2.24.0|
|hideTitle|Whether to hide the title|`boolean`|`false`|2.50.0|
|bodyClass|The classname of the modal|`string \| any[]`|`-`||
|bodyStyle|Modal style|`StyleValue`|`-`||

### ModalReturn

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|close|Close Modal|`() => void`|`-`||
|update|Update Modal|`(config: ModalUpdateConfig) => void`|`-`|2.43.2|

### ModalMethod

|Name|Description|Type|Default|
|---|---|---|:---:|
|open|Open modal|`(config: ModalConfig, appContext?: AppContext) => ModalReturn`|`-`|
|confirm|Open modal (simple mode)|`(config: ModalConfig, appContext?: AppContext) => ModalReturn`|`-`|
|info|Open info modal|`(config: ModalConfig, appContext?: AppContext) => ModalReturn`|`-`|
|success|Open success modal|`(config: ModalConfig, appContext?: AppContext) => ModalReturn`|`-`|
|warning|Open warning modal|`(config: ModalConfig, appContext?: AppContext) => ModalReturn`|`-`|
|error|Open error modal|`(config: ModalConfig, appContext?: AppContext) => ModalReturn`|`-`|
