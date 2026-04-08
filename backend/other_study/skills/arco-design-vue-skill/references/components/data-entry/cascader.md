---
name: arco-vue-cascader
description: "Refers to the use of multi-level classification to separate the options when the number of selector options is large. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Cascader

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

The basic usage of cascader.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-cascader :options="options" :style="{width:'320px'}" placeholder="Please select ..." />
    <a-cascader :options="options" default-value="datunli" expand-trigger="hover" :style="{width:'320px'}" placeholder="Please select ..." />
  </a-space>
</template>

<script>
export default {
  setup() {
    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      options
    }
  },
}
</script>
```

## Allow Clear

Allow clear.

```vue
<template>
  <a-cascader :options="options" v-model="value" :style="{width:'320px'}" placeholder="Please select ..."
              allow-clear />
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref('datunli');

    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      value,
      options
    }
  },
}
</script>
```

## Disabled Option

Specify the `disabled` of the `option` as `true` to disable the option.

```vue
<template>
  <a-cascader :options="options" :style="{width:'320px'}" placeholder="Please select ..." />
</template>

<script>
export default {
  setup() {
    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
            disabled: true
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
                disabled: true
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      options
    }
  },
}
</script>
```

## asdf

Use `formatLabel` to customize the displayed content.

```vue

<template>
  <a-cascader :options="options" default-value="datunli" :style="{width:'320px'}" placeholder="Please select ..." :format-label="format" />
</template>

<script>
export default {
  setup() {
    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];

    const format = (options) => {
      const labels = options.map(option => option.label)
      return labels.join('-')
    }

    return {
      options,
      format
    }
  },
}
</script>
```

## Multiple

Enable multiple selection mode by setting `multiple`.

```vue
<template>
  <a-cascader :options="options" :default-value="['datunli']" :style="{width:'320px'}" placeholder="Please select ..." multiple/>
</template>

<script>
export default {
  setup() {
    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      options
    }
  },
}
</script>
```

## Check strictly

Set the attribute `check-strictly`, turn on any selectable mode, and click any node to select. Multiple selections will disassociate the parent and child nodes.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-cascader :options="options" default-value="beijing" :style="{width:'320px'}" placeholder="Please select ..." check-strictly />
    <a-cascader :options="options" :default-value="['beijing']" :style="{width:'320px'}" placeholder="Please select ..." multiple check-strictly />
  </a-space>
</template>

<script>
export default {
  setup() {
    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
            disabled: true
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      options
    }
  },
}
</script>
```

## Loading

Select boxes and drop-down menus show loading status.

```vue
<template>
  <a-cascader :options="[]" :style="{width:'320px'}" placeholder="Please select ..." loading />
</template>
```

## Lazy load

The lazy data loading function can be turned on through the `load-more` attribute.
After the data lazy loading function is enabled, the leaf nodes need to be marked with `isLeaf: true`. Nodes that are not marked and have no `children` attribute will be considered as requiring lazy loading.
The `load-more` attribute provides a `done` function for callback, and lazy loaded sub-data can be passed in the callback. If the `done` function does not pass in data, it will be considered as a lazy loading failure, and this node can trigger lazy loading again.

```vue
<template>
  <a-space>
    <a-cascader :options="options" :style="{width:'320px'}" placeholder="Please select ..." :load-more="loadMore"/>
  </a-space>
</template>

<script>
export default {
  setup() {
    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
          },
          {
            value: 'haidian',
            label: 'Haidian',
            isLeaf: true
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
            isLeaf: true
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
            isLeaf: true
          },
        ],
      },
    ];
    const loadMore = (option, done) => {
      window.setTimeout(() => {
        const nodes = [{
          value: `${option.value}-option1`,
          label: `${option.label}-Option1`,
          isLeaf: true
        }, {
          value: `${option.value}-option2`,
          label: `${option.label}-Option2`,
          isLeaf: true
        }]
        done(nodes)
      }, 2000)
    };

    return {
      options,
      loadMore
    }
  },
}
</script>
```

## Allow Search

Make the input box support search function by setting `allow-search`.

```vue
<template>
  <a-cascader :options="options" :style="{width:'320px'}" placeholder="Please select ..." allow-search/>
</template>

<script>
export default {
  setup() {
    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      options
    }
  },
}
</script>
```

## path mode

`modelValue` uses the path as the value.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-cascader :options="options" :style="{width:'320px'}" placeholder="Please select ..." path-mode
                @change="handleChange" />
    <a-cascader :options="options"
                :default-value="[['beijing','chaoyang','datunli']]"
                :style="{width:'320px'}"
                placeholder="Please select ..."
                path-mode
                @change="handleChange" />
  </a-space>
</template>

