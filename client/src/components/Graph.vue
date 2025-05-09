<script setup>
<<<<<<< Updated upstream
const emit = defineEmits(['closeModal'])
=======
import { ref, onMounted, watch } from 'vue'
import { Network, DataSet } from 'vis-network/standalone/esm/vis-network'

const props = defineProps({
  type: String,
  id: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close'])

const container = ref(null)
const nodes = ref([])
const edges = ref([])
let network = null

const fetchGraphData = async () => {
  try {
    const res = await fetch(
      `${import.meta.env.VITE_SERVER_URL}/api/graph/${props.type}/${props.id}`
    )
    const data = await res.json()
    nodes.value = data.nodes
    edges.value = data.edges
    drawGraph()
  } catch (err) {
    console.error('Failed to fetch graph data', err)
  }
}

const drawGraph = () => {
  if (!container.value) return

  const data = {
    nodes: new DataSet(
      nodes.value.map((n) => ({
        id: n.id,
        label: n.name,
        group: n.label,
        shape: n.image_path ? 'image' : 'dot',
        image: n.image_path || undefined,
        size: 30,
        font: { size: 16, color: '#fff' }
      }))
    ),
    edges: new DataSet(
      edges.value.map((e) => ({
        from: e.source,
        to: e.target,
        label: e.type,
        arrows: 'to'
      }))
    )
  }

  const options = {
    layout: { improvedLayout: true },
    physics: {
      enabled: true,
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        springLength: 300,
        springConstant: 0.01
      },
      stabilization: {
        iterations: 200
      }
    },
    edges: {
      color: '#aaa',
      font: { align: 'middle' }
    },
    groups: {
      Character: { color: { background: '#f39c12' } },
      Spell: { color: { background: '#3498db' } },
      House: { color: { background: '#2ecc71' } }
    }
  }

  network = new Network(container.value, data, options)
}

const closeGraph = () => {
  console.log('Graph close event emitted')
  emit('close')
}

onMounted(fetchGraphData)
watch(() => props.characterId, fetchGraphData)
>>>>>>> Stashed changes
</script>

<template>
    <div class="absolute w-full h-full bg-[#09306260] top-0 left-0 flex justify-end items-start">
        <button @click="emit('closeModal')" class="mt-10 mr-10 bg-bg rounded-[5px] border-3 border-gold text-gold px-4 py-2">X</button>
        <div class="absolute bg-bg top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] w-4/6 h-4/6 rounded-[10px] border-3 border-gold"></div>
    </div>
</template>