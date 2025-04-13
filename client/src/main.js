import './assets/main.css'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import { createApp } from 'vue'
import App from './App.vue'
import { createHead } from '@vueuse/head'
import CharacterList from './pages/CharacterList.vue'
import Character from './pages/Character.vue'
import PoisonList from './pages/PoisonList.vue'
import SpellList from './pages/SpellList.vue'
import HelloPage from './pages/HelloPage.vue'
import { createRouter, createWebHistory } from 'vue-router'

const head = createHead()

const routes = [
  { path: '/', component: HelloPage },
  { path: '/character', component: CharacterList },
  { path: '/character/:id', component: Character },
  { path: '/poisons', component: PoisonList },
  { path: '/spells', component: SpellList },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)

app.use(head)
app.use(router)
app.use(autoAnimatePlugin)

app.mount('#app')
