<template>
  <div id="app">
    <NavBar />
    <div class="main-content">
      <router-view />
    </div>
    <Footer />
  </div>
</template>

<script>
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    Footer
  }
}
</script>

<style>
/* 全局变量和样式定义 */
:root {
  /* 颜色系统 */
  --primary-color: #3f51b5;
  --primary-light: #757de8;
  --primary-dark: #002984;
  --secondary-color: #00bcd4;
  --accent-color: #ff4081;
  
  --gray-50: #f8f9fa;
  --gray-100: #f1f3f5;
  --gray-200: #e9ecef;
  --gray-300: #dee2e6;
  --gray-400: #ced4da;
  --gray-500: #adb5bd;
  --gray-600: #6c757d;
  --gray-700: #495057;
  --gray-800: #343a40;
  --gray-900: #212529;
  
  /* 字体大小 */
  --font-size-xs: 0.75rem;   /* 12px */
  --font-size-sm: 0.875rem;  /* 14px */
  --font-size-md: 1rem;      /* 16px */
  --font-size-lg: 1.125rem;  /* 18px */
  --font-size-xl: 1.25rem;   /* 20px */
  --font-size-xxl: 1.5rem;   /* 24px */
  
  /* 边框圆角 */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  
  /* 阴影效果 */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.15);
  --shadow-hover: 0 8px 24px rgba(0, 0, 0, 0.18);
  
  /* 过渡效果 */
  --transition-fast: all 0.15s ease;
  --transition-medium: all 0.3s ease;
  --transition-slow: all 0.5s ease;
  
  /* 渐变背景 */
  --tech-gradient: linear-gradient(135deg, #3f51b5 0%, #00bcd4 100%);
  --tech-gradient-alt: linear-gradient(135deg, #3949ab 0%, #039be5 100%);
}

/* 全局默认封面样式 - 使用!important确保覆盖组件内部样式 */
.default-cover {
  background: linear-gradient(135deg, #3f51b5 0%, #00bcd4 100%) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
  overflow: hidden !important;
}

.default-cover::before {
  content: '' !important;
  position: absolute !important;
  top: -50% !important;
  left: -50% !important;
  width: 200% !important;
  height: 200% !important;
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0.2) 0%,
    rgba(255, 255, 255, 0.05) 40%,
    transparent 60%
  ) !important;
  transform: rotate(30deg) !important;
  pointer-events: none !important;
}

.novel-title-overlay {
  color: white !important;
  text-align: center !important;
  padding: 10px !important;
  font-weight: bold !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4) !important;
  font-size: 14px !important;
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  background-color: rgba(0, 0, 0, 0.2) !important;
  z-index: 2 !important;
}

/* 技术风格的卡片 */
.tech-card {
  background-color: #fff;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-medium);
  border: 1px solid var(--gray-200);
  overflow: hidden;
}

.tech-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
  border-color: var(--primary-light);
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}

a {
  text-decoration: none;
  color: inherit;
}

/* 响应式布局工具类 */
.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
