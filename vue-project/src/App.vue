<template>
  <div class="w-screen h-screen flex flex-col bg-white">
    <TabBar 
      :tabs="tabs" 
      :active-tab="activeTab" 
      @update-active="activeTab = $event"
      @rename-tab="renameTab"
      @delete-tab="deleteTab"
      @add-tab="addTab"
    />

    <!-- Validation Report Section -->
    <div class="p-4 overflow-auto max-h-96">
      <ValidationReport 
        :unit-files="currentTab.unitFiles"
        :sections="unitSections"
        @generate-output="generateUnitFileOutput"
      />
    </div>

    <div class="flex flex-1 p-4 gap-4 overflow-hidden">
      <SuggestionsPanel 
        :files="currentTab.suggestions"
        @file-dropped-to-suggestions="dropToSuggestions"
        @file-drag-start="startDrag"
        @file-click="openFile"
      />

      <FileDropzone @files-added="addFilesToSuggestions" />

      <UnitDraftPanel
        :sections="unitSections"
        :unit-files="currentTab.unitFiles"
        @file-drag-start="startDrag"
        @file-dropped-to-section="dropToSection"
        @file-dropped-to-suggestions="dropToSuggestions"
        @file-click="openFile"
      />
    </div>

    <FilePreviewModal 
      v-if="previewFile"
      :file="previewFile"
      :preview-url="previewFileUrl"
      :preview-content="previewContent"
      @close="closePreview"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import TabBar from './components/TabBar.vue'
import SuggestionsPanel from './components/SuggestionsPanel.vue'
import UnitDraftPanel from './components/UnitDraftPanel.vue'
import FileDropzone from './components/FileDropzone.vue'
import FilePreviewModal from './components/FilePreviewModal.vue'
import ValidationReport from './components/ValidationReport.vue'
import { generateUnitFileOutput as generateZip } from './outputGenerator.js'

// ---------- Tabs ----------
const tabs = ref([{ 
  id: 'tab1', title: 'Tab 1', suggestions: [], unitFiles: {} 
}])
const activeTab = ref('tab1')

// ---------- Unit Sections ----------
const unitSections = [
  { id: 'unit1', title: '1.0 Unit Panel Documentation' },
  { id: 'unit2', title: '2.0 Unit Outline' },
  { id: 'unit3', title: '3.0 Learning Materials' },
  { id: 'unit4', title: '4.0 Tutorial Materials' },
  { id: 'unit5', title: "5.0 Assessments and Marking Schemes" },
  { id: 'unit6', title: "6.0 Samples of Students' Work" },
  { id: 'unit7', title: "7.0 Outcome Based Education Report" },
  { id: 'unit8', title: "8.0 Safety Acknowledgement" },
  { id: 'unit9', title: "9.0 Final Exam Script" },
]

// Initialize empty arrays for each section per tab
tabs.value.forEach(tab => {
  unitSections.forEach(s => tab.unitFiles[s.id] = [])
})

// ---------- Current Tab ----------
const currentTab = computed(() => tabs.value.find(t => t.id === activeTab.value) || tabs.value[0])

// ---------- Drag & Drop ----------
const dragItem = ref(null)
const dragFrom = ref(null)
const dragIndex = ref(null)

const startDrag = (event, file, from, index) => {
  console.log('App.startDrag', { name: file?.name, from, index })
  dragItem.value = file
  dragFrom.value = from
  dragIndex.value = index

  // if event is present, ensure dataTransfer is set (defensive)
  try {
    event?.dataTransfer?.setData('text/plain', file?.name || '')
    event?.dataTransfer && (event.dataTransfer.effectAllowed = 'move')
  } catch (e) { /* ignore */ }
}

const dropToSection = (sectionId) => {
  console.log('App.dropToSection', { sectionId, dragging: dragItem.value?.name, dragFrom: dragFrom.value, dragIndex: dragIndex.value })
  if (!dragItem.value) return
  if (dragFrom.value === 'suggestions') {
    currentTab.value.suggestions.splice(dragIndex.value, 1)
  } else {
    currentTab.value.unitFiles[dragFrom.value].splice(dragIndex.value, 1)
  }
  currentTab.value.unitFiles[sectionId].push(dragItem.value)
  dragItem.value = null
  dragFrom.value = null
  dragIndex.value = null
}

const dropToSuggestions = () => {
  if (!dragItem.value) return
  if (dragFrom.value !== 'suggestions') currentTab.value.unitFiles[dragFrom.value].splice(dragIndex.value,1)
  currentTab.value.suggestions.push(dragItem.value)
  dragItem.value = null; dragFrom.value = null; dragIndex.value = null
}

// ---------- File Handling ----------
const addFilesToSuggestions = (files) => {
  files.forEach(file=>{
    if(file.type.startsWith('image/')) file.preview = URL.createObjectURL(file)
    else file.preview = null
  })
  currentTab.value.suggestions.push(...files)
}

// ---------- File Preview ----------
const previewFile = ref(null)
const previewFileUrl = ref('')
const previewContent = ref('')

const openFile = async (file) => {
  previewFile.value = file
  previewContent.value = ''
  previewFileUrl.value = ''
  if (file.type === 'application/pdf') previewFileUrl.value = URL.createObjectURL(file)
  else if (file.type.startsWith('text/')) previewContent.value = await file.text()
}

const closePreview = () => {
  previewFile.value = null
  previewFileUrl.value = ''
  previewContent.value = ''
}

// ---------- Tabs ----------
const addTab = () => {
  const newId = 'tab' + (tabs.value.length + 1)
  const newTab = { id: newId, title: 'New Tab', suggestions: [], unitFiles: {} }
  unitSections.forEach(s => newTab.unitFiles[s.id] = [])
  tabs.value.push(newTab)
  activeTab.value = newId
}

const deleteTab = (index) => {
  if (tabs.value[index].id === activeTab.value) {
    const newIndex = index > 0 ? index - 1 : 1
    activeTab.value = tabs.value[newIndex]?.id
  }
  tabs.value.splice(index, 1)
}

const renameTab = (id, title) => {
  const tab = tabs.value.find(t => t.id === id)
  if(tab) tab.title = title
}

const generateUnitFileOutput = async () => {
  const result = await generateZip(
    currentTab.value.unitFiles,
    unitSections,
    'COS12345',
    'Course Name'
  )
  
  if (result.success) {
    alert('✅ ' + result.message + '\nCheck your Downloads folder!')
  } else {
    alert('❌ ' + result.message)
  }
}

</script>
