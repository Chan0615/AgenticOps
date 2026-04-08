---
name: arco-vue-form
description: "A form with data collection, verification and submission functions, including checkboxes, radio buttons, input boxes, drop-down selection boxes and other elements. Use this reference in Vue 3 and Arco Design Pro Vue pages."
user-invocable: false
---

# Form

> Use the demos and API tables below for exact component behavior.
> For real business pages, check the relevant file in `references/patterns/` first, then return here for props, events, slots, and methods.

## Basic Usage

Basic usage of the form.

```vue
<template>
  <a-form :model="form" :style="{ width: '600px' }" @submit="handleSubmit">
    <a-form-item field="name" tooltip="Please enter username" label="Username">
      <a-input
        v-model="form.name"
        placeholder="please enter your username..."
      />
    </a-form-item>
    <a-form-item field="post" label="Post">
      <a-input v-model="form.post" placeholder="please enter your post..." />
    </a-form-item>
    <a-form-item field="isRead">
      <a-checkbox v-model="form.isRead"> I have read the manual </a-checkbox>
    </a-form-item>
    <a-form-item>
      <a-button html-type="submit">Submit</a-button>
    </a-form-item>
  </a-form>
  {{ form }}
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const form = reactive({
      name: '',
      post: '',
      isRead: false,
    });
    const handleSubmit = (data) => {
      console.log(data);
    };

    return {
      form,
      handleSubmit,
    };
  },
};
</script>
```

## Form Layout

The form supports three layout methods: `horizontal`, `vertical` and `inline`.

```vue
<template>
  <a-space direction="vertical" size="large" :style="{width: '600px'}">
    <a-radio-group v-model="layout" type="button">
      <a-radio value="horizontal">horizontal</a-radio>
      <a-radio value="vertical">vertical</a-radio>
      <a-radio value="inline">inline</a-radio>
    </a-radio-group>
    <a-form :model="form" :layout="layout">
      <a-form-item field="name" label="Username">
        <a-input v-model="form.name" placeholder="please enter your username..." />
      </a-form-item>
      <a-form-item field="post" label="Post">
        <a-input v-model="form.post" placeholder="please enter your post..." />
      </a-form-item>
      <a-form-item field="isRead">
        <a-checkbox v-model="form.isRead">
          I have read the manual
        </a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-button>Submit</a-button>
      </a-form-item>
    </a-form>
    <div>
      {{ form }}
    </div>
  </a-space>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const layout = ref('horizontal')
    const form = reactive({
      name: '',
      post: '',
      isRead: false,
    })

    return {
      layout,
      form,
    }
  },
}
</script>
```

## Extra Message & Help Message

You can use `extra` to add extra information.
You can use the `help` attribute or slot. The verification information will be blocked when `help` is set.

```vue
<template>
  <a-form :model="form" :style="{width:'600px'}">
    <a-form-item field="name" label="Username" validate-trigger="input" required>
      <a-input v-model="form.name" placeholder="please enter your username..." />
      <template #extra>
        <div>Used to login</div>
      </template>
    </a-form-item>
    <a-form-item field="post" label="Post" validate-trigger="input" required>
      <a-input v-model="form.post" placeholder="please enter your post..." />
      <template #extra>
        <div>Used to login</div>
      </template>
      <template #help>
        <div>Custom validation message</div>
      </template>
    </a-form-item>
    <a-form-item field="isRead">
      <a-checkbox v-model="form.isRead">
        I have read the manual
      </a-checkbox>
    </a-form-item>
  </a-form>
  {{ form }}
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const form = reactive({
      name: '',
      post: '',
      isRead: false,
    })

    return {
      form,
    }
  },
}
</script>
```

## Nest Data

Shows a variety of ways to nest form items.
The form item component binds the form item state and events to the first sub-component by default. If you want to use the form item for layout settings, please set `:merge-props="false"` to close the binding, or use a function to specify The data that needs to be bound.
If you use the grid component for layout, please set `:content-flex="false"` to turn off the flex layout of the form item content.

