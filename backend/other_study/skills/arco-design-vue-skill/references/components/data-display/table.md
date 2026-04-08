---
name: arco-vue-table
description: "It is used for data collection, display, analysis and processing, and operation and processing. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Table

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

For the basic usage of the table, you need to pass `columns` and `data`.

```vue
<template>
  <a-table :columns="columns" :data="data" />
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    return {
      columns,
      data
    }
  },
}
</script>
```

## Row Selection

Turn on the row selector by setting `row-selection`.

```vue
<template>
  <a-space direction="vertical" size="large" fill>
    <div>
      <span>OnlyCurrent: </span>
      <a-switch v-model="rowSelection.onlyCurrent" />
    </div>
    <a-table row-key="name" :columns="columns" :data="data" :row-selection="rowSelection"
             v-model:selectedKeys="selectedKeys" :pagination="pagination" />
  </a-space>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const selectedKeys = ref(['Jane Doe', 'Alisa Ross']);

    const rowSelection = reactive({
      type: 'checkbox',
      showCheckedAll: true,
      onlyCurrent: false,
    });
    const pagination = {pageSize: 5}

    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ]
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com',
      disabled: true
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }, {
      key: '6',
      name: 'Jane Doe 2',
      salary: 15000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '7',
      name: 'Alisa Ross 2',
      salary: 28000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '8',
      name: 'Kevin Sandra 2',
      salary: 26000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com',
    }, {
      key: '9',
      name: 'Ed Hellen 2',
      salary: 18000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '10',
      name: 'William Smith 2',
      salary: 12000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    return {
      rowSelection,
      columns,
      data,
      selectedKeys,
      pagination
    }
  },
}
</script>
```

## Row Selection (Radio)

Enable single selection mode by setting `rowSelection.type='radio'`.

```vue
<template>
  <a-table :columns="columns" :data="data" :row-selection="rowSelection" />
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const rowSelection = {
      type: 'radio'
    };
    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ]
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    return {
      rowSelection,
      columns,
      data
    }
  },
}
</script>
```

## Expand Row

Enable the expand line function by setting `expandable`. You can add the `expand` attribute to the `data` to set the expanded line display content.

```vue
<template>
  <a-table :columns="columns" :data="data" :expandable="expandable" />
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const expandable = reactive({
      title: 'Expand',
      width: 80,
      expandedRowRender: (record) => {
        if(record.key==='3'){
          return `My Name is ${record.name}`
        }
      }
    });

    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];

    const data = reactive([
      {
        key: '1',
        name: 'Jane Doe',
        salary: 23000,
        address: '32 Park Road, London',
        email: 'jane.doe@example.com',
        expand: 'Expand Data'
      }, {
        key: '2',
        name: 'Alisa Ross',
        salary: 25000,
        address: '35 Park Road, London',
        email: 'alisa.ross@example.com'
      }, {
        key: '3',
        name: 'Kevin Sandra',
        salary: 22000,
        address: '31 Park Road, London',
        email: 'kevin.sandra@example.com'
      }, {
        key: '4',
        name: 'Ed Hellen',
        salary: 17000,
        address: '42 Park Road, London',
        email: 'ed.hellen@example.com'
      }, {
        key: '5',
        name: 'William Smith',
        salary: 27000,
        address: '62 Park Road, London',
        email: 'william.smith@example.com'
      }
    ]);

    return {
      columns,
      expandable,
      data
    }
  },
}
</script>
```

## Ellipsis And Tooltip

Enable `ellipsis` property to display ellipsis, and also enable `tooltip` to use a text tip when displaying ellipses. Note: Enabling `tooltip` will modify the DOM structure in `table-cell`.

```vue
<template>
  <a-table :columns="columns" :data="data" />
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
        ellipsis: true,
        tooltip: true,
        width: 100
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
        ellipsis: true,
        width: 150,
      },
      {
        title: 'Email',
        dataIndex: 'email',
        ellipsis: true,
        tooltip: {position: 'left'},
        width: 200,
      },
    ];
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    return {
      columns,
      data
    }
  },
}
</script>
```

## SubTree

An example of tree data display, when there is a `children` field in `data`, it will be displayed as a tree table.

```vue

<template>
  <a-space>
    <span>checkStrictly:</span>
    <a-switch v-model="rowSelection.checkStrictly" />
  </a-space>
  <a-table :columns="columns" :data="data" v-model:expandedKeys="expandedKeys" :row-selection="rowSelection" show-empty-tree style="margin-top: 20px"/>
</template>

<script>
import { ref,reactive } from 'vue';

export default {
  setup() {
    const expandedKeys = ref([]);

    const rowSelection = reactive({
      type: 'checkbox',
      showCheckedAll: true,
      checkStrictly: true
    });

    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];
    const data = [{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com',
      children: [
        {
          key: '2',
          name: 'Alisa Ross',
          salary: 25000,
          address: '35 Park Road, London',
          email: 'alisa.ross@example.com',
          children: [
            {
              key: '3',
              name: 'Ed Hellen',
              salary: 17000,
              address: '42 Park Road, London',
              email: 'ed.hellen@example.com'
            }, {
              key: '4',
              name: 'William Smith',
              salary: 27000,
              address: '62 Park Road, London',
              email: 'william.smith@example.com'
            }
          ]
        },
        {
          key: '5',
          name: 'Alisa Ross',
          salary: 25000,
          address: '35 Park Road, London',
          email: 'alisa.ross@example.com'
        }
      ]
    }, {
      key: '6',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '7',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '8',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '9',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com',
      children:[]
    }];

    return {
      columns,
      data,
      expandedKeys,
      rowSelection
    }
  },
}
</script>
```

## Lazy Load

The loading function of sub-slacks can be turned on through the `load-more` property.
After the child slot loading function is enabled, you need to mark `isLeaf: true` on nodes without subtrees. Nodes that are not marked and have no `children` attribute will be considered to need child slot loading processing.
The `load-more` attribute provides a `done` function for callbacks, and lazy loaded subtrees can be passed in the callback. If the `done` function does not pass in data, it will be considered as a lazy loading failure, and this node can trigger lazy loading again.

