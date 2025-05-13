<script setup>
import { onMounted, ref } from 'vue'

const props = defineProps({
  character: Object
})
const emit = defineEmits(['saved'])

const addCharacterModal = ref(false)
const form = ref({ ...props.character })
const filters = ref({})

const toggleCharacterModal = (e) => {
  e.stopPropagation()
  addCharacterModal.value = !addCharacterModal.value
}

const createCharacter = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })

    if (!response.ok) {
      throw new Error('Ошибка при создании персонажа')
    }

    const result = await response.json()
    console.log('Персонаж создан:', result)
    emit('saved')
    toggleCharacterModal(new Event('click'))  // Закрыть модальное окно после успешного создания
  } catch (error) {
    console.error('Ошибка при отправке:', error)
    alert('Произошла ошибка при создании персонажа.')
  }
}

onMounted(async () => {
  filters.value = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters/filters`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  }).then((res) => res.json())

  console.log(filters.value)
})
</script>

<template>
  <li class="flex justify-center" @click="toggleCharacterModal">
    <div
      class="w-[250px] bg-bg flex flex-col items-center justify-center pt-2 rounded-[10px] cursor-pointer"
    >
      <img class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed" src="/images/add.svg" />
      <p class="text-gold text-lg">Create Character</p>
    </div>

    <!-- Модальное окно -->
    <div
      v-if="addCharacterModal"
      class="w-[700px] h-[400px] absolute bg-bg top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] rounded-[10px] border-2 border-gold p-6 overflow-y-auto"
      @click.stop
    >
      <div class="relative w-full h-[500px] flex flex-col justify-between">
        <button
          class="absolute top-4 right-4 border border-gold w-10 h-10 rounded-[10px] text-gold text-xl"
          @click="toggleCharacterModal"
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
              placeholder="Enter character name"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Role</label>
            <input
              v-model="form.role"
              type="text"
              placeholder="Enter character role"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Description</label>
            <textarea
              v-model="form.description"
              rows="3"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display resize-none"
              placeholder="Enter character description"
            ></textarea>
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
              @click="createCharacter"
              class="px-6 py-2 border border-gold text-gold rounded-md font-display hover:bg-gold hover:text-bg transition"
            >
              Create
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
  display: block;
  width: 100%;
}
</style>
