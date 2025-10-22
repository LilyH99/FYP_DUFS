<template>
  <div 
    class="w-1/3 border rounded-lg shadow-sm p-4 overflow-auto"
    @dragover.prevent
    @dragenter.prevent
    @drop.prevent="$emit('file-dropped-to-suggestions', $event)"
  >
    <div class="font-semibold border-b pb-1 mb-2">Suggestions</div>
    <ul class="mt-2 flex flex-col gap-2">
      <FileItem 
        v-for="(file, index) in files" 
        :key="index" 
        :file="file"
        :index="index"
        from="suggestions"
        @drag-start="handleDragStart"
        @file-click="() => $emit('file-click', file)"
      />
    </ul>
  </div>
</template>

<script setup>
import FileItem from './FileItem.vue'
const props = defineProps({ files: Array })
const emit = defineEmits(['file-drag-start','file-click','file-dropped-to-suggestions'])

const handleDragStart = (event, file, from, index) => {
  // forward exactly the same args to parent (App.vue)
  emit('file-drag-start', event, file, from, index)
}
</script>
