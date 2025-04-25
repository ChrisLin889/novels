<template>
  <div class="novels-table">
    <div class="table-header">
      <el-input
        v-model="searchTitle"
        placeholder="搜索小说标题"
        style="width: 300px"
        clearable
        @keyup.enter.native="handleSearch"
        @clear="handleSearch"
      >
        <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
      </el-input>
    </div>
    
    <el-table
      v-loading="loading"
      :data="novels"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="title" label="标题" min-width="200"></el-table-column>
      <el-table-column prop="author_name" label="作者" width="150"></el-table-column>
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
import { getRecycledNovels, restoreNovel, permanentlyDeleteNovel } from '@/api/admin';
import { formatDate } from '@/utils/date';

export default {
  name: 'NovelsTable',
  data() {
    return {
      loading: false,
      novels: [],
      total: 0,
      currentPage: 1,
      pageSize: 20,
      searchTitle: ''
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString();
    },
    fetchData() {
      this.loading = true;
      
      getRecycledNovels({
        page: this.currentPage,
        per_page: this.pageSize,
        title: this.searchTitle || undefined
      }).then(response => {
        this.novels = response.data.novels;
        this.total = response.data.total;
        this.loading = false;
      }).catch(error => {
        console.error('获取回收站小说失败:', error);
        this.$message.error('获取回收站小说失败');
        this.loading = false;
      });
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
    handleRestore(row) {
      this.$confirm(`确定要还原小说"${row.title}"吗？此操作将同时还原该小说的所有章节和评论。`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        restoreNovel(row.id).then(response => {
          this.$message.success(response.data.message || '小说已成功还原');
          this.fetchData();
        }).catch(error => {
          console.error('还原小说失败:', error);
          this.$message.error(error.response?.data?.error || '还原小说失败');
        });
      }).catch(() => {
        // 取消操作
      });
    },
    handlePermanentDelete(row) {
      this.$confirm(`确定要永久删除小说"${row.title}"吗？此操作不可恢复。`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(() => {
        permanentlyDeleteNovel(row.id).then(response => {
          this.$message.success(response.data.message || '小说已永久删除');
          this.fetchData();
        }).catch(error => {
          console.error('永久删除小说失败:', error);
          this.$message.error(error.response?.data?.error || '永久删除小说失败');
        });
      }).catch(() => {
        // 取消操作
      });
    }
  }
};
</script>

<style scoped>
.novels-table {
  margin-top: 20px;
}
.table-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 