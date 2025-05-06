<template>
  <div class="content-management">
    <h1>内容管理</h1>
    
    <el-tabs v-model="activeTab">
      <el-tab-pane label="小说管理" name="novels">
        <novels-management v-if="activeTab === 'novels'" />
      </el-tab-pane>
      <el-tab-pane label="章节管理" name="chapters">
        <chapters-management v-if="activeTab === 'chapters'" />
      </el-tab-pane>
      <el-tab-pane label="评论管理" name="comments">
        <comments-management v-if="activeTab === 'comments'" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import NovelsManagement from './content-management/NovelsManagement.vue';
import ChaptersManagement from './content-management/ChaptersManagement.vue';
import CommentsManagement from './content-management/CommentsManagement.vue';

export default {
  name: 'ContentManagement',
  components: {
    NovelsManagement,
    ChaptersManagement,
    CommentsManagement
  },
  data() {
    return {
      activeTab: 'novels'
    };
  }
};
</script>

<style scoped>
.content-management {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}
</style> 