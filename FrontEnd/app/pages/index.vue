<template>
  <div class="transition-colors duration-300 min-h-screen">
    
    <!-- หน้าจอหมุนโหลด -->
    <div v-show="isLoading" class="flex flex-col items-center justify-center h-[80vh]">
        <div class="animate-spin rounded-full h-24 w-24 border-t-4 border-b-4 border-blue-500 mb-6"></div>
        <h2 class="text-2xl font-bold text-blue-500 animate-pulse">กำลังโหลดข้อมูลระบบ กรุณารอสักครู่...</h2>
        <p class="text-sm mt-2 opacity-70" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">(หากไม่มีการใช้งานนาน เซิร์ฟเวอร์อาจจะใช้เวลาตื่นประมาณ 30-50 วินาทีครับ)</p>
    </div>

    <!-- แจ้งเตือนหมดอายุ -->
    <div v-show="!isLoading && isExpired" class="flex flex-col items-center justify-center h-[80vh]">
        <div class="p-10 rounded-lg shadow-xl text-center max-w-lg border-t-4 border-red-500 transition-colors" :class="isDarkMode ? 'bg-gray-800 text-white' : 'bg-white'">
            <div class="text-7xl mb-4">⚠️</div>
            <h2 class="text-3xl font-bold text-red-500 mb-2">แพ็กเกจหมดอายุแล้ว</h2>
            <p class="mb-4 text-lg">บัญชีของคุณหมดอายุเมื่อเวลา<br><strong class="text-xl text-red-400">{{ expireDateStr }}</strong></p>
            <p class="opacity-70 text-sm mb-6">กรุณาติดต่อแอดมินเพื่อทำการต่ออายุแพ็กเกจครับ</p>
            <a href="https://line.me/ti/p/~@yourline" target="_blank" class="inline-block bg-green-500 text-white px-8 py-3 rounded-full font-bold hover:bg-green-600 transition shadow-md text-lg">💬 ติดต่อแอดมินผ่าน Line</a>
        </div>
    </div>

    <!-- แอปพลิเคชันหลัก -->
    <div v-show="!isLoading && !isExpired" id="mainApp" class="flex flex-wrap gap-6 w-full max-w-[1200px] mx-auto mt-2 relative">
        
        <!-- ฝั่งซ้าย: พรีวิว -->
        <div class="canvas-container flex-1 flex flex-col items-center p-6 rounded-xl shadow-lg min-w-[300px] transition-colors" :class="isDarkMode ? 'bg-gray-800' : 'bg-white'">
            <h3 class="text-xl font-bold mb-4 flex items-center gap-2" :class="isDarkMode ? 'text-white' : 'text-gray-700'">👁️ ภาพพรีวิว</h3>
            
            <canvas id="myCanvas" width="600" height="600" class="w-full max-w-[450px] h-auto border-4 shadow-2xl rounded-lg" :class="isDarkMode ? 'border-gray-600' : 'border-gray-200'"></canvas>
            
            <button class="mt-6 bg-teal-500 text-white py-3 px-6 rounded-lg font-bold shadow-lg hover:bg-teal-600 transition w-full max-w-[450px] text-lg" @click="generatePreviewNumbers">🎲 สุ่มตัวเลขใหม่ (ทดสอบดูตัวอย่าง)</button>

            <div class="flex justify-between items-center mt-10 mb-2 border-b-2 w-full pb-2" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                <h3 class="text-lg font-bold m-0" :class="isDarkMode ? 'text-white' : 'text-gray-700'">🖼️ พรีวิวรูปภาพที่พร้อมสร้าง</h3>
                <button @click="clearAllPreviews" class="bg-red-500 text-white px-4 py-1.5 rounded text-sm font-bold shadow hover:bg-red-600 transition flex items-center gap-1">
                    🗑️ ลบทั้งหมด
                </button>
            </div>
            
            <div id="previewZone" class="flex flex-wrap gap-4 p-6 border-2 border-dashed rounded-lg w-full justify-center min-h-[150px]" :class="isDarkMode ? 'border-gray-600 bg-gray-900' : 'border-gray-300 bg-gray-50'">
                <span class="opacity-50 my-auto text-center font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-500'">เมื่อกดปุ่ม "🚀 สร้างรูปทั้งหมด"<br>รูปพรีวิวทั้งหมดจะมาแสดงที่นี่ครับ</span>
            </div>
        </div>

        <!-- ฝั่งขวา: แผงควบคุม (Accordion) -->
        <div class="controls-container w-[400px] p-6 rounded-xl shadow-lg max-h-[85vh] overflow-y-auto flex flex-col gap-4 transition-colors relative" :class="isDarkMode ? 'bg-gray-800' : 'bg-white'" @change="draw()" @input="draw()">
            <h3 class="text-xl font-bold m-0 text-blue-500 py-2 border-b mb-2" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">⚙️ แผงควบคุม</h3>
            
            <!-- ====== ระบบจัดการรูปแบบ ====== -->
            <div class="p-4 rounded-lg border shadow-sm mb-2 transition-colors" :class="isDarkMode ? 'bg-indigo-900/30 border-indigo-700' : 'bg-indigo-50 border-indigo-200'">
                <label class="block text-sm font-bold mb-2" :class="isDarkMode ? 'text-indigo-300' : 'text-indigo-800'">💾 จัดการรูปแบบที่บันทึกไว้:</label>
                <div class="flex gap-2 mb-3">
                    <select id="formatSelect" class="flex-1 p-2 border rounded text-sm font-bold focus:outline-indigo-500" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-indigo-300'">
                        <option value="NEW">➕ สร้างรูปแบบใหม่</option>
                    </select>
                    <button @click="loadSelectedFormat" class="bg-indigo-600 text-white px-3 py-1 rounded text-sm font-bold shadow hover:bg-indigo-700 transition">โหลด</button>
                    <button @click="deleteSelectedFormat" class="bg-red-500 text-white px-3 py-1 rounded text-sm font-bold shadow hover:bg-red-600 transition">ลบ</button>
                </div>
                
                <div class="flex gap-2">
                    <button @click="saveFormatToDB" class="flex-1 bg-green-600 text-white py-2 rounded font-bold hover:bg-green-700 transition shadow text-sm">💾 บันทึกการตั้งค่าทั้งหมด</button>
                    <button @click="resetFormat" class="bg-gray-500 text-white px-4 py-2 rounded font-bold hover:bg-gray-600 transition shadow text-sm" title="เคลียร์ค่าทุกอย่างกลับเป็นค่าเริ่มต้น">🔄 รีเซ็ต</button>
                </div>
            </div>

            <!-- หมวดหมู่แบบ Combobox (Accordion) -->
            <div class="flex flex-col gap-3">
                
                <!-- 1. รูปภาพ -->
                <div class="border rounded-lg overflow-hidden transition-colors" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                    <div @click="openSection = 1" class="p-3 cursor-pointer flex justify-between items-center font-bold transition-colors" :class="openSection === 1 ? 'bg-blue-600 text-white' : (isDarkMode ? 'bg-gray-700 text-gray-200 hover:bg-gray-600' : 'bg-gray-200 text-gray-700 hover:bg-gray-300')">
                        <span>1. 🏞️ รูปภาพ (Background & Logo)</span>
                        <span>{{ openSection === 1 ? '▲' : '▼' }}</span>
                    </div>
                    <div v-show="openSection === 1" class="p-4 space-y-3 text-sm" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
                        <div class="flex items-center justify-between border-b pb-2" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                            <label class="flex items-center gap-2 font-bold cursor-pointer text-green-500"><input type="checkbox" id="showBg" checked class="w-4 h-4 cursor-pointer"> เปิดใช้ Background</label>
                            <label class="flex items-center gap-2 font-bold cursor-pointer text-blue-500"><input type="checkbox" id="showLogo" checked class="w-4 h-4 cursor-pointer"> เปิดใช้ Logo</label>
                        </div>
                        <div>
                            <label class="block font-bold mt-2">อัปโหลด Background:</label>
                            <input type="file" id="bgUpload" accept="image/*" class="w-full mt-1">
                        </div>
                        <div>
                            <label class="block font-bold mt-2">อัปโหลด Logo:</label>
                            <input type="file" id="logoUpload" accept="image/*" class="w-full mt-1">
                        </div>
                        <div class="text-center mt-2">
                            <button class="bg-gray-500 text-white text-xs px-3 py-1.5 rounded hover:bg-gray-600 shadow" @click="centerElement('logo')">📍 จัด Logo ให้อยู่กึ่งกลาง</button>
                        </div>
                        <div class="p-2 border rounded" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                            <label class="block font-bold">ตำแหน่ง Logo X (แนวนอน):</label><input type="range" id="logoX" min="0" max="600" value="480" class="w-full cursor-pointer">
                            <label class="block font-bold mt-2">ตำแหน่ง Logo Y (แนวตั้ง):</label><input type="range" id="logoY" min="0" max="600" value="90" class="w-full cursor-pointer">
                            <label class="block font-bold mt-2 text-indigo-500">ขนาด Logo: <span id="logoScaleVal">37</span>%</label><input type="range" id="logoScale" min="10" max="300" value="37" class="w-full cursor-pointer">
                        </div>
                    </div>
                </div>

                <!-- 2. หัวข้อ -->
                <div class="border rounded-lg overflow-hidden transition-colors" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                    <div @click="openSection = 2" class="p-3 cursor-pointer flex justify-between items-center font-bold transition-colors" :class="openSection === 2 ? 'bg-purple-600 text-white' : (isDarkMode ? 'bg-gray-700 text-gray-200 hover:bg-gray-600' : 'bg-gray-200 text-gray-700 hover:bg-gray-300')">
                        <span>2. 📝 รายชื่อหัวข้อ & ฟอนต์</span>
                        <span>{{ openSection === 2 ? '▲' : '▼' }}</span>
                    </div>
                    <div v-show="openSection === 2" class="p-4 space-y-3 text-sm" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
                        <div id="lotterySelector" class="border rounded p-2 max-h-[250px] overflow-y-auto mt-1" :class="isDarkMode ? 'border-gray-700 bg-gray-800' : 'border-gray-300 bg-white'"></div>
                        
                        <div class="flex justify-between items-center gap-2 mt-3">
                            <div class="flex-1">
                                <label class="block font-bold">เลือกฟอนต์:</label>
                                <select id="headerFontFamily" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'">
                                    <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                                </select>
                            </div>
                            <div class="flex-1">
                                <label class="block font-bold">สไตล์:</label>
                                <div class="flex gap-2 mt-2">
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="headerFontBold" class="mr-1 w-4 h-4 cursor-pointer"> หนา</label>
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="headerFontItalic" class="mr-1 w-4 h-4 cursor-pointer"> เอียง</label>
                                </div>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-2 mt-2">
                            <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="headerFontSize" value="50" min="10" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold">สีตัวอักษร:</label><input type="color" id="headerColor" value="#000000" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                            <div><label class="block font-bold mt-1">ความหนาขอบ:</label><input type="number" id="headerStrokeWidth" value="0" min="0" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="headerStrokeColor" value="#FFFFFF" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                        </div>
                        
                        <div class="text-center mt-3 border-t pt-3" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                            <button class="bg-gray-500 text-white text-xs px-3 py-1.5 rounded hover:bg-gray-600 shadow" @click="centerElement('header')">📍 จัดหัวข้อกึ่งกลาง</button>
                        </div>
                        <label class="block font-bold mt-2">ตำแหน่ง X:</label><input type="range" id="headerX" min="0" max="600" value="300" class="w-full cursor-pointer">
                        <label class="block font-bold mt-2">ตำแหน่ง Y:</label><input type="range" id="headerY" min="0" max="600" value="100" class="w-full cursor-pointer">
                    </div>
                </div>
                
                <!-- 3. วันที่ -->
                <div class="border rounded-lg overflow-hidden transition-colors" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                    <div @click="openSection = 3" class="p-3 cursor-pointer flex justify-between items-center font-bold transition-colors" :class="openSection === 3 ? 'bg-teal-600 text-white' : (isDarkMode ? 'bg-gray-700 text-gray-200 hover:bg-gray-600' : 'bg-gray-200 text-gray-700 hover:bg-gray-300')">
                        <span>3. 📅 ตั้งค่าวันที่</span>
                        <span>{{ openSection === 3 ? '▲' : '▼' }}</span>
                    </div>
                    <div v-show="openSection === 3" class="p-4 space-y-3 text-sm" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
                        <div>
                            <label class="block font-bold">เลือกวันที่:</label>
                            <input type="date" id="datePicker" value="2024-11-16" class="w-full p-2 border rounded mt-1 cursor-pointer" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'">
                        </div>
                        <div class="flex justify-between items-center gap-2 mt-2">
                            <div class="flex-1">
                                <label class="block font-bold">เลือกฟอนต์:</label>
                                <select id="dateFontFamily" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'">
                                    <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                                </select>
                            </div>
                            <div class="flex-1">
                                <label class="block font-bold">สไตล์:</label>
                                <div class="flex gap-2 mt-2">
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="dateFontBold" class="mr-1 w-4 h-4 cursor-pointer"> หนา</label>
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="dateFontItalic" class="mr-1 w-4 h-4 cursor-pointer"> เอียง</label>
                                </div>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-2 mt-2">
                            <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="dateFontSize" value="45" min="10" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold">สีตัวอักษร:</label><input type="color" id="dateColor" value="#000000" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                            <div><label class="block font-bold mt-1">ความหนาขอบ:</label><input type="number" id="dateStrokeWidth" value="3" min="0" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="dateStrokeColor" value="#FFD700" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                        </div>
                        <div class="text-center mt-3 border-t pt-3" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                            <button class="bg-gray-500 text-white text-xs px-3 py-1.5 rounded hover:bg-gray-600 shadow" @click="centerElement('date')">📍 จัดวันที่กึ่งกลาง</button>
                        </div>
                        <label class="block font-bold mt-2">ตำแหน่ง X:</label><input type="range" id="dateX" min="0" max="600" value="300" class="w-full cursor-pointer">
                        <label class="block font-bold mt-2">ตำแหน่ง Y:</label><input type="range" id="dateY" min="0" max="600" value="530" class="w-full cursor-pointer">
                    </div>
                </div>

                <!-- 4. เลข 3 ตัว -->
                <div class="border rounded-lg overflow-hidden transition-colors" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                    <div @click="openSection = 4" class="p-3 cursor-pointer flex justify-between items-center font-bold transition-colors" :class="openSection === 4 ? 'bg-yellow-500 text-white' : (isDarkMode ? 'bg-gray-700 text-gray-200 hover:bg-gray-600' : 'bg-gray-200 text-gray-700 hover:bg-gray-300')">
                        <span>4. 🎰 เลข 3 ตัว</span>
                        <span>{{ openSection === 4 ? '▲' : '▼' }}</span>
                    </div>
                    <div v-show="openSection === 4" class="p-4 space-y-3 text-sm" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
                        <div class="flex justify-between gap-2">
                            <div class="flex-1"><label class="block font-bold">จำนวนแถว:</label><input type="number" id="row3Count" value="1" min="0" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div class="flex-1"><label class="block font-bold">จำนวนคอลัมน์:</label><input type="number" id="col3Count" value="3" min="1" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                        </div>
                        <div class="flex justify-between items-center gap-2 mt-2">
                            <div class="flex-1">
                                <label class="block font-bold">เลือกฟอนต์:</label>
                                <select id="num3FontFamily" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'">
                                    <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                                </select>
                            </div>
                            <div class="flex-1">
                                <label class="block font-bold">สไตล์:</label>
                                <div class="flex gap-2 mt-2">
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="num3FontBold" class="mr-1 w-4 h-4 cursor-pointer"> หนา</label>
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="num3FontItalic" class="mr-1 w-4 h-4 cursor-pointer"> เอียง</label>
                                </div>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-2 mt-2">
                            <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="num3FontSize" value="50" min="10" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold">สีอักษร:</label><input type="color" id="num3Color" value="#FFD700" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                            <div><label class="block font-bold mt-1">ขอบหนา:</label><input type="number" id="num3StrokeWidth" value="3" min="0" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="num3StrokeColor" value="#000000" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                        </div>
                        <div class="flex justify-between gap-4 mt-3 p-3 border rounded" :class="isDarkMode ? 'border-gray-700 bg-gray-800' : 'border-gray-300 bg-white'">
                            <div class="flex-1"><label class="block font-bold text-red-500">ช่องไฟ ↔ (X):</label><input type="range" id="num3GapX" min="30" max="300" value="110" class="w-full cursor-pointer mt-2"></div>
                            <div class="flex-1"><label class="block font-bold text-green-500">ช่องไฟ ↕ (Y):</label><input type="range" id="num3GapY" min="30" max="200" value="70" class="w-full cursor-pointer mt-2"></div>
                        </div>
                        <div class="text-center mt-3 border-t pt-3" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                            <button class="bg-gray-500 text-white text-xs px-3 py-1.5 rounded hover:bg-gray-600 shadow" @click="centerElement('num3')">📍 จัดกลุ่มกึ่งกลาง</button>
                        </div>
                        <label class="block font-bold mt-2">ตำแหน่งเริ่ม X:</label><input type="range" id="num3X" min="0" max="600" value="190" class="w-full cursor-pointer">
                        <label class="block font-bold mt-2">ตำแหน่งเริ่ม Y:</label><input type="range" id="num3Y" min="0" max="600" value="450" class="w-full cursor-pointer">
                    </div>
                </div>

                <!-- 5. เลข 2 ตัว -->
                <div class="border rounded-lg overflow-hidden transition-colors" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                    <div @click="openSection = 5" class="p-3 cursor-pointer flex justify-between items-center font-bold transition-colors" :class="openSection === 5 ? 'bg-orange-500 text-white' : (isDarkMode ? 'bg-gray-700 text-gray-200 hover:bg-gray-600' : 'bg-gray-200 text-gray-700 hover:bg-gray-300')">
                        <span>5. 🎲 เลข 2 ตัว</span>
                        <span>{{ openSection === 5 ? '▲' : '▼' }}</span>
                    </div>
                    <div v-show="openSection === 5" class="p-4 space-y-3 text-sm" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
                        <div class="flex justify-between gap-2">
                            <div class="flex-1"><label class="block font-bold">จำนวนแถว:</label><input type="number" id="row2Count" value="2" min="0" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div class="flex-1"><label class="block font-bold">จำนวนคอลัมน์:</label><input type="number" id="col2Count" value="2" min="1" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                        </div>
                        <div class="flex justify-between items-center gap-2 mt-2">
                            <div class="flex-1">
                                <label class="block font-bold">เลือกฟอนต์:</label>
                                <select id="num2FontFamily" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'">
                                    <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                                </select>
                            </div>
                            <div class="flex-1">
                                <label class="block font-bold">สไตล์:</label>
                                <div class="flex gap-2 mt-2">
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="num2FontBold" class="mr-1 w-4 h-4 cursor-pointer"> หนา</label>
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="num2FontItalic" class="mr-1 w-4 h-4 cursor-pointer"> เอียง</label>
                                </div>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-2 mt-2">
                            <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="num2FontSize" value="50" min="10" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold">สีอักษร:</label><input type="color" id="num2Color" value="#FFD700" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                            <div><label class="block font-bold mt-1">ขอบหนา:</label><input type="number" id="num2StrokeWidth" value="3" min="0" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="num2StrokeColor" value="#000000" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                        </div>
                        <div class="flex justify-between gap-4 mt-3 p-3 border rounded" :class="isDarkMode ? 'border-gray-700 bg-gray-800' : 'border-gray-300 bg-white'">
                            <div class="flex-1"><label class="block font-bold text-red-500">ช่องไฟ ↔ (X):</label><input type="range" id="num2GapX" min="30" max="300" value="110" class="w-full cursor-pointer mt-2"></div>
                            <div class="flex-1"><label class="block font-bold text-green-500">ช่องไฟ ↕ (Y):</label><input type="range" id="num2GapY" min="30" max="200" value="70" class="w-full cursor-pointer mt-2"></div>
                        </div>
                        <div class="text-center mt-3 border-t pt-3" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                            <button class="bg-gray-500 text-white text-xs px-3 py-1.5 rounded hover:bg-gray-600 shadow" @click="centerElement('num2')">📍 จัดกลุ่มกึ่งกลาง</button>
                        </div>
                        <label class="block font-bold mt-2">ตำแหน่งเริ่ม X:</label><input type="range" id="num2X" min="0" max="600" value="245" class="w-full cursor-pointer">
                        <label class="block font-bold mt-2">ตำแหน่งเริ่ม Y:</label><input type="range" id="num2Y" min="0" max="600" value="280" class="w-full cursor-pointer">
                    </div>
                </div>

                <!-- 6. เลข 1 ตัว (เลขรูด) -->
                <div class="border rounded-lg overflow-hidden transition-colors" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                    <div @click="openSection = 6" class="p-3 cursor-pointer flex justify-between items-center font-bold transition-colors" :class="openSection === 6 ? 'bg-red-500 text-white' : (isDarkMode ? 'bg-gray-700 text-gray-200 hover:bg-gray-600' : 'bg-gray-200 text-gray-700 hover:bg-gray-300')">
                        <span>6. 🎯 เลข 1 ตัว (เลขรูด)</span>
                        <span>{{ openSection === 6 ? '▲' : '▼' }}</span>
                    </div>
                    <div v-show="openSection === 6" class="p-4 space-y-3 text-sm" :class="isDarkMode ? 'bg-gray-900/50' : 'bg-gray-50'">
                        <div class="flex justify-between gap-2">
                            <div class="flex-1"><label class="block font-bold">จำนวนแถว:</label><input type="number" id="row1Count" value="1" min="0" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div class="flex-1"><label class="block font-bold">จำนวนคอลัมน์:</label><input type="number" id="col1Count" value="2" min="1" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                        </div>
                        <div class="flex justify-between items-center gap-2 mt-2">
                            <div class="flex-1">
                                <label class="block font-bold">เลือกฟอนต์:</label>
                                <select id="num1FontFamily" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'">
                                    <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                                </select>
                            </div>
                            <div class="flex-1">
                                <label class="block font-bold">สไตล์:</label>
                                <div class="flex gap-2 mt-2">
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="num1FontBold" class="mr-1 w-4 h-4 cursor-pointer"> หนา</label>
                                    <label class="flex items-center cursor-pointer"><input type="checkbox" id="num1FontItalic" class="mr-1 w-4 h-4 cursor-pointer"> เอียง</label>
                                </div>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-2 mt-2">
                            <div><label class="block font-bold">ขนาดฟอนต์:</label><input type="number" id="num1FontSize" value="50" min="10" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold">สีอักษร:</label><input type="color" id="num1Color" value="#FFD700" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                            <div><label class="block font-bold mt-1">ขอบหนา:</label><input type="number" id="num1StrokeWidth" value="3" min="0" class="w-full p-1 border rounded mt-1" :class="isDarkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white'"></div>
                            <div><label class="block font-bold mt-1">สีขอบ:</label><input type="color" id="num1StrokeColor" value="#000000" class="w-full h-[32px] p-0 border rounded cursor-pointer mt-1"></div>
                        </div>
                        <div class="flex justify-between gap-4 mt-3 p-3 border rounded" :class="isDarkMode ? 'border-gray-700 bg-gray-800' : 'border-gray-300 bg-white'">
                            <div class="flex-1"><label class="block font-bold text-red-500">ช่องไฟ ↔ (X):</label><input type="range" id="num1GapX" min="30" max="300" value="80" class="w-full cursor-pointer mt-2"></div>
                            <div class="flex-1"><label class="block font-bold text-green-500">ช่องไฟ ↕ (Y):</label><input type="range" id="num1GapY" min="30" max="200" value="70" class="w-full cursor-pointer mt-2"></div>
                        </div>
                        <div class="text-center mt-3 border-t pt-3" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
                            <button class="bg-gray-500 text-white text-xs px-3 py-1.5 rounded hover:bg-gray-600 shadow" @click="centerElement('num1')">📍 จัดกลุ่มกึ่งกลาง</button>
                        </div>
                        <label class="block font-bold mt-2">ตำแหน่งเริ่ม X:</label><input type="range" id="num1X" min="0" max="600" value="260" class="w-full cursor-pointer">
                        <label class="block font-bold mt-2">ตำแหน่งเริ่ม Y:</label><input type="range" id="num1Y" min="0" max="600" value="180" class="w-full cursor-pointer">
                    </div>
                </div>
            </div>
            
            <hr class="mt-4" :class="isDarkMode ? 'border-gray-700' : 'border-gray-300'">
            <button class="bg-green-600 text-white py-4 rounded-lg font-bold text-xl shadow-lg hover:bg-green-700 hover:scale-[1.02] transition-transform w-full" @click="generateBatchPreviews">🚀 สร้างรูปทั้งหมด</button>
            <button id="downloadZipBtn" class="bg-yellow-400 text-gray-800 py-3 rounded-lg font-bold text-lg shadow hover:bg-yellow-500 transition hidden w-full" @click="downloadZip">📥 ดาวน์โหลดไฟล์ ZIP</button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useHead, useState } from '#imports'

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

