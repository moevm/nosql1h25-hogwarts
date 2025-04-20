<script setup></script>

<template>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      Category:
      <select
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="Charm">Charm</option>
        <option class="bg-bg text-gold" value="Curse">Curse</option>
      </select>
    </div>
    <div class="text-gold">
      Effect:
      <input class="text-gold outline-none border border-gold rounded-md ml-2" />
    </div>
  </div>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      Light:
      <select
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="Blue">Blue</option>
        <option class="bg-bg text-gold" value="Red">Red</option>
        <option class="bg-bg text-gold" value="Green">Green</option>
        <option class="bg-bg text-gold" value="White">White</option>
        <option class="bg-bg text-gold" value="Yellow">Yellow</option>
      </select>
    </div>
    <div class="text-gold">
      User:
      <input class="text-gold outline-none border border-gold rounded-md ml-2" />
    </div>
  </div>
</template>
