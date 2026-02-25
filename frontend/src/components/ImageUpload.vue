<template>
  <div class="upload-container">
    <el-upload
      class="upload-area"
      :class="{ 'has-image': imageUrl }"
      :show-file-list="false"
      :before-upload="beforeUpload"
      :on-change="handleChange"
      drag
      accept="image/jpeg,image/jpg,image/png"
    >
      <div v-if="!imageUrl" class="upload-placeholder">
        <el-icon class="upload-icon"><Plus /></el-icon>
        <div class="upload-text">拖拽图片到此处或点击上传</div>
        <div class="upload-hint">支持 JPG、PNG 格式</div>
      </div>
      <img v-else :src="imageUrl" class="preview-image" />
    </el-upload>
    <div v-if="imageUrl" class="clear-button">
      <el-button type="danger" link @click="clearImage">删除图片</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: File,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const imageUrl = ref('')

const beforeUpload = (file) => {
  const isImage = file.type === 'image/jpeg' || file.type === 'image/jpg' || file.type === 'image/png'
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传 JPG/PNG 格式的图片!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB!')
    return false
  }
  return true
}

const handleChange = (file) => {
  if (file.status === 'ready') {
    emit('update:modelValue', file.raw)
    imageUrl.value = URL.createObjectURL(file.raw)
  }
}

const clearImage = () => {
  emit('update:modelValue', null)
  imageUrl.value = ''
}
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-area {
  width: 100%;
  max-width: 400px;
}

.upload-area :deep(.el-upload-dragger) {
  width: 100%;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  transition: all 0.3s;
}

.upload-area :deep(.el-upload-dragger:hover) {
  border-color: #409eff;
}

.upload-area.has-image :deep(.el-upload-dragger) {
  border-style: solid;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  font-size: 48px;
  color: #909399;
  margin-bottom: 16px;
}

.upload-text {
  font-size: 16px;
  color: #606266;
  margin-bottom: 8px;
}

.upload-hint {
  font-size: 12px;
  color: #909399;
}

.preview-image {
  max-width: 100%;
  max-height: 280px;
  object-fit: contain;
}

.clear-button {
  margin-top: 12px;
}
</style>
