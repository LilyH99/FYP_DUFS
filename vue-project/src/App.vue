<template>
  <div class="w-screen h-screen flex flex-col bg-white">

    <!-- TOP TAB BAR (unchanged logic, just layout moved up) -->
    <div class="border-b flex">
      <div v-for="(tab, index) in tabs" :key="tab.id" class="flex items-center">
        <button
          class="px-4 py-2"
          :class="activeTab === tab.id ? 'font-bold border-b-2' : ''"
          @click="activeTab = tab.id"
          @dblclick="startRenaming(tab.id)"
        >
          <input
            v-if="renamingTab === tab.id"
            v-model="tab.title"
            @blur="stopRenaming"
            @keyup.enter="stopRenaming"
            class="border px-1"
          />
          <span v-else>{{ tab.title }}</span>
        </button>
        <button class="text-red-500 px-2" @click="deleteTab(index)" v-if="tabs.length > 1">×</button>
      </div>
      <button class="ml-4 px-3 py-2 border-l" @click="addTab">+ Add Tab</button>
    </div>

    <!-- 3 COLUMN MAIN CONTENT -->
    <div class="flex flex-1 p-4 gap-4">
      
      <!-- LEFT COLUMN: SUGGESTIONS -->
      <div class="w-1/3 border rounded-lg shadow-sm p-4">
        <div class="font-semibold border-b pb-1 mb-2">
          Suggestions ({{ currentTab.title }})
        </div>
      </div>

      <!-- MIDDLE COLUMN: DRAG & DROP -->
      <div class="w-1/3 border rounded-lg shadow-sm flex items-center justify-center">
        <span class="text-lg font-medium">Drag & Drop files here</span>
      </div>

      <!-- RIGHT COLUMN: UNIT FILE DRAFT -->
      <div class="w-1/3 border rounded-lg shadow-sm p-4">
        <div class="font-semibold border-b pb-1 mb-2">
          Unit File Draft ({{ currentTab.title }})
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const tabs = ref([{ id: 'tab1', title: 'Tab 1' }])
const activeTab = ref('tab1')
const renamingTab = ref(null)

const addTab = () => {
  const newId = 'tab' + (tabs.value.length + 1)
  tabs.value.push({ id: newId, title: 'New Tab' })
  activeTab.value = newId
}

const deleteTab = (index) => {
  if (tabs.value[index].id === activeTab.value) {
    const newIndex = index > 0 ? index - 1 : 1
    activeTab.value = tabs.value[newIndex]?.id
  }
  tabs.value.splice(index, 1)
}

const startRenaming = (id) => {
  renamingTab.value = id
}
const stopRenaming = () => {
  renamingTab.value = null
}

const currentTab = computed(() => tabs.value.find(t => t.id === activeTab.value) || tabs.value[0])
</script>
