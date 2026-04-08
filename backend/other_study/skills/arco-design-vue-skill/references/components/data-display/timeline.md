---
name: arco-vue-timeline
description: "Display information content in chronological or reverse order. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Timeline

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage

```vue
<template>
  <div :style="{ marginBottom: '40px' }">
    <a-typography-text :style="{ verticalAlign: 'middle', marginRight: '8px' }">
      Reverse
    </a-typography-text>
    <a-radio-group
      @change="onChange"
      style="{ marginBottom: '30px' }"
      :modelValue="isReverse"
    >
      <a-radio :value="false">No Reverse</a-radio>
      <a-radio :value="true">Reverse</a-radio>
    </a-radio-group>
  </div>
  <a-timeline :reverse="isReverse">
    <a-timeline-item label="2017-03-10">The first milestone</a-timeline-item>
    <a-timeline-item label="2018-05-12">The second milestone</a-timeline-item>
    <a-timeline-item label="2020-09-30">The third milestone</a-timeline-item>
  </a-timeline>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const isReverse = ref(false);

    const onChange = (bool) => {
      isReverse.value = bool;
    };

    return {
      isReverse,
      onChange
    }
  },
};
</script>
```

## Icon

Custom node content

```vue
<template>
  <a-timeline>
    <a-timeline-item label="2017-03-10" dotColor="#00B42A">
      The first milestone
    </a-timeline-item>
    <a-timeline-item label="2018-05-22">The second milestone</a-timeline-item>
    <a-timeline-item label="2020-06-22" dotColor="#F53F3F">
      The third milestone
      <IconExclamationCircleFill
        :style="{ color: 'F53F3F', fontSize: '12px', marginLeft: '4px' }"
      />
    </a-timeline-item>
    <a-timeline-item label="2020-09-30" dotColor="#C9CDD4">
      The fourth milestone
    </a-timeline-item>
  </a-timeline>
</template>

<script>
import { IconExclamationCircleFill } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconExclamationCircleFill },
};
</script>
```

## Dot

The color and type of the node can be set through the attributes `dotColor`, `dotType`. At the same time, you can directly pass in DOM node to customize node styles through `slot#dot`. Priority is higher than `dotColor` and `dotType`

```vue
<template>
  <div :style="{ display: 'flex' }">
    <a-timeline :style="{ marginRight: '40px' }">
      <a-timeline-item label="2020-04-12" dotColor="#00B42A">
        The first milestone
      </a-timeline-item>
      <a-timeline-item label="2020-05-17">
        The second milestone
      </a-timeline-item>
      <a-timeline-item label="2020-06-22">
        <template #dot>
          <IconClockCircle :style="{ fontSize: '12px', color: '#F53F3F' }" />
        </template>
        The third milestone
      </a-timeline-item>
      <a-timeline-item label="2020-06-22" dotColor="var(--color-fill-4)">
        The third milestone
      </a-timeline-item>
    </a-timeline>

    <a-timeline :style="{ marginRight: '40px' }">
      <a-timeline-item label="2020-04-12">
        <template #dot>
          <IconCheck
            :style="{
              fontSize: '12px',
              padding: '2px',
              boxSizing: 'border-box',
              borderRadius: '50%',
              backgroundColor: 'var(--color-primary-light-1)',
            }"
          />
        </template>
        The first milestone
      </a-timeline-item>
      <a-timeline-item label="2020-05-17">
        <template #dot>
          <IconCheck
            :style="{
              fontSize: '12px',
              padding: '2px',
              boxSizing: 'border-box',
              borderRadius: '50%',
              backgroundColor: 'var(--color-primary-light-1)',
            }"
          />
        </template>
      </a-timeline-item>
      <a-timeline-item label="2020-06-22">The third milestone</a-timeline-item>
      <a-timeline-item label="2020-06-22" dotColor="var(--color-fill-4)">
        The third milestone
      </a-timeline-item>
    </a-timeline>

    <a-timeline>
      <a-timeline-item label="2020-04-12">The first milestone</a-timeline-item>
      <a-timeline-item label="2020-05-17" dotColor="var(--color-fill-4)">
        The second milestone
      </a-timeline-item>
      <a-timeline-item label="2020-06-22" dotColor="var(--color-fill-4)">
        The third milestone
      </a-timeline-item>
    </a-timeline>
  </div>
</template>

<script>
import { IconCheck } from '@arco-design/web-vue/es/icon';

export default {
  components: { IconCheck },
};
</script>
```

