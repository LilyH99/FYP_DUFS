<template>
  <div class="border rounded-lg shadow-lg bg-white p-6 mb-4">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-2xl font-bold text-gray-800">Validation Report</h2>
      <button 
        @click="runValidation" 
        :disabled="isValidating"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {{ isValidating ? 'Validating...' : 'Run Validation' }}
      </button>
    </div>

    <!-- Show validation results -->
    <div v-if="validationResults" class="space-y-6">
      
      <!-- Overall Status -->
      <div class="flex items-center gap-3 p-4 rounded-lg" 
           :class="overallStatus === 'pass' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'">
        <svg v-if="overallStatus === 'pass'" class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <svg v-else class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="font-semibold text-lg" :class="overallStatus === 'pass' ? 'text-green-800' : 'text-red-800'">
            {{ overallStatus === 'pass' ? 'Validation Passed!' : 'Validation Failed' }}
          </h3>
          <p class="text-sm" :class="overallStatus === 'pass' ? 'text-green-600' : 'text-red-600'">
            {{ overallStatus === 'pass' ? 'All required folders and files are present.' : 'Some required items are missing.' }}
          </p>
        </div>
      </div>

      <!-- Missing Folders Section -->
      <div v-if="validationResults.missingFolders.length > 0" class="border rounded-lg p-4 bg-red-50 border-red-200">
        <div class="flex items-start gap-2">
          <svg class="w-6 h-6 text-red-500 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div class="flex-1">
            <h3 class="font-semibold text-red-800 mb-2">Missing Required Folders ({{ validationResults.missingFolders.length }})</h3>
            <ul class="space-y-1">
              <li v-for="(folder, idx) in validationResults.missingFolders" :key="idx" 
                  class="text-sm text-red-700 bg-white px-3 py-2 rounded border border-red-200">
                {{ folder }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Missing Files in Folders Section -->
      <div v-if="Object.keys(validationResults.missingFiles).length > 0" class="border rounded-lg p-4 bg-yellow-50 border-yellow-200">
        <div class="flex items-start gap-2">
          <svg class="w-6 h-6 text-yellow-500 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <div class="flex-1">
            <h3 class="font-semibold text-yellow-800 mb-3">Missing Required Files in Folders</h3>
            <div class="space-y-3">
              <div v-for="(files, folder) in validationResults.missingFiles" :key="folder" 
                   class="bg-white p-3 rounded border border-yellow-200">
                <p class="font-medium text-yellow-800 mb-2">{{ folder }}</p>
                <ul class="list-disc list-inside space-y-1">
                  <li v-for="(file, idx) in files" :key="idx" class="text-sm text-yellow-700 ml-4">
                    {{ file }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Student Files Summary -->
      <div class="border rounded-lg p-4 bg-blue-50 border-blue-200">
        <h3 class="font-semibold text-blue-800 mb-3">Student Files Summary</h3>
        <div class="grid grid-cols-3 gap-4">
          <div class="bg-white p-4 rounded-lg border border-blue-200 text-center">
            <p class="text-3xl font-bold text-blue-600">{{ validationResults.studentFiles.total }}</p>
            <p class="text-sm text-blue-700 mt-1">Total Files</p>
          </div>
          <div class="bg-white p-4 rounded-lg border border-green-200 text-center">
            <p class="text-3xl font-bold text-green-600">{{ validationResults.studentFiles.valid }}</p>
            <p class="text-sm text-green-700 mt-1">Valid Files</p>
          </div>
          <div class="bg-white p-4 rounded-lg border border-red-200 text-center">
            <p class="text-3xl font-bold text-red-600">{{ validationResults.studentFiles.invalid }}</p>
            <p class="text-sm text-red-700 mt-1">Invalid Files</p>
          </div>
        </div>
      </div>

      <!-- Generate Output Button -->
      <div v-if="overallStatus === 'pass'" class="flex justify-end">
        <button 
          @click="generateOutput" 
          class="px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Generate Unit File Output
        </button>
      </div>

    </div>

    <!-- Initial State - No Validation Yet -->
    <div v-else class="text-center py-12 text-gray-500">
      <svg class="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-lg">Click "Run Validation" to check your unit files</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  unitFiles: Object,
  sections: Array
})

const emit = defineEmits(['generate-output'])

const isValidating = ref(false)
const validationResults = ref(null)

// Define required structure (based on Backend_Test proof of concept)
const requiredStructure = {
  'unit1': ['Assessment Moderation', 'Unit Moderation', 'QEA Report'],
  'unit2': ['Unit Outline'],
  'unit3': ['Lecture'],
  'unit4': ['Tutorial'],
  'unit5': ['Assignment', 'Rubric', 'Test'],
  'unit6': [],
  'unit7': ['OBE'],
  'unit8': [],
  'unit9': []
}

const overallStatus = computed(() => {
  if (!validationResults.value) return null
  const hasIssues = 
    validationResults.value.missingFolders.length > 0 || 
    Object.keys(validationResults.value.missingFiles).length > 0 ||
    validationResults.value.studentFiles.invalid > 0
  return hasIssues ? 'fail' : 'pass'
})

const runValidation = async () => {
  isValidating.value = true
  
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // Perform validation
  const missingFolders = []
  const missingFiles = {}
  
  // Check each section
  props.sections.forEach(section => {
    const files = props.unitFiles[section.id] || []
    const required = requiredStructure[section.id] || []
    
    // Check if folder is empty when it should have files
    if (files.length === 0 && required.length > 0) {
      missingFolders.push(section.title)
    } else if (files.length > 0 && required.length > 0) {
      // Check if required file types are present
      const fileNames = files.map(f => f.name.toLowerCase())
      const missing = required.filter(req => {
        return !fileNames.some(name => name.includes(req.toLowerCase()))
      })
      
      if (missing.length > 0) {
        missingFiles[section.title] = missing
      }
    }
  })
  
  // Validate student files (simple check for now)
  const studentSection = props.unitFiles['unit6'] || []
  const validStudentFiles = studentSection.filter(f => {
    // Simple validation: check if filename matches pattern
    return /\w+_\w+_\d{8}/.test(f.name)
  })
  
  validationResults.value = {
    missingFolders,
    missingFiles,
    studentFiles: {
      total: studentSection.length,
      valid: validStudentFiles.length,
      invalid: studentSection.length - validStudentFiles.length
    }
  }
  
  isValidating.value = false
}

const generateOutput = () => {
  emit('generate-output')
}
</script>