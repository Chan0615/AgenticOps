---
name: arco-vue-radio
description: "In a set of related and mutually exclusive data, the user can only select one option. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Radio

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of radio.

```vue
<template>
  <a-space size="large">
    <a-radio value="radio">Radio</a-radio>
    <a-radio value="disabled radio" :default-checked="true" disabled>Disabled Radio</a-radio>
  </a-space>
</template>
```

## Controlled

Control whether the radio is selected

```vue
<template>
  <a-space size="large">
    <a-radio v-model="checked1">v-model</a-radio>
    <a-radio :model-value="true">binding "true"</a-radio>
    <a-radio :model-value="checked2">binding value2</a-radio>
    <a-radio :default-checked="true">uncontrolled state</a-radio>
  </a-space>
  <div :style="{ marginTop: '20px' }">
    <a-space size="large">
      <a-button type="primary" @click="handleSetCheck">
        {{ checked2 ? 'uncheck' : 'check' }} value2
      </a-button>
      <a-button @click="handleReset"> reset all </a-button>
    </a-space>
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

    const handleReset = () => {
      checked1.value = false;
      checked2.value = false;
    };

    return {
      checked1,
      checked2,
      handleSetCheck,
      handleReset,
    };
  },
};
</script>
```

## Radio Group

The radio group is displayed through the `<a-radio-group>` component.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-radio-group>
      <a-radio value="A">A</a-radio>
      <a-radio value="B">B</a-radio>
      <a-radio value="C">C</a-radio>
      <a-radio value="D">D</a-radio>
    </a-radio-group>
    <a-radio-group>
      <a-radio value="A">A</a-radio>
      <a-radio value="B">B</a-radio>
      <a-radio value="C">C</a-radio>
      <a-radio value="D" disabled>D</a-radio>
    </a-radio-group>
  </a-space>
</template>
```

## Radio group options

`a-radio-group` set child elements through `options` prop

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-radio-group v-model="value1" :options="plainOptions" />
    <a-radio-group v-model="value2" :options="options" />
    <a-radio-group v-model="value2" :options="options">
      <template #label="{ data }">
        <a-tag>{{ data.label }}</a-tag>
      </template>
    </a-radio-group>
  </a-space>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const value1 = ref('plain 1');
    const plainOptions = ['plain 1', 'plain 2', 'plain 3'];

    const value2 = ref('1');
    const options = [
      { label: 'option 1', value: '1' },
      { label: 'option 2', value: '2' },
      { label: 'option 3', value: '3', disabled: true },
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

## Radio Group Direction

By setting `direction="vertical"`, you can display the vertical radio group.

```vue
<template>
  <a-radio-group direction="vertical">
    <a-radio value="A">A</a-radio>
    <a-radio value="B">B</a-radio>
    <a-radio value="C">C</a-radio>
    <a-radio value="D">D</a-radio>
  </a-radio-group>
</template>
```

## Button Radio Group

By specifying `type="button"`, a radio group of button types can be displayed.

```vue
<template>
  <a-radio-group type="button">
    <a-radio value="Beijing">Beijing</a-radio>
    <a-radio value="Shanghai">Shanghai</a-radio>
    <a-radio value="Guangzhou">Guangzhou</a-radio>
    <a-radio value="Shenzhen">Shenzhen</a-radio>
  </a-radio-group>
</template>
```

## Button Radio Group Size

The radio buttons of the button type have four sizes of `mini`, `small`, `medium`, and `large`.

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-radio-group type="button" size="mini">
      <a-radio value="Beijing">Beijing</a-radio>
      <a-radio value="Shanghai">Shanghai</a-radio>
      <a-radio value="Guangzhou">Guangzhou</a-radio>
      <a-radio value="Shenzhen">Shenzhen</a-radio>
    </a-radio-group>
    <a-radio-group type="button" size="small">
      <a-radio value="Beijing">Beijing</a-radio>
      <a-radio value="Shanghai">Shanghai</a-radio>
      <a-radio value="Guangzhou">Guangzhou</a-radio>
      <a-radio value="Shenzhen">Shenzhen</a-radio>
    </a-radio-group>
    <a-radio-group type="button">
      <a-radio value="Beijing">Beijing</a-radio>
      <a-radio value="Shanghai">Shanghai</a-radio>
      <a-radio value="Guangzhou">Guangzhou</a-radio>
      <a-radio value="Shenzhen">Shenzhen</a-radio>
    </a-radio-group>
    <a-radio-group type="button" size="large">
      <a-radio value="Beijing">Beijing</a-radio>
      <a-radio value="Shanghai">Shanghai</a-radio>
      <a-radio value="Guangzhou">Guangzhou</a-radio>
      <a-radio value="Shenzhen">Shenzhen</a-radio>
    </a-radio-group>
  </a-space>
</template>
```

## Layout

We can use `<a-radio>` and `<a-grid>` in `<a-radio-group>`, to implement complex layout.

