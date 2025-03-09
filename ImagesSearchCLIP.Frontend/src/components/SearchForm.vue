// src/components/SearchForm.vue
<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  loading: boolean
  queuePosition: number | null
}>()

const emit = defineEmits<{
  (e: 'search', params: { text: string; limit: number }): void
}>()

const searchText = ref('')
const limit = ref(5)

const handleSearch = () => {
  if (searchText.value.trim() && limit.value > 0) {
    emit('search', {
      text: searchText.value.trim(),
      limit: limit.value
    })
  }
}
</script>

<template>
  <div class="search-container">
    <div class="status" v-if="queuePosition !== null">
      当前队列位置: {{ queuePosition + 1 }}
    </div>
    <div class="input-group">
      <input
          type="number"
          v-model.number="limit"
          min="1"
          max="20"
          class="limit-input"
          placeholder="数量"
      />
      <input
          type="text"
          v-model="searchText"
          class="search-input"
          placeholder="使用自然语言搜索"
          @keyup.enter="handleSearch"
      />
      <button
          @click="handleSearch"
          :disabled="loading"
          class="search-button"
      >
        {{ loading ? '搜索中...' : '搜索' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.search-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.input-group {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.search-input {
  flex: 1;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
}

.limit-input {
  width: 100px;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
}

.search-button {
  padding: 12px 24px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.search-button:hover:not(:disabled) {
  background-color: #45a049;
}

.status {
  text-align: center;
  margin-bottom: 10px;
  color: #666;
}
</style>