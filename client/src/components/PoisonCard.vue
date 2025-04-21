<script setup>
defineProps({
  title: String,
  imageUrl: {
    type: String,
    default: 'images/AguamentiCharm.png'
  }
})
</script>

<template>
  <div class="flex justify-center items-center">
    <div class="w-50 h-60 bg-bg flex flex-col items-center pt-3 rounded-md">
      <img class="w-4/5 mb-2" :src="imageUrl" />
      <p class="text-gold text-lg text-center">{{ title }}</p>
    </div>
  </div>
</template>
