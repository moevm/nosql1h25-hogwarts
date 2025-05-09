<script setup>
import { ref, onMounted, watch } from 'vue'
import { Network, DataSet } from 'vis-network/standalone/esm/vis-network'

const props = defineProps({
  characterId: {
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
      `${import.meta.env.VITE_SERVER_URL}/api/graph/character/${props.characterId}`
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
        springLength: 300, // Увеличь это значение, чтобы соединения стали длиннее
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
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-50">
    <div class="relative bg-bg p-12 rounded-lg w-[90%] max-w-[1000px] h-[600px] shadow-lg">
      <button class="absolute top-2 right-2 px-4 py-2 rounded text-gold" @click="closeGraph">
        X
      </button>

      <div ref="container" class="w-full h-full border-3 border-gold rounded-md" />
    </div>
  </div>
</template>
