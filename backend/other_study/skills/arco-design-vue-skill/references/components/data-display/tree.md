---
name: arco-vue-tree
description: "For content with many levels, such as folders, catalogs, and organizational structures, the tree can clearly show their hierarchical relationship, and has interactive functions such as expanding, collapsing, and selecting. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Tree

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic

Give each node a globally unique `key` (required), and the `title` is the content to be displayed on the node.

```vue
<template>
  <a-tree
    :data="treeData"
    :default-expanded-keys="['0-0-0']"
    :default-selected-keys="['0-0-0', '0-0-1']"
  />
</template>
<script>
  export default {
    data() {
      return {
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
          title: 'Branch 0-0-0',
          key: '0-0-0',
          disabled: true,
          children: [
            {
              title: 'Leaf',
              key: '0-0-0-0',
            },
            {
              title: 'Leaf',
              key: '0-0-0-1',
            }
          ]
        },
        {
          title: 'Branch 0-0-1',
          key: '0-0-1',
          children: [
            {
              title: 'Leaf',
              key: '0-0-1-0',
            },
          ]
        },
      ],
    },
  ];
</script>
```

## BlockNode

The treeNode occupy the remaining horizontal space.

```vue
<template>
  <a-tree blockNode :data="treeData" />
</template>
<script>
  export default {
    data() {
      return {
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
          title: 'Branch 0-0-0',
          key: '0-0-0',
          children: [
            {
              title: 'Leaf',
              key: '0-0-0-0',
            },
            {
              title: 'Leaf',
              key: '0-0-0-1',
            }
          ]
        },
        {
          title: 'Branch 0-0-1',
          key: '0-0-1',
          children: [
            {
              title: 'Leaf',
              key: '0-0-1-0',
            },
          ]
        },
      ],
    },
  ];
</script>
```

## Multiple Selection

Add `:multiple="true"` to `Tree` to enable multiple selection.

```vue
<template>
  <a-checkbox
    style="marginBottom: 24px;"
    v-model="multiple"
    @change="() => {
      selectedKeys = [];
    }"
  >
    multiple
  </a-checkbox>
  <br/>
  <a-typography-text>
    Current: {{ selectedKeys?.join(' , ') }}
  </a-typography-text>
  <br/>
  <a-tree
    v-model:selected-keys="selectedKeys"
    :multiple="multiple"
    :data="treeData"
  />
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const selectedKeys = ref([]);
      const multiple = ref(true);
      const treeData = [
        {
          title: 'Trunk 0-0',
          key: '0-0',
          children: [
            {
              title: 'Leaf',
              key: '0-0-1',
            },
            {
              title: 'Branch 0-0-2',
              key: '0-0-2',
              children: [
                {
                  title: 'Leaf',
                  key: '0-0-2-1'
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
                  title: 'Leaf',
                  key: '0-1-1-1',
                },
                {
                  title: 'Leaf',
                  key: '0-1-1-2',
                },
              ]
            },
            {
              title: 'Leaf',
              key: '0-1-2',
            },
          ],
        },
      ];

      return {
        selectedKeys,
        multiple,
        treeData,
      };
    },
  }
</script>
```

## Checkable

Add the `checkable` attribute to display the checkbox, and you can use `defaultCheckedKeys` to specify which nodes are checked by default.

```vue
<template>
  <a-checkbox
    style="marginBottom: 24px;"
    v-model="checkStrictly"
    @change="() => {
      checkedKeys = [];
    }"
  >
    checkStrictly
  </a-checkbox>
  <a-tree
    :checkable="true"
    v-model:checked-keys="checkedKeys"
    :check-strictly="checkStrictly"
    :data="treeData"
  />
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
    const checkedKeys = ref([]);
    const checkStrictly = ref(false);

      return {
        checkedKeys,
        checkStrictly,
        treeData,
      }
    }
  }

  const treeData = [
    {
      title: 'Trunk 0-0',
      key: '0-0',
      children: [
        {
          title: 'Leaf',
          key: '0-0-1',
        },
        {
          title: 'Branch 0-0-2',
          key: '0-0-2',
          disabled: true,
          children: [
            {
              title: 'Leaf',
              key: '0-0-2-1'
            },
            {
              title: 'Leaf',
              key: '0-0-2-2',
              disableCheckbox: true
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
              title: 'Leaf ',
              key: '0-1-1-1',
            },
            {
              title: 'Leaf ',
              key: '0-1-1-2',
            },
          ]
        },
        {
          title: 'Leaf',
          key: '0-1-2',
        },
      ],
    },
  ];
</script>
```

