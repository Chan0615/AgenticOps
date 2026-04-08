---
name: arco-vue-trigger
description: "Used to add hover, click, focus and other events to the element, and pop up a dropdown. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Trigger

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

---

```vue
<template>
  <a-space>
    <a-trigger position="top" auto-fit-position :unmount-on-close="false">
      <span>Hover Me</span>
      <template #content>
        <div class="demo-basic">
          <a-empty />
        </div>
      </template>
    </a-trigger>
    <a-trigger trigger="click" :unmount-on-close="false">
      <a-button>Click Me</a-button>
      <template #content>
        <div class="demo-basic">
          <a-empty />
        </div>
      </template>
    </a-trigger>
    <a-trigger trigger="focus">
      <a-input placeholder="Focus on me" />
      <template #content>
        <div class="demo-basic">
          <a-empty />
        </div>
      </template>
    </a-trigger>
  </a-space>
</template>

<style scoped>
.demo-basic {
  padding: 10px;
  width: 200px;
  background-color: var(--color-bg-popup);
  border-radius: 4px;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.15);
}
</style>
```

## Nest

---

```vue
<template>
  <a-trigger trigger="click">
    <a-button>Click Me</a-button>
    <template #content>
      <div class="trigger-demo-nest">
        <a-empty />
        <a-trigger position="right">
          <a-button>Hover Me</a-button>
          <template #content>
            <div class="trigger-demo-nest">
              <a-empty />
              <a-trigger trigger="click" position="right">
                <a-button>Click Me</a-button>
                <template #content>
                  <div class="trigger-demo-nest">
                    <a-empty />
                    <a-trigger position="right">
                      <a-button>Hover Me</a-button>
                      <template #content>
                        <a-empty class="trigger-demo-nest" />
                      </template>
                    </a-trigger>
                  </div>
                </template>
              </a-trigger>
            </div>
          </template>
        </a-trigger>
      </div>
    </template>
  </a-trigger>
</template>

<style scoped>
.trigger-demo-nest {
  padding: 10px;
  width: 200px;
  background-color: var(--color-bg-popup);
  border-radius: 4px;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.15);
}

.trigger-demo-nest-popup-content {
  text-align: right;
}
</style>
```

## Triggers

---

```vue
<template>
  <a-trigger :trigger="['click','hover','focus']">
    <a-input placeholder="Click/Hover/Focus on me" />
    <template #content>
      <div class="demo-trigger">
        <a-empty />
      </div>
    </template>
  </a-trigger>
</template>

<style scoped>
.demo-trigger {
  padding: 10px;
  width: 200px;
  background-color: var(--color-bg-popup);
  border-radius: 4px;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.15);
}
</style>
```

## Follow mouse

---

```vue
<template>
  <a-trigger trigger="click" align-point>
    <div class="demo-point-trigger">
      <div>Click Me</div>
    </div>
    <template #content>
      <div class="demo-point">
        <a-empty />
      </div>
    </template>
  </a-trigger>
</template>

<style scoped>
.demo-point-trigger {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  background-color: var(--color-fill-2)
}

.demo-point {
  padding: 10px;
  width: 200px;
  background-color: var(--color-bg-popup);
  border-radius: 4px;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.15);
}

.demo-point-wrapper {
  display: block;
}
</style>
```

## Scroll Container

Monitor the scrolling of the container by setting `update-at-scroll`.

```vue
<template>
  <div :style="{height:'100px',overflowY:'scroll'}">
    <div :style="{height:'200px'}">
      <a-trigger trigger="click" update-at-scroll>
        <a-button :style="{marginTop:'80px'}">Click Me</a-button>
        <template #content>
          <div class="demo-basic">
            <a-empty />
          </div>
        </template>
      </a-trigger>
    </div>
  </div>
</template>

<style scoped>
.demo-basic {
  padding: 10px;
  width: 200px;
  background-color: var(--color-bg-popup);
  border-radius: 4px;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.15);
}
</style>
```

## Show Arrow

---

```vue
<template>
  <a-space>
    <a-trigger trigger="click">
      <a-button>Click Me</a-button>
      <template #content>
        <div class="demo-arrow">
          <a-empty />
        </div>
      </template>
    </a-trigger>
    <a-trigger trigger="click" show-arrow>
      <a-button>Click Me (Arrow)</a-button>
      <template #content>
        <div class="demo-arrow">
          <a-empty />
        </div>
      </template>
    </a-trigger>
  </a-space>
</template>

<style scoped>
.demo-arrow {
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.15);
  padding: 10px;
  width: 200px;
  background-color: var(--color-bg-popup);
  border-radius: 4px;
}
</style>
```

## Popup Translate

---

