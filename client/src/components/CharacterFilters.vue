<template>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      Blood Status:
      <select
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="Mage">Mage</option>
        <option class="bg-bg text-gold" value="Muggle">Muggle</option>
        <option class="bg-bg text-gold" value="Half-blood">Half-blood</option>
      </select>
    </div>
    <div class="text-gold">
      Died:
      <select
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="Yes">Yes</option>
        <option class="bg-bg text-gold" value="No">No</option>
      </select>
    </div>
    <div class="text-gold">
      Gender:
      <select
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="Man">Man</option>
        <option class="bg-bg text-gold" value="Female">Female</option>
        <option class="bg-bg text-gold" value="Helicopter">Helicopter</option>
      </select>
    </div>
  </div>
  <div class="flex flex-col flex-wrap justify-around h-full">
    <div class="text-gold">
      House:
      <select
        class="bg-bg text-gold border border-gold rounded-md px-4 py-2 font-display outline-none focus:ring-1 focus:ring-gold ml-2"
      >
        <option class="bg-bg text-gold" value="Griffindor">Griffindor</option>
        <option class="bg-bg text-gold" value="Cogtenvran">Cogtenvran</option>
        <option class="bg-bg text-gold" value="Slyzerin">Slyzerin</option>
        <option class="bg-bg text-gold" value="Puffendui">Puffendui</option>
      </select>
    </div>
    <div class="text-gold">
      Born:
      <input class="text-gold outline-none border border-gold rounded-md ml-2" />
    </div>
    <div class="text-gold">
      Mentioned:
      <input class="text-gold outline-none border border-gold rounded-md ml-2" />
    </div>
  </div>
</template>