```vue
<template>
  <a-form :model="form" :style="{width:'600px'}">
    <a-form-item label="Username" :content-flex="false" :merge-props="false" extra="Show error message together">
      <a-row :gutter="8">
        <a-col :span="12">
          <a-form-item field="together.firstname" validate-trigger="input"
                       :rules="[{required:true,message:'firstname is required'}]" no-style>
            <a-input v-model="form.together.firstname" placeholder="please enter your firstname..." />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item field="together.lastname" validate-trigger="input"
                       :rules="[{required:true,message:'lastname is required'}]" no-style>
            <a-input v-model="form.together.lastname" placeholder="please enter your lastname..." />
          </a-form-item>
        </a-col>
      </a-row>
    </a-form-item>
    <a-form-item label="Username" :content-flex="false" :merge-props="false">
      <a-row :gutter="8">
        <a-col :span="12">
          <a-form-item field="separate.firstname" validate-trigger="input"
                       extra="Show error message separate"
                       :rules="[{required:true,message:'firstname is required'}]" hide-label>
            <a-input v-model="form.separate.firstname" placeholder="please enter your firstname..." />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item field="separate.lastname" validate-trigger="input"
                       :rules="[{required:true,message:'lastname is required'}]" hide-label>
            <a-input v-model="form.separate.lastname" placeholder="please enter your lastname..." />
          </a-form-item>
        </a-col>
      </a-row>
    </a-form-item>
    <a-form-item label="Posts" :content-flex="false" :merge-props="false">
      <a-space direction="vertical" fill>
        <a-form-item field="posts.post1" label="Post1">
          <a-input v-model="form.posts.post1" placeholder="please enter your post..." />
        </a-form-item>
        <a-form-item field="posts.post2" label="Post2">
          <a-input v-model="form.posts.post2" placeholder="please enter your post..." />
        </a-form-item>
      </a-space>
    </a-form-item>
    <a-form-item field="isRead">
      <a-checkbox v-model="form.isRead">
        I have read the manual
      </a-checkbox>
    </a-form-item>
  </a-form>
  {{ form }}
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const form = reactive({
      together: {
        firstname: '',
        lastname: '',
      },
      separate: {
        firstname: '',
        lastname: '',
      },
      posts: {
        post1: '',
        post2: ''
      },
      isRead: false,
    })

    return {
      form,
    }
  },
}
</script>
```

## Grid

Shows how to use grid layout. You can use the `label-col-flex` property to specify the specific width of the label.

```vue
<template>
  <a-form :model="form">
    <a-row :gutter="16">
      <a-col :span="8">
        <a-form-item field="value1" label="Value 1" label-col-flex="100px">
          <a-input v-model="form.value1" placeholder="please enter..." />
        </a-form-item>
      </a-col>
      <a-col :span="8">
        <a-form-item field="value2" label="Value 2" label-col-flex="80px">
          <a-input v-model="form.value2" placeholder="please enter..." />
        </a-form-item>
      </a-col>
      <a-col :span="8">
        <a-form-item field="value3" label="Value 3" label-col-flex="80px">
          <a-input v-model="form.value3" placeholder="please enter..." />
        </a-form-item>
      </a-col>
    </a-row>
    <a-row :gutter="16">
      <a-col :span="16">
        <a-form-item field="value4" label="Value 4" label-col-flex="100px">
          <a-input v-model="form.value4" placeholder="please enter..." />
        </a-form-item>
      </a-col>
      <a-col :span="8">
        <a-form-item field="value5" label="Value 5" label-col-flex="80px">
          <a-input v-model="form.value5" placeholder="please enter..." />
        </a-form-item>
      </a-col>
    </a-row>
  </a-form>
  {{ form }}
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const form = reactive({
      value1: '',
      value2: '',
      value3: '',
      value4: '',
      value5: '',
    })

    return {
      form,
    }
  },
}
</script>
```

## Auto Label Width

Set `auto-label-width` to enable automatic label width. It only takes effect under the layout of `layout="horizontal"`.
_* Currently it only takes effect after the first load._

```vue
<template>
  <a-form :model="form" :style="{width:'600px'}" auto-label-width @submit="handleSubmit">
    <a-form-item field="name" label="Username">
      <a-input v-model="form.name" placeholder="please enter your username..." />
    </a-form-item>
    <a-form-item field="post" label="Post">
      <a-input v-model="form.post" placeholder="please enter your post..." />
    </a-form-item>
    <a-form-item field="isRead">
      <a-checkbox v-model="form.isRead">
        I have read the manual
      </a-checkbox>
    </a-form-item>
    <a-form-item>
      <a-button html-type="submit">Submit</a-button>
    </a-form-item>
  </a-form>
  {{ form }}
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const form = reactive({
      name: '',
      post: '',
      isRead: false,
    })
    const handleSubmit = (data) => {
      console.log(data)
    }

    return {
      form,
      handleSubmit
    }
  },
}
</script>
```

