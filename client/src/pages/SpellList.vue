<script setup>
import SpellCard from '@/components/SpellCard.vue'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const items = ref([
  { id: 'aguamenti', name: 'Aguamenti Charm' },
  { id: 'alohomora', name: 'Alohomora' },
  { id: 'aparecium', name: 'Aparecium' },
])
</script>

<template>
  <div>
    <router-link to="/" class="text-5xl text-gold font-display flex">
      Harry Potter Wiki
    </router-link>

    <div
      class="w-5/6 mt-5 mb-10 flex items-center bg-bg rounded-md border border-gold overflow-hidden"
    >
      <input
        class="flex-1 pl-3 py-3 bg-bg text-gold outline-none font-display placeholder:text-[#6C6F27]"
        placeholder="Harry Potter"
      />
      <div
        class="text-bg h-full w-12 rounded-md border border-gold flex justify-center items-center"
      >
        <img class="w-6 h-6" src="/images/search.svg" />
      </div>
    </div>

    <ul class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto scrollbar-hide">
      <li v-for="item in items" :key="item.id">
        <router-link :to="`/spells/${item.id}`">
          <SpellCard />
        </router-link>
      </li>
    </ul>
  </div>
</template>
