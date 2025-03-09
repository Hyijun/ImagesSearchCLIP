// src/components/ImageGallery.vue
<script setup lang="ts">

defineProps<{
  imageUrls: string[]
}>()

const emit = defineEmits(['preview'])

const handlePreview = (url: string) => {
  emit('preview', url)
}
</script>

<template>
  <div class="gallery-container">
    <div class="image-grid">
      <div
          v-for="(url, index) in imageUrls"
          :key="index"
          class="image-item"
          @click="handlePreview(url)">
        <img
            :src="url"
            alt="搜索结果"
            class="image"
            loading="lazy"
        />
      </div>
    </div>
  </div>
</template>
<style scoped>
.gallery-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 10px;
}

.image-item {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.image-item:hover {
  transform: translateY(-5px);
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>