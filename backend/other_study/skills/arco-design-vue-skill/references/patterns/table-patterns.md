---
name: arco-vue-table-patterns
description: "Arco Design Pro Vue table patterns. Use for search tables, remote data, column slots, row actions, and pagination wiring."
user-invocable: false
---

# Table Patterns

## End-to-end search table recipe

Use this pattern when the task sounds like:

- "build a search table page"
- "add filter form and result table"
- "create a management list page"

Recommended file set:

1. `src/views/<domain>/<page>/index.vue`
2. `src/router/routes/modules/<domain>.ts`
3. page locale files
4. `src/api/<feature>.ts`
5. mock data if the project still relies on mock endpoints

Recommended page shape:

1. `Breadcrumb`
2. `a-card.general-card`
3. `a-form` filter area
4. action buttons
5. `a-table`

Minimal skeleton:

```vue
<template>
  <div class="container">
    <Breadcrumb :items="['menu.list', 'menu.list.searchTable']" />
    <a-card class="general-card" :title="$t('menu.list.searchTable')">
      <a-form :model="formModel" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item field="keyword" :label="$t('list.keyword')">
              <a-input v-model="formModel.keyword" allow-clear />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item field="status" :label="$t('list.status')">
              <a-select v-model="formModel.status" :options="statusOptions" />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
      <a-space style="margin-bottom: 16px">
        <a-button type="primary" @click="search">{{ $t('list.search') }}</a-button>
        <a-button @click="reset">{{ $t('list.reset') }}</a-button>
      </a-space>
      <a-table
        row-key="id"
        :loading="loading"
        :data="rows"
        :columns="columns"
        :pagination="pagination"
        @page-change="onPageChange"
      />
    </a-card>
  </div>
</template>

<script lang="ts" setup>
import { computed, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import useLoading from '@/hooks/loading';
import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';

const { t } = useI18n();
const { loading, setLoading } = useLoading(true);

const createInitialFilters = () => ({
  keyword: '',
  status: '',
});

const formModel = reactive(createInitialFilters());
const rows = ref([]);
const pagination = reactive({ current: 1, pageSize: 20, total: 0 });

const statusOptions = computed(() => [
  { label: t('list.status.online'), value: 'online' },
  { label: t('list.status.offline'), value: 'offline' },
]);

const columns = computed<TableColumnData[]>(() => [
  { title: t('list.columns.name'), dataIndex: 'name' },
  { title: t('list.columns.status'), dataIndex: 'status' },
  { title: t('list.columns.updatedAt'), dataIndex: 'updatedAt' },
]);

const fetchData = async (current = 1) => {
  setLoading(true);
  try {
    // const { data } = await queryList({ current, pageSize: pagination.pageSize, ...formModel });
    // rows.value = data.list;
    // pagination.total = data.total;
    pagination.current = current;
  } finally {
    setLoading(false);
  }
};

const search = () => fetchData(1);
const reset = () => {
  Object.assign(formModel, createInitialFilters());
  fetchData(1);
};
const onPageChange = (page: number) => fetchData(page);
</script>
```

## Standard search table shape

A common Arco Pro Vue list page contains:

1. `Breadcrumb`
2. filter form
3. action bar
4. `a-table`
5. page-local loading and pagination state

## Remote data pattern

- keep request helpers in `src/api/*.ts`
- call them from the page SFC
- set loading before the request and clear it in `finally`
- keep filter state and pagination state synchronized with the request payload

## Operation column pattern

- use a dedicated operation column or slot
- put destructive actions behind `Popconfirm` or `Modal.confirm`
- protect privileged actions with `v-permission`
- avoid mixing navigation, mutation, and download actions into one unreadable cell

## Column pattern

- define columns together in one computed or constant block
- use `slotName` for rich cell rendering
- keep operation columns explicit and permission-aware
- localize headers when the page already uses i18n

## Quality bar

- reset should restore the filter model and reload the table consistently
- row actions should not drift from permission rules
- pagination should remain stable after filter changes and refreshes
- the request payload should be derivable from one obvious place in the page
