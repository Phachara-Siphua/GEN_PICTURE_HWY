<template>
  <div class="transition-colors duration-300 min-h-screen">
    
    <!-- หน้าจอหมุนโหลด -->
    <div v-show="isLoading" class="flex flex-col items-center justify-center h-[80vh]">
        <div class="animate-spin rounded-full h-24 w-24 border-t-4 border-b-4 border-blue-500 mb-6"></div>
        <h2 class="text-2xl font-bold text-blue-500 animate-pulse">กำลังโหลดข้อมูลแพ็กเกจ...</h2>
    </div>

    <!-- ข้อมูลแพ็กเกจ -->
    <div v-show="!isLoading" class="p-8 rounded-lg shadow-md max-w-2xl mx-auto mt-10 transition-colors duration-300" :class="isDarkMode ? 'bg-gray-800 border border-gray-700' : 'bg-white'">
      <h1 class="text-3xl font-bold mb-6 border-b pb-4" :class="isDarkMode ? 'text-blue-400 border-gray-700' : 'text-blue-700 border-gray-200'">📦 ข้อมูลแพ็กเกจของคุณ</h1>
      <div v-if="userInfo" class="text-lg space-y-5" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
        <p class="flex items-center">
          <span class="w-10 text-2xl">👤</span> 
          <strong class="w-40">ชื่อผู้ใช้:</strong> {{ userInfo.username }}
        </p>
        <p class="flex items-center">
          <span class="w-10 text-2xl">📅</span> 
          <strong class="w-40">วันที่เริ่มแพ็กเกจ:</strong> 
          <span class="font-bold px-3 py-1 rounded" :class="isDarkMode ? 'bg-green-900/50 text-green-400' : 'bg-green-50 text-green-600'">{{ formatDate(userInfo.sub_start) }}</span>
        </p>
        <p class="flex items-center">
          <span class="w-10 text-2xl">⏳</span> 
          <strong class="w-40">หมดอายุเมื่อ:</strong> 
          <span class="font-bold px-3 py-1 rounded" :class="isDarkMode ? 'bg-red-900/50 text-red-400' : 'bg-red-50 text-red-500'">{{ formatDate(userInfo.sub_end) }}</span>
        </p>
        <p class="flex items-center">
          <span class="w-10 text-2xl">💾</span> 
          <strong class="w-40">โควต้ารูปแบบ:</strong> 
          <span class="font-bold" :class="isDarkMode ? 'text-indigo-400' : 'text-indigo-600'">{{ formatCount }} / {{ userInfo.max_formats }} รูปแบบ</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useState } from '#imports'

const isLoading = ref(true)
const isDarkMode = useState('darkMode')
const userInfo = ref(null)
const formatCount = ref(0)
const router = useRouter()

const formatDate = (dateStr) => {
    if(!dateStr) return '-';
    return new Date(dateStr).toLocaleString('th-TH', { 
        year: 'numeric', month: 'long', day: 'numeric', 
        hour: '2-digit', minute: '2-digit', second: '2-digit' 
    });
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')

  try {
      const res = await fetch('https://gen-picture-hwy.onrender.com/users/me', { headers: { 'Authorization': `Bearer ${token}` } });
      if (res.ok) userInfo.value = await res.json();
      else router.push('/login');

      const resFormat = await fetch('https://gen-picture-hwy.onrender.com/formats', { headers: { 'Authorization': `Bearer ${token}` } });
      if (resFormat.ok) {
          const formats = await resFormat.json();
          formatCount.value = formats.length;
      }
  } catch (error) {
      console.log(error);
  }

  isLoading.value = false;
})
</script>