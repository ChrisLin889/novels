<template>
  <div class="about-container">
    <el-card class="about-card">
      <template #header>
        <div class="card-header">
          <h2>关于我们</h2>
        </div>
      </template>
      
      <div class="about-content">
        <div class="about-section">
          <h3>网站简介</h3>
          <p>这是一个专注于提供优质小说阅读体验的网站。我们致力于为用户提供丰富的小说资源，打造舒适的阅读环境。</p>
        </div>
        
        <div class="about-section">
          <h3>我们的特色</h3>
          <ul>
            <li>海量小说资源，持续更新</li>
            <li>简洁清爽的阅读界面</li>
            <li>支持多种阅读模式</li>
            <li>个性化书架管理</li>
            <li>活跃的读者社区</li>
          </ul>
        </div>
        
        <div class="about-section">
          <h3>联系我们</h3>
          <p>如果您有任何问题或建议，欢迎通过以下方式联系我们：</p>
          <p>邮箱：support@novels.com</p>
          <p>客服QQ：123456789</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'About',
  setup() {
    return {};
  }
};
</script>

<style scoped>
.about-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.about-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  color: #303133;
}

.about-content {
  line-height: 1.6;
}

.about-section {
  margin-bottom: 30px;
}

.about-section h3 {
  color: #303133;
  margin-bottom: 15px;
  font-size: 18px;
}

.about-section p {
  color: #606266;
  margin-bottom: 10px;
}

.about-section ul {
  list-style-type: disc;
  padding-left: 20px;
  color: #606266;
}

.about-section li {
  margin-bottom: 8px;
}
</style> 