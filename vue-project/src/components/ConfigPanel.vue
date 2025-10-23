<template>
  <div class="border rounded-lg shadow-lg bg-white mb-4">
  <div 
    @click="isExpanded = !isExpanded"
    class="p-4 cursor-pointer hover:bg-gray-50 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <svg class="w-7 h-7 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
      <h2 class="text-xl font-bold text-gray-800">Configure Validation Rules</h2>
    </div>
    <div class="flex items-center gap-3">
      <span class="text-sm text-gray-500">{{ isExpanded ? 'Click to collapse' : 'Click to expand' }}</span>
      <svg 
        class="w-5 h-5 text-gray-600 transition-transform"
        :class="{ 'rotate-180': isExpanded }"
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
   </div>
  </div>

  <div v-if="isExpanded" class="p-6 border-t">

    <p class="text-sm text-gray-600 mb-6">
      Customize the validation rules for your unit. These settings determine what files are required in each folder.
    </p>

    <!-- Configuration Sections -->
    <div class="space-y-4">
      
      <!-- Section 3: Learning Materials -->
      <div class="border rounded-lg p-4 bg-gray-50">
        <h3 class="font-semibold text-gray-800 mb-3">📚 3.0 Learning Materials</h3>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Material Type
            </label>
            <select v-model="config.learningMaterials.type" class="w-full border rounded px-3 py-2">
              <option value="lecture">Lectures</option>
              <option value="workshop">Workshops</option>
              <option value="module">Modules</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Minimum Number Required
            </label>
            <input 
              type="number" 
              v-model.number="config.learningMaterials.minCount" 
              min="1" 
              max="20"
              class="w-full border rounded px-3 py-2"
            />
          </div>
        </div>
      </div>

      <!-- Section 4: Tutorial/Lab Materials -->
      <div class="border rounded-lg p-4 bg-gray-50">
        <h3 class="font-semibold text-gray-800 mb-3">✏️ 4.0 Tutorial/Lab Materials</h3>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Activity Type
            </label>
            <select v-model="config.practicalMaterials.type" class="w-full border rounded px-3 py-2">
              <option value="tutorial">Tutorials</option>
              <option value="lab">Lab Work</option>
              <option value="both">Both Tutorial & Lab</option>
              <option value="none">None Required</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Minimum Number Required
            </label>
            <input 
              type="number" 
              v-model.number="config.practicalMaterials.minCount" 
              min="0" 
              max="15"
              class="w-full border rounded px-3 py-2"
              :disabled="config.practicalMaterials.type === 'none'"
            />
          </div>
        </div>

        <div v-if="config.practicalMaterials.type === 'both'" class="mt-3">
          <label class="flex items-center gap-2 text-sm">
            <input type="checkbox" v-model="config.practicalMaterials.requireSolutions" class="rounded" />
            <span class="text-gray-700">Require solution files</span>
          </label>
        </div>
      </div>

      <!-- Section 5: Assessment Types -->
      <div class="border rounded-lg p-4 bg-gray-50">
        <h3 class="font-semibold text-gray-800 mb-3">📝 5.0 Assessments and Marking Schemes</h3>
        
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Select Assessment Types for This Unit
            </label>
            <div class="grid grid-cols-2 gap-2">
              <label class="flex items-center gap-2 p-2 border rounded hover:bg-white cursor-pointer">
                <input type="checkbox" v-model="config.assessments.hasAssignments" class="rounded" />
                <span class="text-sm">Assignments</span>
              </label>
              <label class="flex items-center gap-2 p-2 border rounded hover:bg-white cursor-pointer">
                <input type="checkbox" v-model="config.assessments.hasTests" class="rounded" />
                <span class="text-sm">Tests/Quizzes</span>
              </label>
              <label class="flex items-center gap-2 p-2 border rounded hover:bg-white cursor-pointer">
                <input type="checkbox" v-model="config.assessments.hasProject" class="rounded" />
                <span class="text-sm">Project</span>
              </label>
              <label class="flex items-center gap-2 p-2 border rounded hover:bg-white cursor-pointer">
                <input type="checkbox" v-model="config.assessments.hasFinalExam" class="rounded" />
                <span class="text-sm">Final Exam</span>
              </label>
            </div>
          </div>

          <div v-if="config.assessments.hasAssignments" class="pl-4 border-l-2 border-blue-300">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Number of Assignments
            </label>
            <input 
              type="number" 
              v-model.number="config.assessments.assignmentCount" 
              min="1" 
              max="5"
              class="w-32 border rounded px-3 py-2"
            />
          </div>

          <div v-if="config.assessments.hasTests" class="pl-4 border-l-2 border-blue-300">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Number of Tests
            </label>
            <input 
              type="number" 
              v-model.number="config.assessments.testCount" 
              min="1" 
              max="5"
              class="w-32 border rounded px-3 py-2"
            />
          </div>
        </div>
      </div>

      <!-- Section 6: Student Work Sampling -->
      <div class="border rounded-lg p-4 bg-gray-50">
        <h3 class="font-semibold text-gray-800 mb-3">👥 6.0 Student Work Sampling</h3>
        
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Sampling Percentage (Minimum 20%)
            </label>
            <div class="flex items-center gap-4">
              <input 
                type="range" 
                v-model.number="config.sampling.percentage" 
                min="20" 
                max="100"
                class="flex-1"
              />
              <span class="text-lg font-bold text-purple-600 w-16 text-right">
                {{ config.sampling.percentage }}%
              </span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Performance Band Ranges
            </label>
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <span class="w-20 text-sm text-green-700 font-medium">Good:</span>
                <input type="number" v-model.number="config.sampling.goodMin" min="0" max="100" class="w-20 border rounded px-2 py-1" />
                <span class="text-sm">to</span>
                <input type="number" v-model.number="config.sampling.goodMax" min="0" max="100" class="w-20 border rounded px-2 py-1" />
              </div>
              <div class="flex items-center gap-2">
                <span class="w-20 text-sm text-yellow-700 font-medium">Average:</span>
                <input type="number" v-model.number="config.sampling.avgMin" min="0" max="100" class="w-20 border rounded px-2 py-1" />
                <span class="text-sm">to</span>
                <input type="number" v-model.number="config.sampling.avgMax" min="0" max="100" class="w-20 border rounded px-2 py-1" />
              </div>
              <div class="flex items-center gap-2">
                <span class="w-20 text-sm text-red-700 font-medium">Poor:</span>
                <input type="number" v-model.number="config.sampling.poorMin" min="0" max="100" class="w-20 border rounded px-2 py-1" />
                <span class="text-sm">to</span>
                <input type="number" v-model.number="config.sampling.poorMax" min="0" max="100" class="w-20 border rounded px-2 py-1" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section 8 & 9: Optional Sections -->
      <div class="border rounded-lg p-4 bg-gray-50">
        <h3 class="font-semibold text-gray-800 mb-3">⚠️ Optional Sections</h3>
        
        <div class="space-y-2">
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="config.optional.requireSafety" class="rounded" />
            <span class="text-sm">This unit requires Safety Acknowledgement (8.0)</span>
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="config.optional.requireExamScripts" class="rounded" />
            <span class="text-sm">This unit requires Final Exam Scripts (9.0)</span>
          </label>
        </div>
      </div>

    </div>

    <!-- Action Buttons -->
    <div class="flex justify-between items-center mt-6 pt-4 border-t">
      <button 
        @click="exportConfig"
        class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        Export Config
      </button>

      <button 
        @click="saveConfig"
        class="px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition-colors flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        Save Configuration
      </button>
    </div>

    <!-- Current Config Summary -->
    <div class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded text-sm">
      <p class="font-semibold text-blue-800 mb-1">Current Configuration:</p>
      <p class="text-blue-700">
        {{ config.learningMaterials.type }}s (min {{ config.learningMaterials.minCount }}), 
        {{ config.practicalMaterials.type }} (min {{ config.practicalMaterials.minCount }}), 
        {{ assessmentSummary }}, 
        {{ config.sampling.percentage }}% sampling
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const isExpanded = ref(false)

