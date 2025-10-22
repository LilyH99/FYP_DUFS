<template>
  <div 
    class="w-1/3 border rounded-lg shadow-sm flex flex-col items-center justify-center border-dashed border-2 hover:border-blue-400 p-4"
    @dragover.prevent
    @dragenter.prevent
    @drop.prevent="handleDrop"
  >
    <span class="text-lg font-medium mb-2">Drag & Drop files here</span>
    <input type="file" multiple @change="handleInputFiles" class="hidden" ref="fileInput" />
    <button class="px-4 py-2 border rounded" @click="$refs.fileInput.click()">Or select files</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'            // <-- add this
const emit = defineEmits(['files-added'])
const fileInput = ref(null)

const handleDrop = (event) => {
  const files = Array.from(event.dataTransfer.files)
  emit('files-added', files)
}

const handleInputFiles = (event) => {
  emit('files-added', Array.from(event.target.files))
  event.target.value = ''
}
</script>
