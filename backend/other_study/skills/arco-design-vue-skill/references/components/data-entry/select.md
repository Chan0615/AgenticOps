---
name: arco-vue-select
description: "When users need to select one or more from a group of similar data, they can use the drop-down selector, click and select the corresponding item. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Select

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of selectors.
Use the `trigger-props` property to customize the properties of the drop-down box, for example, the drop-down box can automatically adapt to the minimum width.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-select :style="{width:'320px'}" placeholder="Please select ...">
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
    </a-select>
    <a-select :style="{width:'320px'}" placeholder="Please select ...">
      <a-option :value="true">Yes</a-option>
      <a-option :value="false">No</a-option>
    </a-select>
    <a-select defaultValue="Beijing" :style="{width:'320px'}" placeholder="Please select ..." disabled>
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
    </a-select>
    <a-select v-model="value" :style="{width:'320px'}" placeholder="Please select ...">
      <a-option v-for="item of data" :value="item" :label="item.label" />
    </a-select>
    <div>Select Value: {{ value }}</div>
    <a-select :style="{width:'160px'}" placeholder="Select" :trigger-props="{ autoFitPopupMinWidth: true }">
      <a-option>Beijing-Beijing-Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
    </a-select>

  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref();
    const data = [{
      value: 'beijing',
      label: 'Beijing',
      other: 'extra'
    }, {
      value: 'shanghai',
      label: 'Shanghai',
      other: 'extra'
    }, {
      value: 'guangzhou',
      label: 'Guangzhou',
      other: 'extra'
    }, {
      value: 'chengdu',
      label: 'Chengdu',
      other: 'extra'
    }]

    return {
      value,
      data
    }
  },
}
</script>
```

## Allow Clear

By setting `allow-clear`, the clear button is displayed.

```vue

<template>
  <a-select :style="{width:'320px'}" v-model="value" placeholder="Please select ..." allow-clear>
    <a-option>Beijing</a-option>
    <a-option>Shanghai</a-option>
    <a-option>Guangzhou</a-option>
    <a-option disabled>Disabled</a-option>
  </a-select>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref('Shanghai');
    return {
      value
    }
  },
}
</script>
```

## Multiple Select

By setting `multiple`, the selector can support multiple selection. In addition, the maximum number of tags displayed
can be set by `max-tag-count`.

```vue

<template>
  <div style="margin-bottom: 10px">
    <a-switch v-model="scrollbar" />
    Virtual Scrollbar
  </div>
  <a-space direction="vertical" size="large">
    <a-select :default-value="['Beijing','Shanghai']" :style="{width:'360px'}" placeholder="Please select ..." multiple
              :scrollbar="scrollbar">
      <a-option>Beijing</a-option>
      <a-option :tag-props="{color:'red'}">Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
    <a-select :default-value="['Beijing','Shanghai','Guangzhou']" :style="{width:'360px'}"
              placeholder="Please select ..." multiple :max-tag-count="2" allow-clear :scrollbar="scrollbar">
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Chengdu</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
    <a-select :default-value="['Beijing','Shanghai']" :style="{width:'360px'}" placeholder="Please select ..." multiple
              :limit="2" :scrollbar="scrollbar">
      <a-option>Beijing</a-option>
      <a-option :tag-props="{color:'red'}">Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
  </a-space>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const scrollbar = ref(true);

    return {
      scrollbar
    }
  }
}
</script>
```

## Select Size

The selection box is divided into four sizes: `mini`, `small`, `medium`, and `large`.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-radio-group type="button" v-model="size">
      <a-radio value="mini">Mini</a-radio>
      <a-radio value="small">Small</a-radio>
      <a-radio value="medium">Medium</a-radio>
      <a-radio value="large">Large</a-radio>
    </a-radio-group>
    <a-select default-value="Beijing" :style="{width:'320px'}" :size="size" placeholder="Please select ...">
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
    </a-select>
    <a-select :default-value="['Beijing','Shanghai']" :style="{width:'320px'}" :size="size"
              placeholder="Please select ..." multiple>
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Chengdu</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const size = ref('medium');

    return {
      size
    }
  },
}
</script>
```

## Loading

Select boxes and drop-down menus show loading status.

```vue
<template>
  <a-select :style="{width:'320px'}" placeholder="Please select ..." loading>
    <a-option>Beijing</a-option>
    <a-option>Shanghai</a-option>
    <a-option>Guangzhou</a-option>
    <a-option disabled>Disabled</a-option>
  </a-select>
</template>
```

## Dropdown Header

custom dropdown menu header