```vue

<template>
  <a-table :columns="columns" :data="data" :load-more="loadMore" />
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const columns = [{
      title: 'Name',
      dataIndex: 'name',
    }, {
      title: 'Salary',
      dataIndex: 'salary',
    }, {
      title: 'Address',
      dataIndex: 'address',
    }, {
      title: 'Email',
      dataIndex: 'email',
    }];
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com',
      children: [{
        key: '2',
        name: 'Alisa Ross',
        salary: 25000,
        address: '35 Park Road, London',
        email: 'alisa.ross@example.com',
      }, {
        key: '5',
        name: 'Alisa Ross',
        salary: 25000,
        address: '35 Park Road, London',
        email: 'alisa.ross@example.com',
        isLeaf: true,
      }]
    }, {
      key: '6',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com',
    }, {
      key: '7',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com',
      isLeaf: true,
    }, {
      key: '8',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com',
      isLeaf: true,
    }, {
      key: '9',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com',
      isLeaf: true,
    }])

    const loadMore = (record, done) => {
      window.setTimeout(() => {
        done([
          {
            key: `${record.key}-1`,
            name: 'Ed Hellen',
            salary: 17000,
            address: '42 Park Road, London',
            email: 'ed.hellen@example.com',
            isLeaf: true,
          }, {
            key: `${record.key}-2`,
            name: 'William Smith',
            salary: 27000,
            address: '62 Park Road, London',
            email: 'william.smith@example.com',
            isLeaf: true,
          }
        ])
      }, 2000)
    }

    return {
      columns,
      data,
      loadMore
    }
  },
}
</script>
```

## Table Props

Here is a list of some table attributes, you can easily open or close some of the attributes to view its effects.

```vue

<template>
  <a-form layout="inline" :model="form">
    <a-form-item label="Border" field="border">
      <a-switch v-model="form.border" />
    </a-form-item>
    <a-form-item label="Hover" field="hover">
      <a-switch v-model="form.hover" />
    </a-form-item>
    <a-form-item label="stripe" field="stripe">
      <a-switch v-model="form.stripe" />
    </a-form-item>
    <a-form-item label="checkbox" field="checkbox">
      <a-switch v-model="form.checkbox" />
    </a-form-item>
    <a-form-item label="checkAll" field="checkAll">
      <a-switch v-model="rowSelection.showCheckedAll" />
    </a-form-item>
    <a-form-item label="loading" field="loading">
      <a-switch v-model="form.loading" />
    </a-form-item>
    <a-form-item label="tableHeader" field="tableHeader">
      <a-switch v-model="form.tableHeader" />
    </a-form-item>
    <a-form-item label="noData" field="noData">
      <a-switch v-model="form.noData" />
    </a-form-item>
  </a-form>
  <a-table
    :columns="columns"
    :data="form.noData ? [] : data"
    :bordered="form.border"
    :hoverable="form.hover"
    :stripe="form.stripe"
    :loading="form.loading"
    :show-header="form.tableHeader"
    :row-selection="form.checkbox ? rowSelection : undefined"
  />
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const form = reactive({
      border: true,
      borderCell: false,
      hover: true,
      stripe: false,
      checkbox: true,
      loading: false,
      tableHeader: true,
      noData: false
    });

    const rowSelection = reactive({
      type: 'checkbox',
      showCheckedAll: true
    });

    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];

    const data = [{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }];

    return {
      form,
      rowSelection,
      columns,
      data
    }
  },
}
</script>
```

## Sort & Filter

You can configure the sorting and filtering functions by setting the `sortable` and `filterable` attributes in `columns`
. The filter button can be aligned to the left through the `filter-icon-align-left` property. Internal sorting can be
turned off by setting `sortable.sorter=true`, and server-side sorting can be implemented via the `change`
or `sorterChange` events.

```vue
<template>
  <a-space direction="vertical" size="large" fill>
    <a-space>
      <a-switch v-model="alignLeft" />
      <span>Filter icon align left: {{alignLeft}}</span>
    </a-space>
    <a-table :columns="columns" :data="data" :filter-icon-align-left="alignLeft" @change="handleChange" />
  </a-space>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const alignLeft = ref(false);

    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
        sortable: {
          sortDirections: ['ascend', 'descend']
        }
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
        sortable: {
          sortDirections: ['ascend']
        },
        filterable: {
          filters: [{
            text: '> 20000',
            value: '20000',
          }, {
            text: '> 30000',
            value: '30000',
          }],
          filter: (value, record) => record.salary > value,
          multiple: true
        }
      },
      {
        title: 'Address',
        dataIndex: 'address',
        filterable: {
          filters: [{
            text: 'London',
            value: 'London',
          }, {
            text: 'Paris',
            value: 'Paris',
          },],
          filter: (value, row) => row.address.includes(value),
        }
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    const handleChange = (data, extra, currentDataSource) => {
      console.log('change', data, extra, currentDataSource)
    }

    return {
      alignLeft,
      columns,
      data,
      handleChange
    }
  },
}
</script>
```

## Custom Filter Content

The filter menu content can be customized through the slot.

```vue

<template>
  <a-table :columns="columns" :data="data" @change="handleChange">
    <template #name-filter="{ filterValue, setFilterValue, handleFilterConfirm, handleFilterReset}">
      <div class="custom-filter">
        <a-space direction="vertical">
          <a-input :model-value="filterValue[0]" @input="(value)=>setFilterValue([value])" />
          <div class="custom-filter-footer">
            <a-button @click="handleFilterConfirm">Confirm</a-button>
            <a-button @click="handleFilterReset">Reset</a-button>
          </div>
        </a-space>
      </div>
    </template>
  </a-table>
</template>

<script>
import { reactive, h } from 'vue';
import { IconSearch } from '@arco-design/web-vue/es/icon';

export default {
  setup() {
    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
        filterable: {
          filter: (value, record) => record.name.includes(value),
          slotName: 'name-filter',
          icon: () => h(IconSearch)
        }
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
        sortable: {
          sortDirections: ['ascend']
        },
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    const handleChange = (data, extra, currentDataSource) => {
      console.log('change', data, extra, currentDataSource)
    }

    return {
      columns,
      data,
      handleChange
    }
  },
}
</script>

<style>
.custom-filter {
  padding: 20px;
  background: var(--color-bg-5);
  border: 1px solid var(--color-neutral-3);
  border-radius: var(--border-radius-medium);
  box-shadow: 0 2px 5px rgb(0 0 0 / 10%);
}

.custom-filter-footer {
  display: flex;
  justify-content: space-between;
}
</style>
```

## Table Scroll

Setting the scroll property enables table scrolling. x refers to the actual width of the table. Generally, the value set will be larger than the width of the table container; y refers to the display height of the table. When the actual height of the table exceeds, a scroll bar will be displayed.
After version 2.18.0, both x, y can set percentage. Setting y to 100% can make the height of the table container follow the outer container, and automatically display the scroll bar when it exceeds.

