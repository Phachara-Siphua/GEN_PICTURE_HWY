<template>
  <div class="flex h-screen bg-gray-100 font-sans">
    <aside class="w-64 bg-white shadow-lg flex flex-col">
      <div class="p-6 text-center border-b">
        <h2 class="text-2xl font-bold text-blue-600">Lottery Gen</h2>
      </div>
      <nav class="flex-1 p-4 space-y-2">
        <NuxtLink to="/" class="block p-3 rounded hover:bg-blue-50 hover:text-blue-600 font-medium">🖼️ สร้างรูป (Generator)</NuxtLink>
        <NuxtLink to="/package" class="block p-3 rounded hover:bg-blue-50 hover:text-blue-600 font-medium">📦 ข้อมูลแพ็กเกจ</NuxtLink>
        <NuxtLink v-if="isAdmin" to="/admin" class="block p-3 rounded hover:bg-purple-50 hover:text-purple-600 font-bold text-purple-700">👑 จัดการผู้ใช้งาน (Admin)</NuxtLink>
        <a href="https://line.me/ti/p/~@yourline" target="_blank" class="block p-3 rounded hover:bg-green-50 hover:text-green-600 font-medium text-green-600">💬 ติดต่อผ่าน Line</a>
      </nav>
      <div class="p-4 border-t">
        <button @click="logout" class="w-full p-2 bg-red-500 text-white rounded hover:bg-red-600 font-bold">ออกจากระบบ</button>
      </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-6">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isAdmin = ref(false)

onMounted(async () => {
    const token = localStorage.getItem('token')
    if (token) {
        try {
            const res = await fetch('http://localhost:8000/users/me', { headers: { 'Authorization': `Bearer ${token}` } })
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