<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const characters = [
  { id: 'harry', name: 'Harry Potter' },
  { id: 'hermione', name: 'Hermione Granger' },
  { id: 'ron', name: 'Ron Weasley' },
]

const route = useRoute()

const character = computed(() => characters.find((c) => c.id === route.params.id))
</script>

<template>
  <div class="flex flex-col items-center text-center p-4">
    <router-link to="/" class="text-5xl text-gold font-display flex mb-[50px]">
      Harry Potter Wiki
    </router-link>
    <div class="bg-[#09306260] p-[70px] rounded-md overflow-y-auto scrollbar-hide">
      <img
        class="rounded-md w-[250px] h-[250px] float-left mr-10 mb-10 border-3 border-gold"
        :src="`/images/${character.name.replace(' ', '')}.png`"
        :alt="character.name"
      />
      <h2 class="text-5xl text-gold font-display pb-5">{{ character.name }}</h2>
      <p class="text-2xl text-gold font-display text-start">
        Aliases: The Boy Who Lived, Gregory Goyle(under disguise of Polyjuice  Potion),
        Neville Longbottom(the name he told Stanley  Shunpike in his third year),
        Potty (by Peeves and Slytherins), The Boy Who Lied (by the Daily Prophet), The Chosen One,
        Barny Weasley (under disguise of Polyjuice Potion), Albert Runcorn 
        (under disguise of Polyjuice Potion),
        Vernon Dudley (the name he used to disguise his identity from Snatchers)
      </p>
    </div>
  </div>
</template>