```vue
<template>
  <div style="margin-bottom: 20px">
    <a-switch v-model="scrollbar" />
    Virtual Scrollbar
  </div>
  <a-table :columns="columns" :data="data" :scroll="scroll" :scrollbar="scrollbar" />
  <a-split direction="vertical" :default-size="0.9" :style="{height: '500px', marginTop: '30px'}">
    <template #first>
      <a-table :columns="columns" :data="data" :scroll="scrollPercent" :scrollbar="scrollbar" />
    </template>
  </a-split>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const scrollbar = ref(true);
    const scroll = {
      x: 2000,
      y: 200
    };
    const scrollPercent = {
      x: '120%',
      y: '100%'
    };
    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    return {
      scroll,
      scrollPercent,
      columns,
      data,
      scrollbar
    }
  },
}
</script>
```

## Fixed Column

Specify `fixed:'left'` or `fixed:'right'` in `columns` to fix the column to the left or right. Columns with `fixed` must
be set to the width of the column specified by `width`.
**Note**: Use with `:scroll="{ x: number }"`. In addition, there must be at least one column in `columns` that does not
set the width and is adaptive, otherwise there will be style problems.

```vue
<template>
  <a-table :columns="columns" :data="data" :scroll="scroll" :expandable="expandable" />
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
        fixed: 'left',
        width: 140
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
        fixed: 'right',
        width: 200
      },
    ];

    const expandable = {
      title: 'Expand',
      width: 80,
    }

    const scroll = {
      x: 2000,
      y: 200
    }

    const data = reactive([
      {
        key: '1',
        name: 'Jane Doe',
        salary: 23000,
        address: '32 Park Road, London',
        email: 'jane.doe@example.com',
        expand: 'Expand Content'
      }, {
        key: '2',
        name: 'Alisa Ross',
        salary: 25000,
        address: '35 Park Road, London',
        email: 'alisa.ross@example.com'
      }, {
        key: '3',
        name: 'Kevin Sandra',
        salary: 22000,
        address: '31 Park Road, London',
        email: 'kevin.sandra@example.com'
      }, {
        key: '4',
        name: 'Ed Hellen',
        salary: 17000,
        address: '42 Park Road, London',
        email: 'ed.hellen@example.com'
      }, {
        key: '5',
        name: 'William Smith',
        salary: 27000,
        address: '62 Park Road, London',
        email: 'william.smith@example.com'
      }
    ]);

    return {
      columns,
      expandable,
      scroll,
      data
    }
  },
}
</script>
```

## Cell Span

Cell merging is done via the `span-method` property. You can set `span-all` to make the column index include the operation column. Note: At present, if the multiple selectors are merged, the judgment of the all selection state will be wrong.

```vue
<template>
  <a-space direction="vertical" size="large" style="width: 100%">
    <a-table :columns="columns" :data="data" :span-method="spanMethod" />
    <a-table :columns="columns" :data="data" :span-method="dataSpanMethod" :bordered="{wrapper: true, cell: true}" />
    <a-table :columns="columns" :data="data" :row-selection="{type: 'checkbox'}" :span-method="spanMethodAll" span-all :bordered="{wrapper: true, cell: true}" />
  </a-space>
</template>

<script>
export default {
  setup(){
    const spanMethod= ({rowIndex, columnIndex}) => {
      if (rowIndex === 1 && columnIndex === 1) {
        return {
          rowspan: 2,
          colspan: 3
        }
      }
    };
    const  dataSpanMethod= ({record, column}) => {
      if (record.name === 'Alisa Ross' && column.dataIndex === 'salary') {
        return {
          rowspan: 2,
        }
      }
    };
    const  spanMethodAll= ({rowIndex, columnIndex}) => {
      if (rowIndex === 1 && columnIndex === 0) {
        return {rowspan: 2}
      }

      if (rowIndex === 1 && columnIndex === 2) {
        return {
          rowspan: 2,
          colspan: 3
        }
      }
    };
    const columns=[
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];
    const data=[{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }];

    return {
      spanMethod,
      dataSpanMethod,
      spanMethodAll,
      columns,
      data
    }
  },
}
</script>
```

## Sticky Header

Set the header suction via `sticky-header`. The calculation container for the top of the header is the nearest scroll container. When setting the number, you can specify the height from the top of the scroll container.

```vue
<template>
  <a-table :columns="columns" :data="data" :sticky-header="60"/>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    return {
      columns,
      data
    }
  },
}
</script>
```

## Summary

Set `summary` to turn on the summary line at the end of the table, and specify the first column of text
with `summary-text`. If you want to customize the summary line display, you can pass in a function. The return value of
the function is the data to be displayed, the structure is the same as `data`, and it supports multiple rows of data.
Note: The control column cannot be customized for the time being

```vue

<template>
  <a-table :columns="columns" :data="data" :summary="true" :summary-span-method="spanMethod" />
  <a-table :columns="columns" :data="data" :scroll="scroll" :expandable="expandable" :summary="summary">
    <template #summary-cell="{ column,record,rowIndex }">
      <div :style="getColorStyle(column,record)">{{record[column.dataIndex]}}</div>
    </template>
  </a-table>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const expandable = {
      title: 'Expand',
      width: 80
    };
    const scroll = {
      x: 2000,
      y: 200
    }
    const columns = reactive([
      {
        title: 'Name',
        dataIndex: 'name',
        fixed: 'left',
        width: 140
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
        summaryCellStyle: (record) => {
          if (record.salary > 100000) {
            return {
              backgroundColor: 'rgb(var(--arcoblue-6))',
              color: '#fff'
            }
          }
        }
      },
      {
        title: 'Data1',
        dataIndex: 'data1',
      },
      {
        title: 'Data2',
        dataIndex: 'data2',
      },
    ]);
    const data = reactive([
      {
        key: '1',
        name: 'Jane Doe',
        salary: 23000,
        data1: 10,
        data2: 8,
        expand: 'Expand Content'
      }, {
        key: '2',
        name: 'Alisa Ross',
        salary: 25000,
        data1: 9,
        data2: -12,
      }, {
        key: '3',
        name: 'Kevin Sandra',
        salary: 22000,
        data1: 15,
        data2: -2,
      }, {
        key: '4',
        name: 'Ed Hellen',
        salary: 17000,
        data1: 2,
        data2: 3,
      }, {
        key: '5',
        name: 'William Smith',
        salary: 27000,
        data1: 11,
        data2: 0,
      }
    ])

    const summary = ({columns, data}) => {
      let countData = {
        salary: 0,
        data1: 0,
        data2: 0
      };
      data.forEach(record => {
        countData.salary += record.salary;
        countData.data1 += record.data1;
        countData.data2 += record.data2;
      })

      return [{
        name: 'Avg',
        salary: countData.salary / data.length,
        data1: countData.data1 / data.length,
        data2: countData.data2 / data.length,
      }, {
        name: 'Sum',
        salary: countData.salary,
        data1: countData.data1,
        data2: countData.data2,
      }]
    }

    const getColorStyle = (column, record) => {
      if (['data1', 'data2'].includes(column.dataIndex)) {
        return {color: record[column.dataIndex] > 0 ? 'red' : 'green'}
      }
      return undefined
    }

    const spanMethod = ({rowIndex, columnIndex}) => {
      if (rowIndex === 0 && columnIndex === 1) {
        return {
          colspan: 2
        }
      }
    };

    return {
      expandable,
      scroll,
      columns,
      data,
      summary,
      getColorStyle,
      spanMethod
    }
  },
}
</script>
```