## Two-way binding

The `selectedKeys`, `checkedKeys`, and `expandedKeys` attributes can all be controlled, not only supporting `v-model`, but also controlling how to update attribute values in the corresponding `select` / `check` / `expand` events.

```vue
<template>
  <a-button-group style="margin-bottom: 20px;">
    <a-button
      type="primary"
      @click="toggleChecked"
    >
      {{
        checkedKeys?.length ? 'deselect all' : 'select all'
      }}
    </a-button>
    <a-button
      type="primary"
      @click="toggleExpanded"
    >
      {{
        expandedKeys?.length ? 'fold' : 'unfold'
      }}
    </a-button>
  </a-button-group>
  <a-tree
    :checkable="true"
    v-model:selected-keys="selectedKeys"
    v-model:checked-keys="checkedKeys"
    v-model:expanded-keys="expandedKeys"
    @select="onSelect"
    @check="onCheck"
    @expand="onExpand"
    :data="treeData"
  />
</template>
<script>
  import { ref } from 'vue';

  const allCheckedKeys = ['0-0', '0-0-1', '0-0-2', '0-0-2-1', '0-1', '0-1-1', '0-1-2'];
  const allExpandedKeys = ['0-0', '0-1', '0-0-2'];

  export default {
    setup() {
      const selectedKeys = ref([]);
      const checkedKeys = ref([]);
      const expandedKeys = ref([]);

      return {
        selectedKeys,
        checkedKeys,
        expandedKeys,
        treeData,
        toggleChecked() {
          checkedKeys.value = checkedKeys?.value.length ? [] : allCheckedKeys;
        },
        toggleExpanded() {
          expandedKeys.value = expandedKeys?.value.length ? [] : allExpandedKeys;
        },
        onSelect(newSelectedKeys, event) {
          console.log('select: ', newSelectedKeys, event);
        },
        onCheck(newCheckedKeys, event) {
          console.log('check: ', newCheckedKeys, event);
        },
        onExpand(newExpandedKeys, event) {
          console.log('expand: ', newExpandedKeys, event);
        },
      };
    },
  };

  const treeData = [
    {
      title: 'Trunk 0-0',
      key: '0-0',
      children: [
        {
          title: 'Leaf 0-0-1',
          key: '0-0-1',
        },
        {
          title: 'Branch 0-0-2',
          key: '0-0-2',
          children: [
            {
              title: 'Leaf 0-0-2-1',
              key: '0-0-2-1'
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
          title: 'Leaf 0-1-1',
          key: '0-1-1',
        },
        {
          title: 'Leaf 0-1-2',
          key: '0-1-2',
        },
      ],
    },
  ];
</script>
```

## Dynamic Loading

Load nodes dynamically.

```vue
<template>
  <a-tree :data="treeData" :load-more="loadMore" />
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const treeData = ref([
        {
          title: 'Trunk 0-0',
          key: '0-0'
        },
        {
          title: 'Trunk 0-1',
          key: '0-1',
          children: [
            {
              title: 'Branch 0-1-1',
              key: '0-1-1'
            }
          ],
        },
      ]);

      const loadMore = (nodeData) => {
        return new Promise((resolve) => {
          setTimeout(() => {
            nodeData.children = [
              { title: `leaf`, key: `${nodeData.key}-1`, isLeaf: true },
            ];
            resolve();
          }, 1000);
        });
      };

      return {
        treeData,
        loadMore,
      };
    }
  }

</script>
```

## Draggable

Draggable nodes.

