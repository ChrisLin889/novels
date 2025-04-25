import Vue from 'vue'
import Router from 'vue-router'

// 导入布局组件
import Layout from '@/layout'

Vue.use(Router)

export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },
  // 用户路由
  {
    path: '/novels',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Novels',
        component: () => import('@/views/novels/index'),
        meta: { title: '小说列表', icon: 'book' }
      }
    ]
  },
  {
    path: '/novel',
    component: Layout,
    hidden: true,
    children: [
      {
        path: ':id',
        name: 'NovelDetail',
        component: () => import('@/views/novels/detail'),
        meta: { title: '小说详情' }
      }
    ]
  },
  {
    path: '/chapter',
    component: Layout,
    hidden: true,
    children: [
      {
        path: ':id',
        name: 'ChapterDetail',
        component: () => import('@/views/chapters/detail'),
        meta: { title: '章节阅读' }
      }
    ]
  },
  // 管理员路由
  {
    path: '/admin',
    component: Layout,
    redirect: '/admin/dashboard',
    meta: { title: '管理后台', icon: 'dashboard', roles: ['admin'] },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/dashboard'),
        meta: { title: '管理首页', icon: 'dashboard', roles: ['admin'] }
      },
      {
        path: 'novels',
        name: 'NovelManagement',
        component: () => import('@/views/admin/NovelManagement'),
        meta: { title: '小说管理', icon: 'book', roles: ['admin'] }
      },
      {
        path: 'chapters',
        name: 'ChapterManagement',
        component: () => import('@/views/admin/ChapterManagement'),
        meta: { title: '章节管理', icon: 'edit', roles: ['admin'] }
      },
      {
        path: 'comments',
        name: 'CommentManagement',
        component: () => import('@/views/admin/CommentManagement'),
        meta: { title: '评论管理', icon: 'message', roles: ['admin'] }
      },
      {
        path: 'recycle-bin',
        name: 'RecycleBin',
        component: () => import('@/views/admin/RecycleBin'),
        meta: { title: '内容回收站', icon: 'delete', roles: ['admin'] }
      }
    ]
  },
  // 404页面
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'history',
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher
}

export default router 