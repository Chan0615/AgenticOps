---
name: arco-vue-menu
description: "Organize, arrange, and display a list of options. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Menu

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Horizontal

By setting `mode` to `horizontal`, you can use the horizontal menu.

```vue
<template>
  <div class="menu-demo">
    <a-menu mode="horizontal" :default-selected-keys="['1']">
      <a-menu-item key="0" :style="{ padding: 0, marginRight: '38px' }" disabled>
        <div
          :style="{
            width: '80px',
            height: '30px',
            borderRadius: '2px',
            background: 'var(--color-fill-3)',
            cursor: 'text',
          }"
        />
      </a-menu-item>
      <a-menu-item key="1">Home</a-menu-item>
      <a-menu-item key="2">Solution</a-menu-item>
      <a-menu-item key="3">Cloud Service</a-menu-item>
      <a-menu-item key="4">Cooperation</a-menu-item>
    </a-menu>
  </div>
</template>
<style scoped>
.menu-demo {
  box-sizing: border-box;
  width: 100%;
  padding: 40px;
  background-color: var(--color-neutral-2);
}
</style>
```

## Dark Theme

The theme is specified by `theme`, which can be divided into two types: `light` and `dark`.

```vue
<template>
  <div class="menu-demo">
    <a-menu mode="horizontal" theme="dark" :default-selected-keys="['1']">
      <a-menu-item key="0" :style="{ padding: 0, marginRight: '38px' }" disabled>
        <div
          :style="{
            width: '80px',
            height: '30px',
            background: 'var(--color-fill-3)',
            cursor: 'text',
          }"
        />
      </a-menu-item>
      <a-menu-item key="1">Home</a-menu-item>
      <a-menu-item key="2">Solution</a-menu-item>
      <a-menu-item key="3">Cloud Service</a-menu-item>
      <a-menu-item key="4">Cooperation</a-menu-item>
    </a-menu>
  </div>
</template>
<style scoped>
.menu-demo {
  box-sizing: border-box;
  width: 100%;
  padding: 40px;
  background-color: var(--color-neutral-2);
}
</style>
```

## Collapsed Menu

Use `collapsed` to specify the menu to collapse.

```vue
<template>
  <div class="menu-demo">
    <a-button
      :style="{ padding: '0 12px', height: '30px', lineHeight: '30px', marginBottom: '4px' }"
      type="primary"
      @click="toggleCollapse"
    >
      <icon-menu-unfold v-if="collapsed" />
      <icon-menu-fold v-else />
    </a-button>
    <a-menu
      :style="{ width: '200px', borderRadius: '4px' }"
      theme="dark"
      :collapsed="collapsed"
      :default-open-keys="['0']"
      :default-selected-keys="['0_2']"
    >
      <a-sub-menu key="0">
        <template #icon><icon-apps></icon-apps></template>
        <template #title>Navigation 1</template>
        <a-menu-item key="0_0">Menu 1</a-menu-item>
        <a-menu-item key="0_1">Menu 2</a-menu-item>
        <a-menu-item key="0_2">Menu 3</a-menu-item>
        <a-menu-item key="0_3">Menu 4</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="1">
        <template #icon><icon-bug></icon-bug></template>
        <template #title>Navigation 2</template>
        <a-menu-item key="1_0">Menu 1</a-menu-item>
        <a-menu-item key="1_1">Menu 2</a-menu-item>
        <a-menu-item key="1_2">Menu 3</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="2">
        <template #icon><icon-bulb></icon-bulb></template>
        <template #title>Navigation 3</template>
        <a-menu-item key="2_0">Menu 1</a-menu-item>
        <a-menu-item key="2_1">Menu 2</a-menu-item>
        <a-sub-menu key="2_2" title="Navigation 4">
          <a-menu-item key="2_2_0">Menu 1</a-menu-item>
          <a-menu-item key="2_2_1">Menu 2</a-menu-item>
        </a-sub-menu>
      </a-sub-menu>
    </a-menu>
  </div>
</template>
<script>
import { ref } from 'vue';
import {
  IconMenuFold,
  IconMenuUnfold,
  IconApps,
  IconBug,
  IconBulb,
} from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconMenuFold,
    IconMenuUnfold,
    IconApps,
    IconBug,
    IconBulb,
  },
  setup() {
    const collapsed = ref(false);
    return {
      collapsed,
      toggleCollapse: () => { collapsed.value = !collapsed.value; },
    }
  }
};
</script>
<style scoped>
.menu-demo {
  box-sizing: border-box;
  width: 100%;
  padding: 40px;
  background-color: var(--color-neutral-2);
}
</style>
```

