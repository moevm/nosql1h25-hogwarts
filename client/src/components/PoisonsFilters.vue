<script setup>
import { reactive, watch } from 'vue'

const emit = defineEmits(['makeOptions'])

const filters = reactive({
  characteristics: '',
  ingredients: '',
  difficulty: '',
  founder: ''
})

watch(
  () => filters,
  () => {
    const options = Object.entries(filters)
      .filter(([_, value]) => value) // убираем пустые
      .map(([key, value]) => ({ key, value }))
    emit('makeOptions', options)
  },
  { deep: true }
)
</script>

<template>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      Characteristics:
      <input
        v-model="filters.characteristics"
        class="text-gold outline-none border border-gold rounded-md ml-2"
      />
    </div>
    <div class="text-gold">
      Ingredients:
      <input
        v-model="filters.ingredients"
        class="text-gold outline-none border border-gold rounded-md ml-2"
      />
    </div>
  </div>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      Difficulty:
      <select
        v-model="filters.difficulty"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="">--</option>
        <option class="bg-bg text-gold" value="Easy">Easy</option>
        <option class="bg-bg text-gold" value="Medium">Medium</option>
        <option class="bg-bg text-gold" value="Hard">Hard</option>
      </select>
    </div>
    <div class="text-gold">
      Founder:
      <input
        v-model="filters.founder"
        class="text-gold outline-none border border-gold rounded-md ml-2"
      />
    </div>
  </div>
</template>
