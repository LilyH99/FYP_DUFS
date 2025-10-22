<template>
  <div class="w-1/3 border rounded-lg shadow-sm p-4 overflow-auto">
    <div class="font-semibold border-b pb-1 mb-2">Unit File Draft</div>
    <div class="flex flex-col gap-4 mt-2">
      <div 
        v-for="section in sections" 
        :key="section.id"
        class="border rounded-lg p-2 min-h-[60px] bg-gray-50 hover:bg-gray-100"
        @dragover.prevent
        @dragenter.prevent
        @drop.prevent="onDropToSection($event, section.id)"
      >
        <div class="font-medium border-b pb-1 mb-1">{{ section.title }}</div>
        <ul class="flex flex-col gap-1">
          <li 
            v-for="(file, fIndex) in unitFiles[section.id]" 
            :key="fIndex" 
            class="flex items-center gap-2 border p-1 rounded bg-white cursor-move"
          >
            <!-- use FileItem; forward dragstart to parent via local handler -->
            <FileItem
              :file="file"
              :index="fIndex"
              :from="section.id"
              @drag-start="handleDragStart"
              @file-click="() => $emit('file-click', file)"
            />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import FileItem from './FileItem.vue'
const props = defineProps({
  sections: Array,
  unitFiles: Object
})
const emit = defineEmits(['file-drag-start','file-click','file-dropped-to-section'])

const handleDragStart = (event, file, from, index) => {
  emit('file-drag-start', event, file, from, index)
}

const onDropToSection = (event, sectionId) => {
  // prevent default already handled by .prevent modifier,
  // just forward the section id to App.vue
  emit('file-dropped-to-section', sectionId)
}
</script>
