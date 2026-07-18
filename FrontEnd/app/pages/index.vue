<template>
  <div class="transition-colors duration-300 min-h-screen relative font-prompt">
    
    <!-- หน้าจอหมุนโหลด -->
    <div v-show="isLoading" class="flex flex-col items-center justify-center h-[80vh]">
        <div class="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-indigo-500 mb-6"></div>
        <h2 class="text-2xl font-bold text-indigo-500 animate-pulse">กำลังเตรียมระบบ...</h2>
    </div>

    <!-- แจ้งเตือนหมดอายุ -->
    <div v-show="!isLoading && isExpired" class="flex flex-col items-center justify-center h-[80vh] px-4">
        <div class="p-8 md:p-12 rounded-3xl shadow-2xl text-center w-full max-w-lg border-t-4 border-red-500 transition-colors backdrop-blur-xl" :class="isDarkMode ? 'bg-gray-800/90 text-white shadow-black/50' : 'bg-white/90 text-gray-800 shadow-xl'">
            <svg class="w-20 h-20 text-red-500 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            <h2 class="text-2xl md:text-3xl font-extrabold text-red-500 mb-3">แพ็กเกจหมดอายุแล้ว</h2>
            <p class="mb-6 text-base md:text-lg">บัญชีของคุณหมดอายุเมื่อเวลา<br><strong class="text-xl md:text-2xl text-red-400 block mt-2">{{ expireDateStr }}</strong></p>
            <a href="https://line.me/ti/p/~@402iopuh" target="_blank" class="inline-flex items-center gap-2 justify-center bg-gradient-to-r from-[#06C755] to-[#05b34c] text-white px-8 py-3.5 rounded-full font-bold hover:scale-105 transition-transform shadow-lg shadow-[#06C755]/30 text-lg w-full">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
                ติดต่อแอดมิน (Line@)
            </a>
        </div>
    </div>

    <!-- แอปพลิเคชันหลัก -->
    <div v-show="!isLoading && !isExpired" id="mainApp" class="flex flex-col xl:flex-row gap-6 w-full max-w-[1200px] mx-auto mt-2 relative">
        
        <!-- ฝั่งซ้าย: พรีวิว -->
        <div class="canvas-container flex-1 flex flex-col items-center p-5 md:p-8 rounded-3xl shadow-xl w-full transition-all backdrop-blur-xl border" :class="isDarkMode ? 'bg-gray-800/80 border-gray-700/50 shadow-black/20' : 'bg-white/80 border-white/50 shadow-indigo-500/5'">
            <h3 class="text-xl font-bold mb-6 flex items-center gap-2" :class="isDarkMode ? 'text-gray-100' : 'text-gray-800'">
                <svg class="w-6 h-6 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                ภาพพรีวิวจำลอง
            </h3>
            
            <canvas id="myCanvas" width="600" height="600" class="w-full max-w-[450px] h-auto border-4 shadow-2xl rounded-2xl transition-transform hover:scale-[1.01]" :class="isDarkMode ? 'border-gray-700' : 'border-white'"></canvas>
            
            <button class="mt-8 bg-gradient-to-r from-teal-400 to-emerald-500 text-white py-3.5 px-6 rounded-xl font-bold shadow-lg shadow-teal-500/30 hover:scale-[1.02] transition-transform w-full max-w-[450px] text-lg flex justify-center items-center gap-2" @click="generatePreviewNumbers">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                สุ่มตัวเลขใหม่ (ทดสอบตัวอย่าง)
            </button>

            <div class="flex justify-between items-center mt-12 mb-4 border-b-2 w-full pb-3" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                <h3 class="text-lg font-bold m-0 flex items-center gap-2" :class="isDarkMode ? 'text-gray-200' : 'text-gray-800'">
                    <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                    รูปภาพที่พร้อมสร้าง
                </h3>
                <button @click="clearAllPreviews" class="bg-gradient-to-r from-red-500 to-rose-600 text-white px-4 py-2 rounded-lg text-sm font-bold shadow-md shadow-red-500/20 hover:scale-105 transition-transform flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    ลบทั้งหมด
                </button>
            </div>
            
            <div id="previewZone" class="flex flex-wrap gap-4 p-4 md:p-6 border-2 border-dashed rounded-2xl w-full justify-center min-h-[220px] transition-all items-center" :class="isDarkMode ? 'border-gray-600 bg-gray-900/30' : 'border-indigo-200 bg-indigo-50/50'">
                <!-- Empty State สวยๆ -->
                <div class="text-center flex flex-col items-center justify-center opacity-60 hover:opacity-100 transition-opacity w-full py-8">
                    <svg class="w-16 h-16 mb-4" :class="isDarkMode ? 'text-gray-500' : 'text-indigo-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                    <span class="font-bold text-lg" :class="isDarkMode ? 'text-gray-400' : 'text-indigo-500'">พื้นที่พรีวิวรูปภาพ</span>
                    <span class="text-sm mt-1" :class="isDarkMode ? 'text-gray-500' : 'text-indigo-400'">เมื่อกดปุ่ม "สร้างรูปทั้งหมด" รูปจะมาแสดงที่นี่ครับ</span>
                </div>
            </div>
        </div>

        <!-- ฝั่งขวา: แผงควบคุม (🎯 ดักจับ @change และ @input เป็น handleUpdate แล้ว) -->
        <div class="controls-container w-full xl:w-[420px] p-4 md:p-6 rounded-3xl shadow-xl xl:max-h-[85vh] xl:overflow-y-auto flex flex-col gap-4 transition-all backdrop-blur-xl border relative" :class="isDarkMode ? 'bg-gray-800/80 border-gray-700/50 shadow-black/20' : 'bg-white/80 border-white/50 shadow-indigo-500/5'" @change="handleUpdate" @input="handleUpdate">
            <h3 class="text-xl font-bold m-0 text-indigo-600 py-3 border-b mb-1 flex items-center gap-2" :class="isDarkMode ? 'border-gray-700 text-indigo-400' : 'border-gray-200'">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path></svg>
                แผงควบคุม
            </h3>
            
            <div class="p-5 rounded-2xl border shadow-sm mb-2 transition-colors" :class="isDarkMode ? 'bg-gray-900/50 border-gray-700' : 'bg-indigo-50/50 border-indigo-100'">
                <label class="block text-sm font-bold mb-3 flex items-center gap-2" :class="isDarkMode ? 'text-indigo-300' : 'text-indigo-800'">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
                    จัดการเทมเพลตที่บันทึกไว้:
                </label>
                <div class="flex flex-col sm:flex-row gap-2 mb-4">
                    <select id="formatSelect" class="flex-1 p-2.5 border rounded-xl text-sm font-bold focus:outline-indigo-500 transition-colors" :class="isDarkMode ? 'bg-gray-800 border-gray-600 text-white' : 'bg-white border-indigo-200'">
                        <option value="NEW">➕ สร้างเทมเพลตใหม่</option>
                    </select>
                    <div class="flex gap-2">
                        <button @click="loadSelectedFormat" class="flex-1 bg-gradient-to-r from-indigo-500 to-blue-600 text-white px-5 py-2.5 sm:py-1 rounded-xl text-sm font-bold shadow-md shadow-indigo-500/20 hover:scale-105 transition-transform">โหลด</button>
                        <button @click="deleteSelectedFormat" class="flex-1 bg-gradient-to-r from-red-500 to-rose-500 text-white px-5 py-2.5 sm:py-1 rounded-xl text-sm font-bold shadow-md shadow-red-500/20 hover:scale-105 transition-transform">ลบ</button>
                    </div>
                </div>
                
                <div class="flex flex-col sm:flex-row gap-2">
                    <button @click="triggerSaveFormat" class="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 text-white py-3 sm:py-2.5 rounded-xl font-bold hover:scale-[1.02] transition-transform shadow-md shadow-green-500/20 text-sm flex justify-center items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
                        บันทึกเทมเพลตนี้
                    </button>
                    <button @click="resetFormat" class="bg-gray-500 text-white px-5 py-3 sm:py-2.5 rounded-xl font-bold hover:bg-gray-600 hover:scale-[1.02] transition-transform shadow-md text-sm flex justify-center items-center gap-2" title="เคลียร์ค่าทุกอย่างกลับเป็นค่าเริ่มต้น">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                        รีเซ็ต
                    </button>
                </div>
            </div>

            <!-- หมวดหมู่แบบมี Transition Slide -->
            <div class="flex flex-col gap-3">
                
                <!-- 1. รูปภาพ -->
                <div class="border rounded-2xl overflow-hidden transition-colors shadow-sm" :class="isDarkMode ? 'border-gray-700 bg-gray-800/50' : 'border-gray-200 bg-white'">
                    <div @click="openSection = 1" class="p-4 cursor-pointer flex justify-between items-center font-bold transition-all" :class="openSection === 1 ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white' : (isDarkMode ? 'text-gray-200 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-50')">
                        <span class="flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                            1. รูปภาพ (Background & Logo)
                        </span>
                        <svg class="w-5 h-5 transform transition-transform" :class="openSection === 1 ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </div>
                    <transition name="slide-fade">
                        <div v-show="openSection === 1" class="p-5 space-y-4 text-sm">
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b pb-4" :class="isDarkMode ? 'border-gray-700' : 'border-gray-100'">
                                <label class="flex items-center gap-2 font-bold cursor-pointer text-emerald-500"><input type="checkbox" id="showBg" checked class="w-4 h-4 rounded text-emerald-500 focus:ring-emerald-500"> เปิดใช้ Background</label>
                                <label class="flex items-center gap-2 font-bold cursor-pointer text-blue-500"><input type="checkbox" id="showLogo" class="w-4 h-4 rounded text-blue-500 focus:ring-blue-500"> เปิดใช้ Logo</label>
                            </div>
                            <div>
                                <label class="block font-bold mt-2">อัปโหลด Background:</label>
                                <input type="file" id="bgUpload" accept="image/*" class="w-full mt-2 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-bold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer">
                            </div>
                            <div>
                                <label class="block font-bold mt-2">อัปโหลด Logo:</label>
                                <input type="file" id="logoUpload" accept="image/*" class="w-full mt-2 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-bold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer">
                            </div>
                            
                            <!-- 🎯 ปุ่มจัดกึ่งกลางแบบ 3D Button -->
                            <div class="text-center mt-5">
                                <button class="w-full bg-indigo-500 hover:bg-indigo-400 text-white font-bold py-3 rounded-xl border-b-4 border-indigo-700 active:border-b-0 active:translate-y-1 transition-all shadow-md flex items-center justify-center gap-2" @click="centerElement('logo')">
                                    <svg class="w-5 h-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6c0 4.418 6 10 6 10s6-5.582 6-10a6 6 0 00-6-6zm0 8a2 2 0 110-4 2 2 0 010 4z"/></svg>
                                    จัด Logo ให้อยู่กึ่งกลาง
                                </button>
                            </div>

                            <div class="p-4 border rounded-xl mt-4" :class="isDarkMode ? 'border-gray-700 bg-gray-900/50' : 'border-gray-100 bg-gray-50'">
                                <label class="block font-bold">ตำแหน่ง Logo X (แนวนอน):</label><input type="range" id="logoX" min="0" max="600" value="480" class="w-full mt-2 accent-indigo-500">
                                <label class="block font-bold mt-3">ตำแหน่ง Logo Y (แนวตั้ง):</label><input type="range" id="logoY" min="0" max="600" value="90" class="w-full mt-2 accent-indigo-500">
                                <label class="block font-bold mt-3 text-indigo-500">ขนาด Logo: <span id="logoScaleVal">37</span>%</label><input type="range" id="logoScale" min="10" max="300" value="37" class="w-full mt-2 accent-indigo-500">
                            </div>
                        </div>
                    </transition>
                </div>

                <!-- 2. หัวข้อ -->
                <div class="border rounded-2xl overflow-hidden transition-colors shadow-sm" :class="isDarkMode ? 'border-gray-700 bg-gray-800/50' : 'border-gray-200 bg-white'">
                    <div @click="openSection = 2" class="p-4 cursor-pointer flex justify-between items-center font-bold transition-all" :class="openSection === 2 ? 'bg-gradient-to-r from-purple-500 to-fuchsia-600 text-white' : (isDarkMode ? 'text-gray-200 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-50')">
                        <span class="flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                            2. รายชื่อหัวข้อ & ฟอนต์
                        </span>
                        <svg class="w-5 h-5 transform transition-transform" :class="openSection === 2 ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </div>
                    <transition name="slide-fade">
                        <div v-show="openSection === 2" class="p-5 space-y-4 text-sm">
                            <div id="lotterySelector" class="border rounded-xl p-3 max-h-[250px] overflow-y-auto mt-1 custom-scrollbar" :class="isDarkMode ? 'border-gray-700 bg-gray-900/50' : 'border-gray-200 bg-gray-50'"></div>
                            
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mt-4">
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">เลือกฟอนต์:</label>
                                    <!-- 🎯 จับเหตุการณ์ @change ยิงตรงไปหา handleUpdate -->
                                    <select id="headerFontFamily" @change="handleUpdate" class="w-full p-2.5 border rounded-xl mt-1 focus:ring-purple-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'">
                                        <option value="Prompt">Prompt</option><option value="Kanit">Kanit</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option><option value="Arial">Arial</option><option value="Tahoma">Tahoma</option>
                                    </select>
                                </div>
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">สไตล์:</label>
                                    <div class="flex gap-4 mt-3">
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="headerFontBold" class="mr-2 w-4 h-4 text-purple-600 rounded"> หนา</label>
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="headerFontItalic" class="mr-2 w-4 h-4 text-purple-600 rounded"> เอียง</label>
                                    </div>
                                </div>
                            </div>

                            <div class="grid grid-cols-2 gap-4 mt-3">
                                <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="headerFontSize" value="50" min="10" class="w-full p-2 border rounded-xl mt-1 focus:ring-purple-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold">สีตัวอักษร:</label><input type="color" id="headerColor" value="#000000" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">ความหนาขอบ:</label><input type="number" id="headerStrokeWidth" value="0" min="0" class="w-full p-2 border rounded-xl mt-1 focus:ring-purple-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="headerStrokeColor" value="#FFFFFF" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                            </div>
                            
                            <!-- 🎯 ปุ่มจัดกึ่งกลางแบบ 3D Button -->
                            <div class="text-center mt-5">
                                <button class="w-full bg-purple-500 hover:bg-purple-400 text-white font-bold py-3 rounded-xl border-b-4 border-purple-700 active:border-b-0 active:translate-y-1 transition-all shadow-md flex items-center justify-center gap-2" @click="centerElement('header')">
                                    <svg class="w-5 h-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6c0 4.418 6 10 6 10s6-5.582 6-10a6 6 0 00-6-6zm0 8a2 2 0 110-4 2 2 0 010 4z"/></svg>
                                    จัดหัวข้อกึ่งกลาง
                                </button>
                            </div>
                            <label class="block font-bold mt-3">ตำแหน่ง X:</label><input type="range" id="headerX" min="0" max="600" value="300" class="w-full mt-2 accent-purple-500">
                            <label class="block font-bold mt-3">ตำแหน่ง Y:</label><input type="range" id="headerY" min="0" max="600" value="100" class="w-full mt-2 accent-purple-500">
                        </div>
                    </transition>
                </div>

                <!-- 3. เลข 1 ตัว (เลขรูด) -->
                <div class="border rounded-2xl overflow-hidden transition-colors shadow-sm" :class="isDarkMode ? 'border-gray-700 bg-gray-800/50' : 'border-gray-200 bg-white'">
                    <div @click="openSection = 3" class="p-4 cursor-pointer flex justify-between items-center font-bold transition-all" :class="openSection === 3 ? 'bg-gradient-to-r from-red-500 to-rose-600 text-white' : (isDarkMode ? 'text-gray-200 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-50')">
                        <span class="flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                            3. เลข 1 ตัว (เลขรูด)
                        </span>
                        <svg class="w-5 h-5 transform transition-transform" :class="openSection === 3 ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </div>
                    <transition name="slide-fade">
                        <div v-show="openSection === 3" class="p-5 space-y-4 text-sm">
                            <div class="flex justify-between gap-4">
                                <div class="flex-1"><label class="block font-bold">จำนวนแถว:</label><input type="number" id="row1Count" value="1" min="0" class="w-full p-2 border rounded-xl mt-1 focus:ring-rose-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div class="flex-1"><label class="block font-bold">จำนวนคอลัมน์:</label><input type="number" id="col1Count" value="2" min="1" class="w-full p-2 border rounded-xl mt-1 focus:ring-rose-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                            </div>
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mt-2">
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">เลือกฟอนต์:</label>
                                    <select id="num1FontFamily" @change="handleUpdate" class="w-full p-2.5 border rounded-xl mt-1 focus:ring-rose-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'">
                                        <option value="Prompt">Prompt</option><option value="Kanit">Kanit</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option><option value="Arial">Arial</option><option value="Tahoma">Tahoma</option>
                                    </select>
                                </div>
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">สไตล์:</label>
                                    <div class="flex gap-4 mt-3">
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="num1FontBold" class="mr-2 w-4 h-4 text-rose-500 rounded"> หนา</label>
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="num1FontItalic" class="mr-2 w-4 h-4 text-rose-500 rounded"> เอียง</label>
                                    </div>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-4 mt-2">
                                <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="num1FontSize" value="50" min="10" class="w-full p-2 border rounded-xl mt-1 focus:ring-rose-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold">สีอักษร:</label><input type="color" id="num1Color" value="#FFD700" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">ขอบหนา:</label><input type="number" id="num1StrokeWidth" value="3" min="0" class="w-full p-2 border rounded-xl mt-1 focus:ring-rose-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="num1StrokeColor" value="#000000" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                            </div>
                            <div class="flex flex-col sm:flex-row justify-between gap-4 mt-4 p-4 border rounded-xl" :class="isDarkMode ? 'border-gray-700 bg-gray-900/50' : 'border-gray-100 bg-gray-50'">
                                <div class="flex-1"><label class="block font-bold text-rose-500">ช่องไฟ ↔ (X):</label><input type="range" id="num1GapX" min="30" max="300" value="80" class="w-full mt-2 accent-rose-500"></div>
                                <div class="flex-1"><label class="block font-bold text-emerald-500">ช่องไฟ ↕ (Y):</label><input type="range" id="num1GapY" min="30" max="200" value="70" class="w-full mt-2 accent-emerald-500"></div>
                            </div>
                            <!-- 🎯 ปุ่มจัดกึ่งกลางแบบ 3D Button -->
                            <div class="text-center mt-5">
                                <button class="w-full bg-rose-500 hover:bg-rose-400 text-white font-bold py-3 rounded-xl border-b-4 border-rose-700 active:border-b-0 active:translate-y-1 transition-all shadow-md flex items-center justify-center gap-2" @click="centerElement('num1')">
                                    <svg class="w-5 h-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6c0 4.418 6 10 6 10s6-5.582 6-10a6 6 0 00-6-6zm0 8a2 2 0 110-4 2 2 0 010 4z"/></svg>
                                    จัดกลุ่มกึ่งกลาง
                                </button>
                            </div>
                            <label class="block font-bold mt-3">ตำแหน่งเริ่ม X:</label><input type="range" id="num1X" min="0" max="600" value="260" class="w-full mt-2 accent-rose-500">
                            <label class="block font-bold mt-3">ตำแหน่งเริ่ม Y:</label><input type="range" id="num1Y" min="0" max="600" value="180" class="w-full mt-2 accent-rose-500">
                        </div>
                    </transition>
                </div>

                <!-- 4. เลข 2 ตัว -->
                <div class="border rounded-2xl overflow-hidden transition-colors shadow-sm" :class="isDarkMode ? 'border-gray-700 bg-gray-800/50' : 'border-gray-200 bg-white'">
                    <div @click="openSection = 4" class="p-4 cursor-pointer flex justify-between items-center font-bold transition-all" :class="openSection === 4 ? 'bg-gradient-to-r from-orange-400 to-amber-500 text-white' : (isDarkMode ? 'text-gray-200 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-50')">
                        <span class="flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2z"></path></svg>
                            4. เลข 2 ตัว
                        </span>
                        <svg class="w-5 h-5 transform transition-transform" :class="openSection === 4 ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </div>
                    <transition name="slide-fade">
                        <div v-show="openSection === 4" class="p-5 space-y-4 text-sm">
                            <div class="flex justify-between gap-4">
                                <div class="flex-1"><label class="block font-bold">จำนวนแถว:</label><input type="number" id="row2Count" value="2" min="0" class="w-full p-2 border rounded-xl mt-1 focus:ring-orange-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div class="flex-1"><label class="block font-bold">จำนวนคอลัมน์:</label><input type="number" id="col2Count" value="2" min="1" class="w-full p-2 border rounded-xl mt-1 focus:ring-orange-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                            </div>
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mt-2">
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">เลือกฟอนต์:</label>
                                    <select id="num2FontFamily" @change="handleUpdate" class="w-full p-2.5 border rounded-xl mt-1 focus:ring-orange-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'">
                                        <option value="Prompt">Prompt</option><option value="Kanit">Kanit</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option><option value="Arial">Arial</option><option value="Tahoma">Tahoma</option>
                                    </select>
                                </div>
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">สไตล์:</label>
                                    <div class="flex gap-4 mt-3">
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="num2FontBold" class="mr-2 w-4 h-4 text-orange-500 rounded"> หนา</label>
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="num2FontItalic" class="mr-2 w-4 h-4 text-orange-500 rounded"> เอียง</label>
                                    </div>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-4 mt-2">
                                <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="num2FontSize" value="50" min="10" class="w-full p-2 border rounded-xl mt-1 focus:ring-orange-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold">สีอักษร:</label><input type="color" id="num2Color" value="#FFD700" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">ขอบหนา:</label><input type="number" id="num2StrokeWidth" value="3" min="0" class="w-full p-2 border rounded-xl mt-1 focus:ring-orange-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="num2StrokeColor" value="#000000" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                            </div>
                            <div class="flex flex-col sm:flex-row justify-between gap-4 mt-4 p-4 border rounded-xl" :class="isDarkMode ? 'border-gray-700 bg-gray-900/50' : 'border-gray-100 bg-gray-50'">
                                <div class="flex-1"><label class="block font-bold text-orange-500">ช่องไฟ ↔ (X):</label><input type="range" id="num2GapX" min="30" max="300" value="110" class="w-full mt-2 accent-orange-500"></div>
                                <div class="flex-1"><label class="block font-bold text-emerald-500">ช่องไฟ ↕ (Y):</label><input type="range" id="num2GapY" min="30" max="200" value="70" class="w-full mt-2 accent-emerald-500"></div>
                            </div>
                            <!-- 🎯 ปุ่มจัดกึ่งกลางแบบ 3D Button -->
                            <div class="text-center mt-5">
                                <button class="w-full bg-orange-500 hover:bg-orange-400 text-white font-bold py-3 rounded-xl border-b-4 border-orange-700 active:border-b-0 active:translate-y-1 transition-all shadow-md flex items-center justify-center gap-2" @click="centerElement('num2')">
                                    <svg class="w-5 h-5 text-yellow-200" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6c0 4.418 6 10 6 10s6-5.582 6-10a6 6 0 00-6-6zm0 8a2 2 0 110-4 2 2 0 010 4z"/></svg>
                                    จัดกลุ่มกึ่งกลาง
                                </button>
                            </div>
                            <label class="block font-bold mt-3">ตำแหน่งเริ่ม X:</label><input type="range" id="num2X" min="0" max="600" value="245" class="w-full mt-2 accent-orange-500">
                            <label class="block font-bold mt-3">ตำแหน่งเริ่ม Y:</label><input type="range" id="num2Y" min="0" max="600" value="280" class="w-full mt-2 accent-orange-500">
                        </div>
                    </transition>
                </div>

                <!-- 5. เลข 3 ตัว -->
                <div class="border rounded-2xl overflow-hidden transition-colors shadow-sm" :class="isDarkMode ? 'border-gray-700 bg-gray-800/50' : 'border-gray-200 bg-white'">
                    <div @click="openSection = 5" class="p-4 cursor-pointer flex justify-between items-center font-bold transition-all" :class="openSection === 5 ? 'bg-gradient-to-r from-yellow-500 to-amber-600 text-white' : (isDarkMode ? 'text-gray-200 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-50')">
                        <span class="flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5"></path></svg>
                            5. เลข 3 ตัว
                        </span>
                        <svg class="w-5 h-5 transform transition-transform" :class="openSection === 5 ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </div>
                    <transition name="slide-fade">
                        <div v-show="openSection === 5" class="p-5 space-y-4 text-sm">
                            <div class="flex justify-between gap-4">
                                <div class="flex-1"><label class="block font-bold">จำนวนแถว:</label><input type="number" id="row3Count" value="1" min="0" class="w-full p-2 border rounded-xl mt-1 focus:ring-yellow-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div class="flex-1"><label class="block font-bold">จำนวนคอลัมน์:</label><input type="number" id="col3Count" value="3" min="1" class="w-full p-2 border rounded-xl mt-1 focus:ring-yellow-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                            </div>
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mt-2">
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">เลือกฟอนต์:</label>
                                    <select id="num3FontFamily" @change="handleUpdate" class="w-full p-2.5 border rounded-xl mt-1 focus:ring-yellow-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'">
                                        <option value="Prompt">Prompt</option><option value="Kanit">Kanit</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option><option value="Arial">Arial</option><option value="Tahoma">Tahoma</option>
                                    </select>
                                </div>
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">สไตล์:</label>
                                    <div class="flex gap-4 mt-3">
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="num3FontBold" class="mr-2 w-4 h-4 text-yellow-500 rounded"> หนา</label>
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="num3FontItalic" class="mr-2 w-4 h-4 text-yellow-500 rounded"> เอียง</label>
                                    </div>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-4 mt-2">
                                <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="num3FontSize" value="50" min="10" class="w-full p-2 border rounded-xl mt-1 focus:ring-yellow-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold">สีอักษร:</label><input type="color" id="num3Color" value="#FFD700" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">ขอบหนา:</label><input type="number" id="num3StrokeWidth" value="3" min="0" class="w-full p-2 border rounded-xl mt-1 focus:ring-yellow-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="num3StrokeColor" value="#000000" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                            </div>
                            <div class="flex flex-col sm:flex-row justify-between gap-4 mt-4 p-4 border rounded-xl" :class="isDarkMode ? 'border-gray-700 bg-gray-900/50' : 'border-gray-100 bg-gray-50'">
                                <div class="flex-1"><label class="block font-bold text-yellow-500">ช่องไฟ ↔ (X):</label><input type="range" id="num3GapX" min="30" max="300" value="110" class="w-full mt-2 accent-yellow-500"></div>
                                <div class="flex-1"><label class="block font-bold text-emerald-500">ช่องไฟ ↕ (Y):</label><input type="range" id="num3GapY" min="30" max="200" value="70" class="w-full mt-2 accent-emerald-500"></div>
                            </div>
                            <!-- 🎯 ปุ่มจัดกึ่งกลางแบบ 3D Button -->
                            <div class="text-center mt-5">
                                <button class="w-full bg-yellow-500 hover:bg-yellow-400 text-white font-bold py-3 rounded-xl border-b-4 border-yellow-700 active:border-b-0 active:translate-y-1 transition-all shadow-md flex items-center justify-center gap-2" @click="centerElement('num3')">
                                    <svg class="w-5 h-5 text-yellow-100" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6c0 4.418 6 10 6 10s6-5.582 6-10a6 6 0 00-6-6zm0 8a2 2 0 110-4 2 2 0 010 4z"/></svg>
                                    จัดกลุ่มกึ่งกลาง
                                </button>
                            </div>
                            <label class="block font-bold mt-3">ตำแหน่งเริ่ม X:</label><input type="range" id="num3X" min="0" max="600" value="190" class="w-full mt-2 accent-yellow-500">
                            <label class="block font-bold mt-3">ตำแหน่งเริ่ม Y:</label><input type="range" id="num3Y" min="0" max="600" value="450" class="w-full mt-2 accent-yellow-500">
                        </div>
                    </transition>
                </div>

                <!-- 6. วันที่ -->
                <div class="border rounded-2xl overflow-hidden transition-colors shadow-sm" :class="isDarkMode ? 'border-gray-700 bg-gray-800/50' : 'border-gray-200 bg-white'">
                    <div @click="openSection = 6" class="p-4 cursor-pointer flex justify-between items-center font-bold transition-all" :class="openSection === 6 ? 'bg-gradient-to-r from-teal-500 to-emerald-600 text-white' : (isDarkMode ? 'text-gray-200 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-50')">
                        <span class="flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                            6. ตั้งค่าวันที่
                        </span>
                        <svg class="w-5 h-5 transform transition-transform" :class="openSection === 6 ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </div>
                    <transition name="slide-fade">
                        <div v-show="openSection === 6" class="p-5 space-y-4 text-sm">
                            <div>
                                <label class="block font-bold">เลือกวันที่:</label>
                                <input type="date" id="datePicker" class="w-full p-3 border rounded-xl mt-2 cursor-pointer focus:ring-teal-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'">
                            </div>
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mt-2">
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">เลือกฟอนต์:</label>
                                    <select id="dateFontFamily" @change="handleUpdate" class="w-full p-2.5 border rounded-xl mt-1 focus:ring-teal-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'">
                                        <option value="Prompt">Prompt</option><option value="Kanit">Kanit</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option><option value="Arial">Arial</option><option value="Tahoma">Tahoma</option>
                                    </select>
                                </div>
                                <div class="flex-1 w-full">
                                    <label class="block font-bold">สไตล์:</label>
                                    <div class="flex gap-4 mt-3">
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="dateFontBold" class="mr-2 w-4 h-4 text-teal-500 rounded"> หนา</label>
                                        <label class="flex items-center cursor-pointer font-medium"><input type="checkbox" id="dateFontItalic" class="mr-2 w-4 h-4 text-teal-500 rounded"> เอียง</label>
                                    </div>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-4 mt-2">
                                <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="dateFontSize" value="45" min="10" class="w-full p-2 border rounded-xl mt-1 focus:ring-teal-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold">สีตัวอักษร:</label><input type="color" id="dateColor" value="#000000" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">ความหนาขอบ:</label><input type="number" id="dateStrokeWidth" value="3" min="0" class="w-full p-2 border rounded-xl mt-1 focus:ring-teal-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-200'"></div>
                                <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="dateStrokeColor" value="#FFD700" class="w-full h-[42px] p-1 border rounded-xl cursor-pointer mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-200'"></div>
                            </div>
                            <!-- 🎯 ปุ่มจัดกึ่งกลางแบบ 3D Button -->
                            <div class="text-center mt-5">
                                <button class="w-full bg-emerald-500 hover:bg-emerald-400 text-white font-bold py-3 rounded-xl border-b-4 border-emerald-700 active:border-b-0 active:translate-y-1 transition-all shadow-md flex items-center justify-center gap-2" @click="centerElement('date')">
                                    <svg class="w-5 h-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6c0 4.418 6 10 6 10s6-5.582 6-10a6 6 0 00-6-6zm0 8a2 2 0 110-4 2 2 0 010 4z"/></svg>
                                    จัดวันที่กึ่งกลาง
                                </button>
                            </div>
                            <label class="block font-bold mt-3">ตำแหน่ง X:</label><input type="range" id="dateX" min="0" max="600" value="300" class="w-full mt-2 accent-teal-500">
                            <label class="block font-bold mt-3">ตำแหน่ง Y:</label><input type="range" id="dateY" min="0" max="600" value="530" class="w-full mt-2 accent-teal-500">
                        </div>
                    </transition>
                </div>
            </div>
            
            <hr class="my-2 border-t-2" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
            <button class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 rounded-xl font-extrabold text-xl shadow-xl shadow-blue-500/30 hover:scale-[1.02] transition-transform w-full flex items-center justify-center gap-3" @click="generateBatchPreviews">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                สร้างรูปทั้งหมด
            </button>
            <button id="downloadZipBtn" class="bg-gradient-to-r from-yellow-400 to-orange-500 text-gray-900 py-3.5 rounded-xl font-extrabold text-lg shadow-lg shadow-yellow-500/30 hover:scale-[1.02] transition-transform hidden w-full flex items-center justify-center gap-2" @click="downloadZip">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                ดาวน์โหลดไฟล์ ZIP
            </button>
        </div>
    </div>

    <!-- 📦 โมดอล (Popup) บันทึกเทมเพลต -->
    <transition name="fade">
        <div v-if="showSaveModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm px-4" @click.self="showSaveModal = false">
            <div class="p-8 rounded-3xl shadow-2xl w-full max-w-sm transform scale-100 transition-all border" :class="isDarkMode ? 'bg-gray-800 border-gray-700 shadow-black/50' : 'bg-white border-white'">
                <div class="flex items-center gap-3 mb-6">
                    <div class="p-3 bg-blue-100 text-blue-600 rounded-full"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg></div>
                    <h3 class="text-2xl font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-800'">บันทึกเทมเพลต</h3>
                </div>
                <label class="block text-sm font-bold mb-2" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">ตั้งชื่อเทมเพลตของคุณ:</label>
                <input v-model="newFormatName" type="text" placeholder="เช่น หวยไทย 1" class="w-full p-4 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 mb-8 transition-colors" :class="isDarkMode ? 'bg-gray-900/50 border-gray-600 text-white' : 'bg-gray-50 border-gray-200'" @keyup.enter="confirmSaveNew">
                <div class="flex gap-3">
                    <button @click="showSaveModal = false" class="flex-1 bg-gray-200 text-gray-800 py-3 rounded-xl font-bold hover:bg-gray-300 transition shadow-sm">ยกเลิก</button>
                    <button @click="confirmSaveNew" class="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 rounded-xl font-bold hover:scale-105 transition-transform shadow-lg shadow-blue-500/30">บันทึก</button>
                </div>
            </div>
        </div>
    </transition>

    <!-- 🔔 โมดอล (Popup) แจ้งเตือนระบบแบบ Custom ที่ใชั SVG แทน Emoji -->
    <transition name="fade">
        <div v-if="sysModal.show" class="fixed inset-0 z-[110] flex items-center justify-center bg-black/50 backdrop-blur-sm px-4" @click.self="closeSysModal">
            <div class="p-8 rounded-3xl shadow-2xl w-full max-w-sm transform scale-100 transition-all text-center border" :class="isDarkMode ? 'bg-gray-800 border-gray-700 shadow-black/50' : 'bg-white border-white'">
                
                <div class="flex justify-center mb-6">
                    <svg v-if="sysModal.typeVal === 'success'" class="w-20 h-20 text-emerald-500 drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <svg v-else-if="sysModal.typeVal === 'error'" class="w-20 h-20 text-red-500 drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <svg v-else-if="sysModal.typeVal === 'warning'" class="w-20 h-20 text-amber-500 drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                    <svg v-else class="w-20 h-20 text-blue-500 drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>

                <h3 class="text-2xl font-bold mb-3" :class="isDarkMode ? 'text-white' : 'text-gray-800'">{{ sysModal.title }}</h3>
                <p class="mb-8 text-base whitespace-pre-line" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">{{ sysModal.message }}</p>
                <div class="flex gap-3 justify-center">
                    <button v-if="sysModal.type === 'confirm'" @click="sysModal.show = false" class="flex-1 bg-gray-200 text-gray-800 px-5 py-3 rounded-xl font-bold hover:bg-gray-300 transition shadow-sm">ยกเลิก</button>
                    <button @click="sysModal.type === 'confirm' ? sysModal.onConfirm() : (sysModal.show = false)" class="flex-1 text-white py-3 rounded-xl font-bold transition-transform hover:scale-105 shadow-lg" :class="sysModal.typeVal === 'error' || sysModal.typeVal === 'warning' ? 'bg-gradient-to-r from-red-500 to-rose-600 shadow-red-500/30' : 'bg-gradient-to-r from-blue-600 to-indigo-600 shadow-blue-500/30'">
                        {{ sysModal.type === 'confirm' ? 'ยืนยัน' : 'ตกลง' }}
                    </button>
                </div>
            </div>
        </div>
    </transition>

    <!-- 🎯 ฐานเก็บฟอนต์ที่บังคับให้โหลดแน่นอน (แก้บั๊กฟอนต์ 100%) -->
    <div style="position: absolute; left: -9999px; top: -9999px; visibility: hidden; font-size: 20px;">
        <span style="font-family: 'Prompt'">โหลด</span><span style="font-family: 'Kanit'">โหลด</span><span style="font-family: 'Sarabun'">โหลด</span><span style="font-family: 'Mitr'">โหลด</span><span style="font-family: 'Mali'">โหลด</span><span style="font-family: 'Itim'">โหลด</span><span style="font-family: 'Chakra Petch'">โหลด</span><span style="font-family: 'Pattaya'">โหลด</span><span style="font-family: 'Pridi'">โหลด</span><span style="font-family: 'Charm'">โหลด</span><span style="font-family: 'Arial'">โหลด</span><span style="font-family: 'Tahoma'">โหลด</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useHead, useState } from '#imports'

