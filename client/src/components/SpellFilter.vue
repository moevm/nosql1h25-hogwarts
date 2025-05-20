<script setup>
import { reactive, watch, onMounted, ref } from 'vue'

const emit = defineEmits(['makeOptions'])

const filters = reactive({
  category: '',
  effect: '',
  light: '',
  user: ''
})

const filterOptions = ref({
  category: [],
  light: []
})

watch(
  () => filters,
  () => {
    const options = Object.entries(filters)
      .filter(([_, value]) => value) // отбрасываем пустые значения
      .map(([key, value]) => ({ key, value }))
    emit('makeOptions', options)
  },
  { deep: true }
)

onMounted(async () => {
  filterOptions.value = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/spells/filters`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  }).then((res) => res.json())

  console.log('Fetched filter options:', filterOptions.value)
})
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
        <option
          v-for="option in filterOptions.category"
          :key="option"
          :value="option"
          class="bg-bg text-gold"
        >
          {{ option }}
        </option>
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

  <div class="flex flex-col flex-wrap justify-around h-full ml-[-200px]">
    <div class="text-gold">
      Light:
      <select
        v-model="filters.light"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="">--</option>
        <option
          v-for="option in filterOptions.light"
          :key="option"
          :value="option"
          class="bg-bg text-gold"
        >
          {{ option }}
        </option>
      </select>
    </div>
  </div>
</template>
