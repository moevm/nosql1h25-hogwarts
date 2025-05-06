<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  title: String,
  imageUrl: String,
  house: String,
  born: String,
  died: String,
  category: String,
  light: String,
  difficulty: String,
  effect: String,
  gender: String
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
    <div class="w-[250px] h-[300px] bg-bg flex flex-col items-center pt-2 rounded-md overflow-hidden ">
      <img
        class="max-h-[200px] object-cover rounded-[10px]"
        :src="img || getImage()"
      />
      <div>
        <p class="text-gold text-lg text-center px-2">{{ title }}</p>
        <div class="pl-2 overflow-auto">
          <p v-if="house" class="px-2 text-gold text-sm">House: {{ house }}</p>
          <p v-if="born" class="px-2 text-gold text-sm">Born: {{ born }}</p>
          <p v-if="died" class="px-2 text-gold text-sm">Died: {{ died }}</p>
          <p v-if="category" class="px-2 text-gold text-sm">Category: {{ category }}</p>
          <p v-if="light" class="px-2 text-gold text-sm">Light: {{ light }}</p>
          <p v-if="difficulty" class="px-2 text-gold text-sm">Difficulty: {{ difficulty }}</p>
          <p v-if="effect" class="px-2 text-gold text-sm">Effect: {{ effect }}</p>
          <p v-if="gender" class="px-2 text-gold text-sm">Gender: {{ gender }}</p>
        </div>
      </div>
      
    </div>
  </div>
</template>

