<template>
  <div class="crawled-novels-container">
    <h1 class="page-title">爬取小说管理</h1>
    
    <!-- 搜索和筛选 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="选择状态" clearable>
            <el-option label="待审核" value="pending"></el-option>
            <el-option label="已通过" value="approved"></el-option>
            <el-option label="已拒绝" value="rejected"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 爬取小说列表 -->
    <el-card class="list-card" v-loading="loading">
      <el-table :data="crawledNovels" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="title" label="小说标题" min-width="200"></el-table-column>
        <el-table-column prop="author" label="作者" width="150"></el-table-column>
        <el-table-column prop="source" label="来源" width="150"></el-table-column>
        <el-table-column prop="chapter_count" label="章节数" width="100"></el-table-column>
        <el-table-column prop="crawled_at" label="爬取时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.crawled_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.status === 'pending'" type="warning">待审核</el-tag>
            <el-tag v-else-if="scope.row.status === 'approved'" type="success">已通过</el-tag>
            <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
            <el-tag v-else type="info">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewChapters(scope.row)">查看章节</el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="success"
              size="small"
              @click="handleApprove(scope.row)"
            >
              通过
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="danger"
              size="small"
              @click="handleReject(scope.row)"
            >
              拒绝
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
    
    <!-- 章节详情对话框 -->
    <el-dialog v-model="chaptersDialogVisible" :title="chaptersTitle" width="80%" top="5vh">
      <div v-loading="chaptersLoading">
        <div class="novel-info" v-if="selectedNovel">
          <div class="info-item">
            <span class="info-label">小说标题:</span>
            <span class="info-value">{{ selectedNovel.title }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">作者:</span>
            <span class="info-value">{{ selectedNovel.author }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">来源:</span>
            <span class="info-value">{{ selectedNovel.source }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">简介:</span>
            <div class="info-value description">{{ selectedNovel.description || '暂无简介' }}</div>
          </div>
        </div>
        
        <el-divider content-position="center">章节列表</el-divider>
        
        <el-table :data="crawledChapters" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="title" label="章节标题" min-width="250"></el-table-column>
          <el-table-column prop="chapter_index" label="章节序号" width="100"></el-table-column>
          <el-table-column prop="word_count" label="字数" width="100"></el-table-column>
          <el-table-column prop="crawled_at" label="爬取时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.crawled_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button type="primary" size="small" @click="viewChapterContent(scope.row)">查看内容</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="chaptersDialogVisible = false">关闭</el-button>
          <template v-if="selectedNovel && selectedNovel.status === 'pending'">
            <el-button type="success" @click="handleApprove(selectedNovel)">通过</el-button>
            <el-button type="danger" @click="handleReject(selectedNovel)">拒绝</el-button>
          </template>
        </span>
      </template>
    </el-dialog>
    
    <!-- 章节内容对话框 -->
    <el-dialog v-model="contentDialogVisible" :title="contentTitle" width="70%" top="5vh">
      <div class="chapter-content" v-if="selectedChapter">
        <div class="content-preview">{{ selectedChapter.content }}</div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="contentDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 拒绝原因对话框 -->
    <el-dialog v-model="rejectDialogVisible" title="拒绝原因" width="500px">
      <el-form :model="rejectForm" :rules="rejectRules" ref="rejectFormRef" label-width="80px">
        <el-form-item label="拒绝原因" prop="reason">
          <el-input
            v-model="rejectForm.reason"
            type="textarea"
            rows="4"
            placeholder="请输入拒绝原因"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="rejectDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmReject" :loading="submitting">确认拒绝</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'AdminCrawledNovels',
  setup() {
    const store = useStore();
    const rejectFormRef = ref(null);
    
    // 数据
    const loading = computed(() => store.getters['admin/isLoading']('crawledNovels'));
    const chaptersLoading = computed(() => store.getters['admin/isLoading']('crawledChapters'));
    const crawledNovels = computed(() => store.getters['admin/crawledNovelsList']);
    const crawledChapters = computed(() => store.getters['admin/crawledChaptersList']);
    const pagination = computed(() => store.getters['admin/crawledNovelsPagination']);
    const total = computed(() => pagination.value.total);
    
    const currentPage = ref(1);
    const pageSize = ref(20);
    const submitting = ref(false);
    
    // 筛选表单
    const filterForm = reactive({
      status: ''
    });
    
    // 章节对话框
    const chaptersDialogVisible = ref(false);
    const selectedNovel = ref(null);
    const chaptersTitle = computed(() => {
      return selectedNovel.value ? `小说章节列表: ${selectedNovel.value.title}` : '章节列表';
    });
    
    // 章节内容对话框
    const contentDialogVisible = ref(false);
    const selectedChapter = ref(null);
    const contentTitle = computed(() => {
      return selectedChapter.value ? `章节内容: ${selectedChapter.value.title}` : '章节内容';
    });
    
    // 拒绝对话框
    const rejectDialogVisible = ref(false);
    const rejectForm = reactive({
      reason: ''
    });
    const rejectRules = {
      reason: [
        { required: true, message: '请输入拒绝原因', trigger: 'blur' },
        { min: 5, max: 500, message: '长度在 5 到 500 个字符', trigger: 'blur' }
      ]
    };
    
    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleString();
    };
    
    // 加载爬取小说列表
    const loadCrawledNovels = async () => {
      try {
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        };
        
        if (filterForm.status) {
          params.status = filterForm.status;
        }
        
        await store.dispatch('admin/fetchCrawledNovels', params);
      } catch (error) {
        console.error('获取爬取小说列表失败:', error);
        ElMessage.error('获取爬取小说列表失败');
      }
    };
    
    // 初始化
    onMounted(() => {
      loadCrawledNovels();
    });
    
    // 处理筛选
    const handleFilter = () => {
      currentPage.value = 1;
      loadCrawledNovels();
    };
    
    // 重置筛选
    const resetFilter = () => {
      filterForm.status = '';
      currentPage.value = 1;
      loadCrawledNovels();
    };
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size;
      loadCrawledNovels();
    };
    
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      loadCrawledNovels();
    };
    
    // 查看章节
    const viewChapters = async (novel) => {
      selectedNovel.value = novel;
      chaptersDialogVisible.value = true;
      
      try {
        await store.dispatch('admin/fetchCrawledChapters', novel.id);
      } catch (error) {
        console.error('获取爬取小说章节失败:', error);
        ElMessage.error('获取爬取小说章节失败');
      }
    };
    
    // 查看章节内容
    const viewChapterContent = (chapter) => {
      selectedChapter.value = chapter;
      contentDialogVisible.value = true;
    };
    
    // 批准小说
    const handleApprove = (novel) => {
      ElMessageBox.confirm(
        '确定要通过这个爬取的小说吗？通过后将会自动导入到系统中。',
        '确认操作',
        { type: 'info' }
      ).then(async () => {
        try {
          await store.dispatch('admin/manageCrawledNovel', {
            novelId: novel.id,
            data: { action: 'approve' }
          });
          
          ElMessage.success('小说已通过审核');
          chaptersDialogVisible.value = false;
          loadCrawledNovels();
        } catch (error) {
          console.error('审核操作失败:', error);
          ElMessage.error('审核操作失败: ' + error);
        }
      }).catch(() => {});
    };
    
    // 拒绝小说
    const handleReject = (novel) => {
      selectedNovel.value = novel;
      rejectForm.reason = '';
      rejectDialogVisible.value = true;
    };
    
    // 确认拒绝
    const confirmReject = async () => {
      if (!rejectFormRef.value) return;
      
      try {
        await rejectFormRef.value.validate();
        
        submitting.value = true;
        try {
          await store.dispatch('admin/manageCrawledNovel', {
            novelId: selectedNovel.value.id,
            data: {
              action: 'reject',
              reason: rejectForm.reason
            }
          });
          
          ElMessage.success('小说已拒绝');
          rejectDialogVisible.value = false;
          chaptersDialogVisible.value = false;
          loadCrawledNovels();
        } catch (error) {
          console.error('审核操作失败:', error);
          ElMessage.error('审核操作失败: ' + error);
        } finally {
          submitting.value = false;
        }
      } catch (error) {
        console.error('表单验证失败:', error);
      }
    };
    
    return {
      loading,
      chaptersLoading,
      crawledNovels,
      crawledChapters,
      total,
      currentPage,
      pageSize,
      filterForm,
      chaptersDialogVisible,
      contentDialogVisible,
      selectedNovel,
      selectedChapter,
      chaptersTitle,
      contentTitle,
      rejectDialogVisible,
      rejectForm,
      rejectRules,
      rejectFormRef,
      submitting,
      formatDate,
      handleFilter,
      resetFilter,
      handleSizeChange,
      handleCurrentChange,
      viewChapters,
      viewChapterContent,
      handleApprove,
      handleReject,
      confirmReject
    };
  }
};
</script>

<style scoped>
.crawled-novels-container {
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

.novel-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.info-item {
  margin-bottom: 10px;
  display: flex;
}

.info-label {
  font-weight: bold;
  width: 100px;
  flex-shrink: 0;
}

.info-value {
  flex-grow: 1;
}

.description {
  white-space: pre-line;
  background-color: #fff;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ebeef5;
}

.chapter-content {
  padding: 0 20px;
}

.content-preview {
  white-space: pre-line;
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
  max-height: 500px;
  overflow-y: auto;
  font-size: 16px;
  line-height: 1.8;
}
</style> 