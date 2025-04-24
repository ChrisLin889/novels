import request from '@/utils/request';

/**
 * User registration
 * @param {Object} data - User registration data
 * @returns {Promise}
 */
export function register(data) {
  return request({
    url: '/user/register',
    method: 'post',
    data
  });
}

/**
 * User login
 * @param {Object} data - User login credentials
 * @returns {Promise}
 */
export const login = (data) => {
  console.log('发送登录请求:', data);
  return request({
    url: '/user/login',
    method: 'post',
    data
  }).then(response => {
    console.log('登录原始响应:', response);
    return response;
  }).catch(error => {
    console.error('登录请求失败:', error);
    throw error;
  });
};

/**
 * Get user profile
 * @returns {Promise}
 */
export function getProfile() {
  return request({
    url: '/user/profile',
    method: 'get'
  });
}

/**
 * Update user profile
 * @param {Object} data - User profile data to update
 * @returns {Promise}
 */
export function updateProfile(data) {
  return request({
    url: '/user/profile',
    method: 'put',
    data
  });
}

/**
 * Change user password
 * @param {Object} data - Password change data
 * @returns {Promise}
 */
export function changePassword(data) {
  return request({
    url: '/user/password',
    method: 'put',
    data
  });
}

/**
 * User logout
 * @returns {Promise}
 */
export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  });
}

/**
 * Get user profile (alias function)
 * @returns {Promise}
 */
export function getUserProfile() {
  return request({
    url: '/user/profile',
    method: 'get'
  });
} 