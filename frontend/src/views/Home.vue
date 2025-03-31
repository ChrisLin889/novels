<template>
  <div class="home">
    <!-- Banner carousel -->
    <div class="banner-container">
      <el-carousel 
        height="400px"
        :interval="5000"
        :autoplay="true"
        arrow="hover"
        indicator-position="outside"
        :initial-index="0"
        trigger="hover"
      >
        <el-carousel-item v-for="(banner, index) in banners" :key="index" class="carousel-item">
          <div 
            class="banner-item" 
            v-preload-image="banner.image" 
            :style="{
              backgroundImage: banner.loaded ? `url(${banner.image})` : 'linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.1))'
            }"
          >
            <div class="banner-content">
              <h2>{{ banner.title }}</h2>
              <p>{{ banner.description }}</p>
              <el-button type="primary" @click="navigateToNovel(banner.id)" round>立即阅读</el-button>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <div class="container page-container">
      <!-- Novel categories section -->
      <section class="section categories-section">
        <h2 class="section-title">作品分类</h2>
        <div class="categories">
          <el-button 
            v-for="category in categories" 
            :key="category.id" 
            size="large"
            @click="navigateToCategory(category.id)"
            class="category-button"
          >
            {{ category.name }}
          </el-button>
        </div>
      </section>

      <!-- Popular novels section -->
      <section class="section popular-section">
        <div class="section-header">
          <h2 class="section-title">热门小说</h2>
        </div>

        <el-row :gutter="20" justify="center">
          <el-col v-for="novel in popularNovels" :key="novel.id" :xs="12" :sm="8" :md="6" :lg="4" :xl="4">
            <div class="novel-card-wrapper">
              <NovelCard :novel="novel" />
            </div>
          </el-col>
        </el-row>
      </section>

      <!-- New releases section -->
      <section class="section new-releases-section">
        <div class="section-header">
          <h2 class="section-title">最新更新</h2>
        </div>

        <el-row :gutter="20" justify="center">
          <el-col v-for="novel in newReleases" :key="novel.id" :xs="12" :sm="8" :md="6" :lg="4" :xl="4">
            <div class="novel-card-wrapper">
              <NovelCard :novel="novel" />
            </div>
          </el-col>
        </el-row>
      </section>

      <!-- User recommendations section -->
      <section class="section recommendations-section" v-if="isLoggedIn && recommendations.length > 0">
        <div class="section-header">
          <h2 class="section-title">专属推荐</h2>
        </div>

        <el-row :gutter="20" justify="center">
          <el-col v-for="novel in recommendations" :key="novel.id" :xs="12" :sm="8" :md="6" :lg="4" :xl="4">
            <div class="novel-card-wrapper">
              <NovelCard :novel="novel" />
            </div>
          </el-col>
        </el-row>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import NovelCard from '@/components/novel/NovelCard.vue';
import { getNovelList } from '@/api/novel';

// 图片预加载指令
const vPreloadImage = {
  beforeMount(el, binding) {
    // 立即设置默认背景，防止初始空白
    el.style.backgroundImage = `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.1))`;
    el.style.opacity = '1';
    el.style.transition = 'opacity 0.5s';
    
    const img = new Image();
    img.src = binding.value;
    img.onload = () => {
      el.style.backgroundImage = `url(${binding.value})`;
    };
    img.onerror = () => {
      // 图片加载失败时使用渐变背景
      el.style.backgroundImage = `linear-gradient(to right, #3a7bd5, #00d2ff)`;
    };
  }
};

