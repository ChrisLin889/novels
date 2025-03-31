<template>
  <div class="search-result container page-container">
    <div class="search-header">
      <h2>搜索结果: "{{ keyword }}"</h2>
      
      <div class="search-filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="分类">
            <el-select v-model="filters.category" placeholder="全部分类" clearable>
              <el-option
                v-for="item in categories"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="全部状态" clearable>
              <el-option label="连载中" value="ongoing"></el-option>
              <el-option label="已完结" value="completed"></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="applyFilters">筛选</el-button>
            <el-button @click="resetFilters">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="novels.length > 0" class="novels-container">
      <el-row :gutter="20">
        <el-col 
          v-for="novel in novels" 
          :key="novel.id" 
          :xs="12" 
          :sm="8" 
          :md="6" 
          :lg="4" 
          :xl="4"
        >
          <div class="novel-card-wrapper">
            <NovelCard :novel="novel" />
          </div>
        </el-col>
      </el-row>
      
      <div class="pagination-container">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="total"
          :page-size="pageSize"
          :current-page="currentPage"
          @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>
    
    <div v-else class="empty-result">
      <el-empty description="没有找到相关小说，请尝试其他关键词">
        <el-button type="primary" @click="goToHome">返回首页</el-button>
      </el-empty>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import NovelCard from '@/components/novel/NovelCard.vue';
// eslint-disable-next-line no-unused-vars
import { searchNovels } from '@/api/search';
import { ElMessage } from 'element-plus';

export default {
  name: 'SearchResult',
  components: {
    NovelCard
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    const keyword = computed(() => route.query.keyword || '');
    const novels = ref([]);
    const loading = ref(false);
    const total = ref(0);
    const pageSize = ref(12);
    const currentPage = ref(1);
    
    // Categories data
    const categories = ref([
      { id: 'xuanhuan', name: '玄幻奇幻' },
      { id: 'wuxia', name: '武侠仙侠' },
      { id: 'urban', name: '都市现实' },
      { id: 'history', name: '历史军事' },
      { id: 'scifi', name: '科幻灵异' },
      { id: 'game', name: '游戏竞技' },
      { id: 'romance', name: '言情女生' },
      { id: 'other', name: '其他分类' }
    ]);
    
    // Search filters
    const filters = reactive({
      category: '',
      status: '',
      sortBy: 'relevance'
    });
    
    // Fetch search results
    const fetchSearchResults = async () => {
      if (!keyword.value) return;
      
      loading.value = true;
      
      try {
        const params = {
          keyword: keyword.value,
          page: currentPage.value,
          per_page: pageSize.value
        };
        
        // Add filters if selected
        if (filters.category) params.category = filters.category;
        if (filters.status) params.status = filters.status;
        
        // Mock search
        // In real application, uncomment below to call API
        /*
        const response = await searchNovels(params);
        novels.value = response.novels;
        total.value = response.total;
        */
        
        // Mock data for demo
        novels.value = [
          {
            id: 1,
            title: '修真世界',
            author: '方想',
            category: '玄幻奇幻',
            status: 'ongoing',
            cover: 'https://images.unsplash.com/photo-1516373947948-93b232e9b153?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            view_count: 120000,
            word_count: 5000000
          }
        ];
        total.value = 1;
      } catch (error) {
        ElMessage.error('搜索失败，请重试');
        console.error('Search failed:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // Apply search filters
    const applyFilters = () => {
      currentPage.value = 1;
      fetchSearchResults();
    };
    
    // Reset search filters
    const resetFilters = () => {
      Object.keys(filters).forEach(key => {
        filters[key] = '';
      });
      currentPage.value = 1;
      fetchSearchResults();
    };
    
    // Handle page change
    const handlePageChange = (page) => {
      currentPage.value = page;
      fetchSearchResults();
    };
    
    // Navigate to home
    const goToHome = () => {
      router.push('/');
    };
    
    // Watch for keyword changes
    watch(() => route.query.keyword, (newKeyword) => {
      if (newKeyword !== keyword.value) {
        currentPage.value = 1;
        fetchSearchResults();
      }
    });
    
    // Initial fetch
    onMounted(() => {
      fetchSearchResults();
    });
    
    return {
      keyword,
      novels,
      loading,
      total,
      pageSize,
      currentPage,
      categories,
      filters,
      applyFilters,
      resetFilters,
      handlePageChange,
      goToHome
    };
  }
};
</script>

<style scoped>
.search-header {
  margin-bottom: 20px;
}

.search-header h2 {
  margin-bottom: 15px;
}

.search-filters {
  background-color: #fff;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.novels-container {
  margin-bottom: 20px;
}

.novel-card-wrapper {
  height: 100%;
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.loading-container,
.empty-result {
  padding: 40px 0;
}
</style> 