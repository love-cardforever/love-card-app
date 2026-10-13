# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import urllib.request
import base64

# เข้ารหัส Base64 ป้องกันการเปิดอ่านคีย์ลับผ่านคำสั่ง nano
_ENCRYPTED_MASTER_KEY = "dGFwaXBpcGF0" # tapipipat

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def secure_auth():
    clear_screen()
    print("\033[1;35m========================================\033[0m")
    print("\033[1;36m      SECURE CREATOR TERMINAL v2.0      \033[0m")
    print("\033[1;35m========================================\033[0m")
    try:
        pass_input = input("\033[1;33m[*] กรุณากรอก Creator Master Key: \033[0m")
        decoded_key = base64.b64decode(_ENCRYPTED_MASTER_KEY).decode('utf-8')
        if pass_input != decoded_key:
            print("\033[1;31m[!] สิทธิ์การเข้าถึงถูกปฏิเสธ! กำลังทำลายเซสชัน...\033[0m")
            time.sleep(1.5)
            sys.exit()
    except Exception:
        sys.exit()

def run_dashboard():
    URL = "https://love-card-app-86e20-default-rtdb.asia-southeast1.firebasedatabase.app/.json"
    while True:
        clear_screen()
        print("\033[1;35m=== แผงควบคุมเทอร์มินัลผู้สร้าง (Realtime) ===\033[0m")
        print(" [1] ดูข้อมูลผู้ใช้งานทั้งหมด")
        print(" [2] ดูข้อมูลคู่รัก & รูปภาพความทรงจำ")
        print(" [3] ตรวจสอบรายงานจากแอดมิน")
        print(" [4] ออกจากระบบ")
        
        choice = input("\n\033[1;32mเลือกคำสั่ง (1-4): \033[0m")
        try:
            req = urllib.request.urlopen(URL)
            db = json.loads(req.read().decode('utf-8'))
        except Exception as e:
            print(f"\033[1;31m[!] ไม่สามารถดึงข้อมูลคลาวด์ได้: {e}\033[0m")
            time.sleep(2)
            continue

        if choice == '1':
            clear_screen()
            print("\033[1;36m--- รายชื่อผู้ใช้ทั้งหมดในระบบ ---\033[0m")
            for u in db.get('users', []):
                print(f"ID: {u.get('id')} | ชื่อ: {u.get('name')} | อีเมล: {u.get('email')}")
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == '2':
            clear_screen()
            print("\033[1;36m--- ข้อมูลคู่รักและสถานะความทรงจำ ---\033[0m")
            for c in db.get('couples', []):
                print(f"Couple ID: {c.get('id')} | คู่: {c.get('user1Name')} & {c.get('user2Name')} | สถานะ: {c.get('status')}")
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == '3':
            clear_screen()
            print("\033[1;36m--- ข้อความรายงานจากแอดมิน ---\033[0m")
            for r in db.get('creatorReports', []):
                print(f"[{r.get('time')}] {r.get('content')}")
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == '4':
            print("\033[1;31mออกจากเทอร์มินัลสำเร็จ\033[0m")
            break

if __name__ == "__main__":
    secure_auth()
    run_dashboard()