```vue
<template>
  <a-space>
    <a-select :default-value="'Beijing'" :style="{width:'360px'}" placeholder="Please select ..." multiple>
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Wuhan</a-option>
      <template #header>
        <div style="padding: 6px 12px;" >
          <a-checkbox value="1">Select all</a-checkbox>
        </div>
      </template>
    </a-select>

    <a-select :default-value="'Beijing'" :style="{width:'360px'}" placeholder="Please select ..." multiple show-header-on-empty>
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Wuhan</a-option>
      <template #header>
        <div style="padding: 6px 12px;" >
          <a-checkbox value="1">Select all</a-checkbox>
        </div>
      </template>
    </a-select>
  </a-space>
</template>
```

## Dropdown Footer

custom dropdown menu footer

```vue
<template>
  <a-space>
    <a-select :default-value="'Beijing'" :style="{width:'360px'}" placeholder="Please select ..." allow-search>
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Wuhan</a-option>
      <template #footer>
        <div style="padding: 6px 0; text-align: center;">
          <a-button>Click Me</a-button>
        </div>
      </template>
    </a-select>
    <a-select :default-value="'Beijing'" :style="{width:'360px'}" placeholder="Please select ..." allow-search show-footer-on-empty>
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Wuhan</a-option>
      <template #footer>
        <div style="padding: 6px 0; text-align: center;">
          <a-button>Click Me</a-button>
        </div>
      </template>
    </a-select>
  </a-space>
</template>
```

## Borderless

Set `bordered="false"` to enable borderless mode, which is often used for immersive use.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-select :style="{width:'100%'}" placeholder="Please select ..." :bordered="false">
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
    </a-select>
    <a-select :default-value="['Beijing','Shanghai']" :style="{width:'360px'}" placeholder="Please select ..." multiple :bordered="false">
      <a-option>Beijing</a-option>
      <a-option :tag-props="{color:'red'}">Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
  </a-space>
</template>
```

## To Create

By setting `allow-create`, the selector can create items that do not exist in the options.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-select :style="{width:'320px'}" placeholder="Please select ..." allow-create>
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Chengdu</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
    <a-select :style="{width:'320px'}" placeholder="Please select ..." multiple allow-create>
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Chengdu</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
  </a-space>
</template>
```

## Allow Search

By setting `allow-search`, you can make the selector support searching for options, and you can customize the search with `filter-option`.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-select :style="{width:'320px'}" placeholder="Please select ..." allow-search>
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Chengdu</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
    <a-select :style="{width:'320px'}" placeholder="Please select ..." :allow-search="{ retainInputValue: true }">
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Chengdu</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
    <a-select :options="options" :style="{width:'320px'}" :loading="loading" placeholder="Please select ..." multiple
              @search="handleSearch" />
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const options = ref(['Option1', 'Option2', 'Option3']);
    const loading = ref(false);

    const handleSearch = (value) => {
      if (value) {
        loading.value = true;
        window.setTimeout(() => {
          options.value = [`${value}-Option1`, `${value}-Option2`, `${value}-Option3`]
          loading.value = false;
        }, 2000)
      } else {
        options.value = []
      }
    };

    return {
      options,
      loading,
      handleSearch
    }
  },
}
</script>
```

## Dropdown Scroll

You can monitor the scroll event of the drop-down menu through `dropdown-scroll`. Or use `dropdown-reach-bottom` to monitor the event of the drop-down menu scrolling to the bottom.

```vue
<template>
  <a-select
    :style="{width:'320px'}"
    default-value="Beijing"
    placeholder="Please select ..."
    @dropdown-scroll="handleScroll"
    @dropdown-reach-bottom="handleReachBottom"
  >
    <a-option>Beijing</a-option>
    <a-option>Shanghai</a-option>
    <a-option>Guangzhou</a-option>
    <a-option disabled>Disabled</a-option>
    <a-option>Shenzhen</a-option>
    <a-option>Chengdu</a-option>
    <a-option>Wuhan</a-option>
  </a-select>
</template>

<script>
export default {
  setup() {
    const handleScroll = (ev) => {
      console.log('scroll', ev)
    }
    const handleReachBottom = (ev) => {
      console.log('reach the bottom', ev)
    }

    return {
      handleScroll,
      handleReachBottom
    }
  },
}
</script>
```

## Fallback Option

Use `fallback-option` to customize the value that does not exist in the option. By default, the value of the option that does not exist in the input box will display. It may be used when the options have not been obtained, or the options have changed during remote search.

```vue

