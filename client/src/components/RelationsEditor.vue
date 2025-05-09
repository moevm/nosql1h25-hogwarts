<!-- RelationEditor.vue -->
<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const allCharacters = ref([])
const newRelation = ref({ type: '', target_character: '' })

onMounted(async () => {
  const res = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters`)
  allCharacters.value = await res.json()
  console.log(props.modelValue)
})

const addRelation = () => {
  if (newRelation.value.target_character && newRelation.value.type) {
    const updated = [...props.modelValue, { ...newRelation.value }]
    emit('update:modelValue', updated)
    newRelation.value = { type: '', target_character: '' }
  }
}

const removeRelation = (index) => {
  const updated = [...props.modelValue]
  updated.splice(index, 1)
  emit('update:modelValue', updated)
}
</script>

<template>
  <div class="mt-4">
    <h3 class="text-lg font-bold">Relations</h3>

    <div class="flex space-x-2 mb-2">
      <select v-model="newRelation.type" class="input">
        <option value="">-- Relation Type --</option>
        <option value="friend">Friend</option>
        <option value="enemy">Enemy</option>
        <option value="family">Family</option>
      </select>
      <select v-model="newRelation.target_character" class="input">
        <option value="">-- Select Character --</option>
        <option v-for="char in allCharacters" :key="char.id" :value="char.name">
          {{ char.name }}
        </option>
      </select>
      <button @click="addRelation" type="button" class="bg-gold text-bg px-2 py-1 rounded">
        Add
      </button>
    </div>

    <ul>
      <li
        v-for="(relation, index) in modelValue"
        :key="index"
        class="flex justify-between items-center mb-1"
      >
        <span>
          {{ relation.type }}:
          {{ allCharacters.find((c) => c.name === relation.target_character)?.name || 'Unknown' }}
        </span>
        <button @click="removeRelation(index)" class="text-red-500">Remove</button>
      </li>
    </ul>
  </div>
</template>