let canvas = null;
let ctx = null;
let numbers3Grid = [];
let numbers2Grid = [];
let numbers1Grid = [];
let bgImage = null;
let logoImage = null;
let generatedImagesToZip = [];
let savedFormatsList = []; 

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
        sel.innerHTML = '<option value="NEW">➕ สร้างรูปแบบใหม่</option>';
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
    if(sel === 'NEW') return alert('กรุณาเลือกชื่อรูปแบบด้านซ้ายก่อนโหลดครับ');
    
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

        // 🛠️ ท่าไม้ตายแก้บั๊กฟอนต์โหลดไม่ทัน
        setTimeout(() => {
            draw(); // วาดรอบที่ 1: กระตุ้นให้เบราว์เซอร์รู้จักและเริ่มดาวน์โหลดไฟล์ฟอนต์
            setTimeout(draw, 500); // วาดรอบที่ 2: หน่วงเวลา 0.5 วินาที เพื่อวาดทับอีกครั้งตอนฟอนต์มาแล้ว
        }, 50);

        alert(`โหลดรูปแบบ '${sel}' เสร็จสิ้น!`);
    }
}

const clearAllPreviews = () => {
    if (generatedImagesToZip.length === 0) {
        alert('ยังไม่มีรูปภาพพรีวิวให้ลบครับ');
        return;
    }
    if (!confirm('⚠️ คุณแน่ใจหรือไม่ว่าต้องการเคลียร์รูปพรีวิวทั้งหมดทิ้ง?')) return;
    
    generatedImagesToZip = [];
    const previewZone = document.getElementById('previewZone');
    if (previewZone) {
        previewZone.innerHTML = `<span class="opacity-50 my-auto text-center font-bold ${isDarkMode.value ? 'text-white' : 'text-gray-500'}">เมื่อกดปุ่ม "🚀 สร้างรูปทั้งหมด"<br>รูปพรีวิวทั้งหมดจะมาแสดงที่นี่ครับ</span>`;
    }
    document.getElementById('downloadZipBtn').classList.add('hidden');
}