## Validation

Shows how to use form validation.

```vue
<template>
  <a-form ref="formRef" :size="form.size" :model="form" :style="{width:'600px'}" @submit="handleSubmit">
    <a-form-item field="size" label="Form Size" >
      <a-radio-group v-model="form.size" type="button">
        <a-radio value="mini">Mini</a-radio>
        <a-radio value="small">Small</a-radio>
        <a-radio value="medium">Medium</a-radio>
        <a-radio value="large">Large</a-radio>
      </a-radio-group>
    </a-form-item>
    <a-form-item field="name" label="Username"
                 :rules="[{required:true,message:'name is required'},{minLength:5,message:'must be greater than 5 characters'}]"
                 :validate-trigger="['change','input']"
    >
      <a-input v-model="form.name" placeholder="please enter your username..." />
    </a-form-item>
    <a-form-item field="age" label="Age"
                 :rules="[{required:true,message:'age is required'},{type:'number', max:200,message:'age is max than 200'}]"
    >
      <a-input-number v-model="form.age" placeholder="please enter your age..." />
    </a-form-item>
    <a-form-item field="section" label="Section" :rules="[{match:/section one/,message:'must select one'}]">
      <a-select v-model="form.section" placeholder="Please select ..." allow-clear>
        <a-option value="section one">Section One</a-option>
        <a-option value="section two">Section Two</a-option>
        <a-option value="section three">Section Three</a-option>
      </a-select>
    </a-form-item>
    <a-form-item field="province" label="Province" :rules="[{required:true,message:'province is required'}]">
      <a-cascader v-model="form.province" :options="options" placeholder="Please select ..." allow-clear />
    </a-form-item>
    <a-form-item field="options" label="Options"
                 :rules="[{type:'array',minLength:2,message:'must select greater than two options'}]"
    >
      <a-checkbox-group v-model="form.options">
        <a-checkbox value="option one">Section One</a-checkbox>
        <a-checkbox value="option two">Option Two</a-checkbox>
        <a-checkbox value="option three">Option Three</a-checkbox>
        <a-checkbox value="option four">Option Four</a-checkbox>
      </a-checkbox-group>
    </a-form-item>
    <a-form-item field="date" label="Date">
      <a-date-picker v-model="form.date" placeholder="Please select ..."/>
    </a-form-item>
    <a-form-item field="time" label="Time">
      <a-time-picker v-model="form.time" placeholder="Please select ..."/>
    </a-form-item>
    <a-form-item field="radio" label="Radio" :rules="[{match:/one/,message:'must select one'}]">
      <a-radio-group v-model="form.radio">
        <a-radio value="radio one">Radio One</a-radio>
        <a-radio value="radio two">Radio Two</a-radio>
      </a-radio-group>
    </a-form-item>
    <a-form-item field="slider" label="Slider" :rules="[{type:'number', min:5,message:'slider is min than 5'}]">
      <a-slider v-model="form.slider" :max="10" />
    </a-form-item>
    <a-form-item field="score" label="Score">
      <a-rate v-model="form.score" allow-clear />
    </a-form-item>
    <a-form-item field="switch" label="Switch" :rules="[{type:'boolean', true:true,message:'must be true'}]">
      <a-switch v-model="form.switch" />
    </a-form-item>
    <a-form-item field="multiSelect" label="Multiple Select">
      <a-select v-model="form.multiSelect" placeholder="Please select ..." multiple>
        <a-option value="section one">Section One</a-option>
        <a-option value="section two">Section Two</a-option>
        <a-option value="section three">Section Three</a-option>
      </a-select>
    </a-form-item>
    <a-form-item field="treeSelect" label="Tree Select">
      <a-tree-select :data="treeData" v-model="form.treeSelect" placeholder="Please select ..."/>
    </a-form-item>
    <a-form-item>
      <a-space>
        <a-button html-type="submit">Submit</a-button>
        <a-button @click="$refs.formRef.resetFields()">Reset</a-button>
      </a-space>
    </a-form-item>
  </a-form>
  {{ form }}
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const handleSubmit = ({values, errors}) => {
      console.log('values:', values, '\nerrors:', errors)
    }

    const form = reactive({
      size: 'medium',
      name: '',
      age: undefined,
      section: '',
      province: 'haidian',
      options: [],
      date: '',
      time: '',
      radio: 'radio one',
      slider: 5,
      score: 5,
      switch: false,
      multiSelect: ['section one'],
      treeSelect: ''
    });
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
            label: 'XiCheng',
          },
        ],
      },
      {
        value: 'shanghai',
        label: 'Shanghai',
        children: [
          {
            value: 'shanghaishi',
            label: 'Shanghai',
            children: [
              {
                value: 'huangpu',
                label: 'Huangpu',
              },
            ],
          },
        ],
      },
    ];
    const treeData = [
      {
        key: 'node1',
        title: 'Node1',
        children: [
          {
            key: 'node2',
            title: 'Node2',
          },
        ],
      },
      {
        key: 'node3',
        title: 'Node3',
        children: [
          {
            key: 'node4',
            title: 'Node4',
          },
          {
            key: 'node5',
            title: 'Node5',
          },
        ],
      },
    ]

    return {
      form,
      options,
      treeData,
      handleSubmit
    }
  },
}
</script>
```

