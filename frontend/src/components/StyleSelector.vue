<template>
  <div class="style-selector">
    <div class="style-title">选择文案风格</div>
    <el-checkbox-group v-model="selectedStyles" class="style-group">
      <el-checkbox
        v-for="style in styles"
        :key="style.key"
        :label="style.key"
        :value="style.key"
        class="style-checkbox"
      >
        <div class="style-item">
          <div class="style-name">{{ style.name }}</div>
          <div class="style-desc">{{ style.description }}</div>
        </div>
      </el-checkbox>
    </el-checkbox-group>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  styles: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const selectedStyles = ref(props.modelValue || [])

watch(selectedStyles, (newVal) => {
  emit('update:modelValue', newVal)
})

watch(() => props.modelValue, (newVal) => {
  selectedStyles.value = newVal || []
})
</script>

<style scoped>
.style-selector {
  margin: 24px 0;
}

.style-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.style-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.style-checkbox :deep(.el-checkbox__label) {
  padding-left: 8px;
}

.style-checkbox :deep(.el-checkbox) {
  margin-right: 0;
}

.style-item {
  padding: 8px 4px;
}

.style-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.style-desc {
  font-size: 12px;
  color: #909399;
}
</style>
