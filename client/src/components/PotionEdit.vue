<script setup>
import { onMounted, ref } from 'vue'

const props = defineProps({
  potion: Object
})
const emit = defineEmits(['saved'])

const form = ref({
  ...props.potion,
  // Убедимся, что ingredients — это строка
  ingredients: props.potion.ingredients || '', // строка ингредиентов
})

const filters = ref({
  difficulty: [],
  ingredients: []
})

const updatePotion = async () => {
  await fetch(`${import.meta.env.VITE_SERVER_URL}/api/potions/${form.value.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...form.value,
      ingredients: form.value.ingredients.split(',').map((i) => i.trim()).join(', ') // преобразуем строку в массив и обратно
    })
  })
  emit('saved')
}

onMounted(async () => {
  const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/potions/filters`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  })
  const data = await response.json()
  filters.value = data
})

function toggleIngredient(item) {
  const ingredientsArray = form.value.ingredients.split(',').map(i => i.trim()) // разбиваем строку на массив
  const index = ingredientsArray.indexOf(item)
  if (index > -1) {
    ingredientsArray.splice(index, 1)
  } else {
    ingredientsArray.push(item)
  }
  form.value.ingredients = ingredientsArray.join(', ') // сохраняем обратно строку
}
</script>

<template>
  <form @submit.prevent="updatePotion" class="text-gold space-y-4">

    <label>Name:
      <input v-model="form.name" class="input" />
    </label>

    <label>Difficulty:
      <select v-model="form.difficulty" class="input">
        <option disabled value="">Select difficulty</option>
        <option v-for="level in filters.difficulty" :key="level" :value="level">
          {{ level }}
        </option>
      </select>
    </label>

    <label>Effect:
      <input v-model="form.effect" class="input" />
    </label>

    <div>
      <label>Ingredients:</label>
      <div class="flex flex-wrap gap-2 mt-2 max-h-[500px] overflow-y-scroll">
        <button
          v-for="item in filters.ingredients"
          :key="item"
          type="button"
          class="tag"
          :class="{ 'selected': form.ingredients.split(',').map(i => i.trim()).includes(item) }" 
          @click="toggleIngredient(item)"
        >
          {{ item }}
        </button>
      </div>
    </div>

    <label>Image URL:
      <input v-model="form.image_path" class="input" />
    </label>

    <button type="submit" class="bg-gold text-bg px-4 py-2 rounded">Save</button>
  </form>
</template>

<style scoped>
.input {
  background-color: #093062;
  border: 1px solid gold;
  color: gold;
  padding: 0.5em;
  border-radius: 4px;
  width: 100%;
}

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