## Responsive collapsed

set `breakpoint` for responsive contraction.

```vue
<template>
  <div class="menu-demo">
    <a-menu
      :style="{ width: '200px', height: '100%' }"
      :default-open-keys="['0']"
      :default-selected-keys="['0_2']"
      show-collapse-button
      breakpoint="xl"
      @collapse="onCollapse"
    >
      <a-sub-menu key="0">
        <template #icon><icon-apps></icon-apps></template>
        <template #title>Navigation 1</template>
        <a-menu-item key="0_0">Menu 1</a-menu-item>
        <a-menu-item key="0_1">Menu 2</a-menu-item>
        <a-menu-item key="0_2">Menu 3</a-menu-item>
        <a-menu-item key="0_3">Menu 4</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="1">
        <template #icon><icon-bug></icon-bug></template>
        <template #title>Navigation 2</template>
        <a-menu-item key="1_0">Menu 1</a-menu-item>
        <a-menu-item key="1_1">Menu 2</a-menu-item>
        <a-menu-item key="1_2">Menu 3</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="2">
        <template #icon><icon-bulb></icon-bulb></template>
        <template #title>Navigation 3</template>
        <a-menu-item key="2_0">Menu 1</a-menu-item>
        <a-menu-item key="2_1">Menu 2</a-menu-item>
        <a-sub-menu key="2_2" title="Navigation 4">
          <a-menu-item key="2_2_0">Menu 1</a-menu-item>
          <a-menu-item key="2_2_1">Menu 2</a-menu-item>
        </a-sub-menu>
      </a-sub-menu>
    </a-menu>
  </div>
</template>
<script>
import { ref } from 'vue';
import { Message } from '@arco-design/web-vue';
import {
  IconMenuFold,
  IconMenuUnfold,
  IconApps,
  IconBug,
  IconBulb,
} from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconMenuFold,
    IconMenuUnfold,
    IconApps,
    IconBug,
    IconBulb,
  },
  setup() {
    return {
      onCollapse(val, type) {
        const content = type === 'responsive' ? 'Responsive collapse triggered' : 'Click to collapse';
        Message.info({
          content,
          duration: 2000,
        });
      }
    };
  }
};
</script>
<style scoped>
.menu-demo {
  box-sizing: border-box;
  width: 100%;
  height: 600px;
  padding: 40px;
  background-color: var(--color-neutral-2);
}
</style>
```

## Sub Menu

Multiple sub-items can be embedded in the menu, and the items that are opened by default can be set through `openKeys`.

```vue
<template>
  <div class="menu-demo">
    <a-menu
      :style="{ width: '200px', height: '100%' }"
      :default-open-keys="['0']"
      :default-selected-keys="['0_1']"
      show-collapse-button
    >
    <a-menu-item key="0_0_0" data-obj="1">Menu 1</a-menu-item>
      <a-sub-menu key="0">
        <template #icon><icon-apps></icon-apps></template>
        <template #title>Navigation 1</template>
        <a-menu-item key="0_0">Menu 1</a-menu-item>
        <a-menu-item key="0_1">Menu 2</a-menu-item>
        <a-menu-item key="0_2" disabled>Menu 3</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="1">
        <template #icon><icon-bug></icon-bug></template>
        <template #title>Navigation 2</template>
        <a-menu-item key="1_0">Menu 1</a-menu-item>
        <a-menu-item key="1_1">Menu 2</a-menu-item>
        <a-menu-item key="1_2">Menu 3</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="2">
        <template #icon><icon-bulb></icon-bulb></template>
        <template #title>Navigation 3</template>
        <a-menu-item-group title="Menu Group 1">
          <a-menu-item key="2_0">Menu 1</a-menu-item>
          <a-menu-item key="2_1">Menu 2</a-menu-item>
        </a-menu-item-group>
        <a-menu-item-group title="Menu Group 2">
          <a-menu-item key="2_2">Menu 3</a-menu-item>
          <a-menu-item key="2_3">Menu 4</a-menu-item>
        </a-menu-item-group>
      </a-sub-menu>
    </a-menu>
  </div>
</template>
<script>
import {
  IconMenuFold,
  IconMenuUnfold,
  IconApps,
  IconBug,
  IconBulb,
} from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconMenuFold,
    IconMenuUnfold,
    IconApps,
    IconBug,
    IconBulb,
  },
};
</script>
<style scoped>
.menu-demo {
  box-sizing: border-box;
  width: 100%;
  height: 600px;
  padding: 40px;
  background-color: var(--color-neutral-2);
}
</style>
```

