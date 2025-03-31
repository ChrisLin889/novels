<template>
  <div class="category-page">
    <el-breadcrumb class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>小说分类</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="category-container">
      <h1 class="page-title">小说分类</h1>
      
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-label">作品分类:</div>
          <div class="filter-options">
            <el-button 
              v-for="category in categories" 
              :key="category.id"
              :class="{ 'active-filter': selectedCategory === category.id }"
              size="small"
              @click="selectCategory(category.id)"
            >
              {{ category.name }}
            </el-button>
          </div>
        </div>
        
        <div class="filter-row">
          <div class="filter-label">更新状态:</div>
          <div class="filter-options">
            <el-button 
              v-for="status in statusOptions" 
              :key="status.value"
              :class="{ 'active-filter': selectedStatus === status.value }"
              size="small"
              @click="selectStatus(status.value)"
            >
              {{ status.label }}
            </el-button>
          </div>
        </div>
        
        <div class="filter-row">
          <div class="filter-label">排序方式:</div>
          <div class="filter-options">
            <el-button 
              v-for="sort in sortOptions" 
              :key="sort.value"
              :class="{ 'active-filter': selectedSort === sort.value }"
              size="small"
              @click="selectSort(sort.value)"
            >
              {{ sort.label }}
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="novels-section">
        <el-empty v-if="novels.length === 0" description="暂无小说" />
        <div v-else class="novel-list">
          <router-link 
            v-for="novel in novels" 
            :key="novel.id" 
            :to="`/novel/${novel.id}`"
            class="novel-card"
          >
            <div class="novel-cover">
              <img v-if="novel.cover && novel.cover.trim()" :src="novel.cover" :alt="novel.title" @error="handleImageError">
              <div v-else class="novel-title-overlay">{{ novel.title || '未命名小说' }}</div>
            </div>
            <div class="novel-info">
              <h3 class="novel-title">{{ novel.title }}</h3>
              <p class="novel-author">{{ novel.author }}</p>
              <p class="novel-desc">{{ novel.intro }}</p>
              <div class="novel-meta">
                <span><el-icon><View /></el-icon> {{ novel.view_count || 0 }}</span>
                <span><el-icon><Star /></el-icon> {{ novel.collection_count || 0 }}</span>
                <span>{{ novel.status === 'ongoing' ? '连载中' : '已完结' }}</span>
              </div>
            </div>
          </router-link>
        </div>
        
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[12, 24, 36, 48]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { View, Star } from '@element-plus/icons-vue';
import { getNovelsByCategory } from '@/api/novel';

export default {
  name: 'Category',
  components: {
    View,
    Star
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    
    const categories = ref([
      { id: 'all', name: '全部' },
      { id: '玄幻奇幻', name: '玄幻奇幻' },
      { id: '武侠仙侠', name: '武侠仙侠' },
      { id: '都市现实', name: '都市现实' },
      { id: '历史军事', name: '历史军事' },
      { id: '科幻灵异', name: '科幻灵异' },
      { id: '游戏竞技', name: '游戏竞技' },
      { id: '言情女生', name: '言情女生' },
      { id: '其他分类', name: '其他分类' }
    ]);
    
    const statusOptions = ref([
      { value: 'all', label: '全部' },
      { value: 'ongoing', label: '连载中' },
      { value: 'completed', label: '已完结' }
    ]);
    
    const sortOptions = ref([
      { value: 'latest', label: '最近更新' },
      { value: 'hot', label: '人气最高' },
      { value: 'new', label: '最新发布' },
      { value: 'collection', label: '收藏最多' }
    ]);
    
    const novels = ref([]);
    const total = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(12);
    const loading = ref(false);
    
    // 从URL查询参数中获取筛选条件，如果没有则使用默认值
    const selectedCategory = ref(route.query.category || 'all');
    const selectedStatus = ref(route.query.status || 'all');
    const selectedSort = ref(route.query.sort || 'latest');
    
    // 获取小说列表数据
    const fetchNovels = async () => {
      loading.value = true;
      try {
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        };
        
        // 只有当分类不是'all'时才添加category参数
        if (selectedCategory.value !== 'all') {
          params.category = selectedCategory.value;
        }
        
        // 只有当状态不是'all'时才添加status参数
        if (selectedStatus.value !== 'all') {
          params.status = selectedStatus.value;
        }
        
        // 添加排序参数
        if (selectedSort.value) {
          params.sort = selectedSort.value;
        }
        
        const res = await getNovelsByCategory(params);
        novels.value = res.novels || [];
        total.value = res.total || 0;
      } catch (error) {
        console.error('获取小说列表失败', error);
      } finally {
        loading.value = false;
      }
    };
    
    // 监听筛选条件变化，更新URL并重新获取数据
    watch([selectedCategory, selectedStatus, selectedSort, currentPage, pageSize], () => {
      updateUrl();
      fetchNovels();
    });
    
    // 更新URL查询参数
    const updateUrl = () => {
      const query = {};
      
      if (selectedCategory.value !== 'all') {
        query.category = selectedCategory.value;
      }
      
      if (selectedStatus.value !== 'all') {
        query.status = selectedStatus.value;
      }
      
      if (selectedSort.value) {
        query.sort = selectedSort.value;
      }
      
      if (currentPage.value > 1) {
        query.page = currentPage.value;
      }
      
      router.push({
        path: '/category',
        query
      });
    };
    
    // 筛选条件选择方法
    const selectCategory = (id) => {
      selectedCategory.value = id;
      currentPage.value = 1;
    };
    
    const selectStatus = (status) => {
      selectedStatus.value = status;
      currentPage.value = 1;
    };
    
    const selectSort = (sort) => {
      selectedSort.value = sort;
      currentPage.value = 1;
    };
    
    // 分页方法
    const handleSizeChange = (val) => {
      pageSize.value = val;
      currentPage.value = 1;
    };
    
    const handleCurrentChange = (val) => {
      currentPage.value = val;
    };
    
    // 处理图片加载错误
    const handleImageError = (e) => {
      // 设置默认图片
      e.target.src = "https://images.unsplash.com/photo-1610882648335-ced8fc8fa6b6?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60";
      e.target.onerror = null; // 防止循环触发错误
    };
    
    onMounted(() => {
      fetchNovels();
    });
    
    return {
      categories,
      statusOptions,
      sortOptions,
      novels,
      selectedCategory,
      selectedStatus,
      selectedSort,
      total,
      currentPage,
      pageSize,
      loading,
      selectCategory,
      selectStatus,
      selectSort,
      handleSizeChange,
      handleCurrentChange,
      handleImageError
    };
  }
};
</script>

