<template>
  <div class="users-container">
    <h1 class="page-title">用户管理</h1>
    
    <!-- 搜索和筛选 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="角色筛选">
          <el-select v-model="filterForm.role" placeholder="选择角色" clearable>
            <el-option label="普通用户" value="user"></el-option>
            <el-option label="作者" value="author"></el-option>
            <el-option label="管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 用户列表 -->
    <el-card class="list-card" v-loading="loading">
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="username" label="用户名" width="150"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column prop="role" label="角色" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.role === 'admin'" type="danger">管理员</el-tag>
            <el-tag v-else-if="scope.row.role === 'author'" type="warning">作者</el-tag>
            <el-tag v-else type="info">普通用户</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.status === 'active'" type="success">正常</el-tag>
            <el-tag v-else-if="scope.row.status === 'banned'" type="danger">已禁用</el-tag>
            <el-tag v-else type="info">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button
              v-if="scope.row.status === 'active'"
              type="danger"
              size="small"
              @click="handleBan(scope.row)"
            >
              禁用
            </el-button>
            <el-button
              v-else-if="scope.row.status === 'banned'"
              type="success"
              size="small"
              @click="handleUnban(scope.row)"
            >
              解禁
            </el-button>
            <el-button
              type="primary"
              size="small"
              @click="viewUserActions(scope.row.id)"
            >
              操作记录
            </el-button>
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
    
    <!-- 禁用用户对话框 -->
    <el-dialog v-model="banDialogVisible" title="禁用用户" width="500px">
      <el-form :model="banForm" label-width="100px">
        <el-form-item label="用户名">
          <span>{{ selectedUser?.username }}</span>
        </el-form-item>
        <el-form-item label="禁用原因" required>
          <el-input v-model="banForm.reason" type="textarea" rows="3" placeholder="请输入禁用原因"></el-input>
        </el-form-item>
        <el-form-item label="禁用时长">
          <el-radio-group v-model="banForm.permanent">
            <el-radio :label="false">临时禁用</el-radio>
            <el-radio :label="true">永久禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="禁用天数" v-if="!banForm.permanent">
          <el-input-number v-model="banForm.duration" :min="1" :max="365"></el-input-number>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="banDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmBan" :loading="submitting">确认禁用</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 解禁用户对话框 -->
    <el-dialog v-model="unbanDialogVisible" title="解禁用户" width="500px">
      <el-form :model="unbanForm" label-width="100px">
        <el-form-item label="用户名">
          <span>{{ selectedUser?.username }}</span>
        </el-form-item>
        <el-form-item label="解禁原因" required>
          <el-input v-model="unbanForm.reason" type="textarea" rows="3" placeholder="请输入解禁原因"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="unbanDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmUnban" :loading="submitting">确认解禁</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

export default {
  name: 'AdminUsers',
  setup() {
    const store = useStore();
    const router = useRouter();
    
    // 数据
    const loading = computed(() => store.getters['admin/isLoading']('users'));
    const users = computed(() => store.getters['admin/usersList']);
    const pagination = computed(() => store.getters['admin/usersPagination']);
    const total = computed(() => pagination.value.total);
    
    const currentPage = ref(1);
    const pageSize = ref(20);
    const submitting = ref(false);
    
    // 筛选表单
    const filterForm = reactive({
      role: ''
    });
    
    // 禁用用户
    const banDialogVisible = ref(false);
    const selectedUser = ref(null);
    const banForm = reactive({
      reason: '',
      permanent: false,
      duration: 7
    });
    
    // 解禁用户
    const unbanDialogVisible = ref(false);
    const unbanForm = reactive({
      reason: ''
    });
    
    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleString();
    };
    
    // 加载用户列表
    const loadUsers = async () => {
      try {
        await store.dispatch('admin/fetchUsers', {
          page: currentPage.value,
          per_page: pageSize.value,
          role: filterForm.role || undefined
        });
      } catch (error) {
        console.error('获取用户列表失败:', error);
        ElMessage.error('获取用户列表失败');
      }
    };
    
    // 初始化
    onMounted(() => {
      loadUsers();
    });
    
    // 处理筛选
    const handleFilter = () => {
      currentPage.value = 1;
      loadUsers();
    };
    
    // 重置筛选
    const resetFilter = () => {
      filterForm.role = '';
      currentPage.value = 1;
      loadUsers();
    };
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size;
      loadUsers();
    };
    
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      loadUsers();
    };
    
    // 禁用用户
    const handleBan = (user) => {
      selectedUser.value = user;
      banForm.reason = '';
      banForm.permanent = false;
      banForm.duration = 7;
      banDialogVisible.value = true;
    };
    
    const confirmBan = async () => {
      if (!banForm.reason.trim()) {
        ElMessage.warning('请输入禁用原因');
        return;
      }
      
      submitting.value = true;
      try {
        await store.dispatch('admin/manageUser', {
          userId: selectedUser.value.id,
          data: {
            action: 'ban',
            reason: banForm.reason,
            duration: banForm.permanent ? undefined : banForm.duration
          }
        });
        
        ElMessage.success('用户禁用成功');
        banDialogVisible.value = false;
        loadUsers();
      } catch (error) {
        console.error('禁用用户失败:', error);
        ElMessage.error('禁用用户失败: ' + error);
      } finally {
        submitting.value = false;
      }
    };
    
    // 解禁用户
    const handleUnban = (user) => {
      selectedUser.value = user;
      unbanForm.reason = '';
      unbanDialogVisible.value = true;
    };
    
    const confirmUnban = async () => {
      if (!unbanForm.reason.trim()) {
        ElMessage.warning('请输入解禁原因');
        return;
      }
      
      submitting.value = true;
      try {
        await store.dispatch('admin/manageUser', {
          userId: selectedUser.value.id,
          data: {
            action: 'unban',
            reason: unbanForm.reason
          }
        });
        
        ElMessage.success('用户解禁成功');
        unbanDialogVisible.value = false;
        loadUsers();
      } catch (error) {
        console.error('解禁用户失败:', error);
        ElMessage.error('解禁用户失败: ' + error);
      } finally {
        submitting.value = false;
      }
    };
    
    // 查看用户操作记录
    const viewUserActions = (userId) => {
      router.push({
        name: 'AdminUserActions',
        query: { user_id: userId }
      });
    };
    
    return {
      loading,
      users,
      total,
      currentPage,
      pageSize,
      filterForm,
      banDialogVisible,
      unbanDialogVisible,
      selectedUser,
      banForm,
      unbanForm,
      submitting,
      formatDate,
      handleFilter,
      resetFilter,
      handleSizeChange,
      handleCurrentChange,
      handleBan,
      handleUnban,
      confirmBan,
      confirmUnban,
      viewUserActions
    };
  }
};
</script>

<style scoped>
.users-container {
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