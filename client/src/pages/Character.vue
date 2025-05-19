<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import Graph from '../components/Graph.vue'
import CharacterEdit from '../components/CharacterEdit.vue'

const route = useRoute()
const editMode = ref(false)

const item = ref({})
const modalView = ref(false)

const onEditSaved = () => {
  editMode.value = false

  fetchCharacter()
}

const fetchCharacter = async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters/${route.params.id}`)
    item.value = await res.json()
  } catch (err) {
    console.error(err)
  }
}

onMounted(async () => {
  fetchCharacter()
})

const closeModal = () => {
  console.log('click')
  modalView.value = false
}
const openModal = () => {
  modalView.value = true
}
</script>
<template>
  <div class="flex flex-col items-center text-center p-4 min-w-3/5 mt-[-150px]">
    <router-link to="/" class="text-5xl text-gold font-display flex mb-[50px]">
      Harry Potter Wiki
    </router-link>

    <div class="bg-[#09306260] p-[70px] w-full rounded-md overflow-y-auto scrollbar-hide">
      <template v-if="editMode">
        <CharacterEdit :character="item" @saved="onEditSaved" />
      </template>
      <template v-else>
        <!-- текущий просмотр персонажа -->
        <div class="flex flex-col float-left mr-10 mb-10">
          <img
            class="rounded-md w-[250px] h-[250px ] mb-10 border-3 border-gold"
            :src="item.image_path || ''"
            :alt="item.name"
          />
          <button
            class="bg-bg rounded-[5px] border-3 border-gold text-gold px-4 py-2"
            @click="openModal"
          >
            Graph
          </button>

          <Graph v-if="modalView" type="character" :id="item.id" @close="closeModal" />
        </div>
        <div class="flex justify-around">
          <h2 class="text-5xl text-gold font-display pb-5">{{ item.name }}</h2>
          <button
            class="bg-bg rounded-[5px] border-3 border-gold text-gold px-6 py-1 h-1/2"
            @click="editMode = true"
          >
            Edit
          </button>
        </div>
        <p v-if="item.updated_at" class="text-2xl text-gold font-display text-start">
          Last Update: {{  new Date(item.updated_at.replace(' ', 'T')).toLocaleString() }}
        </p>
        <p class="text-2xl text-gold font-display text-start">
          Description: {{ item.description }}
        </p>
        <p class="text-2xl text-gold font-display text-start">
          Blood Status: {{ item.blood_status }}
        </p>
        <p class="text-2xl text-gold font-display text-start">Born: {{ item.born }}</p>
        <p class="text-2xl text-gold font-display text-start">Died: {{ item.died || 'No' }}</p>
        <p class="text-2xl text-gold font-display text-start">Gender: {{ item.gender }}</p>
        <p class="text-2xl text-gold font-display text-start">House: {{ item.house }}</p>
      </template>
    </div>
  </div>
</template>
