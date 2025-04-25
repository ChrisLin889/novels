<template>
  <div class="recycle-bin-container">
    <h1>内容回收站</h1>
    
    <el-tabs v-model="activeTab" @tab-click="handleTabClick">
      <el-tab-pane label="小说" name="novels">
        <novels-table v-if="activeTab === 'novels'" />
      </el-tab-pane>
      <el-tab-pane label="章节" name="chapters">
        <chapters-table v-if="activeTab === 'chapters'" />
      </el-tab-pane>
      <el-tab-pane label="评论" name="comments">
        <comments-table v-if="activeTab === 'comments'" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import NovelsTable from './recycle-bin/NovelsTable.vue';
import ChaptersTable from './recycle-bin/ChaptersTable.vue';
import CommentsTable from './recycle-bin/CommentsTable.vue';

export default {
  name: 'RecycleBin',
  components: {
    NovelsTable,
    ChaptersTable,
    CommentsTable
  },
  data() {
    return {
      activeTab: 'novels'
    };
  },
  methods: {
    handleTabClick() {
      // 在tab切换时重置分页等状态
    }
  }
};
</script>

<style scoped>
.recycle-bin-container {
  padding: 20px;
}
</style> 