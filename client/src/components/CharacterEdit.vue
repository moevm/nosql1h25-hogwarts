<script setup>
import { ref } from 'vue'

import RelationEditor from './RelationsEditor.vue'

const props = defineProps({
  character: Object
})
const emit = defineEmits(['saved'])

const form = ref({
  ...props.character
})
const updateCharacter = async () => {
  const characterToSave = {
    ...form.value,
    born: form.value.born ? Number(form.value.born) : null,
    died: form.value.died ? Number(form.value.died) : null
  }
  console.log(characterToSave)
  await fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters/${form.value.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(characterToSave)
  })
  emit('saved')
}
</script>

<template>
  <form @submit.prevent="updateCharacter" class="text-gold space-y-4">
    <label>Name: <input v-model="form.name" class="input" /></label>
    <label>Description: <textarea v-model="form.description" class="input" /></label>

    <label
      >Blood Status:
      <select v-model="form.blood_status" class="input">
        <option value="">--</option>
        <option value="Pure-blood">Pure-blood</option>
        <option value="Half-blood">Half-blood</option>
        <option value="Muggle-born">Muggle-born</option>
      </select>
    </label>

    <label
      >Gender:
      <select v-model="form.gender" class="input">
        <option value="">--</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
      </select>
    </label>

    <label
      >House:
      <select v-model="form.house" class="input">
        <option value="">--</option>
        <option value="Gryffindor">Gryffindor</option>
        <option value="Ravenclaw">Ravenclaw</option>
        <option value="Slytherin">Slytherin</option>
        <option value="Hufflepuff">Hufflepuff</option>
      </select>
    </label>

    <label>Born: <input v-model="form.born" type="number" class="input" /></label>
    <label>Died: <input v-model="form.died" type="number" class="input" /></label>

    <label>Image URL: <input v-model="form.image_path" class="input" /></label>

    <!-- Отношения -->
    <RelationEditor v-model="form.relationships" />

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
  display: block;
  width: 100%;
}
</style>
