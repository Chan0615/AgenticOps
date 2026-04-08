---
name: arco-vue-result
description: "It is used to feed back the processing results of a series of operation tasks. It is used when there are important operations that need to inform the user of the processing results and the feedback content is more complicated. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Result

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Show the result status.

```vue
<template>
  <a-result title="This is title content" subtitle="This is subtitle content">
    <template #extra>
      <a-space>
        <a-button type="secondary">Again</a-button>
        <a-button type="primary">Back</a-button>
      </a-space>
    </template>
  </a-result>
</template>
```

## Success

Show success status.

```vue
<template>
  <a-result status="success" title="This is title content" >
    <template #subtitle>
      This is subtitle content
    </template>
    <template #extra>
      <a-space>
        <a-button type='primary'>Back</a-button>
      </a-space>
    </template>
  </a-result>
</template>
```

## Warning

Show warning status.

```vue
<template>
  <a-result status="warning" title="This is title content">
    <template #subtitle>
      This is subtitle content
    </template>

    <template #extra>
      <a-space>
        <a-button type='primary'>Back</a-button>
      </a-space>
    </template>
  </a-result>
</template>
```

## Error

Show error status.

```vue
<template>
  <a-result status="error" title="This is title content">
    <template #subtitle>
      This is subtitle content
    </template>

    <template #extra>
      <a-space>
        <a-button type='primary'>Back</a-button>
      </a-space>
    </template>
  </a-result>
</template>
```

## HTTP Status Code 403

No access to the current page.

```vue
<template>
  <a-result
    status="403"
    subtitle="Access to this resource on the server is denied."
  >
    <template #extra>
      <a-space>
        <a-button type="primary">Back</a-button>
      </a-space>
    </template>
  </a-result>
</template>
```

## HTTP Status Code 404

Page not found

```vue
<template>
  <a-result status="404" subtitle="Whoops, that page is gone.">
    <template #extra>
      <a-space>
        <a-button type="primary">Back</a-button>
      </a-space>
    </template>
  </a-result>
</template>
```

## HTTP Status Code 500

Usually indicates a server error

```vue
<template>
  <a-result status="500" subtitle="This page isn’t working.">
    <template #extra>
      <a-space>
        <a-button type="primary">Back</a-button>
      </a-space>
    </template>
  </a-result>
</template>
```

## Custom Status

Custom Status. You need to set the Icon property

```vue
<template>
  <a-result :status="null" title="This is title content" subtitle="This is subtitle content">
    <template #icon>
      <IconFaceSmileFill />
    </template>
    <template #extra>
      <a-space>
        <a-button type="secondary">Again</a-button>
        <a-button type="primary">Back</a-button>
      </a-space>
    </template>
  </a-result>
</template>
<script>
import { IconFaceSmileFill } from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconFaceSmileFill
  },
}
</script>
```

## All features

All features

```vue
<template>
  <a-result status="error" title="No internet ">
    <template #icon>
      <IconFaceFrownFill />
    </template>
    <template #subtitle> DNS_PROBE_FINISHED_NO_INTERNET </template>

    <template #extra>
      <a-button type="primary">Refresh</a-button>
    </template>
    <a-typography style="background: var(--color-fill-2); padding: 24px;">
      <a-typography-paragraph>Try:</a-typography-paragraph>
      <ul>
        <li> Checking the network cables, modem, and router </li>
        <li> Reconnecting to Wi-Fi </li>
      </ul>
    </a-typography>
  </a-result>
</template>

<script>
import { IconFaceFrownFill } from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconFaceFrownFill
  },
}
</script>
```

## API

### `<result>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|status|The status displayed on the result page|`'info' \| 'success' \| 'warning' \| 'error' \| '403' \| '404' \| '500' \| null`|`'info'`|
|title|Title|`string`|`-`|
|subtitle|Subtitle|`string`|`-`|
### `<result>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|icon|Icon|-||
|title|Title|-||
|subtitle|Subtitle|-||
|extra|Extra|-|2.8.0|
|default|Default|-|2.8.0|