## Custom Size

Freely specify width of menu and height of menu item through `style`.

```vue
<template>
  <div class="menu-demo">
    <a-slider
      :style="{ width: '320px', marginBottom: '24px' }"
      v-model="width"
      :step="10"
      :min="160"
      :max="400"
    />
    <a-menu
      showCollapseButton
      :default-open-keys="['0']"
      :default-selected-keys="['0_1']"
      :style="{ width: `${width}px`, height: 'calc(100% - 28px)' }"
    >
      <a-sub-menu key="0">
        <template #icon><IconApps></IconApps></template>
        <template #title>Navigation 1</template>
        <a-menu-item key="0_0">Menu 1</a-menu-item>
        <a-menu-item key="0_1">Menu 2</a-menu-item>
        <a-menu-item key="0_2" disabled>
          Menu 3
        </a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="1">
        <template #icon><IconBug></IconBug></template>
        <template #title>Navigation 2</template>
        <a-menu-item key="1_0">Menu 1</a-menu-item>
        <a-menu-item key="1_1">Menu 2</a-menu-item>
        <a-menu-item key="1_2">Menu 3</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="2">
        <template #icon><IconBulb></IconBulb></template>
        <template #title>Navigation 3</template>
        <a-menu-item key="2_0">Menu 1</a-menu-item>
        <a-menu-item key="2_1">Menu 2</a-menu-item>
        <a-menu-item key="2_2">Menu 3</a-menu-item>
      </a-sub-menu>
    </a-menu>
  </div>
</template>
<script>
import {
  IconMenuFold,
  IconMenuUnfold,
  IconApps,
  IconBug,
  IconBulb,
} from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconMenuFold,
    IconMenuUnfold,
    IconApps,
    IconBug,
    IconBulb,
  },
  data() {
    return {
      width: 240
    }
  }
};
</script>
<style scoped>
.menu-demo {
  box-sizing: border-box;
  width: 100%;
  height: 600px;
  padding: 40px;
  background-color: var(--color-neutral-2);
}
</style>
```

## Floating Menu

Specify `mode` as `pop` to use floating menu.

