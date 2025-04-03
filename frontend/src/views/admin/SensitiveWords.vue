<template>
  <div class="sensitive-words-container">
    <h1 class="page-title">敏感词管理</h1>
    
    <!-- 搜索和筛选 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="分类">
          <el-select v-model="filterForm.category" placeholder="选择分类" clearable>
            <el-option label="政治" value="政治"></el-option>
            <el-option label="色情" value="色情"></el-option>
            <el-option label="暴力" value="暴力"></el-option>
            <el-option label="广告" value="广告"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="handleAddWord">添加敏感词</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 敏感词列表 -->
    <el-card class="list-card" v-loading="loading">
      <el-table :data="sensitiveWords" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="word" label="敏感词" width="200"></el-table-column>
        <el-table-column prop="category" label="分类" width="120">
          <template #default="scope">
            <el-tag :type="getCategoryTag(scope.row.category)">
              {{ scope.row.category }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="level" label="级别" width="120">
          <template #default="scope">
            <el-tag :type="getLevelTag(scope.row.level)">
              {{ getLevelText(scope.row.level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="添加时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="admin_name" label="添加管理员" width="150">
          <template #default="scope">
            {{ scope.row.admin_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-popconfirm
              title="确定要删除这个敏感词吗？"
              @confirm="handleDeleteWord(scope.row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
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
    
    <!-- 添加敏感词对话框 -->
    <el-dialog v-model="addDialogVisible" title="添加敏感词" width="500px">
      <el-form :model="addForm" :rules="addRules" ref="addFormRef" label-width="100px">
        <el-form-item label="敏感词" prop="word">
          <el-input v-model="addForm.word" placeholder="请输入敏感词"></el-input>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="addForm.category" placeholder="选择分类" style="width: 100%">
            <el-option label="政治" value="政治"></el-option>
            <el-option label="色情" value="色情"></el-option>
            <el-option label="暴力" value="暴力"></el-option>
            <el-option label="广告" value="广告"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="级别" prop="level">
          <el-select v-model="addForm.level" placeholder="选择级别" style="width: 100%">
            <el-option label="低级（替换）" :value="1"></el-option>
            <el-option label="中级（警告）" :value="2"></el-option>
            <el-option label="高级（禁止）" :value="3"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAddWord" :loading="submitting">确认添加</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';

export default {
  name: 'AdminSensitiveWords',
  setup() {
    const store = useStore();
    const addFormRef = ref(null);
    
    // 数据
    const loading = computed(() => store.getters['admin/isLoading']('sensitiveWords'));
    const sensitiveWords = computed(() => store.getters['admin/sensitiveWordsList']);
    const pagination = computed(() => store.getters['admin/sensitiveWordsPagination']);
    const total = computed(() => pagination.value.total);
    
    const currentPage = ref(1);
    const pageSize = ref(50);
    const submitting = ref(false);
    
    // 筛选表单
    const filterForm = reactive({
      category: ''
    });
    
    // 添加敏感词
    const addDialogVisible = ref(false);
    const addForm = reactive({
      word: '',
      category: '',
      level: 1
    });
    
    // 表单验证规则
    const addRules = {
      word: [
        { required: true, message: '请输入敏感词', trigger: 'blur' },
        { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
      ],
      category: [
        { required: true, message: '请选择分类', trigger: 'change' }
      ],
      level: [
        { required: true, message: '请选择级别', trigger: 'change' }
      ]
    };
    
    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleString();
    };
    
    // 获取分类标签样式
    const getCategoryTag = (category) => {
      const categories = {
        '政治': 'danger',
        '色情': 'warning',
        '暴力': 'danger',
        '广告': 'info',
        '其他': 'info'
      };
      return categories[category] || 'info';
    };
    
    // 获取级别标签样式
    const getLevelTag = (level) => {
      const levels = {
        1: 'info',
        2: 'warning',
        3: 'danger'
      };
      return levels[level] || 'info';
    };
    
    // 获取级别文本
    const getLevelText = (level) => {
      const texts = {
        1: '低级（替换）',
        2: '中级（警告）',
        3: '高级（禁止）'
      };
      return texts[level] || `级别${level}`;
    };
    
    // 加载敏感词列表
    const loadSensitiveWords = async () => {
      try {
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        };
        
        if (filterForm.category) {
          params.category = filterForm.category;
        }
        
        await store.dispatch('admin/fetchSensitiveWords', params);
      } catch (error) {
        console.error('获取敏感词列表失败:', error);
        ElMessage.error('获取敏感词列表失败');
      }
    };
    
    // 初始化
    onMounted(() => {
      loadSensitiveWords();
    });
    
    // 处理筛选
    const handleFilter = () => {
      currentPage.value = 1;
      loadSensitiveWords();
    };
    
    // 重置筛选
    const resetFilter = () => {
      filterForm.category = '';
      currentPage.value = 1;
      loadSensitiveWords();
    };
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size;
      loadSensitiveWords();
    };
    
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      loadSensitiveWords();
    };
    
    // 打开添加对话框
    const handleAddWord = () => {
      addForm.word = '';
      addForm.category = '';
      addForm.level = 1;
      addDialogVisible.value = true;
    };
    
    // 提交添加敏感词
    const submitAddWord = async () => {
      if (!addFormRef.value) return;
      
      try {
        await addFormRef.value.validate();
        
        submitting.value = true;
        try {
          await store.dispatch('admin/addSensitiveWord', {
            word: addForm.word,
            category: addForm.category,
            level: addForm.level
          });
          
          ElMessage.success('敏感词添加成功');
          addDialogVisible.value = false;
          loadSensitiveWords();
        } catch (error) {
          console.error('添加敏感词失败:', error);
          ElMessage.error('添加敏感词失败: ' + error);
        } finally {
          submitting.value = false;
        }
      } catch (error) {
        console.error('表单验证失败:', error);
      }
    };
    
    // 删除敏感词
    const handleDeleteWord = async (wordId) => {
      try {
        await store.dispatch('admin/deleteSensitiveWord', wordId);
        ElMessage.success('敏感词删除成功');
        loadSensitiveWords();
      } catch (error) {
        console.error('删除敏感词失败:', error);
        ElMessage.error('删除敏感词失败: ' + error);
      }
    };
    
    return {
      loading,
      sensitiveWords,
      total,
      currentPage,
      pageSize,
      filterForm,
      addDialogVisible,
      addForm,
      addRules,
      addFormRef,
      submitting,
      formatDate,
      getCategoryTag,
      getLevelTag,
      getLevelText,
      handleFilter,
      resetFilter,
      handleSizeChange,
      handleCurrentChange,
      handleAddWord,
      submitAddWord,
      handleDeleteWord
    };
  }
};
</script>

<style scoped>
.sensitive-words-container {
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