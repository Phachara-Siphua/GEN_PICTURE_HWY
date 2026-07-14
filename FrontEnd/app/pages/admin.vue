<template>
  <div class="transition-colors duration-300">
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
                
                <div class="flex gap-2 mt-4 pt-2">
                    <button type="submit" class="flex-1 text-white font-bold py-2 rounded shadow transition" :class="isEditing ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-purple-600 hover:bg-purple-700'">
                        {{ isEditing ? '💾 บันทึกการแก้ไข' : '➕ บันทึกผู้ใช้ใหม่' }}
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
                            <span :class="u.used_formats >= u.max_formats ? 'text-red-500' : 'text-indigo-500'">
                                {{ u.used_formats }}
                            </span>
                            <span class="opacity-60"> / {{ u.max_formats }}</span>
                        </td>
                        <td class="p-2 text-center flex justify-center gap-1">
                            <button @click="startEditUser(u)" class="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600 text-xs">แก้ไข</button>
                            <button v-if="u.role !== 'admin'" @click="deleteUser(u.id, u.username)" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-xs">ลบ</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useState } from '#imports'

const isDarkMode = useState('darkMode')
const router = useRouter()
const users = ref([])

const isEditing = ref(false)
const editId = ref(null)

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
}

onMounted(() => { fetchUsers() })

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
    window.scrollTo(0, 0); 
}

const cancelEdit = () => {
    isEditing.value = false;
    editId.value = null;
    form.value = {
        username: '', password: '', role: 'user', max_formats: 2,
        sub_start_date: getToday(), sub_end_date: getNextMonth()
    };
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