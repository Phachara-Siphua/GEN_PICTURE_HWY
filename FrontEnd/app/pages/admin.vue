<template>
  <div class="transition-colors duration-300 min-h-screen">
    
    <!-- หน้าจอหมุนโหลด -->
    <div v-show="isLoading" class="flex flex-col items-center justify-center h-[80vh]">
        <div class="animate-spin rounded-full h-24 w-24 border-t-4 border-b-4 border-blue-500 mb-6"></div>
        <h2 class="text-2xl font-bold text-blue-500 animate-pulse">กำลังโหลดข้อมูลผู้ใช้งาน...</h2>
    </div>

    <div v-show="!isLoading">
      <h1 class="text-3xl font-bold mb-6" :class="isDarkMode ? 'text-purple-400' : 'text-purple-700'">👑 จัดการผู้ใช้งาน (Admin Only)</h1>
      
      <div class="flex gap-6 items-start">
          <div class="w-1/3 p-6 rounded-lg shadow-md border-t-4 transition-colors" :class="isEditing ? 'border-yellow-400' : 'border-purple-600', isDarkMode ? 'bg-gray-800' : 'bg-white'">
              <h2 class="text-xl font-bold mb-4 border-b pb-2" :class="isDarkMode ? 'text-gray-200 border-gray-700' : 'text-gray-700 border-gray-200'">
                  {{ isEditing ? '✏️ แก้ไขข้อมูลผู้ใช้งาน' : '➕ เพิ่มผู้ใช้งานใหม่' }}
              </h2>
              <form @submit.prevent="submitForm" class="space-y-4">
                  <div>
                      <label class="block text-sm font-bold" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Username:</label>
                      <input v-model="form.username" type="text" required class="w-full p-2 border rounded focus:outline-purple-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'">
                  </div>
                  <div>
                      <label class="block text-sm font-bold" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                          Password: 
                          <span v-if="isEditing" class="text-xs text-red-500 font-normal">(เว้นว่างไว้ถ้าไม่ต้องการเปลี่ยนรหัส)</span>
                      </label>
                      <input v-model="form.password" type="text" :required="!isEditing" placeholder="ระบุรหัสผ่าน..." class="w-full p-2 border rounded focus:outline-purple-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'">
                  </div>
                  <div>
                      <label class="block text-sm font-bold" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">สิทธิ์ผู้ใช้:</label>
                      <select v-model="form.role" class="w-full p-2 border rounded focus:outline-purple-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'">
                          <option value="user">User (ลูกค้าทั่วไป)</option>
                          <option value="admin">Admin (ผู้ดูแลระบบ)</option>
                      </select>
                  </div>
                  <div>
                      <label class="block text-sm font-bold" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">โควต้ารูปแบบ (จำกัด):</label>
                      <input v-model="form.max_formats" type="number" min="1" required class="w-full p-2 border rounded focus:outline-purple-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'">
                  </div>
                  <div class="flex gap-2">
                      <div class="flex-1">
                          <label class="block text-sm font-bold" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">วันที่เริ่ม:</label>
                          <input v-model="form.sub_start_date" type="date" required class="w-full p-2 border rounded focus:outline-purple-500 text-sm" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'">
                      </div>
                      <div class="flex-1">
                          <label class="block text-sm font-bold" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">หมดอายุ:</label>
                          <input v-model="form.sub_end_date" type="date" required class="w-full p-2 border rounded focus:outline-purple-500 text-sm" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300'">
                      </div>
                  </div>

                  <!-- 🎯 ส่วนใหม่ที่เพิ่มเข้ามาตามไอเดีย: ลบรูปแบบตอนเกินโควต้า -->
                  <div v-if="isEditing" class="mt-4 p-3 border rounded-lg" :class="isDarkMode ? 'bg-red-900/20 border-red-800' : 'bg-red-50 border-red-200'">
                      <label class="block text-sm font-bold mb-2" :class="isDarkMode ? 'text-red-400' : 'text-red-700'">🗑️ จัดการรูปแบบของ User นี้ (กรณีลบโควต้า):</label>
                      <div class="flex gap-2">
                          <select v-model="selectedFormatToDelete" class="flex-1 p-2 border rounded text-sm focus:outline-red-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-red-300'">
                              <option value="" disabled>-- เลือกรูปแบบที่ต้องการลบ --</option>
                              <option v-for="f in userFormats" :key="f.format_name" :value="f.format_name">{{ f.format_name }}</option>
                          </select>
                          <button type="button" @click="deleteUserFormat" class="bg-red-500 text-white px-3 py-1 rounded text-sm font-bold hover:bg-red-600 shadow">ลบทิ้ง</button>
                      </div>
                      <p v-if="userFormats.length === 0" class="text-xs mt-1" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">ผู้ใช้นี้ยังไม่มีรูปแบบที่บันทึกไว้</p>
                  </div>
                  
                  <div class="flex gap-2 mt-4 pt-2">
                      <button type="submit" class="flex-1 text-white font-bold py-2 rounded shadow transition" :class="isEditing ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-purple-600 hover:bg-purple-700'">
                          {{ isEditing ? '💾 บันทึกการแก้ไขข้อมูล' : '➕ บันทึกผู้ใช้ใหม่' }}
                      </button>
                      <button v-if="isEditing" @click="cancelEdit" type="button" class="bg-gray-500 text-white font-bold py-2 px-4 rounded hover:bg-gray-600 shadow">ยกเลิก</button>
                  </div>
              </form>
          </div>

          <div class="w-2/3 p-6 rounded-lg shadow-md overflow-x-auto transition-colors" :class="isDarkMode ? 'bg-gray-800' : 'bg-white'">
              <h2 class="text-xl font-bold mb-4 border-b pb-2" :class="isDarkMode ? 'text-gray-200 border-gray-700' : 'text-gray-700 border-gray-200'">👥 รายชื่อผู้ใช้งานทั้งหมด</h2>
              <table class="w-full text-left border-collapse">
                  <thead>
                      <tr class="text-sm border-b" :class="isDarkMode ? 'bg-gray-700 text-gray-300 border-gray-600' : 'bg-gray-100 text-gray-600 border-gray-200'">
                          <th class="p-2">ID</th>
                          <th class="p-2">Username</th>
                          <th class="p-2">Role</th>
                          <th class="p-2">วันที่เริ่ม</th>
                          <th class="p-2">วันหมดอายุ</th>
                          <th class="p-2 text-center">ใช้ไป / โควต้า</th>
                          <th class="p-2 text-center">จัดการ</th>
                      </tr>
                  </thead>
                  <tbody :class="isDarkMode ? 'text-gray-200' : 'text-gray-800'">
                      <tr v-for="u in users" :key="u.id" class="border-b text-sm transition-colors" :class="[isDarkMode ? 'border-gray-700 hover:bg-gray-700' : 'border-gray-200 hover:bg-gray-50', {'bg-yellow-100 dark:bg-yellow-900/40': isEditing && editId === u.id}]">
                          <td class="p-2">{{ u.id }}</td>
                          <td class="p-2 font-bold">{{ u.username }}</td>
                          <td class="p-2">
                              <span :class="[u.role === 'admin' ? 'text-purple-600' : 'text-blue-600', isDarkMode ? 'bg-gray-900' : 'bg-gray-100']" class="px-2 py-1 rounded text-xs font-bold">
                                  {{ u.role }}
                              </span>
                          </td>
                          <td class="p-2 opacity-70">{{ formatDate(u.sub_start) }}</td>
                          <td class="p-2" :class="isExpired(u.sub_end) ? 'text-red-500 font-bold' : 'text-green-500'">
                              {{ formatDate(u.sub_end) }}
                          </td>
                          <td class="p-2 text-center font-bold">
                              <span :class="u.used_formats > u.max_formats ? 'text-red-500 animate-pulse' : (u.used_formats === u.max_formats ? 'text-orange-500' : 'text-indigo-500')">
                                  {{ u.used_formats }}
                              </span>
                              <span class="opacity-60"> / {{ u.max_formats }}</span>
                          </td>
                          <td class="p-2 text-center flex justify-center gap-1">
                              <button @click="startEditUser(u)" class="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600 text-xs shadow-sm">แก้ไข</button>
                              <button v-if="u.role !== 'admin'" @click="deleteUser(u.id, u.username)" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-xs shadow-sm">ลบ</button>
                          </td>
                      </tr>
                  </tbody>
              </table>
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
const router = useRouter()
const users = ref([])

