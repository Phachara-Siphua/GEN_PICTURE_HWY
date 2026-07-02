<template>
  <div class="p-6">
    <div v-if="isExpired" class="flex flex-col items-center justify-center h-[80vh]">
        <div class="bg-white p-10 rounded-lg shadow-xl text-center max-w-lg border-t-4 border-red-500">
            <div class="text-7xl mb-4">⚠️</div>
            <h2 class="text-3xl font-bold text-red-600 mb-2">แพ็กเกจหมดอายุแล้ว</h2>
            <p class="text-gray-700 mb-4 text-lg">บัญชีของคุณหมดอายุเมื่อเวลา<br><strong class="text-xl text-red-500">{{ expireDateStr }}</strong></p>
            <p class="text-gray-500 text-sm mb-6">ไม่สามารถใช้งานหน้าสร้างรูปได้ กรุณาติดต่อแอดมินเพื่อทำการต่ออายุแพ็กเกจครับ</p>
            <a href="https://line.me/ti/p/~@yourline" target="_blank" class="inline-block bg-green-500 text-white px-8 py-3 rounded-full font-bold hover:bg-green-600 transition shadow-md text-lg">💬 ติดต่อแอดมินผ่าน Line</a>
        </div>
    </div>

    <div v-show="!isExpired" id="mainApp" class="flex flex-wrap gap-6 w-full max-w-[1200px] mx-auto">
        
        <!-- ฝั่งซ้าย: พรีวิว -->
        <div class="canvas-container flex-1 flex flex-col items-center bg-white p-6 rounded-lg shadow-md min-w-[300px]">
            <h3 class="text-xl font-bold mb-4 text-gray-700">👁️ ภาพพรีวิว</h3>
            <canvas id="myCanvas" width="600" height="600" class="w-full max-w-[450px] h-auto border border-gray-300 shadow-lg rounded"></canvas>
            
            <button class="mt-4 bg-teal-500 text-white py-3 px-6 rounded-lg font-bold shadow hover:bg-teal-600 transition w-full max-w-[450px]" @click="generatePreviewNumbers">🎲 สุ่มตัวเลข 1 ชุด (ดูตัวอย่าง)</button>

            <div class="flex justify-between items-center mt-8 mb-2 border-b-2 border-gray-100 w-full pb-2">
                <h3 class="text-lg font-bold text-gray-700 m-0">🖼️ พรีวิวรูปภาพทั้งหมด</h3>
                <button @click="clearAllPreviews" class="bg-red-500 text-white px-3 py-1 rounded text-sm font-bold shadow hover:bg-red-600 transition flex items-center gap-1">
                    🗑️ ลบทั้งหมด
                </button>
            </div>
            
            <div id="previewZone" class="flex flex-wrap gap-4 p-4 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 w-full justify-center">
                <span class="text-gray-400">กดปุ่ม "🚀 สร้างรูปทั้งหมด" เพื่อดูพรีวิวที่นี่</span>
            </div>
        </div>

        <!-- ฝั่งขวา: แผงควบคุม -->
        <div class="controls-container w-[380px] bg-white p-6 rounded-lg shadow-md max-h-[85vh] overflow-y-auto flex flex-col gap-4">
            <h3 class="text-xl font-bold m-0 text-blue-600">⚙️ แผงควบคุม</h3>
            
            <!-- ====== ระบบ Combobox ====== -->
            <div class="bg-indigo-50 p-4 rounded-lg border border-indigo-200 mb-2">
                <label class="block text-xs font-bold text-indigo-800 mb-2">จัดการรูปแบบที่บันทึกไว้:</label>
                <div class="flex gap-2 mb-3">
                    <select id="formatSelect" class="flex-1 p-2 border border-indigo-300 rounded text-sm focus:outline-indigo-500 bg-white">
                        <option value="NEW">➕ สร้างรูปแบบใหม่</option>
                    </select>
                    <button @click="loadSelectedFormat" class="bg-indigo-600 text-white px-3 py-1 rounded text-sm font-bold shadow hover:bg-indigo-700 transition">โหลด</button>
                    <button @click="deleteSelectedFormat" class="bg-red-500 text-white px-3 py-1 rounded text-sm font-bold shadow hover:bg-red-600 transition">ลบ</button>
                </div>
                
                <div class="flex gap-2">
                    <button @click="saveFormatToDB" class="flex-1 bg-green-600 text-white py-2 rounded font-bold hover:bg-green-700 transition shadow">💾 บันทึก / อัปเดต</button>
                    <button @click="resetFormat" class="bg-gray-500 text-white px-4 py-2 rounded font-bold hover:bg-gray-600 transition shadow" title="เคลียร์ค่าทุกอย่างกลับเป็นค่าเริ่มต้น">🔄 รีเซ็ต</button>
                </div>
            </div>

            <!-- 1. รูปภาพ -->
            <div class="border border-gray-200 p-3 rounded-lg bg-gray-50">
                <h4 class="mt-0 mb-2 text-gray-700 font-bold border-b pb-1">1. รูปภาพ (Background & Logo)</h4>
                <label class="block text-xs font-bold text-gray-600 mt-2">อัปโหลด Background:</label>
                <input type="file" id="bgUpload" accept="image/*" class="w-full mt-1 text-sm">
                <label class="block text-xs font-bold text-gray-600 mt-2">อัปโหลด Logo:</label>
                <input type="file" id="logoUpload" accept="image/*" class="w-full mt-1 text-sm">
                <div class="text-center mt-2">
                    <button class="bg-gray-500 text-white text-xs px-2 py-1 rounded hover:bg-gray-600" @click="centerElement('logo')">📍 จัด Logo กึ่งกลาง</button>
                </div>
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง Logo X:</label>
                <input type="range" id="logoX" min="0" max="600" value="480" class="w-full cursor-pointer">
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง Logo Y:</label>
                <input type="range" id="logoY" min="0" max="600" value="90" class="w-full cursor-pointer">
                <label class="block text-xs font-bold text-gray-600 mt-2">ขนาด Logo: <span id="logoScaleVal">37</span>%</label>
                <input type="range" id="logoScale" min="10" max="300" value="37" class="w-full cursor-pointer">
            </div>

            <div class="border border-gray-200 p-3 rounded-lg bg-gray-50">
                <h4 class="mt-0 mb-2 text-gray-700 font-bold border-b pb-1">2. รายชื่อหัวข้อ (แบบติ๊กเลือก)</h4>
                <div id="lotterySelector" class="border border-gray-300 rounded p-2 max-h-[250px] overflow-y-auto bg-white mt-1"></div>
                
                <div class="flex justify-between items-center gap-2 mt-3">
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">เลือกฟอนต์:</label>
                        <select id="headerFontFamily" class="w-full p-1 border rounded text-sm mt-1">
                            <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                        </select>
                    </div>
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">สไตล์:</label>
                        <div class="flex gap-2 mt-1">
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="headerFontBold" checked class="mr-1"> หนา</label>
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="headerFontItalic" class="mr-1"> เอียง</label>
                        </div>
                    </div>
                </div>

                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ขนาดฟอนต์:</label><input type="number" id="headerFontSize" value="50" min="10" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีตัวอักษร:</label><input type="color" id="headerColor" value="#000000" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ความหนาขอบ:</label><input type="number" id="headerStrokeWidth" value="0" min="0" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีขอบ:</label><input type="color" id="headerStrokeColor" value="#FFFFFF" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="text-center mt-2">
                    <button class="bg-gray-500 text-white text-xs px-2 py-1 rounded hover:bg-gray-600" @click="centerElement('header')">📍 จัดหัวข้อกึ่งกลาง</button>
                </div>
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง X:</label><input type="range" id="headerX" min="0" max="600" value="300" class="w-full cursor-pointer">
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง Y:</label><input type="range" id="headerY" min="0" max="600" value="100" class="w-full cursor-pointer">
            </div>
            
            <div class="border border-gray-200 p-3 rounded-lg bg-gray-50">
                <h4 class="mt-0 mb-2 text-gray-700 font-bold border-b pb-1">3. ตั้งค่าวันที่</h4>
                <div>
                    <label class="block text-xs font-bold text-gray-600">เลือกวันที่:</label>
                    <!-- ค่าเริ่มต้นให้เป็น 2024-11-16 ตามในรูป -->
                    <input type="date" id="datePicker" value="2024-11-16" class="w-full p-1 border rounded text-sm mt-1 cursor-pointer">
                </div>

                <div class="flex justify-between items-center gap-2 mt-2">
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">เลือกฟอนต์:</label>
                        <select id="dateFontFamily" class="w-full p-1 border rounded text-sm mt-1">
                            <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                        </select>
                    </div>
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">สไตล์:</label>
                        <div class="flex gap-2 mt-1">
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="dateFontBold" checked class="mr-1"> หนา</label>
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="dateFontItalic" class="mr-1"> เอียง</label>
                        </div>
                    </div>
                </div>

                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ขนาดฟอนต์:</label><input type="number" id="dateFontSize" value="45" min="10" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีตัวอักษร:</label><input type="color" id="dateColor" value="#000000" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ความหนาขอบ:</label><input type="number" id="dateStrokeWidth" value="3" min="0" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีขอบ:</label><input type="color" id="dateStrokeColor" value="#FFD700" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="text-center mt-2">
                    <button class="bg-gray-500 text-white text-xs px-2 py-1 rounded hover:bg-gray-600" @click="centerElement('date')">📍 จัดวันที่กึ่งกลาง</button>
                </div>
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง X:</label><input type="range" id="dateX" min="0" max="600" value="300" class="w-full cursor-pointer">
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง Y:</label><input type="range" id="dateY" min="0" max="600" value="530" class="w-full cursor-pointer">
            </div>

            <div class="border border-gray-200 p-3 rounded-lg bg-gray-50">
                <h4 class="mt-0 mb-2 text-gray-700 font-bold border-b pb-1">4. ตั้งค่าตัวเลข 3 ตัว</h4>
                <div class="flex justify-between gap-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">แถว:</label><input type="number" id="row3Count" value="1" min="0" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">คอลัมน์:</label><input type="number" id="col3Count" value="3" min="1" class="w-full p-1 border rounded text-sm mt-1"></div>
                </div>
                <div class="flex justify-between items-center gap-2 mt-2">
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">เลือกฟอนต์:</label>
                        <select id="num3FontFamily" class="w-full p-1 border rounded text-sm mt-1">
                            <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                        </select>
                    </div>
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">สไตล์:</label>
                        <div class="flex gap-2 mt-1">
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="num3FontBold" checked class="mr-1"> หนา</label>
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="num3FontItalic" class="mr-1"> เอียง</label>
                        </div>
                    </div>
                </div>
                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ขนาดฟอนต์:</label><input type="number" id="num3FontSize" value="50" min="10" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีอักษร:</label><input type="color" id="num3Color" value="#FFD700" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ขอบหนา:</label><input type="number" id="num3StrokeWidth" value="3" min="0" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีขอบ:</label><input type="color" id="num3StrokeColor" value="#000000" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="flex justify-between gap-2 mt-2 p-2 bg-white border rounded">
                    <div class="flex-1"><label class="block text-xs font-bold text-red-500">ห่าง ↔ (X):</label><input type="range" id="num3GapX" min="30" max="300" value="110" class="w-full cursor-pointer"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-green-500">ห่าง ↕ (Y):</label><input type="range" id="num3GapY" min="30" max="200" value="70" class="w-full cursor-pointer"></div>
                </div>
                <div class="text-center mt-2"><button class="bg-gray-500 text-white text-xs px-2 py-1 rounded hover:bg-gray-600" @click="centerElement('num3')">📍 จัดกลุ่มกึ่งกลาง</button></div>
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง X:</label><input type="range" id="num3X" min="0" max="600" value="190" class="w-full cursor-pointer">
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง Y:</label><input type="range" id="num3Y" min="0" max="600" value="450" class="w-full cursor-pointer">
            </div>

            <div class="border border-gray-200 p-3 rounded-lg bg-gray-50">
                <h4 class="mt-0 mb-2 text-gray-700 font-bold border-b pb-1">5. ตั้งค่าตัวเลข 2 ตัว</h4>
                <div class="flex justify-between gap-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">แถว:</label><input type="number" id="row2Count" value="2" min="0" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">คอลัมน์:</label><input type="number" id="col2Count" value="2" min="1" class="w-full p-1 border rounded text-sm mt-1"></div>
                </div>
                <div class="flex justify-between items-center gap-2 mt-2">
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">เลือกฟอนต์:</label>
                        <select id="num2FontFamily" class="w-full p-1 border rounded text-sm mt-1">
                            <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                        </select>
                    </div>
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">สไตล์:</label>
                        <div class="flex gap-2 mt-1">
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="num2FontBold" checked class="mr-1"> หนา</label>
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="num2FontItalic" class="mr-1"> เอียง</label>
                        </div>
                    </div>
                </div>
                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ขนาดฟอนต์:</label><input type="number" id="num2FontSize" value="50" min="10" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีอักษร:</label><input type="color" id="num2Color" value="#FFD700" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ขอบหนา:</label><input type="number" id="num2StrokeWidth" value="3" min="0" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีขอบ:</label><input type="color" id="num2StrokeColor" value="#000000" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="flex justify-between gap-2 mt-2 p-2 bg-white border rounded">
                    <div class="flex-1"><label class="block text-xs font-bold text-red-500">ห่าง ↔ (X):</label><input type="range" id="num2GapX" min="30" max="300" value="110" class="w-full cursor-pointer"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-green-500">ห่าง ↕ (Y):</label><input type="range" id="num2GapY" min="30" max="200" value="70" class="w-full cursor-pointer"></div>
                </div>
                <div class="text-center mt-2"><button class="bg-gray-500 text-white text-xs px-2 py-1 rounded hover:bg-gray-600" @click="centerElement('num2')">📍 จัดกลุ่มกึ่งกลาง</button></div>
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง X:</label><input type="range" id="num2X" min="0" max="600" value="245" class="w-full cursor-pointer">
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง Y:</label><input type="range" id="num2Y" min="0" max="600" value="280" class="w-full cursor-pointer">
            </div>

            <div class="border border-gray-200 p-3 rounded-lg bg-gray-200">
                <h4 class="mt-0 mb-2 text-gray-700 font-bold border-b pb-1">6. ตั้งค่าตัวเลข 1 ตัว (เลขวิ่ง)</h4>
                <div class="flex justify-between gap-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">แถว:</label><input type="number" id="row1Count" value="1" min="0" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">คอลัมน์:</label><input type="number" id="col1Count" value="2" min="1" class="w-full p-1 border rounded text-sm mt-1"></div>
                </div>
                <div class="flex justify-between items-center gap-2 mt-2">
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">เลือกฟอนต์:</label>
                        <select id="num1FontFamily" class="w-full p-1 border rounded text-sm mt-1">
                            <option value="Arial">Arial</option><option value="Tahoma">Tahoma</option><option value="Kanit">Kanit</option><option value="Prompt">Prompt</option><option value="Sarabun">Sarabun</option><option value="Mitr">Mitr</option><option value="Mali">Mali</option><option value="Itim">Itim</option><option value="Chakra Petch">Chakra Petch</option><option value="Pattaya">Pattaya</option><option value="Pridi">Pridi</option><option value="Charm">Charm</option>
                        </select>
                    </div>
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-600">สไตล์:</label>
                        <div class="flex gap-2 mt-1">
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="num1FontBold" checked class="mr-1"> หนา</label>
                            <label class="text-xs flex items-center cursor-pointer"><input type="checkbox" id="num1FontItalic" class="mr-1"> เอียง</label>
                        </div>
                    </div>
                </div>
                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ขนาดฟอนต์:</label><input type="number" id="num1FontSize" value="50" min="10" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีอักษร:</label><input type="color" id="num1Color" value="#FFD700" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="flex justify-between gap-2 mt-2">
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">ขอบหนา:</label><input type="number" id="num1StrokeWidth" value="3" min="0" class="w-full p-1 border rounded text-sm mt-1"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-gray-600">สีขอบ:</label><input type="color" id="num1StrokeColor" value="#000000" class="w-full h-[30px] p-0 border rounded cursor-pointer mt-1"></div>
                </div>
                <div class="flex justify-between gap-2 mt-2 p-2 bg-white border rounded">
                    <div class="flex-1"><label class="block text-xs font-bold text-red-500">ห่าง ↔ (X):</label><input type="range" id="num1GapX" min="30" max="300" value="80" class="w-full cursor-pointer"></div>
                    <div class="flex-1"><label class="block text-xs font-bold text-green-500">ห่าง ↕ (Y):</label><input type="range" id="num1GapY" min="30" max="200" value="70" class="w-full cursor-pointer"></div>
                </div>
                <div class="text-center mt-2"><button class="bg-gray-500 text-white text-xs px-2 py-1 rounded hover:bg-gray-600" @click="centerElement('num1')">📍 จัดกลุ่มกึ่งกลาง</button></div>
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง X:</label><input type="range" id="num1X" min="0" max="600" value="260" class="w-full cursor-pointer">
                <label class="block text-xs font-bold text-gray-600 mt-2">ตำแหน่ง Y:</label><input type="range" id="num1Y" min="0" max="600" value="180" class="w-full cursor-pointer">
            </div>
            
            <hr class="border-gray-300">
            <button class="bg-green-600 text-white py-3 rounded-lg font-bold text-lg shadow hover:bg-green-700 transition" @click="generateBatchPreviews">🚀 สร้างรูปทั้งหมด</button>
            <button id="downloadZipBtn" class="bg-yellow-400 text-gray-800 py-3 rounded-lg font-bold text-lg shadow hover:bg-yellow-500 transition hidden" @click="downloadZip">📥 ดาวน์โหลดไฟล์ ZIP</button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useHead } from '#imports'

