<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  title: String,
  imageUrl: String
})

const img = ref(props.imageUrl || '')
const route = useRoute()

console.log(route.path)

const getImage = (str) => {
  if (props.imageUrl) {
    return props.imageUrl
  }
  switch (route.path) {
    case '/characters':
      img.value = '/images/defaultCharacter.jpg'
      break
    case '/potions':
      img.value = '/images/defaultPotion.jpg'
      break
    case '/spells':
      img.value = '/images/defaultSpell.jpg'
      break
  }
}
</script>

<template>
  <div class="flex justify-center items-center">
    <div class="w-50 h-60 bg-bg flex flex-col items-center pt-2 rounded-md">
      <img class="flex-1 rounded-[20px] p-4" :src="img || getImage()" />
      <p class="text-gold text-lg">{{ title }}</p>
    </div>
  </div>
</template>