```vue
<template>
  <a-checkbox
    v-model="checked"
    style="margin-bottom: 20px;"
  >
    checkable
  </a-checkbox>
  <a-tree
    class="tree-demo"
    draggable
    blockNode
    :checkable="checked"
    :data="treeData"
    @drop="onDrop"
  />
</template>
<script>
  import { ref } from 'vue';
  export default {
    setup() {
      const treeData = ref(defaultTreeData);
      const checkedKeys = ref([]);
      const checked = ref(false);

      return {
        treeData,
        checkedKeys,
        checked,
        onDrop({ dragNode, dropNode, dropPosition }) {
          const data = treeData.value;
          const loop = (data, key, callback) => {
            data.some((item, index, arr) => {
              if (item.key === key) {
                callback(item, index, arr);
                return true;
              }
              if (item.children) {
                return loop(item.children, key, callback);
              }
              return false;
            });
          };

          loop(data, dragNode.key, (_, index, arr) => {
            arr.splice(index, 1);
          });

          if (dropPosition === 0) {
            loop(data, dropNode.key, (item) => {
              item.children = item.children || [];
              item.children.push(dragNode);
            });
          } else {
            loop(data, dropNode.key, (_, index, arr) => {
              arr.splice(dropPosition < 0 ? index : index + 1, 0, dragNode);
            });
          }
        }
      };
    }
  };

  const defaultTreeData = [
    {
      title: 'Trunk 0-0',
      key: '0-0',
      children: [
        {
          title: 'Leaf 0-0-1',
          key: '0-0-1',
        },
        {
          title: 'Branch 0-0-2',
          key: '0-0-2',
          disableCheckbox: true,
          children: [
            {
              draggable: false,
              title: 'Leaf 0-0-2-1 (Drag disabled)',
              key: '0-0-2-1'
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
          checkable: false,
          children: [
            {
              title: 'Leaf 0-1-1-1',
              key: '0-1-1-1',
            },
            {
              title: 'Leaf 0-1-1-2',
              key: '0-1-1-2',
            },
          ]
        },
        {
          title: 'Leaf 0-1-2',
          key: '0-1-2',
        },
      ],
    },
  ]
</script>
<style scoped>
.tree-demo :deep(.tree-node-dropover) > :deep(.arco-tree-node-title),
.tree-demo :deep(.tree-node-dropover) > :deep(.arco-tree-node-title):hover, {
  animation: blinkBg 0.4s 2;
}

@keyframes blinkBg {
  0% {
    background-color: transparent;
  }

  100% {
    background-color: var(--color-primary-light-1);
  }
}
</style>
```

## Checked Strategy

Add `checkedStrategy` to set the return value when selected.

```vue
<template>
  <a-radio-group
    type='button'
    v-model="checkedStrategy"
    @change="(value) => {
      checkedKeys = []
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
  <br/>
  <a-typography-text style="margin: 24px 0; display: inline-block;">
    Current: {{ checkedKeys?.join(' , ') }}
  </a-typography-text>
  <br/>
  <a-tree
    :checkable="true"
    v-model:checked-keys="checkedKeys"
    :checked-strategy="checkedStrategy"
    :data="treeData"
  />
</template>
<script>
  import { ref } from 'vue';

  const treeData = [
    {
      title: 'Trunk 0-0',
      key: '0-0',
      children: [
        {
          title: 'Leaf',
          key: '0-0-1',
        },
        {
          title: 'Branch 0-0-2',
          key: '0-0-2',
          children: [
            {
              title: 'Leaf',
              key: '0-0-2-1'
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
              title: 'Leaf',
              key: '0-1-1-1',
            },
            {
              title: 'Leaf',
              key: '0-1-1-2',
            },
          ]
        },
        {
          title: 'Leaf',
          key: '0-1-2',
        },
      ],
    },
  ];

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

  export default {
    setup() {
      const checkedKeys = ref([]);
      const checkedStrategy = ref('all');

      return {
        treeData,
        strategyOptions,
        checkedStrategy,
        checkedKeys,
      }
    }
  }
</script>
```

## Show Line

Add the `showLine` property to `Tree` to display the connecting line.

```vue
<template>
  <div>
    <a-typography-text>showLine</a-typography-text>
    <a-switch v-model="showLine" style="margin-left: 12px" />
  </div>
  <a-tree
    :default-selected-keys="['0-0-1']"
    :data="treeData"
    :show-line="showLine"
  />
</template>
<script>
  import { ref } from 'vue';

  export default {
    setup() {
      const showLine = ref(true);

      return {
        showLine,
        treeData,
      };
    },
  };

  const treeData = [
    {
      title: 'Trunk 1',
      key: '0-0',
      children: [
        {
          title: 'Trunk 1-0',
          key: '0-0-0',
          children: [
            { title: 'leaf', key: '0-0-0-0' },
            {
              title: 'leaf',
              key: '0-0-0-1',
              children: [{ title: 'leaf', key: '0-0-0-1-0' }],
            },
            { title: 'leaf', key: '0-0-0-2' },
          ],
        },
        {
          title: 'Trunk 1-1',
          key: '0-0-1',
        },
        {
          title: 'Trunk 1-2',
          key: '0-0-2',
          children: [
            { title: 'leaf', key: '0-0-2-0' },
            {
              title: 'leaf',
              key: '0-0-2-1',
            },
          ],
        },
      ],
    },
    {
      title: 'Trunk 2',
      key: '0-1',
    },
    {
      title: 'Trunk 3',
      key: '0-2',
      children: [
        {
          title: 'Trunk 3-0',
          key: '0-2-0',
          children: [
            { title: 'leaf', key: '0-2-0-0' },
            { title: 'leaf', key: '0-2-0-1' },
          ],
        },
      ],
    },
  ];
</script>
```