<style scoped>
.category-page {
  background-color: #f5f7fa;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(216, 241, 230, 0.46) 0%, rgba(233, 226, 226, 0.28) 50.3%, rgba(121, 140, 162, 0.37) 100.2%),
    linear-gradient(to right, rgba(92, 223, 255, 0.1) 0%, rgba(174, 227, 238, 0.1) 50%, rgba(158, 236, 217, 0.2) 100%);
  min-height: 100vh;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.breadcrumb {
  margin-bottom: 20px;
}

.category-container {
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
  display: inline-block;
  background: linear-gradient(120deg, #409EFF, #53a8ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  padding: 0 10px;
  letter-spacing: 1px;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100px;
  height: 2px;
  background: linear-gradient(90deg, rgba(64, 158, 255, 0.2), rgba(64, 158, 255, 0.8), rgba(64, 158, 255, 0.2));
  border-radius: 2px;
}

.filter-section {
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 4px 15px rgba(31, 38, 135, 0.07);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.filter-section:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(31, 38, 135, 0.1);
}

.filter-row {
  display: flex;
  margin-bottom: 15px;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.filter-label {
  width: 100px;
  font-weight: bold;
  color: #666;
  line-height: 32px;
}

.filter-options {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.active-filter {
  color: #409EFF !important;
  border-color: #409EFF !important;
  background-color: rgba(64, 158, 255, 0.1) !important;
  font-weight: 500;
}

.el-button {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(209, 213, 219, 0.5);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
  background: rgba(64, 158, 255, 0.1);
}

.novels-section {
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(31, 38, 135, 0.07);
}

.novel-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.novel-card {
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 8px;
  transition: all 0.3s ease;
  height: 100%;
  text-decoration: none;
  color: inherit;
}

.novel-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(64, 158, 255, 0.15);
  background: rgba(255, 255, 255, 0.8);
}

.novel-cover {
  height: 180px;
  overflow: hidden;
  border-radius: 8px;
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

.novel-card:hover .novel-cover img {
  transform: scale(1.05);
}

.novel-info {
  padding: 15px;
  flex: 1;
  display: flex;
  flex-direction: column;
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

.novel-desc {
  color: #999;
  font-size: 13px;
  margin: 0 0 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  flex: 1;
}

.novel-meta {
  display: flex;
  justify-content: space-between;
  color: #999;
  font-size: 12px;
}

.novel-meta span {
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

@media (max-width: 768px) {
  .filter-label {
    width: 80px;
  }
  
  .novel-list {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
  
  .novel-cover {
    height: 150px;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}
</style> 