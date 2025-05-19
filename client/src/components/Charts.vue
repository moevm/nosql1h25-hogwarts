<template>
  <div class="chart-wrapper">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
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

// Преобразование API-данных в данные для bubble-графика
function prepareDataset(data) {
  return data.map(item => ({
    x: item.x,
    y: item.y,
    // множитель можно настраивать для визуального размера
    r: item.count * 4
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
      datasets: [
        {
          label: 'Statistics',
          data: bubbleData,
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      scales: {
        x: {
          type: 'category',
          title: {
            display: true,
            text: props.xAxis
          }
        },
        y: {
          type: 'category',
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
      }
    }
  })
}

onMounted(() => {
  renderChart()
})

watch(
  () => [props.data, props.xAxis, props.yAxis],
  () => {
    renderChart()
  },
  { deep: true }
)

onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy()
})
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  max-width: 800px;
  margin: 20px auto;
}
</style>