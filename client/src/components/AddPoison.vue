<script setup>
import { ref } from 'vue'
const emit = defineEmits(['fetchUpdate'])

const addPotionModal = ref(false)
const name = ref('')
const difficulty = ref('')
const ingredients = ref('')
const effect = ref('')

const togglePotionModal = (e) => {
  e.stopPropagation()
  addPotionModal.value = !addPotionModal.value
}

const handleSubmitPotion = async () => {
  const newPotion = {
    name: name.value,
    difficulty: difficulty.value,
    ingredients: ingredients.value
      .split(',')
      .map((ing) => ing.trim())
      .filter(Boolean),
    effect: effect.value
  }

  try {
    const response = await fetch(`${import.meta.env.VITE_SERVER_URL}//api/potions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newPotion)
    })

    if (!response.ok) {
      throw new Error('Ошибка при добавлении зелья')
    }

    const result = await response.json()
    console.log('Успешно отправлено:', result)
    console.log('Добавлено зелье:', newPotion)

    togglePotionModal(new Event('click'))
    name.value = ''
    difficulty.value = ''
    ingredients.value = ''
    effect.value = ''
  } catch (error) {
    console.error('Ошибка при отправке:', error)
    alert('Произошла ошибка при добавлении зелья.')
  } finally {
    emit('fetchUpdate', `${import.meta.env.VITE_SERVER_URL}/api/potions`)
  }
}
</script>

<template>
  <li class="flex justify-center" @click="togglePotionModal">
    <div class="w-[250px] bg-bg flex flex-col items-center justify-center pt-2 rounded-[10px] cursor-pointer">
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
              v-model="name"
              type="text"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display"
              placeholder="Enter potion name"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Difficulty</label>
            <textarea
              v-model="difficulty"
              rows="1"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display resize-none"
              placeholder="Enter difficulty"
            ></textarea>
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Ingredients</label>
            <input
              v-model="ingredients"
              type="text"
              placeholder="Comma-separated ingredients"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Effect</label>
            <input
              v-model="effect"
              type="text"
              placeholder="Potion effect"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div class="flex justify-between">
            <button
              @click="handleSubmitPotion"
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
