<template>
  <div class="min-h-screen transition-colors duration-300 pb-20" :class="isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-800'">
    <div class="max-w-5xl mx-auto pt-8">
      <h1 class="text-3xl md:text-5xl font-bold mb-10 text-center" :class="isDarkMode ? 'text-yellow-400' : 'text-blue-600'">
        🎁 โปรโมชั่น & แพ็กเกจสุดคุ้ม
      </h1>
      
      <div class="flex flex-col gap-10 items-center px-4">
        
        <!-- รูปโปรโมชั่นที่ 1 -->
        <div class="rounded-2xl overflow-hidden shadow-2xl border-4 transition-transform hover:scale-[1.02] w-full max-w-2xl" :class="isDarkMode ? 'border-gray-700 shadow-yellow-500/10' : 'border-white'">
          <img src="/img/Pro1.png" alt="แพ็กเกจเริ่มต้น" class="w-full object-cover">
        </div>
        
        <!-- รูปโปรโมชั่นที่ 2 -->
        <div class="rounded-2xl overflow-hidden shadow-2xl border-4 transition-transform hover:scale-[1.02] w-full max-w-2xl" :class="isDarkMode ? 'border-gray-700 shadow-yellow-500/10' : 'border-white'">
          <img src="/img/Pro2.png" alt="แพ็กเกจเสริม" class="w-full object-cover">
        </div>

        <div class="mt-8 text-center w-full">
          <a href="https://line.me/ti/p/~@402iopuh" target="_blank" class="inline-block bg-[#06C755] text-white px-8 py-4 rounded-full font-bold hover:bg-[#05b34c] transition shadow-lg text-lg md:text-xl animate-bounce w-full max-w-md">
            💬 สนใจสมัครแพ็กเกจ แอด Line เลย!
          </a>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { useState } from '#imports'
const isDarkMode = useState('darkMode', () => false)
</script>