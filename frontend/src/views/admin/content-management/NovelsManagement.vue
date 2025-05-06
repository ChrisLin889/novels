<template>
  <div class="novels-management">
    <div class="filters">
      <el-input v-model="searchTitle" placeholder="搜索小说标题" style="width: 200px; margin-right: 10px;" clearable></el-input>
      <el-select v-model="categoryFilter" placeholder="分类" clearable style="width: 150px; margin-right: 10px;">
        <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat"></el-option>
      </el-select>
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>
    
    <el-table :data="novels" border v-loading="loading">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="title" label="标题" min-width="180"></el-table-column>
      <el-table-column prop="author_name" label="作者" width="120"></el-table-column>
      <el-table-column prop="category" label="分类" width="100"></el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === 'ongoing' ? 'success' : 'info'">
            {{ scope.row.status === 'ongoing' ? '连载中' : '已完结' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160">
        <template #default="scope">{{ formatDate(scope.row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="viewNovel(scope.row)">查看</el-button>
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
import { getAdminNovels, moveToTrash } from '@/api/admin';

export default {
  name: 'NovelsManagement',
  data() {
    return {
      novels: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 20,
      searchTitle: '',
      categoryFilter: '',
      categories: ['玄幻', '奇幻', '武侠', '仙侠', '都市', '现实', '军事', '历史', '游戏', '体育', '科幻', '悬疑', '灵异', '古代言情', '现代言情', '幻想言情', '青春校园', '女尊', '百合']
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
      
      const params = {
        page: this.currentPage,
        per_page: this.pageSize
      };
      
      if (this.searchTitle) {
        params.title = this.searchTitle;
      }
      
      if (this.categoryFilter) {
        params.category = this.categoryFilter;
      }
      
      getAdminNovels(params)
        .then(response => {
          this.novels = response.novels;
          this.total = response.total;
        })
        .catch(error => {
          console.error('获取小说列表失败:', error);
          this.$message.error('获取小说列表失败');
        })
        .finally(() => {
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
    viewNovel(novel) {
      this.$router.push(`/novel/${novel.id}`);
    },
    moveToTrash(novel) {
      this.$confirm(`确定要将小说《${novel.title}》移至回收站吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        moveToTrash('novel', novel.id)
          .then(response => {
            this.$message.success(response.message || '小说已移至回收站');
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
.novels-management {
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