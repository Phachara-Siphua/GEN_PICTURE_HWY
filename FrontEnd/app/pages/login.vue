<template>
  <div class="flex items-center justify-center h-screen bg-gray-800">
    <div class="bg-white p-8 rounded-lg shadow-xl w-96">
      <h2 class="text-2xl font-bold text-center text-blue-600 mb-6">เข้าสู่ระบบ</h2>
      <p v-if="errorMsg" class="text-red-500 text-sm mb-4 text-center">{{ errorMsg }}</p>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">Username</label>
          <input v-model="username" type="text" class="w-full p-3 border rounded focus:outline-none focus:border-blue-500" required>
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">Password</label>
          <input v-model="password" type="password" class="w-full p-3 border rounded focus:outline-none focus:border-blue-500" required>
        </div>
        <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 rounded hover:bg-blue-700">เข้าสู่ระบบ</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({ layout: false }) // ไม่ใช้ Sidebar

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const formData = new URLSearchParams()
    formData.append('username', username.value)
    formData.append('password', password.value)

    const response = await fetch('http://localhost:8000/token', {
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