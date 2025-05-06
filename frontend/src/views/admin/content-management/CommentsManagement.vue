<template>
  <div class="comments-management">
    <div class="filters">
      <el-select 
        v-model="selectedNovelId" 
        placeholder="选择小说" 
        clearable 
        style="width: 250px; margin-right: 10px;"
        @change="handleNovelChange"
      >
        <el-option 
          v-for="novel in novels" 
          :key="novel.id" 
          :label="novel.title" 
          :value="novel.id"
        ></el-option>
      </el-select>
      <el-select 
        v-model="selectedChapterId" 
        placeholder="选择章节" 
        clearable 
        style="width: 250px;"
        :disabled="!selectedNovelId"
      >
        <el-option 
          v-for="chapter in chapters" 
          :key="chapter.id" 
          :label="chapter.title" 
          :value="chapter.id"
        ></el-option>
      </el-select>
      <el-button type="primary" @click="handleSearch" style="margin-left: 10px;">搜索</el-button>
    </div>
    
    <el-table :data="comments" border v-loading="loading">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="user.username" label="用户" width="120"></el-table-column>
      <el-table-column prop="content" label="评论内容" min-width="200"></el-table-column>
      <el-table-column prop="novel_title" label="小说" width="120"></el-table-column>
      <el-table-column prop="chapter_title" label="章节" width="120"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160">
        <template #default="scope">{{ formatDate(scope.row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="scope">
          <el-button size="small" type="danger" @click="moveToTrash(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination-container">
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { getAdminComments, moveToTrash, getAllNovels, getChaptersByNovelId } from '@/api/admin';

export default {
  name: 'CommentsManagement',
  data() {
    return {
      comments: [],
      novels: [],
      chapters: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 20,
      selectedNovelId: null,
      selectedChapterId: null
    };
  },
  created() {
    this.fetchNovels();
    this.fetchData();
  },
  watch: {
    selectedNovelId(newVal) {
      this.selectedChapterId = null;
      if (newVal) {
        this.fetchChapters(newVal);
      } else {
        this.chapters = [];
      }
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString();
    },
    fetchNovels() {
      getAllNovels()
        .then(response => {
          this.novels = response.novels || [];
        })
        .catch(error => {
          console.error('获取小说列表失败:', error);
          this.$message.error('获取小说列表失败');
        });
    },
    fetchChapters(novelId) {
      getChaptersByNovelId(novelId)
        .then(response => {
          this.chapters = response.chapters || [];
        })
        .catch(error => {
          console.error('获取章节列表失败:', error);
          this.$message.error('获取章节列表失败');
        });
    },
    fetchData() {
      this.loading = true;
      
      const params = {
        page: this.currentPage,
        per_page: this.pageSize
      };
      
      if (this.selectedNovelId) {
        params.novel_id = this.selectedNovelId;
      }
      
      if (this.selectedChapterId) {
        params.chapter_id = this.selectedChapterId;
      }
      
      getAdminComments(params)
        .then(response => {
          this.comments = response.comments;
          this.total = response.total;
        })
        .catch(error => {
          console.error('获取评论列表失败:', error);
          this.$message.error('获取评论列表失败');
        })
        .finally(() => {
          this.loading = false;
        });
    },
    handleNovelChange() {
      this.currentPage = 1;
      this.fetchData();
    },
    handleSearch() {
      this.currentPage = 1;
      this.fetchData();
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchData();
    },
    moveToTrash(comment) {
      this.$confirm('确定要将此评论移至回收站吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        moveToTrash('comment', comment.id)
          .then(response => {
            this.$message.success(response.message || '评论已移至回收站');
            this.fetchData();
          })
          .catch(error => {
            console.error('操作失败:', error);
            this.$message.error(error.response?.data?.error || '操作失败');
          });
      }).catch(() => {
        // 用户取消操作
      });
    }
  }
};
</script>

<style scoped>
.comments-management {
  margin-top: 20px;
}
.filters {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 