const deleteSelectedFormat = async () => {
    const token = localStorage.getItem('token');
    const sel = document.getElementById('formatSelect').value;
    
    if(sel === 'NEW') return alert('ไม่สามารถลบรายการนี้ได้ กรุณาเลือกรูปแบบที่บันทึกไว้ครับ');
    if(!confirm(`⚠️ คุณแน่ใจหรือไม่ว่าต้องการลบรูปแบบ '${sel}' ทิ้ง?\n(การกระทำนี้ไม่สามารถกู้คืนได้)`)) return;
    
    try {
        const res = await fetch(`https://gen-picture-hwy.onrender.com/formats/${encodeURIComponent(sel)}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if(res.ok) {
            alert('ลบรูปแบบสำเร็จ!');
            await fetchFormats();
            document.getElementById('formatSelect').value = 'NEW';
        } else {
            alert('เกิดข้อผิดพลาดในการลบ');
        }
    } catch(e) {
        console.error(e);
    }
}

const saveFormatToDB = async () => {
    const token = localStorage.getItem('token');
    const sel = document.getElementById('formatSelect').value;
    let formatName = sel;

    if(sel === 'NEW') {
        formatName = prompt('กรุณาตั้งชื่อรูปแบบใหม่ของคุณ:');
        if(!formatName) return; 
    }

    let settings = {};
    settingInputs.forEach(id => {
        const el = document.getElementById(id);
        if(el) settings[id] = el.type === 'checkbox' ? el.checked : el.value;
    });
    settings['selectedHeaders'] = getSelectedHeaders();
    
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
            alert(data.message);
            await fetchFormats(); 
            document.getElementById('formatSelect').value = formatName; 
        } else {
            alert('❌ ' + data.detail);
        }
    } catch(e) {
        alert('ไม่สามารถเชื่อมต่อฐานข้อมูลได้');
    }
}

const resetFormat = () => {
    if(!confirm('⚠️ คุณแน่ใจหรือไม่ที่จะ "รีเซ็ต" การตั้งค่าปัจจุบันทั้งหมดให้กลับเป็นค่าเริ่มต้น?')) return;
    localStorage.removeItem('lotterySettings'); 
    window.location.reload(); 
}

const renderLotterySelector = () => {
    const container = document.getElementById('lotterySelector');
    if(!container) return;
    container.innerHTML = '';
    for (const [category, items] of Object.entries(lotteryData)) {
        const catDiv = document.createElement('div');
        catDiv.className = 'mb-1 lottery-category';
        const catHeader = document.createElement('div');
        catHeader.className = 'flex items-center justify-between bg-gray-400/20 p-2 rounded cursor-pointer hover:bg-gray-400/40 transition-colors';
        
        const catLabel = document.createElement('label');
        catLabel.className = 'font-bold text-blue-500 flex items-center cursor-pointer text-sm m-0 flex-1';
        const catCb = document.createElement('input');
        catCb.type = 'checkbox';
        catCb.className = 'mr-2 cursor-pointer w-4 h-4 cat-cb';
        catLabel.appendChild(catCb);
        catLabel.appendChild(document.createTextNode(' ' + category));
        
        const toggleBtn = document.createElement('span');
        toggleBtn.className = 'text-xs text-gray-500 p-1 px-3 bg-gray-400/20 rounded hover:bg-gray-400/50 transition font-bold';
        toggleBtn.innerHTML = '▼ เปิด'; 
        
        catHeader.appendChild(catLabel);
        catHeader.appendChild(toggleBtn);
        catDiv.appendChild(catHeader);
        
        const subDiv = document.createElement('div');
        subDiv.className = 'sub-items flex flex-col p-2 bg-transparent border border-t-0 rounded-b border-gray-400/30';
        subDiv.style.display = 'none'; 
        
        items.forEach(item => {
            const subLabel = document.createElement('label');
            subLabel.className = 'font-normal text-xs flex items-center mt-1 cursor-pointer';
            const subCb = document.createElement('input');
            subCb.type = 'checkbox';
            subCb.className = 'mr-2 cursor-pointer w-3 h-3 sub-cb';
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
            setTimeout(draw, 50);
        });
        
        subDiv.querySelectorAll('.sub-cb').forEach(cb => {
            cb.addEventListener('change', function() {
                updateCategoryCheckboxes();
                setTimeout(draw, 50);
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

const handleImageUpload = (e, type) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            if (type === 'bg') bgImage = img;
            if (type === 'logo') logoImage = img;
            setTimeout(draw, 50);
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(file);
}

const createNumbersArray = (rows, cols, digitsCount) => {
    let grid = [];
    for (let i = 0; i < rows; i++) {
        let row = [];
        for (let j = 0; j < cols; j++) {
            if (digitsCount === 3) {
                row.push(Math.floor(Math.random() * 1000).toString().padStart(3, '0'));
            } else if (digitsCount === 2) {
                row.push(Math.floor(Math.random() * 100).toString().padStart(2, '0'));
            } else if (digitsCount === 1) {
                row.push((Math.floor(Math.random() * 9) + 1).toString());
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
    setTimeout(draw, 50);
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
    setTimeout(draw, 50);
}

const getFontString = (idPrefix, fontSize) => {
    const family = document.getElementById(idPrefix + 'FontFamily').value;
    const isBold = document.getElementById(idPrefix + 'FontBold').checked ? 'bold' : 'normal';
    const isItalic = document.getElementById(idPrefix + 'FontItalic').checked ? 'italic' : 'normal';
    return `${isItalic} ${isBold} ${fontSize}px "${family}", sans-serif`;
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

const generateBatchPreviews = () => {
    const previewZone = document.getElementById('previewZone');
    previewZone.innerHTML = ''; 
    generatedImagesToZip = []; 
    
    const headers = getSelectedHeaders();
    if(headers.length === 0) return alert("กรุณาติ๊กเลือกชื่อหัวข้ออย่างน้อย 1 ชื่อครับ");

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
        div.className = 'relative flex flex-col items-center font-bold text-xs';
        
        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = '✖';
        removeBtn.className = 'absolute -top-2 -right-2 bg-red-500 text-white border-none rounded-full w-5 h-5 text-[10px] cursor-pointer shadow hover:bg-red-600 flex items-center justify-center';
        removeBtn.onclick = function() {
            div.remove();
            generatedImagesToZip = generatedImagesToZip.filter(img => img.fileName !== headerName);
            if (generatedImagesToZip.length === 0) document.getElementById('downloadZipBtn').classList.add('hidden');
        };

        const img = document.createElement('img');
        img.src = dataUrl;
        img.className = 'w-[100px] border border-gray-300 rounded shadow-sm mb-1';
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
    document.querySelectorAll('input, select').forEach(el => {
        if(el.type !== 'file' && !el.classList.contains('sub-cb') && !el.classList.contains('cat-cb') && el.id !== 'formatSelect') {
            el.addEventListener('input', () => { setTimeout(draw, 50); });
            if (el.type === 'checkbox' || el.tagName.toLowerCase() === 'select') {
                el.addEventListener('change', () => { setTimeout(draw, 50); });
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
    
    document.fonts.ready.then(() => {
        const defBg = new Image();
        defBg.src = '/img/default-bg.png';
        defBg.onload = () => { bgImage = defBg; setTimeout(draw, 50); };

        const defLogo = new Image();
        defLogo.src = '/img/default-logo.png';
        defLogo.onload = () => { logoImage = defLogo; setTimeout(draw, 50); };
        
        setTimeout(draw, 50); 
    });

    isLoading.value = false;
})
</script>