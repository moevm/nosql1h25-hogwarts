<script setup>
defineProps({
  title: String,
  imageUrl: String
})
</script>

<template>
  <div class="flex justify-center items-center">
    <div class="w-50 h-60 bg-bg flex flex-col items-center pt-2">
      <img class="w-4/5" :src="imageUrl || '/images/defaultSpell.jpg'" />
      <p class="text-gold text-lg">{{ title }}</p>
    </div>
  </div>
</template>
