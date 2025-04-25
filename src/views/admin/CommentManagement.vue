<template>
  <div class="comment-management">
    <div class="page-actions">
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
    },
  }
}
</script>

this.$confirm('确定要将这条评论移至回收站吗？删除后可以从回收站恢复。', '提示', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  type: 'warning'
}) 
</rewritten_file> 