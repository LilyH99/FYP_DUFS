<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="$emit('close')">
    <div class="bg-white rounded-lg p-4 max-w-3xl max-h-[80vh] overflow-auto">
      <div class="flex justify-between items-center mb-2">
        <span class="font-bold">{{ file.name }}</span>
        <button @click="$emit('close')" class="text-red-500 font-bold text-xl">×</button>
      </div>
      <div class="mt-2">
        <img v-if="file.preview" :src="file.preview" class="max-w-full max-h-[70vh]" />
        <iframe v-else-if="file.type==='application/pdf'" :src="previewUrl" class="w-full h-[70vh]"></iframe>
        <pre v-else-if="file.type.startsWith('text/')" class="bg-gray-100 p-2 rounded overflow-auto">{{ previewContent }}</pre>
        <p v-else>Preview not available</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  file: Object,
  previewUrl: String,
  previewContent: String
})
</script>
