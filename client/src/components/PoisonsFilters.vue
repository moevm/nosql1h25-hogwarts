<template>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      Characteristics:
      <input class="text-gold outline-none border border-gold rounded-md ml-2" />
    </div>
    <div class="text-gold">
      Ingredients:
      <input class="text-gold outline-none border border-gold rounded-md ml-2" />
    </div>
  </div>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      Difficulty:
      <select
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="Advanced">Advanced</option>
        <option class="bg-bg text-gold" value="Hard">Hard</option>
        <option class="bg-bg text-gold" value="Very Hard">Very Hard</option>
      </select>
    </div>
    <div class="text-gold">
      Founder:
      <input class="text-gold outline-none border border-gold rounded-md ml-2" />
    </div>
  </div>
</template>
