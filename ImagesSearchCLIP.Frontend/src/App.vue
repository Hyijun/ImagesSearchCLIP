// src/App.vue
<script setup lang="ts">
import { ref } from 'vue'
import SearchForm from './components/SearchForm.vue'
import ImageGallery from './components/ImageGallery.vue'
import ImagePreview from './components/ImagePreview.vue'

const imageUrls = ref<string[]>([])
const loading = ref(false)
const queuePosition = ref<number | null>(null)
let eventSource: EventSource | null = null

const handleSearch = async ({ text, limit }: { text: string; limit: number }) => {
  resetState()
  loading.value = true

  try {
    eventSource = new EventSource(
        `http://localhost:8000/search?search=${encodeURIComponent(text)}&limit=${limit}`
    )

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.position !== undefined) {
        queuePosition.value = data.position
      }

      if (data.urls) {
        imageUrls.value = data.urls
        closeConnection()
      }
    }

    eventSource.onerror = () => {
      closeConnection()
      loading.value = false
      alert('连接发生错误')
    }
  } catch (error) {
    console.error('Search error:', error)
    loading.value = false
  }
}

const resetState = () => {
  imageUrls.value = []
  queuePosition.value = null
}

const closeConnection = () => {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
  loading.value = false
  queuePosition.value = null
}

// 新增预览相关状态
const previewVisible = ref(false)
const selectedImageUrl = ref('')

const handlePreview = (url: string) => {
  selectedImageUrl.value = url
  previewVisible.value = true
}

const closePreview = () => {
  previewVisible.value = false
}
</script>

<template>
  <div class="app-container">
    <h1 class="title">自然语言图片搜索</h1>
    <SearchForm
        :loading="loading"
        :queue-position="queuePosition"
        @search="handleSearch"
    />
    <ImageGallery
        :image-urls="imageUrls"
        @preview="handlePreview"
    />
    <ImagePreview
        :image-url="selectedImageUrl"
        :visible="previewVisible"
        @close="closePreview"
    />
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.app-container {
  min-height: 100vh;
  padding: 40px 20px;
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 2.5em;
  font-weight: 300;
}

@media (max-width: 768px) {
  .input-group {
    flex-direction: column;
  }

  .limit-input,
  .search-button {
    width: 100%;
  }
}
</style>