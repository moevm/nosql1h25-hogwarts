<script setup>
import { ref } from 'vue'

const emit = defineEmits(['fetchUpdate'])

const addItemModal = ref(false)
const name = ref('')
const description = ref('')
const imageFile = ref(null)
const born = ref('')
const died = ref('')
const bloodStatus = ref('')
const gender = ref('')
const house = ref('')
const spells = ref('')
const poisons = ref('')
const relationships = ref('')

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

  reader.onload = async () => {
    const newItem = {
      id,
      name: name.value,
      born: born.value || null,
      died: died.value || null,
      blood_status: bloodStatus.value,
      gender: gender.value,
      description: description.value,
      house: house.value,
      spells: spells.value
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean),
      poisons: poisons.value
        .split(',')
        .map((p) => p.trim())
        .filter(Boolean),
      relationships: relationships.value
        .split(',')
        .map((r) => {
          const [target_character, type] = r.split(':').map((s) => s.trim())
          return { target_character, type }
        })
        .filter((rel) => rel.target_character && rel.type),
      image_path: reader.result
    }

    try {
      const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newItem)
      })

      if (!response.ok) {
        throw new Error('Ошибка при добавлении персонажа')
      }

      const result = await response.json()
      console.log('Успешно отправлено:', result)
      alert('Персонаж добавлен!')

      // Очистка
      toggleModal(new Event('click'))
      name.value = ''
      description.value = ''
      born.value = ''
      died.value = ''
      bloodStatus.value = ''
      gender.value = ''
      house.value = ''
      spells.value = ''
      poisons.value = ''
      relationships.value = ''
      imageFile.value = null
    } catch (error) {
      console.error('Ошибка при отправке:', error)
      alert('Произошла ошибка при добавлении персонажа.')
    } finally {
      emit('fetchUpdate', `${import.meta.env.VITE_SERVER_URL}/api/characters`)
    }
  }

  if (imageFile.value) {
    reader.readAsDataURL(imageFile.value) // Start reading the file
  } else {
    // Handle case where no file is selected
    reader.onload()
  }
}
</script>

<template>
  <li class="flex justify-center" @click="toggleModal">
    <div class="w-50 h-60 bg-bg flex flex-col items-center pt-2 rounded-md cursor-pointer">
      <img class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed" src="/images/add.svg" />
      <p class="text-gold text-lg">Add Character</p>
    </div>

    <div
      v-if="addItemModal"
      class="w-[700px] h-[500px] absolute bg-bg top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] rounded-[10px] border-2 border-gold p-6 overflow-y-auto scrollbar-hide"
      @click.stop
    >
      <div class="relative w-full h-[500px] flex flex-col justify-between">
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
              rows="3"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold placeholder:text-[#6C6F27] font-display resize-none"
              placeholder="Enter description"
            ></textarea>
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Born</label>
            <input
              v-model="born"
              type="date"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Died</label>
            <input
              v-model="died"
              type="date"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Blood Status</label>
            <input
              v-model="bloodStatus"
              type="text"
              placeholder="pure-blood / muggle-born"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Gender</label>
            <input
              v-model="gender"
              type="text"
              placeholder="male / female / other"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">House</label>
            <input
              v-model="house"
              type="text"
              placeholder="e.g. Gryffindor"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Spells</label>
            <input
              v-model="spells"
              type="text"
              placeholder="Comma-separated: Expelliarmus, Lumos"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Poisons</label>
            <input
              v-model="poisons"
              type="text"
              placeholder="Comma-separated"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div>
            <label class="block mb-2 text-gold text-lg font-display">Relationships</label>
            <input
              v-model="relationships"
              type="text"
              placeholder="e.g. Harry Potter: friend, Draco Malfoy: enemy"
              class="w-full p-2 rounded border border-gold bg-transparent text-gold font-display"
            />
          </div>

          <div class="flex items-center justify-between">
            <div>
              <label
                class="cursor-pointer inline-block border border-gold bg-bg text-gold px-4 py-2 rounded-md font-display hover:bg-gold hover:text-bg transition"
              >
                Add file
                <input type="file" accept="image/*" @change="handleFileChange" class="hidden" />
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
