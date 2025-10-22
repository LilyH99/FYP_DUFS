<template>
  <li
    class="flex items-center gap-2 border p-1 rounded bg-white cursor-move"
    draggable="true"
    @dragstart="onDragStart"
    @click="onClick"
  >
    <img v-if="file.preview" :src="file.preview" alt="preview" class="w-8 h-8 object-cover rounded" />
    <span>{{ file.name }}</span>
  </li>
</template>

<script setup>
import { defineEmits, defineProps } from 'vue'

const props = defineProps({
  file: Object,
  index: Number,
  from: String
})

const emit = defineEmits(['drag-start','file-click'])

const onDragStart = (event) => {
  // give the browser a small payload so it treats this as a real drag
  try {
    event.dataTransfer.setData('text/plain', props.file.name || '')
    event.dataTransfer.effectAllowed = 'move'
  } catch (e) {
    // ignore if browser forbids it
  }

  // emit a clean payload: (event, file, from, index)
  emit('drag-start', event, props.file, props.from, props.index)
}

const onClick = () => emit('file-click', props.file)
</script>
