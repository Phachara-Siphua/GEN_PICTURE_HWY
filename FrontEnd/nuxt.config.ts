// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  app: {
    head: {
      title: 'RunBi', // เปลี่ยนชื่อเว็บตรงนี้ได้เลย
      link: [
        // อ้างอิงไปที่ไฟล์รูปไอคอนของคุณ
        { rel: 'icon', type: 'image/png', href: '/img/icon.png' } 
      ]
    }
  },
  // เพิ่มส่วนนี้เพื่ออนุญาตให้ LocalTunnel (หรือ URL อื่นๆ) เข้าถึงเว็บได้
  vite: {
    server: {
      allowedHosts: true // ยอมรับทุก URL ที่ชี้เข้ามา
    }
  }
})