// 🎯 แก้บั๊ก: นำเข้าลิงก์ Google Fonts ที่ถูกต้อง
useHead({
  script: [{ src: 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js' }],
  link: [{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Chakra+Petch:ital,wght@0,400;0,700;1,400;1,700&family=Charm:wght@400;700&family=Itim&family=Kanit:ital,wght@0,400;0,700;1,400;1,700&family=Mali:ital,wght@0,400;0,700;1,400;1,700&family=Mitr:wght@400;700&family=Pattaya&family=Pridi:wght@400;700&family=Prompt:ital,wght@0,400;0,700;1,400;1,700&family=Sarabun:ital,wght@0,400;0,700;1,400;1,700&display=swap' }]
})

const router = useRouter()

const isLoading = ref(true)
const isDarkMode = useState('darkMode')
const isExpired = ref(false)
const expireDateStr = ref('')
const openSection = ref(1) 

const showSaveModal = ref(false)
const newFormatName = ref('')

const bgBase64 = ref(null);
const logoBase64 = ref(null);

const sysModal = ref({ show: false, title: '', message: '', type: 'alert', typeVal: 'info', onConfirm: null })

const showAlert = (title, message, typeVal='info') => {
    sysModal.value = { show: true, title, message, type: 'alert', typeVal, onConfirm: null }
}
const showConfirm = (title, message, onConfirmCallback, typeVal='warning') => {
    sysModal.value = { show: true, title, message, type: 'confirm', typeVal, onConfirm: () => {
        sysModal.value.show = false;
        onConfirmCallback();
    }}
}

const closeSysModal = () => {
    if (sysModal.value.type === 'alert') {
        sysModal.value.show = false;
    }
}

let canvas = null;
let ctx = null;
let numbers3Grid = [];
let numbers2Grid = [];
let numbers1Grid = [];
let bgImage = null;
let logoImage = null;
let generatedImagesToZip = [];
let savedFormatsList = []; 

const getTodayStr = () => {
    const d = new Date();
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().split('T')[0];
};

const lotteryData = {
    "หวยหุ้น": ["เกาหลี", "จีนเช้า", "จีนบ่าย", "จีนรอบเช้า", "ดาวโจนส์", "ไต้หวัน", "ไทยเย็น", "น้ำมันปิด", "น้ำมันเปิด", "นิเคอิเช้า", "นิเคอิบ่าย", "มาเลย์", "เยอรมัน", "รัสเซีย", "สิงคโปร์", "หุ้นทองปิด", "หุ้นทองเปิด", "หุ้นฮั่งเส็งเช้า", "หุ้นฮั่งเส็งบ่าย", "อังกฤษ", "อินเดีย", "อียิปต์", "ฮั่งเส็งเช้า", "ฮั่งเส็งบ่าย"],
    "หวยหุ้น VIP": ["เกาหลี VIP", "จีน VIP (เช้า)", "จีน VIP (บ่าย)", "จีนเช้า VIP", "จีนบ่าย VIP", "ดาวโจนส์ VIP", "ไต้หวัน VIP", "นิเคอิ VIP (เช้า)", "นิเคอิ VIP (บ่าย)", "นิเคอิเช้า VIP", "นิเคอิบ่าย VIP", "เยอรมัน VIP", "รัสเซีย VIP", "สิงคโปร์ VIP", "อังกฤษ VIP", "ฮั่งเส็ง VIP (เช้า)", "ฮั่งเส็ง VIP (บ่าย)", "ฮั่งเส็งเช้า VIP", "ฮั่งเส็งบ่าย VIP"],
    "หวยหุ้นพิเศษ": ["เกาหลี พิเศษ", "จีน พิเศษ เช้า", "จีน พิเศษ บ่าย", "ดาวโจนส์ พิเศษ", "ไต้หวัน พิเศษ", "นิเคอิ พิเศษ เช้า", "นิเคอิ พิเศษ บ่าย", "เยอรมัน พิเศษ", "รัสเซีย พิเศษ", "เวียดนาม พิเศษ เช้า", "เวียดนาม พิเศษ บ่าย", "สิงคโปร์ พิเศษ", "อังกฤษ พิเศษ", "ฮั่งเส็ง พิเศษ เช้า", "ฮั่งเส็ง พิเศษ บ่าย"],
    "ฮานอย": ["เวียดนาม VIP ออนไลน์", "เวียดนาม พิเศษ ออนไลน์", "เวียดนาม ออนไลน์", "ฮานอย", "ฮานอย EXTRA", "ฮานอย HD", "ฮานอยกาชาด", "ฮานอยเช้า", "ฮานอยซุปเปอร์", "ฮานอยดานัง", "ฮานอยพรีเมี่ยม", "ฮานอยพัฒนา", "ฮานอย พิเศษ", "ฮานอยรอบดึก", "ฮานอยสามัคคี", "ฮานอยอาเซียน"],
    "ลาว": ["ลาว EXTRA", "ลาว HD", "ลาว STAR VIP", "ลาว TV", "ลาว VIP", "ลาวกาชาด", "ลาวเช้า", "ลาวดิจิตอล", "ลาวทดแทน", "ลาวเที่ยง", "ลาวนิยม", "ลาวประชาชน", "ลาวประตูชัย", "ลาวพัฒนา", "ลาวมิตรภาพ", "ลาวสตาร์", "ลาวสะหวันมะเขต", "ลาวสันติภาพ", "ลาวสามัคคี", "ลาวสามัคคี VIP", "ลาวอาเซียน"],
    "ไทย": ["ธกส", "รัฐบาลไทย", "ออมสิน"],
    "หวยรายวัน": ["ดาวโจนส์STAR", "ดาวโจนส์อเมริกา", "ยี่กี", "ยูโร", "สยาม"]
};

const settingInputs = [
    'showBg', 'showLogo',
    'logoX', 'logoY', 'logoScale', 
    'headerX', 'headerY', 'headerFontSize', 'headerColor', 'headerStrokeWidth', 'headerStrokeColor', 'headerFontFamily', 'headerFontBold', 'headerFontItalic',
    'datePicker', 'dateX', 'dateY', 'dateFontSize', 'dateColor', 'dateStrokeWidth', 'dateStrokeColor', 'dateFontFamily', 'dateFontBold', 'dateFontItalic',
    'row3Count', 'col3Count', 'num3X', 'num3Y', 'num3FontSize', 'num3Color', 'num3GapX', 'num3GapY', 'num3StrokeWidth', 'num3StrokeColor', 'num3FontFamily', 'num3FontBold', 'num3FontItalic',
    'row2Count', 'col2Count', 'num2X', 'num2Y', 'num2FontSize', 'num2Color', 'num2GapX', 'num2GapY', 'num2StrokeWidth', 'num2StrokeColor', 'num2FontFamily', 'num2FontBold', 'num2FontItalic',
    'row1Count', 'col1Count', 'num1X', 'num1Y', 'num1FontSize', 'num1Color', 'num1GapX', 'num1GapY', 'num1StrokeWidth', 'num1StrokeColor', 'num1FontFamily', 'num1FontBold', 'num1FontItalic'
];

const fetchFormats = async () => {
    const token = localStorage.getItem('token');
    const res = await fetch('https://gen-picture-hwy.onrender.com/formats', { headers: { 'Authorization': `Bearer ${token}` } });
    if(res.ok) {
        savedFormatsList = await res.json();
        const sel = document.getElementById('formatSelect');
        sel.innerHTML = '<option value="NEW">➕ สร้างเทมเพลตใหม่</option>';
        savedFormatsList.forEach(f => {
            const opt = document.createElement('option');
            opt.value = f.format_name;
            opt.innerText = f.format_name;
            sel.appendChild(opt);
        });
    }
}

const loadSelectedFormat = () => {
    const sel = document.getElementById('formatSelect').value;
    if(sel === 'NEW') return showAlert('แจ้งเตือน', 'กรุณาเลือกชื่อเทมเพลตด้านซ้ายก่อนโหลดครับ', 'info');
    
    const format = savedFormatsList.find(f => f.format_name === sel);
    if(format) {
        const settings = format.settings_data;
        settingInputs.forEach(id => {
            const el = document.getElementById(id);
            if(el && settings[id] !== undefined) {
                if(el.type === 'checkbox') el.checked = settings[id];
                else el.value = settings[id];
            }
        });
        if(settings['selectedHeaders']) {
            document.querySelectorAll('.sub-cb').forEach(cb => cb.checked = false);
            settings['selectedHeaders'].forEach(val => {
                const cb = document.querySelector(`.sub-cb[value="${val}"]`);
                if(cb) cb.checked = true;
            });
            updateCategoryCheckboxes();
        }

        if(settings['bgBase64']) {
            bgBase64.value = settings['bgBase64'];
            const img = new Image();
            img.onload = () => { bgImage = img; handleUpdate(); };
            img.src = settings['bgBase64'];
        } else {
            bgBase64.value = null;
            const defBg = new Image();
            defBg.src = '/img/default-bg.png';
            defBg.onload = () => { bgImage = defBg; handleUpdate(); };
        }

        if(settings['logoBase64']) {
            logoBase64.value = settings['logoBase64'];
            const img2 = new Image();
            img2.onload = () => { logoImage = img2; handleUpdate(); };
            img2.src = settings['logoBase64'];
        } else {
            logoBase64.value = null;
            const defLogo = new Image();
            defLogo.src = '/img/default-logo.png';
            defLogo.onload = () => { logoImage = defLogo; handleUpdate(); };
        }

        setTimeout(() => { generatePreviewNumbers(); }, 100);
        showAlert('สำเร็จ', `โหลดเทมเพลต '${sel}' เสร็จสิ้น!`, 'success');
    }
}

const clearAllPreviews = () => {
    if (generatedImagesToZip.length === 0) return showAlert('แจ้งเตือน', 'ยังไม่มีรูปภาพพรีวิวให้ลบครับ', 'info');
    
    showConfirm('ยืนยันการลบ', 'คุณแน่ใจหรือไม่ว่าต้องการเคลียร์รูปพรีวิวทั้งหมดทิ้ง?', () => {
        generatedImagesToZip = [];
        const previewZone = document.getElementById('previewZone');
        if (previewZone) {
            previewZone.innerHTML = `
                <div class="text-center flex flex-col items-center justify-center opacity-60 hover:opacity-100 transition-opacity w-full py-8">
                    <svg class="w-16 h-16 mb-4 ${isDarkMode.value ? 'text-gray-500' : 'text-indigo-300'}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                    <span class="font-bold text-lg ${isDarkMode.value ? 'text-gray-400' : 'text-indigo-500'}">พื้นที่พรีวิวรูปภาพ</span>
                    <span class="text-sm mt-1 ${isDarkMode.value ? 'text-gray-500' : 'text-indigo-400'}">เมื่อกดปุ่ม "สร้างรูปทั้งหมด" รูปจะมาแสดงที่นี่ครับ</span>
                </div>`;
        }
        document.getElementById('downloadZipBtn').classList.add('hidden');
    }, 'warning');
}

const deleteSelectedFormat = async () => {
    const token = localStorage.getItem('token');
    const sel = document.getElementById('formatSelect').value;
    
    if(sel === 'NEW') return showAlert('แจ้งเตือน', 'ไม่สามารถลบรายการนี้ได้ กรุณาเลือกเทมเพลตที่บันทึกไว้ครับ', 'error');
    
    showConfirm('ยืนยันการลบ', `ยืนยันการลบเทมเพลต '${sel}' ทิ้งแบบถาวร? \n(การกระทำนี้ไม่สามารถกู้คืนได้)`, async () => {
        try {
            const res = await fetch(`https://gen-picture-hwy.onrender.com/formats/${encodeURIComponent(sel)}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if(res.ok) {
                showAlert('สำเร็จ', 'ลบเทมเพลตสำเร็จ!', 'success');
                await fetchFormats();
                document.getElementById('formatSelect').value = 'NEW';
            } else {
                showAlert('ข้อผิดพลาด', 'เกิดข้อผิดพลาดในการลบ', 'error');
            }
        } catch(e) {
            console.error(e);
        }
    }, 'warning');
}

const triggerSaveFormat = () => {
    const sel = document.getElementById('formatSelect').value;
    if (sel === 'NEW') {
        newFormatName.value = '';
        showSaveModal.value = true;
    } else {
        showConfirm('อัปเดตเทมเพลต', `คุณต้องการอัปเดตและบันทึกทับเทมเพลต '${sel}' ใช่หรือไม่?`, () => {
            executeSaveFormat(sel);
        }, 'info');
    }
}

const confirmSaveNew = () => {
    if (!newFormatName.value.trim()) return showAlert('แจ้งเตือน', 'กรุณากรอกชื่อเทมเพลต!', 'warning');
    showSaveModal.value = false;
    executeSaveFormat(newFormatName.value.trim());
}

const executeSaveFormat = async (formatName) => {
    const token = localStorage.getItem('token');
    let settings = {};
    settingInputs.forEach(id => {
        const el = document.getElementById(id);
        if(el) settings[id] = el.type === 'checkbox' ? el.checked : el.value;
    });
    settings['selectedHeaders'] = getSelectedHeaders();
    
    settings['bgBase64'] = bgBase64.value;
    settings['logoBase64'] = logoBase64.value;

    try {
        const response = await fetch('https://gen-picture-hwy.onrender.com/formats', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                format_name: formatName,
                settings_data: settings
            })
        });
        const data = await response.json();
        if(response.ok) {
            showAlert('สำเร็จ', data.message.replace('รูปแบบ', 'เทมเพลต'), 'success');
            await fetchFormats(); 
            document.getElementById('formatSelect').value = formatName; 
        } else {
            showAlert('ข้อผิดพลาด', data.detail, 'error');
        }
    } catch(e) {
        showAlert('ข้อผิดพลาด', 'ไม่สามารถเชื่อมต่อฐานข้อมูลได้', 'error');
    }
}

const resetFormat = () => {
    showConfirm('รีเซ็ตการตั้งค่า', 'คุณแน่ใจหรือไม่ที่จะ "รีเซ็ต" การตั้งค่าปัจจุบันทั้งหมดให้กลับเป็นค่าเริ่มต้น?', () => {
        localStorage.removeItem('lotterySettings'); 
        window.location.reload(); 
    }, 'warning');
}

const renderLotterySelector = () => {
    const container = document.getElementById('lotterySelector');
    if(!container) return;
    container.innerHTML = '';
    for (const [category, items] of Object.entries(lotteryData)) {
        const catDiv = document.createElement('div');
        catDiv.className = 'mb-1 lottery-category';
        const catHeader = document.createElement('div');
        catHeader.className = 'flex items-center justify-between bg-gray-400/20 p-3 rounded-xl cursor-pointer hover:bg-gray-400/40 transition-colors';
        
        const catLabel = document.createElement('label');
        catLabel.className = 'font-bold text-indigo-600 flex items-center cursor-pointer text-sm m-0 flex-1';
        const catCb = document.createElement('input');
        catCb.type = 'checkbox';
        catCb.className = 'mr-3 cursor-pointer w-4 h-4 cat-cb rounded text-indigo-600 focus:ring-indigo-500';
        catLabel.appendChild(catCb);
        catLabel.appendChild(document.createTextNode(' ' + category));
        
        const toggleBtn = document.createElement('span');
        toggleBtn.className = 'text-xs text-indigo-600 bg-indigo-100/50 p-1.5 px-3 rounded-lg font-bold';
        toggleBtn.innerHTML = '▼ เปิด'; 
        
        catHeader.appendChild(catLabel);
        catHeader.appendChild(toggleBtn);
        catDiv.appendChild(catHeader);
        
        const subDiv = document.createElement('div');
        subDiv.className = 'sub-items flex flex-col p-3 bg-transparent border border-t-0 rounded-b-xl border-gray-400/20';
        subDiv.style.display = 'none'; 
        
        items.forEach(item => {
            const subLabel = document.createElement('label');
            subLabel.className = 'font-medium text-xs flex items-center mt-2 cursor-pointer text-gray-600 dark:text-gray-300';
            const subCb = document.createElement('input');
            subCb.type = 'checkbox';
            subCb.className = 'mr-3 cursor-pointer w-3.5 h-3.5 sub-cb rounded text-purple-500 focus:ring-purple-500';
            subCb.value = item;
            subLabel.appendChild(subCb);
            subLabel.appendChild(document.createTextNode(' ' + item));
            subDiv.appendChild(subLabel);
        });
        catDiv.appendChild(subDiv);
        container.appendChild(catDiv);

        toggleBtn.addEventListener('click', () => {
            const isHidden = subDiv.style.display === 'none';
            subDiv.style.display = isHidden ? 'flex' : 'none';
            toggleBtn.innerHTML = isHidden ? '▲ ปิด' : '▼ เปิด';
        });

        catCb.addEventListener('change', function() {
            const childCbs = subDiv.querySelectorAll('.sub-cb');
            childCbs.forEach(cb => cb.checked = this.checked);
            handleUpdate();
        });
        
        subDiv.querySelectorAll('.sub-cb').forEach(cb => {
            cb.addEventListener('change', function() {
                updateCategoryCheckboxes();
                handleUpdate();
            });
        });
    }
}

const updateCategoryCheckboxes = () => {
    document.querySelectorAll('.lottery-category').forEach(cat => {
        const total = cat.querySelectorAll('.sub-cb').length;
        const checkedCount = cat.querySelectorAll('.sub-cb:checked').length;
        const catCb = cat.querySelector('.cat-cb');
        if (checkedCount > 0 && checkedCount < total) {
            catCb.indeterminate = true;
            catCb.checked = false;
        } else {
            catCb.indeterminate = false;
            catCb.checked = (total > 0 && total === checkedCount);
        }
    });
}

const getSelectedHeaders = () => {
    const checkboxes = document.querySelectorAll('.sub-cb:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

const compressImage = (imgSrc, maxWidth, callback) => {
    const img = new Image();
    img.onload = () => {
        const canvas = document.createElement('canvas');
        let width = img.width;
        let height = img.height;
        if (width > maxWidth) {
            height = Math.round((height * maxWidth) / width);
            width = maxWidth;
        }
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);
        callback(canvas.toDataURL('image/jpeg', 0.6));
    };
    img.src = imgSrc;
};

const handleImageUpload = (e, type) => {
    const file = e.target.files[0];
    if (!file) return;
    
    if (file.size > 2 * 1024 * 1024) {
        showAlert('ไฟล์ใหญ่เกินไป', 'กรุณาอัปโหลดรูปภาพขนาดไม่เกิน 2MB เพื่อป้องกันระบบหน่วงครับ', 'warning');
        e.target.value = '';
        return;
    }

    const reader = new FileReader();
    reader.onload = function(event) {
        compressImage(event.target.result, type === 'bg' ? 800 : 400, (compressedBase64) => {
            const img = new Image();
            img.onload = function() {
                if (type === 'bg') {
                    bgImage = img;
                    bgBase64.value = compressedBase64;
                }
                if (type === 'logo') {
                    logoImage = img;
                    logoBase64.value = compressedBase64;
                }
                handleUpdate();
            }
            img.src = compressedBase64;
        });
    }
    reader.readAsDataURL(file);
}

const createNumbersArray = (rows, cols, digitsCount) => {
    let grid = [];
    let used1Digits = new Set(); 

    for (let i = 0; i < rows; i++) {
        let row = [];
        for (let j = 0; j < cols; j++) {
            if (digitsCount === 3) {
                row.push(Math.floor(Math.random() * 1000).toString().padStart(3, '0'));
            } else if (digitsCount === 2) {
                row.push(Math.floor(Math.random() * 100).toString().padStart(2, '0'));
            } else if (digitsCount === 1) {
                let num;
                let attempts = 0;
                do {
                    num = (Math.floor(Math.random() * 9) + 1).toString();
                    attempts++;
                    if(attempts > 50) break; 
                } while (used1Digits.has(num));
                
                used1Digits.add(num);
                row.push(num);
            }
        }
        grid.push(row);
    }
    return grid;
}

const generatePreviewNumbers = () => {
    numbers3Grid = createNumbersArray(document.getElementById('row3Count').value, document.getElementById('col3Count').value, 3);
    numbers2Grid = createNumbersArray(document.getElementById('row2Count').value, document.getElementById('col2Count').value, 2);
    numbers1Grid = createNumbersArray(document.getElementById('row1Count').value, document.getElementById('col1Count').value, 1);
    handleUpdate();
}

const centerElement = (type) => {
    if(!canvas) return;
    if (type === 'num3') {
        const cols = parseInt(document.getElementById('col3Count').value);
        const gapX3 = parseInt(document.getElementById('num3GapX').value);
        document.getElementById('num3X').value = (canvas.width - ((cols - 1) * gapX3)) / 2;
    } else if (type === 'num2') {
        const cols = parseInt(document.getElementById('col2Count').value);
        const gapX2 = parseInt(document.getElementById('num2GapX').value);
        document.getElementById('num2X').value = (canvas.width - ((cols - 1) * gapX2)) / 2;
    } else if (type === 'num1') {
        const cols = parseInt(document.getElementById('col1Count').value);
        const gapX1 = parseInt(document.getElementById('num1GapX').value);
        document.getElementById('num1X').value = (canvas.width - ((cols - 1) * gapX1)) / 2;
    } else if (type === 'logo' || type === 'header' || type === 'date') {
        document.getElementById(type + 'X').value = canvas.width / 2;
    }
    handleUpdate();
}

const getFontString = (idPrefix, fontSize) => {
    const family = document.getElementById(idPrefix + 'FontFamily').value;
    const isBold = document.getElementById(idPrefix + 'FontBold').checked ? 'bold' : 'normal';
    const isItalic = document.getElementById(idPrefix + 'FontItalic').checked ? 'italic' : 'normal';
    return `${isItalic} ${isBold} ${fontSize}px "${family}", sans-serif`;
}

// 🎯 ฟังก์ชันจัดการอัปเดตระบบ เพื่อแก้บั๊ก Canvas วาดฟอนต์ไม่ทัน 100%
const handleUpdate = () => {
    draw();
    setTimeout(draw, 50);
    setTimeout(draw, 150);
    setTimeout(draw, 300);
    setTimeout(draw, 500);
    setTimeout(draw, 800);
}

const draw = (currentHeader = null) => {
    if(!ctx || !canvas) return;
    if(document.getElementById('logoScaleVal')) {
        document.getElementById('logoScaleVal').innerText = document.getElementById('logoScale').value;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    const isShowBg = document.getElementById('showBg') ? document.getElementById('showBg').checked : true;
    if (isShowBg && bgImage) {
        ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
    } else { 
        ctx.fillStyle = isDarkMode.value ? '#1f2937' : '#ffffff'; 
        ctx.fillRect(0, 0, canvas.width, canvas.height); 
    }

    const isShowLogo = document.getElementById('showLogo') ? document.getElementById('showLogo').checked : true;
    if (isShowLogo && logoImage) {
        const logoX = parseInt(document.getElementById('logoX').value);
        const logoY = parseInt(document.getElementById('logoY').value);
        const scale = parseInt(document.getElementById('logoScale').value) / 100;
        const width = logoImage.width * scale;
        const height = logoImage.height * scale;
        ctx.drawImage(logoImage, logoX - (width/2), logoY - (height/2), width, height);
    }
    
    const headerX = parseInt(document.getElementById('headerX').value);
    const headerY = parseInt(document.getElementById('headerY').value);
    const headerFontSize = document.getElementById('headerFontSize').value;
    const headerStrokeWidth = parseInt(document.getElementById('headerStrokeWidth').value);
    
    const selectedHeaders = getSelectedHeaders();
    let displayHeader = currentHeader || (selectedHeaders.length > 0 ? selectedHeaders[0] : 'โปรดเลือกหัวข้อหวย');
    
    ctx.fillStyle = document.getElementById('headerColor').value;
    ctx.strokeStyle = document.getElementById('headerStrokeColor').value;
    ctx.lineWidth = headerStrokeWidth;
    ctx.font = getFontString('header', headerFontSize);
    ctx.textAlign = 'center';
    ctx.fillText(displayHeader, headerX, headerY);
    if (headerStrokeWidth > 0) ctx.strokeText(displayHeader, headerX, headerY);
    
    const dateVal = document.getElementById('datePicker').value;
    if (dateVal) {
        const parts = dateVal.split('-');
        const year = (parseInt(parts[0]) + 543).toString().slice(-2);
        const formattedDate = `${parts[2]}/${parts[1]}/${year}`;
        
        const dateX = parseInt(document.getElementById('dateX').value);
        const dateY = parseInt(document.getElementById('dateY').value);
        const dateFontSize = document.getElementById('dateFontSize').value;
        const dateStrokeWidth = parseInt(document.getElementById('dateStrokeWidth').value);
        
        ctx.fillStyle = document.getElementById('dateColor').value;
        ctx.strokeStyle = document.getElementById('dateStrokeColor').value;
        ctx.lineWidth = dateStrokeWidth;
        ctx.font = getFontString('date', dateFontSize);
        ctx.textAlign = 'center';
        ctx.fillText(formattedDate, dateX, dateY);
        if (dateStrokeWidth > 0) ctx.strokeText(formattedDate, dateX, dateY);
    }

    const drawNumbers = (grid, idPrefix) => {
        const fontSize = document.getElementById(idPrefix + 'FontSize').value;
        const startX = parseInt(document.getElementById(idPrefix + 'X').value);
        const startY = parseInt(document.getElementById(idPrefix + 'Y').value);
        const gapX = parseInt(document.getElementById(idPrefix + 'GapX').value);
        const gapY = parseInt(document.getElementById(idPrefix + 'GapY').value);
        
        ctx.fillStyle = document.getElementById(idPrefix + 'Color').value;
        ctx.strokeStyle = document.getElementById(idPrefix + 'StrokeColor').value;
        ctx.lineWidth = parseInt(document.getElementById(idPrefix + 'StrokeWidth').value);
        ctx.font = getFontString(idPrefix, fontSize);
        
        grid.forEach((row, rowIndex) => {
            row.forEach((num, colIndex) => {
                const x = startX + (colIndex * gapX);
                const y = startY + (rowIndex * gapY);
                ctx.fillText(num, x, y);
                if (ctx.lineWidth > 0) ctx.strokeText(num, x, y);
            });
        });
    };

    drawNumbers(numbers3Grid, 'num3');
    drawNumbers(numbers2Grid, 'num2');
    drawNumbers(numbers1Grid, 'num1');
}

// 🎯 ระบบบังคับโหลดฟอนต์ทั้งหมดล่วงหน้าแบบใหม่ รองรับทุกเบราว์เซอร์
const preloadFonts = () => {
    const fontsToLoad = ['Prompt', 'Kanit', 'Sarabun', 'Mitr', 'Mali', 'Itim', 'Chakra Petch', 'Pattaya', 'Pridi', 'Charm', 'Arial', 'Tahoma'];
    if (document.fonts) {
        fontsToLoad.forEach(font => {
            document.fonts.load(`16px "${font}"`).then(() => {
                handleUpdate(); 
            }).catch(e => {});
        });
    }
}

const generateBatchPreviews = () => {
    const previewZone = document.getElementById('previewZone');
    previewZone.innerHTML = ''; 
    generatedImagesToZip = []; 
    
    const headers = getSelectedHeaders();
    if(headers.length === 0) return showAlert('แจ้งเตือน', "กรุณาติ๊กเลือกชื่อหัวข้ออย่างน้อย 1 ชื่อครับ", 'info');

    const r3 = document.getElementById('row3Count').value, c3 = document.getElementById('col3Count').value;
    const r2 = document.getElementById('row2Count').value, c2 = document.getElementById('col2Count').value;
    const r1 = document.getElementById('row1Count').value, c1 = document.getElementById('col1Count').value;

    for (let i = 0; i < headers.length; i++) {
        const headerName = headers[i];
        numbers3Grid = createNumbersArray(r3, c3, 3);
        numbers2Grid = createNumbersArray(r2, c2, 2);
        numbers1Grid = createNumbersArray(r1, c1, 1);
        
        draw(headerName);
        
        const dataUrl = canvas.toDataURL('image/png');
        generatedImagesToZip.push({ fileName: headerName, data: dataUrl });
        
        const div = document.createElement('div');
        div.className = 'relative flex flex-col items-center font-bold text-xs transform transition-transform hover:scale-105';
        
        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
        removeBtn.className = 'absolute -top-2 -right-2 bg-red-500 text-white border-none rounded-full w-6 h-6 text-xs cursor-pointer shadow-lg hover:bg-red-600 flex items-center justify-center transition-colors';
        removeBtn.onclick = function() {
            div.remove();
            generatedImagesToZip = generatedImagesToZip.filter(img => img.fileName !== headerName);
            if (generatedImagesToZip.length === 0) {
                document.getElementById('downloadZipBtn').classList.add('hidden');
                previewZone.innerHTML = `
                    <div class="text-center flex flex-col items-center justify-center opacity-60 hover:opacity-100 transition-opacity w-full py-8">
                        <svg class="w-16 h-16 mb-4 ${isDarkMode.value ? 'text-gray-500' : 'text-indigo-300'}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                        <span class="font-bold text-lg ${isDarkMode.value ? 'text-gray-400' : 'text-indigo-500'}">พื้นที่พรีวิวรูปภาพ</span>
                        <span class="text-sm mt-1 ${isDarkMode.value ? 'text-gray-500' : 'text-indigo-400'}">เมื่อกดปุ่ม "สร้างรูปทั้งหมด" รูปจะมาแสดงที่นี่ครับ</span>
                    </div>`;
            }
        };

        const img = document.createElement('img');
        img.src = dataUrl;
        img.className = 'w-[100px] border-2 border-indigo-100 rounded-xl shadow-md mb-2';
        const span = document.createElement('span');
        span.innerText = headerName;
        span.className = isDarkMode.value ? 'text-gray-300' : 'text-gray-700';
        
        div.appendChild(removeBtn);
        div.appendChild(img);
        div.appendChild(span);
        previewZone.appendChild(div);
    }

    document.getElementById('downloadZipBtn').classList.remove('hidden');
    generatePreviewNumbers(); 
}

const downloadZip = () => {
    if (generatedImagesToZip.length === 0 || typeof window.JSZip === 'undefined') return;
    const zip = new window.JSZip();
    generatedImagesToZip.forEach(imageObj => {
        const base64Data = imageObj.data.replace(/^data:image\/png;base64,/, "");
        zip.file(`${imageObj.fileName}.png`, base64Data, {base64: true});
    });
    zip.generateAsync({type:"blob"}).then(function(content) {
        const link = document.createElement('a');
        link.href = URL.createObjectURL(content);
        link.download = "lucky_numbers_batch.zip";
        link.click();
    });
}

const initApp = () => {
    const dateInput = document.getElementById('datePicker');
    if(dateInput) dateInput.value = getTodayStr();

    document.querySelectorAll('input, select').forEach(el => {
        if(el.type !== 'file' && !el.classList.contains('sub-cb') && !el.classList.contains('cat-cb') && el.id !== 'formatSelect') {
            if (el.id.includes('Count')) {
                el.addEventListener('input', () => { setTimeout(generatePreviewNumbers, 50); });
                el.addEventListener('change', () => { setTimeout(generatePreviewNumbers, 50); });
            } else {
                el.addEventListener('input', handleUpdate);
                if (el.type === 'checkbox' || el.tagName.toLowerCase() === 'select') {
                    el.addEventListener('change', handleUpdate);
                }
            }
        }
    });
    
    const bgUpload = document.getElementById('bgUpload');
    const logoUpload = document.getElementById('logoUpload');
    if(bgUpload) bgUpload.addEventListener('change', (e) => handleImageUpload(e, 'bg'));
    if(logoUpload) logoUpload.addEventListener('change', (e) => handleImageUpload(e, 'logo'));
}

onMounted(async () => {
    const token = localStorage.getItem('token');
    if (!token) return router.push('/login');

    try {
        const res = await fetch('https://gen-picture-hwy.onrender.com/users/me', { headers: { 'Authorization': `Bearer ${token}` } });
        if(res.ok) {
            const userData = await res.json();
            const end_date = new Date(userData.sub_end);
            if (end_date < new Date()) {
                isExpired.value = true;
                expireDateStr.value = end_date.toLocaleString('th-TH', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' });
                isLoading.value = false;
                return; 
            }
        } else {
            return router.push('/login');
        }
    } catch(e) {
        console.error(e);
    }

    canvas = document.getElementById('myCanvas');
    if(canvas) ctx = canvas.getContext('2d');

    renderLotterySelector();
    await fetchFormats(); 
    initApp();
    generatePreviewNumbers(); 
    
    preloadFonts();

    document.fonts.ready.then(() => {
        const defBg = new Image();
        defBg.src = '/img/default-bg.png';
        defBg.onload = () => { bgImage = defBg; handleUpdate(); };

        const defLogo = new Image();
        defLogo.src = '/img/default-logo.png';
        defLogo.onload = () => { logoImage = defLogo; handleUpdate(); };
        
        handleUpdate(); 
    });

    isLoading.value = false;
})
</script>

<style scoped>
.slide-fade-enter-active { transition: all 0.3s ease-out; }
.slide-fade-leave-active { transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1); }
.slide-fade-enter-from, .slide-fade-leave-to { transform: translateY(-10px); opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>