<script setup>
import { useHead } from '@vueuse/head'
import { ref } from 'vue'
import TopButton from './components/TopButton.vue'

useHead({
  title: 'Главная страница',
  meta: [
    { name: 'description', content: 'Описание моей замечательной страницы' },
    { name: 'keywords', content: 'vue, seo, vueuse, head' },
    { property: 'og:title', content: 'Моя страница в соцсетях' },
    { property: 'og:description', content: 'Краткое описание для соцсетей' }
  ],
  link: [{ rel: 'icon', href: '/images/favicon.ico' }]
})
const isOpen = ref(false)
</script>

<template>
  <div
    class="w-full h-screen bg-no-repeat bg-cover bg-center flex relative"
    style="background-image: url('/images/background.svg')"
  >
    <div class="w-[175px] grid grid-rows-[1fr_6fr] relative">
      <button
        @click="isOpen = !isOpen"
        class="w-full flex items-center px-4 bg-bg border-b-3 border-r-3 border-gold text-gold pl-10 outline-none"
      >
        <p class="text-xl">Categories</p>
        <span
          :class="['ml-6 transition-transform duration-300', isOpen ? 'rotate-180' : 'rotate-0']"
        >
          ▼
        </span>
      </button>
      <transition name="fade">
        <ul v-if="isOpen" class="flex flex-col border-r-3 border-gold">
          <li class="flex-1">
            <router-link
              to="/character"
              class="block text-center py-2 bg-bg text-gold border-b-3 border-gold w-full h-full flex items-center justify-center text-xl"
            >
              Character
            </router-link>
          </li>
          <li class="flex-1">
            <router-link
              to="/poisons"
              class="block text-center py-2 bg-bg text-gold border-b-3 border-gold w-full h-full flex items-center justify-center text-xl"
            >
              Poison
            </router-link>
          </li>
          <li class="flex-1">
            <router-link
              to="/spells"
              class="block text-center py-2 bg-bg text-gold border-b-3 border-gold w-full h-full flex items-center justify-center text-xl"
            >
              Spell
            </router-link>
          </li>
        </ul>
      </transition>
    </div>
    <div class="absolute top-[50px] right-[70px] flex gap-5">
      <TopButton action="Statistics" disabled />
      <TopButton action="Import" />
      <TopButton action="Export" />
    </div>
    <router-view class="flex-1 flex flex-col items-center pt-[250px]"></router-view>
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
  transform: translateY(-50px);
}
</style>