## Validation2

It shows how to use form validation rules on `a-form`, and how to verify `email`, `ip`, and `url` directly

```vue
<template>
  <a-form ref="formRef" :rules="rules" :model="form" :style="{width:'600px'}" @submit="handleSubmit">
    <a-form-item field="name" label="Username" validate-trigger="blur">
      <a-input v-model="form.name" placeholder="please enter your username..." />
    </a-form-item>
    <a-form-item field="password" label="Password" validate-trigger="blur">
      <a-input-password v-model="form.password" placeholder="please enter your password..." />
    </a-form-item>
    <a-form-item field="password2" label="Confirm Password" validate-trigger="blur">
      <a-input-password v-model="form.password2" placeholder="please confirm your password..." />
    </a-form-item>
    <a-form-item field="email" label="email">
      <a-input v-model="form.email" placeholder="please enter your email..." />
    </a-form-item>
    <a-form-item field="ip" label="IP">
      <a-input v-model="form.ip" placeholder="please enter your ip..." />
    </a-form-item>
    <a-form-item field="url" label="URL">
      <a-input v-model="form.url" placeholder="please enter your url..." />
    </a-form-item>
    <a-form-item field="match" label="match">
      <a-input v-model="form.match" placeholder="please enter your match..." />
    </a-form-item>
    <a-form-item>
      <a-space>
        <a-button html-type="submit">Submit</a-button>
        <a-button @click="$refs.formRef.resetFields()">Reset</a-button>
      </a-space>
    </a-form-item>
  </a-form>
  {{ form }}
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const handleSubmit = ({values, errors}) => {
      console.log('values:', values, '\nerrors:', errors)
    }

    const form = reactive({
      name: '',
      password: '',
      password2: '',
      email: '',
      ip: '192.168.2.1',
      url: '',
      match: ''
    });

    const rules = {
      name: [
        {
          required: true,
          message:'name is required',
        },
      ],
      password: [
        {
          required: true,
          message:'password is required',
        },
      ],
      password2: [
        {
          required: true,
          message:'password is required',
        },
        {
          validator: (value, cb) => {
            if (value !== form.password) {
              cb('two passwords do not match')
            } else {
              cb()
            }
          }
        }
      ],
      email: [
        {
          type: 'email',
          required: true,
        }
      ],
      ip: [
        {
          type: 'ip',
          required: true,
        }
      ],
      url: [
        {
          type: 'url',
          required: true,
        }
      ],
      match: [
        {
          required: true,
          validator: (value, cb) => {
            return new Promise((resolve) => {
              if (!value) {
                cb('Please enter match')
              }
              if (value !== 'match') {
                cb('match must be match!')
              }
              resolve()
            })
          }
        }
      ],
    }

    return {
      form,
      rules,
      handleSubmit
    }
  },
}
</script>
```

## Form

Enable `feedback` to allow some input components to display current state information

