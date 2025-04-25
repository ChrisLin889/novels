/**
 * 格式化日期
 * @param {string|Date} date - 日期对象或ISO日期字符串
 * @param {boolean} showSeconds - 是否显示秒
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date, showSeconds = true) {
  if (!date) return '';
  
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(dateObj.getTime())) {
    return '';
  }
  
  const year = dateObj.getFullYear();
  const month = String(dateObj.getMonth() + 1).padStart(2, '0');
  const day = String(dateObj.getDate()).padStart(2, '0');
  const hours = String(dateObj.getHours()).padStart(2, '0');
  const minutes = String(dateObj.getMinutes()).padStart(2, '0');
  
  if (showSeconds) {
    const seconds = String(dateObj.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  }
  
  return `${year}-${month}-${day} ${hours}:${minutes}`;
}

/**
 * 获取相对时间描述（例如：刚刚、5分钟前、2小时前等）
 * @param {string|Date} date - 日期对象或ISO日期字符串
 * @returns {string} 相对时间描述
 */
export function getRelativeTime(date) {
  if (!date) return '';
  
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(dateObj.getTime())) {
    return '';
  }
  
  const now = new Date();
  const diff = Math.floor((now - dateObj) / 1000); // 差异（秒）
  
  if (diff < 60) {
    return '刚刚';
  } else if (diff < 3600) {
    return `${Math.floor(diff / 60)}分钟前`;
  } else if (diff < 86400) {
    return `${Math.floor(diff / 3600)}小时前`;
  } else if (diff < 2592000) {
    return `${Math.floor(diff / 86400)}天前`;
  } else if (diff < 31536000) {
    return `${Math.floor(diff / 2592000)}个月前`;
  } else {
    return `${Math.floor(diff / 31536000)}年前`;
  }
} 