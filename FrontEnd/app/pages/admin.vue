<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6 text-purple-700">👑 จัดการผู้ใช้งาน (Admin Only)</h1>
    
    <div class="flex gap-6 items-start">
        <!-- ฟอร์มเพิ่ม / แก้ไข ผู้ใช้งาน -->
        <div class="w-1/3 bg-white p-6 rounded-lg shadow-md border-t-4" :class="isEditing ? 'border-yellow-400' : 'border-purple-600'">
            <h2 class="text-xl font-bold mb-4 text-gray-700 border-b pb-2">
                {{ isEditing ? '✏️ แก้ไขข้อมูลผู้ใช้งาน' : '➕ เพิ่มผู้ใช้งานใหม่' }}
            </h2>
            <form @submit.prevent="submitForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-bold text-gray-700">Username:</label>
                    <input v-model="form.username" type="text" required class="w-full p-2 border rounded focus:outline-purple-500 bg-gray-50">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-700">
                        Password: 
                        <span v-if="isEditing" class="text-xs text-red-500 font-normal">(เว้นว่างไว้ถ้าไม่ต้องการเปลี่ยนรหัส)</span>
                    </label>
                    <input v-model="form.password" type="text" :required="!isEditing" placeholder="ระบุรหัสผ่าน..." class="w-full p-2 border rounded focus:outline-purple-500">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-700">สิทธิ์ผู้ใช้:</label>
                    <select v-model="form.role" class="w-full p-2 border rounded focus:outline-purple-500">
                        <option value="user">User (ลูกค้าทั่วไป)</option>
                        <option value="admin">Admin (ผู้ดูแลระบบ)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-700">โควต้ารูปแบบ (จำกัด):</label>
                    <input v-model="form.max_formats" type="number" min="1" required class="w-full p-2 border rounded focus:outline-purple-500">
                </div>
                <div class="flex gap-2">
                    <div class="flex-1">
                        <label class="block text-sm font-bold text-gray-700">วันที่เริ่ม:</label>
                        <input v-model="form.sub_start_date" type="date" required class="w-full p-2 border rounded focus:outline-purple-500 text-sm">
                    </div>
                    <div class="flex-1">
                        <label class="block text-sm font-bold text-gray-700">หมดอายุ:</label>
                        <input v-model="form.sub_end_date" type="date" required class="w-full p-2 border rounded focus:outline-purple-500 text-sm">
                    </div>
                </div>
                
                <div class="flex gap-2 mt-4 pt-2">
                    <button type="submit" class="flex-1 text-white font-bold py-2 rounded shadow transition" :class="isEditing ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-purple-600 hover:bg-purple-700'">
                        {{ isEditing ? '💾 บันทึกการแก้ไข' : '➕ บันทึกผู้ใช้ใหม่' }}
                    </button>
                    <button v-if="isEditing" @click="cancelEdit" type="button" class="bg-gray-400 text-white font-bold py-2 px-4 rounded hover:bg-gray-500 shadow">ยกเลิก</button>
                </div>
            </form>
        </div>

        <!-- ตารางแสดงรายชื่อ -->
        <div class="w-2/3 bg-white p-6 rounded-lg shadow-md overflow-x-auto">
            <h2 class="text-xl font-bold mb-4 text-gray-700 border-b pb-2">👥 รายชื่อผู้ใช้งานทั้งหมด</h2>
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-100 text-sm text-gray-600 border-b">
                        <th class="p-2">ID</th>
                        <th class="p-2">Username</th>
                        <th class="p-2">Role</th>
                        <th class="p-2">วันที่เริ่ม</th>
                        <th class="p-2">วันหมดอายุ</th>
                        <th class="p-2 text-center">ใช้ไป / โควต้า</th>
                        <th class="p-2 text-center">จัดการ</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="u in users" :key="u.id" class="border-b hover:bg-gray-50 text-sm" :class="{'bg-yellow-50': isEditing && editId === u.id}">
                        <td class="p-2">{{ u.id }}</td>
                        <td class="p-2 font-bold">{{ u.username }}</td>
                        <td class="p-2">
                            <span :class="u.role === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'" class="px-2 py-1 rounded text-xs">
                                {{ u.role }}
                            </span>
                        </td>
                        <td class="p-2 text-gray-500">{{ formatDate(u.sub_start) }}</td>
                        <td class="p-2" :class="isExpired(u.sub_end) ? 'text-red-500 font-bold' : 'text-green-600'">
                            {{ formatDate(u.sub_end) }}
                        </td>
                        <!-- แสดงจำนวนที่ใช้ไป / โควต้าสูงสุด -->
                        <td class="p-2 text-center font-bold">
                            <span :class="u.used_formats >= u.max_formats ? 'text-red-500' : 'text-indigo-600'">
                                {{ u.used_formats }}
                            </span>
                            <span class="text-gray-500"> / {{ u.max_formats }}</span>
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

const router = useRouter()
const users = ref([])

// ตัวแปรสำหรับโหมดแก้ไข
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
    const res = await fetch('http://localhost:8000/users', { headers: { 'Authorization': `Bearer ${token}` } })
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
    
    const url = isEditing.value ? `http://localhost:8000/users/${editId.value}` : 'http://localhost:8000/register';
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
    const res = await fetch(`http://localhost:8000/users/${id}`, {
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