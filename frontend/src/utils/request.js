import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from '@/router';

// Create axios instance with base URL from environment
const request = axios.create({
  baseURL: '/api', // 改为相对路径，依赖代理配置
  timeout: 15000, // 延长超时时间
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor: add token to headers
request.interceptors.request.use(
  config => {
    console.log('发送请求:', config.url, '参数:', config.params || config.data);
    
    // 不做URL前缀处理，保持一致性
    // 注意：baseURL会自动添加/api前缀，所以使用request时不需要在url中包含/api
    
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
    
    console.error('API响应错误:', error.config?.url, 
      error.response?.data || error.message, 
      error.code || '无错误代码');
    
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
    } else if (error.code === 'ECONNABORTED') {
      // 请求超时
      ElMessage.error('请求超时，请检查网络连接并重试');
    } else if (error.code === 'ERR_NETWORK') {
      // 网络连接错误
      ElMessage.error('无法连接到服务器，请检查网络连接');
    } else {
      // 网络错误等
      ElMessage.error(error.message || '网络错误，请检查您的网络连接');
    }
    
    // 将错误对象向上传递，以便在组件中处理
    return Promise.reject(error);
  }
);

export default request; 