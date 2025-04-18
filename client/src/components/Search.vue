<script setup>
defineProps({
  modalToggle: Function,
  placeholder: String,
  modalOpen: Boolean
})
</script>

<template>
  <div class="w-5/6 my-5 relative">
    <div class="flex w-full gap-5">
      <div class="w-full flex items-center bg-bg rounded-md border border-gold overflow-hidden">
        <input
          class="flex-1 pl-3 py-3 bg-bg text-gold outline-none font-display placeholder:text-[#6C6F27]"
          :placeholder="placeholder"
        />
        <button
          class="text-bg h-14 w-14 rounded-md border border-gold flex justify-center items-center"
        >
          <img class="w-6 h-6" src="/images/search.svg" />
        </button>
      </div>
      <button
        class="text-bg w-25 h-14 bg-bg rounded-md border border-gold flex justify-center items-center text-gold outline-none flex gap-2"
        @click="() => modalToggle()"
      >
        Search
        <span :class="['transition-transform duration-200', modalOpen ? 'rotate-180' : 'rotate-0']">
          ▼
        </span>
      </button>
    </div>
    <transition name="fade">
      <div
        v-if="modalOpen"
        class="bg-bg w-full h-[400px] rounded-md border border-gold absolute b-[-1px] l-0"
      ></div>
    </transition>
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
}
</style>
