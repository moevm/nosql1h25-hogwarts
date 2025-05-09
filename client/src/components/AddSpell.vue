<script setup>
import { ref } from 'vue'
import RelationEditor from './RelationsEditor.vue'

const emit = defineEmits(['fetchUpdate'])

const addSpellModal = ref(false)
const name = ref('')
const light = ref('')
const category = ref('')
const effect = ref('')
const relationships = ref([])

const toggleSpellModal = (e) => {
  e.stopPropagation()
  addSpellModal.value = !addSpellModal.value
}

const handleSubmitSpell = async () => {
  const newSpell = {
    name: name.value,
    light: light.value,
    category: category.value,
    effect: effect.value,
    relationships: relationships.value
  }

  try {
    const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/spells`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newSpell)
    })

    if (!response.ok) {
      throw new Error('Ошибка при добавлении зелья')
    }

    const result = await response.json()
    console.log('Успешно отправлено:', result)
    console.log('Добавлено заклинание:', newSpell)

    toggleSpellModal(new Event('click'))
    name.value = ''
    light.value = ''
    category.value = ''
    effect.value = ''
    relationships.value = []
  } catch (error) {
    console.error('Ошибка при отправке:', error)
    alert('Произошла ошибка при добавлении заклинания.')
  } finally {
    emit('fetchUpdate', `${import.meta.env.VITE_SERVER_URL}/api/spells`)
  }
}
</script>

<template>
  <li class="flex justify-center" @click="toggleSpellModal">
    <div
      class="w-[250px] bg-bg flex flex-col items-center justify-center pt-2 rounded-[10px] cursor-pointer"
    >
      <img class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed" src="/images/add.svg" />
      <p class="text-gold text-lg">Add Spell</p>
    </div>

    <div
      v-if="addSpellModal"
      class="w-[700px] h-[400px] absolute bg-bg top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] rounded-[10px] border-2 border-gold p-6 overflow-y-auto"
      @click.stop
    >
      <div class="relative w-full h-[500px] flex flex-col justify-between">
        <button
          class="absolute top-4 right-4 border border-gold w-10 h-10 rounded-[10px] text-gold text-xl"
          @click="toggleSpellModal"
        >
          ×
        </button>

        <div class="flex flex-col gap-4 mt-8">
          <div>
            <label class="block mb-2 text-gold text-lg font-display">Name</label>
            <input
              v-model="name"
              type="text"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display"
              placeholder="Enter spell name"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Light</label>
            <textarea
              v-model="Light"
              rows="1"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display resize-none"
              placeholder="Enter light color"
            ></textarea>
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Category</label>
            <input
              v-model="category"
              type="text"
              placeholder="Enter category"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Effect</label>
            <input
              v-model="effect"
              type="text"
              placeholder="Spell effect"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>
          <RelationEditor v-model="relationships" />

          <div class="flex justify-between">
            <button
              @click="handleSubmitSpell"
              class="px-6 py-2 border border-gold text-gold rounded-md font-display hover:bg-gold hover:text-bg transition"
            >
              Add Spell
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
