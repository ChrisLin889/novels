<template>
  <div class="content-audit-container">
    <div class="page-header">
      <h1 class="page-title">内容审核 - {{ contentTypeText }}</h1>
      <el-button type="warning" @click="goToRecycleBin">
        <el-icon><Delete /></el-icon>
        回收站
      </el-button>
    </div>
    
    <!-- 内容列表 -->
    <el-card class="list-card" v-loading="loading">
      <!-- 小说审核列表 -->
      <div v-if="contentType === 'novel'">
        <el-table :data="contentList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="title" label="小说标题" min-width="200"></el-table-column>
          <el-table-column prop="author_name" label="作者" width="120"></el-table-column>
          <el-table-column prop="category" label="分类" width="100"></el-table-column>
          <el-table-column prop="tags" label="标签" width="150">
            <template #default="scope">
              <template v-if="scope.row.tags">
                <template v-if="typeof scope.row.tags === 'string'">
                  <el-tag v-for="tag in scope.row.tags.split(',')" :key="tag" size="small" style="margin: 0 3px 3px 0">
                    {{ tag }}
                  </el-tag>
                </template>
                <template v-else-if="Array.isArray(scope.row.tags)">
                  <el-tag v-for="tag in scope.row.tags" :key="tag" size="small" style="margin: 0 3px 3px 0">
                    {{ tag }}
                  </el-tag>
                </template>
                <template v-else>
                  {{ scope.row.tags }}
                </template>
              </template>
              <template v-else>
                <span>无标签</span>
              </template>
            </template>
          </el-table-column>
          <el-table-column prop="submitted_at" label="提交时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.submitted_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button type="primary" size="small" @click="viewDetails(scope.row)">查看详情</el-button>
              <el-button type="success" size="small" @click="handleApprove(scope.row)">通过</el-button>
              <el-button type="danger" size="small" @click="handleReject(scope.row)">拒绝</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 章节审核列表 -->
      <div v-else-if="contentType === 'chapter'">
        <el-table :data="contentList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="title" label="章节标题" min-width="200"></el-table-column>
          <el-table-column prop="novel_title" label="所属小说" width="200"></el-table-column>
          <el-table-column prop="author_name" label="作者" width="120"></el-table-column>
          <el-table-column prop="word_count" label="字数" width="100"></el-table-column>
          <el-table-column prop="submitted_at" label="提交时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.submitted_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button type="primary" size="small" @click="viewDetails(scope.row)">查看详情</el-button>
              <el-button type="success" size="small" @click="handleApprove(scope.row)">通过</el-button>
              <el-button type="danger" size="small" @click="handleReject(scope.row)">拒绝</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 评论审核列表 -->
      <div v-else-if="contentType === 'comment'">
        <el-table :data="contentList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="content" label="评论内容" min-width="300" show-overflow-tooltip></el-table-column>
          <el-table-column prop="user_name" label="评论用户" width="120"></el-table-column>
          <el-table-column prop="target_type" label="评论对象" width="100">
            <template #default="scope">
              {{ getTargetTypeText(scope.row.target_type) }}
            </template>
          </el-table-column>
          <el-table-column prop="target_title" label="对象标题" width="150" show-overflow-tooltip></el-table-column>
          <el-table-column prop="created_at" label="评论时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button type="success" size="small" @click="handleApprove(scope.row)">通过</el-button>
              <el-button type="danger" size="small" @click="handleReject(scope.row)">拒绝</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
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
    
    <!-- 查看详情对话框 -->
    <el-dialog v-model="detailsDialogVisible" :title="detailsTitle" width="65%" top="5vh">
      <div v-loading="detailsLoading">
        <!-- 小说详情 -->
        <template v-if="contentType === 'novel' && selectedContent">
          <div class="content-details">
            <div class="detail-item">
              <span class="detail-label">小说标题：</span>
              <span class="detail-value">{{ selectedContent.title }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">作者：</span>
              <span class="detail-value">{{ selectedContent.author_name }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">分类：</span>
              <span class="detail-value">{{ selectedContent.category }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">标签：</span>
              <span class="detail-value">
                <template v-if="selectedContent.tags">
                  <template v-if="typeof selectedContent.tags === 'string'">
                    <el-tag v-for="tag in selectedContent.tags.split(',')" :key="tag" size="small" style="margin: 0 3px 3px 0">
                      {{ tag }}
                    </el-tag>
                  </template>
                  <template v-else-if="Array.isArray(selectedContent.tags)">
                    <el-tag v-for="tag in selectedContent.tags" :key="tag" size="small" style="margin: 0 3px 3px 0">
                      {{ tag }}
                    </el-tag>
                  </template>
                  <template v-else>
                    {{ selectedContent.tags }}
                  </template>
                </template>
                <template v-else>
                  <span>无标签</span>
                </template>
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-label">简介：</span>
              <div class="detail-value description">{{ selectedContent.description }}</div>
            </div>
            <div class="detail-item">
              <span class="detail-label">封面：</span>
              <div class="detail-value">
                <el-image
                  v-if="selectedContent.cover"
                  :src="selectedContent.cover"
                  style="max-width: 200px; max-height: 300px"
                ></el-image>
                <span v-else>暂无封面</span>
              </div>
            </div>
          </div>
        </template>
        
        <!-- 章节详情 -->
        <template v-if="contentType === 'chapter' && selectedContent">
          <div class="content-details">
            <div class="detail-item">
              <span class="detail-label">章节标题：</span>
              <span class="detail-value">{{ selectedContent.title }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">所属小说：</span>
              <span class="detail-value">{{ selectedContent.novel_title }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">作者：</span>
              <span class="detail-value">{{ selectedContent.author_name }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">字数：</span>
              <span class="detail-value">{{ selectedContent.word_count }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">内容预览：</span>
              <div class="detail-value content-preview">{{ selectedContent.content }}</div>
            </div>
          </div>
        </template>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailsDialogVisible = false">关闭</el-button>
          <el-button type="success" @click="handleApprove(selectedContent)">通过</el-button>
          <el-button type="danger" @click="handleReject(selectedContent)">拒绝</el-button>
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
            :rows="4"
            placeholder="请输入拒绝原因，将通知给内容提交者"
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
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete } from '@element-plus/icons-vue';

export default {
  name: 'AdminContent',
  components: {
    Delete
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    const rejectFormRef = ref(null);
    
    // 内容类型
    const contentType = computed(() => route.params.type || 'novel');
    const contentTypeText = computed(() => {
      const types = {
        'novel': '小说审核',
        'chapter': '章节审核',
        'comment': '评论审核'
      };
      return types[contentType.value] || '内容审核';
    });
    
    // 数据
    const loading = computed(() => store.getters['admin/isLoading']('pendingContent'));
    const contentList = computed(() => store.getters['admin/pendingContent'](contentType.value) || []);
    const pagination = computed(() => store.getters['admin/pendingContentPagination'](contentType.value));
    const total = computed(() => pagination.value.total);
    
    const currentPage = ref(1);
    const pageSize = ref(20);
    const submitting = ref(false);
    
    // 详情对话框
    const detailsDialogVisible = ref(false);
    const detailsLoading = ref(false);
    const selectedContent = ref(null);
    const detailsTitle = computed(() => {
      if (!selectedContent.value) return '内容详情';
      if (contentType.value === 'novel') return `小说详情: ${selectedContent.value.title}`;
      if (contentType.value === 'chapter') return `章节详情: ${selectedContent.value.title}`;
      return '内容详情';
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
    
    // 监听路由参数变化
    watch(() => route.params.type, (newType) => {
      if (newType !== contentType.value) {
        currentPage.value = 1;
        loadContent();
      }
    });
    
    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleString();
    };
    
    // 获取评论对象类型文本
    const getTargetTypeText = (type) => {
      const types = {
        'novel': '小说',
        'chapter': '章节',
        'comment': '评论'
      };
      return types[type] || type;
    };
    
    // 加载内容列表
    const loadContent = async () => {
      try {
        await store.dispatch('admin/fetchPendingContent', {
          contentType: contentType.value,
          params: {
            page: currentPage.value,
            per_page: pageSize.value
          }
        });
        
        // 调试信息：检查返回的内容
        console.log('加载的待审核内容:', store.getters['admin/pendingContent'](contentType.value));
        const items = store.getters['admin/pendingContent'](contentType.value);
        if (items && items.length > 0) {
          console.log('第一个待审核内容的结构:', items[0]);
          console.log('待审核内容是否包含audit_id:', Object.prototype.hasOwnProperty.call(items[0], 'audit_id'));
        }
        
      } catch (error) {
        console.error('获取待审核内容失败:', error);
        ElMessage.error('获取待审核内容失败');
      }
    };
    
    // 初始化
    onMounted(() => {
      loadContent();
    });
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size;
      loadContent();
    };
    
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      loadContent();
    };
    
    // 查看详情
    const viewDetails = (content) => {
      selectedContent.value = content;
      detailsDialogVisible.value = true;
    };
    
    // 批准内容
    const handleApprove = (content) => {
      console.log('处理审批的内容对象:', content);
      console.log('content.audit_id =', content.audit_id);
      
      ElMessageBox.confirm(
        '确定要通过这个内容吗？',
        '确认操作',
        { type: 'info' }
      ).then(async () => {
        try {
          await store.dispatch('admin/auditContent', {
            auditId: content.audit_id,
            data: { status: 'approved' },
            contentType: contentType.value
          });
          
          ElMessage.success('内容已通过审核');
          detailsDialogVisible.value = false;
          loadContent();
        } catch (error) {
          console.error('审核操作失败:', error);
          ElMessage.error('审核操作失败: ' + error);
        }
      }).catch(() => {});
    };
    
    // 拒绝内容
    const handleReject = (content) => {
      selectedContent.value = content;
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
          await store.dispatch('admin/auditContent', {
            auditId: selectedContent.value.audit_id,
            data: {
              status: 'rejected',
              reason: rejectForm.reason
            },
            contentType: contentType.value
          });
          
          ElMessage.success('内容已拒绝');
          rejectDialogVisible.value = false;
          detailsDialogVisible.value = false;
          loadContent();
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
    
    // 跳转到回收站
    const goToRecycleBin = () => {
      router.push('/admin/recycle-bin');
    };
    
    return {
      contentType,
      contentTypeText,
      loading,
      contentList,
      total,
      currentPage,
      pageSize,
      detailsDialogVisible,
      detailsLoading,
      selectedContent,
      detailsTitle,
      rejectDialogVisible,
      rejectForm,
      rejectRules,
      rejectFormRef,
      submitting,
      formatDate,
      getTargetTypeText,
      handleSizeChange,
      handleCurrentChange,
      viewDetails,
      handleApprove,
      handleReject,
      confirmReject,
      goToRecycleBin
    };
  }
};
</script>

<style scoped>
.content-audit-container {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.list-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.content-details {
  padding: 10px;
}

.detail-item {
  margin-bottom: 15px;
  display: flex;
}

.detail-label {
  font-weight: bold;
  width: 100px;
  flex-shrink: 0;
}

.detail-value {
  flex-grow: 1;
}

.description, .content-preview {
  white-space: pre-line;
  background-color: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
}
</style> 