## Type

Example of custom axis.

```vue
<template>
  <a-timeline>
    <a-timeline-item label="2017-03-10" lineType="dashed">
      The first milestone
      <br />
      <a-typography-text
        type="secondary"
        :style="{ fontSize: '12px', marginTop: '4px' }"
      >
        This is a descriptive message
      </a-typography-text>
    </a-timeline-item>
    <a-timeline-item label="2018-05-12" lineType="dashed">
      The second milestone
      <br />
      <a-typography-text
        type="secondary"
        :style="{ fontSize: '12px', marginTop: '4px' }"
      >
        This is a descriptive message
      </a-typography-text>
    </a-timeline-item>
    <a-timeline-item label="2020-09-30" lineType="dashed">
      The third milestone
      <br />
      <a-typography-text
        type="secondary"
        :style="{ fontSize: '12px', marginTop: '4px' }"
      >
        This is a descriptive message
      </a-typography-text>
    </a-timeline-item>
  </a-timeline>
</template>
```

## Pending

When the task state is happening and the recording is still in progress, ghost nodes can be used to represent the current time node, and its pivot point can be customized through `slot#pending-dot`.

```vue

<template>
  <a-row align="center" :style="{ marginBottom: '24px' }">
    <a-checkbox
      :checked="!!pendingProps.direction"
      @change="(v) => onChange({ direction: v ? 'horizontal' : '' })"
    >
      horizontal &nbsp; &nbsp;
    </a-checkbox>
    <a-checkbox
      :checked="!!pendingProps.reverse"
      @change="(v) => onChange({ reverse: v })"
    >
      reverse &nbsp; &nbsp;
    </a-checkbox>
    <a-checkbox
      :checked="!!pendingProps.pending"
      @change="
        (v) => onChange({ pending: v ? 'This is a pending dot' : false })
      "
    >
      pending &nbsp; &nbsp;
    </a-checkbox>

    <a-checkbox
      :checked="!!pendingProps.hasPendingDot"
      @change="(v) => onChange({ hasPendingDot: v })"
    >
      custom pendingDot
    </a-checkbox>
  </a-row>
  <a-timeline v-bind="pendingProps">
    <template v-if="pendingProps.hasPendingDot" #dot>
      <IconFire :style="{ color: '#e70a0a' }" />
    </template>
    <a-timeline-item label="2017-03-10" dotColor="#52C419">
      The first milestone
    </a-timeline-item>
    <a-timeline-item label="2018-05-12" dotColor="#F5222D">
      The second milestone
    </a-timeline-item>
    <a-timeline-item label="2020-09-30">The third milestone</a-timeline-item>
  </a-timeline>
</template>

<script>
import { ref } from 'vue';
import { IconFire } from '@arco-design/web-vue/es/icon';

export default {
  components: {
    IconFire,
  },
  setup() {
    const pendingProps = ref({});

    const onChange = (newProps) => {
      pendingProps.value = {
        ...pendingProps.value,
        ...newProps,
      };
    };

    return {
      pendingProps,
      onChange
    }
  },
};
</script>
```

## Mode

The content will be displayed alternately when `mode=alternate` is set. At the same time, you can control the position of the timeline node by setting the positon property of TimelineItem.

```vue
<template>
  <a-row justify="space-between">
    <a-timeline mode="alternate" :style="{ flex: 1 }">
      <a-timeline-item label="2017-03-10">The first milestone</a-timeline-item>
      <a-timeline-item label="2018-05-12">The second milestone</a-timeline-item>
      <a-timeline-item label="2020-09-30" position="bottom">
        The third milestone
      </a-timeline-item>
    </a-timeline>
    <a-timeline mode="right" :style="{ flex: 1 }">
      <a-timeline-item label="2017-03-10">The first milestone</a-timeline-item>
      <a-timeline-item label="2018-05-12">The second milestone</a-timeline-item>
      <a-timeline-item label="2020-09-30" position="bottom">
        The third milestone
      </a-timeline-item>
    </a-timeline>
  </a-row>
</template>
```

