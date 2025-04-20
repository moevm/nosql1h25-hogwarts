<!-- components/AddCharacterForm.vue -->
<template>
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-96">
        <h2 class="text-xl font-bold mb-4">Добавить персонажа</h2>
        <form @submit.prevent="submitForm" class="flex flex-col gap-4">
          <input v-model="name" type="text" placeholder="Имя" class="border p-2 rounded" required />
          <textarea v-model="description" placeholder="Описание" class="border p-2 rounded" required />
          <input @change="handleImageUpload" type="file" accept="image/*" required />
          <div class="flex gap-2 justify-end">
            <button type="button" @click="$emit('close')" class="px-4 py-2 bg-gray-300 rounded">Отмена</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded">Добавить</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const emit = defineEmits(['add', 'close'])
  
  const name = ref('')
  const description = ref('')
  const imageFile = ref(null)
  
  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      imageFile.value = URL.createObjectURL(file) // временный путь
    }
  }
  
  const submitForm = () => {
    emit('add', {
      name: name.value,
      description: description.value,
      imageUrl: imageFile.value || '' // если вдруг не выбрано изображение
    })
    emit('close')
    name.value = ''
    description.value = ''
    imageFile.value = null
  }
  </script>
  