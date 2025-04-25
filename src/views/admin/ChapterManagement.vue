<template>
  <div class="chapter-management">
    <div class="page-actions">
      <el-button type="primary" icon="el-icon-plus" @click="handleCreate">新增章节</el-button>
      <el-button type="warning" icon="el-icon-delete" @click="goToRecycleBin">回收站</el-button>
    </div>
    
    <!-- Rest of the component -->
  </div>
</template>

<script>
export default {
  methods: {
    goToRecycleBin() {
      this.$router.push('/admin/recycle-bin');
    }
  }
}
</script>

this.$confirm('确定要将这个章节移至回收站吗？此操作将同时移除相关联的评论，但可以从回收站恢复。', '提示', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  type: 'warning'
}) 