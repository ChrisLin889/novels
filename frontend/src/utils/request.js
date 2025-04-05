import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from '@/router';

// Create axios instance with base URL from environment
const request = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 5000
});

// Request interceptor: add token to headers
request.interceptors.request.use(
  config => {
    console.log('发送请求:', config.url, '参数:', config.params || config.data);
    
    // 确保URL没有重复的/api前缀
    if (config.url.startsWith('/api/')) {
      config.url = config.url.substring(4); // 移除重复的/api前缀
    }
    
    // 重定向author相关请求到novel下的端点
    if (config.url.startsWith('/author/')) {
      config.url = '/novel' + config.url;
      console.log('重定向作家请求到:', config.url);
    }
    
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// Response interceptor: handle common responses
request.interceptors.response.use(
  response => {
    // 记录API响应
    console.log('API响应成功:', response.config.url, response.data);
    
    // Return data directly for successful requests
    return response.data;
  },
  error => {
    // 忽略特定路径的错误
    if (error.config?.url?.includes('/user/check_country')) {
      console.log('忽略 /user/check_country 请求错误');
      return Promise.resolve(null);
    }
    
    console.error('API响应错误:', error.config?.url, error.response?.data || error.message);
    
    // 处理错误响应
    if (error.response) {
      // 服务器返回错误状态码
      const { status, data } = error.response;
      
      if (status === 401) {
        // 未授权，清除 token 并跳转到登录页
        localStorage.removeItem('token');
        router.push('/login');
        ElMessage.error(data?.message || '身份验证失败，请重新登录');
      } else if (status === 400) {
        // 请求参数错误，显示具体错误信息
        const errorMessage = data?.error || data?.message || '请求参数错误';
        ElMessage.error(errorMessage);
      } else if (status === 403) {
        // 权限不足
        ElMessage.error(data?.message || '权限不足，无法执行该操作');
      } else if (status === 404) {
        // 资源不存在
        ElMessage.error(data?.message || '请求的资源不存在');
      } else if (status >= 500) {
        // 服务器错误
        ElMessage.error('服务器错误，请稍后再试');
      } else {
        // 其他错误
        ElMessage.error(data?.message || '请求失败');
      }
    } else {
      // 网络错误等
      ElMessage.error(error.message || '网络错误，请检查您的网络连接');
    }
    
    // 将错误对象向上传递，以便在组件中处理
    return Promise.reject(error);
  }
);

export default request; 