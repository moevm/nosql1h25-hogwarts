<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const items = ref([])

onMounted(async () => {
  const data = await fetch(`${import.meta.SERVER_URL}/spells`, {
    method: 'GET'
  })

  if (!data.ok) {
    throw new Error('Ошибка при загрузке зелий')
  }

  items.value = await data.json()

  console.log(items.value)
})

const route = useRoute()

const spell = computed(() => items.find((c) => c.id === route.params.id))
</script>

<template>
  <div class="flex flex-col items-center text-center p-4">
    <router-link to="/" class="text-5xl text-gold font-display flex mb-[50px]">
      Harry Potter Wiki
    </router-link>
    <div class="bg-[#09306260] p-[70px] rounded-md overflow-y-auto scrollbar-hide">
      <img
        class="rounded-md w-[300px] h-[300px] float-left mr-10 mb-10"
        :src="`/images/${spell.name.replace(' ', '')}.png`"
        :alt="spell.name"
      />
      <h2 class="text-6xl text-gold font-display pb-5">{{ spell.name }}</h2>
      <p class="text-4xl text-gold font-display text-start">{{ spell }}</p>
    </div>
  </div>
</template>
