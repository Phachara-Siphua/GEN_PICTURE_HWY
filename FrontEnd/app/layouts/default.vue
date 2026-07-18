<template>
  <div class="flex h-screen transition-colors duration-300 overflow-hidden font-prompt" :class="isDarkMode ? 'bg-gradient-to-br from-gray-900 to-gray-800 text-gray-200' : 'bg-gradient-to-br from-blue-50 to-indigo-50 text-gray-900'">
    
    <button @click="toggleDarkMode" class="fixed top-4 right-4 lg:right-6 z-50 p-2 md:p-3 rounded-full shadow-lg transition-transform hover:scale-110 font-bold text-xs md:text-base backdrop-blur-md border" :class="isDarkMode ? 'bg-gray-800/80 text-yellow-400 border-gray-600' : 'bg-white/80 text-indigo-600 border-white'">
        {{ isDarkMode ? '☀️ ธีมสว่าง' : '🌙 ธีมมืด' }}
    </button>

    <div class="lg:hidden fixed w-full z-40 flex justify-between items-center p-4 border-b backdrop-blur-xl transition-colors shadow-sm" :class="isDarkMode ? 'bg-gray-900/80 border-gray-700' : 'bg-white/80 border-white/50'">
        <div class="flex-1 flex justify-center pl-8">
            <img src="/img/logo.png" alt="Logo" class="h-10 object-contain drop-shadow-md" onerror="this.outerHTML='<h2 class=\'text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600\'>RunBi</h2>'">
        </div>
        <button @click="isSidebarOpen = !isSidebarOpen" class="text-2xl px-2 rounded focus:outline-none" :class="isDarkMode ? 'text-white' : 'text-gray-800'">
            ☰
        </button>
    </div>

    <div v-if="isSidebarOpen" @click="isSidebarOpen = false" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 lg:hidden transition-opacity"></div>

    <aside :class="(isSidebarOpen ? 'left-0 ' : '-left-64 lg:left-0 ') + (isDarkMode ? 'bg-gray-900/90 border-gray-700' : 'bg-white/80 border-white/50')" class="w-64 shadow-2xl flex flex-col border-r transition-all duration-300 fixed lg:relative z-50 h-full backdrop-blur-2xl">
      <div class="p-6 text-center border-b flex justify-between items-center lg:block" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200/50'">
        <div class="w-full flex justify-center">
            <img src="/img/logo.png" alt="Logo" class="h-20 w-full object-contain drop-shadow-lg mx-auto hover:scale-105 transition-transform" onerror="this.outerHTML='<h2 class=\'text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600\'>RunBi</h2>'">
        </div>
        <button @click="isSidebarOpen = false" class="lg:hidden text-gray-500 hover:text-red-500 text-xl font-bold">✕</button>
      </div>
      <nav class="flex-1 p-4 space-y-3 overflow-y-auto">
        <NuxtLink to="/" @click="isSidebarOpen = false" class="flex items-center gap-3 p-3 rounded-xl font-medium transition-all duration-200" :class="isDarkMode ? 'hover:bg-gray-800 hover:text-blue-400 hover:shadow-lg' : 'hover:bg-blue-100 hover:text-blue-700 hover:shadow-md'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
            สร้างรูป (Generator)
        </NuxtLink>
        <NuxtLink to="/promotion" @click="isSidebarOpen = false" class="flex items-center gap-3 p-3 rounded-xl font-bold transition-all duration-200" :class="isDarkMode ? 'hover:bg-gray-800 text-yellow-400 hover:text-yellow-300 hover:shadow-lg' : 'bg-gradient-to-r from-yellow-50 to-orange-50 text-orange-600 hover:from-yellow-100 hover:to-orange-100 hover:shadow-md border border-yellow-200/50'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"></path></svg>
            โปรโมชั่นราคา
        </NuxtLink>
        <NuxtLink to="/package" @click="isSidebarOpen = false" class="flex items-center gap-3 p-3 rounded-xl font-medium transition-all duration-200" :class="isDarkMode ? 'hover:bg-gray-800 hover:text-blue-400 hover:shadow-lg' : 'hover:bg-blue-100 hover:text-blue-700 hover:shadow-md'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
            ข้อมูลแพ็กเกจ
        </NuxtLink>
        <NuxtLink v-if="isAdmin" to="/admin" @click="isSidebarOpen = false" class="flex items-center gap-3 p-3 rounded-xl font-bold transition-all duration-200" :class="isDarkMode ? 'hover:bg-gray-800 text-purple-400 hover:text-purple-300 hover:shadow-lg' : 'bg-purple-50 text-purple-700 hover:bg-purple-100 hover:shadow-md'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            จัดการผู้ใช้งาน
        </NuxtLink>
        <a href="https://line.me/ti/p/~@402iopuh" target="_blank" class="flex items-center gap-3 p-3 rounded-xl font-medium transition-all duration-200" :class="isDarkMode ? 'hover:bg-gray-800 text-green-400 hover:text-green-300 hover:shadow-lg' : 'hover:bg-green-100 text-green-700 hover:shadow-md'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
            ติดต่อผ่าน Line
        </a>
      </nav>
      <div class="p-4 border-t" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200/50'">
        <button @click="logout" class="w-full p-3 bg-gradient-to-r from-red-500 to-rose-600 text-white rounded-xl hover:from-red-600 hover:to-rose-700 font-bold transition-all shadow-lg shadow-red-500/30 flex items-center justify-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
            ออกจากระบบ
        </button>
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
import { useState, useHead } from '#imports'

useHead({
  link: [{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap' }]
})

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

<style>
body {
  font-family: 'Prompt', sans-serif !important;
}
.font-prompt {
  font-family: 'Prompt', sans-serif !important;
}
</style>