```vue
<template>
  <div class="menu-demo">
    <a-menu mode="pop" showCollapseButton>
      <a-menu-item key="1">
        <template #icon><icon-apps></icon-apps></template>
        Navigation 1
      </a-menu-item>
      <a-sub-menu key="2">
        <template #icon><icon-bug></icon-bug></template>
        <template #title>Navigation 2</template>
        <a-menu-item key="2_0">Beijing</a-menu-item>
        <a-menu-item key="2_1">Shanghai</a-menu-item>
        <a-menu-item key="2_2">Guangzhou</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="3">
        <template #icon><icon-bulb></icon-bulb></template>
        <template #title>Navigation 3</template>
        <a-menu-item key="3_0">Wuhan</a-menu-item>
        <a-menu-item key="3_1">Chengdu</a-menu-item>
      </a-sub-menu>
      <a-menu-item key="4">
        <template #icon><icon-safe></icon-safe></template>
        Navigation 4
      </a-menu-item>
      <a-menu-item key="5">
        <template #icon><icon-fire></icon-fire></template>
        Navigation 5
      </a-menu-item>
    </a-menu>
  </div>
</template>
<script>
import {
  IconApps,
  IconBug,
  IconBulb,
} from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconApps,
    IconBug,
    IconBulb,
  },
};
</script>
<style scoped>
.menu-demo {
  width: 100%;
  height: 600px;
  padding: 40px;
  box-sizing: border-box;
  background-color: var(--color-neutral-2);
}

.menu-demo .arco-menu {
  width: 200px;
  height: 100%;
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.3);
}

.menu-demo .arco-menu :deep(.arco-menu-collapse-button) {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.menu-demo .arco-menu:not(.arco-menu-collapsed) :deep(.arco-menu-collapse-button) {
  right: 0;
  bottom: 8px;
  transform: translateX(50%);
}

.menu-demo .arco-menu:not(.arco-menu-collapsed)::before {
  content: '';
  position: absolute;
  right: 0;
  bottom: 0;
  width: 48px;
  height: 48px;
  background-color: inherit;
  border-radius: 50%;
  box-shadow: -4px 0 2px var(--color-bg-2), 0 0 1px rgba(0, 0, 0, 0.3);
  transform: translateX(50%);
}

.menu-demo .arco-menu.arco-menu-collapsed {
  width: 48px;
  height: auto;
  padding-top: 24px;
  padding-bottom: 138px;
  border-radius: 22px;
}

.menu-demo .arco-menu.arco-menu-collapsed :deep(.arco-menu-collapse-button) {
  right: 8px;
  bottom: 8px;
}
</style>
```

## Floating Button Menu

By setting `mode` to `popButton`, you can use a button group style floating menu.

```vue
<template>
  <div class="menu-demo">
    <a-trigger
      :trigger="['click', 'hover']"
      clickToClose
      position="top"
      v-model:popupVisible="popupVisible1"
    >
      <div :class="`button-trigger ${popupVisible1 ? 'button-trigger-active' : ''}`">
        <IconClose v-if="popupVisible1" />
        <IconMessage v-else />
      </div>
      <template #content>
        <a-menu
          :style="{ marginBottom: '-4px' }"
          mode="popButton"
          :tooltipProps="{ position: 'left' }"
          showCollapseButton
        >
          <a-menu-item key="1">
            <template #icon><IconBug></IconBug></template>
            Bugs
          </a-menu-item>
          <a-menu-item key="2">
            <template #icon><IconBulb></IconBulb></template>
            Ideas
          </a-menu-item>
        </a-menu>
      </template>
    </a-trigger>

    <a-trigger
      :trigger="['click', 'hover']"
      clickToClose
      position="top"
      v-model:popupVisible="popupVisible2"
    >
      <div :class="`button-trigger ${popupVisible2 ? 'button-trigger-active' : ''}`">
        <IconClose v-if="popupVisible2" />
        <IconMessage v-else />
      </div>
      <template #content>
        <a-menu
          :style="{ marginBottom: '-4px' }"
          mode="popButton"
          :tooltipProps="{ position: 'left' }"
          showCollapseButton
        >
          <a-menu-item key="1">
            <template #icon><IconBug></IconBug></template>
            Bugs
          </a-menu-item>
          <a-menu-item key="2">
            <template #icon><IconBulb></IconBulb></template>
            Ideas
          </a-menu-item>
        </a-menu>
      </template>
    </a-trigger>
  </div>
</template>
<script>
import {
  IconBug,
  IconBulb,
  IconClose,
  IconMessage,
} from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconBug,
    IconBulb,
    IconClose,
    IconMessage,
  },
  data() {
    return {
      popupVisible1: false,
      popupVisible2: false,
    };
  }
};
</script>
<style scoped>
.menu-demo {
  box-sizing: border-box;
  width: 660px;
  height: 300px;
  padding: 40px;
  background-color: var(--color-fill-2);
  position: relative;
}
.button-trigger {
  position: absolute;
  bottom: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  color: var(--color-white);
  font-size: 14px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.1s;
}
/* button left */
.button-trigger:nth-child(1) {
  left: 150px;
  background-color: var(--color-neutral-5);
}
.button-trigger:nth-child(1).button-trigger-active {
  background-color: var(--color-neutral-4);
}
/* button right */
.button-trigger:nth-child(2) {
  left: 372px;
  background-color: rgb(var(--arcoblue-6));
}
.button-trigger:nth-child(3).button-trigger-active {
  background-color: var(--color-primary-light-4);
}
</style>
```

