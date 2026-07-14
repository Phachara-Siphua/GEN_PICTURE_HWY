<template>
  <div class="flex items-center justify-center h-screen transition-colors duration-300" :class="isDarkMode ? 'bg-gray-900' : 'bg-gray-100'">
    
    <button @click="toggleDarkMode" class="fixed top-4 right-4 z-50 p-3 rounded-full shadow-lg transition-transform hover:scale-110 font-bold" :class="isDarkMode ? 'bg-yellow-400 text-gray-900' : 'bg-gray-800 text-white'">
        {{ isDarkMode ? '☀️ ธีมสว่าง' : '🌙 ธีมมืด' }}
    </button>

    <div class="p-8 rounded-xl shadow-2xl w-96 transition-colors duration-300" :class="isDarkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white'">
      <h2 class="text-2xl font-bold text-center mb-6" :class="isDarkMode ? 'text-blue-400' : 'text-blue-600'">เข้าสู่ระบบ</h2>
      <p v-if="errorMsg" class="text-red-500 text-sm mb-4 text-center font-bold">{{ errorMsg }}</p>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-sm font-bold mb-2" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Username</label>
          <input v-model="username" type="text" class="w-full p-3 border rounded focus:outline-none focus:border-blue-500 transition-colors" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'" required>
        </div>
        <div class="mb-6">
          <label class="block text-sm font-bold mb-2" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Password</label>
          <input v-model="password" type="password" class="w-full p-3 border rounded focus:outline-none focus:border-blue-500 transition-colors" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'" required>
        </div>
        <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 rounded hover:bg-blue-700 shadow-lg hover:shadow-blue-500/50 transition-all">เข้าสู่ระบบ</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useState } from '#imports'

definePageMeta({ layout: false })

const isDarkMode = useState('darkMode', () => false)
const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

onMounted(() => {
    if (localStorage.getItem('theme') === 'dark') isDarkMode.value = true
})

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const formData = new URLSearchParams()
    formData.append('username', username.value)
    formData.append('password', password.value)

    const response = await fetch('https://gen-picture-hwy.onrender.com/token', {
      method: 'POST',
      body: formData
    })

    const data = await response.json()
    if (response.ok) {
      localStorage.setItem('token', data.access_token)
      router.push('/')
    } else {
      errorMsg.value = data.detail
    }
  } catch (error) {
    errorMsg.value = "ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้"
  }
}
</script>