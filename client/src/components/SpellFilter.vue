<script setup>
import { reactive, watch } from 'vue'

const emit = defineEmits(['makeOptions'])

const filters = reactive({
  category: '',
  effect: '',
  light: '',
  user: ''
})

watch(
  () => filters,
  () => {
    console.log(filters)
    const options = Object.entries(filters)
      .filter(([_, value]) => value) // отбрасываем пустые
      .map(([key, value]) => ({ key, value }))
    emit('makeOptions', options)
  },
  { deep: true }
)
</script>

<template>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      Category:
      <select
        v-model="filters.category"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="">--</option>
        <option class="bg-bg text-gold" value="Charm">Charm</option>
        <option class="bg-bg text-gold" value="Curse">Curse</option>
        <option class="bg-bg text-gold" value="Hex">Hex</option>
        <option class="bg-bg text-gold" value="Spell">Spell</option>
      </select>
    </div>
    <div class="text-gold">
      Effect:
      <input
        v-model="filters.effect"
        class="text-gold outline-none border border-gold rounded-md ml-2"
      />
    </div>
  </div>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      Light:
      <select
        v-model="filters.light"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="">--</option>
        <option class="bg-bg text-gold" value="blue">Blue</option>
        <option class="bg-bg text-gold" value="red">Red</option>
        <option class="bg-bg text-gold" value="green">Green</option>
        <option class="bg-bg text-gold" value="yellow">None</option>
      </select>
    </div>
    <div class="text-gold">
      User:
      <input
        v-model="filters.user"
        class="text-gold outline-none border border-gold rounded-md ml-2"
      />
    </div>
  </div>
</template>