<template>
  <a-space direction="vertical" size="large">
    <a-select defaultValue="Shanxi" :style="{width:'320px'}" placeholder="Please select ..." :fallback-option="fallback">
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
    </a-select>
    <a-select defaultValue="Shanxi" :style="{width:'320px'}" placeholder="Please select ..." :fallback-option="fallback" :show-extra-options="false">
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
    </a-select>
    <a-select :default-value="['Shanxi','Nanjing','Hangzhou']" :style="{width:'320px'}" placeholder="Please select ..." multiple :fallback-option="fallback">
      <a-option>Beijing</a-option>
      <a-option>Shanghai</a-option>
      <a-option>Guangzhou</a-option>
      <a-option disabled>Disabled</a-option>
      <a-option>Shenzhen</a-option>
      <a-option>Chengdu</a-option>
      <a-option>Wuhan</a-option>
    </a-select>
  </a-space>
</template>

<script>
export default {
  setup() {
    const fallback = (value) => {
      return {
        value,
        label: `++${value}++`
      }
    };
    return {
      fallback
    }
  },
}
</script>
```

## Remote search

Use the `search` event to search remotely and change options.

```vue

<template>
  <a-space direction="vertical" size="large">
    <div>Show selections after search options</div>
    <a-select :style="{width:'320px'}" :loading="loading" placeholder="Please select ..." multiple
              @search="handleSearch" :filter-option="false">
      <a-option v-for="item of options" :value="item">{{item}}</a-option>
    </a-select>
    <div>Hide selections after search options</div>
    <a-select :options="options" :style="{width:'320px'}" :loading="loading" placeholder="Please select ..." multiple
              @search="handleSearch" :filter-option="false" :show-extra-options="false" />
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const options = ref(['Option1', 'Option2', 'Option3']);
    const loading = ref(false);

    const handleSearch = (value) => {
      if (value) {
        loading.value = true;
        window.setTimeout(() => {
          options.value = [`${value}-Option1`, `${value}-Option2`, `${value}-Option3`]
          loading.value = false;
        }, 2000)
      } else {
        options.value = []
      }
    };

    return {
      options,
      loading,
      handleSearch
    }
  },
}
</script>
```

## Group

Use the `optgroup` component to add grouping options.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-select :style="{width:'320px'}" placeholder="Please select ...">
      <a-optgroup label="Group-1">
        <a-option>Beijing</a-option>
        <a-option>Shanghai</a-option>
      </a-optgroup>
      <a-optgroup label="Group-2">
        <a-option>Guangzhou</a-option>
        <a-option disabled>Disabled</a-option>
        <a-option>Shenzhen</a-option>
      </a-optgroup>
      <a-optgroup label="Group-3">
        <a-option>Chengdu</a-option>
        <a-option>Wuhan</a-option>
      </a-optgroup>
    </a-select>
    <a-select :style="{width:'320px'}" placeholder="Please select ..." multiple>
      <a-optgroup label="Group-1">
        <a-option>Beijing</a-option>
        <a-option>Shanghai</a-option>
      </a-optgroup>
      <a-optgroup label="Group-2">
        <a-option>Guangzhou</a-option>
        <a-option disabled>Disabled</a-option>
        <a-option>Shenzhen</a-option>
      </a-optgroup>
      <a-optgroup label="Group-3">
        <a-option>Chengdu</a-option>
        <a-option>Wuhan</a-option>
      </a-optgroup>
    </a-select>
  </a-space>
</template>
```

## Label

The display content of the select box can be customized through the `#label` slot.

```vue
<template>
  <a-select default-value="Beijing" :style="{width:'320px'}" placeholder="Please select ...">
    <template #label="{ data }">
      <span><icon-plus/>{{data?.label}}</span>
    </template>
    <a-option>Beijing</a-option>
    <a-option>Shanghai</a-option>
    <a-option>Guangzhou</a-option>
    <a-option disabled>Disabled</a-option>
  </a-select>
</template>

<script>
import { IconPlus } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconPlus }
};
</script>
```

## Linkage Select

Show how to realize the linkage selection box.

```vue

<template>
  <a-space>
    <a-select :style="{width:'200px'}" v-model="province">
      <a-option v-for="value of Object.keys(data)">{{value}}</a-option>
    </a-select>
    <a-select :style="{width:'200px'}" :options="data[province] || []" v-model="city" />
  </a-space>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  setup() {
    const province = ref('Sichuan');
    const city = ref('Chengdu');
    const data = {
      Beijing: ['Haidian', 'Chaoyang', 'Changping'],
      Sichuan: ['Chengdu', 'Mianyang', 'Aba'],
      Guangdong: ['Guangzhou', 'Shenzhen', 'Shantou']
    };

    watch(province, () => {
      city.value = ''
    })

    return {
      province,
      city,
      data
    }
  },
}
</script>
```