## Size

Trees of different sizes.

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
  <a-tree
    style="margin-right: 20px;"
    :blockNode="true"
    :checkable="true"
    :size="size"
    :data="treeData" />
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
      title: 'Trunk 0-0',
      key: '0-0',
      children: [
        {
          title: 'Branch 0-0-0',
          key: '0-0-0',
          children: [
            {
              title: 'Leaf',
              key: '0-0-0-0',
            },
            {
              title: 'Leaf',
              key: '0-0-0-1',
            }
          ]
        },
        {
          title: 'Branch 0-0-1',
          key: '0-0-1',
          children: [
            {
              title: 'Leaf',
              key: '0-0-1-0',
            },
          ]
        },
      ],
    },
  ];
</script>
```

## Node Icon

The icon of a node can be specified globally via the `icon` slot of the `tree`, or individually via the `icon` property of the node.

```vue
<template>
  <a-tree :data="treeData">
    <template #icon>
      <IconStar />
    </template>
  </a-tree>
</template>
<script>
  import { h } from 'vue';
  import { IconStar, IconDriveFile } from '@arco-design/web-vue/es/icon';

  export default {
    components: {
      IconStar
    },
    setup() {
      return {
        treeData,
      };
    },
  };

  const treeData = [
    {
      title: 'Trunk',
      key: 'node1',
      children: [
        {
          title: 'Leaf',
          key: 'node2',
        },
      ],
    },
    {
      title: 'Trunk',
      key: 'node3',
      children: [
        {
          title: 'Leaf',
          key: 'node4',
          icon: () => h(IconDriveFile),
        },
        {
          title: 'Leaf',
          key: 'node5',
          icon: () => h(IconDriveFile),
        },
      ],
    },
  ];
</script>
```

## Extra Node

`Tree` provides `Slot` named `extra`, which can customize extra content on the node.

```vue
<template>
  <div style="width: 500px; padding: 2px; overflow: auto">
    <a-tree
      :blockNode="true"
      :checkable="true"
      :data="treeData"
    >
      <template #extra="nodeData">
        <IconPlus
          style="position: absolute; right: 8px; font-size: 12px; top: 10px; color: #3370ff;"
          @click="() => onIconClick(nodeData)"
        />
      </template>
    </a-tree>
  </div>
</template>
<script>
 import {ref} from 'vue';
 import { IconPlus } from '@arco-design/web-vue/es/icon';

 export default {
   components: {
     IconPlus,
   },
   setup() {
     function onIconClick(nodeData) {
      const children = nodeData.children || []
      children.push({
        title: 'new tree node',
        key: nodeData.key + '-' + (children.length + 1)
      })
      nodeData.children = children

      treeData.value = [...treeData.value];
    }

    const treeData = ref(
      [
        {
          title: 'Trunk',
          key: '0-0',
          children: [
            {
              title: 'Leaf',
              key: '0-0-1',
            },
            {
              title: 'Branch',
              key: '0-0-2',
              children: [
                {
                  title: 'Leaf',
                  key: '0-0-2-1'
                }
              ]
            },
          ],
        },
        {
          title: 'Trunk',
          key: '0-1',
          children: [
            {
              title: 'Branch',
              key: '0-1-1',
              children: [
                {
                  title: 'Leaf',
                  key: '0-1-1-1',
                },
                {
                  title: 'Leaf',
                  key: '0-1-1-2',
                },
              ]
            },
            {
              title: 'Leaf',
              key: '0-1-2',
            },
          ],
        },
      ]
    );

    return {
      onIconClick,
      treeData,
    };
   }
 };
