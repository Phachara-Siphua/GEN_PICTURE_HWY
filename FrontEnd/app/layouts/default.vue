<template>
  <div class="flex h-screen font-sans transition-colors duration-300 overflow-hidden" :class="isDarkMode ? 'bg-gray-900 text-gray-200' : 'bg-gray-100 text-gray-900'">
    
    <button @click="toggleDarkMode" class="fixed top-4 right-4 lg:right-6 z-50 p-2 md:p-3 rounded-full shadow-lg transition-transform hover:scale-110 font-bold text-xs md:text-base" :class="isDarkMode ? 'bg-yellow-400 text-gray-900' : 'bg-gray-800 text-white border border-gray-700'">
        {{ isDarkMode ? '☀️ ธีมสว่าง' : '🌙 ธีมมืด' }}
    </button>

    <div class="lg:hidden fixed w-full z-40 flex justify-between items-center p-4 border-b transition-colors" :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'">
        <!-- เปลี่ยนเป็น Logo -->
        <img src="/img/logo.png" alt="Logo" class="h-8 object-contain drop-shadow-sm" onerror="this.outerHTML='<h2 class=\'text-xl font-bold text-blue-500\'>Lottery Gen</h2>'">
        <button @click="isSidebarOpen = !isSidebarOpen" class="text-2xl px-2 rounded focus:outline-none" :class="isDarkMode ? 'text-white' : 'text-gray-800'">
            ☰
        </button>
    </div>

    <div v-if="isSidebarOpen" @click="isSidebarOpen = false" class="fixed inset-0 bg-black/50 z-40 lg:hidden"></div>

    <aside :class="[
        'w-64 shadow-xl flex flex-col border-r transition-all duration-300 fixed lg:relative z-50 h-full',
        isSidebarOpen ? 'left-0' : '-left-64 lg:left-0',
        isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
    ]">
      <div class="p-6 text-center border-b flex justify-between items-center lg:block" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
        <!-- เปลี่ยนเป็น Logo -->
        <div class="w-full flex justify-center lg:justify-start">
            <img src="/img/logo.png" alt="Logo" class="h-12 object-contain drop-shadow-sm" onerror="this.outerHTML='<h2 class=\'text-2xl font-bold text-blue-500\'>Lottery Gen</h2>'">
        </div>
        <button @click="isSidebarOpen = false" class="lg:hidden text-gray-500 hover:text-red-500 text-xl font-bold">✕</button>
      </div>
      <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
        <NuxtLink to="/" @click="isSidebarOpen = false" class="block p-3 rounded font-medium transition-colors" :class="isDarkMode ? 'hover:bg-gray-700 hover:text-blue-400' : 'hover:bg-blue-50 hover:text-blue-600'">🖼️ สร้างรูป (Generator)</NuxtLink>
        <NuxtLink to="/package" @click="isSidebarOpen = false" class="block p-3 rounded font-medium transition-colors" :class="isDarkMode ? 'hover:bg-gray-700 hover:text-blue-400' : 'hover:bg-blue-50 hover:text-blue-600'">📦 ข้อมูลแพ็กเกจ</NuxtLink>
        <NuxtLink v-if="isAdmin" to="/admin" @click="isSidebarOpen = false" class="block p-3 rounded font-bold transition-colors" :class="isDarkMode ? 'hover:bg-gray-700 text-purple-400 hover:text-purple-300' : 'hover:bg-purple-50 hover:text-purple-600 text-purple-700'">👑 จัดการผู้ใช้งาน (Admin)</NuxtLink>
        <a href="https://line.me/ti/p/~@402iopuh" target="_blank" class="block p-3 rounded font-medium transition-colors" :class="isDarkMode ? 'hover:bg-gray-700 text-green-400 hover:text-green-300' : 'hover:bg-green-50 text-green-600 hover:text-green-700'">💬 ติดต่อผ่าน Line</a>
      </nav>
      <div class="p-4 border-t" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
        <button @click="logout" class="w-full p-2 bg-red-500 text-white rounded hover:bg-red-600 font-bold transition-colors shadow">ออกจากระบบ</button>
      </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-4 md:p-6 relative pt-20 lg:pt-6 w-full">
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
const isSidebarOpen = ref(false)

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