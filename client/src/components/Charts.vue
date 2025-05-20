<template>
  <div class="chart-wrapper">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue'
import Chart from 'chart.js/auto'
import zoomPlugin from 'chartjs-plugin-zoom'

// Подключаем плагин
Chart.register(zoomPlugin)

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

const xLabels = computed(() => [...new Set(props.data.map(item => item.x))])
const yLabels = computed(() => [...new Set(props.data.map(item => item.y))])

function prepareDataset(data) {
  return data.map(item => ({
    x: item.x,
    y: item.y,
    r: Math.max(item.count, 3)
  }))
}

function renderChart() {
  if (!canvasRef.value) return

  const ctx = canvasRef.value.getContext('2d')
  const bubbleData = prepareDataset(props.data)

  if (chartInstance) chartInstance.destroy()

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
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'category',
          labels: xLabels.value,
          title: {
            display: true,
            text: props.xAxis
          },
          ticks: {
            autoSkip: true,
            maxTicksLimit: 15,
            maxRotation: 45,
            minRotation: 0
          }
        },
        y: {
          type: 'category',
          labels: yLabels.value,
          title: {
            display: true,
            text: props.yAxis
          },
          ticks: {
            autoSkip: true,
            maxTicksLimit: 15
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label(ctx) {
              const { x, y, r } = ctx.raw
              return `${props.xAxis}: ${x} | ${props.yAxis}: ${y} | Count: ${r}`
            }
          }
        },
        legend: {
          display: false
        },
        zoom: {
          pan: {
            enabled: true,
            mode: 'xy',
            // modifierKey: 'ctrl' // чтобы избежать случайных перемещений
          },
          zoom: {
            wheel: {
              enabled: true
            },
            pinch: {
              enabled: true
            },
            mode: 'xy'
          }
        }
      }
    }
  })
}

onMounted(renderChart)

watch(
  () => [props.data, props.xAxis, props.yAxis],
  renderChart,
  { deep: true }
)

onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy()
})
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

canvas {
  flex-grow: 1;
  width: 100% !important;
  height: 100% !important;
  display: block;
}
</style>
