<template>
  <div class="flex h-screen font-sans transition-colors duration-300" :class="isDarkMode ? 'bg-gray-900 text-gray-200' : 'bg-gray-100 text-gray-900'">
    
    <!-- ปุ่ม Theme (แสดงทุกหน้าที่มี Layout) -->
    <button @click="toggleDarkMode" class="fixed top-4 right-4 z-50 p-3 rounded-full shadow-lg transition-transform hover:scale-110 font-bold" :class="isDarkMode ? 'bg-yellow-400 text-gray-900' : 'bg-gray-800 text-white border border-gray-700'">
        {{ isDarkMode ? '☀️ ธีมสว่าง' : '🌙 ธีมมืด' }}
    </button>

    <aside :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'" class="w-64 shadow-lg flex flex-col border-r transition-colors duration-300">
      <div class="p-6 text-center border-b" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
        <h2 class="text-2xl font-bold" :class="isDarkMode ? 'text-blue-400' : 'text-blue-600'">RunBi</h2>
      </div>
      <nav class="flex-1 p-4 space-y-2">
        <NuxtLink to="/" class="block p-3 rounded font-medium transition-colors" :class="isDarkMode ? 'hover:bg-gray-700 hover:text-blue-400' : 'hover:bg-blue-50 hover:text-blue-600'">🖼️ สร้างรูป (Generator)</NuxtLink>
        <NuxtLink to="/package" class="block p-3 rounded font-medium transition-colors" :class="isDarkMode ? 'hover:bg-gray-700 hover:text-blue-400' : 'hover:bg-blue-50 hover:text-blue-600'">📦 ข้อมูลแพ็กเกจ</NuxtLink>
        <NuxtLink v-if="isAdmin" to="/admin" class="block p-3 rounded font-bold transition-colors" :class="isDarkMode ? 'hover:bg-gray-700 text-purple-400 hover:text-purple-300' : 'hover:bg-purple-50 hover:text-purple-600 text-purple-700'">👑 จัดการผู้ใช้งาน (Admin)</NuxtLink>
        <a href="https://line.me/ti/p/~@yourline" target="_blank" class="block p-3 rounded font-medium transition-colors" :class="isDarkMode ? 'hover:bg-gray-700 text-green-400 hover:text-green-300' : 'hover:bg-green-50 text-green-600 hover:text-green-700'">💬 ติดต่อผ่าน Line</a>
      </nav>
      <div class="p-4 border-t" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
        <button @click="logout" class="w-full p-2 bg-red-500 text-white rounded hover:bg-red-600 font-bold transition-colors">ออกจากระบบ</button>
      </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-6 relative">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useState } from '#imports'

const router = useRouter()
const isAdmin = ref(false)

const isDarkMode = useState('darkMode', () => false)

const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

onMounted(async () => {
    if (localStorage.getItem('theme') === 'dark') {
        isDarkMode.value = true
    }

    const token = localStorage.getItem('token')
    if (token) {
        try {
            const res = await fetch('https://gen-picture-hwy.onrender.com/users/me', { headers: { 'Authorization': `Bearer ${token}` } })
            if (res.ok) {
                const data = await res.json()
                if (data.role === 'admin') isAdmin.value = true
            }
        } catch (e) {}
    }
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>