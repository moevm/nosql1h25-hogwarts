<script setup>
import { ref } from 'vue'

const addItemModal = ref(false)

const toggleModal = (e) => {
  e.stopPropagation()
  console.log('click')
  addItemModal.value = !addItemModal.value
}
</script>

<template>
  <li class="flex justify-center" @click="(e) => toggleModal(e)">
    <div class="w-50 h-50 bg-bg flex flex-col items-center pt-2 rounded-md">
      <img class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed" src="/images/add.svg" />
      <p class="text-gold text-lg">Add Item</p>
    </div>
    <div
      v-if="addItemModal"
      class="w-[700px] h-[500px] absolute bg-bg top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] rounded-[10px] border-2 border-gold"
    >
      <div class="relative w-full h-full">
        <button
          class="absolute top-0 right-0 border-2 border-gold w-10 h-10 rounded-[10px]"
          @click="(e) => toggleModal(e)"
        ></button>
      </div>
    </div>
  </li>
</template>
