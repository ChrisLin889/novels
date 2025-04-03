<template>
  <div class="search-result container page-container">
    <div class="search-header">
      <h2>搜索结果: "{{ keyword }}"</h2>
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
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import NovelCard from '@/components/novel/NovelCard.vue';
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
    const pageSize = ref(20);
    const currentPage = ref(1);
    
    // Fetch search results
    const fetchSearchResults = async () => {
      if (!keyword.value) {
        novels.value = [];
        total.value = 0;
        return;
      }
      
      loading.value = true;
      try {
        const response = await searchNovels({
          q: keyword.value,
          page: currentPage.value,
          per_page: pageSize.value
        });
        
        novels.value = response.results;
        total.value = response.total;
      } catch (error) {
        ElMessage.error('搜索失败，请稍后重试');
      } finally {
        loading.value = false;
      }
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