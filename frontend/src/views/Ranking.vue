<template>
  <div class="ranking-page">
    <div class="breadcrumb">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>排行榜</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    
    <div class="container ranking-container">
      <h1 class="page-title">小说排行榜</h1>
      
      <el-tabs v-model="activeTab" @tab-click="handleTabClick" class="ranking-tabs">
        <el-tab-pane v-for="tab in tabs" :key="tab.name" :label="tab.label" :name="tab.name">
          <div class="ranking-content">
            <div class="time-filter">
              <el-radio-group v-model="timeRange" @change="handleTimeChange">
                <el-radio-button label="day">日榜</el-radio-button>
                <el-radio-button label="week">周榜</el-radio-button>
                <el-radio-button label="month">月榜</el-radio-button>
                <el-radio-button label="year">年榜</el-radio-button>
                <el-radio-button label="all">总榜</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="ranking-list">
              <el-skeleton :rows="10" animated v-if="loading" />
              
              <div v-else-if="!rankings || rankings.length === 0" class="no-data">
                <el-empty description="当前排行榜暂无数据" />
              </div>
              
              <el-row v-else :gutter="20" justify="center">
                <el-col v-for="(novel, index) in rankings" :key="novel.id || index" :xs="12" :sm="8" :md="6" :lg="4" :xl="4">
                  <div class="novel-card-wrapper">
                    <div class="rank-number" :class="{'top-rank': index < 3}">{{ index + 1 }}</div>
                    <router-link :to="`/novel/${novel.id}`" class="novel-card">
                      <div class="novel-cover">
                        <img v-if="novel.cover && novel.cover.trim()" :src="novel.cover" :alt="novel.title" @error="handleImageError">
                        <div v-else class="novel-title-overlay">{{ novel.title || '未命名小说' }}</div>
                      </div>
                      <div class="novel-info">
                        <h3 class="novel-title">{{ novel.title || '未命名小说' }}</h3>
                        <p class="novel-author">{{ novel.author || '佚名' }}</p>
                        <div class="novel-category">
                          <el-tag size="small">{{ novel.category || '未分类' }}</el-tag>
                          <el-tag size="small" type="info">{{ novel.status === 'ongoing' ? '连载中' : '已完结' }}</el-tag>
                        </div>
                        <div class="novel-stats">
                          <span><el-icon><View /></el-icon> {{ novel.view_count || 0 }}</span>
                          <span><el-icon><Star /></el-icon> {{ novel.collection_count || 0 }}</span>
                          <span><el-icon><GoodsFilled /></el-icon> {{ novel.recommend_count || 0 }}</span>
                        </div>
                      </div>
                    </router-link>
                  </div>
                </el-col>
              </el-row>
              
              <div class="pagination-container" v-if="total > pageSize">
                <el-pagination
                  v-model:current-page="currentPage"
                  :page-size="pageSize"
                  layout="prev, pager, next"
                  :total="total"
                  @current-change="handleCurrentChange"
                  hide-on-single-page
                />
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <pre v-if="debug">{{ rankings }}</pre>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { View, Star, GoodsFilled } from '@element-plus/icons-vue';
import { getRankings } from '@/api/novel';

export default {
  name: 'Ranking',
  components: {
    View,
    Star,
    GoodsFilled
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    
    const tabs = ref([
      { name: 'views', label: '阅读榜' },
      { name: 'favorites', label: '收藏榜' },
      { name: 'recommends', label: '推荐榜' },
      { name: 'comments', label: '评论榜' }
    ]);
    
    const categories = ref([
      { id: 1, name: '玄幻' },
      { id: 2, name: '奇幻' },
      { id: 3, name: '武侠' },
      { id: 4, name: '仙侠' },
      { id: 5, name: '都市' },
      { id: 6, name: '现实' },
      { id: 7, name: '军事' },
      { id: 8, name: '历史' },
      { id: 9, name: '游戏' },
      { id: 10, name: '科幻' }
    ]);
    
    // 获取分类名称
    const getCategoryName = (categoryId) => {
      const category = categories.value.find(c => c.id === categoryId);
      return category ? category.name : '未分类';
    };
    
    const rankings = ref([]);
    const total = ref(0);
    const loading = ref(false);
    
    // 从URL查询参数中获取筛选条件，如果没有则使用默认值
    const activeTab = ref(route.query.type || 'views');
    const timeRange = ref(route.query.time || 'week');
    const currentPage = ref(parseInt(route.query.page || 1));
    const pageSize = ref(20);
    
    const debug = ref(false);
    
    // 获取排行榜数据
    const fetchRankings = async () => {
      loading.value = true;
      rankings.value = [];
      
      try {
        const params = {
          type: activeTab.value,
          time: timeRange.value,
          page: currentPage.value,
          per_page: pageSize.value
        };
        
        console.log('获取排行榜数据，参数:', params);
        const res = await getRankings(params);
        console.log('排行榜API响应:', res);
        
        if (res && res.novels && Array.isArray(res.novels)) {
          rankings.value = res.novels;
          total.value = res.total || 0;
          console.log(`成功获取${rankings.value.length}条排行榜数据，总计${total.value}条`);
        } else if (res && Array.isArray(res)) {
          rankings.value = res;
          total.value = res.length;
          console.log(`成功获取${rankings.value.length}条排行榜数据（直接数组）`);
        } else {
          console.warn('排行榜返回数据格式异常:', res);
          rankings.value = [];
          total.value = 0;
        }
      } catch (error) {
        console.error('获取排行榜数据失败:', error);
        rankings.value = [];
        total.value = 0;
      } finally {
        loading.value = false;
      }
    };
    
    // 更新URL查询参数
    const updateUrl = () => {
      router.push({
        path: '/ranking',
        query: {
          type: activeTab.value,
          time: timeRange.value,
          page: currentPage.value
        }
      });
    };
    
    // Tab切换处理
    const handleTabClick = () => {
      currentPage.value = 1;
    };
    
    // 时间范围切换
    const handleTimeChange = () => {
      currentPage.value = 1;
    };
    
    // 分页处理
    const handleCurrentChange = (val) => {
      currentPage.value = val;
    };
    
    // 处理图片加载错误
    const handleImageError = (e) => {
      // 设置默认图片
      e.target.src = "https://images.unsplash.com/photo-1610882648335-ced8fc8fa6b6?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60";
      e.target.onerror = null; // 防止循环触发错误
    };
    
    // 监听筛选条件变化，更新URL并重新获取数据
    watch([activeTab, timeRange, currentPage], () => {
      updateUrl();
      fetchRankings();
    });
    
    onMounted(() => {
      console.log('排行榜页面加载，模式：', activeTab.value, timeRange.value);
      fetchRankings();
    });
    
    return {
      tabs,
      rankings,
      activeTab,
      timeRange,
      currentPage,
      pageSize,
      total,
      loading,
      handleTabClick,
      handleTimeChange,
      handleCurrentChange,
      getCategoryName,
      handleImageError,
      debug
    };
  }
};
</script>

