---
name: arco-vue-verification-code
description: "Verification code input component. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# VerificationCode

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage

```vue
<template>
  <a-verification-code v-model="value" style="width: 300px" @finish="onFinish" />
</template>

<script setup>
import { ref } from 'vue';
import { Message} from '@arco-design/web-vue';

const value = ref('654321');
const onFinish = (value) => Message.info(`Verification code: ${value}`);
</script>
```
## Different status

Disabled, readonly, error status.

```vue
<template>
  <a-space direction="vertical">
    <a-space>
      <a-typography-text style="width: 80px">Disabled:</a-typography-text>
      <a-verification-code defaultValue="123456" style="width: 300px" disabled />
    </a-space>
    <a-space>
      <a-typography-text  style="width: 80px">Readonly:</a-typography-text>
      <a-verification-code defaultValue="123456" style="width: 300px" readonly />
    </a-space>
    <a-space>
      <a-typography-text style="width: 80px">Error:</a-typography-text>
      <a-verification-code defaultValue="123456" style="width: 300px" error />
    </a-space>
  </a-space>
</template>
```
## Masked

Use `masked = true` to turn on password mode

```vue
<template>
  <a-verification-code defaultValue="123" style="width: 300px"  masked @finish="onFinish" />
</template>

<script setup>
import { Message} from '@arco-design/web-vue';

const onFinish = (value) => Message.info(`Verification code: ${value}`);
</script>
```
## Custom separator

Specify `separator` to customize the rendering separator

```vue
<template>
  <a-verification-code
    style="width: 400px"
    :length="9"
    :separator="(index) => (index + 1) % 3 || index > 7 ? null : '-'"
    @finish="(value) => Message.info(`Verification code: ${value}`)"
  />
</template>

<script setup>
import { Message} from '@arco-design/web-vue';
</script>
```
## With Form

Use with forms to implement verification.

```vue
<template>
  <a-form ref="formRef" :model="form" style="width: 300px">
    <a-form-item
      field="code"
      label="code"
      :rules="[
        {required:true,message:'Verification code is required'},
        {minLength:6, message:'Verification code is incomplete'},
        { match: /^\d+$/, message: 'Must be numeric' },
      ]"
    >
      <a-verification-code v-model="form.code" style="width: 300px" @finish="onFinish" />
    </a-form-item>
    <a-form-item>
      <a-button style="width: 60px" type='primary' size='large' htmlType='submit'>Submit</a-button>
    </a-form-item>
  </a-form>
</template>

<script setup>
import { ref } from 'vue';
import { Message} from '@arco-design/web-vue';

const value = ref('654321');
const formRef = ref(null);
const form = ref({
  code: '',
})
const onFinish = (value) => Message.info(`Verification code: ${value}`);
</script>
```
## Formatter input

Validate input using `formatter`. Additionally, it can return non-boolean types to format the user-entered string into a specific format.

```vue
<template>
  <a-space direction="vertical">
    <a-verification-code
      defaultValue='123456'
      style="width: 300px"
      :formatter="(inputValue) =>  /^\d*$/.test(inputValue) ? inputValue : false"
    />
    <a-verification-code
      defaultValue='abcdef'
      style="width: 300px"
      :formatter="(inputValue) => /^[a-zA-Z]*$/.test(inputValue) ? inputValue.toUpperCase() : ''"
    />
  </a-space>
</template>
```

## API

### `<verification-code>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|model-value **(v-model)**|Value|`string`|`-`|
|default-value|Default value (uncontrolled state)|`string`|`''`|
|length|The length of the verification code, rendering the corresponding number of input boxes according to the length.|`number`|`6`|
|size|Input size|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`|
|disabled|Whether to disable|`boolean`|`false`|
|masked|Password mode|`boolean`|`false`|
|readonly|Readonly|`boolean`|`false`|
|error|Whether it is an error state|`boolean`|`false`|
|separator|Separator. Customizable rendering separators after input boxes with different indexes|`(index: number, character: string) => VNode`|`-`|
|formatter|Formatter function, triggered when the user input value changes|`(inputValue: string, index: number, value: string) => string \| boolean`|`-`|
### `<verification-code>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when the value changes|value: ` string `|
|finish|Triggered when the filling is complete|value: ` string `|
|input|Triggered on input|inputValue: ` string `<br>index: ` number `<br>ev: `Event`|