## Column Width Resize

Enable column resizing using the `column-resizable` property. It is recommended to initially set default column widths for all but the last column.

```vue
<template>
  <a-table :columns="columns" :data="data" column-resizable :bordered="{cell:true}"></a-table>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const columns = reactive([
      {
        title: 'Name',
        dataIndex: 'name',
        width: 150,
        minWidth: 100,
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
        width: 120,
        minWidth: 80,
      },
      {
        title: 'Address',
        dataIndex: 'address',
        width: 300,
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ]);
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    return {
      columns,
      data
    }
  },
}
</script>
```

## Draggable table

(experimental)
Enable drag and drop function of table rows

```vue
<template>
  <a-table :columns="columns" :data="data" @change="handleChange" :draggable="{}"></a-table>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const columns = reactive([
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ]);
    const data = ref([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);
    const handleChange = (_data) => {
      console.log(_data);
      data.value = _data
    }

    return {
      columns,
      data,
      handleChange
    }
  },
}
</script>
```

## Drag handle

(experimental)
Enable anchor dragging

```vue
<template>
  <a-table :columns="columns" :data="data" @change="handleChange" :draggable="{ type: 'handle', width: 40 }" />
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const columns = reactive([
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Salary',
        dataIndex: 'salary',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ]);
    const data = ref([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);
    const handleChange = (_data) => {
      console.log(_data);
      data.value = _data
    }

    return {
      columns,
      data,
      handleChange
    }
  },
}
</script>
```

## Column Group

`Children` can be set in `columns` for header grouping.

```vue
<template>
  <a-table :columns="columns" :data="data" :bordered="{headerCell:true}"/>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const columns = [{
      title: 'Name',
      dataIndex: 'name',
      fixed: 'left',
      width: 140,
    }, {
      title: 'User Info',
      children: [{
        title: 'Birthday',
        dataIndex: 'birthday'
      }, {
        title: 'Address',
        children: [{
          title: 'City',
          dataIndex: 'city'
        }, {
          title: 'Road',
          dataIndex: 'road'
        }, {
          title: 'No.',
          dataIndex: 'no'
        }]
      }]
    }, {
      title: 'Information',
      children: [{
        title: 'Email',
        dataIndex: 'email',
      }, {
        title: 'Phone',
        dataIndex: 'phone',
      }]
    }, {
      title: 'Salary',
      dataIndex: 'salary',
      fixed: 'right',
      width: 120
    }];
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      birthday: '1994-04-21',
      city: 'London',
      road: 'Park',
      no: '34',
      phone: '12345678',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      birthday: '1994-05-21',
      city: 'London',
      road: 'Park',
      no: '37',
      phone: '12345678',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      birthday: '1992-02-11',
      city: 'Paris',
      road: 'Arco',
      no: '67',
      phone: '12345678',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      birthday: '1991-06-21',
      city: 'London',
      road: 'Park',
      no: '317',
      phone: '12345678',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      birthday: '1996-08-21',
      city: 'Paris',
      road: 'Park',
      no: '114',
      phone: '12345678',
      email: 'william.smith@example.com'
    }]);

    return {
      columns,
      data
    }
  },
}
</script>
```

## Column Group & Fixed Column

When a fixed column is used in the grouping header, the data column needs to be specified as a fixed column first.
If all data columns under a group are fixed columns, you can set the group column to be a fixed column, and the width is the sum of the widths of the sub-columns.

```vue
<template>
  <a-table :columns="columns" :data="data" :bordered="{cell:true}" :scroll="{ x: 2000 }"/>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const columns = [{
      title: 'Name',
      dataIndex: 'name',
      fixed: 'left',
      width: 140,
    }, {
      title: 'User Info',
      children: [{
        title: 'Birthday',
        dataIndex: 'birthday',
        fixed: 'left',
        width: 200,
      }, {
        title: 'Address',
        children: [{
          title: 'City',
          dataIndex: 'city',
          fixed: 'left',
          width: 100,
        }, {
          title: 'Road',
          dataIndex: 'road',
        }, {
          title: 'No.',
          dataIndex: 'no',
        }]
      }]
    }, {
      title: 'Information',
      children: [{
        title: 'Email',
        dataIndex: 'email',
      }, {
        title: 'Phone',
        dataIndex: 'phone',
      }]
    }, {
      title: 'Salary',
      dataIndex: 'salary',
      fixed: 'right',
      width: 120
    }];
    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      birthday: '1994-04-21',
      city: 'London',
      road: 'Park',
      no: '34',
      phone: '12345678',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      birthday: '1994-05-21',
      city: 'London',
      road: 'Park',
      no: '37',
      phone: '12345678',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      birthday: '1992-02-11',
      city: 'Paris',
      road: 'Arco',
      no: '67',
      phone: '12345678',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      birthday: '1991-06-21',
      city: 'London',
      road: 'Park',
      no: '317',
      phone: '12345678',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      birthday: '1996-08-21',
      city: 'Paris',
      road: 'Park',
      no: '114',
      phone: '12345678',
      email: 'william.smith@example.com'
    }]);

    return {
      columns,
      data
    }
  },
}
</script>
```

## Editable

You can use the data obtained from the slot to modify the data in `data` to achieve the function of editing the table.
After the `2.25.0` version, you can directly modify the `record` variable from the slot. This `record` variable is a reference to the corresponding data in the incoming `data`, please make sure that `data` is of Reactive type.

