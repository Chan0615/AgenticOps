---
name: arco-vue-upload
description: "Users can transfer files or submit corresponding content. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Upload

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of upload component.

```vue
<template>
  <a-space direction="vertical" :style="{ width: '100%' }">
    <a-upload action="/" />
    <a-upload action="/" disabled style="margin-top: 40px;"/>
  </a-space>
</template>
```

## Avatar Upload

Click to upload user's avatar, and validate size and format of picture with beforeUpload.

```vue

<template>
  <a-space direction="vertical" :style="{ width: '100%' }">
    <a-upload
      action="/"
      :fileList="file ? [file] : []"
      :show-file-list="false"
      @change="onChange"
      @progress="onProgress"
    >
      <template #upload-button>
        <div
          :class="`arco-upload-list-item${
            file && file.status === 'error' ? ' arco-upload-list-item-error' : ''
          }`"
        >
          <div
            class="arco-upload-list-picture custom-upload-avatar"
            v-if="file && file.url"
          >
            <img :src="file.url" />
            <div class="arco-upload-list-picture-mask">
              <IconEdit />
            </div>
            <a-progress
              v-if="file.status === 'uploading' && file.percent < 100"
              :percent="file.percent"
              type="circle"
              size="mini"
              :style="{
                position: 'absolute',
                left: '50%',
                top: '50%',
                transform: 'translateX(-50%) translateY(-50%)',
              }"
            />
          </div>
          <div class="arco-upload-picture-card" v-else>
            <div class="arco-upload-picture-card-text">
              <IconPlus />
              <div style="margin-top: 10px; font-weight: 600">Upload</div>
            </div>
          </div>
        </div>
      </template>
    </a-upload>
  </a-space>
</template>

<script>
import { IconEdit, IconPlus } from '@arco-design/web-vue/es/icon';
import { ref } from 'vue';

export default {
  components: {IconPlus, IconEdit},
  setup() {
    const file = ref();

    const onChange = (_, currentFile) => {
      file.value = {
        ...currentFile,
        // url: URL.createObjectURL(currentFile.file),
      };
    };
    const onProgress = (currentFile) => {
      file.value = currentFile;
    };
    return {
      file,
      onChange,
      onProgress
    }
  },
};
</script>
```

## File List

You can specify a default list of uploaded files.

```vue
<template>
  <a-upload action="/" :default-file-list="fileList" />
</template>

<script>
export default {
  setup() {
    const fileList = [
      {
        uid: '-1',
        name: 'ice.png',
        url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp',
      },
      {
        status: 'error',
        uid: '-2',
        percent: 0,
        response: 'Upload error message',
        name: 'cat.png',
        url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/e278888093bef8910e829486fb45dd69.png~tplv-uwbnlip3yd-webp.webp',
      },
      {
        uid: '-3',
        name: 'light.png',
        url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp',
      },
    ];

    return {
      fileList
    }
  },
};
</script>
```

## Picture Card

Enable the photo wall mode by setting `list-type="picture-card"`.

```vue
<template>
  <a-upload
    list-type="picture-card"
    action="/"
    :default-file-list="fileList"
    image-preview
  />
</template>

<script>
export default {
  setup() {
    const fileList = [
      {
        uid: '-2',
        name: '20200717-103937.png',
        url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp',
      },
      {
        uid: '-1',
        name: 'hahhahahahaha.png',
        url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/e278888093bef8910e829486fb45dd69.png~tplv-uwbnlip3yd-webp.webp',
      },
    ];

    return {
      fileList
    }
  },
};
</script>
```

## Draggable

Enable drag and drop support by setting `draggable`.

```vue
<template>
  <a-upload draggable action="/" />
</template>
```

## Picture List

Enable the picture list mode by setting `list-type="picture"`.

```vue
<template>
  <a-upload
    list-type="picture"
    action="/"
    :default-file-list="fileList"
  />
</template>

<script>
export default {
  setup() {
    const fileList = [
      {
        uid: '-2',
        name: '20200717-103937.png',
        url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp',
      },
      {
        uid: '-1',
        name: 'hahhahahahaha.png',
        url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/e278888093bef8910e829486fb45dd69.png~tplv-uwbnlip3yd-webp.webp',
      },
    ];

    return {
      fileList
    }
  },
};
</script>
```

## manual upload

When setting `auto-upload` to `false`, you can manually upload by calling the `submit` method.

