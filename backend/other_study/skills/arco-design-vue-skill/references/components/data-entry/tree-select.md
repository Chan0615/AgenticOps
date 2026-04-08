---
name: arco-vue-tree-select
description: "The tree structure data can be selected. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# TreeSelect

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

Basic usage example.

```vue
<template>
  <a-tree-select
    :data="treeData"
    placeholder="Please select ..."
    style="width: 300px"
  ></a-tree-select>
</template>
<script>
  import { h } from 'vue';
  import { IconCalendar } from '@arco-design/web-vue/es/icon';

  export default {
    setup() {
      return {
        treeData,
      };
    },
  };

  const treeData = [
    {
      key: 'node1',
      icon: () => h(IconCalendar),
      title: 'Trunk',
      disabled: true,
      children: [
        {
          key: 'node2',
          title: 'Leaf',
        },
      ],
    },
    {
      key: 'node3',
      title: 'Trunk2',
      icon: () => h(IconCalendar),
      children: [
        {
          key: 'node4',
          title: 'Leaf',
        },
        {
          key: 'node5',
          title: 'Leaf',
        },
      ],
    },
  ];
</script>
```

## Value Format

When `labelInValue` is `true`, the format of `value` is: `{ label: string, value: string }`.

```vue
<template>
  <a-tree-select
    :data="treeData"
    :label-in-value="true"
    :default-value="{ value: 'node2', label: 'Leaf' }"
    placeholder="Please select ..."
    style="width: 300px"
    @change="onChange"
  ></a-tree-select>
</template>
<script>
  import { h } from 'vue';
  import { IconCalendar } from '@arco-design/web-vue/es/icon';

  export default {
    setup() {
      function onChange(value) {
        console.log(value);
      }

      return {
        onChange,
        treeData,
      };
    },
  };

  const treeData = [
    {
      key: 'node1',
      icon: () => h(IconCalendar),
      title: 'Trunk',
      disabled: true,
      children: [
        {
          key: 'node2',
          title: 'Leaf',
        },
      ],
    },
    {
      key: 'node3',
      title: 'Trunk2',
      icon: () => h(IconCalendar),
      children: [
        {
          key: 'node4',
          title: 'Leaf',
        },
        {
          key: 'node5',
          title: 'Leaf',
        },
      ],
    },
  ];
</script>
```

## Two-way binding

The selected value supports two-way binding.

```vue
<template>
  <a-tree-select
    :data="treeData"
    v-model="selected"
    placeholder="Please select ..."
    style="width: 300px"
  ></a-tree-select>
</template>
<script>
  import { h, ref } from 'vue';
  import { IconCalendar } from '@arco-design/web-vue/es/icon';

  export default {
    setup() {
      const selected = ref('node2');

      return {
        selected,
        treeData,
      };
    },
  };

  const treeData = [
    {
      key: 'node1',
      icon: () => h(IconCalendar),
      title: 'Trunk',
      disabled: true,
      children: [
        {
          key: 'node2',
          title: 'Leaf',
        },
      ],
    },
    {
      key: 'node3',
      title: 'Trunk2',
      icon: () => h(IconCalendar),
      children: [
        {
          key: 'node4',
          title: 'Leaf',
        },
        {
          key: 'node5',
          title: 'Leaf',
        },
      ],
    },
  ];
</script>
```

## Dynamic Loading

Load nodes dynamically via `loadMore`. At this time, `isLeaf` can be set to indicate leaf nodes.

```vue
<template>
  <a-tree-select
    :data="treeData"
    :load-more="loadMore"
    placeholder="Please select ..."
    style="width: 300px"
  ></a-tree-select>
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const treeData = ref(defaultTreeData);
      const loadMore = (nodeData) => {
        const { title, key } = nodeData;
        const children = [
          { title: `${title}-0`, value: `${title}-0`, key: `${key}-0` },
          { title: `${title}-1`, value: `${title}-1`, key: `${key}-1` },
        ];

        return new Promise((resolve) => {
          setTimeout(() => {
            nodeData.children = children;
            resolve();
          }, 1000);
        });
      };

      return {
        treeData,
        loadMore,
      };
    },
  };

  const defaultTreeData = [
    {
      key: 'node1',
      title: 'node1',
      disabled: true,
      children: [
        {
          key: 'node2',
          title: 'node2',
        },
      ],
    },
    {
      key: 'node3',
      title: 'node3',
      children: [
        {
          key: 'node4',
          title: 'node4',
          isLeaf: true,
        },
        {
          key: 'node5',
          title: 'node5',
          isLeaf: true,
        },
      ],
    },
  ];
</script>
```

