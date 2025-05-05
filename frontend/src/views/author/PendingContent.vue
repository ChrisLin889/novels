<template>
  <div class="pending-content">
    <h2>待审核内容</h2>

    <el-tabs v-model="activeTab">
      <el-tab-pane label="小说" name="novels">
        <el-table :data="pendingNovels" style="width: 100%" v-loading="loadingNovels" empty-text="没有待审核的小说">
          <el-table-column prop="title" label="标题" width="200">
            <template #default="{ row }">
              <router-link :to="'/novel/' + row.id">{{ row.title }}</router-link>
            </template>
          </el-table-column>
          <el-table-column prop="category" label="分类" width="120"></el-table-column>
          <el-table-column prop="audit_status" label="审核状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.audit_status === 'pending' ? 'warning' : 'info'">{{ row.audit_status === 'pending' ? '审核中' : row.audit_status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button size="small" @click="showEditNovelDialog(row)">编辑</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="章节" name="chapters">
        <el-table :data="pendingChapters" style="width: 100%" v-loading="loadingChapters" empty-text="没有待审核的章节">
          <el-table-column prop="novel_title" label="所属小说" width="200"></el-table-column>
          <el-table-column prop="title" label="章节标题" width="200">
            <template #default="{ row }">
              <router-link :to="'/novel/' + row.novel_id + '/chapter/' + row.id">{{ row.title }}</router-link>
            </template>
          </el-table-column>
          <el-table-column prop="audit_status" label="审核状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.audit_status === 'pending' ? 'warning' : 'info'">{{ row.audit_status === 'pending' ? '审核中' : row.audit_status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button size="small" @click="showEditChapterDialog(row)">编辑</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- Edit Novel Dialog -->
    <el-dialog v-model="novelDialogVisible" title="编辑小说" width="500px">
      <el-form :model="novelForm" label-width="80px" :rules="novelRules" ref="novelFormRef">
        <el-form-item label="标题" prop="title">
          <el-input v-model="novelForm.title"></el-input>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="novelForm.category" placeholder="请选择分类">
            <el-option label="玄幻" value="玄幻"></el-option>
            <el-option label="奇幻" value="奇幻"></el-option>
            <el-option label="武侠" value="武侠"></el-option>
            <el-option label="仙侠" value="仙侠"></el-option>
            <el-option label="都市" value="都市"></el-option>
            <el-option label="历史" value="历史"></el-option>
            <el-option label="军事" value="军事"></el-option>
            <el-option label="游戏" value="游戏"></el-option>
            <el-option label="科幻" value="科幻"></el-option>
            <el-option label="灵异" value="灵异"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="简介" prop="intro">
          <el-input type="textarea" v-model="novelForm.intro" :rows="4"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="novelDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleNovelSubmit">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Edit Chapter Dialog -->
    <el-dialog v-model="chapterDialogVisible" title="编辑章节" width="600px">
      <el-form :model="chapterForm" label-width="80px" :rules="chapterRules" ref="chapterFormRef">
        <el-form-item label="标题" prop="title">
          <el-input v-model="chapterForm.title"></el-input>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input type="textarea" v-model="chapterForm.content" :rows="15"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="chapterDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleChapterSubmit">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getPendingContent } from '@/api/author'
import { updateNovel } from '@/api/author'
import { updateChapter } from '@/api/chapter'

export default {
  name: 'PendingContent',
  setup() {
    const activeTab = ref('novels')
    const pendingNovels = ref([])
    const pendingChapters = ref([])
    const loadingNovels = ref(false)
    const loadingChapters = ref(false)
    
    const novelDialogVisible = ref(false)
    const chapterDialogVisible = ref(false)
    const novelForm = ref({
      title: '',
      category: '',
      intro: ''
    })
    const chapterForm = ref({
      title: '',
      content: ''
    })
    const currentNovelId = ref(null)
    const currentChapterId = ref(null)
    const novelFormRef = ref(null)
    const chapterFormRef = ref(null)
    
    const novelRules = {
      title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
      category: [{ required: true, message: '请选择分类', trigger: 'change' }],
      intro: [{ required: true, message: '请输入简介', trigger: 'blur' }]
    }
    
    const chapterRules = {
      title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
      content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
    }
    
    const loadPendingContent = async () => {
      loadingNovels.value = true
      loadingChapters.value = true
      try {
        const response = await getPendingContent()
        console.log('Pending content response:', response)
        if (response) {
          pendingNovels.value = response.pending_novels || []
          pendingChapters.value = response.pending_chapters || []
        }
      } catch (error) {
        console.error('获取待审核内容失败:', error)
        ElMessage.error('获取待审核内容失败')
      } finally {
        loadingNovels.value = false
        loadingChapters.value = false
      }
    }
    
    const showEditNovelDialog = (novel) => {
      currentNovelId.value = novel.id
      novelForm.value = {
        title: novel.title,
        category: novel.category,
        intro: novel.intro
      }
      novelDialogVisible.value = true
    }
    
    const showEditChapterDialog = (chapter) => {
      currentChapterId.value = chapter.id
      chapterForm.value = {
        title: chapter.title,
        content: chapter.content
      }
      chapterDialogVisible.value = true
    }
    
    const handleNovelSubmit = async () => {
      if (!novelFormRef.value) return
      
      await novelFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            await updateNovel(currentNovelId.value, novelForm.value)
            ElMessage.success('更新成功')
            novelDialogVisible.value = false
            loadPendingContent()
          } catch (error) {
            ElMessage.error('更新失败')
          }
        }
      })
    }
    
    const handleChapterSubmit = async () => {
      if (!chapterFormRef.value) return
      
      await chapterFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            await updateChapter(currentChapterId.value, chapterForm.value)
            ElMessage.success('更新成功')
            chapterDialogVisible.value = false
            loadPendingContent()
          } catch (error) {
            ElMessage.error('更新失败')
          }
        }
      })
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    onMounted(() => {
      loadPendingContent()
    })
    
    return {
      activeTab,
      pendingNovels,
      pendingChapters,
      loadingNovels,
      loadingChapters,
      novelDialogVisible,
      chapterDialogVisible,
      novelForm,
      chapterForm,
      novelRules,
      chapterRules,
      novelFormRef,
      chapterFormRef,
      showEditNovelDialog,
      showEditChapterDialog,
      handleNovelSubmit,
      handleChapterSubmit,
      formatDate
    }
  }
}
</script>

<style scoped>
.pending-content {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}
</style> 