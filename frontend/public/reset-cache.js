// 重置章节评论相关的缓存
(function() {
  // 1. 清除localStorage中可能导致问题的项目
  localStorage.removeItem('current_novel_id');
  
  // 2. 从URL中获取当前小说ID和章节ID
  const path = window.location.pathname;
  const matches = path.match(/\/read\/(\d+)\/(\d+)/);
  
  if (matches && matches[1]) {
    const novelId = matches[1];
    const chapterId = matches[2];
    
    // 3. 重新设置正确的小说ID和章节ID
    console.log('从URL提取并重置小说ID:', novelId, '章节ID:', chapterId);
    localStorage.setItem('current_novel_id', novelId);
    
    // 4. 输出调试信息
    console.log('localStorage已重置');
    console.log('current_novel_id:', localStorage.getItem('current_novel_id'));
  } else {
    console.log('当前页面不是阅读页面，不进行重置');
  }
})(); 