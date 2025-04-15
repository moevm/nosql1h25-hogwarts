<script setup>
import Card from '../components/Card.vue'
import { ref } from 'vue'

const items = ref([
  { id: 'harry', name: 'Harry Potter', imageUrl: '/images/HarryPotter.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'ron', name: 'Ron Weasley', imageUrl: '/images/RonWeasley.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' }
])

const modalOpen = ref(false)
</script>

<template>
  <div>
    <router-link to="/" class="text-5xl text-gold font-display flex">
      Harry Potter Wiki
    </router-link>

    <div class="w-5/6 my-5 relative">
      <div class="max-w-full flex items-center bg-bg rounded-md border border-gold overflow-hidden">
        <input
          class="flex-1 pl-3 py-3 bg-bg text-gold outline-none font-display placeholder:text-[#6C6F27]"
          placeholder="Harry Potter"
        />
        <button
          class="text-bg w-12 h-12 rounded-md border border-gold flex justify-center items-center text-gold outline-none"
          @click="
            () => {
              modalOpen = !modalOpen
            }
          "
        >
          <span
            :class="['transition-transform duration-200', modalOpen ? 'rotate-180' : 'rotate-0']"
          >
            ▼
          </span>
        </button>
        <button
          class="text-bg h-12 w-12 rounded-md border border-gold flex justify-center items-center"
        >
          <img class="w-6 h-6" src="/images/search.svg" />
        </button>
      </div>
      <transition name="fade">
        <div
          v-if="modalOpen"
          class="bg-bg w-full h-[400px] rounded-md border border-gold absolute b-[-1px] l-0"
        ></div>
      </transition>
    </div>

    <ul class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto scrollbar-hide">
      <li class="flex justify-center">
        <div class="w-50 h-50 bg-bg flex flex-col items-center pt-2 rounded-md">
          <img
            class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed"
            src="/images/add.svg"
          />
          <p class="text-gold text-lg">Add Item</p>
        </div>
      </li>
      <li v-for="item in items" :key="item.id" class="flex justify-center">
        <router-link :to="`/character/${item.id}`">
          <Card :title="item.name" :image-url="item.imageUrl" />
        </router-link>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s ease-in-out;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
