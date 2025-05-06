<template>
  <div class="chapters-management">
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
      <el-input 
        v-model="searchTitle" 
        placeholder="章节标题" 
        style="width: 200px; margin-right: 10px;"
        clearable
      ></el-input>
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>
    
    <el-table :data="chapters" border v-loading="loading">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="title" label="章节标题" min-width="180"></el-table-column>
      <el-table-column prop="novel_title" label="所属小说" width="150"></el-table-column>
      <el-table-column prop="word_count" label="字数" width="100"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160">
        <template #default="scope">{{ formatDate(scope.row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="viewChapter(scope.row)">查看</el-button>
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
import { getAdminChapters, moveToTrash, getAllNovels } from '@/api/admin';

export default {
  name: 'ChaptersManagement',
  data() {
    return {
      chapters: [],
      novels: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 20,
      searchTitle: '',
      selectedNovelId: null
    };
  },
  created() {
    this.fetchNovels();
    this.fetchData();
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
    fetchData() {
      this.loading = true;
      
      const params = {
        page: this.currentPage,
        per_page: this.pageSize
      };
      
      if (this.selectedNovelId) {
        params.novel_id = this.selectedNovelId;
      }
      
      if (this.searchTitle) {
        params.title = this.searchTitle;
      }
      
      getAdminChapters(params)
        .then(response => {
          this.chapters = response.chapters;
          this.total = response.total;
        })
        .catch(error => {
          console.error('获取章节列表失败:', error);
          this.$message.error('获取章节列表失败');
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
    viewChapter(chapter) {
      this.$router.push(`/read/${chapter.novel_id}/${chapter.id}`);
    },
    moveToTrash(chapter) {
      this.$confirm(`确定要将章节《${chapter.title}》移至回收站吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        moveToTrash('chapter', chapter.id)
          .then(response => {
            this.$message.success(response.message || '章节已移至回收站');
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
.chapters-management {
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