```vue
<template>
  <a-space direction="vertical" size="large">
    <a-radio-group v-model="status" type="button">
      <a-radio value="validating">validating</a-radio>
      <a-radio value="success">success</a-radio>
      <a-radio value="error">error</a-radio>
      <a-radio value="warning">warning</a-radio>
    </a-radio-group>
    <a-radio-group v-model="size" type="button">
      <a-radio value="mini">mini</a-radio>
      <a-radio value="small">small</a-radio>
      <a-radio value="medium">medium</a-radio>
      <a-radio value="large">large</a-radio>
    </a-radio-group>
  </a-space>
  <a-form
    :model="form"
    :style="{ width: '600px', marginTop: '20px' }"
    :size="size"
  >
    <a-form-item
      field="name"
      label="Username"
      help="This is custom message"
      extra="This is extra text"
      :validate-status="status"
      feedback
    >
      <a-input
        v-model="form.name"
        placeholder="please enter your username..."
      />
    </a-form-item>
    <a-form-item
      field="post"
      label="Post"
      help="This is custom message"
      extra="This is extra text"
      :validate-status="status"
      feedback
    >
      <a-input-number
        v-model="form.post"
        placeholder="please enter your post..."
      />
    </a-form-item>
    <a-form-item
      field="tags"
      label="Tags"
      help="This is custom message"
      extra="This is extra text"
      :validate-status="status"
      feedback
    >
      <a-input-tag
        v-model="form.tags"
        placeholder="please enter your post..."
      />
    </a-form-item>
    <a-form-item
      field="section"
      label="Section"
      :rules="[{ match: /section one/, message: 'must select one' }]"
      :validate-status="status"
      feedback
    >
      <a-select v-model="form.section" placeholder="Please select ...">
        <a-option value="section one">Section One</a-option>
        <a-option value="section two">Section Two</a-option>
        <a-option value="section three">Section Three</a-option>
      </a-select>
    </a-form-item>
    <a-form-item label="DateRange" :validate-status="status" feedback>
      <a-range-picker></a-range-picker>
    </a-form-item>

    <a-form-item field="date" label="Date" :validate-status="status" feedback>
      <a-date-picker></a-date-picker>
    </a-form-item>

    <a-form-item field="time" label="Time" :validate-status="status" feedback>
      <a-time-picker></a-time-picker>
    </a-form-item>
  </a-form>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const status = ref('success');
    const size = ref('medium');
    const form = reactive({
      name: '',
      post: undefined,
      tags: ['tag1'],
      section: '',
    });

    return {
      status,
      size,
      form,
    };
  },
};
</script>
```

## Dynamic Form

Dynamically control form content through data.

```vue
<template>
  <a-form :model="form" :style="{width:'600px'}">
    <a-form-item field="name" label="Username">
      <a-input v-model="form.name" placeholder="please enter your username..." />
    </a-form-item>
    <a-form-item v-for="(post,index) of form.posts" :field="`posts[${index}].value`" :label="`Post-${index}`" :key="index">
      <a-input v-model="post.value" placeholder="please enter your post..." />
      <a-button @click="handleDelete(index)" :style="{marginLeft:'10px'}">Delete</a-button>
    </a-form-item>
  </a-form>
  <div>
    <a-button @click="handleAdd">Add Post</a-button>
  </div>
  {{ form }}
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const form = reactive({
      name: '',
      posts: [{value: ''}]
    })
    const handleAdd = () => {
      form.posts.push({
        value: ''
      })
    };
    const handleDelete = (index) => {
      form.posts.splice(index, 1)
    }

    return {
      form,
      handleAdd,
      handleDelete
    }
  },
}
</script>
```

## Global Disabled

The entire form can be disabled through the `disabled` attribute.

```vue
<template>
  <a-form :model="form" :style="{width:'600px'}" disabled>
    <a-form-item field="name" label="Username">
      <a-input v-model="form.name" placeholder="please enter your username..." />
    </a-form-item>
    <a-form-item field="post" label="Post">
      <a-input v-model="form.post" placeholder="please enter your post..." />
    </a-form-item>
    <a-form-item field="isRead">
      <a-checkbox v-model="form.isRead">
        I have read the manual
      </a-checkbox>
    </a-form-item>
    <a-form-item>
      <a-button>Submit</a-button>
    </a-form-item>
  </a-form>
  {{ form }}
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    const form = reactive({
      name: '',
      post: '',
      isRead: false,
    })

    return {
      form,
    }
  },
}
</script>
```

## Asynchronous validation

Verify the form function through an asynchronous method.