</script>
```

## Component Icons

The node icons `loadingIcon`, `switcherIcon`, support customization at the two latitudes of `tree` and `node` at the same time, and `node` has a higher priority.

```vue
<template>
  <a-tree :data="treeData" show-line>
     <template #switcher-icon="node, { isLeaf }">
      <IconDown v-if="!isLeaf" />
      <IconStar v-if="isLeaf" />
    </template>
  </a-tree>
</template>

<script>
  import { h } from 'vue';
  import { IconDriveFile, IconDown, IconStar } from '@arco-design/web-vue/es/icon';

  export default {
    components: {
      IconDown,
      IconStar
    },
    setup() {
      return {
        treeData,
      };
    },
  };

  const treeData = [
    {
      title: 'Trunk',
      key: 'node1',
      children: [
        {
          title: 'Leaf',
          key: 'node2',
        },
      ],
    },
    {
      title: 'Trunk',
      key: 'node3',
      children: [
        {
          title: 'Leaf',
          key: 'node4',
          switcherIcon: () => h(IconDriveFile),
        },
        {
          title: 'Leaf',
          key: 'node5',
          switcherIcon: () => h(IconDriveFile),
        },
      ],
    },
  ];
</script>
```

## Virtual List

By specifying `virtualListProps` to turn on the virtual list, high performance can be obtained when a large amount of data is used.

```vue
<template>
  <a-button
    type="primary"
    :style="{ marginBottom: '20px' }"
    @click="scrollIntoView"
  >
    Scroll to 0-0-2-2, i.e. the 26th.
  </a-button>
  <a-tree
    ref="treeRef"
    blockNode
    checkable
    :data="treeData"
    :virtualListProps="{
      height: 200,
    }"
  />
