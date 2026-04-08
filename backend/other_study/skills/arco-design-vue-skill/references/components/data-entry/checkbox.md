---
name: arco-vue-checkbox
description: "In a set of data, the user can select one or more data through the check box. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Checkbox

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of checkbox.

```vue
<template>
  <a-checkbox value="1">Option 1</a-checkbox>
</template>
```

## Controlled

Control whether the check box is selected

```vue
<template>
  <a-space size="large">
    <a-checkbox v-model="checked1">v-model</a-checkbox>
    <a-checkbox :model-value="true">binding value</a-checkbox>
    <a-checkbox :model-value="checked2">binding value2</a-checkbox>
    <a-checkbox :default-checked="true">uncontrolled state</a-checkbox>
  </a-space>
  <div :style="{ marginTop: '20px' }">
    <a-button type="primary" @click="handleSetCheck">
      {{ checked2 ? 'uncheck' : 'check' }} value2
    </a-button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const checked1 = ref(false);
    const checked2 = ref(false);

    const handleSetCheck = () => {
      checked2.value = !checked2.value;
    };

    return {
      checked1,
      checked2,
      handleSetCheck,
    };
  },
};
</script>
```

## Disabled

Disable the checkbox.

```vue
<template>
  <a-space size="large">
    <a-checkbox value="1" disabled>Disabled Option 1</a-checkbox>
    <a-checkbox :default-checked="true" disabled>Disabled Option 2</a-checkbox>
  </a-space>
</template>
```

## Checkbox Group

Display the checkbox group through the `<a-checkbox-group>` component. Set `direction="vertical"` to show the vertical checkbox group.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-checkbox-group :default-value="['1']">
      <a-checkbox value="1">Option 1</a-checkbox>
      <a-checkbox value="2">Option 2</a-checkbox>
      <a-checkbox value="3">Option 3</a-checkbox>
    </a-checkbox-group>
    <a-checkbox-group direction="vertical">
      <a-checkbox value="1">Option 1</a-checkbox>
      <a-checkbox value="2">Option 2</a-checkbox>
      <a-checkbox value="3">Option 3</a-checkbox>
    </a-checkbox-group>
  </a-space>
</template>
```

## Checkbox Group options

`a-checkbox-group` set child elements through `options` prop

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-checkbox-group v-model="value1" :options="plainOptions" />
    <a-checkbox-group v-model="value2" :options="options" />
    <a-checkbox-group v-model="value2" :options="options">
      <template #label="{ data }">
        <a-tag>{{ data.label }}</a-tag>
      </template>
    </a-checkbox-group>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value1 = ref(['Plain 1']);
    const plainOptions = ['Plain 1', 'Plain 2', 'Plain 3'];

    const value2 = ref(['1']);
    const options = [
      { label: 'Option 1', value: '1' },
      { label: 'Option 2', value: '2' },
      { label: 'Option 3', value: '3', disabled: true },
    ];

    return {
      plainOptions,
      options,
      value1,
      value2,
    };
  },
};
</script>
```

## Limit the number of boxes that can be checked

Limit the maximum number of items that can be checked by setting `max`.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-checkbox-group :max="2" v-model="value1" :options="plainOptions" />
    <a-checkbox-group :max="2" :default-value="['1']">
      <a-checkbox value="1" disabled>Option 1</a-checkbox>
      <a-checkbox value="2">Option 2</a-checkbox>
      <a-checkbox value="3">Option 3</a-checkbox>
      <a-checkbox value="4">Option 4</a-checkbox>
    </a-checkbox-group>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value1 = ref(['Plain 1']);
    const plainOptions = ['Plain 1', 'Plain 2', 'Plain 3', 'Plain 4'];

    return {
      plainOptions,
      value1,
    };
  },
};
</script>
```

## Check All

When implementing the function of selecting all, you can display the half-selection effect through the indeterminate property.

```vue
<template>
  <a-space direction="vertical">
    <a-checkbox :model-value="checkedAll" :indeterminate="indeterminate" @change="handleChangeAll">Check All
    </a-checkbox>
    <a-checkbox-group v-model="data" @change="handleChange">
      <a-checkbox value="1">Option 1</a-checkbox>
      <a-checkbox value="2">Option 2</a-checkbox>
      <a-checkbox value="3">Option 3</a-checkbox>
    </a-checkbox-group>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const indeterminate = ref(false)
    const checkedAll = ref(false)
    const data = ref([])

    const handleChangeAll = (value) => {
      indeterminate.value = false;
      if (value) {
        checkedAll.value = true;
        data.value = ['1', '2', '3']
      } else {
        checkedAll.value = false;
        data.value = []
      }
    }

    const handleChange = (values) => {
      if (values.length === 3) {
        checkedAll.value = true
        indeterminate.value = false;
      } else if (values.length === 0) {
        checkedAll.value = false
        indeterminate.value = false;
      } else {
        checkedAll.value = false
        indeterminate.value = true;
      }
    }

    return {
      indeterminate,
      checkedAll,
      data,
      handleChangeAll,
      handleChange
    }
  },
}
</script>
```

## Layout

We can use `<a-checkbox>` and `<a-grid>` in `<a-checkbox-group>`, to implement complex layout.

```vue
<template>
  <a-checkbox-group v-model="checkedValue">
    <a-grid :cols="3" :colGap="24" :rowGap="16">
      <a-grid-item>
        <a-checkbox value="1">Option 1</a-checkbox>
      </a-grid-item>
      <a-grid-item>
        <a-checkbox value="2" disabled>Option 2</a-checkbox>
      </a-grid-item>
      <a-grid-item>
        <a-checkbox value="3">Option 3</a-checkbox>
      </a-grid-item>
      <a-grid-item>
        <a-checkbox value="4">Option 4</a-checkbox>
      </a-grid-item>
      <a-grid-item>
        <a-checkbox value="5">Option 5</a-checkbox>
      </a-grid-item>
    </a-grid>
  </a-checkbox-group>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const checkedValue = ref(['1', '2']);

    return {
      checkedValue,
    };
  },
};
</script>
```

## Custom CheckBox Display

Use the #checkbox slot to customize the display of checkboxes

```vue
<template>
  <a-checkbox-group :default-value="['1']">
    <a-checkbox value="1">
      <template #checkbox="{ checked }">
        <a-tag :checked="checked" checkable>This is a tag checkbox 1</a-tag>
      </template>
    </a-checkbox>
    <a-checkbox value="2">
      <template #checkbox="{ checked }">
        <a-tag :checked="checked" checkable>This is a tag checkbox 2</a-tag>
      </template>
    </a-checkbox>
    <a-checkbox value="3">
      <template #checkbox="{ checked }">
        <a-tag :checked="checked" checkable>This is a tag checkbox 3</a-tag>
      </template>
    </a-checkbox>
  </a-checkbox-group>

  <div :style="{ marginTop: '20px' }">
    <a-checkbox-group :default-value="[1]">
      <template v-for="item in 2" :key="item">
        <a-checkbox :value="item">
          <template #checkbox="{ checked }">
            <a-space
              align="start"
              class="custom-checkbox-card"
              :class="{ 'custom-checkbox-card-checked': checked }"
            >
              <div class="custom-checkbox-card-mask">
                <div class="custom-checkbox-card-mask-dot" />
              </div>
              <div>
                <div class="custom-checkbox-card-title">
                  Checkbox Card {{ item }}
                </div>
                <a-typography-text type="secondary">
                  this is a text
                </a-typography-text>
              </div>
            </a-space>
          </template>
        </a-checkbox>
      </template>
    </a-checkbox-group>
  </div>
