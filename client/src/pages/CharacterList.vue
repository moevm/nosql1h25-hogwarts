<script setup>
import Card from '../components/Card.vue'
import { onMounted, ref } from 'vue'
import Search from '../components/Search.vue'
import AddCharacter from '../components/AddCharacter.vue'

const items = ref([])

onMounted(async () => {
  try {
    const data = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters`, {
      method: 'GET'
    })
    items.value = await data.json()
    console.log(items.value)
  } catch (err) {
    console.error(err)
  }
})

const fetchUpdate = async (str) => {
  try {
    const data = await fetch(str, {
      method: 'GET'
    })
    items.value = data.json()
  } catch (err) {
    console.error(err)
  }
}

const modalOpen = ref(false)

const modalToggle = () => {
  modalOpen.value = !modalOpen.value
}
</script>

<template>
  <div class="mt-[-150px]">
    <router-link to="/" class="text-5xl text-gold font-display flex">
      Harry Potter Wiki
    </router-link>
    <Search
      @fetchUpdate="fetchUpdate"
      :modal-toggle="modalToggle"
      placeholder="Harry Potter"
      :modal-open="modalOpen"
    />
    <ul class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto scrollbar-hide">
      <AddCharacter @fetchUpdate="fetchUpdate" />
      <li v-for="item in items" :key="item.id" class="flex justify-center">
        <router-link :to="`/characters/${item.id}`">
          <Card :title="item.name" :image-url="item.image_path" :blood-status="item.blood_status" :born="item.born" :died="item.died? item.died : 'No'" :house="item.house" :gender="item.gender"/>
        </router-link>
      </li>
    </ul>
  </div>
</template>