const emit = defineEmits(['config-updated'])

const config = ref({
  learningMaterials: {
    type: 'lecture',
    minCount: 6
  },
  practicalMaterials: {
    type: 'tutorial',
    minCount: 3,
    requireSolutions: true
  },
  assessments: {
    hasAssignments: true,
    hasTests: true,
    hasProject: false,
    hasFinalExam: false,
    assignmentCount: 2,
    testCount: 1
  },
  sampling: {
    percentage: 20,
    goodMin: 70,
    goodMax: 100,
    avgMin: 50,
    avgMax: 69,
    poorMin: 0,
    poorMax: 49
  },
  optional: {
    requireSafety: false,
    requireExamScripts: false
  }
})

const assessmentSummary = computed(() => {
  const types = []
  if (config.value.assessments.hasAssignments) types.push(`${config.value.assessments.assignmentCount} assignment(s)`)
  if (config.value.assessments.hasTests) types.push(`${config.value.assessments.testCount} test(s)`)
  if (config.value.assessments.hasProject) types.push('project')
  if (config.value.assessments.hasFinalExam) types.push('final exam')
  return types.join(', ') || 'no assessments'
})

const resetToDefaults = () => {
  if (confirm('Reset all configuration to default values?')) {
    config.value = {
      learningMaterials: { type: 'lecture', minCount: 6 },
      practicalMaterials: { type: 'tutorial', minCount: 3, requireSolutions: true },
      assessments: {
        hasAssignments: true,
        hasTests: true,
        hasProject: false,
        hasFinalExam: false,
        assignmentCount: 2,
        testCount: 1
      },
      sampling: {
        percentage: 20,
        goodMin: 70,
        goodMax: 100,
        avgMin: 50,
        avgMax: 69,
        poorMin: 0,
        poorMax: 49
      },
      optional: {
        requireSafety: false,
        requireExamScripts: false
      }
    }
  }
}

const saveConfig = () => {
  emit('config-updated', config.value)
  alert('✅ Configuration saved! Validation rules will use these settings.')
}

const exportConfig = () => {
  const dataStr = JSON.stringify(config.value, null, 2)
  const blob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `unit_config_${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
}
</script>