```vue

<template>
  <a-form ref="formRef" :model="form" :style="{width:'600px'}">
    <a-form-item field="name" label="Username" :rules="rules">
      <a-input v-model="form.name" placeholder="please enter your username..." />
    </a-form-item>
    <a-form-item field="post" label="Post">
      <a-input v-model="form.post" placeholder="please enter your post..." />
    </a-form-item>
    <a-form-item field="isRead">
      <a-checkbox v-model="form.isRead">
        I have read the manual
      </a-checkbox>
    </a-form-item>
    <a-form-item>
      <a-button @click="handleClick">Set Status</a-button>
    </a-form-item>
  </a-form>
  {{ form }}
</template>

<script>
import { ref, reactive } from 'vue';

export default {
  setup() {
    const formRef = ref()
    const form = reactive({
      name: '',
      post: '',
      isRead: false,
    })
    const rules = [{
      validator: (value, cb) => {
        return new Promise(resolve => {
          window.setTimeout(() => {
            if (value !== 'admin') {
              cb('name must be admin')
            }
            resolve()
          }, 2000)
        })
      }
    }];
    const handleClick = () => {
      formRef.value.setFields({
        name: {
          status: 'error',
          message: 'async name error'
        },
        post: {
          status: 'error',
          message: 'valid post'
        }
      })
    }

    return {
      formRef,
      form,
      rules,
      handleClick
    }
  },
}
</script>
```

## Custom Form Item

Customize form components with `useFormItem`. Available since version 2.18.0.

```vue
<template>
  <a-space style="margin-bottom: 20px;">
    <a-switch v-model="disabled" />
    Disabled: {{disabled}}
  </a-space>
  <Form :model="form" :disabled="disabled" :style="{width:'600px'}">
    <FormItem field="name" label="Username"
              :rules="[{required:true,message:'name is required'},{minLength:5,message:'must be greater than 5 characters'}]">
      <MyInput v-model="form.name" placeholder="please enter your username..." />
    </FormItem>
  </Form>
</template>

<script lang="ts">
import { h, reactive, ref } from 'vue';
import { Form, FormItem, useFormItem } from '@arco-design/web-vue';

const MyInput = {
  emits: ['update:modelValue'],
  setup(_, { emit }) {
    const { mergedDisabled, eventHandlers } = useFormItem();
    const handleInput = (ev) => {
      const { value } = ev.target;
      emit('update:modelValue', value)
      eventHandlers.value?.onChange?.(ev)
    }
    return () => h('input', { disabled: mergedDisabled.value, onInput: handleInput })
  }
}

export default {
  components: {
    Form,
    FormItem,
    MyInput
  },
  setup() {
    const disabled = ref(false);
    const form = reactive({
      name: ''
    })

    return {
      disabled,
      form
    }
  },
}
</script>
```

## Scroll To Field

Showed the usage methods for automatically scrolling to the first error field on submission failure and manually scrolling to the corresponding field.

```vue
<template>
  <a-space>
    <a-button @click="formRef && formRef.validate()">Submit</a-button>
    <a-button @click="formRef && formRef.resetFields()">Reset</a-button>
    <a-button @click="formRef && formRef.scrollToField('name19')">Scroll to the last field</a-button>
  </a-space>
  <a-form
    ref="formRef"
    style="width: 500px;height: 300px;margin-top:20px;padding-right: 16px;overflow: auto"
    :model="form"
    :scrollToFirstError="true"
  >
    <template v-for="(fieldName, index) in fieldNames" :key="index">
      <a-form-item
        :field="fieldName"
        :label="'user' + index"
        :rules="[
          { required: true, message: 'Name is required' },
        ]"
      >
        <a-input v-model="form[fieldName]" />
      </a-form-item>
    </template>
  </a-form>
</template>

<script>
import { reactive, ref } from 'vue';

export default {
  setup() {
    const formRef = ref(null);
    const fieldCount = 20;
    const fieldNames = Array.from({ length: fieldCount }, (_, index) => `name${index}`);
    const form = reactive(Object.fromEntries(
      fieldNames.map((fieldName, index) => [fieldName, index === 7 ? '' : index.toString()])
    ));

    return {
      form,
      formRef,
      fieldCount,
      fieldNames
    };
  },
};
</script>
```

## API

