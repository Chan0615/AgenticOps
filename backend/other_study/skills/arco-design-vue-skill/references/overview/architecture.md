---
name: arco-vue-architecture
description: "Arco Design Pro Vue architecture guide. Use for routes, menus, layout, permissions, mocks, Pinia, and project directory conventions."
user-invocable: false
---

# Architecture

## Directory Structure

## Content

```
README.md
package.json
index.html
src/
  api/                # Request interfaces
  assets/             # Static resources
    style/            # Global styles
  components/         # Shared business components
  config/             # Global config and themes
    settings.json     # Runtime settings
  directive/          # Custom directives
  filters/            # Optional filters
  hooks/              # Global hooks and composables
  layout/             # Layout files
  locale/             # Language packs
  mock/               # Mock data
  views/              # Page templates
  router/             # Route configuration
  store/              # State management
  types/              # TypeScript types
  utils/              # Utility helpers
  App.vue             # App entry component
  main.ts             # App bootstrap
tsconfig.json
```

ps: [Filter description](https://v3-migration.vuejs.org/breaking-changes/filters.html)

## Routes and menu

The routing is usually tied to the menu. In order to reduce the amount of maintenance, we directly generate the menu through the routing table.

## Router

First, you need to understand the configuration of the routing table. For basic routing configuration, please refer to the official documentation of [Vue-Router](https://router.vuejs.org/)

 ```ts
// In this example, the final path to the page is /dashboard/workplace
export default {
  path: 'dashboard',
  name: 'dashboard',
  component: () => import('@/views/dashboard/index.vue'),
  meta: {
    locale: 'menu.dashboard',
    requiresAuth: true,
    icon: 'icon-dashboard',
  },
  children: [
    {
      path: 'workplace',
      name: 'workplace',
      component: () => import('@/views/dashboard/workplace/index.vue'),
      meta: {
        locale: 'menu.dashboard.workplace',
        requiresAuth: true,
        roles: ['admin'],
        hideInMenu: false,
      },
    },
  ],
};
```

Route `Meta` meta information

| Key	 | Description | Type | default|
| ------------- | ------------- | -------------- | -------------- |
roles | Configure the role that can access the page. If it does not match, it will be forbidden to access the routing page	 | string[]| - |
requiresAuth | Whether login authentication is required | boolean| false |
icon | Menu configuration icon | string| - |
locale | First-level menu name (language pack key name) | string| - |
hideInMenu | Whether to hide this item in the left menu | boolean| - |
hideChildrenInMenu | Force single item to be displayed in left menu | boolean| - |
activeMenu | If set name, the menu will be highlighted according to the name you set | string| - |
order | Sort routing menu items. If this value is set, the higher the value, the higher the front. | number| - |
noAffix | If set to true, the tabs will not be added to the tab-bar. | boolean| - |
ignoreCache | If set to true the page will not be cached | boolean| - |

## Menu

Front-end menu generation process:

- Through the computed property of [appRoute](https://github.com/arco-design/arco-design-pro-vue/blob/23a21ceb939e1e2334e8c3b0f1f8a8049503ad9d/arco-design-pro-vite/src/components/menu/useMenuTree.ts#L10), a routing tree with routing information is obtained.

- Use the routing information obtained in the previous step to filter permissions to generate a menu [tree for rendering](https://github.com/arco-design/arco-design-pro-vue/blob/23a21ceb939e1e2334e8c3b0f1f8a8049503ad9d/arco-design-pro-vite/src/components/menu/useMenuTree.ts#L23).

- Recursively generate menus by [rendering](https://github.com/arco-design/arco-design-pro-vue/blob/23a21ceb939e1e2334e8c3b0f1f8a8049503ad9d/arco-design-pro-vite/src/components/menu/index.vue#L48) the menu tree.

Server menu generation process:

- Add the [action](https://github.com/arco-design/arco-design-pro-vue/blob/23a21ceb939e1e2334e8c3b0f1f8a8049503ad9d/arco-design-pro-vite/src/store/modules/app/index.ts#L47) of the api request to the Store to obtain the routing configuration of the server.

- Add the action of the api request to the Store to obtain the routing configuration of the server.

- Through the computed property of [appRoute](https://github.com/arco-design/arco-design-pro-vue/blob/23a21ceb939e1e2334e8c3b0f1f8a8049503ad9d/arco-design-pro-vite/src/components/menu/useMenuTree.ts#L10), a routing tree with routing information is obtained.

- Use the routing information obtained in the previous step to filter permissions to generate a menu [tree for rendering](https://github.com/arco-design/arco-design-pro-vue/blob/23a21ceb939e1e2334e8c3b0f1f8a8049503ad9d/arco-design-pro-vite/src/components/menu/useMenuTree.ts#L23).

- Recursively generate menus by [rendering](https://github.com/arco-design/arco-design-pro-vue/blob/23a21ceb939e1e2334e8c3b0f1f8a8049503ad9d/arco-design-pro-vite/src/components/menu/index.vue#L48) the menu tree.

**Note: Compared with the local menu generation process, the server menu only has more interface requests and server routing configuration information storage steps.**
**Individual companies may have corresponding authority management systems to generate corresponding server-side routing configuration information and store them for front-end interface retrieval. However, the overall situation is similar, as long as the routing configuration information returned by the back-end interface conforms to the above routing configuration specifications and can be correctly parsed by the front-end**

## Steps to add a new menu item

After understanding the routing and menu generation, you can configure a new menu item. Take a new monitoring page as an example.

- Add a monitor folder in views/dashboard and add index.vue to it

 ```ts
<script lang="ts" setup>
// monitor page logic
</script>
```

- Add the routing configuration of the monitoring page in the routing table

```diff
export default {
  path:'dashboard',
  name:'dashboard',
  component: () => import('@/views/dashboard/index.vue'),
  meta: {
    locale:'menu.dashboard',
    requiresAuth: true,
    icon:'icon-dashboard',
  },
  children: [
    {
      path:'workplace',
      name:'workplace',
      component: () => import('@/views/dashboard/workplace/index.vue'),
      meta: {
        locale:'menu.dashboard.workplace',
        requiresAuth: true,
      },
    },
+   {
+     path:'monitor',
+     name:'monitor',
+     component: () => import('@/views/dashboard/monitor/index.vue'),
+     meta: {
+       locale:'menu.dashboard.monitor',
+       requiresAuth: true,
+       roles: ['admin'],
+     },
+   },
  ],
};
```

- Added menu name in language pack

The following is the Chinese language pack, other language packs will not be repeated.

```diff
// src/locale/zh-CN.ts
export default {
  'menu.dashboard':'Dashboard',
  'menu.dashboard.workplace':'Workbench',
+ 'menu.dashboard.monitor':'Real-time monitoring',
}
```

Above, the configuration of a menu item is completed. Now refresh the page to see the new menu item.

## Layout

## Layout

There is only one set of layouts currently provided, which is applied to all routing pages, including side menu bar, top notification bar, footer and content area. The side bar and top notification bar are fixed to facilitate the scrolling process of users Focus on other views.

![](https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/ebd0bd6d4c044c1e945527194384fcaa.png~tplv-uwbnlip3yd-webp.webp)

In addition, the responsive sidebar will automatically shrink as follows when the window width is less than `1200px`:

![](https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/c730fddca82cf8c4cda27cef9ecd6683.png~tplv-uwbnlip3yd-webp.webp)

## Permission control

### A button permission management

Arco Design Pro encapsulates the `v-permission` directives . Can be used on components or native elements.
As follows, place the authorized role types in the array.

```vue
<button v-permission="['admin']">Delete</button>

<a-button v-permission="['user']">Delete</a-button>
```

The above is the specific method of using the front-end page for permission control, but it needs to combine the back-end interface to return the specific permissions owned by the user to the front-end.

At the same time, in the middle and back-end systems, it is far from enough to have simple front-end permission control, and the back-end is also required to perform interface permission control. In particular, some interfaces involving write operations need to strictly control permissions.

## Accomplish

### Routing authority management

Pro provides corresponding permission management hooks. The permission requirements of the business can be customized.

```ts
#src/hooks/permission.ts

import { RouteLocationNormalized, RouteRecordRaw } from 'vue-router';
import { useUserStore } from '@/store';

export default function usePermission() {
  const userStore = useUserStore();
  return {
    accessRouter(route: RouteLocationNormalized | RouteRecordRaw) { // Determine whether the current user has permission to the route
      return (
        !route.meta?.requiresAuth ||
        !route.meta?.roles ||
        route.meta?.roles?.includes('*') ||
        route.meta?.roles?.includes(userStore.role)
      );
    },
    // You can add any rules you want
  };
}
```

Set up a route guard, and manage the user's page entry and exit in the route guard. For example, whether the current user has logged in and whether the current user has page permissions.

``` ts
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  async function crossroads() {
    const Permission = usePermission();
    if (Permission.accessRouter(to)) await next();
    else {
      const destination = Permission.findFirstPermissionRoute(
        appRoutes,
        userStore.role
      ) || {
        name: 'notFound',
      }; // Go to the first authorized page or 404.
      await next(destination);
    }
  }
  if (isLogin()) { // Check if the user is logged in
    if (userStore.role) { // If there is role information, it means that the current user has logged in and obtained user information.
      crossroads();
    } else {
      try {
        await userStore.info(); // Obtain user role information and then perform subsequent jump processing
        crossroads();
      } catch (error) {
        next({
          name: 'login',
          query: {
            redirect: to.name,
            ...to.query,
          } as LocationQueryRaw,
        });
      }
    }
  } else {
    // Redirect to login page if not logged in
    if (to.name === 'login') {
      next();
      return;
    }
    next({
      name: 'login',
      query: {
        redirect: to.name,
        ...to.query,
      } as LocationQueryRaw,
    });
  }
});
```

Custom permission directive

```ts
import { DirectiveBinding } from 'vue';
import { useUserStore } from '@/store';

function checkPermission(el: HTMLElement, binding: DirectiveBinding) {
  const { value } = binding;
  const userStore = useUserStore();
  const { role } = userStore;

  if (Array.isArray(value)) {
    if (value.length > 0) {
      const permissionValues = value;
      // Compare the role permission of the current user with the permission type of the incoming command. If the current user does not have permission, the node deletion operation will be performed.
      const hasPermission = permissionValues.includes(role);
      if (!hasPermission && el.parentNode) {
        el.parentNode.removeChild(el);
      }
    }
  } else {
    throw new Error(`need roles! Like v-permission="['admin','user']"`);
  }
}

export default {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    checkPermission(el, binding);
  },
  updated(el: HTMLElement, binding: DirectiveBinding) {
    checkPermission(el, binding);
  },
};
```

## Interface and Mock

## Network request

Use axios to make remote interface requests.

It is recommended to improve the type definition of the returned and requested data.

 ```ts
import axios from 'axios';

export interface UserToken {
  token: string;
}

export interface UserStateTypes {
  name: string;
  location: string;
}
export function getUserInfo(data: UserToken) {
  // Get complete type hints by passing generics.
  return axios.post<UserStateTypes>('/api/user/info', data);
}
```

## Interceptor

Multi-layer interceptors can be added according to the needs of your own system.

 ```ts
import axios, {AxiosRequestConfig, AxiosResponse} from 'axios';
// Users can modify according to their own background system
export interface HttpResponse<T = unknown> {
  status: number;
  msg: string;
  code: number;
  data: T;
}

axios.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // Configure the request here
    return config;
  },
  (error) => {
    // What to do with request errors
    return Promise.reject(error);
  }
);
// Add response interceptor
axios.interceptors.response.use(
  (response: AxiosResponse<HttpResponse>) => {
    const res = response.data;
    // if the custom code is not 20000, it is judged as an error.
    if (res.code !== 20000) {
      // remind users

      // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      if (
        [50008, 50012, 50014].includes(res.code)
      ) {
        // do something
      }
      return Promise.reject(new Error(res.msg ||'Error'));
    }
    return res;
  },
  (error) => {
    return Promise.reject(error);
  }
);
```

Intercept ajax and return simulated data

## mock solution

Parallel development of the front and back ends means that the front end needs to be developed without interface data. In this case, if the function of simulating data requests can be provided, our data request code can be written normally. Pro uses Mock.js to achieve This feature.

Mock.js will intercept the ajax request. If there is a matching mock rule, the ajax will not be sent out, but the mock data will be returned. Mock.js has a wealth of simulation data generation methods, it is recommended to read the document first, the document is very clear and easy to understand [MockJs document](http://mockjs.com/)

 ```ts
import Mock from 'mockjs';
import {
  successResponseWrap,
} from '@/utils/setup-mock';

Mock.mock(new RegExp('/api/chatList'), () => {
    const data = Mock.mock(successResponseWrap({
        'data|4-6': [
            {
                'id|+1': 1,
                username:'User 7352772',
                content:'It will start soon, so excited! ',
                time: '13:09:12',
                'isCollect|2': true,
            },
        ],
    }));

    return data.data;
});
```

When the request url sent by the client is matched by `new RegExp('/api/chatList')`, Mock.js will intercept the request, execute the corresponding callback function, and return the data returned in the callback function.

> Note: Requests that are matched and intercepted by Mock.js will not appear in the network panel of the developer tools.

## Close Mock

In order to facilitate the opening and closing of the data simulation function, each `Mock` will be wrapped by `setupMock.setup`, the setupMock is as follows:

 ```ts
import {debug} from './env';
export default ({ mock, setup }: {mock?: boolean; setup: () => void; }) => {
  if (mock !== false && debug) setup();
};
```

Data simulation is started by default in a non-production environment. When we need to debug the interface, we only need to set the mock parameter of setupMock to false, as follows:

 ```ts
import Mock from 'mockjs';
import setupMock from '../utils/setupMock';

setupMock({
  mock: false,
  setup() {
  // User Info
    Mock.mock(new RegExp('/api/userInfo'), () => {
        return {
          name:'name',
        };
    });
  },
});
```

## State management - Pinia

## Add new module

1.  Add state type declaration

```ts
// store/modulers/user/types.ts
export interface UserState {
  name: string;
  avatar: string;
}
```

2.  Defining a store is as easy as defining a component

```ts
// store/modulers/user/index.ts
import { defineStore } from 'pinia';
import {
  login as userLogin,
  getUserInfo,
  LoginData,
} from '@/api/user';
import { setToken } from '@/utils/auth';
import { UserState } from './types';

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    name: '',
    avatar: '',
  }),

  getters: {
    userInfo(state: UserState): UserState {
      return { ...state };
    },
  },

  actions: {

    // Get user's information
    async info() {
      const res = await getUserInfo();

      this.setInfo(res.data);
    },

    // Login
    async login(loginForm: LoginData) {
      const res = await userLogin(loginForm);
      setToken(res.data.token);
    },
  },
});

```

## Specific use

```ts
import { defineComponent } from 'vue';
import { useUserStore } from '@/store';

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const login = () => {
      const userInfo ={
        username: 'admin',
        password: 'admin',
      };
      await userStore.login(userInfo);
    }
    return {
      login,
    }
  }
})
```

## Package build

## Package and build

When the code is written, execute the following command to package the code

```bash
npm run build
```

This command calls the packaging command provided by vite. After the packaging is completed, a `dist` folder will be generated in the root directory, which is the code that can be used for deployment.

PS: Tips for reducing package size! ! !

Because in the Pro project, the displayed table component requires the vue compile function, so a version with a compiler is introduced.

If you don't need the Vue template compilation function, delete the corresponding business code, configure the specified Vue version, and build and package to reduce the package size.

If you need the ability to compile vue templates, you can configure it in the vite.config.prod.ts file (see below).

 ```ts
// config/vite.config.build.ts
import {defineConfig} from 'vite';

export default defineConfig({
  mode:'production',
  ...
  resolve: {
    alias: [
      {
        find:'vue',
        replacement:'vue/dist/vue.esm-bundler.js', // need to compile tmp
      },
    ],
  },
});
```

For more specific configuration details, please refer to [vite](https://vitejs.dev/)[Official Website](https://vitejs.dev/).
