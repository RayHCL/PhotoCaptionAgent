import axios from 'axios'

const api = axios.create({
  baseURL: '',  // 使用 Vite 代理
  timeout: 120000,
})

// 获取支持的风格列表
export function getStyles() {
  return api.get('/api/styles')
}

// 生成文案
export function generateCaption(imageFile, styles, emoji) {
  const formData = new FormData()
  formData.append('image', imageFile)
  formData.append('styles', JSON.stringify(styles))
  formData.append('emoji', emoji)
  return api.post('/api/generate/caption', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export default api
