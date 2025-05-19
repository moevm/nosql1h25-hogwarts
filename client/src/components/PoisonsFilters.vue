<script setup>
import { reactive, ref, watch, onMounted } from 'vue'

const emit = defineEmits(['makeOptions'])

const filters = reactive({
  difficulty: '',
  ingredients: [], // теперь массив
  effect: ''
})

// Доступные значения с сервера
const availableFilters = ref({
  difficulty: [],
  ingredients: []
})

// Загрузка доступных фильтров
onMounted(async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/potions/filters`)
    const data = await response.json()
    availableFilters.value = data
  } catch (err) {
    console.error('Failed to fetch filter options:', err)
  }
})

// Слежение за фильтрами
watch(
  () => filters,
  () => {
    const options = Object.entries(filters)
      .filter(([_, value]) => {
        // для ingredients — массив, у которого есть длина
        if (Array.isArray(value)) return value.length > 0
        return !!value
      })
      .map(([key, value]) => ({
        key,
        value: Array.isArray(value) ? value.join(',') : value
      }))
    emit('makeOptions', options)
  },
  { deep: true }
)

// Переключение ингредиента (тег)
function toggleIngredient(item) {
  const index = filters.ingredients.indexOf(item)
  if (index !== -1) {
    filters.ingredients.splice(index, 1)
  } else {
    filters.ingredients.push(item)
  }
}
</script>

<template>
  <div class="flex flex-col gap-4 w-full">
    <!-- Effect -->
    <div class="text-gold">
      Effect:
      <input
        v-model="filters.effect"
        class="text-gold outline-none border border-gold rounded-md ml-2 px-2 py-1 bg-transparent"
        placeholder="e.g. causes laughter"
      />
    </div>

    <!-- Difficulty -->
    <div class="text-gold">
      Difficulty:
      <select
        v-model="filters.difficulty"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option value="">--</option>
        <option v-for="level in availableFilters.difficulty" :key="level" :value="level">
          {{ level }}
        </option>
      </select>
    </div>

    <!-- Ingredients (теги) -->
    <div class="text-gold">
      Ingredients:
      <div class="flex flex-wrap gap-2 mt-2 ml-2">
        <button
          v-for="item in availableFilters.ingredients"
          :key="item"
          type="button"
          class="tag"
          :class="{ 'selected': filters.ingredients.includes(item) }"
          @click="toggleIngredient(item)"
        >
          {{ item }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tag {
  padding: 0.3em 0.8em;
  border: 1px solid gold;
  border-radius: 20px;
  cursor: pointer;
  background-color: transparent;
  color: gold;
  transition: all 0.2s ease;
}

.tag.selected {
  background-color: gold;
  color: #093062;
  font-weight: bold;
}
</style>
