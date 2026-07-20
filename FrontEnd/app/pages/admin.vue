<template>
  <div class="transition-colors duration-300 min-h-screen font-prompt relative">
    
    <div v-show="isLoading" class="flex flex-col items-center justify-center h-[80vh]">
        <div class="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-purple-500 mb-6"></div>
        <h2 class="text-2xl font-bold text-purple-500 animate-pulse">กำลังโหลดข้อมูลผู้ใช้งาน...</h2>
    </div>

    <div v-show="!isLoading">
      <h1 class="text-2xl md:text-3xl font-extrabold mb-8 flex items-center gap-3" :class="isDarkMode ? 'text-purple-400' : 'text-purple-700'">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
        จัดการผู้ใช้งาน (Admin Only)
      </h1>
      
      <div class="flex flex-col lg:flex-row gap-8 items-start">
          
          <div class="w-full lg:w-1/3 p-6 md:p-8 rounded-3xl shadow-2xl border-t-4 transition-all backdrop-blur-xl border" :class="[isEditing ? 'border-t-yellow-400' : 'border-t-purple-600', isDarkMode ? 'bg-gray-800/80 border-gray-700/50 shadow-black/30' : 'bg-white/80 border-white/50 shadow-purple-500/10']">
              <h2 class="text-xl font-bold mb-6 border-b pb-3" :class="isDarkMode ? 'border-gray-700 text-gray-200' : 'border-gray-200 text-gray-800'">
                  {{ isEditing ? '✏️ แก้ไขข้อมูลผู้ใช้งาน' : '➕ เพิ่มผู้ใช้งานใหม่' }}
              </h2>
              <form @submit.prevent="submitForm" class="space-y-5">
                  <div>
                      <label class="block text-sm font-bold mb-1.5" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Username:</label>
                      <input v-model="form.username" type="text" required class="w-full p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-colors" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white' : 'bg-gray-50 border-gray-200'">
                  </div>
                  <div>
                      <label class="block text-sm font-bold mb-1.5" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                          Password: 
                          <span v-if="isEditing" class="text-xs text-red-500 font-normal ml-1">(เว้นว่างถ้าไม่เปลี่ยน)</span>
                      </label>
                      <input v-model="form.password" type="text" :required="!isEditing" placeholder="ระบุรหัสผ่าน..." class="w-full p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-colors" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white' : 'bg-gray-50 border-gray-200'">
                  </div>
                  <div>
                      <label class="block text-sm font-bold mb-1.5" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">สิทธิ์ผู้ใช้:</label>
                      <select v-model="form.role" class="w-full p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-colors" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white' : 'bg-gray-50 border-gray-200'">
                          <option value="user">User (ลูกค้าทั่วไป)</option>
                          <option value="admin">Admin (ผู้ดูแลระบบ)</option>
                      </select>
                  </div>
                  <div>
                      <label class="block text-sm font-bold mb-1.5" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">โควต้าเทมเพลต (จำกัด):</label>
                      <input v-model="form.max_formats" type="number" min="1" required class="w-full p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-colors" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white' : 'bg-gray-50 border-gray-200'">
                      
                      <p v-if="isEditing && form.max_formats < userFormats.length" class="text-xs text-red-500 font-bold mt-3 p-3 rounded-lg animate-pulse" :class="isDarkMode ? 'bg-red-900/30' : 'bg-red-50'">
                          ⚠️ คำเตือน: โควต้าใหม่น้อยกว่าเทมเพลตที่ User บันทึกไว้ (มี {{ userFormats.length }} อัน) กรุณาลบออกด้านล่างด้วยครับ!
                      </p>
                  </div>
                  <div class="flex gap-4">
                      <div class="flex-1">
                          <label class="block text-sm font-bold mb-1.5" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">วันที่เริ่ม:</label>
                          <input v-model="form.sub_start_date" type="date" required class="w-full p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm transition-colors" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white' : 'bg-gray-50 border-gray-200'">
                      </div>
                      <div class="flex-1">
                          <label class="block text-sm font-bold mb-1.5" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">หมดอายุ:</label>
                          <input v-model="form.sub_end_date" type="date" required class="w-full p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm transition-colors" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white' : 'bg-gray-50 border-gray-200'">
                      </div>
                  </div>

                  <div v-if="isEditing" class="mt-6 p-4 border rounded-2xl" :class="isDarkMode ? 'bg-red-900/20 border-red-800' : 'bg-red-50/50 border-red-200'">
                      <label class="block text-sm font-bold mb-3" :class="isDarkMode ? 'text-red-400' : 'text-red-600'">🗑️ จัดการเทมเพลตของ User นี้:</label>
                      <div class="flex flex-col xl:flex-row gap-3">
                          <select v-model="selectedFormatToDelete" class="flex-1 p-3 border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors" :class="isDarkMode ? 'bg-gray-800 border-gray-600 text-white' : 'bg-white border-red-200'">
                              <option value="" disabled>-- เลือกเทมเพลต --</option>
                              <option v-for="f in userFormats" :key="f.format_name" :value="f.format_name">{{ f.format_name }}</option>
                          </select>
                          <button type="button" @click="deleteUserFormat" class="bg-gradient-to-r from-red-500 to-rose-600 text-white px-5 py-3 xl:py-1 rounded-xl text-sm font-bold shadow-lg shadow-red-500/20 hover:scale-105 transition-transform">ลบทิ้ง</button>
                      </div>
                      <p v-if="userFormats.length === 0" class="text-xs mt-3 text-center" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">ไม่มีเทมเพลตที่บันทึกไว้</p>
                  </div>
                  
                  <div class="flex gap-3 mt-6 pt-4">
                      <button type="submit" class="flex-1 text-white font-bold py-3.5 rounded-xl shadow-lg transition-transform hover:scale-105 text-sm md:text-base" :class="isEditing ? 'bg-gradient-to-r from-yellow-500 to-orange-500 shadow-yellow-500/30' : 'bg-gradient-to-r from-purple-600 to-indigo-600 shadow-purple-500/30'">
                          {{ isEditing ? '💾 บันทึกการแก้ไขข้อมูล' : '➕ บันทึกผู้ใช้ใหม่' }}
                      </button>
                      <button v-if="isEditing" @click="cancelEdit" type="button" class="bg-gray-200 text-gray-800 font-bold py-3.5 px-6 rounded-xl hover:bg-gray-300 shadow-md transition-colors">ยกเลิก</button>
                  </div>
              </form>
          </div>

          <div class="w-full lg:w-2/3 p-4 md:p-8 rounded-3xl shadow-2xl transition-all backdrop-blur-xl border" :class="isDarkMode ? 'bg-gray-800/80 border-gray-700/50 shadow-black/30' : 'bg-white/80 border-white/50 shadow-purple-500/10'">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 border-b pb-4 gap-4" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                  <h2 class="text-xl font-bold whitespace-nowrap" :class="isDarkMode ? 'text-gray-200' : 'text-gray-800'">👥 รายชื่อในระบบ</h2>
                  <div class="w-full md:w-72 relative">
                      <span class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                      </span>
                      <input v-model="searchQuery" type="text" placeholder="ค้นหาชื่อผู้ใช้..." class="w-full pl-11 p-3 border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 transition-colors shadow-sm" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white' : 'bg-gray-50 border-gray-200'">
                  </div>
              </div>

              <div class="overflow-x-auto rounded-xl border" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                  <table class="w-full text-left border-collapse min-w-[700px]">
                      <thead>
                          <tr class="text-sm border-b" :class="isDarkMode ? 'bg-gray-900/50 text-gray-300 border-gray-700' : 'bg-gray-50 text-gray-600 border-gray-200'">
                              <th class="p-4 text-center w-16 font-bold">ลำดับ</th>
                              <th class="p-4 font-bold">Username</th>
                              <th class="p-4 font-bold">Role</th>
                              <th class="p-4 font-bold">วันที่เริ่ม</th>
                              <th class="p-4 font-bold">วันหมดอายุ</th>
                              <th class="p-4 text-center font-bold">โควต้าเทมเพลต</th>
                              <th class="p-4 text-center font-bold">จัดการ</th>
                          </tr>
                      </thead>
                      <tbody :class="isDarkMode ? 'text-gray-200' : 'text-gray-800'">
                          <tr v-for="(u, index) in filteredUsers" :key="u.id" class="border-b text-sm transition-colors" :class="(isDarkMode ? 'border-gray-700 hover:bg-gray-700/50 ' : 'border-gray-100 hover:bg-indigo-50/30 ') + (isEditing && editId === u.id ? (isDarkMode ? 'bg-yellow-900/30' : 'bg-yellow-50') : '')">
                              
                              <td class="p-4 text-center font-medium text-gray-400">{{ index + 1 }}</td>
                              
                              <td class="p-4 font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{ u.username }}</td>
                              <td class="p-4">
                                  <span :class="(u.role === 'admin' ? 'text-purple-600 border-purple-200 ' : 'text-blue-600 border-blue-200 ') + (isDarkMode ? 'bg-gray-800 border-gray-600' : 'bg-white border')" class="px-3 py-1 rounded-full text-xs font-bold shadow-sm">
                                      {{ u.role }}
                                  </span>
                              </td>
                              <td class="p-4 opacity-80">{{ formatDate(u.sub_start) }}</td>
                              <td class="p-4" :class="isExpired(u.sub_end) ? 'text-red-500 font-bold' : 'text-emerald-600 font-medium'">
                                  {{ formatDate(u.sub_end) }}
                              </td>
                              <td class="p-4 text-center font-bold">
                                  <span :class="u.used_formats > u.max_formats ? 'text-red-500 animate-pulse' : (u.used_formats === u.max_formats ? 'text-orange-500' : 'text-indigo-600')">
                                      {{ u.used_formats }}
                                  </span>
                                  <span class="opacity-50"> / {{ u.max_formats }}</span>
                              </td>
                              <td class="p-4 text-center flex justify-center gap-2">
                                  <button @click="startEditUser(u)" class="bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-4 py-1.5 rounded-lg hover:scale-105 transition-transform text-xs font-bold shadow-md shadow-yellow-500/20">แก้ไข</button>
                                  <button v-if="u.role !== 'admin'" @click="deleteUser(u.id, u.username)" class="bg-gradient-to-r from-red-500 to-rose-600 text-white px-4 py-1.5 rounded-lg hover:scale-105 transition-transform text-xs font-bold shadow-md shadow-red-500/20">ลบ</button>
                              </td>
                          </tr>
                          <!-- Empty State สำหรับตาราง -->
                          <tr v-if="filteredUsers.length === 0">
                              <td colspan="7" class="text-center p-12">
                                  <div class="flex flex-col items-center justify-center opacity-50" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">
                                      <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                                      <span class="text-lg font-bold">ไม่พบผู้ใช้งานที่ค้นหา</span>
                                  </div>
                              </td>
                          </tr>
                      </tbody>
                  </table>
              </div>
          </div>
      </div>
    </div>

    <!-- 🔔 โมดอล (Popup) แจ้งเตือนระบบแบบ Custom. -->
    <transition name="fade">
        <div v-if="sysModal.show" class="fixed inset-0 z-[110] flex items-center justify-center bg-black/50 backdrop-blur-sm px-4" @click.self="closeSysModal">
            <div class="p-8 rounded-3xl shadow-2xl w-full max-w-sm transform scale-100 transition-all text-center border" :class="isDarkMode ? 'bg-gray-800 border-gray-700 shadow-black/50' : 'bg-white border-white'">
                <div class="text-6xl mb-6">{{ sysModal.icon }}</div>
                <h3 class="text-2xl font-bold mb-3" :class="isDarkMode ? 'text-white' : 'text-gray-800'">{{ sysModal.title }}</h3>
                <p class="mb-8 text-base whitespace-pre-line" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">{{ sysModal.message }}</p>
                <div class="flex gap-3 justify-center">
                    <button v-if="sysModal.type === 'confirm'" @click="sysModal.show = false" class="flex-1 bg-gray-200 text-gray-800 px-5 py-3 rounded-xl font-bold hover:bg-gray-300 transition shadow-sm">ยกเลิก</button>
                    <button @click="sysModal.type === 'confirm' ? sysModal.onConfirm() : (sysModal.show = false)" class="flex-1 text-white py-3 rounded-xl font-bold transition-transform hover:scale-105 shadow-lg" :class="sysModal.icon === '❌' || sysModal.icon === '🗑️' ? 'bg-gradient-to-r from-red-500 to-rose-600 shadow-red-500/30' : 'bg-gradient-to-r from-purple-600 to-indigo-600 shadow-purple-500/30'">
                        {{ sysModal.type === 'confirm' ? 'ยืนยัน' : 'ตกลง' }}
                    </button>
                </div>
            </div>
        </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useState } from '#imports'

