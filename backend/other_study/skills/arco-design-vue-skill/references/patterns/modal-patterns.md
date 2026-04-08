---
name: arco-vue-modal-patterns
description: "Arco Design Pro Vue modal patterns. Use for confirm flows, edit dialogs, modal vs drawer choices, and close-after-success behavior."
user-invocable: false
---

# Modal Patterns

## Choose the right feedback primitive

- `Message`: one-line transient feedback after save, delete, refresh, or copy
- `Notification`: richer global event feedback
- `Popconfirm`: low-friction confirmation on one button
- `Modal`: compact dialog that blocks the current task
- `Drawer`: larger edit or detail flow that needs more fields or context

## When to use a modal

Use a modal for:

- short confirmation flows
- compact edit tasks
- destructive actions that need an extra decision

Do not use a modal for long, multi-section business forms when a drawer or full page would read better.

## Close behavior

- keep the modal open while an async submit is pending
- close only after success
- preserve user input if the request fails

## Async submit modal example

```vue
<template>
  <a-modal v-model:visible="visible" :confirm-loading="loading" @ok="handleOk">
    <a-form :model="form" layout="vertical">
      <a-form-item field="reason" label="Reason">
        <a-input v-model="form.reason" />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue';
import useLoading from '@/hooks/loading';

const visible = ref(false);
const form = reactive({ reason: '' });
const { loading, setLoading } = useLoading(false);

const handleOk = async () => {
  setLoading(true);
  try {
    // await submitAction(form);
    visible.value = false;
  } finally {
    setLoading(false);
  }
};
</script>
```

## Confirmation copy

Confirmation text should answer two questions:

- what action is about to happen
- what object or record it affects

## Drawer vs modal

Choose a drawer when the task needs more fields, more explanation, or side-by-side context from the underlying page.

## Common mistakes

- closing the modal before the request succeeds
- using a modal for a form that should be a drawer or full page
- putting complex table filters inside a modal instead of on the page
- showing generic success copy without naming the business action
