import axios from 'axios'
import { Message, MessageBox } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// 创建axios实例
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url 基础地址，会和url拼接
  // withCredentials: true, // 跨域请求时发送 cookies
  timeout: 5000 // 请求超时时间
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 发送请求前的处理

    if (store.getters.token) {
      // 如果存在token，则添加到请求头中
      config.headers['Authorization'] = `Bearer ${getToken()}`
    }
    return config
  },
  error => {
    // 请求错误处理
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  /**
   * 如果要获取http信息（例如headers或status）
   * 就返回 response => response
  */

  /**
   * 通过判断状态码确定返回
   */
  response => {
    const res = response.data

    // 如果状态码不是200，则判定为错误
    if (response.status !== 200) {
      Message({
        message: res.message || '服务器响应错误',
        type: 'error',
        duration: 5 * 1000
      })

      // 401: 未登录或token已过期
      if (response.status === 401) {
        // 重新登录
        MessageBox.confirm('您已登出，请重新登录', '登出确认', {
          confirmButtonText: '重新登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          store.dispatch('user/resetToken').then(() => {
            location.reload()
          })
        })
      }
      return Promise.reject(new Error(res.message || '服务器响应错误'))
    } else {
      return response
    }
  },
  error => {
    const { response } = error
    
    // 处理HTTP错误码
    if (response) {
      const { status, data } = response
      
      // 处理401未授权
      if (status === 401) {
        MessageBox.confirm('您的登录已过期，请重新登录', '系统提示', {
          confirmButtonText: '重新登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          store.dispatch('user/resetToken').then(() => {
            location.reload()
          })
        })
      } else {
        // 其他错误
        Message({
          message: data.error || data.message || '请求失败',
          type: 'error',
          duration: 5 * 1000
        })
      }
    } else {
      // 请求没有响应（可能是网络问题）
      Message({
        message: '网络异常，请检查您的网络连接',
        type: 'error',
        duration: 5 * 1000
      })
    }
    
    console.log('err' + error) // for debug
    return Promise.reject(error)
  }
)

export default service 