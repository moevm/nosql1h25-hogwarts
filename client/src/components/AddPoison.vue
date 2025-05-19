<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'
const emit = defineEmits(['fetchUpdate'])

const addPotionModal = ref(false)
const form = ref({
  name: '',
  difficulty: '',
  ingredients: '',
  effect: '',
  image_path: ''
})

const filters = ref({
  difficulty: [],
  ingredients: []
})

const togglePotionModal = (e) => {
  e.stopPropagation()
  addPotionModal.value = !addPotionModal.value
}

const updatePotion = async () => {
  const newPotion = {
    ...form.value,
    ingredients: form.value.ingredients.split(',').map((i) => i.trim()).join(', ')
  }

  try {
    const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/potions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newPotion)
    })

    if (!response.ok) {
      throw new Error('Ошибка при добавлении зелья')
    }

    const result = await response.json()
    console.log('Успешно отправлено:', result)

    togglePotionModal(new Event('click'))
    form.value = { name: '', difficulty: '', ingredients: '', effect: '', image_path: '' }
  } catch (error) {
    console.error('Ошибка при отправке:', error)
    alert('Произошла ошибка при добавлении зелья.')
  } finally {
    emit('fetchUpdate', `${import.meta.env.VITE_SERVER_URL}/api/potions`)
  }
}

onMounted(async () => {
  const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/potions/filters`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  })
  const data = await response.json()
  filters.value = data
})

function toggleIngredient(item) {
  const ingredientsArray = form.value.ingredients.split(',').map(i => i.trim())
  const index = ingredientsArray.indexOf(item)
  if (index > -1) {
    ingredientsArray.splice(index, 1)
  } else {
    ingredientsArray.push(item)
  }
  form.value.ingredients = ingredientsArray.join(', ')
}
</script>

<template>
  <li class="flex justify-center h-[300px]" @click="togglePotionModal">
    <div class="w-[220px] bg-bg flex flex-col items-center justify-center pt-2 rounded-[10px] cursor-pointer">
      <img class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed" src="/images/add.svg" />
      <p class="text-gold text-lg">Add Potion</p>
    </div>

    <div
      v-if="addPotionModal"
      class="w-[700px] h-[400px] absolute bg-bg top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] rounded-[10px] border-2 border-gold p-6 overflow-y-auto"
      @click.stop
    >
      <div class="relative w-full h-[500px] flex flex-col justify-between">
        <button
          class="absolute top-4 right-4 border border-gold w-10 h-10 rounded-[10px] text-gold text-xl"
          @click="togglePotionModal"
        >
          ×
        </button>

        <div class="flex flex-col gap-4 mt-8">
          <div>
            <label class="block mb-2 text-gold text-lg font-display">Name</label>
            <input
              v-model="form.name"
              type="text"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display"
              placeholder="Enter potion name"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Difficulty</label>
            <select
              v-model="form.difficulty"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display"
            >
              <option disabled value="">Select difficulty</option>
              <option v-for="level in filters.difficulty" :key="level" :value="level">
                {{ level }}
              </option>
            </select>
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Effect</label>
            <input
              v-model="form.effect"
              type="text"
              placeholder="Potion effect"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Ingredients</label>
            <div class="flex flex-wrap gap-2 mt-2">
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

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Image URL</label>
            <input
              v-model="form.image_path"
              type="text"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
              placeholder="Enter image URL"
            />
          </div>

          <div class="flex justify-between">
            <button
              @click="updatePotion"
              class="px-6 py-2 border border-gold text-gold rounded-md font-display hover:bg-gold hover:text-bg transition"
            >
              Add Potion
            </button>
          </div>
        </div>
      </div>
    </div>
  </li>
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