```vue
<template>
  <div>
    <a-upload
      action="/"
      :auto-upload="false"
      ref="uploadRef"
      @change="onChange"
      multiple
    >
      <template #upload-button>
        <a-space>
          <a-button> select file</a-button>
          <a-button type="primary" @click="submit"> start upload</a-button>
          <a-button type="primary" @click="submitOne">
            only upload one
          </a-button>
        </a-space>
      </template>
    </a-upload>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const uploadRef = ref();
    const files = ref([]);

    const submitOne = (e) => {
      e.stopPropagation();
      console.log(files.value);
      uploadRef.value.submit(files.value.find((x) => x.status === 'init'));
    };

    const submit = (e) => {
      e.stopPropagation();
      uploadRef.value.submit();
    };

    const onChange = (fileList) => {
      files.value = fileList;
    };

    return {
      uploadRef,
      files,
      submitOne,
      submit,
      onChange,
    };
  },
};
</script>
```

## On Before Upload

The function will be executed before each file upload. Uploading will be aborted when the return value is false or a Promise which resolve(false) or reject.

```vue
<template>
  <a-space direction="vertical" :style="{ width: '100%' }">
    <a-upload action="/" @before-upload="beforeUpload" />
  </a-space>
</template>

<script>
import { Modal } from '@arco-design/web-vue';

export default {
  setup() {
    const beforeUpload = (file) => {
      return new Promise((resolve, reject) => {
        Modal.confirm({
          title: 'beforeUpload',
          content: `Confirm upload ${file.name}`,
          onOk: () => resolve(true),
          onCancel: () => reject('cancel'),
        });
      });
    };
    return {
      beforeUpload
    }
  },
};
</script>
```

## On Before Remove

The function will be executed before each file remove. Removing will be aborted when the return value is false or a Promise which resolve(false) or reject.

```vue
<template>
  <a-space direction="vertical" :style="{ width: '100%' }">
    <a-upload
      action="/"
      :default-file-list="[
        {
          uid: '-2',
          name: 'light.png',
          url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp',
        },
        {
          uid: '-1',
          name: 'ice.png',
          url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp',
        },
      ]"
      @before-remove="beforeRemove"
    />
  </a-space>
</template>

<script>
import { Modal } from '@arco-design/web-vue';

export default {
  setup() {
    const beforeRemove = (file) => {
      return new Promise((resolve, reject) => {
        Modal.confirm({
          title: 'on-before-remove',
          content: `Confirm delete ${file.name}`,
          onOk: () => resolve(true),
          onCancel: () => reject('cancel'),
        });
      });
    };

    return {
      beforeRemove
    }
  },
};
</script>
```

## Limit

Limit the maximum number of uploaded files.

```vue
<template>
  <a-upload multiple action="/" :limit="3" />
</template>
```

## custom upload button

You can pass in custom content through the slot `upload-button` as the trigger node for file upload.

```vue
<template>
  <a-upload action="/">
    <template #upload-button>
      <div
        style="
        background-color: var(--color-fill-2);
        color: var(--color-text-1);
        border: 1px dashed var(--color-fill-4);
        height: 158px;
        width: 380px;
        border-radius: 2;
        line-height: 158px;
        text-align: center;"
      >
        <div>
          Drag the file here or
          <span style="color: #3370FF"> Click to upload</span>
        </div>
      </div>
    </template>
  </a-upload>
</template>
```

## custom icon

custom icon

```vue

<template>
  <div>
    <div style="margin-bottom: 20px;">
      <a-space>
        <span>Type: </span>
        <a-radio-group v-model="type">
          <a-radio value="text">text</a-radio>
          <a-radio value="picture">picture</a-radio>
          <a-radio value="picture-card">picture-card</a-radio>
        </a-radio-group>
      </a-space>
    </div>
    <a-upload
      action="/"
      :list-type="type"
      :default-file-list="[
        {
          uid: '-1',
          name: 'ice.png',
          url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp',
        },
        {
          uid: '-3',
          name: 'light.png',
          url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp',
        },
      ]"
      :custom-icon="getCustomIcon()"
    />
  </div>
</template>

<script>
import { h, ref } from 'vue';
import { IconUpload, IconFileAudio, IconClose, IconFaceFrownFill } from '@arco-design/web-vue/es/icon';

export default {
  setup() {
    const type = ref('text');
    const getCustomIcon = () => {
      return {
        retryIcon: () => h(IconUpload),
        cancelIcon: () => h(IconClose),
        fileIcon: () => h(IconFileAudio),
        removeIcon: () => h(IconClose),
        errorIcon: () => h(IconFaceFrownFill),
        fileName: (file) => {
          return `File name: ${file.name}`
        },
      };
    };

    return {
      type,
      getCustomIcon
    }
  },
};
</script>
```

