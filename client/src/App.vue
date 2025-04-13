<script setup>
import { useHead } from '@vueuse/head'
import { ref } from 'vue'

useHead({
  title: 'Главная страница',
  meta: [
    { name: 'description', content: 'Описание моей замечательной страницы' },
    { name: 'keywords', content: 'vue, seo, vueuse, head' },
    { property: 'og:title', content: 'Моя страница в соцсетях' },
    { property: 'og:description', content: 'Краткое описание для соцсетей' },
  ],
  link: [{ rel: 'icon', href: '/images/favicon.ico' }],
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
        class="w-full flex items-center px-4 bg-bg border-b-3 border-gold text-gold pl-10"
      >
        <p class="text-xl">Categories</p>
        <span
          :class="['ml-6 transition-transform duration-300', isOpen ? 'rotate-180' : 'rotate-0']"
        >
          ▼
        </span>
      </button>
      <transition name="fade">
        <ul v-if="isOpen" class="flex flex-col">
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
      <!-- Вынести в отдельный компонент + стили одинаковые - в отдельную переменную -->
      <button
        class="bg-bg rounded-md px-2 py-3 border border-gold border-3 disabled:bg-gray-200"
        disabled
      >
        <span class="text-xl text-gold">Statistics</span>
      </button>
      <button class="bg-bg rounded-md px-2 py-3 border border-gold border-3">
        <span class="text-xl text-gold">Import</span>
      </button>
      <button class="bg-bg rounded-md px-2 py-3 border border-gold border-3">
        <span class="text-xl text-gold">Export</span>
      </button>
    </div>
    <router-view class="flex-1 flex flex-col items-center justify-center pt-[150px]"></router-view>
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
