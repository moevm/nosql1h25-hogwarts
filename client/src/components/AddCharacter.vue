<script setup>
import { ref } from 'vue'
import RelationEditor from './RelationsEditor.vue'

const emit = defineEmits(['fetchUpdate'])

const addItemModal = ref(false)
const name = ref('')
const description = ref('')
const imagePath = ref('')
const born = ref('')
const died = ref('')
const bloodStatus = ref('')
const gender = ref('')
const house = ref('')
const spells = ref('')
const poisons = ref('')
const relationships = ref([])

const toggleModal = (e) => {
  e.stopPropagation()
  addItemModal.value = !addItemModal.value
}

const handleSubmit = async () => {
  const id = name.value.toLowerCase().replace(/\s+/g, '-')

  const newItem = {
    id,
    name: name.value,
    born: born.value || null,
    died: died.value || null,
    blood_status: bloodStatus.value,
    gender: gender.value,
    description: description.value,
    house: house.value,
    image_path: imagePath.value,
    spells: spells.value
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean),
    poisons: poisons.value
      .split(',')
      .map((p) => p.trim())
      .filter(Boolean),
    relationships: relationships.value
  }

  try {
    const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newItem)
    })

    if (!response.ok) throw new Error('Ошибка при добавлении персонажа')

    alert('Персонаж добавлен!')
    toggleModal(new Event('click'))

    // очистка
    name.value = ''
    description.value = ''
    born.value = ''
    died.value = ''
    bloodStatus.value = ''
    gender.value = ''
    house.value = ''
    spells.value = ''
    poisons.value = ''
    imagePath.value = ''
    relationships.value = []

    emit('fetchUpdate', `${import.meta.env.VITE_SERVER_URL}/api/characters`)
  } catch (error) {
    console.error(error)
    alert('Произошла ошибка при добавлении персонажа.')
  }
}
</script>

<template>
  <li class="flex justify-center" @click="toggleModal">
    <div
      class="w-[220px] bg-bg flex flex-col items-center justify-center pt-2 rounded-[10px] cursor-pointer"
    >
      <img class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed" src="/images/add.svg" />
      <p class="text-gold text-lg">Add Character</p>
    </div>

    <div
      v-if="addItemModal"
      class="w-[700px] h-[90vh] absolute bg-bg top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] rounded-[10px] border-2 border-gold p-6 overflow-y-auto text-gold"
      @click.stop
    >
      <div class="relative flex flex-col gap-4">
        <button
          class="absolute top-0 right-0 border border-gold w-10 h-10 rounded-[10px] text-gold text-xl"
          @click="toggleModal"
        >
          ×
        </button>

        <label class="mt-8">Name: <input v-model="name" class="input" /></label>
        <label>Description: <textarea v-model="description" class="input" rows="2" /></label>
        <label>Born: <input v-model="born" type="date" class="input" /></label>
        <label>Died: <input v-model="died" type="date" class="input" /></label>

        <label
          >Blood Status:
          <select v-model="bloodStatus" class="input">
            <option value="">--</option>
            <option value="Pure-blood">Pure-blood</option>
            <option value="Half-blood">Half-blood</option>
            <option value="Muggle-born">Muggle-born</option>
          </select>
        </label>

        <label
          >Gender:
          <select v-model="gender" class="input">
            <option value="">--</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </label>

        <label
          >House:
          <select v-model="house" class="input">
            <option value="">--</option>
            <option value="Gryffindor">Gryffindor</option>
            <option value="Ravenclaw">Ravenclaw</option>
            <option value="Hufflepuff">Hufflepuff</option>
            <option value="Slytherin">Slytherin</option>
          </select>
        </label>
        <label
          >Image URL: <input v-model="imagePath" placeholder="https://..." class="input"
        /></label>

        <RelationEditor v-model="relationships" />

        <div class="flex justify-end">
          <button
            @click="handleSubmit"
            class="px-6 py-2 border border-gold text-gold rounded-md font-display hover:bg-gold hover:text-bg transition"
          >
            Add
          </button>
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
  display: block;
  width: 100%;
}
</style>
