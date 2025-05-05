<template>
  <div class="chapter-management">
    <div class="header">
      <h2>{{ novelTitle }} - 章节管理</h2>
      <el-button type="primary" @click="showAddDialog">添加章节</el-button>
    </div>

    <el-table :data="chapters" style="width: 100%" v-loading="loading">
      <el-table-column prop="chapter_number" label="章节号" width="100"></el-table-column>
      <el-table-column prop="title" label="标题" width="200">
        <template #default="{ row }">
          <router-link :to="'/novel/' + novelId + '/chapter/' + row.id">{{ row.title }}</router-link>
        </template>
      </el-table-column>
      <el-table-column prop="word_count" label="字数" width="100"></el-table-column>
      <el-table-column prop="audit_status" label="审核状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getAuditStatusType(row.audit_status)">
            {{ getAuditStatusText(row.audit_status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="dialogType === 'add' ? '添加章节' : '编辑章节'" width="600px">
      <el-form :model="chapterForm" label-width="80px" :rules="rules" ref="chapterFormRef">
        <el-form-item label="标题" prop="title">
          <el-input v-model="chapterForm.title"></el-input>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input type="textarea" v-model="chapterForm.content" :rows="15"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getNovelDetail, getNovelChapters } from '@/api/novel'
import { addChapter, updateChapter, deleteChapter } from '@/api/chapter'

export default {
  name: 'ChapterManagement',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // 记录路由信息，方便调试
    console.log('ChapterManagement mounted, route:', route);
    console.log('Route params:', route.params);
    console.log('Novel ID from route:', route.params.novelId);
    
    // 尝试多种方式获取小说ID
    const getNovelId = () => {
      // 1. 首先尝试从路由参数中获取
      let id = route.params.novelId;
      console.log('从路由获取的小说ID:', id);
      
      // 2. 如果路由参数中没有，则尝试从localStorage中获取
      if (!id) {
        id = localStorage.getItem('current_novel_id');
        console.log('从localStorage获取的小说ID:', id);
      }
      
      // 3. 如果还是获取不到，则返回undefined
      return id;
    };
    
    const novelId = ref(getNovelId())
    const novelTitle = ref('')
    const chapters = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogType = ref('add')
    const chapterFormRef = ref(null)
    const chapterForm = ref({
      title: '',
      content: ''
    })
    const currentChapterId = ref(null)

    const rules = {
      title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
      content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
    }

    const loadNovelInfo = async () => {
      try {
        console.log('正在获取小说信息，ID:', novelId.value);
        const response = await getNovelDetail(novelId.value);
        console.log('获取到的小说信息:', response);
        novelTitle.value = response.novel.title;
      } catch (error) {
        console.error('获取小说信息失败:', error);
        ElMessage.error('获取小说信息失败');
        router.push('/author');
      }
    }

    const loadChapters = async () => {
      loading.value = true;
      try {
        console.log('正在获取章节列表，小说ID:', novelId.value);
        const response = await getNovelChapters(novelId.value);
        console.log('获取到的章节列表:', response);
        // 确保chapters是数组
        chapters.value = response?.chapters || [];
        
        if (chapters.value.length === 0) {
          console.log('当前小说没有章节');
        }
      } catch (error) {
        console.error('获取章节列表失败:', error);
        ElMessage.error('获取章节列表失败');
      } finally {
        loading.value = false;
      }
    }

    const showAddDialog = () => {
      dialogType.value = 'add'
      chapterForm.value = {
        title: '',
        content: ''
      }
      dialogVisible.value = true
    }

    const showEditDialog = (row) => {
      dialogType.value = 'edit'
      currentChapterId.value = row.id
      chapterForm.value = {
        title: row.title,
        content: row.content
      }
      dialogVisible.value = true
    }

    const handleSubmit = async () => {
      if (!chapterFormRef.value) return
      
      await chapterFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            if (dialogType.value === 'add') {
              await addChapter(novelId.value, chapterForm.value)
              ElMessage.success('添加成功')
            } else {
              await updateChapter(currentChapterId.value, chapterForm.value)
              ElMessage.success('更新成功')
            }
            dialogVisible.value = false
            loadChapters()
          } catch (error) {
            ElMessage.error(dialogType.value === 'add' ? '添加失败' : '更新失败')
          }
        }
      })
    }

    const handleDelete = async (row) => {
      try {
        await ElMessageBox.confirm('确定要删除该章节吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await deleteChapter(row.id)
        ElMessage.success('删除成功')
        loadChapters()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getAuditStatusType = (status) => {
      switch(status) {
        case 'approved': return 'success'
        case 'pending': return 'warning'
        case 'rejected': return 'danger'
        default: return 'info'
      }
    }
    
    const getAuditStatusText = (status) => {
      switch(status) {
        case 'approved': return '已通过'
        case 'pending': return '审核中'
        case 'rejected': return '已拒绝'
        default: return '未知'
      }
    }

    onMounted(() => {
      console.log('ChapterManagement组件已挂载');
      console.log('当前小说ID:', novelId.value);
      
      // 如果ID不存在，尝试再次获取
      if (!novelId.value) {
        console.log('尝试再次获取小说ID');
        novelId.value = getNovelId();
      }
      
      if (!novelId.value) {
        console.error('警告：未找到小说ID');
        ElMessage.warning('未找到小说ID，无法管理章节');
        setTimeout(() => {
          router.push('/author');
        }, 1500);
        return;
      }
      
      // 尝试加载数据
      console.log('开始加载小说信息和章节列表，小说ID:', novelId.value);
      loadNovelInfo()
      loadChapters()
    })

    return {
      novelId,
      novelTitle,
      chapters,
      loading,
      dialogVisible,
      dialogType,
      chapterFormRef,
      chapterForm,
      rules,
      getAuditStatusType,
      getAuditStatusText,
      showAddDialog,
      showEditDialog,
      handleSubmit,
      handleDelete,
      formatDate
    }
  }
}
</script>

<style scoped>
.chapter-management {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 