</template>

<style scoped>
.custom-checkbox-card {
  padding: 10px 16px;
  border: 1px solid var(--color-border-2);
  border-radius: 4px;
  width: 250px;
  box-sizing: border-box;
}

.custom-checkbox-card-mask {
  height: 14px;
  width: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 2px;
  border: 1px solid var(--color-border-2);
  box-sizing: border-box;
}

.custom-checkbox-card-mask-dot {
  width: 8px;
  height: 8px;
  border-radius: 2px;
}

.custom-checkbox-card-title {
  color: var(--color-text-1);
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
}

.custom-checkbox-card:hover,
.custom-checkbox-card-checked,
.custom-checkbox-card:hover .custom-checkbox-card-mask,
.custom-checkbox-card-checked .custom-checkbox-card-mask {
  border-color: rgb(var(--primary-6));
}

.custom-checkbox-card-checked {
  background-color: var(--color-primary-light-1);
}

.custom-checkbox-card:hover .custom-checkbox-card-title,
.custom-checkbox-card-checked .custom-checkbox-card-title {
  color: rgb(var(--primary-6));
}

.custom-checkbox-card-checked .custom-checkbox-card-mask-dot {
  background-color: rgb(var(--primary-6));
}
</style>
```

## API

### `<checkbox>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|model-value **(v-model)**|Value|`boolean \| Array<string \| number \| boolean>`|`-`|
|default-checked|Whether checked by default (uncontrolled state)|`boolean`|`false`|
|value|The `value` of the option|`string\|number\|boolean`|`-`|
|disabled|Whether to disable|`boolean`|`false`|
|indeterminate|Whether it is half-selected|`boolean`|`false`|
### `<checkbox>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Trigger when the value changes|value: ` boolean \| (string \| number \| boolean)[] `<br>ev: `Event`|
### `<checkbox>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|checkbox|Custom checkbox|checked: `boolean`<br>disabled: `boolean`|2.18.0|

### `<checkbox-group>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`Array<string \| number \| boolean>`|`-`||
|default-value|Default value (uncontrolled state)|`Array<string \| number \| boolean>`|`[]`||
|max|Support the maximum number of selections|`number`|`-`|2.36.0|
|options|Options|`Array<string \| number \| CheckboxOption>`|`-`|2.27.0|
|direction|Arrangement direction of checkboxes|`Direction`|`'horizontal'`||
|disabled|Whether to disable|`boolean`|`false`||
### `<checkbox-group>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Trigger when the value changes|value: `(string \| number \| boolean)[]`<br>ev: `Event`|
### `<checkbox-group>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|checkbox|Custom checkbox|checked: `boolean`<br>disabled: `boolean`|2.27.0|
|label|checkbox label content|data: `CheckboxOption`|2.27.0|

### CheckboxOption

|Name|Description|Type|Default|
|---|---|---|:---:|
|label|label content|`RenderContent`|`-`|
|value|The `value` of the option|`string \| number`|`-`|
|disabled|Whether to disable|`boolean`|`false`|
|indeterminate|Whether it is half-selected|`boolean`|`false`|
