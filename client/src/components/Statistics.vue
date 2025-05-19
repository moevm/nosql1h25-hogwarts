<template>
  <div>
    <!-- Statistics Button -->
    <TopButton action="Statistics" @click="openModal" />

    <!-- Configuration Modal -->
    <transition name="fade">
      <div v-if="isModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-bg rounded-lg p-6 w-full max-w-2xl border border-gold">
          <h2 class="text-2xl text-gold mb-4">Statistics Configuration</h2>

          <!-- Steps Navigation -->
          <div class="mb-6 flex space-x-4">
            <button
              v-for="(stepName, idx) in stepNames"
              :key="idx"
              @click="currentStep = idx"
              :class="[
                'px-4 py-2 rounded-lg font-display',
                currentStep === idx ? 'bg-gold text-bg' : 'bg-gray-700 text-gold'
              ]"
            >{{ stepName }}</button>
          </div>

          <!-- Step 1: Entity -->
          <div v-if="currentStep === 0" class="space-y-4">
            <label class="block text-gold font-medium">Entity:</label>
            <select v-model="form.entity" class="w-full p-2 rounded-lg bg-transparent border border-gold text-gold">
              <option disabled value="">-- Select Entity --</option>
              <option v-for="ent in entities" :key="ent" :value="ent" class="bg-bg text-gold">{{ ent }}</option>
            </select>
          </div>

          <!-- Step 2: Filters -->
          <div v-if="currentStep === 1" class="space-y-4">
            <h3 class="text-lg text-gold">Filters for {{ form.entity }}</h3>

            <!-- Character filters -->
            <div v-if="form.entity === 'Character'" class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-gold">Blood Status</label>
                <select v-model="form.filters.blood_status" class="w-full p-2 rounded-lg bg-transparent border border-gold text-gold">
                  <option value="" class="bg-bg text-gold">-- Any --</option>
                  <option value="Pure-blood">Pure-blood</option>
                  <option value="Half-blood">Half-blood</option>
                  <option value="Muggle-born">Muggle-born</option>
                </select>
              </div>
              <div>
                <label class="block text-gold">House</label>
                <select v-model="form.filters.house" class="w-full p-2 rounded-lg bg-transparent border border-gold text-gold">
                  <option value="" class="bg-bg text-gold">-- Any --</option>
                  <option>Gryffindor</option>
                  <option>Slytherin</option>
                  <option>Ravenclaw</option>
                  <option>Hufflepuff</option>
                </select>
              </div>
              <div>
                <label class="block text-gold">Gender</label>
                <select v-model="form.filters.gender" class="w-full p-2 rounded-lg bg-transparent border border-gold text-gold">
                  <option value="" class="bg-bg text-gold">-- Any --</option>
                  <option>Male</option>
                  <option>Female</option>
                </select>
              </div>
              <div>
                <label class="block text-gold">Born Year</label>
                <div class="flex space-x-2">
                  <input v-model.number="form.filters.born_min" type="number" placeholder="from" class="w-1/2 p-2 rounded-lg bg-transparent border border-gold text-gold" />
                  <input v-model.number="form.filters.born_max" type="number" placeholder="to" class="w-1/2 p-2 rounded-lg bg-transparent border border-gold text-gold" />
                </div>
              </div>
              <div>
                <label class="block text-gold">Died Year</label>
                <div class="flex space-x-2">
                  <input v-model.number="form.filters.died_min" type="number" placeholder="from" class="w-1/2 p-2 rounded-lg bg-transparent border border-gold text-gold" />
                  <input v-model.number="form.filters.died_max" type="number" placeholder="to" class="w-1/2 p-2 rounded-lg bg-transparent border border-gold text-gold" />
                </div>
              </div>
            </div>

            <!-- Potions filters -->
            <div v-if="form.entity === 'Poison'" class="space-y-4">
              <label class="block text-gold">Difficulty</label>
              <select v-model="form.filters.difficulty" class="w-full p-2 rounded-lg bg-transparent border border-gold text-gold">
                <option value="" class="bg-bg text-gold">-- Any --</option>
                <option v-for="lvl in potionsFilters.difficulty" :key="lvl">{{ lvl }}</option>
              </select>

              <label class="block text-gold">Ingredients</label>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="ing in potionsFilters.ingredients"
                  :key="ing"
                  type="button"
                  class="tag"
                  :class="{ 'selected': selectedIngredients.includes(ing) }"
                  @click="toggleIngredient(ing)"
                >{{ ing }}</button>
              </div>
            </div>

            <!-- Spell filters -->
            <div v-if="form.entity === 'Spell'" class="space-y-4">
              <label class="block text-gold">Category</label>
              <select v-model="form.filters.category" class="w-full p-2 rounded-lg bg-transparent border border-gold text-gold">
                <option value="" class="bg-bg text-gold">-- Any --</option>
                <option v-for="opt in spellFilters.category" :key="opt">{{ opt }}</option>
              </select>

              <label class="block text-gold">Light</label>
              <select v-model="form.filters.light" class="w-full p-2 rounded-lg bg-transparent border border-gold text-gold">
                <option value="" class="bg-bg text-gold">-- Any --</option>
                <option v-for="opt in spellFilters.light" :key="opt">{{ opt }}</option>
              </select>
            </div>
          </div>

          <!-- Step 3: Axes -->
          <div v-if="currentStep === 2" class="space-y-4">
            <label class="block text-gold">X Axis:</label>
            <select v-model="form.x_axis" class="w-full p-2 rounded-lg bg-transparent border border-gold text-gold">
              <option disabled value="" class="bg-bg text-gold">-- Select Field --</option>
              <option v-for="f in axisFields" :key="f">{{ f }}</option>
            </select>
            <label class="block text-gold">Y Axis:</label>
            <select v-model="form.y_axis" class="w-full p-2 rounded-lg bg-transparent border border-gold text-gold">
              <option disabled value="" class="bg-bg text-gold">-- Select Field --</option>
              <option v-for="f in axisFields" :key="f">{{ f }}</option>
            </select>
          </div>

          <!-- Footer -->
          <div class="mt-6 flex justify-end space-x-4">
            <button @click="closeModal" class="px-4 py-2 bg-gray-700 text-gold rounded-lg">Cancel</button>
            <button @click="onSubmit" :disabled="!isFormComplete" class="px-4 py-2 bg-gold text-bg rounded-lg disabled:opacity-50">Submit</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Chart Modal -->
    <transition name="fade">
      <div v-if="chartModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-bg rounded-lg p-6 w-full max-w-3xl border border-gold">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl text-gold">Statistics Results</h2>
            <button @click="closeChart" class="text-gold text-2xl">×</button>
          </div>
          <ChartComponent :data="chartData" :xAxis="form.x_axis" :yAxis="form.y_axis" />
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import TopButton from './TopButton.vue'
import ChartComponent from './Charts.vue'

