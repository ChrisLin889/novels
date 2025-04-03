<template>
  <div class="user-actions-container">
    <h1 class="page-title">用户操作记录</h1>
    
    <!-- 搜索和筛选 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="用户ID">
          <el-input v-model="filterForm.userId" placeholder="输入用户ID" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 操作记录列表 -->
    <el-card class="list-card" v-loading="loading">
      <el-table :data="userActions" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="user_id" label="用户ID" width="100"></el-table-column>
        <el-table-column prop="username" label="用户名" width="120"></el-table-column>
        <el-table-column prop="action_type" label="操作类型" width="120">
          <template #default="scope">
            <el-tag :type="getActionTypeTag(scope.row.action_type)">
              {{ getActionTypeText(scope.row.action_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="action_details" label="操作详情">
          <template #default="scope">
            <div v-if="scope.row.action_details">
              <div v-for="(value, key) in parseActionDetails(scope.row.action_details)" :key="key">
                <strong>{{ formatKey(key) }}:</strong> {{ value }}
              </div>
            </div>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="ip_address" label="IP地址" width="140"></el-table-column>
        <el-table-column prop="created_at" label="操作时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';

export default {
  name: 'AdminUserActions',
  setup() {
    const store = useStore();
    const route = useRoute();
    
    // 数据
    const loading = computed(() => store.getters['admin/isLoading']('userActions'));
    const userActions = computed(() => store.getters['admin/userActionsList']);
    const pagination = computed(() => store.getters['admin/userActionsPagination']);
    const total = computed(() => pagination.value.total);
    
    const currentPage = ref(1);
    const pageSize = ref(20);
    
    // 筛选表单
    const filterForm = reactive({
      userId: ''
    });
    
    // 监听路由参数变化
    watch(() => route.query, (query) => {
      if (query.user_id) {
        filterForm.userId = query.user_id;
        loadUserActions();
      }
    }, { immediate: true });
    
    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleString();
    };
    
    // 获取操作类型标签样式
    const getActionTypeTag = (type) => {
      const types = {
        'login': 'info',
        'register': 'success',
        'comment': 'warning',
        'edit': 'primary',
        'delete': 'danger',
        'report': 'danger',
        'rate': 'info',
        'bookmark': 'success',
        'admin': 'danger'
      };
      return types[type] || 'info';
    };
    
    // 获取操作类型中文文本
    const getActionTypeText = (type) => {
      const texts = {
        'login': '登录',
        'register': '注册',
        'comment': '评论',
        'edit': '编辑',
        'delete': '删除',
        'report': '举报',
        'rate': '评分',
        'bookmark': '收藏',
        'admin': '管理操作'
      };
      return texts[type] || type;
    };
    
    // 解析操作详情JSON
    const parseActionDetails = (details) => {
      if (!details) return {};
      try {
        return typeof details === 'object' ? details : JSON.parse(details);
      } catch (e) {
        return { details };
      }
    };
    
    // 格式化键名
    const formatKey = (key) => {
      const keyMap = {
        'target_id': '目标ID',
        'target_type': '目标类型',
        'content': '内容',
        'before': '修改前',
        'after': '修改后',
        'reason': '原因',
        'score': '分数'
      };
      return keyMap[key] || key;
    };
    
    // 加载用户操作记录
    const loadUserActions = async () => {
      try {
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        };
        
        if (filterForm.userId) {
          params.user_id = filterForm.userId;
        }
        
        await store.dispatch('admin/fetchUserActions', params);
      } catch (error) {
        console.error('获取用户操作记录失败:', error);
        ElMessage.error('获取用户操作记录失败');
      }
    };
    
    // 初始化
    onMounted(() => {
      if (!route.query.user_id) {
        loadUserActions();
      }
    });
    
    // 处理筛选
    const handleFilter = () => {
      currentPage.value = 1;
      loadUserActions();
    };
    
    // 重置筛选
    const resetFilter = () => {
      filterForm.userId = '';
      currentPage.value = 1;
      loadUserActions();
    };
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size;
      loadUserActions();
    };
    
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      loadUserActions();
    };
    
    return {
      loading,
      userActions,
      total,
      currentPage,
      pageSize,
      filterForm,
      formatDate,
      getActionTypeTag,
      getActionTypeText,
      parseActionDetails,
      formatKey,
      handleFilter,
      resetFilter,
      handleSizeChange,
      handleCurrentChange
    };
  }
};
</script>

<style scoped>
.user-actions-container {
  padding: 20px 0;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  align-items: center;
}

.list-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 