<script setup>
import { ref } from 'vue'

const addItemModal = ref(false)
const name = ref('')
const description = ref('')
const imageFile = ref(null)

const toggleModal = (e) => {
  e.stopPropagation()
  addItemModal.value = !addItemModal.value
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file
  }
}

const handleSubmit = () => {
  const id = name.value.toLowerCase().replace(/\s+/g, '-')
  const reader = new FileReader()

  reader.onload = () => {
    const newItem = {
      id,
      name: name.value,
      description: description.value,
      image_path: reader.result // base64
    }
    console.log('Добавленный персонаж:', newItem)
    // emit или запрос на сервер
    toggleModal(new Event('click'))
    name.value = ''
    description.value = ''
    imageFile.value = null
  }

  if (imageFile.value) {
    reader.readAsDataURL(imageFile.value)
  }
}
</script>

<template>
  <li class="flex justify-center" @click="toggleModal">
    <div class="w-50 h-60 bg-bg flex flex-col items-center pt-2 rounded-md cursor-pointer">
      <img class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed" src="/images/add.svg" />
      <p class="text-gold text-lg">Add Item</p>
    </div>

    <div
      v-if="addItemModal"
      class="w-[700px] h-[500px] absolute bg-bg top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] rounded-[10px] border-2 border-gold p-6"
      @click.stop
    >
      <div class="relative w-full h-full flex flex-col justify-between">
        <button
          class="absolute top-4 right-4 border border-gold w-10 h-10 rounded-[10px] text-gold text-xl"
          @click="toggleModal"
        >
          ×
        </button>

        <div class="flex flex-col gap-4 mt-8">
          <div>
            <label class="block mb-2 text-gold text-lg font-display">Name</label>
            <input
              v-model="name"
              type="text"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display"
              placeholder="Enter name"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Description</label>
            <textarea
              v-model="description"
              rows="8"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display resize-none"
              placeholder="Enter description"
            ></textarea>
          </div>

          <div class="flex items-center justify-between">
            <div>
              <label
                class="cursor-pointer inline-block border border-gold bg-bg text-gold px-4 py-2 rounded-md font-display hover:bg-gold hover:text-bg transition"
              >
                Add file
                <input
                  type="file"
                  accept="image/*"
                  @change="handleFileChange"
                  class="hidden"
                />
              </label>
              <span v-if="imageFile" class="text-gold ml-4 font-display">{{ imageFile.name }}</span>
            </div>

            <button
              @click="handleSubmit"
              class="px-6 py-2 border border-gold text-gold rounded-md font-display hover:bg-gold hover:text-bg transition"
            >
              Add
            </button>
          </div>
        </div>
      </div>
    </div>
  </li>
</template>
