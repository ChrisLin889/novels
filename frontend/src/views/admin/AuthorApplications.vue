<template>
  <div class="author-applications">
    <h1 class="page-title">作者申请审核</h1>
    
    <!-- 状态筛选 -->
    <div class="filter-section">
      <el-radio-group v-model="statusFilter" @change="handleFilterChange">
        <el-radio-button label="all">全部</el-radio-button>
        <el-radio-button label="pending">待审核</el-radio-button>
        <el-radio-button label="approved">已通过</el-radio-button>
        <el-radio-button label="rejected">已拒绝</el-radio-button>
      </el-radio-group>
      
      <el-button type="primary" @click="fetchApplications">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>
    
    <!-- 申请列表 -->
    <el-table
      v-loading="loading"
      :data="applications"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="user_id" label="用户ID" width="100" />
      <el-table-column prop="user_name" label="用户名" width="120" />
      <el-table-column prop="pen_name" label="笔名" width="120" />
      
      <el-table-column label="简介" min-width="200">
        <template #default="scope">
          <el-tooltip 
            class="box-item" 
            effect="dark" 
            :content="scope.row.bio" 
            placement="top-start"
            :hide-after="0"
          >
            <div class="truncated-text">{{ scope.row.bio }}</div>
          </el-tooltip>
        </template>
      </el-table-column>
      
      <el-table-column label="申请理由" min-width="200">
        <template #default="scope">
          <el-tooltip 
            class="box-item" 
            effect="dark" 
            :content="scope.row.reason" 
            placement="top-start"
            :hide-after="0"
          >
            <div class="truncated-text">{{ scope.row.reason }}</div>
          </el-tooltip>
        </template>
      </el-table-column>
      
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag 
            :type="getStatusTagType(scope.row.status)" 
            effect="plain"
          >
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column label="申请时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <div v-if="scope.row.status === 'pending'">
            <el-button 
              type="success" 
              size="small"
              @click="handleApprove(scope.row)"
            >
              通过
            </el-button>
            <el-button 
              type="danger" 
              size="small"
              @click="handleReject(scope.row)"
            >
              拒绝
            </el-button>
          </div>
          <div v-else>
            <el-button 
              type="primary" 
              size="small"
              @click="viewApplicationDetail(scope.row)"
            >
              查看详情
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    
    <!-- 拒绝申请对话框 -->
    <el-dialog
      title="拒绝作者申请"
      v-model="rejectDialogVisible"
      width="500px"
    >
      <el-form
        ref="rejectFormRef"
        :model="rejectForm"
        :rules="rejectRules"
        label-width="100px"
      >
        <el-form-item label="拒绝原因" prop="comment">
          <el-input
            v-model="rejectForm.comment"
            type="textarea"
            :rows="4"
            placeholder="请输入拒绝原因，该内容将展示给申请用户"
          ></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmReject" :loading="submitting">确认拒绝</el-button>
      </template>
    </el-dialog>
    
    <!-- 申请详情对话框 -->
    <el-dialog
      title="申请详情"
      v-model="detailDialogVisible"
      width="700px"
    >
      <div v-if="currentApplication" class="application-detail">
        <div class="detail-item">
          <div class="detail-label">用户ID:</div>
          <div class="detail-value">{{ currentApplication.user_id }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">用户名:</div>
          <div class="detail-value">{{ currentApplication.user_name }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">笔名:</div>
          <div class="detail-value">{{ currentApplication.pen_name }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">申请状态:</div>
          <div class="detail-value">
            <el-tag :type="getStatusTagType(currentApplication.status)">
              {{ getStatusText(currentApplication.status) }}
            </el-tag>
          </div>
        </div>
        <div class="detail-item">
          <div class="detail-label">申请时间:</div>
          <div class="detail-value">{{ formatDate(currentApplication.created_at) }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">处理时间:</div>
          <div class="detail-value">
            {{ currentApplication.updated_at ? formatDate(currentApplication.updated_at) : '未处理' }}
          </div>
        </div>
        <div class="detail-item">
          <div class="detail-label">处理人:</div>
          <div class="detail-value">{{ currentApplication.admin_id ? '管理员#' + currentApplication.admin_id : '未处理' }}</div>
        </div>
        <div class="detail-item detail-full">
          <div class="detail-label">作者简介:</div>
          <div class="detail-value detail-text">{{ currentApplication.bio }}</div>
        </div>
        <div class="detail-item detail-full">
          <div class="detail-label">申请理由:</div>
          <div class="detail-value detail-text">{{ currentApplication.reason }}</div>
        </div>
        <div v-if="currentApplication.admin_comment" class="detail-item detail-full">
          <div class="detail-label">管理员评论:</div>
          <div class="detail-value detail-text">{{ currentApplication.admin_comment }}</div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getAuthorApplications, processAuthorApplication } from '@/api/admin';
import { Refresh } from '@element-plus/icons-vue';

export default {
  name: 'AuthorApplications',
  components: {
    Refresh
  },
  setup() {
    const loading = ref(false);
    const submitting = ref(false);
    const applications = ref([]);
    const total = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const statusFilter = ref('all');
    
    // 拒绝申请相关
    const rejectDialogVisible = ref(false);
    const rejectForm = reactive({
      applicationId: null,
      comment: ''
    });
    const rejectFormRef = ref(null);
    const rejectRules = {
      comment: [
        { required: true, message: '请输入拒绝原因', trigger: 'blur' },
        { min: 5, max: 200, message: '长度在 5 到 200 个字符', trigger: 'blur' }
      ]
    };
    
    // 申请详情相关
    const detailDialogVisible = ref(false);
    const currentApplication = ref(null);
    
    // 获取作者申请列表
    const fetchApplications = async () => {
      loading.value = true;
      try {
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        };
        
        if (statusFilter.value !== 'all') {
          params.status = statusFilter.value;
        }
        
        const res = await getAuthorApplications(params);
        applications.value = res.applications || [];
        total.value = res.total || 0;
      } catch (error) {
        ElMessage.error('获取作者申请列表失败');
        console.error('获取作者申请列表失败:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    };
    
    // 获取状态标签类型
    const getStatusTagType = (status) => {
      switch (status) {
        case 'approved':
          return 'success';
        case 'rejected':
          return 'danger';
        case 'pending':
          return 'warning';
        default:
          return 'info';
      }
    };
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'approved':
          return '已通过';
        case 'rejected':
          return '已拒绝';
        case 'pending':
          return '待审核';
        default:
          return '未知';
      }
    };
    
    // 处理筛选变化
    const handleFilterChange = () => {
      currentPage.value = 1;
      fetchApplications();
    };
    
    // 处理页码变化
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      fetchApplications();
    };
    
    // 处理每页数量变化
    const handleSizeChange = (size) => {
      pageSize.value = size;
      currentPage.value = 1;
      fetchApplications();
    };
    
    // 处理通过申请
    const handleApprove = (application) => {
      ElMessageBox.confirm(
        `确定要通过「${application.pen_name}」的作者申请吗？`,
        '确认操作',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'success'
        }
      ).then(async () => {
        try {
          submitting.value = true;
          await processAuthorApplication(application.id, {
            action: 'approve',
            comment: '恭喜您，您的作者申请已通过审核！'
          });
          
          ElMessage.success('已通过该作者申请');
          fetchApplications();
        } catch (error) {
          ElMessage.error('操作失败：' + (error.message || '未知错误'));
        } finally {
          submitting.value = false;
        }
      }).catch(() => {});
    };
    
    // 处理拒绝申请
    const handleReject = (application) => {
      rejectForm.applicationId = application.id;
      rejectForm.comment = '';
      rejectDialogVisible.value = true;
    };
    
    // 确认拒绝
    const confirmReject = async () => {
      if (!rejectFormRef.value) return;
      
      await rejectFormRef.value.validate(async (valid) => {
        if (!valid) return;
        
        try {
          submitting.value = true;
          await processAuthorApplication(rejectForm.applicationId, {
            action: 'reject',
            comment: rejectForm.comment
          });
          
          ElMessage.success('已拒绝该作者申请');
          rejectDialogVisible.value = false;
          fetchApplications();
        } catch (error) {
          ElMessage.error('操作失败：' + (error.message || '未知错误'));
        } finally {
          submitting.value = false;
        }
      });
    };
    
    // 查看申请详情
    const viewApplicationDetail = (application) => {
      currentApplication.value = application;
      detailDialogVisible.value = true;
    };
    
    onMounted(() => {
      fetchApplications();
    });
    
    return {
      loading,
      submitting,
      applications,
      total,
      currentPage,
      pageSize,
      statusFilter,
      rejectDialogVisible,
      rejectForm,
      rejectFormRef,
      rejectRules,
      detailDialogVisible,
      currentApplication,
      fetchApplications,
      formatDate,
      getStatusTagType,
      getStatusText,
      handleFilterChange,
      handleCurrentChange,
      handleSizeChange,
      handleApprove,
      handleReject,
      confirmReject,
      viewApplicationDetail
    };
  }
};
</script>

<style scoped>
.author-applications {
  padding: 20px;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #409EFF;
}

.filter-section {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.truncated-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.application-detail {
  display: flex;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  width: 50%;
  margin-bottom: 15px;
}

.detail-full {
  width: 100%;
}

.detail-label {
  font-weight: bold;
  width: 100px;
}

.detail-value {
  flex: 1;
}

.detail-text {
  white-space: pre-wrap;
  line-height: 1.5;
}
</style> 