## Search

Set `:allow-search="true"` to enable the search function. You can only search in the loaded data during dynamic loading. The default keyword search is to match from the `value` field. You can also pass in `filterTreeNode` to customize the filtering method.

```vue
<template>
  <a-space>
    <a-tree-select
      :allow-search="true"
      :allow-clear="true"
      :data="treeData"
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
    <a-tree-select
      :allow-search="true"
      :allow-clear="true"
      :data="treeData"
      :filter-tree-node="filterTreeNode"
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
  </a-space>
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      function filterTreeNode(searchValue, nodeData) {
        return nodeData.title.toLowerCase().indexOf(searchValue.toLowerCase()) > -1;
      }

      return {
        filterTreeNode,
        treeData,
      };
    },
  };

  const treeData = [
    {
      title: 'Trunk 0-0',
      key: '0-0',
      children: [
        {
          title: 'Branch 0-0-1',
          key: '0-0-1',
          children: [
            {
              title: 'Leaf 0-0-1-1',
              key: '0-0-1-1'
            },
            {
              title: 'Leaf 0-0-1-2',
              key: '0-0-1-2'
            }
          ]
        },
      ],
    },
    {
      title: 'Trunk 0-1',
      key: '0-1',
      children: [
        {
          title: 'Branch 0-1-1',
          key: '0-1-1',
          children: [
            {
              title: 'Leaf 0-1-1-0',
              key: '0-1-1-0',
            }
          ]
        },
        {
          title: 'Branch 0-1-2',
          key: '0-1-2',
          children: [
            {
              title: 'Leaf 0-1-2-0',
              key: '0-1-2-0',
            }
          ]
        },
      ],
    },
  ];
</script>
```

## Remote search

Listen to the `search` event, get the data in the event processing function and update the `treeData`. When customizing the search logic, it is recommended to turn off the internal filtering logic (`:disable-filter="true"`) to prevent the customized results be affected.

```vue
<template>
  <a-tree-select
    :allow-search="true"
    :allow-clear="true"
    :disable-filter="true"
    :data="treeData"
    :loading="loading"
    style="width: 300px"
    placeholder="Please select ..."
    @search="onSearch"
  ></a-tree-select>
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const treeData = ref(defaultTreeData);
      const loading = ref(false);

      function searchData(keyword) {
        const loop = (data) => {
          const result = [];
          data.forEach(item => {
            if (item.title.toLowerCase().indexOf(keyword.toLowerCase()) > -1) {
              result.push({...item});
            } else if (item.children) {
              const filterData = loop(item.children);
              if (filterData.length) {
                result.push({
                  ...item,
                  children: filterData
                })
              }
            }
          })
          return result;
        }

        return loop(defaultTreeData);
      }

      const onSearch = (searchKey) => {
        loading.value = true;
        setTimeout(() => {
          loading.value = false;
          treeData.value = searchData(searchKey);
        }, 200)
      };

      return {
        treeData,
        loading,
        onSearch,
      };
    },
  };

  const defaultTreeData = [
    {
      title: 'Trunk 0-0',
      key: '0-0',
      children: [
        {
          title: 'Branch 0-0-1',
          key: '0-0-1',
          children: [
            {
              title: 'Leaf 0-0-1-1',
              key: '0-0-1-1'
            },
            {
              title: 'Leaf 0-0-1-2',
              key: '0-0-1-2'
            }
          ]
        },
      ],
    },
    {
      title: 'Trunk 0-1',
      key: '0-1',
      children: [
        {
          title: 'Branch 0-1-1',
          key: '0-1-1',
          children: [
            {
              title: 'Leaf 0-1-1-0',
              key: '0-1-1-0',
            }
          ]
        },
        {
          title: 'Branch 0-1-2',
          key: '0-1-2',
          children: [
            {
              title: 'Leaf 0-1-2-0',
              key: '0-1-2-0',
            }
          ]
        },
      ],
    },
  ];
</script>
```