useHead({
  script: [{ src: 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js' }],
  link: [{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Chakra+Petch:ital,wght@0,400;0,700;1,400;1,700&family=Charm:wght@400;700&family=Itim&family=Kanit:ital,wght@0,400;0,700;1,400;1,700&family=Mali:ital,wght@0,400;0,700;1,400;1,700&family=Mitr:wght@400;700&family=Pattaya&family=Pridi:wght@400;700&family=Prompt:ital,wght@0,400;0,700;1,400;1,700&family=Sarabun:ital,wght@0,400;0,700;1,400;1,700&display=swap' }]
})

const router = useRouter()

const isExpired = ref(false)
const expireDateStr = ref('')

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
    'logoX', 'logoY', 'logoScale', 
    'headerX', 'headerY', 'headerFontSize', 'headerColor', 'headerStrokeWidth', 'headerStrokeColor', 'headerFontFamily', 'headerFontBold', 'headerFontItalic',
    'datePicker', 'dateX', 'dateY', 'dateFontSize', 'dateColor', 'dateStrokeWidth', 'dateStrokeColor', 'dateFontFamily', 'dateFontBold', 'dateFontItalic',
    'row3Count', 'col3Count', 'num3X', 'num3Y', 'num3FontSize', 'num3Color', 'num3GapX', 'num3GapY', 'num3StrokeWidth', 'num3StrokeColor', 'num3FontFamily', 'num3FontBold', 'num3FontItalic',
    'row2Count', 'col2Count', 'num2X', 'num2Y', 'num2FontSize', 'num2Color', 'num2GapX', 'num2GapY', 'num2StrokeWidth', 'num2StrokeColor', 'num2FontFamily', 'num2FontBold', 'num2FontItalic',
    'row1Count', 'col1Count', 'num1X', 'num1Y', 'num1FontSize', 'num1Color', 'num1GapX', 'num1GapY', 'num1StrokeWidth', 'num1StrokeColor', 'num1FontFamily', 'num1FontBold', 'num1FontItalic'
];

const fetchFormats = async () => {
    const token = localStorage.getItem('token');
    const res = await fetch('http://localhost:8000/formats', { headers: { 'Authorization': `Bearer ${token}` } });
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
        draw();
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
        previewZone.innerHTML = '<span class="text-gray-400">กดปุ่ม "🚀 สร้างรูปทั้งหมด" เพื่อดูพรีวิวที่นี่</span>';
    }
    
    document.getElementById('downloadZipBtn').classList.add('hidden');
}

const deleteSelectedFormat = async () => {
    const token = localStorage.getItem('token');
    const sel = document.getElementById('formatSelect').value;
    
    if(sel === 'NEW') return alert('ไม่สามารถลบรายการนี้ได้ กรุณาเลือกรูปแบบที่บันทึกไว้ครับ');
    if(!confirm(`⚠️ คุณแน่ใจหรือไม่ว่าต้องการลบรูปแบบ '${sel}' ทิ้ง?\n(การกระทำนี้ไม่สามารถกู้คืนได้)`)) return;
    
    try {
        const res = await fetch(`http://localhost:8000/formats/${encodeURIComponent(sel)}`, {
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
        const response = await fetch('http://localhost:8000/formats', {
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
        catDiv.className = 'mb-1';
        const catHeader = document.createElement('div');
        catHeader.className = 'flex items-center justify-between bg-gray-100 p-2 rounded cursor-pointer hover:bg-gray-200';
        
        const catLabel = document.createElement('label');
        catLabel.className = 'font-bold text-blue-600 flex items-center cursor-pointer text-sm m-0 flex-1';
        const catCb = document.createElement('input');
        catCb.type = 'checkbox';
        catCb.className = 'mr-2 cursor-pointer w-4 h-4 cat-cb';
        catLabel.appendChild(catCb);
        catLabel.appendChild(document.createTextNode(' ' + category));
        
        const toggleBtn = document.createElement('span');
        toggleBtn.className = 'text-xs text-gray-500 p-1 px-3 bg-gray-200 rounded hover:bg-gray-300 transition';
        toggleBtn.innerHTML = '▼ เปิด'; 
        
        catHeader.appendChild(catLabel);
        catHeader.appendChild(toggleBtn);
        catDiv.appendChild(catHeader);
        
        const subDiv = document.createElement('div');
        subDiv.className = 'sub-items flex flex-col p-2 bg-gray-50 border border-t-0 rounded-b';
        subDiv.style.display = 'none'; 
        
        items.forEach(item => {
            const subLabel = document.createElement('label');
            subLabel.className = 'font-normal text-xs flex items-center mt-1 cursor-pointer text-gray-800';
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
            draw();
        });
        
        subDiv.querySelectorAll('.sub-cb').forEach(cb => {
            cb.addEventListener('change', function() {
                updateCategoryCheckboxes();
                draw();
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
            draw();
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
            if (digitsCount === 3) row.push(Math.floor(Math.random() * 1000).toString().padStart(3, '0'));
            else if (digitsCount === 2) row.push(Math.floor(Math.random() * 100).toString().padStart(2, '0'));
            else if (digitsCount === 1) row.push(Math.floor(Math.random() * 10).toString());
        }
        grid.push(row);
    }
    return grid;
}

const generatePreviewNumbers = () => {
    numbers3Grid = createNumbersArray(document.getElementById('row3Count').value, document.getElementById('col3Count').value, 3);
    numbers2Grid = createNumbersArray(document.getElementById('row2Count').value, document.getElementById('col2Count').value, 2);
    numbers1Grid = createNumbersArray(document.getElementById('row1Count').value, document.getElementById('col1Count').value, 1);
    draw();
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
    draw();
}

const getFontString = (idPrefix, fontSize) => {
    const family = document.getElementById(idPrefix + 'FontFamily').value;
    const isBold = document.getElementById(idPrefix + 'FontBold').checked ? 'bold' : 'normal';
    const isItalic = document.getElementById(idPrefix + 'FontItalic').checked ? 'italic' : 'normal';
    return `${isItalic} ${isBold} ${fontSize}px "${family}", sans-serif`;
}

const draw = (currentHeader = null) => {
    if(!ctx || !canvas) return;
    document.getElementById('logoScaleVal').innerText = document.getElementById('logoScale').value;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (bgImage) ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
    else { ctx.fillStyle = '#ff4d4d'; ctx.fillRect(0, 0, canvas.width, canvas.height); }

    if (logoImage) {
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
        div.className = 'relative flex flex-col items-center font-bold text-xs text-gray-700';
        
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
            el.addEventListener('input', () => { draw(); });
            if (el.type === 'checkbox' || el.tagName.toLowerCase() === 'select') {
                el.addEventListener('change', () => { draw(); });
            }
        }
    });
    
    const bgUpload = document.getElementById('bgUpload');
    const logoUpload = document.getElementById('logoUpload');
    if(bgUpload) bgUpload.addEventListener('change', (e) => handleImageUpload(e, 'bg'));
    if(logoUpload) logoUpload.addEventListener('change', (e) => handleImageUpload(e, 'logo'));

    generatePreviewNumbers(); 
}

onMounted(async () => {
    const token = localStorage.getItem('token');
    if (!token) return router.push('/login');

    try {
        const res = await fetch('http://localhost:8000/users/me', { headers: { 'Authorization': `Bearer ${token}` } });
        if(res.ok) {
            const userData = await res.json();
            const end_date = new Date(userData.sub_end);
            if (end_date < new Date()) {
                isExpired.value = true;
                expireDateStr.value = end_date.toLocaleString('th-TH', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' });
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
    
    document.fonts.ready.then(() => {
        const defBg = new Image();
        defBg.src = '/img/default-bg.png';
        defBg.onload = () => { bgImage = defBg; draw(); };

        const defLogo = new Image();
        defLogo.src = '/img/default-logo.png';
        defLogo.onload = () => { logoImage = defLogo; draw(); };
        
        draw(); 
    });
})
</script>