<script>
export default {
  setup() {
    const handleChange = (path) => {
      console.log(path)
    }

    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      options,
      handleChange
    }
  },
}
</script>
```

## Fallback

The component will display the value that does not exist in the options by default, which can be displayed or turned off through `fallback`

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-cascader :options="options" v-model="value" :style="{width:'320px'}" placeholder="Please select ..." multiple />
    <a-cascader :options="options" v-model="value2" :style="{width:'320px'}"
                placeholder="Please select ..." path-mode multiple :fallback="fallback" />
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref(['datunli', 'wuhou']);
    const value2 = ref([['beijing', 'chaoyang', 'datunli'], ['sichuan', 'chengdu', 'wuhou']]);
    const fallback = (value) => {
      return value.map(item => item.toUpperCase()).join('-')
    }

    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      options,
      value,
      value2,
      fallback
    }
  },
}
</script>
```

## Custom FieldNames

The format of the data in `options` can be customized through the `field-names` attribute.

```vue
<template>
  <a-cascader :options="options" :field-names="fieldNames" :style="{width:'320px'}"
            placeholder="Please select ..." />
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const fieldNames = {value: 'city', label: 'text'}
    const options = reactive([
      {
        city: 'beijing',
        text: 'Beijing',
        children: [
          {
            city: 'chaoyang',
            text: 'ChaoYang',
            children: [
              {
                city: 'datunli',
                text: 'Datunli',
              },
            ],
          },
          {
            city: 'haidian',
            text: 'Haidian',
          },
          {
            city: 'dongcheng',
            text: 'Dongcheng',
          },
          {
            city: 'xicheng',
            text: 'Xicheng',
            children: [
              {
                city: 'jinrongjie',
                text: 'Jinrongjie',
              },
              {
                city: 'tianqiao',
                text: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        city: 'shanghai',
        text: 'Shanghai',
        children: [
          {
            city: 'huangpu',
            text: 'Huangpu',
          },
        ],
      },
    ]);

    return {
      fieldNames,
      options
    }
  }
}
</script>
```

## Expand child menu

The first submenu can be expanded on selection by setting `expand-child`

```vue
<template>
  <a-cascader :options="options" :style="{width:'320px'}" placeholder="Please select ..." expand-child/>
</template>

<script>
export default {
  setup() {
    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      options
    }
  },
}
</script>
```

## Cascader Panel

Cascading menu can be used alone, in this case it is the `data display` component

```vue
<template>
  <a-cascader-panel :options="options" v-model="value" expand-child/>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref('');

    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'huangpu',
            label: 'Huangpu',
          },
        ],
      },
    ];
    return {
      value,
      options
    }
  },
}
</script>
```

## Virtual List

How to use the virtual list.

```vue

<template>
  <a-cascader :options="options" :style="{width:'320px'}" placeholder="Please select ..."
              :virtual-list-props="{height:200}" />
</template>

<script>
export default {
  setup() {
    const options = [
      {
        value: 'beijing',
        label: 'Beijing',
        children: [
          {
            value: 'chaoyang',
            label: 'ChaoYang',
            children: [
              {
                value: 'datunli',
                label: 'Datunli',
              },
            ],
          },
          {
            value: 'haidian',
            label: 'Haidian',
          },
          {
            value: 'dongcheng',
            label: 'Dongcheng',
          },
          {
            value: 'xicheng',
            label: 'Xicheng',
            children: [
              {
                value: 'jinrongjie',
                label: 'Jinrongjie',
              },
              {
                value: 'tianqiao',
                label: 'Tianqiao',
              },
            ],
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: Array(1000).fill(null).map((_, index) => {
          return {
            value: `Option ${index}`,
            label: `Option ${index}`
          }
        })
      },
    ];

    return {
      options
    }
  },
}
</script>
```

## API

