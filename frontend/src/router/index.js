import { createRouter, createWebHistory } from 'vue-router';

// Lazy loading routes for better performance
const Home = () => import('@/views/Home.vue');
const NovelDetail = () => import('@/views/NovelDetail.vue');
const Reader = () => import('@/views/Reader.vue');
const Login = () => import('@/views/Login.vue');
const Register = () => import('@/views/Register.vue');
const UserCenter = () => import('@/views/UserCenter.vue');
const UserProfile = () => import('@/views/UserProfile.vue');
const UserBookshelf = () => import('@/views/UserBookshelf.vue');
const SearchResult = () => import('@/views/SearchResult.vue');
const Category = () => import('@/views/Category.vue');
const Ranking = () => import('@/views/Ranking.vue');

// 互动模块路由
const Messages = () => import('@/views/interaction/Messages.vue');
const UserFollowing = () => import('@/views/interaction/UserFollowing.vue');
const UserFollowers = () => import('@/views/interaction/UserFollowers.vue');
const Conversation = () => import('@/views/interaction/Conversation.vue');
const UserComments = () => import('@/views/UserComments.vue');

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '首页 - 小说网站' }
  },
  {
    path: '/novel/:id',
    name: 'NovelDetail',
    component: NovelDetail,
    meta: { title: '小说详情' }
  },
  {
    path: '/read/:novelId/:chapterId',
    name: 'Reader',
    component: Reader,
    meta: { title: '阅读' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: '注册' }
  },
  {
    path: '/search',
    name: 'SearchResult',
    component: SearchResult,
    meta: { title: '搜索结果' }
  },
  {
    path: '/category',
    name: 'Category',
    component: Category,
    meta: { title: '小说分类' }
  },
  {
    path: '/ranking',
    name: 'Ranking',
    component: Ranking,
    meta: { title: '小说排行榜' }
  },
  {
    path: '/user',
    component: UserCenter,
    meta: { requiresAuth: true, title: '用户中心' },
    children: [
      {
        path: 'profile',
        component: UserProfile,
        name: 'UserProfile',
        meta: { title: '个人资料' }
      },
      {
        path: 'bookshelf',
        component: UserBookshelf,
        name: 'UserBookshelf',
        meta: { title: '我的书架' }
      },
      {
        path: 'messages',
        component: Messages,
        name: 'Messages',
        meta: { title: '我的私信' }
      },
      {
        path: 'conversation/:userId',
        component: Conversation,
        name: 'Conversation',
        meta: { title: '私信对话' }
      },
      {
        path: 'following',
        component: UserFollowing,
        name: 'UserFollowing',
        meta: { title: '我的关注' }
      },
      {
        path: 'followers',
        component: UserFollowers,
        name: 'UserFollowers',
        meta: { title: '我的粉丝' }
      },
      {
        path: 'comments',
        component: UserComments,
        name: 'UserComments',
        meta: { title: '我的评论' }
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Global navigation guard
router.beforeEach((to, from, next) => {
  // Update document title
  if (to.meta.title) {
    if (to.name === 'NovelDetail' && to.params.id) {
      // 如果是小说详情页，添加小说ID到标题中
      document.title = `${to.meta.title} #${to.params.id} - 科技小说网`;
    } else if (to.name === 'Reader' && to.params.novelId && to.params.chapterId) {
      // 如果是阅读页面，添加小说ID和章节ID到标题中
      document.title = `阅读小说 #${to.params.novelId} - 章节 ${to.params.chapterId} - 科技小说网`;
    } else if (to.name === 'Conversation' && to.params.userId) {
      // 如果是私信对话页面
      document.title = `私信对话 - 科技小说网`;
    } else {
      document.title = `${to.meta.title} - 科技小说网`;
    }
  }
  
  // Check auth requirement
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token');
    if (!token) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router; 