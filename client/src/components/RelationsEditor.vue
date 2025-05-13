<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: Array,  // character.relationships
  spells: Array,      // character.spells
  poisons: Array      // character.poisons
})

const emit = defineEmits([
  'update:modelValue',
  'update:spells',
  'update:poisons'
])

const newRelation = ref({ type: '', target_name: '' })
const availableOptions = ref([])

const relationTypes = [
  { value: 'friend', label: 'Friend', target: 'characters' },
  { value: 'enemy', label: 'Enemy', target: 'characters' },
  { value: 'family', label: 'Family', target: 'characters' },
  { value: 'brewed', label: 'Brewed', target: 'poisons' },
  { value: 'knows', label: 'Knows', target: 'spells' }
]

const dataCache = {
  characters: [],
  poisons: [],
  spells: []
}

const fetchData = async () => {
  try {
    const [chars, poisons, spells] = await Promise.all([
      fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters`).then(r => r.json()),
      fetch(`${import.meta.env.VITE_SERVER_URL}/api/potions`).then(r => r.json()),
      fetch(`${import.meta.env.VITE_SERVER_URL}/api/spells`).then(r => r.json())
    ])
    dataCache.characters = chars
    dataCache.poisons = poisons
    dataCache.spells = spells
  } catch (err) {
    console.error('Failed to load data for relations:', err)
  }
}

onMounted(fetchData)

watch(() => newRelation.value.type, (type) => {
  const target = relationTypes.find(r => r.value === type)?.target
  availableOptions.value = target ? dataCache[target] : []
})

const addRelation = () => {
  const { type, target_name } = newRelation.value
  if (!type || !target_name) return

  if (type === 'knows') {
    const current = props.spells || []
    if (!current.includes(target_name)) {
      emit('update:spells', [...current, target_name])
    }
  } else if (type === 'brewed') {
    const current = props.poisons || []
    if (!current.includes(target_name)) {
      emit('update:poisons', [...current, target_name])
    }
  } else {
    const exists = props.modelValue.some(
      r => r.type === type && r.target_character === target_name
    )
    if (!exists) {
      emit('update:modelValue', [
        ...props.modelValue,
        { type, target_character: target_name }
      ])
    }
  }

  newRelation.value = { type: '', target_name: '' }
}

const removeRelation = (type, value) => {
  if (type === 'knows') {
    const current = props.spells || []
    emit('update:spells', current.filter(name => name !== value))
  } else if (type === 'brewed') {
    const current = props.poisons || []
    emit('update:poisons', current.filter(name => name !== value))
  } else {
    const updated = props.modelValue.filter(
      r => !(r.type === type && r.target_character === value)
    )
    emit('update:modelValue', updated)
  }
}
</script>

<template>
  <div class="mt-4">
    <h3 class="text-lg font-bold text-gold">Relations</h3>

    <div class="flex space-x-2 mb-2 text-gold">
      <select v-model="newRelation.type" class="input">
        <option value="">-- Relation Type --</option>
        <option v-for="type in relationTypes" :key="type.value" :value="type.value">
          {{ type.label }}
        </option>
      </select>

      <select v-model="newRelation.target_name" class="input">
        <option value="">-- Select Target --</option>
        <option
          v-for="target in availableOptions"
          :key="target.name || target.title"
          :value="target.name || target.title"
        >
          {{ target.name || target.title }}
        </option>
      </select>

      <button @click="addRelation" type="button" class="bg-gold text-bg px-2 py-1 rounded">
        Add
      </button>
    </div>

    <ul>
      <!-- Обычные связи -->
      <li
        v-for="(relation, index) in modelValue"
        :key="'rel-' + index"
        class="flex justify-between items-center mb-1"
      >
        <span>{{ relation.type }}: {{ relation.target_character }}</span>
        <button @click.prevent="removeRelation(relation.type, relation.target_character)" class="text-red-500">Remove</button>
      </li>

      <!-- Зелья -->
      <li
        v-for="name in poisons"
        :key="'poison-' + name"
        class="flex justify-between items-center mb-1"
      >
        <span>Brewed: {{ name }}</span>
        <button @click.prevent="removeRelation('brewed', name)" class="text-red-500">Remove</button>
      </li>

      <!-- Заклинания -->
      <li
        v-for="name in spells"
        :key="'spell-' + name"
        class="flex justify-between items-center mb-1"
      >
        <span>Knows: {{ name }}</span>
        <button @click.prevent="removeRelation('knows', name)" class="text-red-500">Remove</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.input {
  background-color: #093062;
  border: 1px solid gold;
  color: gold;
  padding: 0.5em;
  border-radius: 4px;
  display: block;
}
</style>
