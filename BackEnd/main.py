from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import pymysql
import json
import hashlib

# ================= ตั้งค่า Database และ JWT =================
SECRET_KEY = "super-secret-key-lottery-app"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def get_db_connection():
#     return pymysql.connect(host='localhost', user='root', password='', database='lottery_db', cursorclass=pymysql.cursors.DictCursor)
def get_db_connection():
    return pymysql.connect(
        host='dbgenpicturehwy-genpicturehwy.j.aivencloud.com',
        user='avnadmin',
        password='AVNS__fa2yeBXwsXcV_eon6B',
        database='defaultdb',
        port=20513,
        cursorclass=pymysql.cursors.DictCursor
    )

def get_password_hash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password, hashed_password):
    return get_password_hash(plain_password) == hashed_password

# ================= Models =================
class FormatSave(BaseModel):
    format_name: str
    settings_data: dict

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user" 
    max_formats: int = 2
    sub_start_date: Optional[str] = None 
    sub_end_date: Optional[str] = None   

class UserUpdate(BaseModel):
    username: str
    password: Optional[str] = None
    role: str
    max_formats: int
    sub_start_date: str
    sub_end_date: str

# ================= ระบบ Login & Auth =================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: raise credentials_exception
    except JWTError: raise credentials_exception
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
    conn.close()
    if user is None: raise credentials_exception
    return user

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", (form_data.username,))
        user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Username หรือ Password ไม่ถูกต้อง")
    
    if user['sub_end'] and user['sub_end'] < datetime.now():
        raise HTTPException(status_code=403, detail="แพ็กเกจของคุณหมดอายุแล้ว โปรดติดต่อแอดมิน")

    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user['id'],
        "username": current_user['username'], 
        "role": current_user['role'],
        "sub_start": current_user['sub_start'],
        "sub_end": current_user['sub_end'],
        "max_formats": current_user['max_formats']
    }

# ================= API จัดการผู้ใช้งาน (แอดมินเท่านั้น) =================
@app.get("/users")
async def get_all_users(current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="ไม่มีสิทธิ์เข้าถึง")
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # อัปเดตคำสั่ง SQL ให้นับจำนวนรูปแบบที่ User แต่ละคนบันทึกไว้ (used_formats)
        cursor.execute("""
            SELECT u.id, u.username, u.role, u.sub_start, u.sub_end, u.max_formats, u.created_at,
                   (SELECT COUNT(*) FROM formats f WHERE f.user_id = u.id) AS used_formats
            FROM users u 
            ORDER BY u.id DESC
        """)
        users = cursor.fetchall()
    conn.close()
    return users

@app.post("/register")
async def register_user(user: UserCreate, current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="แอดมินเท่านั้นที่เพิ่มผู้ใช้ได้")
        
    conn = get_db_connection()
    hashed_pw = get_password_hash(user.password)
    now_time = datetime.now().time()

    try:
        if user.sub_start_date:
            start_date_obj = datetime.strptime(user.sub_start_date, "%Y-%m-%d").date()
            sub_start = datetime.combine(start_date_obj, now_time)
        else:
            sub_start = datetime.now()

        if user.sub_end_date:
            end_date_obj = datetime.strptime(user.sub_end_date, "%Y-%m-%d").date()
            sub_end = datetime.combine(end_date_obj, now_time)
        else:
            sub_end = sub_start + timedelta(days=365)
            
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password, role, sub_start, sub_end, max_formats) VALUES (%s, %s, %s, %s, %s, %s)", 
                (user.username, hashed_pw, user.role, sub_start, sub_end, user.max_formats)
            )
            conn.commit()
        return {"message": f"สร้างบัญชี {user.username} สำเร็จ!"}
    except pymysql.IntegrityError:
        raise HTTPException(status_code=400, detail="ชื่อผู้ใช้นี้มีในระบบแล้ว")
    except Exception as e:
        raise HTTPException(status_code=500, detail="รูปแบบวันที่ผิดพลาด โปรดใช้ YYYY-MM-DD")
    finally:
        conn.close()

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="ไม่มีสิทธิ์เข้าถึง")
        
    conn = get_db_connection()
    now_time = datetime.now().time()
    try:
        start_date_obj = datetime.strptime(user.sub_start_date, "%Y-%m-%d").date()
        sub_start = datetime.combine(start_date_obj, now_time)
        
        end_date_obj = datetime.strptime(user.sub_end_date, "%Y-%m-%d").date()
        sub_end = datetime.combine(end_date_obj, now_time)
        
        with conn.cursor() as cursor:
            if user.password: 
                hashed_pw = get_password_hash(user.password)
                cursor.execute("""
                    UPDATE users 
                    SET username=%s, password=%s, role=%s, max_formats=%s, sub_start=%s, sub_end=%s 
                    WHERE id=%s
                """, (user.username, hashed_pw, user.role, user.max_formats, sub_start, sub_end, user_id))
            else:
                cursor.execute("""
                    UPDATE users 
                    SET username=%s, role=%s, max_formats=%s, sub_start=%s, sub_end=%s 
                    WHERE id=%s
                """, (user.username, user.role, user.max_formats, sub_start, sub_end, user_id))
            conn.commit()
        return {"message": f"แก้ไขข้อมูลผู้ใช้ '{user.username}' สำเร็จ!"}
    except pymysql.IntegrityError:
        raise HTTPException(status_code=400, detail="ชื่อผู้ใช้นี้มีซ้ำในระบบแล้ว")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="ไม่มีสิทธิ์เข้าถึง")
    if current_user['id'] == user_id:
        raise HTTPException(status_code=400, detail="ไม่สามารถลบบัญชีตัวเองได้")
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
        return {"message": "ลบผู้ใช้สำเร็จ"}
    finally:
        conn.close()

# ================= API สำหรับจัดการ Format =================
@app.get("/formats")
async def get_formats(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, format_name, settings_data FROM formats WHERE user_id = %s ORDER BY id DESC", (current_user['id'],))
        formats = cursor.fetchall()
    conn.close()
    for f in formats:
        f['settings_data'] = json.loads(f['settings_data'])
    return formats

@app.post("/formats")
async def save_format(format_data: FormatSave, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM formats WHERE user_id = %s AND format_name = %s", (current_user['id'], format_data.format_name))
            existing = cursor.fetchone()
            settings_json = json.dumps(format_data.settings_data)

            if existing:
                cursor.execute("UPDATE formats SET settings_data = %s WHERE id = %s", (settings_json, existing['id']))
                msg = f"อัปเดตรูปแบบ '{format_data.format_name}' สำเร็จ!"
            else:
                cursor.execute("SELECT COUNT(*) as c FROM formats WHERE user_id = %s", (current_user['id'],))
                count = cursor.fetchone()['c']
                if count >= current_user['max_formats']:
                    raise HTTPException(status_code=400, detail=f"สร้างรูปแบบไม่ได้! คุณใช้โควต้าครบแล้ว ({current_user['max_formats']} อัน)")
                
                cursor.execute("INSERT INTO formats (user_id, format_name, settings_data) VALUES (%s, %s, %s)", 
                               (current_user['id'], format_data.format_name, settings_json))
                msg = f"บันทึกรูปแบบใหม่ '{format_data.format_name}' สำเร็จ!"
            conn.commit()
        return {"message": msg}
    finally:
        conn.close()

@app.delete("/formats/{format_name}")
async def delete_format(format_name: str, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM formats WHERE user_id = %s AND format_name = %s", (current_user['id'], format_name))
            conn.commit()
        return {"message": f"ลบรูปแบบ '{format_name}' สำเร็จ"}
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)