const isLoading = ref(true)
const isDarkMode = useState('darkMode')
const router = useRouter()
const users = ref([])

const searchQuery = ref('')
const isEditing = ref(false)
const editId = ref(null)

const userFormats = ref([])
const selectedFormatToDelete = ref('')

const sysModal = ref({ show: false, title: '', message: '', type: 'alert', icon: '🔔', onConfirm: null })

const showAlert = (title, message, icon='🔔') => {
    sysModal.value = { show: true, title, message, type: 'alert', icon, onConfirm: null }
}

const showConfirm = (title, message, onConfirmCallback, icon='⚠️') => {
    sysModal.value = { show: true, title, message, type: 'confirm', icon, onConfirm: () => {
        sysModal.value.show = false;
        onConfirmCallback();
    }}
}

const closeSysModal = () => {
    if (sysModal.value.type === 'alert') {
        sysModal.value.show = false;
    }
}

const filteredUsers = computed(() => {
    if (!searchQuery.value) return users.value;
    return users.value.filter(u => u.username.toLowerCase().includes(searchQuery.value.toLowerCase()));
})

const getToday = () => {
    const d = new Date();
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().split('T')[0];
};

const getNextMonth = () => {
    let d = new Date(); d.setDate(d.getDate() + 30);
    return d.toISOString().split('T')[0];
}