### `<form>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|model **(required)**|Form data object|`object`|`-`||
|layout|The layout of the form, including horizontal, vertical, and multi-column|`'horizontal' \| 'vertical' \| 'inline'`|`'horizontal'`||
|size|The size of the form|`'mini' \| 'small' \| 'medium' \| 'large'`|`'medium'`||
|label-col-props|Label element layout options. The parameters are the same as the `<col>` component|`object`|` span: 5, offset: 0 `||
|wrapper-col-props|Form control layout options. The parameters are the same as the `<col>` component|`object`|` span: 19, offset: 0 `||
|label-align|Alignment direction of the label|`'left' \| 'right'`|`'right'`||
|disabled|Whether to disable the form|`boolean`|`-`||
|rules|Form item validation rules|`Record<string, FieldRule \| FieldRule[]>`|`-`||
|auto-label-width|Whether to enable automatic label width, it only takes effect under `layout="horizontal"`.|`boolean`|`false`|2.13.0|
|id|Form `id` attribute and form control `id` prefix|`string`|`-`||
|scroll-to-first-error|Scroll to the first error field after verification fails|`boolean`|`false`|2.51.0|
### `<form>` Events

|Event Name|Description|Parameters|
|---|---|---|
|submit|Triggered when the form is submitted|data: `{values: Record<string, any>; errors: Record<string, ValidatedError> \| undefined}`<br>ev: `Event`|
|submit-success|Triggered when verification is successful|values: `Record<string, any>`<br>ev: `Event`|
|submit-failed|Triggered when verification failed|data: `{values: Record<string, any>; errors: Record<string, ValidatedError>}`<br>ev: `Event`|
### `<form>` Methods

|Method|Description|Parameters|Return|version|
|---|---|---|:---:|:---|
|validate|Verify all form data|callback: `(errors: undefined \| Record<string, ValidatedError>) => void`|Promise<undefined \| Record<string, ValidatedError>>||
|validateField|Validate part of the form data|field: `string \| string[]`<br>callback: `(errors: undefined \| Record<string, ValidatedError>) => void`|Promise<undefined \| Record<string, ValidatedError>>||
|resetFields|Reset form data|field: `string \| string[]`|-||
|clearValidate|Clear verification status|field: `string \| string[]`|-||
|setFields|Set the value and status of the form item|data: `Record<string, FieldData>`|-||
|scrollToField|Scroll to the specified form item|field: `string`|-|2.51.0|

### `<form-item>` Props

|Attribute|Description|Type|Default|version|
|---|---|---|:---:|:---|
|field|The path of the form element in the data object (required for the data item)|`string`|`''`||
|label|Label text|`string`|`-`||
|tooltip|Tooltip text|`string`|`-`|2.41.0|
|show-colon|Whether to show a colon|`boolean`|`false`||
|no-style|Whether to remove the style|`boolean`|`false`||
|disabled|Whether to disable|`boolean`|`-`||
|help|Help copywriting|`string`|`-`||
|extra|Additional display copy|`string`|`-`||
|required|Is it required|`boolean`|`false`||
|asterisk-position|Optionally place an asterisk before/after the label|`'start' \| 'end'`|`'start'`|2.41.0|
|rules|Form item validation rules (The priority is higher than the rules of form)|`FieldRule \| FieldRule[]`|`-`||
|validate-status|Validate status|`'success' \| 'warning' \| 'error' \| 'validating'`|`-`||
|validate-trigger|The event that triggers the verification|`'change' \| 'input' \| 'focus' \| 'blur'`|`'change'`||
|label-col-props|Label element layout options. The parameters are the same as the `<col>` component|`object`|`-`||
|wrapper-col-props|Form control layout options. The parameters are the same as the `<col>` component|`object`|`-`||
|hide-label|Whether to hide the label|`boolean`|`false`||
|hide-asterisk|Whether to hide the asterisk|`boolean`|`false`||
|label-col-style|The style of the label element layout component|`object`|`-`|2.10.0|
|wrapper-col-style|The style of the form control layout component|`object`|`-`|2.10.0|
|row-props|Form item layout options. The parameters are the same as the `<row>` component|`object`|`-`|2.10.0|
|row-class|The class of the form item layout component|`string\|array\|object`|`-`|2.10.0|
|content-class|The class of the form control wrapping layer|`string\|array\|object`|`-`|2.10.0|
|content-flex|Whether to enable flex layout in the content layer|`boolean`|`true`|2.13.0|
|merge-props|(Repealed) Control the Props passed to the child element. The default includes disabled, error, size, events and additional attributes on FormItem. Version 2.18.0 deprecated|`boolean \| ((props: Record<string, any>) => Record<string, any>)`|`true`|2.13.0|
|label-col-flex|Set the flex property of the label `Col` component. When set, the flex property of the form `Col` component will be set to `auto`.|`number\|string`|`-`|2.13.0|
|feedback|Whether to show the feedback icon for the form control|`boolean`|`false`|2.16.0|
|label-component|The element that the form item label renders|`string`|`'label'`|2.22.0|
|label-attrs|Attributes of the form item element|`object`|`-`|2.22.0|
### `<form-item>` Slots