## Custom FieldNames

The format of the data in `options` can be customized through the `field-names` attribute.

```vue
<template>
  <a-select v-model="value" :options="options" :field-names="fieldNames" :style="{width:'320px'}"
            placeholder="Please select ..." />
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const value = ref('bj');
    const fieldNames = {value: 'city', label: 'text'}
    const options = reactive([
      {
        city: 'bj',
        text: 'Beijing'
      },
      {
        city: 'sh',
        text: 'Shanghai'
      },
      {
        city: 'gz',
        text: 'Guangzhou'
      },
      {
        city: 'cd',
        text: 'Chengdu'
      },
    ]);

    return {
      value,
      fieldNames,
      options
    }
  }
}
</script>
```

## Virtual List

How to use the virtual list.

```vue

<template>
  <a-select :style="{width:'320px'}" :options="options" placeholder="Please select ..." :virtual-list-props="{height:200}" />
</template>

<script>
export default {
  setup() {
    const options = Array(1000).fill(null).map((_, index) => `Option ${index}`);

    return {
      options
    }
  },
}
</script>
```

## API

### `<select>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|multiple|Whether to open multi-select mode (The search is turned on by default in the multi-select mode)|`boolean`|`false`||
|model-value **(v-model)**|Value|`string\| number\| boolean\| Record<string, any>\| (string \| number \| boolean \| Record<string, any>)[]`|`-`||
|default-value|Default value (uncontrolled mode)|`string\| number\| boolean\| Record<string, unknown>\| (string \| number \| boolean \| Record<string, unknown>)[]`|`'' \| []`||
|input-value **(v-model)**|The value of the input|`string`|`-`||
|default-input-value|The default value of the input (uncontrolled mode)|`string`|`''`||
|size|The size of the select|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|placeholder|Placeholder|`string`|`-`||
|loading|Whether it is loading state|`boolean`|`false`||
|disabled|Whether to disable|`boolean`|`false`||
|error|Whether it is an error state|`boolean`|`false`||
|allow-clear|Whether to allow clear|`boolean`|`false`||
|allow-search|Whether to allow searching|`boolean \| { retainInputValue?: boolean }`|`false (single) \| true (multiple)`||
|allow-create|Whether to allow creation|`boolean`|`false`||
|max-tag-count|In multi-select mode, the maximum number of labels displayed. 0 means unlimited|`number`|`0`||
|popup-container|Mount container for popup|`string \| HTMLElement`|`-`||
|bordered|Whether to display the border of the input box|`boolean`|`true`||
|default-active-first-option|Whether to select the first option by default when there is no value|`boolean`|`true`|2.43.0|
|popup-visible **(v-model)**|Whether to show the dropdown|`boolean`|`-`||
|default-popup-visible|Whether the popup is visible by default (uncontrolled mode)|`boolean`|`false`||
|unmount-on-close|Whether to destroy the element when the dropdown is closed|`boolean`|`false`||
|filter-option|Whether to filter options|`boolean \| ((inputValue: string, option: SelectOptionData) => boolean)`|`true`||
|options|Option data|`(string \| number \| boolean \| SelectOptionData \| SelectOptionGroup)[]`|`[]`||
|virtual-list-props|Pass the virtual list attribute, pass in this parameter to turn on virtual scrolling [VirtualListProps](#VirtualListProps)|`VirtualListProps`|`-`||
|trigger-props|Trigger props of the drop-down menu|`TriggerProps`|`-`||
|format-label|Format display content|`(data: SelectOptionData) => string`|`-`||
|fallback-option|Options that do not exist in custom values|`boolean\| ((    value: string \| number \| boolean \| Record<string, unknown>  ) => SelectOptionData)`|`true`|2.10.0|
|show-extra-options|Options that do not exist in custom values|`boolean`|`true`|2.10.0|
|value-key|Used to determine the option key value attribute name|`string`|`'value'`|2.18.0|
|search-delay|Delay time to trigger search event|`number`|`500`|2.18.0|
|limit|Maximum number of choices in multiple choice|`number`|`0`|2.18.0|
|field-names|Customize fields in `SelectOptionData`|`SelectFieldNames`|`-`|2.22.0|
|scrollbar|Whether to enable virtual scroll bar|`boolean \| ScrollbarProps`|`true`|2.38.0|
|show-header-on-empty|Whether to display the header in the empty state|`boolean`|`false`||
|show-footer-on-empty|Whether to display the footer in the empty state|`boolean`|`false`||
|tag-nowrap|Tag content does not wrap|`boolean`|`false`|2.56.1|
### `<select>` Events

|Event Name|Description|Parameters|version|
|---|---|---|:---|
|change|Triggered when the value changes|value: ` string \| number \| boolean \| Record<string, any> \| (string \| number \| boolean \| Record<string, any>)[] `||
|input-value-change|Triggered when the value of the input changes|inputValue: `string`||
|popup-visible-change|Triggered when the display state of the drop-down box changes|visible: `boolean`||
|clear|Triggered when the clear button is clicked|-||
|remove|Triggered when the delete button of the label is clicked|removed: `string \| number \| boolean \| Record<string, any> \| undefined`||
|search|Triggered when the user searches|inputValue: `string`||
|dropdown-scroll|Triggered when the drop-down scrolls|-||
|dropdown-reach-bottom|Triggered when the drop-down menu is scrolled to the bottom|-||
|exceed-limit|Triggered when multiple selection exceeds the limit|value: `string \| number \| boolean \| Record<string, any> \| undefined`<br>ev: `Event`|2.18.0|
### `<select>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|trigger|Custom trigger element|-|2.22.0|
|prefix|Prefix|-|2.22.0|
|search-icon|Search icon for select box|-|2.16.0|
|loading-icon|Loading icon for select box|-|2.16.0|
|arrow-icon|Arrow icon for select box|-|2.16.0|
|footer|The footer of the drop-down box|-||
|header|The header of the drop-down box|-|2.43.0|
|label|Display content of label|data: `SelectOptionData`||
|option|Display content of options|data: `SelectOptionData`||
|empty|Display content when the option is empty|-||

### `<option>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|value|Option value (if not filled, it will be obtained from the content)|`string\|number\|boolean\|object`|`-`||
|label|Option label (if not filled, it will be obtained from the content)|`string`|`-`||
|disabled|Whether to disable|`boolean`|`false`||
|tag-props|Displayed tag attributes|`TagProps`|`-`|2.8.0|
|extra|Extra data|`object`|`-`|2.10.0|
|index|index for manually specifying option|`number`|`-`|2.20.0|

### `<optgroup>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|label|Title of option group|`string`|`-`|
### `<optgroup>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|label|Title of option group|-|2.10.0|

### Type

```ts
/**
 * @zh Option
 * @en Option
 */
type Option = string | number | SelectOptionData | SelectOptionGroup;

/**
 * @zh Filter
 * @en Filter
 */
type FilterOption = boolean | ((inputValue: string, option: SelectOptionData) => boolean);
```

### SelectOptionData

|Name|Description|Type|Default|
|---|---|---|:---:|
|value|Option Value|`string \| number \| boolean \| Record<string, unknown>`|`-`|
|label|Option content|`string`|`-`|
|disabled|Whether to disable|`boolean`|`false`|
|tagProps|Props of the multi-select label corresponding to the option|`any`|`-`|
|render|Custom Render|`RenderFunction`|`-`|

### SelectOptionGroup

|Name|Description|Type|Default|
|---|---|---|:---:|
|isGroup|Whether it is an option group|`true`|`-`|
|label|Option group title|`string`|`-`|
|options|Options in the option group|`SelectOption[]`|`-`|

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

### Use `Object` format as option value
When using the `Object` format as the value of the option, you need to specify the field name to obtain the unique identifier for the selector through the `value-key` attribute, and the default value is `value`.
In addition, the object value of `value` needs to be defined in `setup`, and the object cannot be created in the template, which will lead to repeated rendering of the `Option` component.

For example, when I need to specify `key` as a unique identifier:
```vue
<template>
  <a-select v-model="value" :style="{width:'320px'}" placeholder="Please select ..." value-key="key">
    <a-option v-for="item of data" :value="item" :label="item.label" />
  </a-select>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value = ref();
    const data = [{
      value: 'beijing',
      label: 'Beijing',
      key: 'extra1'
    }, {
      value: 'shanghai',
      label: 'Shanghai',
      key: 'extra2'
    }, {
      value: 'guangzhou',
      label: 'Guangzhou',
      key: 'extra3'
    }, {
      value: 'chengdu',
      label: 'Chengdu',
      key: 'extra4'
    }]

    return {
      value,
      data
    }
  },
}
</script>
```

### Dropdown menu separation issue in scroll container
The `Select` component does not enable the container scrolling event monitoring function by default. If you encounter the problem of separating the drop-down menu in the scrolling container, you can manually enable the `updateAtScroll` function of the internal `Trigger` component.
If this is the case in the global environment, you can use the `ConfigProvider` component to enable this property by default.

```vue
<a-select :trigger-props="{updateAtScroll:true}"></a-select>
```