const form = ref({
    username: '', password: '', role: 'user', max_formats: 1,
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

const fetchUserFormats = async (userId) => {
    const token = localStorage.getItem('token')
    const res = await fetch(`https://gen-picture-hwy.onrender.com/admin/users/${userId}/formats`, { 
        headers: { 'Authorization': `Bearer ${token}` } 
    })
    if(res.ok) {
        userFormats.value = await res.json()
        selectedFormatToDelete.value = '' 
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
    fetchUserFormats(u.id); 
    window.scrollTo({ top: 0, behavior: 'smooth' }); 
}

const cancelEdit = () => {
    isEditing.value = false;
    editId.value = null;
    userFormats.value = [];
    selectedFormatToDelete.value = '';
    form.value = {
        username: '', password: '', role: 'user', max_formats: 1,
        sub_start_date: getToday(), sub_end_date: getNextMonth()
    };
}

const deleteUserFormat = async () => {
    if (!selectedFormatToDelete.value) return showAlert('แจ้งเตือน', "กรุณาเลือกเทมเพลตที่ต้องการลบใน Combobox ก่อนครับ", 'ℹ️');
    
    showConfirm('ยืนยันการลบ', `⚠️ ยืนยันการลบเทมเพลต '${selectedFormatToDelete.value}' ของ User นี้ทิ้งแบบถาวร?`, async () => {
        const token = localStorage.getItem('token')
        const res = await fetch(`https://gen-picture-hwy.onrender.com/admin/users/${editId.value}/formats/${encodeURIComponent(selectedFormatToDelete.value)}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        })
        
        if(res.ok) {
            showAlert('สำเร็จ', '🗑️ ลบเทมเพลตสำเร็จ!', '✅');
            await fetchUserFormats(editId.value); 
            await fetchUsers(); 
        } else {
            showAlert('ข้อผิดพลาด', 'เกิดข้อผิดพลาดในการลบ', '❌');
        }
    }, '🗑️');
}

const executeSubmitForm = async () => {
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
        showAlert('สำเร็จ', data.message, '✅')
        cancelEdit() 
        fetchUsers() 
    } else {
        showAlert('ข้อผิดพลาด', '❌ ' + data.detail, '❌')
    }
}

const submitForm = async () => {
    if (isEditing.value && form.value.max_formats < userFormats.value.length) {
        showConfirm('⚠️ โควต้าขัดแย้งกัน', `คุณกำลังจะลดโควต้าลงเหลือ ${form.value.max_formats} แต่ User นี้มีเทมเพลตบันทึกไว้ถึง ${userFormats.value.length} อัน\n\nระบบแนะนำให้ "ยกเลิก" และกลับไปลบเทมเพลตของ User ออกก่อนเพื่อไม่ให้โควต้าแสดงผลเกิน\n\nคุณแน่ใจหรือไม่ที่จะฝืนบันทึกข้อมูลโดยไม่ลบเทมเพลตก่อน?`, () => {
            executeSubmitForm();
        }, '🚨');
        return;
    }
    executeSubmitForm();
}

const deleteUser = async (id, name) => {
    showConfirm('ลบผู้ใช้งาน', `⚠️ ต้องการลบผู้ใช้ '${name}' ทิ้งถาวรหรือไม่?`, async () => {
        const token = localStorage.getItem('token')
        const res = await fetch(`https://gen-picture-hwy.onrender.com/users/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        })
        if(res.ok) { 
            showAlert('สำเร็จ', 'ลบผู้ใช้สำเร็จ!', '✅'); 
            fetchUsers() 
        }
    }, '🗑️');
}

const formatDate = (dateStr) => {
    if(!dateStr) return '-';
    const d = new Date(dateStr);
    return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth()+1).toString().padStart(2, '0')}/${d.getFullYear()}`;
}

const isExpired = (dateStr) => new Date(dateStr) < new Date()
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>