export default {
  name: 'Home',
  components: {
    NovelCard
  },
  directives: {
    preloadImage: vPreloadImage
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    
    // User authentication status
    const isLoggedIn = computed(() => store.getters['user/isAuthenticated']);
    
    // Banner data with loaded flag
    const banners = ref([
      {
        id: 1,
        title: '幻境奇缘',
        description: '穿越异界，探索魔法与冒险的史诗旅程',
        image: 'https://images.unsplash.com/photo-1518132746889-495f577c5018?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        loaded: false
      },
      {
        id: 2,
        title: '都市之巅',
        description: '商战职场，步步为营的都市传奇',
        image: 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        loaded: false
      },
      {
        id: 3,
        title: '未来战场',
        description: '星际争霸，科技与人性的终极对决',
        image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        loaded: false
      }
    ]);
    
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
    
    // Novel list data
    const popularNovels = ref([]);
    const newReleases = ref([]);
    const recommendations = ref([]);
    
    // Mock data for demo purposes
    const mockPopularNovels = [
      {
        id: 1,
        title: '修真世界',
        author: '方想',
        category: '玄幻奇幻',
        status: 'ongoing',
        cover: 'https://images.unsplash.com/photo-1516373947948-93b232e9b153?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
        view_count: 120000,
        word_count: 5000000
      },
      // Add more mock data as needed
    ];
    
    // 预加载所有轮播图片
    const preloadBannerImages = () => {
      banners.value.forEach((banner, index) => {
        const img = new Image();
        img.src = banner.image;
        img.onload = () => {
          banners.value[index].loaded = true;
        };
      });
    };
    
    // Fetch novel data from API
    const fetchNovels = async () => {
      try {
        // Get popular novels (sorted by view count)
        const popularResponse = await getNovelList({ 
          sort_by: 'view_count', 
          page: 1, 
          per_page: 6 
        });
        popularNovels.value = popularResponse.novels || [];
        
        // 使用热门小说作为轮播内容
        if (popularNovels.value && popularNovels.value.length > 0) {
          // 选择最多3本热门小说用于轮播
          const topNovels = popularNovels.value.slice(0, 3);
          banners.value = topNovels.map(novel => ({
            id: novel.id,
            title: novel.title,
            description: novel.intro || '点击查看详情',
            image: novel.cover || 'https://images.unsplash.com/photo-1518132746889-495f577c5018?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
            loaded: false
          }));
          
          // 更新banner后预加载图片
          preloadBannerImages();
        }
        
        // Get latest novels
        const newResponse = await getNovelList({ 
          sort_by: 'updated_at', 
          page: 1, 
          per_page: 6 
        });
        newReleases.value = newResponse.novels || [];
        
        // Get recommendations for logged in users
        if (isLoggedIn.value) {
          // For now, just use popular novels as recommendations
          // In the future, a real recommendation API can be implemented
          recommendations.value = popularNovels.value;
        }
      } catch (error) {
        console.error('Failed to fetch novels:', error);
        // Fallback to mock data in case of errors
        popularNovels.value = mockPopularNovels;
        newReleases.value = mockPopularNovels;
        
        // 确保预加载轮播图片
        preloadBannerImages();
      }
    };
    
    // Navigation methods
    const navigateToNovel = (id) => {
      router.push(`/novel/${id}`);
    };
    
    const navigateToCategory = (categoryId) => {
      router.push({
        path: '/category',
        query: { id: categoryId }
      });
    };
    
    // Lifecycle hooks
    onMounted(() => {
      fetchNovels();
      preloadBannerImages(); // 立即尝试预加载默认轮播图片
    });
    
    return {
      banners,
      categories,
      popularNovels,
      newReleases,
      recommendations,
      isLoggedIn,
      navigateToNovel,
      navigateToCategory
    };
  }
};
</script>

<style scoped>
.home {
  background-color: #f5f7fa;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(216, 241, 230, 0.46) 0%, rgba(233, 226, 226, 0.28) 50.3%, rgba(121, 140, 162, 0.37) 100.2%),
    linear-gradient(to right, rgba(92, 223, 255, 0.1) 0%, rgba(174, 227, 238, 0.1) 50%, rgba(158, 236, 217, 0.2) 100%);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.home::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.5), transparent);
  z-index: 1;
}

