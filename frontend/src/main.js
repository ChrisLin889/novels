import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/css/main.css'
import './assets/css/global.css'

const app = createApp(App)

// Use plugins
app.use(router)
app.use(store)
app.use(ElementPlus)

// Mount the app
app.mount('#app')

// Test console log for debugging
console.log('Frontend application started successfully. Backend API URL:', process.env.VUE_APP_API_BASE_URL)
