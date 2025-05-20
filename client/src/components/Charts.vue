<template>
  <div class="chart-wrapper">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue'
import Chart from 'chart.js/auto'

// Props: массив объектов { x, y, count }
const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  xAxis: {
    type: String,
    required: true
  },
  yAxis: {
    type: String,
    required: true
  }
})

const canvasRef = ref(null)
let chartInstance = null

// Собираем уникальные метки для каждой оси
const xLabels = computed(() =>
  Array.from(new Set(props.data.map(item => item.x)))
)
const yLabels = computed(() =>
  Array.from(new Set(props.data.map(item => item.y)))
)

// Преобразование API-данных в данные для bubble-графика
function prepareDataset(data) {
  return data.map(item => ({
    x: item.x,
    y: item.y,
    r: item.count    // размер пузырька
  }))
}

function renderChart() {
  if (!canvasRef.value) return
  const ctx = canvasRef.value.getContext('2d')
  const bubbleData = prepareDataset(props.data)

  if (chartInstance) {
    chartInstance.destroy()
  }

  chartInstance = new Chart(ctx, {
    type: 'bubble',
    data: {
      datasets: [{
        label: 'Statistics',
        data: bubbleData,
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        borderColor:     'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        x: {
          type: 'category',
          labels: xLabels.value,
          offset: true,              // смещение меток от краёв
          ticks: {
            padding: 10             // внутренний отступ
          },
          title: {
            display: true,
            text: props.xAxis
          }
        },
        y: {
          type: 'category',
          labels: yLabels.value,
          offset: true,              // смещение меток от краёв
          ticks: {
            padding: 10             // внутренний отступ
          },
          title: {
            display: true,
            text: props.yAxis
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label(ctx) {
              const { x, y, r } = ctx.raw
              const count = r / 4
              return `${props.xAxis}: ${x} | ${props.yAxis}: ${y} | Count: ${count}`
            }
          }
        }
      },
      responsive: true,
      maintainAspectRatio: false
    }
  })
}

onMounted(renderChart)
watch(() => props.data, renderChart, { deep: true })
onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy()
})
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  max-width: 800px;
  margin: 20px auto;
  height: 400px;
}
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
