<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-logo">
          <h2>小说网站</h2>
          <p>探索无限阅读世界</p>
        </div>
        
        <div class="footer-links">
          <div class="links-section">
            <h3>关于我们</h3>
            <ul>
              <li><a href="#">网站介绍</a></li>
              <li><a href="#">联系我们</a></li>
              <li><a href="#">加入我们</a></li>
            </ul>
          </div>
          
          <div class="links-section">
            <h3>帮助中心</h3>
            <ul>
              <li><a href="#">阅读指南</a></li>
              <li><a href="#">常见问题</a></li>
              <li><a href="#">意见反馈</a></li>
            </ul>
          </div>
          
          <div class="links-section">
            <h3>友情链接</h3>
            <ul>
              <li><a href="#">作家社区</a></li>
              <li><a href="#">读书论坛</a></li>
              <li><a href="#">合作伙伴</a></li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>© {{ currentYear }} 小说网站 - 毕业设计项目 版权所有</p>
        <p>ICP备案号: 京ICP备XXXXXXXX号</p>
      </div>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue';

export default {
  name: 'Footer',
  setup() {
    const currentYear = computed(() => new Date().getFullYear());
    
    return {
      currentYear
    };
  }
};
</script>

<style scoped>
.footer {
  background-color: #2c3e50;
  color: #fff;
  padding: 40px 0 20px;
  margin-top: 50px;
}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-bottom: 30px;
}

.footer-logo {
  flex: 0 0 300px;
  margin-bottom: 20px;
}

.footer-logo h2 {
  margin: 0 0 10px;
  font-size: 24px;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  flex: 1;
  justify-content: space-around;
}

.links-section {
  margin-bottom: 20px;
  min-width: 120px;
}

.links-section h3 {
  margin-bottom: 15px;
  font-size: 18px;
  font-weight: bold;
}

.links-section ul {
  list-style: none;
  padding: 0;
}

.links-section li {
  margin-bottom: 10px;
}

.links-section a {
  color: #ddd;
  text-decoration: none;
  transition: color 0.3s;
}

.links-section a:hover {
  color: #fff;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #aaa;
}

.footer-bottom p {
  margin: 5px 0;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
  }
  
  .footer-logo {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .footer-links {
    justify-content: space-between;
  }
}
</style> 