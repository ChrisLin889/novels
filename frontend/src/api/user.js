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
export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  });
}

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
    url: '/user/change-password',
    method: 'post',
    data
  });
} 