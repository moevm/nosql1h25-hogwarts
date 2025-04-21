<script setup>
import { reactive, watch } from 'vue'

const emit = defineEmits(['makeOptions'])

const filters = reactive({
  blood_status: '',
  died: null,
  gender: '',
  house: '',
  born: ''
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
      Blood Status:
      <select
        v-model="filters.blood_status"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="">--</option>
        <option class="bg-bg text-gold" value="Pure-blood">Pure-blood</option>
        <option class="bg-bg text-gold" value="Muggle-born">Muggle-born</option>
        <option class="bg-bg text-gold" value="Half-blood">Half-blood</option>
      </select>
    </div>
    <div class="text-gold">
      Died:
      <input
        v-model="filters.died"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      />
    </div>
    <div class="text-gold">
      Gender:
      <select
        v-model="filters.gender"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="">--</option>
        <option class="bg-bg text-gold" value="Man">Man</option>
        <option class="bg-bg text-gold" value="Female">Female</option>
      </select>
    </div>
  </div>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      House:
      <select
        v-model="filters.house"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="">--</option>
        <option class="bg-bg text-gold" value="Gryffindor">Gryffindor</option>
        <option class="bg-bg text-gold" value="Ravenclaw">Ravenclaw</option>
        <option class="bg-bg text-gold" value="Slytherin">Slytherin</option>
        <option class="bg-bg text-gold" value="Hufflepuff">Hufflepuff</option>
      </select>
    </div>
    <div class="text-gold">
      Born:
      <input
        v-model="filters.born"
        class="text-gold outline-none border border-gold rounded-md ml-2"
      />
    </div>
  </div>
</template>
