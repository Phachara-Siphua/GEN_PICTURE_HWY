<template>
  <div class="transition-colors duration-300 min-h-screen font-prompt">
    
    <div v-show="isLoading" class="flex flex-col items-center justify-center h-[80vh]">
        <div class="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-blue-500 mb-6"></div>
        <h2 class="text-2xl font-bold text-blue-500 animate-pulse">กำลังโหลดข้อมูลแพ็กเกจ...</h2>
    </div>

    <div v-show="!isLoading" class="p-8 md:p-12 rounded-3xl shadow-2xl w-full max-w-2xl mx-auto mt-6 md:mt-12 transition-all backdrop-blur-xl border" :class="isDarkMode ? 'bg-gray-800/80 border-gray-700/50 shadow-black/30' : 'bg-white/80 border-white/50 shadow-blue-500/10'">
      
      <div class="flex items-center gap-4 border-b pb-6 mb-8" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
          <div class="p-4 bg-gradient-to-br from-blue-100 to-indigo-100 text-indigo-600 rounded-2xl shadow-sm">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
          </div>
          <h1 class="text-3xl md:text-4xl font-extrabold" :class="isDarkMode ? 'text-white' : 'text-gray-800'">ข้อมูลแพ็กเกจของคุณ</h1>
      </div>

      <div v-if="userInfo" class="text-lg md:text-xl space-y-6" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
        
        <div class="flex flex-col md:flex-row md:items-center p-4 rounded-2xl transition-colors" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
          <span class="flex items-center w-48 text-gray-500 dark:text-gray-400 font-medium"><svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>ชื่อผู้ใช้งาน:</span> 
          <span class="mt-2 md:mt-0 font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{ userInfo.username }}</span>
        </div>
        
        <div class="flex flex-col md:flex-row md:items-center p-4 rounded-2xl transition-colors" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
          <span class="flex items-center w-48 text-gray-500 dark:text-gray-400 font-medium"><svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>วันที่เริ่มแพ็กเกจ:</span> 
          <span class="mt-2 md:mt-0 font-bold px-4 py-1.5 rounded-xl shadow-sm w-fit" :class="isDarkMode ? 'bg-emerald-900/40 text-emerald-400 border border-emerald-800' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'">{{ formatDate(userInfo.sub_start) }}</span>
        </div>
        
        <div class="flex flex-col md:flex-row md:items-center p-4 rounded-2xl transition-colors" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
          <span class="flex items-center w-48 text-gray-500 dark:text-gray-400 font-medium"><svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>หมดอายุเมื่อ:</span> 
          <span class="mt-2 md:mt-0 font-bold px-4 py-1.5 rounded-xl shadow-sm w-fit" :class="isDarkMode ? 'bg-rose-900/40 text-rose-400 border border-rose-800' : 'bg-rose-50 text-rose-700 border border-rose-200'">{{ formatDate(userInfo.sub_end) }}</span>
        </div>
        
        <div class="flex flex-col md:flex-row md:items-center p-4 rounded-2xl transition-colors" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
          <span class="flex items-center w-48 text-gray-500 dark:text-gray-400 font-medium"><svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"></path></svg>โควต้าเทมเพลต:</span> 
          <span class="mt-2 md:mt-0 font-extrabold text-2xl" :class="isDarkMode ? 'text-indigo-400' : 'text-indigo-600'">{{ formatCount }} <span class="text-lg text-gray-400">/ {{ userInfo.max_formats }}</span></span>
        </div>

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