### `<cascader>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|path-mode|Whether the value is a path|`boolean`|`false`||
|multiple|Whether it is a multi-selection state (The search is turned on by default in the multi-select mode)|`boolean`|`false`||
|model-value **(v-model)**|Value|`string\| number\| Record<string, any>\| (    \| string    \| number    \| Record<string, any>    \| (string \| number \| Record<string, any>)[]  )[]\| undefined`|`-`||
|default-value|Default value (uncontrolled state)|`string\| number\| Record<string, any>\| (    \| string    \| number    \| Record<string, any>    \| (string \| number \| Record<string, any>)[]  )[]\| undefined`|`'' \| undefined \| []`||
|options|Options for cascader|`CascaderOption[]`|`[]`||
|disabled|Whether to disable|`boolean`|`false`||
|error|Whether it is an error state|`boolean`|`false`||
|size|The size of the select|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|allow-search|Whether to allow searching|`boolean`|`false (single) \| true (multiple)`||
|allow-clear|Whether to allow clear|`boolean`|`false`||
|input-value **(v-model)**|The value of the input|`string`|`-`||
|default-input-value|The default value of the input (uncontrolled state)|`string`|`''`||
|popup-visible **(v-model)**|Whether to show the dropdown|`boolean`|`-`||
|expand-trigger|Expand the trigger method of the next level|`'click' \| 'hover'`|`'click'`||
|default-popup-visible|Whether to display the dropdown by default (uncontrolled state)|`boolean`|`false`||
|placeholder|Placeholder|`string`|`-`||
|filter-option|Custom options filter method|`(inputValue: string, option: CascaderOption) => boolean`|`-`||
|popup-container|Mount container for popup|`string \| HTMLElement`|`-`||
|max-tag-count|In multi-select mode, the maximum number of labels displayed. 0 means unlimited|`number`|`0`||
|format-label|Format display content|`(options: CascaderOption[]) => string`|`-`||
|trigger-props|Trigger props of the drop-down menu|`TriggerProps`|`-`||
|check-strictly|Whether to enable strict selection mode|`boolean`|`false`||
|load-more|Data lazy loading function, open the lazy loading function when it is passed in|`(  option: CascaderOption,  done: (children?: CascaderOption[]) => void) => void`|`-`|2.13.0|
|loading|Whether it is loading state|`boolean`|`false`|2.15.0|
|search-option-only-label|Whether the options in the search dropdown show only label|`boolean`|`false`|2.18.0|
|search-delay|Delay time to trigger search event|`number`|`500`|2.18.0|
|field-names|Customize fields in `CascaderOption`|`CascaderFieldNames`|`-`|2.22.0|
|value-key|Used to determine the option key value attribute name|`string`|`'value'`|2.29.0|
|fallback|Options that do not exist in custom values|`boolean\| ((    value:      \| string      \| number      \| Record<string, unknown>      \| (string \| number \| Record<string, unknown>)[]  ) => string)`|`true`|2.29.0|
|expand-child|whether to expand the submenu|`boolean`|`false`|2.29.0|
|virtual-list-props|Pass the virtual list attribute, pass in this parameter to turn on virtual scrolling [VirtualListProps](#VirtualListProps)|`VirtualListProps`|`-`|2.49.0|
|tag-nowrap|Tag content does not wrap|`boolean`|`false`|2.56.1|
### `<cascader>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when the selected value changes|value: `string \| number \| (string \| number \| (string \| number)[])[] \| undefined`|
|input-value-change|Triggered when the input value changes|value: `string`|
|clear|Triggered when the clear button is clicked|-|
|search|Triggered when the user searches|value: `string`|
|popup-visible-change|Triggered when the display state of the dropdown changes|visible: `boolean`|
|focus|Triggered when focus|ev: `FocusEvent`|
|blur|Triggered when blur|ev: `FocusEvent`|
### `<cascader>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|label|Display content of label|data: `CascaderOption`|2.18.0|
|prefix|Prefix|-|2.23.0|
|arrow-icon|Arrow icon for select box|-|2.16.0|
|loading-icon|Loading icon for select box|-|2.16.0|
|search-icon|Search icon for select box|-|2.16.0|
|empty|Display content when the option is empty|-|2.23.0|
|option|Display content of options|data: `CascaderOption`|2.18.0|

### `<cascader-panel>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|path-mode|Whether the value is a path|`boolean`|`false`||
|multiple|Whether it is a multi-selection state (The search is turned on by default in the multi-select mode)|`boolean`|`false`||
|model-value **(v-model)**|Value|`string\| number\| Record<string, any>\| (    \| string    \| number    \| Record<string, any>    \| (string \| number \| Record<string, any>)[]  )[]\| undefined`|`-`||
|default-value|Default value (uncontrolled state)|`string\| number\| Record<string, any>\| (    \| string    \| number    \| Record<string, any>    \| (string \| number \| Record<string, any>)[]  )[]\| undefined`|`'' \| undefined \| []`||
|options|Options for cascader|`CascaderOption[]`|`[]`||
|expand-trigger|Expand the trigger method of the next level|`string`|`'click'`||
|check-strictly|Whether to enable strict selection mode|`boolean`|`false`||
|load-more|Data lazy loading function, open the lazy loading function when it is passed in|`(  option: CascaderOption,  done: (children?: CascaderOption[]) => void) => void`|`-`|2.13.0|
|field-names|Customize fields in `CascaderOption`|`CascaderFieldNames`|`-`|2.22.0|
|value-key|Used to determine the option key value attribute name|`string`|`'value'`|2.29.0|
|expand-child|whether to expand the submenu|`boolean`|`false`|2.29.0|
### `<cascader-panel>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Triggered when the selected value changes|value: `string \| number \| (string \| number \| (string \| number)[])[] \| undefined`|
### `<cascader-panel>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|empty|Display content when the option is empty|-|2.23.0|

### CascaderOption

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|value|Option value, version 2.29.0 supports objects|`string \| number \| Record<string, any>`|`-`||
|label|Option text|`string`|`-`||
|render|Custom render|`RenderFunction`|`-`||
|disabled|Whether to disable|`boolean`|`false`||
|tagProps|Displayed tag attributes|`TagProps`|`-`|2.8.0|
|children|Next level options|`CascaderOption[]`|`-`||
|isLeaf|Whether it is a leaf node|`boolean`|`false`||