```vue
<template>
  <a-radio-group v-model="checkedValue">
    <a-grid :cols="3" :colGap="24" :rowGap="16">
      <a-grid-item>
        <a-radio value="1">Option 1</a-radio>
      </a-grid-item>
      <a-grid-item>
        <a-radio value="2" disabled>Option 2</a-radio>
      </a-grid-item>
      <a-grid-item>
        <a-radio value="3">Option 3</a-radio>
      </a-grid-item>
      <a-grid-item>
        <a-radio value="4">Option 4</a-radio>
      </a-grid-item>
      <a-grid-item>
        <a-radio value="5">Option 5</a-radio>
      </a-grid-item>
    </a-grid>
  </a-radio-group>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const checkedValue = ref('1');

    return {
      checkedValue,
    };
  },
};
</script>
```

## Custom radio Display

Use the #radio slot to customize the display of radios

```vue
<template>
  <a-radio-group default-value="1">
    <a-radio value="1">
      <template #radio="{ checked }">
        <a-tag :checked="checked" checkable>This is a tag radio 1</a-tag>
      </template>
    </a-radio>
    <a-radio value="2">
      <template #radio="{ checked }">
        <a-tag :checked="checked" checkable>This is a tag radio 2</a-tag>
      </template>
    </a-radio>
    <a-radio value="3">
      <template #radio="{ checked }">
        <a-tag :checked="checked" checkable>This is a tag radio 3</a-tag>
      </template>
    </a-radio>
  </a-radio-group>

  <div :style="{ marginTop: '20px' }">
    <a-radio-group>
      <template v-for="item in 2" :key="item">
        <a-radio :value="item">
          <template #radio="{ checked }">
            <a-space
              align="start"
              class="custom-radio-card"
              :class="{ 'custom-radio-card-checked': checked }"
            >
              <div class="custom-radio-card-mask">
                <div class="custom-radio-card-mask-dot" />
              </div>
              <div>
                <div class="custom-radio-card-title">
                  radio Card {{ item }}
                </div>
                <a-typography-text type="secondary">
                  this is a text
                </a-typography-text>
              </div>
            </a-space>
          </template>
        </a-radio>
      </template>
    </a-radio-group>
  </div>
</template>

<style scoped>
.custom-radio-card {
  padding: 10px 16px;
  border: 1px solid var(--color-border-2);
  border-radius: 4px;
  width: 250px;
  box-sizing: border-box;
}

.custom-radio-card-mask {
  height: 14px;
  width: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 100%;
  border: 1px solid var(--color-border-2);
  box-sizing: border-box;
}

.custom-radio-card-mask-dot {
  width: 8px;
  height: 8px;
  border-radius: 100%;
}

.custom-radio-card-title {
  color: var(--color-text-1);
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
}

.custom-radio-card:hover,
.custom-radio-card-checked,
.custom-radio-card:hover .custom-radio-card-mask,
.custom-radio-card-checked  .custom-radio-card-mask{
  border-color: rgb(var(--primary-6));
}

.custom-radio-card-checked {
  background-color: var(--color-primary-light-1);
}

.custom-radio-card:hover .custom-radio-card-title,
.custom-radio-card-checked .custom-radio-card-title {
  color: rgb(var(--primary-6));
}

.custom-radio-card-checked .custom-radio-card-mask-dot {
  background-color: rgb(var(--primary-6));
}
</style>
```

## API

### `<radio>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|model-value **(v-model)**|Value|`string \| number \| boolean`|`-`|
|default-checked|Whether checked by default (uncontrolled state)|`boolean`|`false`|
|value|The `value` of the option|`string \| number \| boolean`|`true`|
|type|Radio type|`'radio' \| 'button'`|`'radio'`|
|disabled|Whether to disable|`boolean`|`false`|
### `<radio>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Trigger when the value changes|value: ` string \| number \| boolean `<br>ev: `Event`|
### `<radio>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|radio|Custom radio|checked: `boolean`<br>disabled: `boolean`|2.18.0|

### `<radio-group>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model-value **(v-model)**|Value|`string \| number \| boolean`|`-`||
|default-value|Default value (uncontrolled state)|`string \| number \| boolean`|`''`||
|type|Types of radio group|`'radio' \| 'button'`|`'radio'`||
|size|The size of the radio group|`'mini' \| 'small' \| 'medium' \| 'large'`|`-`||
|options|Options|`Array<string \| number \| RadioOption>`|`-`|2.27.0|
|direction|The direction of the radio group|`'horizontal' \| 'vertical'`|`'horizontal'`||
|disabled|Whether to disable|`boolean`|`false`||
### `<radio-group>` Events

|Event Name|Description|Parameters|
|---|---|---|
|change|Trigger when the value changes|value: ` string \| number \| boolean `|
### `<radio-group>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|radio|Custom radio|checked: `boolean`<br>disabled: `boolean`|2.27.0|
|label|radio label content|data: `RadioOption`|2.27.0|

### RadioOption

|Name|Description|Type|Default|
|---|---|---|:---:|
|label|label content|`RenderContent`|`-`|
|value|The `value` of the option|`string \| number`|`-`|
|disabled|Whether to disable|`boolean`|`false`|
