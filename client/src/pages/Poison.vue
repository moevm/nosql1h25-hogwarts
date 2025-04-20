<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const items = ref([])

onMounted(async () => {
  const data = await fetch(`${import.meta.SERVER_URL}/poisons`, {
    method: 'GET'
  })

  if (!data.ok) {
    throw new Error('Ошибка при загрузке зелий')
  }

  items.value = await data.json()

  console.log(items.value)
})

const route = useRoute()

const poison = computed(() => items.find((c) => c.id === route.params.id))
</script>

<template>
  <div class="flex flex-col items-center text-center p-4">
    <router-link to="/" class="text-5xl text-gold font-display flex mb-[50px]">
      Harry Potter Wiki
    </router-link>
    <div class="bg-[#09306260] p-[70px] rounded-md overflow-y-auto scrollbar-hide">
      <img
        class="rounded-md w-[300px] h-[300px] float-left mr-10 mb-10"
        :src="`/images/${poison.name.replace(' ', '')}.png`"
        :alt="poison.name"
      />
      <h2 class="text-6xl text-gold font-display pb-5">{{ poison.name }}</h2>
      <p class="text-4xl text-gold font-display text-start">
        Amortentia is the most powerful love potion in the world. It is distinctive for its
        mother-of-pearl sheen, and steam rises from the potion in spirals. Amortentia smells
        different to each person, according to what attracts them.
      </p>
    </div>
  </div>
</template>
