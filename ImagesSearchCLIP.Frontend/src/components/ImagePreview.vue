// src/components/ImagePreview.vue
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  imageUrl: string
  visible: boolean
}>()

const emit = defineEmits(['close'])

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    emit('close')
  }
}

const handleClickBackground = (e: MouseEvent) => {
  if (e.target === e.currentTarget) {
    emit('close')
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <transition name="preview">
    <div
        v-if="visible"
        class="preview-overlay"
        @click="handleClickBackground"
    >
      <div class="preview-content">
        <img
            :src="imageUrl"
            class="preview-image"
            alt="预览大图"
            style="margin-right: 10px"
        />
        <button
            class="close-button"
            @click="emit('close')"
        >
          &times;
        </button>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.preview-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.preview-image {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

.close-button {
  position: absolute;
  top: -40px;
  right: -40px;
  background: none;
  border: none;
  color: white;
  font-size: 40px;
  width: 60px;
  height: 60px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.close-button:hover {
  opacity: 0.8;
}

/* 入场退场动画 */
.preview-enter-active,
.preview-leave-active {
  transition: all 0.3s ease;
}

.preview-enter-from,
.preview-leave-to {
  opacity: 0;
  backdrop-filter: blur(0);
}

.preview-enter-to {
  opacity: 1;
  backdrop-filter: blur(10px);
}
</style>