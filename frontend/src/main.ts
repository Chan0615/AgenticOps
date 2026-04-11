import { createApp } from 'vue'
import { createPinia } from 'pinia'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import updateLocale from 'dayjs/plugin/updateLocale'
import 'ant-design-vue/dist/reset.css'
import router from './router'
import App from './App.vue'
import './style.css'

dayjs.extend(updateLocale)
dayjs.locale('zh-cn')
dayjs.updateLocale('zh-cn', {
  weekStart: 1,
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