|Slot Name|Description|Parameters|
|---|---|---|
|label|Label|-|
|help|Help message|-|
|extra|Extra content|-|

## Type

### FieldRule

|Name|Description|Type|Default|
|---|---|---|:---:|
|type|The type of the value to be checked, the default is `'string'`|`'string'    \| 'number'    \| 'boolean'    \| 'array'    \| 'object'    \| 'email'    \| 'url'    \| 'ip'`|`-`|
|required|Is it required|`boolean`|`false`|
|message|Information displayed when verification fails|`string`|`-`|
|length|Check length (string, array)|`number`|`-`|
|maxLength|Maximum length (string)|`number`|`-`|
|minLength|Minimum length (string)|`number`|`-`|
|match|Match check (string)|`RegExp`|`-`|
|uppercase|Uppercase (string)|`boolean`|`false`|
|lowercase|Lowercase (string)|`boolean`|`false`|
|min|Minimum (number)|`number`|`-`|
|max|Maximum (number)|`number`|`-`|
|equal|Check value (number)|`number`|`-`|
|positive|Positive number (number)|`boolean`|`false`|
|negative|Negative number (number)|`boolean`|`false`|
|true|Whether it is `true` (boolean)|`boolean`|`false`|
|false|Whether it is `false` (boolean)|`boolean`|`false`|
|includes|Does the array contain the given value (array)|`any[]`|`-`|
|deepEqual|Are array elements equal (array)|`any`|`-`|
|empty|Is it empty (object)|`boolean`|`false`|
|hasKeys|Does the object contain the given attribute (object)|`string[]`|`-`|
|validator|Custom verification rules|`(    value: FieldValue \| undefined,    callback: (error?: string) => void  ) => void`|`-`|

### FieldData

|Name|Description|Type|Default|
|---|---|---|:---:|
|value|Field value|`any`|`-`|
|status|Field status|`ValidateStatus`|`-`|
|message|Field error message|`string`|`-`|

### ValidatedError

|Name|Description|Type|Default|version|
|---|---|---|:---:|:---|
|label|Label text|`string`|`-`|2.18.0|
|field|Field name|`string`|`-`||
|value|Field value|`any`|`-`||
|type|Field Type|`string`|`-`||
|isRequiredError|Is it a `required` error|`boolean`|`false`||
|message|Error message|`string`|`-`||

### FormItemEventHandler

|Name|Description|Type|Default|
|---|---|---|:---:|
|onChange|onChange|`(ev?: Event) => void`|`-`|
|onInput|onInput|`(ev?: Event) => void`|`-`|
|onFocus|onFocus|`(ev?: Event) => void`|`-`|
|onBlur|onBlur|`(ev?: Event) => void`|`-`|

### useFormItem

```ts
const useFormItem = (data: {
  size?: Ref<Size | undefined>;
  disabled?: Ref<boolean>;
  error?: Ref<boolean>;
}) => {
  mergedSize:Ref<Size>;
  mergedDisabled:Ref<boolean>;
  mergedError:Ref<boolean>;
  feedback:Ref<string>;
  eventHandlers:Ref<FormItemEventHandler>;
}
```

## FAQ

### About the `field` attribute of `form-item`
The value of the `field` attribute is the path string to get the corresponding value of the current `form-item`. Array division can also use `[]`, for example `field="people[2].id"`

For example, the data structure passed into the model property is:
```ts
const data = reactive({
   name:'xiaoming',
   people:[
     {
       id:'1111'
     },
     {
       // bind this value
       id:'2222'
     }
   ]
})
````
At this point, if you want to specify the value corresponding to the current `form-item` as `id: '2222'`, you need to set `field="people.2.id"`, and the separator in the value needs to use `.`

### About using clickable elements in the label slot

The title area of the form component is wrapped with the `label` element by default, which will activate the input component when clicked. If you put a clickable component in it, it will affect its normal function.
At this point, you can use the `label-component` attribute to modify the wrapping element to `span` to solve this problem.
