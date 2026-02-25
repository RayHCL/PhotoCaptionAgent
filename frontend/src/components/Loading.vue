<template>
  <div class="loading-container">
    <div class="loading-content">
      <el-icon class="loading-icon is-loading"><Loading /></el-icon>
      <div class="loading-text">{{ text }}</div>
    </div>
  </div>
</template>

<script setup>
import { Loading } from '@element-plus/icons-vue'

defineProps({
  text: {
    type: String,
    default: 'AI 正在生成文案中...'
  }
})
</script>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
}

.loading-content {
  text-align: center;
}

.loading-icon {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 16px;
}

.loading-text {
  font-size: 16px;
  color: #606266;
}
</style>