```vue
<template>
  <a-table :columns="columns" :data="data">
    <template #name="{ rowIndex }">
      <a-input v-model="data[rowIndex].name" />
    </template>
    <template #province="{ rowIndex }">
      <a-select v-model="data[rowIndex].province" @change="()=>handleChange(rowIndex)">
        <a-option v-for="value of Object.keys(options)">{{value}}</a-option>
      </a-select>
    </template>
    <template #city="{ rowIndex }">
      <a-select :options="options[data[rowIndex].province] || []" v-model="data[rowIndex].city" />
    </template>
  </a-table>
  <!-- support from v2.25.0  -->
  <a-table :columns="columns" :data="data" style="margin-top: 20px">
    <template #name="{ record, rowIndex }">
      <a-input v-model="record.name" />
    </template>
    <template #province="{ record,rowIndex }">
      <a-select v-model="record.province" @change="()=>{record.city=''}">
        <a-option v-for="value of Object.keys(options)">{{value}}</a-option>
      </a-select>
    </template>
    <template #city="{ record,rowIndex }">
      <a-select :options="options[record.province] || []" v-model="record.city" />
    </template>
  </a-table>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const options = {
      Beijing: ['Haidian', 'Chaoyang', 'Changping'],
      Sichuan: ['Chengdu', 'Mianyang', 'Aba'],
      Guangdong: ['Guangzhou', 'Shenzhen', 'Shantou']
    }
    const columns = [{
      title: 'Name',
      dataIndex: 'name',
      slotName: 'name'
    }, {
      title: 'Salary',
      dataIndex: 'salary',
    }, {
      title: 'Address',
      dataIndex: 'address',
    }, {
      title: 'Province',
      dataIndex: 'province',
      slotName: 'province'
    }, {
      title: 'City',
      dataIndex: 'city',
      slotName: 'city'
    }, {
      title: 'Email',
      dataIndex: 'email',
    }];

    const data = reactive([{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      province: 'Beijing',
      city: 'Haidian',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      province: 'Sichuan',
      city: 'Mianyang',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }]);

    const handleChange = (rowIndex) => {
      data[rowIndex].city = ''
    }
    return {
      options,
      columns,
      data,
      handleChange
    }
  },
}
</script>
```

## Custom Columns

With the `#columns` slot and the `<a-table-column>` component, you can customize the column rendering using the template
method.
**Note**: After using the `#columns` slot, the `columns` attribute will be blocked

```vue
<template>
  <a-table :columns="columns" :data="data">
    <template #optional="{ record }">
      <a-button @click="$modal.info({ title:'Name', content:record.name })">view</a-button>
    </template>
  </a-table>
  <a-table :data="data" style="margin-top: 30px">
    <template #columns>
      <a-table-column title="Name">
        <a-table-column title="First Name" data-index="first"></a-table-column>
        <a-table-column title="Last Name" data-index="last"></a-table-column>
      </a-table-column>
      <a-table-column title="Salary" data-index="salary"></a-table-column>
      <a-table-column title="Address" data-index="address"></a-table-column>
      <a-table-column title="Email" data-index="email"></a-table-column>
      <a-table-column title="Optional">
        <template #cell="{ record }">
          <a-button @click="$modal.info({ title:'Name', content:record.name })">view</a-button>
        </template>
      </a-table-column>
    </template>
  </a-table>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const show = ref(true)

    const columns = [{
      title: 'Name',
      dataIndex: 'name',
    }, {
      title: 'Salary',
      dataIndex: 'salary',
    }, {
      title: 'Address',
      dataIndex: 'address',
    }, {
      title: 'Email',
      dataIndex: 'email',
    }, {
      title: 'Optional',
      slotName: 'optional'
    }];
    const data = [{
      key: '1',
      name: 'Jane Doe',
      first: 'Jane',
      last: 'Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      first: 'Alisa',
      last: 'Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      first: 'Kevin',
      last: 'Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      first: 'Ed',
      last: 'Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      first: 'William',
      last: 'Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }];

    return {
      columns,
      data,
      show
    }
  },
}
</script>
```

## Custom Table Element

The rendering of table elements can be customized through specific slots. Only need to pass in the table element, the
internal attributes will be automatically attached

```vue
<template>
  <a-table :columns="columns" :data="data" row-class="common-row">
    <template #tr>
      <tr class="my-tr" @contextmenu="onContextMenu" />
    </template>
    <template #td>
      <td class="my-td" />
    </template>
  </a-table>
</template>

<script>
export default {
  setup() {
    const onContextMenu = () => {
      console.log('right click')
    }

    const columns = [{
      title: 'Name',
      dataIndex: 'name',
    }, {
      title: 'Salary',
      dataIndex: 'salary',
    }, {
      title: 'Address',
      dataIndex: 'address',
    }, {
      title: 'Email',
      dataIndex: 'email',
    }];
    const data = [{
      key: '1',
      name: 'Jane Doe',
      salary: 23000,
      address: '32 Park Road, London',
      email: 'jane.doe@example.com'
    }, {
      key: '2',
      name: 'Alisa Ross',
      salary: 25000,
      address: '35 Park Road, London',
      email: 'alisa.ross@example.com'
    }, {
      key: '3',
      name: 'Kevin Sandra',
      salary: 22000,
      address: '31 Park Road, London',
      email: 'kevin.sandra@example.com'
    }, {
      key: '4',
      name: 'Ed Hellen',
      salary: 17000,
      address: '42 Park Road, London',
      email: 'ed.hellen@example.com'
    }, {
      key: '5',
      name: 'William Smith',
      salary: 27000,
      address: '62 Park Road, London',
      email: 'william.smith@example.com'
    }];

    return {
      columns,
      data,
      onContextMenu,
    }
  },
}
</script>
```

## Virtual List

Set `virtual-list-props` to enable the virtual list function.
Currently, there are many restrictions on virtual scrolling tables. After enabling virtual scrolling, functions such as expanded rows, tree data, and fixed columns cannot be used.

```vue
<template>
  <a-table :columns="columns" :data="data"  :row-selection="rowSelection"  :virtual-list-props="{height:400}" :pagination="false" :scroll="{x:1000}" />
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
        fixed: 'left',
        width: 140
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
      {
        title: 'Email',
        dataIndex: 'email',
      },
    ];
    const data = reactive(Array(1000).fill(null).map((_, index) => ({
      key: String(index),
      name: `User ${index + 1}`,
      address: '32 Park Road, London',
      email: `user.${index + 1}@example.com`
    })));
    const rowSelection = {
      type: 'checkbox',
      showCheckedAll: true
    };

    return {
      columns,
      data,
      rowSelection
    }
  },
}
</script>
```

## API

