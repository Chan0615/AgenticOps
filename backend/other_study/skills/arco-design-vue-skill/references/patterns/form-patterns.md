---
name: arco-vue-form-patterns
description: "Arco Design Pro Vue form patterns. Use for search forms, edit forms, validation, async submit, and multi-section business forms."
user-invocable: false
---

# Form Patterns

## End-to-end page recipe

Use this when the task is "build a create page", "build an edit page", or "add a settings form".

Required files usually are:

1. `src/views/<domain>/<page>/index.vue`
2. `src/router/routes/modules/<domain>.ts` if the page is routed
3. locale files for page text and menu title
4. `src/api/<feature>.ts` when submit or load data is required

Recommended page skeleton:

```vue
<template>
  <div class="container">
    <Breadcrumb :items="['menu.form', 'menu.form.group']" />
    <a-card class="general-card" :title="$t('menu.form.group')">
      <a-form :model="form" layout="vertical" @submit="handleSubmit">
        <a-form-item field="name" :label="$t('form.name')">
          <a-input v-model="form.name" />
        </a-form-item>
        <a-form-item field="type" :label="$t('form.type')">
          <a-select v-model="form.type" :options="typeOptions" />
        </a-form-item>
        <a-space>
          <a-button type="primary" :loading="loading" html-type="submit">
            {{ $t('form.submit') }}
          </a-button>
          <a-button @click="reset">{{ $t('form.reset') }}</a-button>
        </a-space>
      </a-form>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
import { computed, reactive } from 'vue';
import { useI18n } from 'vue-i18n';
import { Message } from '@arco-design/web-vue';
import useLoading from '@/hooks/loading';

const { t } = useI18n();
const { loading, setLoading } = useLoading(false);

const createInitialForm = () => ({
  name: '',
  type: 'internal',
});

const form = reactive(createInitialForm());
const typeOptions = computed(() => [
  { label: t('form.type.internal'), value: 'internal' },
  { label: t('form.type.external'), value: 'external' },
]);

const reset = () => {
  Object.assign(form, createInitialForm());
};

const handleSubmit = async () => {
  setLoading(true);
  try {
    // await saveFeature(form);
    Message.success(t('form.submitSuccess'));
  } finally {
    setLoading(false);
  }
};
</script>
```

## Search form inside a list page

Common pattern:

1. page-level `formModel`
2. `a-form` inside a `general-card`
3. filter controls using `v-model`
4. `search()` converts current filters into request params
5. `reset()` restores default filter state

## Edit form inside a page or drawer

Use this when the business task is more complex than a confirmation dialog.

- keep a typed or clearly shaped reactive form model
- localize labels and action text
- show submit loading explicitly
- close the drawer or return from the page only after success

## Field rules that matter in business pages

- Use `field` names that match your payload shape.
- Keep enum values stable and translate labels separately.
- Use `a-switch`, `a-checkbox`, `a-date-picker`, and `a-upload` only after checking the backend contract for boolean, date, and file payload shape.
- If the page edits existing data, normalize API data into the form model once instead of mutating fields from multiple watchers.

## Validation rules

- keep validation inside `a-form` instead of scattered watchers
- use stable `field` names
- reflect backend-required fields clearly in the UI
- test boolean fields, date ranges, and upload fields carefully

## Async submit checklist

- disable duplicate submission
- show loading state on the main action
- preserve field values on failure
- surface backend validation errors with useful copy
- call `Message.success(...)` or `Message.error(...)` with business-specific text, not generic "Success"
