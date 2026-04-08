---
name: arco-vue-config-provider
description: "Arco Design Vue ConfigProvider reference. Use for global size, locale, popup container, and application-wide component configuration."
user-invocable: false
---

# ConfigProvider

## Basic Usage

Set the basic usage of internationalized languages.

```vue
<template>
  <a-config-provider :locale="locale">
    <a-radio-group
      type="button"
      v-model="localeType"
      :options="localeOptions"
    ></a-radio-group>
    <div>
      <a-pagination
        :total="50"
        show-total
        show-jumper
        show-page-size
        style="margin-top: 20px; margin-bottom: 20px;"
      />
    </div>
    <a-space :size="20" style="margin-bottom: 20px;">
      <a-range-picker style="width: 300px;" />
      <a-time-picker type="time-range" style="width: 300px;" />
      <a-popconfirm content="Are you sure you want to delete?">
        <a-button type="primary">Popconfirm</a-button>
      </a-popconfirm>
    </a-space>
  </a-config-provider>
</template>

<script>
import { ref, computed } from 'vue';
import zhCN from '@arco-design/web-vue/es/locale/lang/zh-cn';
import enUS from '@arco-design/web-vue/es/locale/lang/en-us';
import esES from '@arco-design/web-vue/es/locale/lang/es-es';
import jaJP from '@arco-design/web-vue/es/locale/lang/ja-jp';
import idID from '@arco-design/web-vue/es/locale/lang/id-id';
import frFR from '@arco-design/web-vue/es/locale/lang/fr-fr';
import ptPT from '@arco-design/web-vue/es/locale/lang/pt-pt';
import deDE from '@arco-design/web-vue/es/locale/lang/de-de';
import koKR from '@arco-design/web-vue/es/locale/lang/ko-kr';
import itIT from '@arco-design/web-vue/es/locale/lang/it-it';
import thTH from '@arco-design/web-vue/es/locale/lang/th-th';
import viVN from '@arco-design/web-vue/es/locale/lang/vi-vn';
import nlNL from '@arco-design/web-vue/es/locale/lang/nl-nl';

const locales = {
  'zh-CN': zhCN,
  'en-US': enUS,
  'es-ES': esES,
  'ja-JP': jaJP,
  'id-ID': idID,
  'fr-FR': frFR,
  'pt-PT': ptPT,
  'de-DE': deDE,
  'ko-KR': koKR,
  'it-IT': itIT,
  'th-TH': thTH,
  'vi-VN': viVN,
  'nl-NL': nlNL,
};

export default {
  setup() {
    const localeType = ref('es-ES');
    const locale = computed(() => {
      return locales[localeType.value] || zhCN;
    });

    return {
      localeType,
      locale,
      localeOptions: Object.keys(locales),
    };
  },
};
</script>
```

## Custom Empty Element

Empty state elements can be customized globally via the `empty` slot.

```vue
<template>
  <a-config-provider>
    <template #empty="scope">
      <a-empty v-if="scope?.component==='cascader'" description="cascader no data!" in-config-provider>
      </a-empty>
      <a-empty v-else-if="scope?.component==='select'" description="select no data!" in-config-provider></a-empty>
      <a-empty v-else-if="scope?.component==='tree-select'" description="tree-select no data!" in-config-provider></a-empty>
      <a-empty v-else-if="scope?.component==='list'" description="list no data!" in-config-provider></a-empty>
      <a-empty v-else-if="scope?.component==='table'" description="table no data!" in-config-provider></a-empty>
      <div v-else class="my-empty">
        <icon-trophy />
      </div>
    </template>
    <a-space direction="vertical" fill>
      <a-cascader :options="[]" placeholder="cascader" allow-search />
      <a-select placeholder="select" allow-search />
      <a-tree-select placeholder="tree-select"/>
      <a-list>
        <template #header>
          Empty List
        </template>
      </a-list>
      <a-table :columns="columns" :data="[]" />
      <a-empty></a-empty>
    </a-space>
  </a-config-provider>
</template>

<script>
import { IconTrophy } from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconTrophy
  },
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
    return {
      columns
    }
  }
}
</script>

<style>
.my-empty {
  padding: 20px;
  width: 100%;
  text-align: center;
  box-sizing: border-box;
}
</style>
```

## RTL

Set the component to a view that reads from right to left.

```vue
<template>
  <div>
    <a-switch v-model="rtlType" style="margin-bottom: 20px;">
      <template #checked>
        RTL
      </template>
      <template #unchecked>
        LTR
      </template>
    </a-switch>
    <a-config-provider :rtl="rtlType">
      <a-tabs :default-active-key="2" style="margin-bottom: 20px;">
        <a-tab-pane
          v-for="i in 36"
          :key="i"
          :title="`Tab ${i}`"
        >
          Content of Tab Panel {{ i }}
        </a-tab-pane>
      </a-tabs>
      <a-space :direction="'vertical'" style="width: 100%;">
        <a-space :size="40">
          <a-badge :count="9">
            <a-avatar shape="square" />
          </a-badge>
          <a-badge :count="9" dot :dotStyle="{ width: '10px', height: '10px' }">
            <a-avatar shape="square" />
          </a-badge>
          <a-badge :dotStyle="{ height: '16px', width: '16px', fontSize: '14px' }">
            <template #content>
              <IconClockCircle
                :style="{ verticalAlign: 'middle', color: 'var(--color-text-2)' }"
              />
            </template>
            <a-avatar shape="square" />
          </a-badge>
          <a-tag :color="'red'" closable>red</a-tag>
          <a-tag :color="'blue'" closable>blue</a-tag>
          <a-tag :color="'green'" closable>green</a-tag>
        </a-space>
      </a-space>
    </a-config-provider>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const rtlType = ref(true);

    return {
      rtlType,
    };
  },
};
</script>
```

## API

### `<config-provider>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|prefix-cls|Component classname prefix|`string`|`'arco'`||
|locale|Configure language pack|`ArcoLang`|`-`||
|size|Size|`Size`|`-`|2.14.0|
|global|Is global effect|`boolean`|`false`|2.25.0|
|scroll-to-close|Whether to close the popover when scrolling|`boolean`|`false`|2.46.0|
|exchange-time|Whether to exchange time|`boolean`|`true`|2.48.0|
|rtl|View starts from the right and ends on the left|`boolean`|`false`||
### `<config-provider>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|loading|Custom loading element|-|2.28.0|
|empty|Custom empty element|component: `string`|2.28.0|

## FAQ

### Global Config

When the `global` property is set to `true`, the configuration content will be injected into the Vue AppContext, which is generally used to solve the problem that the configuration content cannot take effect when the functional call method of the Modal and Message components is used.

### Customize empty state display

You can customize the display of the global empty state of the component library in `#empty`. If the `Empty` component is used in the slot, you need to enable the `inConfigProvider` property.