.banner-container {
  width: 100%;
  margin-bottom: 40px;
  padding: 20px 0;
  overflow: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-container {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
  padding: 30px;
  margin-bottom: 40px;
}

/* 自定义轮播样式 */
:deep(.el-carousel__container) {
  border-radius: 16px;
  overflow: hidden;
  max-width: 1200px;
  margin: 0 auto;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
  background-color: rgba(0, 0, 0, 0.1) !important;
}

:deep(.el-carousel__item) {
  opacity: 1;
  transition: opacity 0.8s ease, transform 0.8s ease;
}

:deep(.el-carousel__item.is-animating) {
  transition: opacity 0.8s ease, transform 0.8s ease;
}

:deep(.el-carousel__indicators) {
  bottom: -10px;
}

:deep(.el-carousel__indicator) {
  padding: 8px 4px;
}

:deep(.el-carousel__button) {
  width: 30px;
  height: 4px;
  border-radius: 2px;
  opacity: 0.3;
  transition: all 0.3s ease;
  background-color: rgba(0, 0, 0, 0.5);
}

:deep(.el-carousel__indicator.is-active .el-carousel__button) {
  opacity: 1;
  width: 40px;
  background-color: rgba(64, 158, 255, 0.8);
}

:deep(.el-carousel__arrow) {
  background-color: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  color: #333;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

:deep(.el-carousel:hover .el-carousel__arrow) {
  opacity: 0.8;
}

:deep(.el-carousel__mask) {
  background-color: transparent !important;
}

.carousel-item {
  transition: all 0.8s cubic-bezier(0.25, 1, 0.5, 1);
  opacity: 1;
  background-color: transparent !important;
}

.banner-item {
  height: 100%;
  opacity: 1;
  transition: opacity 0.8s ease, transform 0.8s ease;
  background-position: center center;
  background-size: cover;
  background-color: transparent !important;
  display: flex;
  align-items: center;
  position: relative;
  border-radius: 16px;
}

/* 确保所有轮播相关元素背景透明 */
:deep(.el-carousel), :deep(.el-carousel__container), :deep(.el-carousel__item) {
  background-color: transparent !important;
}

.banner-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to right, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.25) 50%, rgba(0,0,0,0.1) 100%);
  border-radius: 16px;
  transition: opacity 0.6s ease;
  z-index: 1;
}

/* 进入和离开的动画 */
:deep(.el-carousel__item--card) {
  z-index: 1;
  background-color: transparent !important;
}

:deep(.el-carousel__item--card.is-active) {
  z-index: 2;
}

:deep(.el-carousel__item--card.is-in-stage) {
  transition: transform 0.6s ease, opacity 0.6s ease;
  background-color: transparent !important;
}

/* 覆盖Element Plus轮播的默认白色闪烁效果 */
:deep(.el-carousel__container .el-carousel__item) {
  background-color: transparent !important;
}

:deep(.el-carousel__item:not(.is-active)) {
  opacity: 0.8;
  filter: brightness(0.8);
}

.banner-content {
  position: relative;
  z-index: 10;
  color: white;
  max-width: 600px;
  padding: 0 60px;
  transform: translateY(0);
  opacity: 1;
  transition: transform 0.6s ease, opacity 0.6s ease;
}

.banner-content h2 {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 10px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  transform: translateY(0);
  transition: transform 0.7s ease;
}

.banner-content p {
  font-size: 1.2rem;
  margin-bottom: 20px;
  font-weight: 300;
  opacity: 0.9;
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
  transform: translateY(0);
  transition: transform 0.7s ease 0.1s;
}

.banner-content .el-button {
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.4);
  transform: translateY(0);
  padding: 12px 24px;
  font-size: 16px;
}

/* 响应式样式调整 */
@media (max-width: 768px) {
  .banner-content h2 {
    font-size: 1.8rem;
  }
  
  .banner-content p {
    font-size: 1rem;
  }
  
  .section-title {
    font-size: 1.2rem;
  }
  
  :deep(.el-carousel__container) {
    border-radius: 10px;
  }
  
  .banner-content {
    padding: 0 30px;
  }
}

.section {
  margin-bottom: 40px;
  text-align: center;
  padding: 15px;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 15px rgba(31, 38, 135, 0.07);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.section:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(31, 38, 135, 0.1);
}

.section-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #303133;
  position: relative;
  margin: 0;
  display: inline-block;
  background: linear-gradient(120deg, #409EFF, #53a8ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  padding: 0 10px;
  letter-spacing: 1px;
}

.section-title::before {
  content: none;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 50%;
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, rgba(64, 158, 255, 0.2), rgba(64, 158, 255, 0.8), rgba(64, 158, 255, 0.2));
  transform: translateX(-50%);
  border-radius: 2px;
}

.view-more {
  color: #909399;
  font-size: 14px;
}

.view-more:hover {
  color: #409EFF;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
  justify-content: center;
}

.category-button {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(209, 213, 219, 0.5);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.category-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
  background: rgba(64, 158, 255, 0.1);
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
}

.novel-card-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(64, 158, 255, 0.15);
  background: rgba(255, 255, 255, 0.8);
}
</style> 