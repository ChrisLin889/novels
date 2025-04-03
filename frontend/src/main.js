import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// Create app
const app = createApp(App)

// Use plugins
app.use(router)
app.use(store)
app.use(ElementPlus, { size: 'default' })

// Register all icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// Mount
app.mount('#app')

// Test console log for debugging
console.log('Frontend application started successfully. Backend API URL:', process.env.VUE_APP_API_BASE_URL)
