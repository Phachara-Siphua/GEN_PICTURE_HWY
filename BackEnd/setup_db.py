import pymysql
import hashlib

# ข้อมูลจาก Aiven ของคุณ
DB_HOST = 'dbgenpicturehwy-genpicturehwy.j.aivencloud.com'
DB_USER = 'avnadmin'
DB_PASS = 'AVNS__fa2yeBXwsXcV_eon6B'
DB_NAME = 'defaultdb'
DB_PORT = 20513

print("1. กำลังเชื่อมต่อฐานข้อมูล Aiven บนคลาวด์...")
try:
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    print("2. กำลังสร้างตาราง users...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(20) DEFAULT 'user',
        sub_start DATETIME,
        sub_end DATETIME,
        max_formats INT DEFAULT 2,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    print("3. กำลังสร้างตาราง formats...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS formats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        format_name VARCHAR(100) NOT NULL,
        settings_data JSON NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    print("4. กำลังสร้างไอดี Admin...")
    admin_pass = hashlib.sha256("1234".encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (username, password, role, sub_start, sub_end, max_formats)
            VALUES ('admin', %s, 'admin', NOW(), DATE_ADD(NOW(), INTERVAL 1 YEAR), 10)
        """, (admin_pass,))
        conn.commit()
        print("-> สร้างไอดี Admin สำเร็จ! (User: admin / Pass: 1234)")
    else:
        print("-> ไอดี Admin มีอยู่แล้ว")

    conn.close()
    print("🎉 ตั้งค่าฐานข้อมูลบน Aiven คลาวด์เสร็จสมบูรณ์!")

except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")