const isEditing = ref(false)
const editId = ref(null)

// ตัวแปรสำหรับฟีเจอร์จัดการรูปแบบ
const userFormats = ref([])
const selectedFormatToDelete = ref('')

const getToday = () => new Date().toISOString().split('T')[0]
const getNextMonth = () => {
    let d = new Date(); d.setDate(d.getDate() + 30);
    return d.toISOString().split('T')[0];
}

const form = ref({
    username: '', password: '', role: 'user', max_formats: 2,
    sub_start_date: getToday(), sub_end_date: getNextMonth()
})

const fetchUsers = async () => {
    const token = localStorage.getItem('token')
    const res = await fetch('https://gen-picture-hwy.onrender.com/users', { headers: { 'Authorization': `Bearer ${token}` } })
    if(res.ok) users.value = await res.json()
    else router.push('/') 
    isLoading.value = false;
}

onMounted(() => { fetchUsers() })

// โหลดรายการรูปแบบของ User คนที่กำลังโดนแก้ไข
const fetchUserFormats = async (userId) => {
    const token = localStorage.getItem('token')
    const res = await fetch(`https://gen-picture-hwy.onrender.com/admin/users/${userId}/formats`, { 
        headers: { 'Authorization': `Bearer ${token}` } 
    })
    if(res.ok) {
        userFormats.value = await res.json()
        selectedFormatToDelete.value = '' // รีเซ็ตค่า combobox
    }
}

