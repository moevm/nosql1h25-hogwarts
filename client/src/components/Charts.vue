<template>
  <div class="chart-wrapper">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue'
import Chart from 'chart.js/auto'
import zoomPlugin from 'chartjs-plugin-zoom'

// Регистрируем плагин
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

// Уникальные значения для осей
const xKeys = computed(() => [...new Set(props.data.map(item => item.x))].sort())
const yKeys = computed(() => [...new Set(props.data.map(item => item.y))].sort())

// Маппинг значений в индексы
const xMap = computed(() => Object.fromEntries(xKeys.value.map((v, i) => [v, i])))
const yMap = computed(() => Object.fromEntries(yKeys.value.map((v, i) => [v, i])))

// Подготовка данных
function prepareDataset(data) {
  const max = Math.max(...data.map(d => d.count))
  return data.map(item => ({
    x: xMap.value[item.x],
    y: yMap.value[item.y],
    r: (item.count / max) * 25 + 5, // масштабирование радиуса
    xLabel: item.x,
    yLabel: item.y
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
      datasets: [{
        label: 'Statistics',
        data: bubbleData,
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'category',
          labels: xKeys.value,
          title: {
            display: true,
            text: props.xAxis
          },
          ticks: {
            maxRotation: 45,
          },
        },
        y: {
          type: 'category',
          labels: yKeys.value,
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
              const { xLabel, yLabel, r } = ctx.raw
              const maxCount = Math.max(...props.data.map(d => d.count))
              const count = Math.round((r - 5) / 25 * maxCount)
              return `${props.xAxis}: ${xLabel} | ${props.yAxis}: ${yLabel} | Count: ${count}`
            }
          }
        },
        zoom: {
          zoom: {
            wheel: { enabled: true },
            drag: {
              enabled: true,
              backgroundColor: 'rgba(75,192,192,0.15)',
              borderColor: 'rgba(75,192,192,0.25)'
            },
            mode: 'xy'
          },
          pan: {
            enabled: true,
            mode: 'xy',
            modifierKey: 'ctrl'
          },
          limits: {
            x: { minRange: 1 },
            y: { minRange: 1 }
          }
        }
      }
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
  height: 100%;
  padding: 1rem;
  box-sizing: border-box;
}
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