## Custom Upload Request

Custom upload request can be realized through `custom-request`.

```vue
<template>
  <a-upload :custom-request="customRequest" />
</template>

<script>
export default {
  setup() {
    const customRequest = (option) => {
      const {onProgress, onError, onSuccess, fileItem, name} = option
      const xhr = new XMLHttpRequest();
      if (xhr.upload) {
        xhr.upload.onprogress = function (event) {
          let percent;
          if (event.total > 0) {
            // 0 ~ 1
            percent = event.loaded / event.total;
          }
          onProgress(percent, event);
        };
      }
      xhr.onerror = function error(e) {
        onError(e);
      };
      xhr.onload = function onload() {
        if (xhr.status < 200 || xhr.status >= 300) {
          return onError(xhr.responseText);
        }
        onSuccess(xhr.response);
      };

      const formData = new FormData();
      formData.append(name || 'file', fileItem.file);
      xhr.open('post', '//upload-z2.qbox.me/', true);
      xhr.send(formData);

      return {
        abort() {
          xhr.abort()
        }
      }
    };

    return {
      customRequest
    }
  },
}
</script>
```

## Upload directory

Upload directory

```vue
<template>
  <a-space direction="vertical" :style="{ width: '100%' }">
    <a-upload action="/" directory />
  </a-space>
</template>
```

## API

