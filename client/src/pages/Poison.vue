<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const item = ref({})

onMounted(async () => {
  try{
    const data = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/poisons/${route.params.id}`, {
      method: 'GET'
    })
    item.value = await data.json()
    console.log(item.value)
  }
  catch(err){
    console.error(err)
  }
})

</script>

<template>
  <div class="flex flex-col items-center text-center p-4 min-w-3/5 mt-[-150px]">
    <router-link to="/" class="text-5xl text-gold font-display flex mb-[50px]">
      Harry Potter Wiki
    </router-link>
    <div class="bg-[#09306260] p-[70px] w-full rounded-md overflow-y-auto scrollbar-hide">
      <img
        class="rounded-md w-[300px] h-[300px] float-left mr-10 mb-10"
        :src="item.image_path || ''"
        :alt="item.name"
      />
      <h2 class="text-6xl text-gold font-display pb-5">{{ item.name }}</h2>
      <p class="text-4xl text-gold font-display text-start">
        Difficulty: {{item.difficulty}}
      </p>
      <p class="text-4xl text-gold font-display text-start">
        Effect: {{item.effect}}
      </p>
      <p class="text-4xl text-gold font-display text-start">
        ingredients: {{item.ingridients}}
      </p>
    </div>
  </div>
</template>