const startEditUser = (u) => {
    isEditing.value = true;
    editId.value = u.id;
    form.value = {
        username: u.username,
        password: '', 
        role: u.role,
        max_formats: u.max_formats,
        sub_start_date: u.sub_start.split('T')[0], 
        sub_end_date: u.sub_end.split('T')[0]
    };
    fetchUserFormats(u.id); // ดึงข้อมูลรูปแบบมาใส่ Combobox
    window.scrollTo(0, 0); 
}

const cancelEdit = () => {
    isEditing.value = false;
    editId.value = null;
    userFormats.value = [];
    selectedFormatToDelete.value = '';
    form.value = {
        username: '', password: '', role: 'user', max_formats: 2,
        sub_start_date: getToday(), sub_end_date: getNextMonth()
    };
}

// ฟังก์ชันสำหรับกดลบรูปแบบของ User ในหน้า Admin
const deleteUserFormat = async () => {
    if (!selectedFormatToDelete.value) return alert("กรุณาเลือกรูปแบบที่ต้องการลบใน Combobox ก่อนครับ");
    if (!confirm(`⚠️ ยืนยันการลบรูปแบบ '${selectedFormatToDelete.value}' ของ User นี้ทิ้งแบบถาวร?`)) return;

    const token = localStorage.getItem('token')
    const res = await fetch(`https://gen-picture-hwy.onrender.com/admin/users/${editId.value}/formats/${encodeURIComponent(selectedFormatToDelete.value)}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if(res.ok) {
        alert('🗑️ ลบรูปแบบสำเร็จ!');
        await fetchUserFormats(editId.value); // อัปเดตรายการใน Combobox ใหม่
        await fetchUsers(); // ดึงข้อมูลตารางใหม่ เพื่อให้ช่อง "ใช้ไป / โควต้า" ลดลงแบบเรียลไทม์
    } else {
        alert('เกิดข้อผิดพลาดในการลบ');
    }
}

const submitForm = async () => {
    const token = localStorage.getItem('token')
    
    const url = isEditing.value ? `https://gen-picture-hwy.onrender.com/users/${editId.value}` : 'https://gen-picture-hwy.onrender.com/register';
    const method = isEditing.value ? 'PUT' : 'POST';

    const payload = { ...form.value };
    if (isEditing.value && !payload.password) {
        delete payload.password; 
    }

    const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(payload)
    })
    
    const data = await res.json()
    if(res.ok) {
        alert(data.message)
        cancelEdit() 
        fetchUsers() 
    } else {
        alert('❌ ' + data.detail)
    }
}

const deleteUser = async (id, name) => {
    if(!confirm(`⚠️ ต้องการลบผู้ใช้ '${name}' ทิ้งถาวรหรือไม่?`)) return
    const token = localStorage.getItem('token')
    const res = await fetch(`https://gen-picture-hwy.onrender.com/users/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    })
    if(res.ok) { alert('ลบสำเร็จ!'); fetchUsers() }
}

const formatDate = (dateStr) => {
    if(!dateStr) return '-';
    const d = new Date(dateStr);
    return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth()+1).toString().padStart(2, '0')}/${d.getFullYear()}`;
}

const isExpired = (dateStr) => new Date(dateStr) < new Date()
</script>