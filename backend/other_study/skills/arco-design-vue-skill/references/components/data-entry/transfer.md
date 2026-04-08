---
name: arco-vue-transfer
description: "A two-column multi-select component that moves elements from one column to another in real time. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Transfer

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of the transfer.

```vue
<template>
  <a-transfer :data="data" :default-value="value" />
</template>

<script>
export default {
  setup() {
    const data = Array(8).fill(undefined).map((_, index) => ({
      value: `option${index + 1}`,
      label: `Option ${index + 1}`
    }));
    const value = ['option1', 'option3', 'option5'];

    return {
      data,
      value
    }
  },
}
</script>
```

## Search

You can customize the search function by setting `show-search` to use the shuttle box with search box.

```vue
<template>
  <a-transfer
    show-search
    :data="data"
    :default-value="value"
    :source-input-search-props="{
      placeholder:'source item search'
    }"
    :target-input-search-props="{
      placeholder:'target item search'
    }"
  />
</template>

<script>
export default {
  setup() {
    const data = Array(8).fill(undefined).map((_, index) => ({
      value: `option${index + 1}`,
      label: `Option ${index + 1}`
    }));
    const value = ['option1', 'option3', 'option5'];

    return {
      data,
      value
    }
  },
}
</script>
```

## One Way

By setting `one-way`, the shuttle frame in one-way mode is used.

```vue
<template>
  <a-transfer :data="data" :default-value="value" one-way/>
</template>

<script>
export default {
  setup() {
    const data = Array(8).fill(undefined).map((_, index) => ({
      value: `option${index + 1}`,
      label: `Option ${index + 1}`
    }));
    const value = ['option1', 'option3', 'option5'];

    return {
      data,
      value
    }
  },
}
</script>
```

## Custom Item

Customize the rendering content of the options through the `item` slot.

```vue

<template>
  <a-transfer :data="data" :default-value="value">
    <template #item="{ label }">
      <icon-up />
      {{ label }}
    </template>
  </a-transfer>
</template>

<script>
export default {
  setup() {
    const data = Array(8).fill(undefined).map((_, index) => {
      return {
        value: `option${index + 1}`,
        label: `Option ${index + 1}`,
        disabled: index === 1
      }
    });
    const value = ['option1', 'option3', 'option5'];

    return {
      data,
      value
    }
  },
}
</script>
```

## Simple

Turn on the simple mode by setting `simple`, and click the option to move.

```vue
<template>
  <a-transfer :data="data" :default-value="value" simple />
</template>

<script>
export default {
  setup() {
    const data = Array(8).fill(undefined).map((_, index) => ({
      value: `option${index + 1}`,
      label: `Option ${index + 1}`
    }));
    const value = ['option1', 'option3', 'option5'];

    return {
      data,
      value
    }
  },
}
</script>
```

## Tree Transfer

The tree-type shuttle box can be realized by customizing the interface of the shuttle box.

```vue

<template>
  <a-transfer :data="transferData" :default-value="value">
    <template #source="{data,selectedKeys,onSelect}">
      <a-tree
        :checkable="true"
        checked-strategy="child"
        :checked-keys="selectedKeys"
        :data="getTreeData(data)"
        @check="onSelect"
      />
    </template>
  </a-transfer>
</template>

<script>
export default {
  setup() {
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
              },
              {
                title: 'Leaf 0-0-2-2',
                key: '0-0-2-2',
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
    ];

    const getTransferData = (treeData = [], transferDataSource = []) => {
      treeData.forEach((item) => {
        if (item.children) getTransferData(item.children, transferDataSource);
        else transferDataSource.push({label: item.title, value: item.key});
      });
      return transferDataSource;
    };

    const getTreeData = (data = []) => {
      const values = data.map(item => item.value)

      const travel = (_treeData = []) => {
        const treeDataSource = []
        _treeData.forEach((item) => {
          if (item.children || values.includes(item.key)) {
            treeDataSource.push({title: item.title, key: item.key, children: travel(item.children)})
          }
        });
        return treeDataSource
      }

      return travel(treeData)
    }

    const transferData = getTransferData(treeData);

    const value = ['0-0-2-1'];

    return {
      transferData,
      value,
      getTreeData
    }
  },
}
</script>
```

