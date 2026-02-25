<template>
  <div class="caption-result">
    <div class="result-header">
      <div class="header-title">生成的文案</div>
      <el-button type="primary" link @click="$emit('regenerate')">
        <el-icon><Refresh /></el-icon>
        重新生成
      </el-button>
    </div>

    <div v-if="imageSummary" class="image-summary">
      <div class="summary-label">图片内容：</div>
      <div class="summary-text">{{ imageSummary }}</div>
    </div>

    <div class="captions-container">
      <el-collapse v-model="activeCollapse">
        <el-collapse-item
          v-for="(captions, style) in captions"
          :key="style"
          :name="style"
        >
          <template #title>
            <div class="collapse-title">
              <span class="style-name">{{ style }}</span>
              <el-tag size="small" type="info">{{ captions.length }} 条</el-tag>
            </div>
          </template>

          <div class="caption-list">
            <div
              v-for="(caption, index) in captions"
              :key="index"
              class="caption-item"
            >
              <div class="caption-text">{{ caption }}</div>
              <el-button
                type="primary"
                size="small"
                :icon="DocumentCopy"
                circle
                @click="copyCaption(caption)"
              />
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, DocumentCopy } from '@element-plus/icons-vue'

const props = defineProps({
  imageSummary: {
    type: String,
    default: ''
  },
  captions: {
    type: Object,
    default: () => ({})
  }
})

defineEmits(['regenerate'])

const activeCollapse = ref(Object.keys(props.captions || {}))

const copyCaption = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('复制成功')
  } catch (err) {
    ElMessage.error('复制失败')
  }
}
</script>

<style scoped>
.caption-result {
  margin-top: 32px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.image-summary {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.summary-label {
  font-size: 14px;
  font-weight: 500;
  color: #606266;
  margin-bottom: 8px;
}

.summary-text {
  font-size: 14px;
  color: #909399;
  line-height: 1.6;
}

.captions-container :deep(.el-collapse) {
  border: none;
}

.captions-container :deep(.el-collapse-item__header) {
  font-size: 16px;
  font-weight: 500;
}

.collapse-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.style-name {
  color: #303133;
}

.caption-list {
  padding: 8px 0;
}

.caption-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 12px;
}

.caption-item:last-child {
  margin-bottom: 0;
}

.caption-text {
  flex: 1;
  font-size: 15px;
  color: #303133;
  line-height: 1.6;
  padding-right: 12px;
}
</style>