<style scoped>
.ranking-page {
  background-color: #f5f7fa;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(216, 241, 230, 0.46) 0%, rgba(233, 226, 226, 0.28) 50.3%, rgba(121, 140, 162, 0.37) 100.2%),
    linear-gradient(to right, rgba(92, 223, 255, 0.1) 0%, rgba(174, 227, 238, 0.1) 50%, rgba(158, 236, 217, 0.2) 100%);
  min-height: 100vh;
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumb {
  margin-bottom: 20px;
  max-width: 1200px;
  margin: 0 auto 20px;
  padding: 0 20px;
}

.ranking-container {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  padding: 30px;
  margin-bottom: 40px;
}

.page-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #303133;
  position: relative;
  margin-bottom: 25px;
  text-align: center;
  display: inline-block;
  background: linear-gradient(120deg, #409EFF, #53a8ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  padding: 0 10px;
  letter-spacing: 1px;
  left: 50%;
  transform: translateX(-50%);
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, rgba(64, 158, 255, 0.2), rgba(64, 158, 255, 0.8), rgba(64, 158, 255, 0.2));
  border-radius: 2px;
}

.time-filter {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.ranking-content {
  margin-top: 20px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(31, 38, 135, 0.07);
}

.ranking-list {
  margin-top: 20px;
}

.novel-card-wrapper {
  height: 100%;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 8px;
  position: relative;
}

.novel-card-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(64, 158, 255, 0.15);
  background: rgba(255, 255, 255, 0.8);
}

.rank-number {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.top-rank {
  background: linear-gradient(135deg, #f5515f, #ff9f43);
  box-shadow: 0 2px 8px rgba(245, 81, 95, 0.4);
}

.novel-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  text-decoration: none;
  color: inherit;
}

.novel-cover {
  height: 180px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 10px;
  position: relative;
}

.novel-cover img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.novel-default-cover {
  background: linear-gradient(135deg, #3f51b5 0%, #00bcd4 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.novel-card:hover .novel-cover img {
  transform: scale(1.05);
}

.novel-title-overlay {
  color: white;
  text-align: center;
  padding: 10px;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
  font-size: 14px;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
  background: linear-gradient(135deg, #3f51b5 0%, #00bcd4 100%);
}

.novel-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 5px;
}

.novel-title {
  font-size: 16px;
  margin: 0 0 8px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 600;
}

.novel-author {
  color: #666;
  font-size: 14px;
  margin: 0 0 8px;
}

.novel-category {
  margin-bottom: 10px;
}

.novel-category .el-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.novel-stats {
  display: flex;
  justify-content: space-between;
  color: #999;
  font-size: 12px;
  margin-top: auto;
}

.novel-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

:deep(.el-pagination .el-pagination__sizes .el-input .el-input__inner) {
  font-size: 13px;
  border-radius: 20px;
}

:deep(.el-pagination .btn-prev),
:deep(.el-pagination .btn-next) {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  transition: all 0.3s ease;
}

:deep(.el-pagination .el-pager li) {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 4px;
  transition: all 0.3s ease;
}

:deep(.el-pagination .el-pager li.active) {
  background-color: #409EFF;
  color: white;
}

:deep(.el-tabs__nav-wrap::after) {
  background-color: rgba(73, 80, 87, 0.1);
}

:deep(.el-tabs__active-bar) {
  background: linear-gradient(90deg, #409EFF, #53a8ff);
}

:deep(.el-tabs__item) {
  color: #606266;
  transition: all 0.3s;
}

:deep(.el-tabs__item.is-active) {
  color: #409EFF;
  font-weight: bold;
}

:deep(.el-tabs__item:hover) {
  color: #409EFF;
}

.no-data {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 15px;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .novel-cover {
    height: 150px;
  }
  
  .time-filter {
    flex-wrap: wrap;
  }
}
</style> 