import axios from 'axios';
import router from '@/router';

// Create axios instance with base URL from environment
const request = axios.create({
  baseURL: `${process.env.VUE_APP_API_BASE_URL}/api` || 'http://localhost:5000/api',
  timeout: 5000
});

// Request interceptor: add token to headers
request.interceptors.request.use(
  config => {
    console.log('发送请求:', config.url, '参数:', config.params);
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    console.error('请求出错:', error);
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
    console.error('API错误:', error.config?.url, error.response?.data);
    
    // Handle authentication errors
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
    }
    
    // Return friendly error message from backend if available
    if (error.response && error.response.data && error.response.data.error) {
      return Promise.reject(error.response.data.error);
    }
    
    // Return friendly error message
    return Promise.reject(error.response?.data?.message || '网络错误，请稍后重试');
  }
);

export default request; 