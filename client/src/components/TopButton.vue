<script setup>
defineProps({
  action: String,
  disabled: Boolean
})
</script>

<template>
  <button
    class="bg-bg rounded-md px-2 py-3 border border-gold border-3 text-xl! text-gold disabled:bg-[#041c3b] disabled:text-[#46494d] disabled:border-[#46494d] outline-none"
    :disabled="disabled"
  >
    {{ action }}
  </button>
</template>
