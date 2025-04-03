<template>
  <div class="dashboard-container">
    <h1 class="page-title">管理员仪表盘</h1>
    
    <el-row :gutter="20" v-loading="loading">
      <!-- 用户统计 -->
      <el-col :xs="24" :sm="12" :md="8" :lg="8">
        <el-card class="dashboard-card">
          <template #header>
            <div class="card-header">
              <span>用户统计</span>
              <el-tooltip content="用户相关的统计数据" placement="top">
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <div class="stat-list">
            <div class="stat-item">
              <div class="stat-label">总用户数</div>
              <div class="stat-value">{{ userStats.total_users || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">今日新增用户</div>
              <div class="stat-value">{{ userStats.new_users_today || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">今日活跃用户</div>
              <div class="stat-value">{{ userStats.active_users_today || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">被禁用户数</div>
              <div class="stat-value">{{ userStats.banned_users || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 内容统计 -->
      <el-col :xs="24" :sm="12" :md="8" :lg="8">
        <el-card class="dashboard-card">
          <template #header>
            <div class="card-header">
              <span>内容统计</span>
              <el-tooltip content="小说和章节相关的统计数据" placement="top">
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <div class="stat-list">
            <div class="stat-item">
              <div class="stat-label">小说总数</div>
              <div class="stat-value">{{ contentStats.total_novels || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">章节总数</div>
              <div class="stat-value">{{ contentStats.total_chapters || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">待审核内容</div>
              <div class="stat-value">{{ contentStats.pending_moderation || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">被拒绝内容</div>
              <div class="stat-value">{{ contentStats.rejected_content || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 活动统计 -->
      <el-col :xs="24" :sm="12" :md="8" :lg="8">
        <el-card class="dashboard-card">
          <template #header>
            <div class="card-header">
              <span>活动统计</span>
              <el-tooltip content="用户互动相关的统计数据" placement="top">
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <div class="stat-list">
            <div class="stat-item">
              <div class="stat-label">今日评论数</div>
              <div class="stat-value">{{ activityStats.comments_today || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">今日阅读量</div>
              <div class="stat-value">{{ activityStats.readings_today || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">今日打赏数</div>
              <div class="stat-value">{{ activityStats.tips_today || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快捷链接 -->
    <el-card class="quick-links-card">
      <template #header>
        <div class="card-header">
          <span>快捷操作</span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <router-link to="/admin/users">
            <el-card class="quick-link-item" shadow="hover">
              <el-icon :size="32"><User /></el-icon>
              <div class="link-title">用户管理</div>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <router-link to="/admin/content">
            <el-card class="quick-link-item" shadow="hover">
              <el-icon :size="32"><Reading /></el-icon>
              <div class="link-title">小说审核</div>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <router-link to="/admin/sensitive-words">
            <el-card class="quick-link-item" shadow="hover">
              <el-icon :size="32"><Warning /></el-icon>
              <div class="link-title">敏感词管理</div>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <router-link to="/admin/crawled-novels">
            <el-card class="quick-link-item" shadow="hover">
              <el-icon :size="32"><Download /></el-icon>
              <div class="link-title">爬取小说管理</div>
            </el-card>
          </router-link>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';
import { InfoFilled, User, Reading, Warning, Download } from '@element-plus/icons-vue';

export default {
  name: 'AdminDashboard',
  components: {
    InfoFilled,
    User,
    Reading,
    Warning,
    Download
  },
  setup() {
    const store = useStore();
    
    // 计算属性
    const loading = computed(() => store.getters['admin/isLoading']('dashboard'));
    const dashboard = computed(() => store.getters['admin/dashboardData']);
    const userStats = computed(() => dashboard.value.userStats);
    const contentStats = computed(() => dashboard.value.contentStats);
    const activityStats = computed(() => dashboard.value.activityStats);
    
    // 获取仪表盘数据
    onMounted(async () => {
      try {
        await store.dispatch('admin/fetchDashboard');
      } catch (error) {
        console.error('获取仪表盘数据失败:', error);
        ElMessage.error('获取仪表盘数据失败');
      }
    });
    
    return {
      loading,
      userStats,
      contentStats,
      activityStats
    };
  }
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px 0;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.dashboard-card {
  margin-bottom: 20px;
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-list {
  display: flex;
  flex-direction: column;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  color: #606266;
}

.stat-value {
  font-weight: bold;
  color: #409eff;
}

.quick-links-card {
  margin-top: 20px;
}

.quick-link-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  cursor: pointer;
  margin-bottom: 15px;
  transition: all 0.3s;
  color: #606266;
}

.quick-link-item:hover {
  color: #409eff;
  transform: translateY(-5px);
}

.link-title {
  margin-top: 10px;
  font-size: 14px;
}

a {
  text-decoration: none;
}
</style> 