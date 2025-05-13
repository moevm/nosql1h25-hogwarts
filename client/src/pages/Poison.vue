<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Graph from '../components/Graph.vue'
import PotionEdit from '../components/PotionEdit.vue'

const route = useRoute()
const item = ref({})
const modalView = ref(false)
const editMode = ref(false)

const fetchPotion = async () => {
  try {
    const data = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/potions/${route.params.id}`)
    item.value = await data.json()
  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchPotion)

const closeModal = () => {
  modalView.value = false
}
const openModal = () => {
  modalView.value = true
}

const onEditSaved = () => {
  editMode.value = false
  fetchPotion()
}
</script>

<template>
  <div class="flex flex-col items-center text-center p-4 min-w-3/5 mt-[-150px]">
    <router-link to="/" class="text-5xl text-gold font-display flex mb-[50px]">Harry Potter Wiki</router-link>
    <div class="bg-[#09306260] p-[70px] w-full rounded-md overflow-y-auto scrollbar-hide">
      <template v-if="editMode">
        <PotionEdit :potion="item" @saved="onEditSaved" />
      </template>
      <template v-else>
        <div class="flex flex-col float-left mr-10 mb-10">
          <img class="rounded-md w-[250px] h-[250px ] mb-10 border-3 border-gold" :src="item.image_path || ''" :alt="item.name" />
          <button class="bg-bg rounded-[5px] border-3 border-gold text-gold px-4 py-2" @click="openModal">Graph</button>
          <Graph v-if="modalView" type="poison" :id="item.id" @close="closeModal" />
        </div>
        <div class="flex justify-around">
          <h2 class="text-6xl text-gold font-display pb-5">{{ item.name }}</h2>
          <button class="bg-bg rounded-[5px] border-3 border-gold text-gold px-6 py-1 h-1/2" @click="editMode = true">Edit</button>
        </div>
        <p class="text-4xl text-gold font-display text-start">Difficulty: {{ item.difficulty }}</p>
        <p class="text-4xl text-gold font-display text-start">Effect: {{ item.effect }}</p>
        <p class="text-4xl text-gold font-display text-start">Ingredients: {{ item.ingredients }}</p>
      </template>
    </div>
  </div>
</template>
