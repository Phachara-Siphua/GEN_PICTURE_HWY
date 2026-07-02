<template>
  <div class="bg-white p-8 rounded-lg shadow-md max-w-2xl mx-auto mt-10">
    <h1 class="text-3xl font-bold mb-6 text-blue-700 border-b pb-4">📦 ข้อมูลแพ็กเกจของคุณ</h1>
    <div v-if="userInfo" class="text-lg space-y-5 text-gray-700">
      <p class="flex items-center">
        <span class="w-10 text-2xl">👤</span> 
        <strong class="w-40">ชื่อผู้ใช้:</strong> {{ userInfo.username }}
      </p>
      <p class="flex items-center">
        <span class="w-10 text-2xl">📅</span> 
        <strong class="w-40">วันที่เริ่มแพ็กเกจ:</strong> 
        <span class="text-green-600 font-bold bg-green-50 px-3 py-1 rounded">{{ formatDate(userInfo.sub_start) }}</span>
      </p>
      <p class="flex items-center">
        <span class="w-10 text-2xl">⏳</span> 
        <strong class="w-40">หมดอายุเมื่อ:</strong> 
        <span class="text-red-500 font-bold bg-red-50 px-3 py-1 rounded">{{ formatDate(userInfo.sub_end) }}</span>
      </p>
      <p class="flex items-center">
        <span class="w-10 text-2xl">💾</span> 
        <strong class="w-40">โควต้ารูปแบบ:</strong> 
        <span class="font-bold text-indigo-600">{{ formatCount }} / {{ userInfo.max_formats }} รูปแบบ</span>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

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
      const res = await fetch('http://localhost:8000/users/me', { headers: { 'Authorization': `Bearer ${token}` } });
      if (res.ok) userInfo.value = await res.json();
      else router.push('/login');

      const resFormat = await fetch('http://localhost:8000/formats', { headers: { 'Authorization': `Bearer ${token}` } });
      if (resFormat.ok) {
          const formats = await resFormat.json();
          formatCount.value = formats.length;
      }
  } catch (error) {
      console.log(error);
  }
})
</script>