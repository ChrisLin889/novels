<template>
  <div class="author-center">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="profile-card">
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
            </div>
          </template>
          <div class="profile-info">
            <el-avatar :size="100" :src="avatarUrl"></el-avatar>
            <h3>{{ username }}</h3>
            <p>{{ user?.email || '' }}</p>
            <el-tag type="success">{{ user?.role || '' }}</el-tag>
            <div class="action-buttons">
              <el-button type="danger" @click="handleResignAuthor" size="small" style="margin-top: 15px;">注销作者身份</el-button>
            </div>
            <div v-if="debug" class="debug-info">
              <p>User state: {{ JSON.stringify(user) }}</p>
            </div>
          </div>
        </el-card>

        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>创作统计</span>
            </div>
          </template>
          <div class="stats-info">
            <div class="stat-item">
              <span class="label">作品数</span>
              <span class="value">{{ stats.novel_count || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="label">总字数</span>
              <span class="value">{{ stats.total_words || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="label">收藏数</span>
              <span class="value">{{ stats.total_collections || 0 }}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="18">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>我的小说</span>
              <el-button type="primary" @click="showAddNovelDialog">添加小说</el-button>
            </div>
          </template>
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
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button-group>
                  <el-button size="small" @click="showEditNovelDialog(row)">编辑</el-button>
                  <el-button size="small" @click="showChapterManagement(row)">章节</el-button>
                  <el-button size="small" type="danger" @click="handleDeleteNovel(row)">删除</el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 添加/编辑小说对话框 -->
    <el-dialog v-model="novelDialogVisible" :title="novelDialogType === 'add' ? '添加小说' : '编辑小说'" width="500px">
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
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="novelForm.status">
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
            <img v-if="novelForm.cover" :src="novelForm.cover" class="cover">
            <i v-else class="el-icon-plus cover-uploader-icon"></i>
          </el-upload>
        </el-form-item>
        <el-form-item label="简介" prop="intro">
          <el-input type="textarea" v-model="novelForm.intro" :rows="4"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="novelDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleNovelSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAuthorStats, getMyNovels, addNovel, updateNovel, deleteNovel, resignAuthor } from '@/api/author'

export default {
  name: 'AuthorCenter',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    // 添加state getter以解决Vuex状态更新问题 (GitHub issue: vuejs/vuex#2046)
    const storeState = computed(() => store.state)
    
    // 初始化用户数据
    const initUserData = () => {
      // 检查是否需要从localStorage恢复用户数据到store
      if (!storeState.value.user.user) {
        try {
          const storedUser = localStorage.getItem('user')
          if (storedUser) {
            const userData = JSON.parse(storedUser)
            console.log('从localStorage恢复用户数据到store:', userData)
            store.dispatch('user/setUser', userData)
          }
        } catch (e) {
          console.error('解析localStorage用户数据失败:', e)
        }
      }
    }
    
    // 调用初始化函数
    initUserData()
    
    // 尝试多种方式获取用户数据，确保数据可用
    const userFromStore = computed(() => storeState.value.user.user)
    const userFromLocalStorage = ref(null)
    
    try {
      const userStr = localStorage.getItem('user')
      if (userStr) {
        userFromLocalStorage.value = JSON.parse(userStr)
      }
    } catch (e) {
      console.error('解析localStorage中的user数据失败:', e)
    }
    
    const user = computed(() => userFromStore.value || userFromLocalStorage.value || {})
    
    // 调试，打印用户状态
    console.log('用户信息 - store:', userFromStore.value)
    console.log('用户信息 - localStorage:', userFromLocalStorage.value)
    
    const username = computed(() => user.value?.username || '作者用户')
    const avatarUrl = computed(() => {
      const avatar = user.value?.avatar || 'default.jpg'
      // 修复头像路径问题，增加fallback默认图片
      if (!avatar || avatar === 'default.jpg') {
        return 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
      }
      return avatar.startsWith('http') ? avatar : `/uploads/${avatar}`
    })
    
    const debug = ref(true) // 开启调试信息
    const stats = ref({})
    const novels = ref([])
    const loading = ref(false)
    const novelDialogVisible = ref(false)
    const novelDialogType = ref('add')
    const novelFormRef = ref(null)
    const currentNovelId = ref(null)

    const novelRules = {
      title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
      category: [{ required: true, message: '请选择分类', trigger: 'change' }],
      status: [{ required: true, message: '请选择状态', trigger: 'change' }],
      intro: [{ required: true, message: '请输入简介', trigger: 'blur' }]
    }

    const loadStats = async () => {
      try {
        console.log('Loading author stats...');
        stats.value = {
          novel_count: 0,
          total_words: 0,
          total_collections: 0
        }; // 初始化默认值
        
        const response = await getAuthorStats();
        console.log('Author stats response:', response);
        if (response) {
          stats.value = response;
        } else {
          ElMessage.warning('无法获取统计信息，将显示默认值');
        }
      } catch (error) {
        console.error('获取统计信息失败:', error);
        ElMessage.error('获取统计信息失败');
      }
    }

    const loadNovels = async () => {
      loading.value = true;
      try {
        console.log('Loading author novels...');
        const response = await getMyNovels();
        console.log('Author novels response:', response);
        
        // 更详细的响应检查和数据提取
        if (response) {
          console.log('Response type:', typeof response);
          console.log('Response keys:', Object.keys(response));
          
          // 检查多种可能的响应格式
          if (Array.isArray(response)) {
            // 如果响应直接是数组
            console.log('Response is an array');
            novels.value = response;
          } else if (response.novels) {
            // 如果响应有novels字段
            console.log('Response has novels field');
            novels.value = response.novels;
          } else {
            // 尝试其他可能的响应格式
            const possibleKeys = ['data', 'items', 'list', 'results'];
            for (const key of possibleKeys) {
              if (response[key] && Array.isArray(response[key])) {
                console.log(`Found novels in response.${key}`);
                novels.value = response[key];
                break;
              }
            }
            
            // 如果仍然没有找到小说数据，检查response本身是否包含小说对象的特征
            if (novels.value.length === 0 && response.id && response.title) {
              console.log('Response appears to be a single novel');
              novels.value = [response];
            }
          }
          
          // 修改条件判断逻辑，区分"无法解析"和"没有小说"两种情况
          if (!novels.value) {
            console.log('Failed to parse novels from response');
            novels.value = [];
            ElMessage.warning('无法解析小说列表，请联系管理员');
          } else if (novels.value.length === 0) {
            console.log('Author has no novels yet');
            // 这是正常情况，不需要显示错误消息
          }
        } else {
          novels.value = [];
          ElMessage.warning('无法获取小说列表，请稍后再试');
        }
      } catch (error) {
        console.error('获取小说列表失败:', error);
        ElMessage.error('获取小说列表失败');
        novels.value = [];
      } finally {
        loading.value = false;
      }
    }

    // 初始化小说表单
    const initNovelForm = () => {
      return {
        title: '',
        category: '',
        status: 'ongoing',
        author: user.value?.username || '匿名作者', // 确保作者字段存在
        cover: 'default_cover.jpg',
        intro: ''
      };
    };

    // 创建小说表单引用
    const novelForm = ref(initNovelForm());

    const showAddNovelDialog = () => {
      novelDialogType.value = 'add';
      novelForm.value = initNovelForm();
      novelDialogVisible.value = true;
    };

    const showEditNovelDialog = (row) => {
      novelDialogType.value = 'edit';
      currentNovelId.value = row.id;
      
      // 确保编辑时也包含作者字段
      novelForm.value = { 
        ...row,
        author: row.author || user.value?.username || '匿名作者'
      };
      
      novelDialogVisible.value = true;
    };

    const handleNovelSubmit = async () => {
      if (!novelFormRef.value) return
      
      await novelFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            loading.value = true;
            const formData = { ...novelForm.value };
            
            // 确保作者字段存在，使用当前用户名
            if (!formData.author) {
              formData.author = user.value?.username || '匿名作者';
            }
            
            console.log('提交小说数据:', formData);
            
            if (novelDialogType.value === 'add') {
              const response = await addNovel(formData);
              console.log('添加小说响应:', response);
              ElMessage.success('添加成功');
            } else {
              const response = await updateNovel(currentNovelId.value, formData);
              console.log('更新小说响应:', response);
              ElMessage.success('更新成功');
            }
            novelDialogVisible.value = false;
            
            // 添加延迟以确保后端处理完成
            setTimeout(() => {
              console.log('重新加载小说列表和统计数据');
              loadNovels();
              loadStats();
            }, 500);
          } catch (error) {
            console.error('小说操作失败:', error);
            // 尝试获取更详细的错误信息
            const errorMessage = error.response?.data?.error || 
                                error.message || 
                                (novelDialogType.value === 'add' ? '添加失败' : '更新失败');
            
            ElMessage.error(errorMessage);
          } finally {
            loading.value = false;
          }
        }
      })
    }

    const handleDeleteNovel = async (row) => {
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
      try {
        console.log('章节管理：准备跳转，小说ID为', row.id);
        // 确保novelId是字符串
        const novelId = row.id.toString();
        console.log('转换后的小说ID:', novelId);
        
        // 直接使用window.location.href跳转，而不是通过Vue Router
        const targetUrl = `${window.location.origin}/author/novel/${novelId}/chapters`;
        console.log('目标URL:', targetUrl);
        
        // 设置小说ID到localStorage，作为备用获取方式
        localStorage.setItem('current_novel_id', novelId);
        
        // 直接跳转
        window.location.href = targetUrl;
        
        console.log('已发出跳转指令');
      } catch (error) {
        console.error('章节管理导航错误:', error);
        ElMessage.error(`跳转到章节管理页面失败: ${error.message}`);
      }
    };

    const handleCoverSuccess = (res) => {
      novelForm.value.cover = res.url
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

    // 处理注销作者身份
    const handleResignAuthor = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要注销作者身份吗？注销后将无法发布新小说，已发布的小说不会被删除。',
          '警告',
          {
            confirmButtonText: '确定注销',
            cancelButtonText: '取消',
            type: 'warning',
            distinguishCancelAndClose: true
          }
        )
        
        // 调用注销API
        await resignAuthor()
        
        ElMessage.success('已成功注销作者身份')
        
        // 更新用户状态
        if (user.value) {
          const updatedUser = {...user.value, role: 'user'};
          store.dispatch('user/setUser', updatedUser);
          localStorage.setItem('user', JSON.stringify(updatedUser));
        }
        
        // 跳转到首页
        setTimeout(() => {
          router.push('/');
        }, 1500);
      } catch (error) {
        if (error !== 'cancel') {
          console.error('注销作者身份失败:', error);
          const errorMessage = error.response?.data?.error || error.message || '注销作者身份失败';
          ElMessage.error(errorMessage);
        }
      }
    }

    onMounted(() => {
      console.log('AuthorCenter mounted, user:', user.value)
      loadStats()
      loadNovels()
    })

    return {
      user,
      username,
      avatarUrl,
      debug,
      stats,
      novels,
      loading,
      novelDialogVisible,
      novelDialogType,
      novelFormRef,
      novelForm,
      currentNovelId,
      novelRules,
      showAddNovelDialog,
      showEditNovelDialog,
      handleNovelSubmit,
      handleDeleteNovel,
      showChapterManagement,
      handleCoverSuccess,
      beforeCoverUpload,
      handleResignAuthor
    }
  }
}
</script>

<style scoped>
.author-center {
  padding: 20px;
}

.profile-card {
  margin-bottom: 20px;
}

.profile-info {
  text-align: center;
}

.profile-info h3 {
  margin: 10px 0;
}

.stats-card {
  margin-bottom: 20px;
}

.stats-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-item .label {
  color: #666;
}

.stat-item .value {
  font-weight: bold;
  color: #409EFF;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.debug-info {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 12px;
  color: #606266;
  word-break: break-all;
  white-space: pre-wrap;
  max-height: 200px;
  overflow-y: auto;
}
</style> 