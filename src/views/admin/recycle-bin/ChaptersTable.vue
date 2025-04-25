<template>
  <div class="chapters-table">
    <div class="table-header">
      <el-select
        v-model="selectedNovelId"
        placeholder="按小说筛选"
        clearable
        @change="handleNovelChange"
        style="width: 300px"
      >
        <el-option
          v-for="novel in novels"
          :key="novel.id"
          :label="novel.title"
          :value="novel.id"
        ></el-option>
      </el-select>
    </div>
    
    <el-table
      v-loading="loading"
      :data="chapters"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="novel_title" label="小说" width="200"></el-table-column>
      <el-table-column prop="title" label="章节标题" min-width="200"></el-table-column>
      <el-table-column prop="chapter_number" label="章节序号" width="100"></el-table-column>
      <el-table-column prop="deleted_at" label="删除时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.deleted_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="success"
            @click="handleRestore(scope.row)"
          >还原</el-button>
          <el-button
            size="mini"
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
        :current-page.sync="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { getRecycledChapters, restoreChapter, permanentlyDeleteChapter, getAllNovels } from '@/api/admin';

export default {
  name: 'ChaptersTable',
  data() {
    return {
      loading: false,
      chapters: [],
      novels: [],
      selectedNovelId: null,
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
        this.novels = response.data.novels || [];
      }).catch(error => {
        console.error('获取小说列表失败:', error);
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
      
      getRecycledChapters(params).then(response => {
        this.chapters = response.data.chapters;
        this.total = response.data.total;
        this.loading = false;
      }).catch(error => {
        console.error('获取回收站章节失败:', error);
        this.$message.error('获取回收站章节失败');
        this.loading = false;
      });
    },
    handleNovelChange() {
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
      this.$confirm(`确定要还原章节"${row.title}"吗？此操作将同时还原该章节的所有评论。`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        restoreChapter(row.id).then(response => {
          this.$message.success(response.data.message || '章节已成功还原');
          this.fetchData();
        }).catch(error => {
          console.error('还原章节失败:', error);
          this.$message.error(error.response?.data?.error || '还原章节失败');
        });
      }).catch(() => {
        // 取消操作
      });
    },
    handlePermanentDelete(row) {
      this.$confirm(`确定要永久删除章节"${row.title}"吗？此操作不可恢复。`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(() => {
        permanentlyDeleteChapter(row.id).then(response => {
          this.$message.success(response.data.message || '章节已永久删除');
          this.fetchData();
        }).catch(error => {
          console.error('永久删除章节失败:', error);
          this.$message.error(error.response?.data?.error || '永久删除章节失败');
        });
      }).catch(() => {
        // 取消操作
      });
    }
  }
};
</script>

<style scoped>
.chapters-table {
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