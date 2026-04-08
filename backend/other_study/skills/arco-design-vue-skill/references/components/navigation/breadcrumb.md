---
name: arco-vue-breadcrumb
description: "Breadcrumb is an auxiliary navigation mode used to identify the position of the page within the hierarchy and return upwards as needed. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Breadcrumb

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of breadcrumb.

```vue
<template>
  <a-breadcrumb>
    <a-breadcrumb-item>Home</a-breadcrumb-item>
    <a-breadcrumb-item>Channel</a-breadcrumb-item>
    <a-breadcrumb-item>News</a-breadcrumb-item>
  </a-breadcrumb>
</template>
```

## Custom separator

Customize the delimiter through the `separator` attribute or slot. Bread crumb child items can also be customized through the `separator` attribute or slot delimiter, and the priority is higher than the parent item.

```vue
<template>
  <a-space direction="vertical">
    <a-breadcrumb>
      <template #separator>
        <icon-right />
      </template>
      <a-breadcrumb-item>Home</a-breadcrumb-item>
      <a-breadcrumb-item>Channel</a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
    </a-breadcrumb>
    <a-breadcrumb separator="~">
      <a-breadcrumb-item>Home</a-breadcrumb-item>
      <a-breadcrumb-item>Channel</a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
    </a-breadcrumb>
    <a-breadcrumb>
      <template #separator>
        <icon-right />
      </template>
      <a-breadcrumb-item separator="->">Home</a-breadcrumb-item>
      <a-breadcrumb-item>Channel</a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
    </a-breadcrumb>
  </a-space>
</template>
```

## Custom Size

Customize the breadcrumb size by specifying the style.

```vue
<template>
  <a-space direction="vertical">
    <a-breadcrumb>
      <a-breadcrumb-item>Home</a-breadcrumb-item>
      <a-breadcrumb-item>Channel</a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
    </a-breadcrumb>
    <a-breadcrumb :style="{fontSize: `12px`}">
      <a-breadcrumb-item>Home</a-breadcrumb-item>
      <a-breadcrumb-item>Channel</a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
    </a-breadcrumb>
  </a-space>
</template>
```

## Custom Icon

You can use custom icons in the content.

```vue
<template>
  <a-space direction="vertical">
    <a-breadcrumb>
      <a-breadcrumb-item>
        <icon-home/>
      </a-breadcrumb-item>
      <a-breadcrumb-item>Channel</a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
    </a-breadcrumb>
     <a-breadcrumb>
      <a-breadcrumb-item>
        <icon-home/>
      </a-breadcrumb-item>
      <a-breadcrumb-item>
        <icon-at />
        Channel
      </a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
    </a-breadcrumb>
  </a-space>
</template>
```

## Parameterized configuration

Transfer breadcrumb data through `routes`. If you want to customize bread crumbs, it is recommended to use the `< a-breadcrumb-item />` component. the path is bound with the `href` attribute of the `a` tag by default, you can customize the rendering through the `item` slot.

```vue
<template>
  <a-space direction="vertical">
    <a-breadcrumb :routes="routes"/>
    <a-breadcrumb :routes="routes">
      <template #item-render="{route, paths}">
        <a-link :href="paths.join('/')">
          {{route.label}}
        </a-link>
      </template>
    </a-breadcrumb>
  </a-space>
</template>

<script>
export default {
  data() {
    return {
      routes: [
        {
          path: '/',
          label: 'Home'
        },
        {
          path: '/channel',
          label: 'Channel',
        },
        {
          path: '/news',
          label: 'News'
        },
      ],
    }
  }
}
</script>
```

## Dropdown menu

use `droplist` or `routes` settings dropdown menu