## Size

Four sizes (small, default, large, huge) can be selected through `size`. The height corresponds to 24px, 28px, 32px, 36px.

```vue
<template>
  <div style="margin-bottom: 20px;">
    <a-radio-group v-model="size" type='button'>
      <a-radio value="mini">mini</a-radio>
      <a-radio value="small">small</a-radio>
      <a-radio value="medium">medium</a-radio>
      <a-radio value="large">large</a-radio>
    </a-radio-group>
  </div>
  <a-tree-select
    defaultValue="node1"
    :size="size"
    :data="treeData"
    placeholder="Please select ..."
    style="width: 300px;"
  ></a-tree-select>
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const size = ref('medium');

      return {
        size,
        treeData,
      };
    },
  };

  const treeData = [
    {
      key: 'node1',
      title: 'node1',
      disabled: true,
      children: [
        {
          key: 'node2',
          title: 'node2',
        },
      ],
    },
    {
      key: 'node3',
      title: 'node3',
      children: [
        {
          key: 'node4',
          title: 'node4',
          isLeaf: true,
        },
        {
          key: 'node5',
          title: 'node5',
          isLeaf: true,
        },
      ],
    },
  ];
</script>
```

## Dropdown Header and Footer

Custom Tree Select the header and footer of the drop-down box.

```vue
<template>
  <a-form layout="inline" :model="form">
   <a-form-item label="empty">
      <a-switch v-model="form.empty" />
    </a-form-item>
    <a-form-item label="showHeaderOnEmpty">
      <a-switch v-model="form.showHeaderOnEmpty" />
    </a-form-item>
    <a-form-item label="showFooterOnEmpty">
      <a-switch v-model="form.showFooterOnEmpty" />
    </a-form-item>
  </a-form>
  <a-tree-select
    style="width: 300px"
    placeholder="Please select ..."
    :data="computedTreeData"
    :show-header-on-empty="form.showHeaderOnEmpty"
    :show-footer-on-empty="form.showFooterOnEmpty"
  >
    <template #header>
      <div style="padding: 6px 12px;" >
        <a-checkbox value="1">All</a-checkbox>
      </div>
    </template>
      <template #footer>
      <div style="padding: 6px 0; text-align: center;">
        <a-button>Click Me</a-button>
      </div>
    </template>
  </a-tree-select>
</template>
<script>
  import { h, reactive, computed } from 'vue';
  import { IconCalendar } from '@arco-design/web-vue/es/icon';

  export default {
    setup() {
      const form = reactive({
        empty: false,
        showHeaderOnEmpty: false,
        showFooterOnEmpty: false,
      });

      const treeData = [
        {
          key: 'node1',
          icon: () => h(IconCalendar),
          title: 'Trunk',
          children: [
            {
              key: 'node2',
              title: 'Leaf',
            },
          ],
        },
        {
          key: 'node3',
          title: 'Trunk2',
          icon: () => h(IconCalendar),
          children: [
            {
              key: 'node4',
              title: 'Leaf',
            },
            {
              key: 'node5',
              title: 'Leaf',
            },
          ],
        },
        {
          key: 'node6',
          title: 'Trunk3',
          icon: () => h(IconCalendar),
          children: [
            {
              key: 'node7',
              title: 'Leaf',
            },
            {
              key: 'node8',
              title: 'Leaf',
            },
          ],
        },
      ];

      const computedTreeData = computed(() => {
        return form.empty ? [] : treeData;
      });

      return {
        form,
        computedTreeData,
      };
    },
  };
</script>
```

## Customize trigger element

Customize trigger element.