```vue
<template>
  <a-space>
    <a-trigger>
      <a-button>BOTTOM</a-button>
      <template #content>
        <div class="trigger-demo-translate">
          <a-empty />
        </div>
      </template>
    </a-trigger>
    <a-trigger :popup-translate="[100, 20]">
      <a-button>BOTTOM OFFSET[100, 20]</a-button>
      <template #content>
        <div class="trigger-demo-translate">
          <a-empty />
        </div>
      </template>
    </a-trigger>
    <a-trigger :popup-translate="[-100, 20]">
      <a-button>BOTTOM OFFSET[-100, 20]</a-button>
      <template #content>
        <div class="trigger-demo-translate">
          <a-empty />
        </div>
      </template>
    </a-trigger>
  </a-space>
</template>

<style scoped>
.trigger-demo-translate {
  padding: 10px;
  width: 200px;
  background-color: var(--color-bg-popup);
  border-radius: 4px;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.15);
}
</style>
```

## API

### `<trigger>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|popup-visible **(v-model)**|Whether the popup is visible|`boolean`|`-`||
|default-popup-visible|Whether the popup is visible by default (uncontrolled mode)|`boolean`|`false`||
|trigger|Trigger method|`'hover' \| 'click' \| 'focus' \| 'contextMenu'`|`'hover'`||
|position|Popup position|`'top' \| 'tl' \| 'tr' \| 'bottom' \| 'bl' \| 'br' \| 'left' \| 'lt' \| 'lb' \| 'right' \| 'rt' \| 'rb'`|`'bottom'`||
|disabled|Whether the trigger is disabled|`boolean`|`false`||
|popup-offset|The offset of the popup (the offset distance of the popup from the trigger)|`number`|`0`||
|popup-translate|The moving distance of the popup|`TriggerPopupTranslate`|`-`||
|show-arrow|Whether the popup shows an arrow|`boolean`|`false`||
|align-point|Whether the popup follows the mouse|`boolean`|`false`||
|popup-hover-stay|Whether to keep the popup displayed when the trigger is moved out and moved into the popup|`boolean`|`true`||
|blur-to-close|Whether to close the popup when the trigger loses focus|`boolean`|`true`||
|click-to-close|Whether to close the popup when the trigger is clicked|`boolean`|`true`||
|click-outside-to-close|Whether to close the popup when clicking on the outer area|`boolean`|`true`||
|unmount-on-close|Whether to uninstall the popup node when closing|`boolean`|`true`||
|content-class|The class name of the popup content|`string\|array\|object`|`-`||
|content-style|The style of the popup content|`CSSProperties`|`-`||
|arrow-class|The class name of the popup arrow|`string\|array\|object`|`-`||
|arrow-style|The style of the popup arrow|`CSSProperties`|`-`||
|popup-style|The style of the popup|`CSSProperties`|`-`||
|animation-name|The name of the popup animation|`string`|`'fade-in'`||
|duration|The duration of the popup animation|`number\| {    enter: number;    leave: number;  }`|`-`||
|mouse-enter-delay|Delay trigger time of mouseenter event (ms)|`number`|`100`||
|mouse-leave-delay|Delay trigger time of mouseleave event (ms)|`number`|`100`||
|focus-delay|Delay trigger time of focus event (ms)|`number`|`0`||
|auto-fit-popup-width|Whether to set the width of the popup to the width of the trigger|`boolean`|`false`||
|auto-fit-popup-min-width|Whether to set the minimum width of the popup to the trigger width|`boolean`|`false`||
|auto-fix-position|When the size of the trigger changes, whether to recalculate the position of the popup|`boolean`|`true`||
|popup-container|Mount container for popup|`string \| HTMLElement`|`-`||
|auto-fit-position|Whether to automatically adjust the position of the popup to fit the window size|`boolean`|`true`||
|render-to-body|Whether to mount under the `body` element|`boolean`|`true`||
|prevent-focus|Whether to prevent elements in the pop-up layer from gaining focus when clicked|`boolean`|`false`||
|scroll-to-close|Whether to close the popover when scrolling|`boolean`|`false`|2.46.0|
|scroll-to-close-distance|Scroll threshold, trigger close when the scroll distance exceeds this value|`number`|`0`||
### `<trigger>` Events

|Event Name|Description|Parameters|version|
|---|---|---|:---|
|popup-visible-change|Emitted when the status of the popup changes|visible: `boolean`||
|show|Triggered after the trigger is shown (the animation ends)|-|2.18.0|
|hide|Triggered after the popup is hidden (the animation ends)|-|2.18.0|
### `<trigger>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|content|Popup content|-|

## Type

```ts
type TriggerPopupTranslate =
  | [number, number]
  | { [key in TriggerPosition]?: [number, number] };
```

## FAQ

### About the mount location of the pop-up box

The popup box is mounted on the `body` element by default. If you want to modify the mounted element, you can use the `popup-container` attribute to specify it. At the same time, you need to pay attention to ensure that the location of the mounted element can be accurately located. Generally, you can Add `position: relative` style for mount elements.

In the micro-frontend project, it is necessary to ensure that the mounting position of the sub-application is accurate, you can add `position: relative` to the `body` style of the sub-application

### scroll trigger container

By default, the component only listens to the scrolling event of `window`, and does not listen to the scrolling of the internal `div`, and the function similar to `scroll-to-close` will only take effect on the scrolling of `window`. You can support scroll event listening on the parent `div` element by enabling the `update-at-scroll` attribute.