```vue
<template>
  <a-space direction="vertical">
    <a-breadcrumb :routes="routes"/>
    <a-breadcrumb>
      <a-breadcrumb-item>Home</a-breadcrumb-item>
      <a-breadcrumb-item :droplist="droplist">
        Channel
      </a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
    </a-breadcrumb>
    <a-breadcrumb>
      <a-breadcrumb-item>Home</a-breadcrumb-item>
      <a-breadcrumb-item>
        <template #droplist>
          <a-doption>Option 1</a-doption>
          <a-dsubmenu value="option-1">
            <template #default>Option 2</template>
            <template #content>
              <a-doption>Option 2-1</a-doption>
              <a-doption>Option 2-2</a-doption>
              <a-doption>Option 2-3</a-doption>
            </template>
            <template #footer>
              <div style="padding: 6px; text-align: center;">
                <a-button>Click</a-button>
              </div>
            </template>
          </a-dsubmenu>
          <a-doption>Option 3</a-doption>
        </template>
        Channel
      </a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
    </a-breadcrumb>
  </a-space>
</template>

<script>
export default {
  data() {
    return {
      routes: [
        {
          path: '/',
          label: 'Home'
        },
        {
          path: '/channel',
          label: 'Channel',
          children: [
            {
              path: '/users',
              label: 'Users',
            },
            {
              path: '/permission',
              label: 'Permission',
            }
          ]
        },
        {
          path: '/news',
          label: 'News'
        },
      ],
      droplist: [
        {
          path: '/goods',
          label: 'Goods',
        },
        {
          path: '/wallet',
          label: 'Wallet',
        }
      ]
    }
  }
}
</script>
```

## Show ellipsis

Use `max-count` to specify the maximum number of breadcrumbs to render, and the excess will be displayed as an ellipsis.

```vue
<template>
  <a-space direction="vertical">
    <a-breadcrumb :max-count="3">
      <a-breadcrumb-item>Home</a-breadcrumb-item>
      <a-breadcrumb-item>Sub Home</a-breadcrumb-item>
      <a-breadcrumb-item>All Channel</a-breadcrumb-item>
      <a-breadcrumb-item>Channel</a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
      <a-breadcrumb-item>Post</a-breadcrumb-item>
    </a-breadcrumb>
    <a-breadcrumb :max-count="3">
      <template #more-icon>
        <a-tooltip content="more routes a/b/c">
          <icon-more />
        </a-tooltip>
      </template>
      <a-breadcrumb-item>Home</a-breadcrumb-item>
      <a-breadcrumb-item>Sub Home</a-breadcrumb-item>
      <a-breadcrumb-item>All Channel</a-breadcrumb-item>
      <a-breadcrumb-item>Channel</a-breadcrumb-item>
      <a-breadcrumb-item>News</a-breadcrumb-item>
      <a-breadcrumb-item>Post</a-breadcrumb-item>
    </a-breadcrumb>
  </a-space>
</template>
```

## API

### `<breadcrumb>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|max-count|Maximum number of breadcrumbs displayed (0 means no limit)|`number`|`0`||
|routes|Set routes|`BreadcrumbRoute[]`|`-`|2.36.0|
|separator|Delimiter text|`string\|number`|`-`|2.36.0|
|custom-url|Custom link address|`(paths: string[]) => string`|`-`|2.36.0|
### `<breadcrumb>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|more-icon|Custom more icon|-|2.36.0|
|item-render|Effective when setting routes, custom render breadcrumbs|route: `BreadcrumbRoute`<br>routes: `BreadcrumbRoute[]`<br>paths: `string[]`|2.36.0|
|separator|Custom separator|-||

### `<breadcrumb-item>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|separator|Delimiter text|`string\|number`|`-`|2.36.0|
|droplist|Dropdown content|`BreadcrumbRoute['children']`|`-`|2.36.0|
|dropdown-props|Dropdown props|`DropDownProps`|`-`|2.36.0|
### `<breadcrumb-item>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|droplist|Custom droplist|-|2.36.0|
|separator|Custom separator|-|2.36.0|

### BreadcrumbRoute

|Name|Description|Type|Default|
|---|---|---|:---:|
|label|Breadcrumb name|`string`|`-`|
|path|Jump path (`a` tag `href` value)|`string`|`-`|
|children|Dropdown menu items|`{    label: string;    path: string;  }[]`|`-`|

## Tips

The custom slot with the same name takes precedence over the attribute.
