<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const spells = [
  { id: 'aguamenti', name: 'Aguamenti Charm' },
  { id: 'alohomora', name: 'Alohomora' },
  { id: 'aparecium', name: 'Aparecium' },
]

const route = useRoute()

const spell = computed(() => spells.find((c) => c.id === route.params.id))
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
      <p class="text-4xl text-gold font-display text-start">
        The Unlocking Charm (Alohomora), also known as the Unlocking Spell 
        or the Thief's Friend was a charm that unlocked objects such as doors or windows. 
        It was also able to open doors locked by the Locking Spell (Colloportus), and as such, 
        acted as its counter-charm. The Anti-Alohomora Charm could be used to prevent this charm 
        from working on a locked target.
      </p>
    </div>
  </div>
</template>
