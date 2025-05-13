<script setup>
import { onMounted, ref } from 'vue'

const props = defineProps({
  spell: Object
})
const emit = defineEmits(['saved'])

const form = ref({ ...props.spell })

const filters = ref({})

const updateSpell = async () => {
  await fetch(`${import.meta.env.VITE_SERVER_URL}/api/spells/${form.value.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  emit('saved')
}

onMounted(async () => {
  filters.value = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/spells/filters`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  }).then((res) => res.json())

  console.log(filters.value)
})
</script>

<template>
  <form @submit.prevent="updateSpell" class="text-gold space-y-4">
    <label>Name: <input v-model="form.name" class="input" /></label>
    <label>Effect: <input v-model="form.effect" class="input" /></label>
    <label>
  Light:
  <select v-model="form.light" class="input">
    <option v-for="option in filters.light" :key="option" :value="option">
      {{ option }}
    </option>
  </select>
</label>

<label>
  Category:
  <select v-model="form.category" class="input">
    <option v-for="option in filters.category" :key="option" :value="option">
      {{ option }}
    </option>
  </select>
</label>
    <label>Image URL: <input v-model="form.image_path" class="input" /></label>
    <button type="submit" class="bg-gold text-bg px-4 py-2 rounded">Save</button>
  </form>
</template>

<style scoped>
.input {
  background-color: #093062;
  border: 1px solid gold;
  color: gold;
  padding: 0.5em;
  border-radius: 4px;
  width: 100%;
}
</style>