</template>
<script>
  import { ref } from 'vue';
  export default {
    setup() {
      const treeRef = ref();
      const treeData = loop();
      return {
        treeRef,
        treeData,
        scrollIntoView() {
          treeRef.value && treeRef.value.scrollIntoView({ key: '0-0-2-2' });
        }
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

## Searchable

Show how to achieve the search tree effect.

```vue
<template>
  <div>
    <a-input-search
      style="margin-bottom: 8px; max-width: 240px"
      v-model="searchKey"
    />
    <a-tree :data="treeData">
      <template #title="nodeData">
        <template v-if="index = getMatchIndex(nodeData?.title), index < 0">{{ nodeData?.title }}</template>
        <span v-else>
          {{ nodeData?.title?.substr(0, index) }}
          <span style="color: var(--color-primary-light-4);">
            {{ nodeData?.title?.substr(index, searchKey.length) }}
          </span>{{ nodeData?.title?.substr(index + searchKey.length) }}
        </span>
      </template>
    </a-tree>
  </div>
</template>
<script>
  import { ref, computed } from 'vue';

  const originTreeData = [
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

  export default {
    setup() {
      const searchKey = ref('');
      const treeData = computed(() => {
        if (!searchKey.value) return originTreeData;
        return searchData(searchKey.value);
      })

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

        return loop(originTreeData);
      }

      function getMatchIndex(title) {
        if (!searchKey.value) return -1;
        return title.toLowerCase().indexOf(searchKey.value.toLowerCase());
      }

      return {
        searchKey,
        treeData,
        getMatchIndex,
      }
    }
  }
</script>
```

## Customize data

You can customize `data` by `fieldNames`.

```vue
<template>
  <a-tree
    :default-selected-keys="['0-0-1']"
    :fieldNames="{
      key: 'value',
      title: 'label',
      children: 'items',
      icon: 'customIcon'
    }"
    :data="treeData"
  />
</template>
<script>
  import { h } from 'vue';
  import { IconStar, IconDriveFile } from '@arco-design/web-vue/es/icon';
  export default {
    data() {
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
          customIcon: () => h(IconDriveFile),
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
                      customIcon: () => h(IconStar),
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

## API

### `<tree>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|size|Size|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|block-node|Whether the node occupies a row|`boolean`|`false`||
|default-expand-all|Whether to expand the parent node by default|`boolean`|`true`||
|multiple|Whether to support multiple selection|`boolean`|`false`||
|checkable|Whether to add a checkbox before the node, function format is supported since `2.27.0`|`boolean\| ((    node: TreeNodeData,    info: {      level: number;      isLeaf: boolean;    }  ) => boolean)`|`false`||
|selectable|Whether to support selection, function format is supported since `2.27.0`|`boolean\| ((    node: TreeNodeData,    info: {      level: number;      isLeaf: boolean;    }  ) => boolean)`|`true`||
|check-strictly|Whether to cancel the parent-child node association|`boolean`|`false`||
|checked-strategy|Customized backfill method <br/> all: return all selected nodes <br/> parent: return only parent node when both parent and child nodes are selected <br/> child: return only child nodes|`'all' \| 'parent' \| 'child'`|`'all'`||
|default-selected-keys|Tree node selected by default|`Array<string \| number>`|`-`||
|selected-keys **(v-model)**|Selected tree node|`Array<string \| number>`|`-`||
|default-checked-keys|Tree node with checkbox selected by default|`Array<string \| number>`|`-`||
|checked-keys **(v-model)**|Tree node with check box selected|`Array<string \| number>`|`-`||
|default-expanded-keys|Nodes expanded by default|`Array<string \| number>`|`-`||
|expanded-keys **(v-model)**|Expanded node|`Array<string \| number>`|`-`||
|data|Pass in `data` to generate the corresponding tree structure|`TreeNodeData[]`|`[]`||
|field-names|Specify the field name in the node data|`TreeFieldNames`|`-`||
|show-line|Whether to display the connection line|`boolean`|`false`||
|load-more|A callback for loading data asynchronously, returning a `Promise`|`(node: TreeNodeData) => Promise<void>`|`-`||
|draggable|Whether it can be dragged|`boolean`|`false`||
|allow-drop|Whether to allow release on a node when dragging|`(options: {  dropNode: TreeNodeData;  dropPosition: -1 \| 0 \| 1;}) => boolean`|`-`||
|virtual-list-props|Pass virtual list properties, pass in this parameter to turn on virtual scrolling, [VirtualListProps](#VirtualListProps)|`VirtualListProps`|`-`||
|default-expand-selected|Whether to expand the parent node of the selected node by default|`boolean`|`false`|2.9.0|
|default-expand-checked|Whether to expand the parent node of the checked node by default|`boolean`|`false`|2.9.0|
|auto-expand-parent|Whether to automatically expand the parent node of the expanded node|`boolean`|`true`|2.9.0|
|half-checked-keys **(v-model)**|The keys of half checked. Only valid when checkable and checkStrictly|`Array<string \| number>`|`-`|2.19.0|
|only-check-leaf|When enabled, checkedKeys is only for checked leaf nodes, and the status of the parent node is determined by the child node.(Only valid when checkable and checkStrictly is false)|`boolean`|`false`|2.21.0|
|animation|Whether to enable expand transition animation|`boolean`|`true`|2.21.0|
|action-on-node-click|The action triggered when the node is clicked|`'expand'`|`-`|2.27.0|
### `<tree>` Events

|Event Name|Description|Parameters|
|---|---|---|
|select|Triggered when the tree node is clicked|selectedKeys: `Array<string \| number>`<br>data: `{ selected?: boolean; selectedNodes: TreeNodeData[]; node?: TreeNodeData; e?: Event; }`|
|check|Triggered when the tree node checkbox is clicked. `halfCheckedKeys` and `halfCheckedNodes` support from `2.19.0`.|checkedKeys: `Array<string \| number>`<br>data: `{ checked?: boolean; checkedNodes: TreeNodeData[]; node?: TreeNodeData; e?: Event; halfCheckedKeys: (string \| number)[]; halfCheckedNodes: TreeNodeData[]; }`|
|expand|Expand/close|expandKeys: `Array<string \| number>`<br>data: `{ expanded?: boolean; expandNodes: TreeNodeData[]; node?: TreeNodeData; e?: Event; }`|
|drag-start|Node starts dragging|ev: `DragEvent`<br>node: `TreeNodeData`|
|drag-end|Node end drag|ev: `DragEvent`<br>node: `TreeNodeData`|
|drag-over|The node is dragged to the releasable target|ev: `DragEvent`<br>node: `TreeNodeData`|
|drag-leave|Node leaves to release the target|ev: `DragEvent`<br>node: `TreeNodeData`|
|drop|The node is released on a releasable target|data: `{ e: DragEvent; dragNode: TreeNodeData; dropNode: TreeNodeData; dropPosition: number; }`|
### `<tree>` Methods

|Method|Description|Parameters|Return|version|
|---|---|---|:---:|:---|
|scrollIntoView|Virtual list scroll to an element|options: `{ index?: number; key?: number \| string; align: 'auto' \| 'top' \| 'bottom'}`|-||
|getSelectedNodes|Get selected nodes|-|TreeNodeData[]|2.19.0|
|getCheckedNodes|Get checked nodes. Supports passing in `checkedStrategy`, if not passed, the configuration of the component is taken.|options: ` checkedStrategy?: 'all' \| 'parent' \| 'child'; includeHalfChecked?: boolean; `|TreeNodeData[]|2.19.0|
|getHalfCheckedNodes|Get half checked nodes|-|TreeNodeData[]|2.19.0|
|getExpandedNodes|Get expanded nodes|-|TreeNodeData[]|2.19.0|
|checkAll|Set the checkbox state of all nodes|checked: ` boolean `|-|2.20.0|
|checkNode|Sets the checkbox state of the specified node|key: ` TreeNodeKey \| TreeNodeKey[] `<br>checked: ` boolean `<br>onlyCheckLeaf: ` boolean `|-|2.20.0, onlyCheckLeaf from 2.21.0|
|selectAll|Set the selected state of all nodes|selected: ` boolean `|-|2.20.0|
|selectNode|Sets the selected state of the specified node|key: ` TreeNodeKey \| TreeNodeKey[] `<br>selected: ` boolean `|-|2.20.0|
|expandAll|Set the expanded state of all nodes|expanded: ` boolean `|-|2.20.0|
|expandNode|Sets the expanded state of the specified node|key: ` TreeNodeKey \| TreeNodeKey[] `<br>expanded: ` boolean `|-|2.20.0|
### `<tree>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|title|Title|title: `string`||
|extra|Render additional node content|-||
|drag-icon|Custom drag icon|node: `TreeNodeData`||
|loading-icon|Custom loading icon|-||
|switcher-icon|Custom switcher icon|-||
|icon|Custom node icon|node: `TreeNodeData`|2.18.0|

### TreeNodeData

|Name|Description|Type|Default|
|---|---|---|:---:|
|key|Unique key|`string \| number`|`-`|
|title|The title of the node|`string`|`-`|
|selectable|Whether to allow selection|`boolean`|`false`|
|disabled|Whether to disable the node|`boolean`|`false`|
|disableCheckbox|Whether to disable the checkbox|`boolean`|`false`|
|checkable|Whether to show checkbox|`boolean`|`false`|
|draggable|Whether it can be dragged|`boolean`|`false`|
|isLeaf|Whether it is a leaf node. Effective when loading dynamically|`boolean`|`false`|
|icon|Node icon|`() => VNode`|`-`|
|switcherIcon|Custom switcher icon, priority is greater than tree|`() => VNode`|`-`|
|loadingIcon|Customize loading icon, priority is greater than tree|`() => VNode`|`-`|
|dragIcon|Custom drag icon, priority is greater than tree|`() => VNode`|`-`|
|children|Child node|`TreeNodeData[]`|`-`|

### TreeFieldNames

|Name|Description|Type|Default|
|---|---|---|:---:|
|key|Specify the field name of key in TreeNodeData|`string`|`key`|
|title|Specify the field name of title in TreeNodeData|`string`|`title`|
|disabled|Specify the field name of disabled in TreeNodeData|`string`|`disabled`|
|children|Specify the field name of children in TreeNodeData|`string`|`children`|
|isLeaf|Specify the field name of isLeaf in TreeNodeData|`string`|`isLeaf`|
|disableCheckbox|Specify the field name of disableCheckbox in TreeNodeData|`string`|`disableCheckbox`|
|checkable|Specify the field name of checkable in TreeNodeData|`string`|`checkable`|
|icon|Specify the field name of icon in TreeNodeData|`string`|`checkable`|

### VirtualListProps

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|height|Viewable area height|`number \| string`|`-`||
|threshold|The threshold of the number of elements to enable virtual scrolling. When the number of data is less than the threshold, virtual scrolling will not be enabled.|`number`|`-`||
|isStaticItemHeight|(Repealed) Is the element height fixed. Version 2.18.0 deprecated, please use `fixedSize`|`boolean`|`false`||
|fixedSize|Is the element height fixed.|`boolean`|`false`|2.34.1|
|estimatedSize|Is the element height fixed.|`number`|`-`|2.34.1|
|buffer|The number of elements mounted in advance outside the boundary of the viewport.|`number`|`10`|2.34.1|
