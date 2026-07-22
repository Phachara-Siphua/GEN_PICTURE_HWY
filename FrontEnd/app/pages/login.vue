<template>
  <div class="flex items-center justify-center min-h-screen p-4 transition-colors duration-300 font-prompt" :class="isDarkMode ? 'bg-gradient-to-br from-gray-900 to-gray-800' : 'bg-gradient-to-br from-blue-50 to-indigo-100'">
    
    <button @click="toggleDarkMode" class="fixed top-4 right-4 z-50 p-3 rounded-full shadow-xl transition-transform hover:scale-110 font-bold text-xs md:text-base backdrop-blur-md border" :class="isDarkMode ? 'bg-gray-800/80 text-yellow-400 border-gray-600' : 'bg-white/80 text-indigo-600 border-white'">
        {{ isDarkMode ? '☀️ ธีมสว่าง' : '🌙 ธีมมืด' }}
    </button>

    <div class="p-8 md:p-10 rounded-3xl shadow-2xl w-full max-w-sm transition-all duration-300 backdrop-blur-2xl border" :class="isDarkMode ? 'bg-gray-800/90 border-gray-700/50 shadow-black/50' : 'bg-white/90 border-white shadow-indigo-500/10'">
      
      <div class="flex justify-center mb-6">
        <img src="/img/logo.png" alt="Logo" class="h-20 object-contain drop-shadow-md" onerror="this.outerHTML='<h2 class=\'text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600\'>RunBi</h2>'">
      </div>
      
      <h2 class="text-xl font-bold text-center mb-8" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">ลงชื่อเข้าใช้งานระบบ</h2>
      <p v-if="errorMsg" class="text-red-500 text-sm mb-4 text-center font-bold bg-red-100/50 p-2 rounded-lg">{{ errorMsg }}</p>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-5">
          <label class="block text-sm font-semibold mb-2" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Username</label>
          <input v-model="username" type="text" class="w-full p-3.5 border rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white focus:bg-gray-700' : 'bg-gray-50 border-gray-200 focus:bg-white'" :disabled="isLoading" required>
        </div>
        
        <!-- 🎯 ช่อง Password แบบมีปุ่มกดดูรหัส (👁️) -->
        <div class="mb-8 relative">
          <label class="block text-sm font-semibold mb-2" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">Password</label>
          <div class="relative">
              <input v-model="password" :type="showPassword ? 'text' : 'password'" class="w-full p-3.5 pr-12 border rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white focus:bg-gray-700' : 'bg-gray-50 border-gray-200 focus:bg-white'" :disabled="isLoading" required>
              
              <!-- ปุ่มเปิด-ปิดตา -->
              <button type="button" @click="showPassword = !showPassword" class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-indigo-500 dark:text-gray-400 dark:hover:text-indigo-400 focus:outline-none transition-colors">
                  <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path></svg>
              </button>
          </div>
        </div>
        
        <button type="submit" :disabled="isLoading" class="w-full text-white font-bold py-3.5 rounded-xl shadow-lg transition-all flex justify-center items-center gap-2 transform active:scale-95" :class="isLoading ? 'bg-gray-500 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-blue-500/30'">
          <svg v-if="isLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isLoading ? 'กำลังเชื่อมต่อ...' : 'เข้าสู่ระบบ' }}
        </button>

        <p v-if="isLoading" class="text-xs text-center mt-4 opacity-70" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">
          (กำลังเตรียมระบบ...)
        </p>

        <div class="mt-8 pt-6 border-t text-center" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
            <p class="text-xs font-medium mb-3" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">พบปัญหา หรือต้องการเช่าแพ็กเกจ?</p>
            <a href="https://line.me/ti/p/~@402iopuh" target="_blank" class="w-full flex justify-center items-center gap-2 bg-gradient-to-r from-[#06C755] to-[#05b34c] text-white font-bold py-3 rounded-xl shadow-lg shadow-[#06C755]/30 hover:scale-[1.02] transition-transform">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
                ติดต่อแอดมิน (Line@)
            </a>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useState, useHead } from '#imports'

useHead({
  link: [{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap' }]
})

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
const showPassword = ref(false) // 🎯 ตัวแปรเก็บสถานะการโชว์รหัสผ่าน
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

<style>
body { font-family: 'Prompt', sans-serif !important; }
.font-prompt { font-family: 'Prompt', sans-serif !important; }
</style>