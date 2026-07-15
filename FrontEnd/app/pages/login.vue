<template>
  <div class="flex items-center justify-center min-h-screen p-4 transition-colors duration-300" :class="isDarkMode ? 'bg-gray-900' : 'bg-gray-100'">
    
    <button @click="toggleDarkMode" class="fixed top-4 right-4 z-50 p-3 rounded-full shadow-lg transition-transform hover:scale-110 font-bold text-xs md:text-base" :class="isDarkMode ? 'bg-yellow-400 text-gray-900' : 'bg-gray-800 text-white'">
        {{ isDarkMode ? '☀️ ธีมสว่าง' : '🌙 ธีมมืด' }}
    </button>

    <div class="p-6 md:p-8 rounded-xl shadow-2xl w-full max-w-sm transition-colors duration-300" :class="isDarkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white'">
      <h2 class="text-2xl font-bold text-center mb-6" :class="isDarkMode ? 'text-blue-400' : 'text-blue-600'">เข้าสู่ระบบ</h2>
      <p v-if="errorMsg" class="text-red-500 text-sm mb-4 text-center font-bold">{{ errorMsg }}</p>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-sm font-bold mb-2" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Username</label>
          <input v-model="username" type="text" class="w-full p-3 border rounded focus:outline-none focus:border-blue-500 transition-colors" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'" :disabled="isLoading" required>
        </div>
        <div class="mb-6">
          <label class="block text-sm font-bold mb-2" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Password</label>
          <input v-model="password" type="password" class="w-full p-3 border rounded focus:outline-none focus:border-blue-500 transition-colors" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'" :disabled="isLoading" required>
        </div>
        
        <button type="submit" :disabled="isLoading" class="w-full text-white font-bold py-3 rounded shadow-lg transition-all flex justify-center items-center gap-2" :class="isLoading ? 'bg-gray-500 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 hover:shadow-blue-500/50'">
          <svg v-if="isLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isLoading ? 'กำลังปลุกเซิร์ฟเวอร์...' : 'เข้าสู่ระบบ' }}
        </button>

        <p v-if="isLoading" class="text-xs text-center mt-3 opacity-70" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
          (หากไม่มีการใช้งานนาน อาจใช้เวลา 30-50 วินาที)
        </p>

        <!-- เพิ่มปุ่มติดต่อ Line@ ตรงหน้า Login -->
        <div class="mt-6 border-t pt-4 text-center" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
            <p class="text-sm mb-3" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">พบปัญหา หรือต้องการเช่าแพ็กเกจ?</p>
            <a href="https://line.me/ti/p/~@402iopuh" target="_blank" class="w-full inline-block bg-[#06C755] text-white font-bold py-2.5 rounded shadow hover:bg-[#05b34c] transition-colors">
                💬 ติดต่อแอดมิน (Line@)
            </a>
        </div>
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
const isLoading = ref(false) 
const router = useRouter()

const handleLogin = async () => {
  isLoading.value = true 
  errorMsg.value = ''    
  
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
  } finally {
    isLoading.value = false 
  }
}
</script>