## Vertical

The vertical time axis.

```vue
<template>
  <div>
    <a-row align="center" :style="{ marginBottom: '24px' }">
      <a-typography-text>mode: &nbsp; &nbsp;</a-typography-text>
      <a-radio-group @change="onChange" :modelValue="mode">
        <a-radio value="left">left</a-radio>
        <a-radio value="right">right</a-radio>
        <a-radio value="alternate">alternate</a-radio>
      </a-radio-group>
    </a-row>
    <a-timeline :mode="mode" labelPosition="relative">
      <a-timeline-item label="2012-08">
        <a-row :style="{ display: 'inline-flex', alignItems: 'center' }">
          <img
            width="40"
            :style="{ marginRight: '16px', marginBottom: '12px' }"
            src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/b5d834b83708a269b4562924436eac48.png~tplv-uwbnlip3yd-png.png"
          />
          <div :style="{ marginBottom: '12px' }">
            Toutiao
            <div :style="{ fontSize: '12px', color: '#4E5969' }">
              Founded in 2012
            </div>
          </div>
        </a-row>
      </a-timeline-item>
      <a-timeline-item label="2017-05">
        <a-row :style="{ display: 'inline-flex', alignItems: 'center' }">
          <img
            width="40"
            :style="{ marginRight: '16px', marginBottom: '12px' }"
            src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/385ed540c359ec8a9b9ce2b5fe89b098.png~tplv-uwbnlip3yd-png.png"
          />
          <div :style="{ marginBottom: '12px' }">
            Xigua Video
            <div :style="{ fontSize: '12px', color: '#4E5969' }">
              Founded in 2017
            </div>
          </div>
        </a-row>
      </a-timeline-item>
      <a-timeline-item label="2018-07">
        <a-row :style="{ display: 'inline-flex', alignItems: 'center' }">
          <img
            width="40"
            :style="{ marginRight: '16px', marginBottom: '12px' }"
            src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/385ed540c359ec8a9b9ce2b5fe89b098.png~tplv-uwbnlip3yd-png.png"
          />
          <div :style="{ marginBottom: '12px' }">
            Pipidance
            <div :style="{ fontSize: '12px', color: '#4E5969' }">
              Founded in 2018
            </div>
          </div>
        </a-row>
      </a-timeline-item>
    </a-timeline>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const mode = ref('left');

    const onChange = (_mode) => {
      mode.value = _mode;
    };

    return {
      mode,
      onChange
    }
  },
};
</script>
```

## Direction

You can set the display horizontal timeline through `direction`

```vue
<template>
  <div>
    <a-row align="center" :style="{ marginBottom: '24px' }">
      <a-typography-text>mode: &nbsp; &nbsp;</a-typography-text>
      <a-radio-group @change="onChange" :modelValue="mode">
        <a-radio value="top">top</a-radio>
        <a-radio value="bottom">bottom</a-radio>
        <a-radio value="alternate">alternate</a-radio>
      </a-radio-group>
    </a-row>
    <a-timeline direction="horizontal" pending :mode="mode">
      <a-timeline-item label="2012-08">
        <a-row :style="{ display: 'inline-flex', alignItems: 'center' }">
          <img
            width="40"
            :style="{ marginRight: '16px', marginBottom: '12px' }"
            src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/b5d834b83708a269b4562924436eac48.png~tplv-uwbnlip3yd-png.png"
          />
          <div :style="{ marginBottom: '12px' }">
            Toutiao
            <div :style="{ fontSize: '12px', color: '#4E5969' }">
              Founded in 2012
            </div>
          </div>
        </a-row>
      </a-timeline-item>
      <a-timeline-item label="2017-05">
        <a-row :style="{ display: 'inline-flex', alignItems: 'center' }">
          <img
            width="40"
            :style="{ marginRight: '16px', marginBottom: '12px' }"
            src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/385ed540c359ec8a9b9ce2b5fe89b098.png~tplv-uwbnlip3yd-png.png"
          />
          <div :style="{ marginBottom: '12px' }">
            Xigua Video
            <div :style="{ fontSize: '12px', color: '#4E5969' }">
              Founded in 2017
            </div>
          </div>
        </a-row>
      </a-timeline-item>
      <a-timeline-item label="2018-07">
        <a-row :style="{ display: 'inline-flex', alignItems: 'center' }">
          <img
            width="40"
            :style="{ marginRight: '16px', marginBottom: '12px' }"
            src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/385ed540c359ec8a9b9ce2b5fe89b098.png~tplv-uwbnlip3yd-png.png"
          />
          <div :style="{ marginBottom: '12px' }">
            Pipidance
            <div :style="{ fontSize: '12px', color: '#4E5969' }">
              Founded in 2018
            </div>
          </div>
        </a-row>
      </a-timeline-item>
    </a-timeline>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const mode = ref('top');

    const onChange = (_mode) => {
      mode.value = _mode;
    };

    return {
      mode,
      onChange
    }
  },
};
</script>
```

