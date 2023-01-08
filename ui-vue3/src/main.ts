import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from '@/App.vue'
import router from '@/router'
import {BootstrapVue3} from 'bootstrap-vue-3'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
// 全局样式
import '@less/global.less'

createApp(App)
  .use(createPinia()) // 启用 Pinia
  .use(router)
  .use(BootstrapVue3)
  .mount('#app')
