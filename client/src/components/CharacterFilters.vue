<script setup>
import { reactive, watch } from 'vue'

const emit = defineEmits(['makeOptions'])

const filters = reactive({
  blood_status: '',
  died: '',
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
        <option class="bg-bg text-gold" value="Mage">Pure-blood</option>
        <option class="bg-bg text-gold" value="Muggle">Muggle-born
</option>
        <option class="bg-bg text-gold" value="Half-blood">Half-blood</option>
      </select>
    </div>
    <div class="text-gold">
      Died:
      <select
        v-model="filters.died"
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="">--</option>
        <option class="bg-bg text-gold" value="Yes">Yes</option>
        <option class="bg-bg text-gold" value="No">No</option>
      </select>
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
        <option class="bg-bg text-gold" value="Helicopter">Helicopter</option>
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
        <option class="bg-bg text-gold" value="Griffindor">Griffindor</option>
        <option class="bg-bg text-gold" value="Cogtenvran">Cogtenvran</option>
        <option class="bg-bg text-gold" value="Slyzerin">Slyzerin</option>
        <option class="bg-bg text-gold" value="Puffendui">Puffendui</option>
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