```vue
<template>
  <a-tree-select
    :data="treeData"
    default-value="node1"
    @change="onChange"
  >
    <template #trigger>
      <a-typography-paragraph style="width: 300px">
        You selected: <a href='javascript: void(0)'>{{ text }}</a>
      </a-typography-paragraph>
    </template>
  </a-tree-select>
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const text = ref('node1');

      function onChange(selected) {
        text.value = selected;
      }

      return {
        treeData,
        text,
        onChange,
      };
    },
  };

  const treeData = [
    {
      key: 'node1',
      title: 'node1',
      children: [
        {
          key: 'node2',
          title: 'node2',
        },
      ],
    },
    {
      key: 'node3',
      title: 'node3',
      children: [
        {
          key: 'node4',
          title: 'node4',
        },
        {
          key: 'node5',
          title: 'node5',
          children: [
            {
              key: 'node6',
              title: 'node6',
            },
            {
              key: 'node7',
              title: 'node7',
            },
          ]
        },
      ],
    },
  ];
</script>
```

## Multiple Selection

Multiple Selection

```vue
<template>
  <a-space>
    <a-tree-select
      v-model="selected"
      :multiple="true"
      :allow-clear="true"
      :allow-search="true"
      :data="treeData"
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
    <a-tree-select
      v-model="selected"
      :multiple="true"
      :max-tag-count="2"
      :allow-clear="true"
      :allow-search="true"
      :data="treeData"
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
  </a-space>
</template>
<script>
  import { h, ref } from 'vue';
  import { IconCalendar } from '@arco-design/web-vue/es/icon';

  export default {
    setup() {
      const selected = ref([]);

      return {
        selected,
        treeData,
      };
    },
  };

  const treeData = [
    {
      key: 'node1',
      icon: () => h(IconCalendar),
      title: 'node1',
      children: [
        {
          key: 'node2',
          title: 'node2',
        },
      ],
    },
    {
      key: 'node3',
      title: 'node3',
      icon: () => h(IconCalendar),
      children: [
        {
          key: 'node4',
          title: 'node4',
        },
        {
          key: 'node5',
          title: 'node5',
        },
      ],
    },
  ];
</script>
```

## Checkable

The `treeCheckable` property can display checkbox.

```vue
<template>
  <div style="marginBottom: 24px;">
    <a-checkbox
      v-model="treeCheckStrictly"
      @change="() => {
        selected = [];
      }"
    >
    treeCheckStrictly
    </a-checkbox>
  </div>
  <a-tree-select
    v-model="selected"
    :allow-search="true"
    :allow-clear="true"
    :tree-checkable="true"
    :tree-check-strictly="treeCheckStrictly"
    :data="treeData"
    placeholder="Please select ..."
    style="width: 300px;"
  ></a-tree-select>
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const selected = ref([]);
      const treeCheckStrictly = ref(false);

      return {
        selected,
        treeCheckStrictly,
        treeData,
      };
    },
  };

  const treeData = [
    {
      title: 'Trunk 0-0',
      value: 'Trunk 0-0',
      key: '0-0',
      children: [
        {
          title: 'Leaf 0-0-1',
          value: 'Leaf 0-0-1',
          key: '0-0-1',
        },
        {
          title: 'Branch 0-0-2',
          value: 'Branch 0-0-2',
          key: '0-0-2',
          children: [
            {
              title: 'Leaf 0-0-2-1',
              value: 'Leaf 0-0-2-1',
              key: '0-0-2-1'
            }
          ]
        },
      ],
    },
    {
      title: 'Trunk 0-1',
      value: 'Trunk 0-1',
      key: '0-1',
      children: [
        {
          title: 'Branch 0-1-1',
          value: 'Branch 0-1-1',
          key: '0-1-1',
          checkable: false,
          children: [
            {
              title: 'Leaf 0-1-1-1',
              value: 'Leaf 0-1-1-1',
              key: '0-1-1-1',
            },
            {
              title: 'Leaf 0-1-1-2',
              value: 'Leaf 0-1-1-2',
              key: '0-1-1-2',
              disabled: true
            },
          ]
        },
        {
          title: 'Leaf 0-1-2',
          value: 'Leaf 0-1-2',
          key: '0-1-2',
        },
      ],
    },
  ];
</script>
```