### `<table>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|columns|Column info of the table|`TableColumnData[]`|`[]`||
|data|Table data|`TableData[]`|`[]`||
|bordered|Whether to show the border|`boolean \| TableBorder`|`true`||
|hoverable|Whether to show the hover effect|`boolean`|`true`||
|stripe|Whether to enable the stripe effect|`boolean`|`false`||
|size|The size of the table|`'mini' \| 'small' \| 'medium' \| 'large'`|`'large'`||
|table-layout-fixed|The table-layout property of the table is set to fixed. After it is set to fixed, the width of the table will not be stretched beyond 100% by the content.|`boolean`|`false`||
|loading|Whether it is loading state|`boolean\|object`|`false`||
|row-selection|Table row selector configuration|`TableRowSelection`|`-`||
|expandable|Expand row configuration of the table|`TableExpandable`|`-`||
|scroll|Scrolling attribute configuration of the table. The `2.13.0` version adds support for character values. `2.20.0` version adds support for `minWidth`, `maxHeight`.|`{  x?: number \| string;  y?: number \| string;  minWidth?: number \| string;  maxHeight?: number \| string;}`|`-`||
|pagination|Pagination properties configuration|`boolean \| PaginationProps`|`true`||
|page-position|The position of the page selector|`'tl' \| 'top' \| tr' \| 'bl' \| 'bottom' \| 'br'`|`'br'`||
|indent-size|The indentation distance of the tree table|`number`|`16`||
|row-key|Value field of table row `key`|`string`|`'key'`||
|show-header|Whether to show the header|`boolean`|`true`||
|virtual-list-props|Pass the virtual list attribute, pass in this parameter to turn on virtual scrolling [VirtualListProps](#VirtualListProps)|`VirtualListProps`|`-`||
|span-method|Cell merge method (The index starts counting from the data item)|`(data: {  record: TableData;  column: TableColumnData \| TableOperationColumn;  rowIndex: number;  columnIndex: number;}) => { rowspan?: number; colspan?: number } \| void`|`-`|2.10.0|
|span-all|Whether to make the index of the span method contain all|`boolean`|`false`|2.18.0|
|load-more|Data lazy loading function, open the lazy loading function when it is passed in|`(record: TableData, done: (children?: TableData[]) => void) => void`|`-`|2.13.0|
|filter-icon-align-left|Whether the filter icon is aligned to the left|`boolean`|`false`|2.13.0|
|hide-expand-button-on-empty|Whether to hide expand button when subtree is empty|`boolean`|`false`|2.14.0|
|row-class|The class name of the table row element. The `2.34.0` version adds support for function values.|`string\| any[]\| Record<string, any>\| ((record: TableData, rowIndex: number) => any)`|`-`|2.16.0|
|draggable|Table drag and drop sorting configuration|`TableDraggable`|`-`|2.16.0|
|column-resizable|Whether to allow the column width to be adjusted|`boolean`|`false`|2.16.0|
|summary|Show footer summary row|`boolean\| ((params: {    columns: TableColumnData[];    data: TableData[];  }) => TableData[])`|`-`|2.21.0|
|summary-text|The first column of text in the summary line|`string`|`'Summary'`|2.21.0|
|summary-span-method|Cell Merge Method for Summarizing Rows|`(data: {  record: TableData;  column: TableColumnData \| TableOperationColumn;  rowIndex: number;  columnIndex: number;}) => { rowspan?: number; colspan?: number } \| void`|`-`|2.21.0|
|selected-keys|Selected row (controlled mode) takes precedence over `rowSelection`|`(string \| number)[]`|`-`|2.25.0|
|default-selected-keys|The selected row by default (uncontrolled mode) takes precedence over `rowSelection`|`(string \| number)[]`|`-`|2.25.0|
|expanded-keys|Displayed Expanded Row, Subtree (Controlled Mode) takes precedence over `expandable`|`(string \| number)[]`|`-`|2.25.0|
|default-expanded-keys|Expand row, Subtree displayed by default (Uncontrolled mode) takes precedence over `expandable`|`(string \| number)[]`|`-`|2.25.0|
|default-expand-all-rows|Whether to expand all rows by default|`boolean`|`false`|2.25.0|
|sticky-header|Whether to open the sticky header|`boolean\|number`|`false`|2.30.0|
|scrollbar|Whether to enable virtual scroll bar|`boolean \| ScrollbarProps`|`true`|2.38.0|
|show-empty-tree|Whether to display empty subtrees|`boolean`|`false`|2.51.0|
### `<table>` Events

|Event Name|Description|Parameters|version|
|---|---|---|:---|
|expand|Triggered when a row is clicked to expand|rowKey: `string \| number`<br>record: `TableData`||
|expanded-change|Triggered when the expanded data row changes|rowKeys: `(string \| number)[]`||
|select|Triggered when the row selector is clicked|rowKeys: `string \| number[]`<br>rowKey: `string \| number`<br>record: `TableData`||
|select-all|Triggered when the select all selector is clicked|checked: `boolean`||
|selection-change|Triggered when the selected data row changes|rowKeys: `(string \| number)[]`||
|sorter-change|Triggered when the collation changes|dataIndex: `string`<br>direction: `string`||
|filter-change|Triggered when the filter options are changed|dataIndex: `string`<br>filteredValues: `string[]`||
|page-change|Triggered when the table pagination changes|page: `number`||
|page-size-change|Triggered when the number of data per page of the table changes|pageSize: `number`||
|change|Triggered when table data changes|data: `TableData[]`<br>extra: `TableChangeExtra`<br>currentData: `TableData[]`|2.40.0 added currentData|
|cell-mouse-enter|Triggered when hovering into a cell|record: `TableData`<br>column: `TableColumnData`<br>ev: `Event`||
|cell-mouse-leave|Triggered when hovering out of a cell|record: `TableData`<br>column: `TableColumnData`<br>ev: `Event`||
|cell-click|Triggered when a cell is clicked|record: `TableData`<br>column: `TableColumnData`<br>ev: `Event`||
|row-click|Triggered when row data is clicked|record: `TableData`<br>ev: `Event`||
|header-click|Triggered when the header data is clicked|column: `TableColumnData`<br>ev: `Event`||
|column-resize|Triggered when column width is adjusted|dataIndex: `string`<br>width: `number`|2.28.0|
|row-dblclick|Triggered when row data is double clicked|record: `TableData`<br>ev: `Event`||
|cell-dblclick|Triggered when a cell is double clicked|record: `TableData`<br>column: `TableColumnData`<br>ev: `Event`||
|row-contextmenu|Triggered when row data is right clicked|record: `TableData`<br>ev: `Event`||
|cell-contextmenu|Triggered when a cell is right clicked|record: `TableData`<br>column: `TableColumnData`<br>ev: `Event`||
### `<table>` Methods

|Method|Description|Parameters|Return|version|
|---|---|---|:---:|:---|
|selectAll|Set select all state|checked: ` boolean `|-|2.22.0|
|select|Set row selector state|rowKey: ` string \| number \| (string \| number)[] `<br>checked: ` boolean `|-|2.31.0|
|expandAll|Set all expanded state|checked: ` boolean `|-|2.31.0|
|expand|Set select all state|rowKey: ` string \| number \| (string \| number)[] `<br>checked: ` boolean `|-|2.31.0|
|resetFilters|Reset the filter for columns|dataIndex: ` string \| string[] `|-|2.31.0|
|clearFilters|Clear the filter for columns|dataIndex: ` string \| string[] `|-|2.31.0|
|resetSorters|Reset the order of columns|-|-|2.31.0|
|clearSorters|Clear the order of columns|-|-|2.31.0|
### `<table>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|th|Custom th element|column: `TableColumnData`|2.26.0|
|thead|Custom thead element|-|2.26.0|
|empty|Empty|-||
|summary-cell|Content on the right side of the pagination|column: `TableColumnData`<br>record: `TableData`<br>rowIndex: `number`|2.23.0|
|pagination-right|Content on the right side of the pagination|-|2.18.0|
|pagination-left|Content on the left side of the pagination|-|2.18.0|
|td|Custom td element|column: `TableColumnData`<br>record: `TableData`<br>rowIndex: `number`|2.16.0|
|tr|Custom tr element|record: `TableData`<br>rowIndex: `number`|2.16.0|
|tbody|Custom tbody element|-|2.16.0|
|drag-handle-icon|Drag handle icon|-|2.16.0|
|footer|Table Footer|-||
|expand-row|Expand row content|record: `TableData`||
|expand-icon|Expand row icon|expanded: `boolean`<br>record: `TableData`||
|columns|Table column definitions. When enabled, the columns attribute is masked|-||

### `<table-column>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|data-index|Identifies the column information, corresponding to the data in TableData|`string`|`-`||
|title|Column title|`string`|`-`||
|width|Column width|`number`|`-`||
|min-width|Minimum column width|`number`|`-`||
|align|Alignment direction|`TableColumnData['align']`|`-`||
|fixed|Fixed position|`TableColumnData['fixed']`|`-`||
|ellipsis|Whether to display as omitted|`boolean`|`false`||
|sortable|Sorting related options|`TableSortable`|`-`||
|filterable|Filter related options|`TableFilterable`|`-`||
|cell-class|Custom cell class|`ClassName`|`-`|2.36.0|
|header-cell-class|Custom cell class|`ClassName`|`-`|2.36.0|
|body-cell-class|Custom cell class|`ClassName \| ((record: TableData) => ClassName)`|`-`|2.36.0|
|summary-cell-class|Customize summary column cell class|`ClassName \| ((record: TableData) => ClassName)`|`-`|2.36.0|
|cell-style|Custom cell style|`CSSProperties`|`-`|2.11.0|
|header-cell-style|Custom cell style|`CSSProperties`|`-`|2.29.0|
|body-cell-style|Custom cell style|`CSSProperties \| ((record: TableData) => CSSProperties)`|`-`|2.29.0|
|summary-cell-style|Customize summary column cell style|`CSSProperties \| ((record: TableData) => CSSProperties)`|`-`|2.30.0|
|index|index for manually specifying option. Manual specification is no longer required after version 2.26.0|`number`|`-`|2.20.2|
|tooltip|Whether to show text hints when omitted|`boolean\|object`|`false`|2.26.0|
### `<table-column>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|filter-icon|Title|-|2.23.0|
|filter-content|Title|filterValue: `string[]`<br>setFilterValue: `(filterValue: string[]) => void`<br>handleFilterConfirm: `(event: Event) => void`<br>handleFilterReset: `(event: Event) => void`|2.23.0|
|title|Title|-||
|cell|Cell|record: `TableData`<br>column: `TableColumnData`<br>rowIndex: `number`||

## Type

```ts
type Filters = Record<string, string[]>;

type Sorter = { filed: string; direction: 'ascend' | 'descend' } | Record<string, never>;
```

### TableData

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|key|The key of the data row|`string`|`-`||
|expand|Expand row content|`string \| RenderFunction`|`-`||
|children|Sub data|`TableData[]`|`-`||
|disabled|Whether to disable the row selector|`boolean`|`false`||
|isLeaf|Whether it is a leaf node|`boolean`|`false`|2.13.0|

### TableSortable

|Name|Description|Type|Default|
|---|---|---|:---:|
|sortDirections|Supported sort direction|`('ascend' \| 'descend')[]`|`-`|
|sorter|Sorting function. Set to `true` to turn off internal sorting. Version 2.19.0 modifies outgoing data.|`((        a: TableData,        b: TableData,        extra: { dataIndex: string; direction: 'ascend' \| 'descend' }      ) => number)    \| boolean`|`-`|
|sortOrder|Sort direction|`'ascend' \| 'descend' \| ''`|`-`|
|defaultSortOrder|Default sort direction (uncontrolled mode)|`'ascend' \| 'descend' \| ''`|`-`|

### TableFilterData

|Name|Description|Type|Default|
|---|---|---|:---:|
|text|Filter the content of the data option|`string \| RenderFunction`|`-`|
|value|Filter the value of the data option|`string`|`-`|

### TableFilterable

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|filters|Filter data|`TableFilterData[]`|`-`||
|filter|Filter function|`(filteredValue: string[], record: TableData) => boolean`|`-`||
|multiple|Whether to support multiple selection|`boolean`|`false`||
|filteredValue|Filter value|`string[]`|`-`||
|defaultFilteredValue|Default filter value|`string[]`|`-`||
|renderContent|The content of filter box|`(data: {    filterValue: string[];    setFilterValue: (filterValue: string[]) => void;    handleFilterConfirm: (event: Event) => void;    handleFilterReset: (event: Event) => void;  }) => VNodeChild`|`-`||
|icon|Filter icon for button|`RenderFunction`|`-`||
|triggerProps|Pop-up box configuration of filter box|`TriggerProps`|`-`||
|alignLeft|Whether the filter icon is aligned to the left|`boolean`|`false`|2.13.0|

### TableColumnData

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|dataIndex|The identifier of the column information, corresponding to the data in `TableData`|`string`|`-`||
|title|Column header|`string \| RenderFunction`|`-`||
|width|Column width|`number`|`-`||
|minWidth|Minimum column width|`number`|`-`||
|align|Alignment direction|`'left' \| 'center' \| 'right'`|`-`||
|fixed|Fixed position|`'left' \| 'right'`|`-`||
|ellipsis|Whether to show ellipsis|`boolean`|`false`||
|tooltip|Whether to show a text hint when an ellipsis is displayed. Can be filled in tooltip component properties|`boolean \| Record<string, any>`|`-`|2.26.0|
|sortable|Sorting related options|`TableSortable`|`-`||
|filterable|Filter related options|`TableFilterable`|`-`||
|children|Header sub-data, used for header grouping|`TableColumnData[]`|`-`||
|cellClass|Custom cell class|`ClassName`|`-`|2.36.0|
|headerCellClass|Custom header cell class|`ClassName`|`-`|2.36.0|
|bodyCellClass|Custom body cell class|`ClassName \| ((record: TableData) => ClassName)`|`-`|2.36.0|
|summaryCellClass|Custom body cell class|`ClassName \| ((record: TableData) => ClassName)`|`-`|2.36.0|
|cellStyle|Custom cell style|`CSSProperties`|`-`|2.11.0|
|headerCellStyle|Custom header cell style|`CSSProperties`|`-`|2.29.0|
|bodyCellStyle|Custom body cell style|`CSSProperties \| ((record: TableData) => CSSProperties)`|`-`|2.29.0|
|summaryCellStyle|Custom summary cell style|`CSSProperties \| ((record: TableData) => CSSProperties)`|`-`|2.30.0|
|render|Customize the rendering of column cells|`(data: {    record: TableData;    column: TableColumnData;    rowIndex: number;  }) => VNodeChild`|`-`||
|slotName|Sets the name of the render slot for the current column. Slot parameters are the same as #cell|`string`|`-`|2.18.0|
|titleSlotName|Set the name of the render slot for the header of the current column|`string`|`-`|2.23.0|

### TableBorder

|Name|Description|Type|Default|
|---|---|---|:---:|
|wrapper|Whether to display the outer border|`boolean`|`false`|
|cell|Whether to display the cell border (header + body)|`boolean`|`false`|
|headerCell|Whether to display the header cell border|`boolean`|`false`|
|bodyCell|Whether to display the body cell border|`boolean`|`false`|

### TableRowSelection

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|type|The type of row selector|`'checkbox' \| 'radio'`|`-`||
|selectedRowKeys|Selected row (controlled mode)|`BaseType[]`|`-`||
|defaultSelectedRowKeys|The selected row by default (uncontrolled mode)|`BaseType[]`|`-`||
|showCheckedAll|Whether to show the select all selector|`boolean`|`false`||
|title|Column title|`string`|`-`||
|width|Column width|`number`|`-`||
|fixed|Is it fixed|`boolean`|`false`||
|checkStrictly|Whether to enable strict selection mode|`boolean`|`true`|2.29.0|
|onlyCurrent|Whether to display only the keys of the current page (clear keys when switching paging)|`boolean`|`false`|2.32.0|

### TableExpandable

|Name|Description|Type|Default|
|---|---|---|:---:|
|expandedRowKeys|Displayed Expanded Row (Controlled Mode)|`BaseType[]`|`-`|
|defaultExpandedRowKeys|Expand row displayed by default (Uncontrolled mode)|`BaseType[]`|`-`|
|defaultExpandAllRows|Whether to expand all rows by default|`boolean`|`false`|
|expandedRowRender|Customize expanded row content|`(record: TableData) => VNodeChild`|`-`|
|icon|Expand icon|`(expanded: boolean, record: TableData) => VNodeChild`|`-`|
|title|Column title|`string`|`-`|
|width|Column width|`number`|`-`|
|fixed|Is it fixed|`boolean`|`false`|

### TableDraggable

|Name|Description|Type|Default|
|---|---|---|:---:|
|type|drag type|`'row' \| 'handle'`|`-`|
|title|Column title|`string`|`-`|
|width|Column width|`number`|`-`|
|fixed|Is it fixed|`boolean`|`false`|

### TableChangeExtra

|Name|Description|Type|Default|
|---|---|---|:---:|
|type|Trigger type|`'pagination' \| 'sorter' \| 'filter' \| 'drag'`|`-`|
|page|page number|`number`|`-`|
|pageSize|number per page|`number`|`-`|
|sorter|Sort information|`Sorter`|`-`|
|filters|Filter information|`Filters`|`-`|
|dragTarget|Drag and drop information|`TableData`|`-`|

### VirtualListProps

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|height|Viewable area height|`number \| string`|`-`||
|threshold|The threshold of the number of elements to enable virtual scrolling. When the number of data is less than the threshold, virtual scrolling will not be enabled.|`number`|`-`||
|isStaticItemHeight|(Repealed) Is the element height fixed. Version 2.18.0 deprecated, please use `fixedSize`|`boolean`|`false`||
|fixedSize|Is the element height fixed.|`boolean`|`false`|2.34.1|
|estimatedSize|Is the element height fixed.|`number`|`-`|2.34.1|
|buffer|The number of elements mounted in advance outside the boundary of the viewport.|`number`|`10`|2.34.1|

## FAQ

The table component provides custom slots for internal elements, which are different from normal slots and have certain restrictions on what the user can pass in.
Because the slot of vue does not provide a way to send out children and render them in the slot, we have done some special processing for the element slot in the table, and will append the original children to the content passed in by the user to ensure that children Normal rendering of the element.
At this point, the user needs to pay attention that when custom rendering in the element slot, a single empty element needs to be passed in, and content cannot be added to the passed in element (refer to Example 1).
If the user needs to pass in a composite element, he can customize the component, specify the default slot, and then pass it into the element slot of the table (refer to Example 2).

example 1:
```vue
<!-- Only one element -->
<template>
  <a-table>
    <template #td>
      <td @click="onClick"></td>
    </template>
  </a-table>
</template>
```
example 2：
```vue
<!-- Only one component -->
<template>
  <a-table>
    <template #td>
      <MyTd></MyTd>
    </template>
  </a-table>
</template>
```
```vue
<!-- MyTd.vue -->
<template>
  <td>
    <div>my td content</div>
    <div>
      <slot/>
    </div>
  </td>
</template>
```

### 2. About the `row-key` setting in the data

By default, the table will uniquely locate the row data through the `key` field set in the data. When providing data, please ensure that the `key` field is set in the row data. This field is a necessary field when enabling functions such as selectors. If you want to change the default field name, you can modify `row-key` to set it.
