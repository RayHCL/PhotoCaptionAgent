<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import ImageUpload from './components/ImageUpload.vue'
import StyleSelector from './components/StyleSelector.vue'
import CaptionResult from './components/CaptionResult.vue'
import Loading from './components/Loading.vue'
import { getStyles, generateCaption } from './api'

// 状态
const imageFile = ref(null)
const selectedStyles = ref([])
const styles = ref([])
const emojiEnabled = ref(true)
const loading = ref(false)
const result = ref(null)

// 加载风格列表
onMounted(async () => {
  try {
    console.log('Fetching styles...')
    const res = await getStyles()
    console.log('Styles response:', res)
    styles.value = res.data.styles
  } catch (err) {
    console.error('Error fetching styles:', err)
    ElMessage.error('获取风格列表失败，请确保后端服务已启动')
  }
})

// 生成文案
const handleGenerate = async () => {
  if (!imageFile.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  if (!selectedStyles.value || selectedStyles.value.length === 0) {
    ElMessage.warning('请至少选择一个文案风格')
    return
  }

  loading.value = true
  result.value = null

  try {
    const res = await generateCaption(
      imageFile.value,
      selectedStyles.value,
      emojiEnabled.value
    )
    result.value = res.data
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '生成失败，请重试')
  } finally {
    loading.value = false
  }
}

// 重新生成
const handleRegenerate = () => {
  result.value = null
  handleGenerate()
}
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1 class="app-title">朋友圈文案生成器</h1>
      <p class="app-subtitle">上传图片，AI 为你生成多种风格的朋友圈文案</p>
    </header>

    <main class="app-main">
      <section class="upload-section">
        <ImageUpload v-model="imageFile" />
      </section>

      <section class="style-section">
        <StyleSelector
          v-model="selectedStyles"
          :styles="styles"
        />

        <div class="emoji-setting">
          <el-switch
            v-model="emojiEnabled"
            active-text="带 emoji"
            inactive-text="不带 emoji"
          />
        </div>
      </section>

      <section class="action-section">
        <el-button
          type="primary"
          size="large"
          :loading="loading"
          :disabled="!imageFile || selectedStyles.length === 0"
          @click="handleGenerate"
        >
          {{ loading ? '生成中...' : '生成文案' }}
        </el-button>
      </section>

      <section v-if="loading" class="loading-section">
        <Loading />
      </section>

      <section v-if="result" class="result-section">
        <CaptionResult
          :image-summary="result.image_summary"
          :captions="result.captions"
          @regenerate="handleRegenerate"
        />
      </section>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  padding: 40px 20px;
}

.app-header {
  text-align: center;
  margin-bottom: 40px;
}

.app-title {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 12px;
}

.app-subtitle {
  font-size: 16px;
  color: #909399;
}

.app-main {
  max-width: 800px;
  margin: 0 auto;
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.upload-section {
  display: flex;
  justify-content: center;
}

.style-section {
  margin-top: 24px;
}

.emoji-setting {
  margin-top: 20px;
  display: flex;
  align-items: center;
}

.action-section {
  text-align: center;
  margin-top: 24px;
}

.action-section .el-button {
  min-width: 200px;
}

.loading-section {
  margin-top: 24px;
}

.result-section {
  margin-top: 24px;
}
</style>
