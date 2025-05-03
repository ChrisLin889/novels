<template>
  <div class="comments-table">
    <div class="table-header">
      <el-select
        v-model="selectedNovelId"
        placeholder="按小说筛选"
        clearable
        @change="handleNovelChange"
        style="width: 300px; margin-right: 15px;"
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
        placeholder="按章节筛选"
        clearable
        @change="handleChapterChange"
        style="width: 300px"
        :disabled="!selectedNovelId"
      >
        <el-option
          v-for="chapter in chapters"
          :key="chapter.id"
          :label="chapter.title"
          :value="chapter.id"
        ></el-option>
      </el-select>
    </div>
    
    <el-table
      v-loading="loading"
      :data="comments"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="user.username" label="用户" width="150"></el-table-column>
      <el-table-column prop="novel_title" label="小说" width="150"></el-table-column>
      <el-table-column prop="chapter_title" label="章节" width="150"></el-table-column>
      <el-table-column prop="content" label="内容" min-width="200"></el-table-column>
      <el-table-column prop="deleted_at" label="删除时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.deleted_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template #default="scope">
          <el-button
            size="small"
            type="success"
            @click="handleRestore(scope.row)"
          >还原</el-button>
          <el-button
            size="small"
            type="danger"
            @click="handlePermanentDelete(scope.row)"
          >永久删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination-container">
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { getRecycledComments, restoreComment, permanentlyDeleteComment, getAllNovels, getChaptersByNovelId } from '@/api/admin';

export default {
  name: 'CommentsTable',
  data() {
    return {
      loading: false,
      comments: [],
      novels: [],
      chapters: [],
      selectedNovelId: null,
      selectedChapterId: null,
      total: 0,
      currentPage: 1,
      pageSize: 20
    };
  },
  created() {
    this.fetchData();
    this.fetchNovels();
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString();
    },
    fetchNovels() {
      getAllNovels().then(response => {
        this.novels = response.novels || [];
      }).catch(error => {
        console.error('获取小说列表失败:', error);
      });
    },
    fetchChapters() {
      if (this.selectedNovelId) {
        getChaptersByNovelId(this.selectedNovelId).then(response => {
          this.chapters = response.chapters || [];
        }).catch(error => {
          console.error('获取章节列表失败:', error);
        });
      } else {
        this.chapters = [];
      }
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
      
      getRecycledComments(params).then(response => {
        this.comments = response.comments;
        this.total = response.total;
        this.loading = false;
      }).catch(error => {
        console.error('获取回收站评论失败:', error);
        this.$message.error('获取回收站评论失败');
        this.loading = false;
      });
    },
    handleNovelChange() {
      this.selectedChapterId = null;
      this.fetchChapters();
      this.currentPage = 1;
      this.fetchData();
    },
    handleChapterChange() {
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
    handleRestore(row) {
      this.$confirm('确定要还原此评论吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        restoreComment(row.id).then(response => {
          this.$message.success(response.message || '评论已成功还原');
          this.fetchData();
        }).catch(error => {
          console.error('还原评论失败:', error);
          this.$message.error(error.response?.data?.error || '还原评论失败');
        });
      }).catch(() => {
        // 取消操作
      });
    },
    handlePermanentDelete(row) {
      this.$confirm('确定要永久删除此评论吗？此操作不可恢复。', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(() => {
        permanentlyDeleteComment(row.id).then(response => {
          this.$message.success(response.message || '评论已永久删除');
          this.fetchData();
        }).catch(error => {
          console.error('永久删除评论失败:', error);
          this.$message.error(error.response?.data?.error || '永久删除评论失败');
        });
      }).catch(() => {
        // 取消操作
      });
    }
  }
};
</script>

<style scoped>
.comments-table {
  margin-top: 20px;
}
.table-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-start;
}
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 