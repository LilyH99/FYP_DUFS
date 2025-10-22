<script setup>
import { ref } from 'vue'

const emit = defineEmits(['update-active', 'delete-tab', 'add-tab', 'rename-tab']) // ✅ ADD THIS

const props = defineProps({
  tabs: Array,
  activeTab: String
})

const renamingTab = ref(null)
const startRenaming = (id) => renamingTab.value = id
const stopRenaming = (tab) => {
  renamingTab.value = null
  tab && tab.title && emit('rename-tab', tab.id, tab.title) // ✅ FIXED
}
</script>

<template>
  <div class="border-b flex">
    <div v-for="(tab, index) in tabs" :key="tab.id" class="flex items-center">
      <button
        class="px-4 py-2"
        :class="activeTab === tab.id ? 'font-bold border-b-2' : ''"
        @click="emit('update-active', tab.id)"
        @dblclick="startRenaming(tab.id)"
      >
        <input
          v-if="renamingTab === tab.id"
          v-model="tab.title"
          @blur="stopRenaming(tab)"
          @keyup.enter="stopRenaming(tab)"
          class="border px-1"
        />
        <span v-else>{{ tab.title }}</span>
      </button>
      <button class="text-red-500 px-2" @click="emit('delete-tab', index)" v-if="tabs.length > 1">×</button>
    </div>
    <button class="ml-4 px-3 py-2 border-l" @click="emit('add-tab')">+ Add Tab</button>
  </div>
</template>

