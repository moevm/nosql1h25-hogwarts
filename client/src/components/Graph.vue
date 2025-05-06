<script setup>
const emit = defineEmits(['closeModal'])
</script>

<template>
    <div class="absolute w-full h-full bg-[#09306260] top-0 left-0 flex justify-end items-start">
        <button @click="emit('closeModal')" class="mt-10 mr-10 bg-bg rounded-[5px] border-3 border-gold text-gold px-4 py-2">X</button>
        <div class="absolute bg-bg top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] w-4/6 h-4/6 rounded-[10px] border-3 border-gold"></div>
    </div>
</template>