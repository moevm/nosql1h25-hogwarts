<script setup>
import { onMounted, ref } from 'vue'

const props = defineProps({
  Spell: Object
})
const emit = defineEmits(['saved'])

const addSpellModal = ref(false)
const form = ref({ ...props.Spell })
const filters = ref({})

const toggleSpellModal = (e) => {
  e.stopPropagation()
  addSpellModal.value = !addSpellModal.value
}

const createSpell = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/spells`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })

    if (!response.ok) {
      throw new Error('Ошибка при создании персонажа')
    }

    const result = await response.json()
    emit('saved')
    toggleSpellModal(new Event('click'))
  } catch (error) {
    console.error('Ошибка при отправке:', error)
    alert('Произошла ошибка при создании персонажа.')
  }
}

onMounted(async () => {
  filters.value = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/spells/filters`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  }).then((res) => res.json())

  console.log(filters.value)
})
</script>
<template>
  <li class="flex justify-center" @click="toggleSpellModal">
    <div class="w-[220px] bg-bg flex flex-col items-center justify-center pt-2 rounded-[10px] cursor-pointer">
      <img class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed" src="/images/add.svg" />
      <p class="text-gold text-lg">Create Spell</p>
    </div>

    <!-- Модальное окно -->
    <div
      v-if="addSpellModal"
      class="w-[700px] h-[500px] absolute bg-bg top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] rounded-[10px] border-2 border-gold p-6 overflow-y-auto"
      @click.stop
    >
      <div class="relative w-full h-full flex flex-col justify-between">
        <button
          class="absolute top-4 right-4 border border-gold w-10 h-10 rounded-[10px] text-gold text-xl"
          @click="toggleSpellModal"
        >
          ×
        </button>

        <form @submit.prevent="createSpell" class="flex flex-col gap-4 mt-8 text-gold">
          <label>
            Name:
            <input v-model="form.name" class="input" type="text" placeholder="Enter name" />
          </label>

          <label>
            Effect:
            <input v-model="form.effect" class="input" type="text" placeholder="Enter effect" />
          </label>

          <label>
            Light:
            <select v-model="form.light" class="input">
              <option v-for="option in filters.light" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </label>

          <label>
            Category:
            <select v-model="form.category" class="input">
              <option v-for="option in filters.category" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </label>

          <label>
            Image URL:
            <input v-model="form.image_path" class="input" type="text" placeholder="Enter image URL" />
          </label>

          <button
            type="submit"
            class="px-6 py-2 border border-gold text-gold rounded-md font-display hover:bg-gold hover:text-bg transition"
          >
            Create
          </button>
        </form>
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
</style>