## Custom Header

Customize the rendering content of the title bar through the `source-title` and `target-title` slots

```vue
<template>
  <a-transfer :data="data" :default-value="value">
    <template
      #source-title="{
        countTotal,
        countSelected,
        checked,
        indeterminate,
        onSelectAllChange,
      }"
    >
      <div :style="styleHeader">
        Source Title {{ countSelected }}-{{ countTotal }}
        <a-checkbox
          :model-value="checked"
          :indeterminate="indeterminate"
          @change="onSelectAllChange"
        />
      </div>
    </template>

    <template #target-title="{ countTotal, countSelected, onClear }">
      <div :style="styleHeader">
        Target Title {{ countSelected }}-{{ countTotal }}
        <IconDelete @click="onClear" />
      </div>
    </template>
  </a-transfer>
</template>

<script>
import { IconDelete } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconDelete },
  setup() {
    const data = Array(8)
      .fill(undefined)
      .map((_, index) => ({
        value: `option${index + 1}`,
        label: `Option ${index + 1}`,
      }));
    const value = ['option1', 'option3', 'option5'];

    const styleHeader = {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      paddingRight: '8px'
    };

    return {
      styleHeader,
      data,
      value,
    };
  },
};
</script>
```

## API

### `<transfer>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|data|Data of the transfer|`TransferItem[]`|`[]`||
|model-value **(v-model)**|Value in the target selection box|`string[]`|`-`||
|default-value|The default value in the target selection box (uncontrolled state)|`string[]`|`[]`||
|selected **(v-model)**|Selected option value|`string[]`|`-`||
|default-selected|The option value selected by default (uncontrolled state)|`string[]`|`[]`||
|disabled|Whether to disable|`boolean`|`false`||
|simple|Whether to open the simple mode (click the option to move)|`boolean`|`false`||
|one-way|Whether to open the one-way mode (only move to the target selection box)|`boolean`|`false`||
|show-search|Whether to show the search input|`boolean`|`false`||
|show-select-all|Whether show select all checkbox on the header|`boolean`|`true`|2.39.0|
|title|The title of the source and target selection boxes|`string[]`|`['Source', 'Target']`||
|source-input-search-props|Search box configuration for source selection box|`object`|`-`|2.51.1|
|target-input-search-props|Search box configuration for target selection box|`object`|`-`|2.51.1|
### `<transfer>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when the value of the target selection box changes|value: `string[]`|
|select|Triggered when the selected value changes|selected: `string[]`|
|search|Triggered when the user searches|value: `string`<br>type: `'target'\|'source'`|
### `<transfer>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|source|Source content|data: `TransferItem[]`<br>selectedKeys: `string[]`<br>onSelect: `(value: string[]) => void`|2.39.0|
|source-title|Source Header|countTotal: `number`<br>countSelected: `number`<br>searchValue: `string`<br>checked: `boolean`<br>indeterminate: `boolean`<br>onSelectAllChange: `(checked:boolean) => void`<br>onClear: `() => void`|2.45.0|
|to-target-icon|To target icon slot|-|2.52.0|
|to-source-icon|To source icon slot|-|2.52.0|
|target|Target content|data: `TransferItem[]`<br>selectedKeys: `string[]`<br>onSelect: `(value: string[]) => void`|2.39.0|
|target-title|Target Header|countTotal: `number`<br>countSelected: `number`<br>searchValue: `string`<br>checked: `boolean`<br>indeterminate: `boolean`<br>onSelectAllChange: `(checked:boolean) => void`<br>onClear: `() => void`|2.45.0|
|item|Option|value: `string`<br>label: `string`||

### TransferItem

|Name|Description|Type|Default|
|---|---|---|:---:|
|value|Option value|`string`|`-`|
|label|Option label|`string`|`-`|
|disabled|Whether to disable|`boolean`|`false`|