const entities = ['Character', 'Poison', 'Spell']
const axisOptions = {
  Character: ['house', 'blood_status', 'gender'],
  Poison: ['difficulty', 'ingredients'],
  Spell: ['category', 'light']
}

const isModalOpen = ref(false)
const chartModal = ref(false)
const currentStep = ref(0)

const form = reactive({
  entity: '',
  filters: {
    born_min: null, born_max: null, died_min: null, died_max: null,
    blood_status: '', house: '', gender: '',
    difficulty: '', ingredients: [],
    category: '', light: ''
  },
  x_axis: '', y_axis: ''
})
const chartData = ref(null)
const stepNames = ['Entity', 'Filters', 'Axes']

const potionsFilters = reactive({ difficulty: [], ingredients: [] })
const spellFilters = reactive({ category: [], light: [] })

const axisFields = computed(() => axisOptions[form.entity] || [])
const isFormComplete = computed(() => form.entity && form.x_axis && form.y_axis)

watch(() => form.entity, async (ent) => {
  form.x_axis = ''
  form.y_axis = ''
  currentStep.value = 0
  if (ent === 'Poison') {
    const { difficulty, ingredients } = await fetch(
      `${import.meta.env.VITE_SERVER_URL}/api/potions/filters`
    ).then(r => r.json())
    potionsFilters.difficulty = difficulty
    potionsFilters.ingredients = ingredients
    form.filters.difficulty = ''
    form.filters.ingredients = []
  } else if (ent === 'Spell') {
    const { category, light } = await fetch(
      `${import.meta.env.VITE_SERVER_URL}/api/spells/filters`
    ).then(r => r.json())
    spellFilters.category = category
    spellFilters.light = light
    form.filters.category = ''
    form.filters.light = ''
  }
})

function openModal() { isModalOpen.value = true }
function closeModal() { isModalOpen.value = false }
function closeChart() { chartModal.value = false }

const selectedIngredients = computed(() => form.filters.ingredients)
function toggleIngredient(item) {
  const idx = form.filters.ingredients.indexOf(item)
  if (idx > -1) form.filters.ingredients.splice(idx, 1)
  else form.filters.ingredients.push(item)
}

async function onSubmit() {
  const clean = {}
  for (const [k, v] of Object.entries(form.filters)) {
    if (Array.isArray(v) ? v.length : v) clean[k] = v
  }
  const { data } = await fetch(
    `${import.meta.env.VITE_SERVER_URL}/api/statistics`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        entity: form.entity,
        filters: clean,
        x_axis: form.x_axis,
        y_axis: form.y_axis
      })
    }
  ).then(r => r.json())
  chartData.value = data
  closeModal()
  chartModal.value = true
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s }
.fade-enter-from, .fade-leave-to { opacity: 0 }
.tag { padding: .3em .8em; border:1px solid gold; border-radius:20px; cursor:pointer; color:gold }
.tag.selected { background:gold; color:#093062; font-weight:bold }
@media (min-width:640px){ .grid-cols-2{ display:grid; grid-template-columns:repeat(2,1fr); gap:1rem } }
</style>