## Label Position

The position of the label text can be set by `labelPosition`.

```vue
<template>
  <div>
    <a-row align="center">
      <a-typography-text>labelPosition: &nbsp; &nbsp;</a-typography-text>
      <a-radio-group @change="onLabelPositionChange" :modelValue="pos">
        <a-radio value="same">same</a-radio>
        <a-radio value="relative">relative</a-radio>
      </a-radio-group>
    </a-row>
    <a-row align="center" :style="{ margin: '20px 0px 24px' }">
      <a-typography-text>mode: &nbsp; &nbsp;</a-typography-text>
      <a-radio-group @change="onModeChange" :modelValue="mode">
        <a-radio value="left">left</a-radio>
        <a-radio value="right">right</a-radio>
        <a-radio value="alternate">alternate</a-radio>
      </a-radio-group>
    </a-row>
    <a-timeline :mode="mode" :labelPosition="pos">
      <a-timeline-item label="2017-03-10" dotColor="#52C419">
        The first milestone
      </a-timeline-item>
      <a-timeline-item
        label="2018-05-12"
        dotColor="#F5222D"
        labelPosition="same"
      >
        The second milestone
      </a-timeline-item>
      <a-timeline-item label="2020-09-30" position="bottom">
        The third milestone
      </a-timeline-item>
    </a-timeline>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const mode = ref('left');
    const pos = ref('same');

    const onLabelPositionChange = (_pos) => {
      pos.value = _pos;
    };

    const onModeChange = (_mode) => {
      mode.value = _mode;
    };

    return {
      mode,
      pos,
      onLabelPositionChange,
      onModeChange
    }
  },
};
</script>
```

## Custom Label

You can customize labels through the 'label' slot

```vue
<template>
  <a-timeline>
    <a-timeline-item>
      Code Review
      <template #label>
        <a-tag>
          <template #icon>
            <icon-check-circle-fill />
          </template>
          Passed
        </a-tag>
      </template>
    </a-timeline-item>
  </a-timeline>
</template>
```

## API

### `<timeline>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|reverse|Whether reverse order|`boolean`|`false`|
|direction|Timeline direction|`'horizontal' \| 'vertical'`|`'vertical'`|
|mode|The display mode of Timeline|`'left' \| 'right' \| 'top' \| 'bottom' \| 'alternate'`|`'left'`|
|pending|Whether to display ghost nodes. When set to true, only ghost nodes are displayed. When passed a string, it will be displayed as node content|`boolean\|string`|`-`|
|label-position|Position of label text|`'relative' \| 'same'`|`'same'`|
### `<timeline>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|dot|Custom dot|-|

### `<timeline-item>` Props

|Attribute|Description|Type|Default|
|---|---|---|:---:|
|dot-color|Dot color|`string`|`-`|
|dot-type|Dot type|`'hollow' \| 'solid'`|`'solid'`|
|line-type|Line type|`'solid' \| 'dashed' \| 'dotted'`|`'solid'`|
|line-color|Line Color|`string`|`-`|
|label|Label text|`string`|`-`|
|position|Item position|`PositionType`|`-`|
### `<timeline-item>` Slots

|Slot Name|Description|Parameters|version|
|---|---|---|:---|
|dot|Custom dot|-||
|label|Custom label|-|2.50.0|