## Check Strategy

Customize the return value through the `treeCheckStrategy` property.

```vue
<template>
  <div style="margin-bottom: 24px;">
    <a-radio-group
      type='button'
      v-model="treeCheckedStrategy"
      @change="(value) => {
        selected = []
      }"
    >
      <a-radio
        v-for="item in strategyOptions"
        :key="item?.value"
        :value="item?.value"
      >
        {{ item?.label }}
      </a-radio>
    </a-radio-group>
  </div>
  <a-tree-select
    v-model="selected"
    :allow-search="true"
    :allow-clear="true"
    :tree-checkable="true"
    :tree-checked-strategy="treeCheckedStrategy"
    :data="treeData"
    placeholder="Please select ..."
    style="width: 300px;"
  ></a-tree-select>
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const selected = ref([]);
      const treeCheckedStrategy = ref('all');

      return {
        selected,
        treeCheckedStrategy,
        strategyOptions,
        treeData,
      };
    },
  };

  const strategyOptions = [
    {
      value: 'all',
      label: 'show all'
    },
    {
      value: 'parent',
      label: 'show parent'
    },
    {
      value: 'child',
      label: 'show child'
    }
  ];

  const treeData = [
    {
      title: 'Trunk 0-0',
      value: 'Trunk 0-0',
      key: '0-0',
      children: [
        {
          title: 'Leaf 0-0-1',
          value: 'Leaf 0-0-1',
          key: '0-0-1',
        },
        {
          title: 'Branch 0-0-2',
          value: 'Branch 0-0-2',
          key: '0-0-2',
          children: [
            {
              title: 'Leaf 0-0-2-1',
              value: 'Leaf 0-0-2-1',
              key: '0-0-2-1'
            }
          ]
        },
      ],
    },
    {
      title: 'Trunk 0-1',
      value: 'Trunk 0-1',
      key: '0-1',
      children: [
        {
          title: 'Branch 0-1-1',
          value: 'Branch 0-1-1',
          key: '0-1-1',
          checkable: false,
          children: [
            {
              title: 'Leaf 0-1-1-1',
              value: 'Leaf 0-1-1-1',
              key: '0-1-1-1',
            },
            {
              title: 'Leaf 0-1-1-2',
              value: 'Leaf 0-1-1-2',
              key: '0-1-1-2',
              disabled: true
            },
          ]
        },
        {
          title: 'Leaf 0-1-2',
          value: 'Leaf 0-1-2',
          key: '0-1-2',
        },
      ],
    },
  ];
</script>
```

## Control Collapse

The dropdown expanded by default. Use popupVisible and onVisibleChange to control the expansion and collapse of the dropdown.

For example, in this demo, onVisibleChange is triggered when the mouse moves out of the dropdown and the popup, the parameter is false, and the dropdown box is collapsed.

```vue
<template>
  <div style="margin-bottom: 24px;">
    <a-button type="primary" @click="onClick">toggle</a-button>
  </div>
  <a-tree-select
    :popupVisible="popupVisible"
    :allow-clear="true"
    :data="treeData"
    placeholder="Please select ..."
    style="width: 300px"
  ></a-tree-select>
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const popupVisible = ref(false);
      function onClick() {
        popupVisible.value = !popupVisible.value;
      }

      return {
        onClick,
        popupVisible,
        treeData,
      };
    },
  };

  const treeData = [
    {
      key: 'node1',
      title: 'Trunk',
      children: [
        {
          key: 'node2',
          title: 'Leaf',
        },
      ],
    },
    {
      key: 'node3',
      title: 'Trunk2',
      children: [
        {
          key: 'node4',
          title: 'Leaf',
        },
        {
          key: 'node5',
          title: 'Leaf',
        },
      ],
    },
  ];
</script>
```

## Customize treeData

You can customize `treeData` by `fieldNames`.