## API

### `<menu>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|theme|Menu theme|`'light' \| 'dark'`|`'light'`||
|mode|The mode of menu|`'vertical' \| 'horizontal' \| 'pop' \| 'popButton'`|`'vertical'`||
|level-indent|Indentation between levels|`number`|`-`||
|auto-open|Expand all multi-level menus by default|`boolean`|`false`||
|collapsed **(v-model)**|Whether to collapse the menu|`boolean`|`-`||
|default-collapsed|Whether to collapse the menu by default|`boolean`|`false`||
|collapsed-width|Collapse menu width|`number`|`-`||
|accordion|Turn on the accordion effect|`boolean`|`false`||
|auto-scroll-into-view|Whether to automatically scroll the selected item to the visible area|`boolean`|`false`||
|show-collapse-button|Whether built-in folding button|`boolean`|`false`||
|selected-keys **(v-model)**|The selected menu item key array|`string[]`|`-`||
|default-selected-keys|The key array of the menu items selected by default|`string[]`|`[]`||
|open-keys **(v-model)**|Expanded submenu key array|`string[]`|`-`||
|default-open-keys|The default expanded submenu key array|`string[]`|`[]`||
|scroll-config|Scroll to the configuration items in the visible area and receive all the parameters of [scroll-into-view-if-needed](https://github.com/stipsan/scroll-into-view-if-needed)|`{ [key: string]: any }`|`-`||
|trigger-props|Accept all `Props` of `Trigger` in pop-up mode|`TriggerProps`|`-`||
|tooltip-props|Accept all `Props` of `ToolTip` in pop-up mode|`object`|`-`||
|auto-open-selected|Expand the selected menus by default|`boolean`|`false`|2.8.0|
|breakpoint|Responsive breakpoints, see [Responsive Grid](../layout/grid.md) for details|`'xxl' \| 'xl' \| 'lg' \| 'md' \| 'sm' \| 'xs'`|`-`|2.18.0|
|popup-max-height|The maximum height of popover|`boolean \| number`|`true`|2.23.0|
### `<menu>` Events

|Event Name|Description|Parameters|
|---|---|---|
|collapse|Triggered when the collapsed state changes|collapsed: `boolean`<br>type: `'clickTrigger'\|'responsive'`|
|menu-item-click|Triggered when the menu item is clicked|key: `string`|
|sub-menu-click|Triggered when the submenu is clicked|key: `string`<br>openKeys: `string[]`|
### `<menu>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|collapse-icon|Collapse icon|collapsed: `boolean`|
|expand-icon-right|Icon expand right|-|
|expand-icon-down|Icon expand down|-|

### `<sub-menu>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|title|The title of the submenu|`string`|`-`||
|selectable|In the pop-up mode, whether the multi-level menu header is also used as a menu item to support the state such as click to select|`boolean`|`false`||
|popup|Whether to force the use of pop-up mode, `level` indicates the level of the current submenu|`boolean \| ((level: number) => boolean)`|`false`||
|popup-max-height|The maximum height of popover|`boolean \| number`|`true`|2.23.0|
### `<sub-menu>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|title|Title|-||
|expand-icon-right|Icon expand right|-||
|expand-icon-down|Icon expand down|-||
|icon|the icon of menu item|-|2.11.0|

### `<menu-item-group>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|title|The title of the menu group|`string`|`-`|
### `<menu-item-group>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|title|Title|-|

### `<menu-item>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|disabled|Whether to disable|`boolean`|`false`|
### `<menu-item>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|icon|the icon of menu item|-|2.11.0|

## FAQ

### The `key` attribute of `<MenuItem>` and `<SubMenu>` components is required
When using `<MenuItem>` and `<SubMenu>` components in the `<Menu>` component, please pass in the unique `key` attribute.
The component will rely on this value when calculating internally. If no value is assigned, some Abnormality in the scene
