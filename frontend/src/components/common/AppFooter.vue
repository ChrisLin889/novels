<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>关于我们</h3>
        <p>科技小说网是一个专注于科技类小说的在线阅读平台，提供丰富的高质量科技小说内容。</p>
      </div>
      
      <div class="footer-section">
        <h3>快速链接</h3>
        <ul>
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/category">分类</router-link></li>
          <li><router-link to="/ranking">排行榜</router-link></li>
          <li><router-link to="/about">关于我们</router-link></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h3>联系我们</h3>
        <ul>
          <li>邮箱: support@tech-novel.xx</li>
          <li>电话: 400-XXX-XXXX</li>
          <li>地址: XX市XX区XX路XX号</li>
        </ul>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; 2025 科技小说网 版权所有 | <a href="/privacy">隐私政策</a> | <a href="/terms">使用条款</a></p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
};
</script>

<style scoped>
.app-footer {
  background-color: #1e293b;
  color: #e2e8f0;
  padding: 40px 0 20px;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  padding: 0 20px;
}

.footer-section {
  flex: 1;
  min-width: 250px;
  margin-bottom: 30px;
}

.footer-section h3 {
  color: #fff;
  font-size: 18px;
  margin-bottom: 15px;
  position: relative;
  padding-bottom: 10px;
}

.footer-section h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 2px;
  background-color: #6366f1;
}

.footer-section p {
  line-height: 1.6;
  color: #cbd5e1;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section ul li {
  margin-bottom: 10px;
}

.footer-section ul li a {
  color: #cbd5e1;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-section ul li a:hover {
  color: #6366f1;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 20px;
}

.footer-bottom p {
  color: #94a3b8;
  font-size: 14px;
}

.footer-bottom a {
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-bottom a:hover {
  color: #6366f1;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
  }
  
  .footer-section {
    margin-bottom: 30px;
  }
}
</style> 