```vue
<template>
  <a-tree-select
    default-value="0-0-1"
    :fieldNames="{
      key: 'value',
      title: 'label',
      children: 'items'
    }"
    :data="treeData"
    placeholder="Please select ..."
    style="width: 300px;"
  ></a-tree-select>
</template>
<script>
  export default {
    setup() {
      return {
        treeData,
      };
    },
  };

  const treeData = [
    {
      label: 'Trunk 0-0',
      value: '0-0',
      items: [
        {
          label: 'Branch 0-0-2',
          value: '0-0-2',
          selectable: false,
          items: [
            {
              label: 'Leaf',
              value: '0-0-2-1',
              items: [
                {
                  label: 'Leaf 0-0-2',
                  value: '0-0-2-1-0',
                  items: [
                    {
                      label: 'Leaf',
                      value: '0-0-2-1-0-0'
                    }
                  ]
                },
              ],
            }
          ]
        },
      ],
    },
    {
      label: 'Trunk 0-1',
      value: '0-1',
      items: [
        {
          label: 'Branch 0-1-1',
          value: '0-1-1',
          items: [
            {
              label: 'Leaf',
              value: '0-1-1-0',
            }
          ]
        },
      ],
    },
  ];
</script>
```

## Virtual List

By specifying `treeProps.virtualListProps` to turn on the virtual list, high performance can be obtained when a large
amount of data is used.

```vue
<template>
  <a-tree-select
    :data="treeData"
    :allow-search="{
      retainInputValue: true
    }"
    multiple
    tree-checkable
    :scrollbar="false"
    tree-checked-strategy="parent"
    :treeProps="{
      virtualListProps: {
        height: 200,
      },
    }"
  />
</template>
<script>
export default {
  setup() {
    const treeData = loop();
    return {
      treeData
    }
  }
}

function loop(path = '0', level = 2) {
  const list = [];
  for (let i = 0; i < 10; i += 1) {
    const key = `${path}-${i}`;
    const treeNode = {
      title: key,
      key,
    };

    if (level > 0) {
      treeNode.children = loop(key, level - 1);
    }

    list.push(treeNode);
  }
  return list;
}
</script>
```

## Fallback Option

Use `fallback-option` to customize the display effect of the value of the option that is not found. By default, the value itself is displayed when the option is not found. Users can set this to `false` to hide values that do not match node data.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-tree-select
      defaultValue="node0"
      :data="treeData"
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
    <a-tree-select
      defaultValue="node0"
      :data="treeData"
      :fallback-option="false"
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
    <a-tree-select
      defaultValue="node0"
      :data="treeData"
      :fallback-option="fallback"
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
    <a-tree-select
      :defaultValue="['node0', 'node2']"
      :data="treeData"
      multiple
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
    <a-tree-select
      :defaultValue="['node0', 'node2']"
      :data="treeData"
      :fallback-option="false"
      multiple
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
    <a-tree-select
      :default-value="['node0', 'node2']"
      :data="treeData"
      :fallback-option="fallback"
      multiple
      placeholder="Please select ..."
      style="width: 300px"
    ></a-tree-select>
  </a-space>
</template>

<script>
export default {
  setup() {
    return {
      treeData,
      fallback(key) {
        return {
          key,
          title: `++${key}++`
        }
      }
    }
  }
}

const treeData = [
    {
      key: 'node1',
      title: 'Trunk1',
      children: [
        {
          key: 'node2',
          title: 'Leaf1',
        },
      ],
    },
    {
      key: 'node3',
      title: 'Trunk2',
      children: [
        {
          key: 'node4',
          title: 'Leaf2',
        },
        {
          key: 'node5',
          title: 'Leaf3',
        },
      ],
    },
  ];
