<template>
  <div class="novel-management">
    <div class="header">
      <h2>我的小说</h2>
      <el-button type="primary" @click="showAddDialog">添加小说</el-button>
    </div>

    <el-table :data="novels" style="width: 100%" v-loading="loading">
      <el-table-column prop="title" label="标题" width="200">
        <template #default="{ row }">
          <router-link :to="'/novel/' + row.id">{{ row.title }}</router-link>
        </template>
      </el-table-column>
      <el-table-column prop="category" label="分类" width="120"></el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'ongoing' ? 'success' : 'info'">
            {{ row.status === 'ongoing' ? '连载中' : '已完结' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="chapter_count" label="章节数" width="100"></el-table-column>
      <el-table-column prop="word_count" label="字数" width="100"></el-table-column>
      <el-table-column prop="view_count" label="阅读数" width="100"></el-table-column>
      <el-table-column prop="collection_count" label="收藏数" width="100"></el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button size="small" @click="showChapterManagement(row)">章节</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="dialogType === 'add' ? '添加小说' : '编辑小说'" width="500px">
      <el-form :model="form" label-width="80px" :rules="rules" ref="formRef">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类">
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
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio label="ongoing">连载中</el-radio>
            <el-radio label="completed">已完结</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="封面" prop="cover">
          <el-upload
            class="cover-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleCoverSuccess"
            :before-upload="beforeCoverUpload">
            <img v-if="form.cover" :src="form.cover" class="cover">
            <i v-else class="el-icon-plus cover-uploader-icon"></i>
          </el-upload>
        </el-form-item>
        <el-form-item label="简介" prop="intro">
          <el-input type="textarea" v-model="form.intro" :rows="4"></el-input>
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyNovels, addNovel, updateNovel, deleteNovel } from '@/api/author'

export default {
  name: 'NovelManagement',
  setup() {
    const router = useRouter()
    const novels = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogType = ref('add')
    const formRef = ref(null)
    const form = ref({
      title: '',
      category: '',
      status: 'ongoing',
      cover: '',
      intro: ''
    })
    const currentNovelId = ref(null)

    const rules = {
      title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
      category: [{ required: true, message: '请选择分类', trigger: 'change' }],
      status: [{ required: true, message: '请选择状态', trigger: 'change' }],
      intro: [{ required: true, message: '请输入简介', trigger: 'blur' }]
    }

    const loadNovels = async () => {
      loading.value = true
      try {
        const response = await getMyNovels()
        novels.value = response.novels
      } catch (error) {
        ElMessage.error('获取小说列表失败')
      } finally {
        loading.value = false
      }
    }

    const showAddDialog = () => {
      dialogType.value = 'add'
      form.value = {
        title: '',
        category: '',
        status: 'ongoing',
        cover: '',
        intro: ''
      }
      dialogVisible.value = true
    }

    const showEditDialog = (row) => {
      dialogType.value = 'edit'
      currentNovelId.value = row.id
      form.value = { ...row }
      dialogVisible.value = true
    }

    const handleSubmit = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            if (dialogType.value === 'add') {
              await addNovel(form.value)
              ElMessage.success('添加成功')
            } else {
              await updateNovel(currentNovelId.value, form.value)
              ElMessage.success('更新成功')
            }
            dialogVisible.value = false
            loadNovels()
          } catch (error) {
            ElMessage.error(dialogType.value === 'add' ? '添加失败' : '更新失败')
          }
        }
      })
    }

    const handleDelete = async (row) => {
      try {
        await ElMessageBox.confirm('确定要删除该小说吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await deleteNovel(row.id)
        ElMessage.success('删除成功')
        loadNovels()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }

    const showChapterManagement = (row) => {
      router.push(`/author/novel/${row.id}/chapters`)
    }

    const handleCoverSuccess = (res) => {
      form.value.cover = res.url
    }

    const beforeCoverUpload = (file) => {
      const isJPG = file.type === 'image/jpeg'
      const isPNG = file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG && !isPNG) {
        ElMessage.error('上传封面图片只能是 JPG/PNG 格式!')
      }
      if (!isLt2M) {
        ElMessage.error('上传封面图片大小不能超过 2MB!')
      }
      return (isJPG || isPNG) && isLt2M
    }

    onMounted(() => {
      loadNovels()
    })

    return {
      novels,
      loading,
      dialogVisible,
      dialogType,
      formRef,
      form,
      rules,
      showAddDialog,
      showEditDialog,
      handleSubmit,
      handleDelete,
      showChapterManagement,
      handleCoverSuccess,
      beforeCoverUpload
    }
  }
}
</script>

<style scoped>
.novel-management {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.cover-uploader {
  text-align: center;
}

.cover-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.cover-uploader .el-upload:hover {
  border-color: #409EFF;
}

.cover-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.cover {
  width: 178px;
  height: 178px;
  display: block;
}
</style> 