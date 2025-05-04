/**
 * 图片工具函数
 */

/**
 * 处理封面图片URL，确保正确编码中文字符
 * @param {String} url - 原始封面URL
 * @returns {String} 处理后的URL
 */
export function processCoverUrl(url) {
  if (!url) return '/images/default_cover.jpg';
  
  // 如果已经是完整URL或内部默认路径，则直接返回
  if (url.startsWith('http') || url.startsWith('/images/')) {
    return url;
  }
  
  try {
    // 提取基础路径和文件名
    const lastSlashIndex = url.lastIndexOf('/');
    if (lastSlashIndex === -1) return url;
    
    const basePath = url.substring(0, lastSlashIndex + 1);
    const filename = url.substring(lastSlashIndex + 1);
    
    // 对文件名进行URL编码，确保中文字符可以正确传输
    const encodedFilename = encodeURIComponent(filename);
    
    return `${basePath}${encodedFilename}`;
  } catch (error) {
    console.error('处理封面URL时出错:', error);
    return '/images/default_cover.jpg';
  }
} 