</script>
```

## API

### `<tree-select>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|disabled|Whether to disable|`boolean`|`false`||
|loading|Whether it is loading state|`boolean`|`false`||
|error|Whether it is an error state|`boolean`|`false`||
|size|The size of the selection box.|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|border|Whether to show the border|`boolean`|`true`||
|allow-search|Whether to allow searching|`boolean \| { retainInputValue?: boolean }`|`false (single) \| true (multiple)`||
|allow-clear|Whether to allow clear|`boolean`|`false`||
|placeholder|Prompt copy|`string`|`-`||
|max-tag-count|The maximum number of labels displayed, only valid in multi-select mode|`number`|`-`||
|multiple|Whether to support multiple selection|`boolean`|`false`||
|default-value|Default value|`string \| number \| Array<string \| number> \| LabelValue \| LabelValue[]`|`-`||
|model-value **(v-model)**|Value|`string \| number \| Array<string \| number> \| LabelValue \| LabelValue[]`|`-`||
|field-names|Specify the field name in the node data|`TreeFieldNames`|`-`||
|data|Data|`TreeNodeData[]`|`[]`||
|label-in-value|Set the value format. The default is string, when set to true, the value format is: {label: string, value: string}|`boolean`|`false`||
|tree-checkable|Whether to show checkbox|`boolean`|`false`||
|tree-check-strictly|Whether the parent and child nodes are related|`boolean`|`false`||
|tree-checked-strategy|Customized echo method|`'all' \| 'parent' \| 'child'`|`'all'`||
|tree-props|Can accept Props of all [Tree](../data-display/tree.md) components|`Partial<TreeProps>`|`-`||
|trigger-props|Can accept Props of all [Trigger](../other/trigger.md) components|`Partial<TriggerProps>`|`-`||
|popup-visible **(v-model)**|Whether the pop-up box is visible|`boolean`|`-`||
|default-popup-visible|Whether the default pop-up box is visible|`boolean`|`false`||
|dropdown-style|Drop-down box style|`CSSProperties`|`-`||
|dropdown-class-name|Drop-down box style class|`string \| string[]`|`-`||
|filter-tree-node|Custom node filter function|`(searchKey: string, nodeData: TreeNodeData) => boolean`|`-`||
|load-more|Load data dynamically|`(nodeData: TreeNodeData) => Promise<void>`|`-`||
|disable-filter|Disable internal filtering logic|`boolean`|`false`||
|popup-container|Mount container for pop-up box|`string \| HTMLElement`|`-`||
|fallback-option|Customize node data for keys that do not match options|`boolean \| ((key: number \| string) => TreeNodeData \| boolean)`|`true`|2.22.0|
|selectable|Set the nodes that can be selected, all can be selected by default|`boolean\| 'leaf'\| ((    node: TreeNodeData,    info: { isLeaf: boolean; level: number }  ) => boolean)`|`true`|2.27.0|
|scrollbar|Whether to enable virtual scroll bar|`boolean \| ScrollbarProps`|`true`|2.39.0|
|show-header-on-empty|Whether to display the header in the empty state|`boolean`|`false`||
|show-footer-on-empty|Whether to display the footer in the empty state|`boolean`|`false`||
|input-value **(v-model)**|The value of the input|`string`|`-`|2.55.0|
|default-input-value|The default value of the input (uncontrolled mode)|`string`|`''`|2.55.0|
### `<tree-select>` Events

|Event Name|Description|Parameters|version|
|---|---|---|:---|
|change|Trigger when the value changes|value: `string \| number \| LabelValue \| Array<string \| number> \| LabelValue[] \| undefined`||
|popup-visible-change|Triggered when the status of the drop-down box changes|visible: `boolean`||
|search|Triggered when the search value changes|searchKey: `string`||
|clear|Triggered when clear is clicked|-||
|input-value-change|Triggered when the value of the input changes|inputValue: `string`|2.55.0|
### `<tree-select>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|trigger|Custom trigger element|-||
|prefix|Prefix|-||
|label|Custom Label|data: `mixed`||
|header|The header of the drop-down box|-||
|loader|Customizing the content displayed during loading|-||
|empty|Custom empty data display|-||
|footer|The footer of the drop-down box|-||
|tree-slot-extra|Render additional node content of the tree component|-||
|tree-slot-title|Custom the node title of the tree component|title: `string`||
|tree-slot-icon|Custom node icon for the tree component|node: `TreeNodeData`|2.18.0|
|tree-slot-switcher-icon|Custom switcher icon for the tree component|-||
