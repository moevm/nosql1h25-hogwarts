<script setup>
import { useHead } from '@vueuse/head'
import { ref } from 'vue'
import TopButton from './components/TopButton.vue'
import StatisticsModal from './components/Statistics.vue'

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
const fileInput = ref(null)

function triggerFileInput() {
  fileInput.value?.click()
}
function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()

  reader.onload = async (e) => {
    try {
      const data = JSON.parse(e.target.result)
      console.log('Imported:', data)

      const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/import`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })

      if (!response.ok) {
        throw new Error('Ошибка при импорте данных')
      }

      const result = await response.json()

      // Используем ответ от сервера, если есть
      const count = result?.import_counts ?? data.length

      alert(`Импорт завершен. Добавлено записей: ${count}`)
    } catch (err) {
      console.error('Ошибка при загрузке файла:', err)
      alert('Ошибка: неверный формат или структура файла.')
    }
  }

  reader.readAsText(file)
}

const exportStatus = ref('')

async function handleExport() {
  try {
    const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/export`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Ошибка при экспорте данных')
    }

    const data = await response.json()

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = 'exported_data.json'
    link.click()

    URL.revokeObjectURL(url)

    exportStatus.value = 'Экспорт успешно завершён!'
    alert(exportStatus.value)
  } catch (error) {
    console.error('Export failed:', error)
    exportStatus.value = 'Ошибка при экспорте данных'
    alert(exportStatus.value)
  }
}

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
              to="/characters"
              class="block text-center py-2 bg-bg text-gold border-b-3 border-gold w-full h-full flex items-center justify-center text-xl"
            >
              Character
            </router-link>
          </li>
          <li class="flex-1">
            <router-link
              to="/potions"
              class="block text-center py-2 bg-bg text-gold border-b-3 border-gold w-full h-full flex items-center justify-center text-xl"
            >
              Potions
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
      <StatisticsModal />
      <TopButton action="Import" @click="triggerFileInput" />
      <TopButton action="Export"  @click="handleExport" />
      <input
        type="file"
        accept="application/json"
        @change="handleFileUpload"
        ref="fileInput"
        class="hidden"
      />
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
