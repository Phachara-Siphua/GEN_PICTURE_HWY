<template>
  <div class="min-h-screen transition-colors duration-300 pb-20 font-prompt" :class="isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-800'">
    
    <!-- หน้าจอหมุนโหลด -->
    <div v-show="isLoading" class="flex flex-col items-center justify-center h-[80vh]">
        <div class="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-orange-500 mb-6"></div>
        <h2 class="text-2xl font-bold text-orange-500 animate-pulse">กำลังโหลดโปรโมชั่น...</h2>
    </div>

    <!-- เนื้อหาหลัก -->
    <div v-show="!isLoading" class="max-w-5xl mx-auto pt-12">
      
      <div class="text-center mb-12 px-4">
          <span class="inline-flex items-center gap-2 px-6 py-2.5 rounded-full font-bold text-sm tracking-widest uppercase bg-gradient-to-r from-yellow-400 to-orange-500 text-white shadow-lg shadow-orange-500/30 mb-6">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
              Special Offers
          </span>
          <h1 class="text-3xl md:text-5xl font-extrabold flex flex-col md:flex-row items-center justify-center gap-4 md:gap-6" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
            <div class="p-4 bg-gradient-to-tr from-yellow-400 to-orange-500 rounded-2xl shadow-xl shadow-orange-500/40 text-white transform hover:scale-110 transition-transform">
                <svg class="w-10 h-10 md:w-12 md:h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"></path></svg>
            </div>
            <span>โปรโมชั่น & แพ็กเกจสุดคุ้ม</span>
          </h1>
      </div>
      
      <div class="flex flex-col gap-12 items-center px-4">
        
        <a href="https://line.me/ti/p/~@402iopuh" target="_blank" class="block rounded-3xl overflow-hidden shadow-2xl transition-transform hover:scale-[1.02] w-full max-w-2xl backdrop-blur-xl border border-white/20 cursor-pointer" :class="isDarkMode ? 'bg-gray-800/80 shadow-black/50' : 'bg-white/80 shadow-orange-500/10'">
          <img src="/img/Pro1.png" alt="แพ็กเกจเริ่มต้น" class="w-full object-cover">
        </a>
        
        <a href="https://line.me/ti/p/~@402iopuh" target="_blank" class="block rounded-3xl overflow-hidden shadow-2xl transition-transform hover:scale-[1.02] w-full max-w-2xl backdrop-blur-xl border border-white/20 cursor-pointer" :class="isDarkMode ? 'bg-gray-800/80 shadow-black/50' : 'bg-white/80 shadow-orange-500/10'">
          <img src="/img/Pro2.png" alt="แพ็กเกจเสริม" class="w-full object-cover">
        </a>

        <div class="mt-8 text-center w-full">
          <a href="https://line.me/ti/p/~@402iopuh" target="_blank" class="inline-flex justify-center items-center gap-3 bg-gradient-to-r from-[#06C755] to-[#05b34c] text-white px-10 py-5 rounded-full font-extrabold hover:scale-105 transition-transform shadow-xl shadow-[#06C755]/30 text-lg md:text-xl animate-bounce w-full max-w-md">
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
            สนใจสมัครแพ็กเกจ แอด Line เลย!
          </a>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useState } from '#imports'

const isDarkMode = useState('darkMode', () => false)
const isLoading = ref(true)

onMounted(() => {
    // หน่วงเวลาโหลดเล็กน้อยให้ดูสมูท
    setTimeout(() => {
        isLoading.value = false;
    }, 500);
})
</script>