### `<upload>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|file-list **(v-model)**|File List|`FileItem[]`|`-`||
|default-file-list|Default file list (uncontrolled state)|`FileItem[]`|`[]`||
|accept|For the received upload file type, please refer to [HTML standard](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#htmlattrdefaccept "_blank")|`string`|`-`||
|action|Uploaded URL|`string`|`-`||
|disabled|Whether to disable|`boolean`|`false`||
|multiple|Whether to support multiple file upload|`boolean`|`false`||
|directory|Whether to support folder upload (requires browser support)|`boolean`|`false`||
|draggable|Whether to support drag and drop upload|`boolean`|`false`||
|tip|Prompt text|`string`|`-`||
|headers|Additional header information for upload request|`Record<string, string>`|`-`||
|data|Upload request additional data|`Record<string, string \| Blob>\| ((fileItem: FileItem) => Record<string, string \| Blob>)`|`-`||
|name|Uploaded file name|`string \| ((fileItem: FileItem) => string)`|`-`||
|with-credentials|Whether the upload request carries cookies|`boolean`|`false`||
|custom-request|Custom upload behavior|`(option: RequestOption) => UploadRequest`|`-`||
|limit|Limit the number of uploaded files. `0` means no limit|`number`|`0`||
|auto-upload|Whether to upload files automatically|`boolean`|`true`||
|show-file-list|Whether to display the file list|`boolean`|`true`||
|show-remove-button|Whether to display the remove button|`boolean`|`true`|2.11.0|
|show-retry-button|Whether to display the retry button|`boolean`|`true`|2.11.0|
|show-cancel-button|Whether to display the cancel button|`boolean`|`true`|2.11.0|
|show-upload-button|Whether to display the retry button. Added `showOnExceedLimit` support in version 2.14.0|`boolean \| { showOnExceedLimit: boolean }`|`true`|2.11.0|
|show-preview-button|Whether to display the preview button in picture-card|`boolean`|`true`|2.42.0|
|download|Whether to add download attribute to `<a>` link|`boolean`|`false`|2.11.0|
|show-link|In the list mode, if the uploaded file has a URL, the link will be displayed. If you turn off only display text and click to trigger the `preview` event.|`boolean`|`true`|2.13.0|
|image-loading|Native HTML attributes of `<img>`, browser support is required|`'eager' \| 'lazy'`|`-`|2.11.0|
|list-type|Picture list type|`'text' \| 'picture' \| 'picture-card'`|`'text'`||
|response-url-key|Get the key of the image URL in the Response. After opening, it will replace the pre-load image with the uploaded image|`string \| ((fileItem: FileItem) => string)`|`-`||
|custom-icon|Custom icon|`CustomIcon`|`-`||
|on-before-upload|Trigger before uploading a file|`(file: File) => boolean \| Promise<boolean \| File>`|`-`||
|on-before-remove|Triggered before removing the file|`(fileItem: FileItem) => Promise<boolean>`|`-`||
|on-button-click|Click the upload button to trigger (if the Promise is returned, the default input upload will be closed)|`(event: Event) => Promise<FileList> \| void`|`-`||
### `<upload>` Events

|Event Name|Description|Parameters|
|---|---|---|
|exceed-limit|Triggered when the uploaded file exceeds the limit|fileList: `FileItem[]`<br>files: `File[]`|
|change|Triggered when the status of the uploaded file changes|fileList: `FileItem[]`<br>fileItem: `fileItem`|
|progress|Triggered when the uploading file progress changes|fileItem: `fileItem`<br>ev: `ProgressEvent`|
|preview|Trigger when the image preview is clicked|fileItem: `FileItem`|
|success|Triggered when upload is successful|fileItem: `FileItem`|
|error|Triggered when upload fails|fileItem: `FileItem`|
### `<upload>` Methods

|Method|Description|Parameters|Return|version|
|---|---|---|:---:|:---|
|submit|Upload file (file that has been initialized)|fileItem: `FileItem`|-||
|abort|Abort upload|fileItem: `FileItem`|-||
|updateFile|Update file|id: `string`<br>file: `File`|-||
|upload|Upload file|files: `File[]`|-|2.41.0|
### `<upload>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|extra-button|Extra button|fileItem: `FileItem`|2.43.0|
|image|Image|fileItem: `FileItem`|2.23.0|
|file-name|File name|-|2.23.0|
|file-icon|File icon|-|2.23.0|
|remove-icon|Remove icon|-|2.23.0|
|preview-icon|Preview icon|-|2.23.0|
|cancel-icon|Cancel icon|-|2.23.0|
|start-icon|Start icon|-|2.23.0|
|error-icon|Error icon|-|2.23.0|
|success-icon|Success icon|-|2.23.0|
|retry-icon|Retry icon|-|2.23.0|
|upload-button|Upload button|-||
|upload-item|Upload list item|fileItem: `FileItem`<br>index: `number`||

### FileItem

|Name|Description|Type|Default|
|---|---|---|:---:|
|uid|The unique identifier of the currently uploaded file|`string`|`-`|
|status|The status of the currently uploaded file|`FileStatus`|`-`|
|file|File object|`File`|`-`|
|percent|Upload progress percentage|`number`|`-`|
|response|The response returned by the current file upload request|`any`|`-`|
|url|The file address|`string`|`-`|
|name|The file name|`string`|`-`|

### CustomIcon

|Name|Description|Type|Default|
|---|---|---|:---:|
|startIcon|Start icon|`RenderFunction`|`-`|
|cancelIcon|Cancel icon|`RenderFunction`|`-`|
|retryIcon|Retry icon|`RenderFunction`|`-`|
|successIcon|Success icon|`RenderFunction`|`-`|
|errorIcon|Error icon|`RenderFunction`|`-`|
|removeIcon|Remove icon|`RenderFunction`|`-`|
|previewIcon|Preview icon|`RenderFunction`|`-`|
|fileIcon|File icon|`(fileItem: FileItem) => VNode`|`-`|
|fileName|File name|`(fileItem: FileItem) => string \| VNode`|`-`|

### RequestOption

|Name|Description|Type|Default|
|---|---|---|:---:|
|action|Uploaded URL|`string`|`-`|
|headers|Header information of the request message|`Record<string, string>`|`-`|
|name|File name of the uploaded file|`string \| ((fileItem: FileItem) => string)`|`-`|
|fileItem|upload files|`FileItem`|`-`|
|data|Additional requested information|`Record<string, string \| Blob>    \| ((fileItem: FileItem) => Record<string, string \| Blob>)`|`-`|
|withCredentials|Whether to carry cookie information|`boolean`|`false`|
|onProgress|Update the upload progress of the current file. percent: current upload progress percentage|`(percent: number, event?: ProgressEvent) => void`|`-`|
|onSuccess|After the upload is successful, call the onSuccess method, the incoming response parameter will be appended to the response field of the currently uploaded file|`(response?: any) => void`|`-`|
|onError|After the upload fails, call the onError method, and the response parameter passed in will be appended to the response field of the currently uploaded file|`(response?: any) => void`|`-`|

### UploadRequest

|Name|Description|Type|Default|
|---|---|---|:---:|
|abort|Terminate upload|`() => void`|`-`|
