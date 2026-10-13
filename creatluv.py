# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import urllib.request
import base64
import threading

# เข้ารหัส Base64 ป้องกันการเปิดอ่านคีย์ลับผ่านคำสั่ง nano
_ENCRYPTED_MASTER_KEY = "dGFwaXBpcGF0" # tapipipat
FIREBASE_URL = "https://love-card-app-86e20-default-rtdb.asia-southeast1.firebasedatabase.app/.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def secure_auth():
    clear_screen()
    print("\033[1;35m========================================\033[0m")
    print("\033[1;36m     CREATOR MASTER TERMINAL v3.0       \033[0m")
    print("\033[1;35m========================================\033[0m")
    try:
        pass_input = input("\033[1;33m[*] กรุณากรอก Creator Master Key: \033[0m")
        decoded_key = base64.b64decode(_ENCRYPTED_MASTER_KEY).decode('utf-8')
        if pass_input != decoded_key:
            print("\033[1;31m[!] สิทธิ์การเข้าถึงถูกปฏิเสธ! รหัสผ่านไม่ถูกต้อง\033[0m")
            time.sleep(1.5)
            sys.exit()
    except Exception:
        sys.exit()

def fetch_database():
    try:
        req = urllib.request.urlopen(FIREBASE_URL, timeout=5)
        return json.loads(req.read().decode('utf-8')) or {}
    except Exception:
        return {}

def update_database(data):
    try:
        data_encoded = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(FIREBASE_URL, data=data_encoded, method='PUT')
        req.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(req)
        return True
    except Exception:
        return False

def send_creator_broadcast():
    clear_screen()
    print("\033[1;31m=== ส่งประกาศด่วนจากผู้สร้างถึงผู้ใช้ทุกคน ===\033[0m")
    msg = input("\nพิมพ์ข้อความประกาศ (หรือเว้นว่างเพื่อยกเลิก): ").strip()
    if not msg:
        return
    
    db = fetch_database()
    if 'users' in db and isinstance(db['users'], list):
        for u in db['users']:
            if 'notifications' not in u:
                u['notifications'] = []
            u['notifications'].append({
                'id': time.time(),
                'type': 'CREATOR_BROADCAST',
                'message': f"👑 ประกาศจากผู้สร้างระบบ: {msg}",
                'time': time.strftime('%d/%m/%Y %H:%M:%S'),
                'read': False
            })
        if update_database(db):
            print("\n\033[1;32m[✔] ส่งประกาศถึงผู้ใช้งานทุกคนสำเร็จแบบเรียลไทม์!\033[0m")
        else:
            print("\n\033[1;31m[✘] เกิดข้อผิดพลาดในการส่งข้อมูล\033[0m")
    else:
        print("\n\033[1;33m[!] ไม่พบรายชื่อผู้ใช้งานในระบบ\033[0m")
    input("\nกด Enter เพื่อกลับเมนู...")

def view_all_users():
    db = fetch_database()
    clear_screen()
    print("\033[1;36m--- 📁 โฟลเดอร์ข้อมูลผู้ใช้งานทั้งหมด (Users) ---\033[0m")
    users = db.get('users', [])
    if not users:
        print("ยังไม่มีผู้ใช้งานในระบบ")
    else:
        for idx, u in enumerate(users, 1):
            print(f"[{idx}] ID: {u.get('id')} | ชื่อ: {u.get('name')} | อีเมล: {u.get('email')} | คู่รักID: {u.get('coupleId') or 'ไม่มี'}")
    input("\nกด Enter เพื่อกลับเมนู...")

def view_couples_and_media():
    db = fetch_database()
    clear_screen()
    print("\033[1;36m--- 📁 โฟลเดอร์ข้อมูลคู่รัก, รูปภาพ และถังขยะ ---\033[0m")
    couples = db.get('couples', [])
    if not couples:
        print("ยังไม่มีข้อมูลคู่รักในระบบ")
    else:
        for c in couples:
            print(f"\n❤️ Couple ID: {c.get('id')} | {c.get('user1Name')} & {c.get('user2Name')} | โควต้าคืนดี: {c.get('reconcileQuota', 3)}")
            photos = c.get('photos', [])
            trash = c.get('trashPhotos', [])
            print(f"   - รูปในอัลบั้ม: {len(photos)} รูป | รูปในถังขยะ (30 วัน): {len(trash)} รูป")
    input("\nกด Enter เพื่อกลับเมนู...")

def view_reports_and_issues():
    db = fetch_database()
    clear_screen()
    print("\033[1;33m--- ⚠️ รายงานปัญหาจากแอดมินและผู้ใช้งาน ---\033[0m")
    
    print("\n[รายงานจากแอดมินถึงผู้สร้าง]:")
    reports = db.get('creatorReports', [])
    if not reports:
        print(" - ไม่มีรายงาน")
    else:
        for r in reports:
            print(f" [{r.get('time')}] {r.get('content')}")

    print("\n[รายงานปัญหาจากผู้ใช้ทั่วไป (Admin Requests)]:")
    admin_reqs = db.get('adminRequests', [])
    if not admin_reqs:
        print(" - ไม่มีรายงานปัญหา")
    else:
        for ar in admin_reqs:
            print(f" [{ar.get('time')}] User ID: {ar.get('userId')} -> {ar.get('content')}")

    input("\nกด Enter เพื่อกลับเมนู...")

def run_dashboard():
    while True:
        clear_screen()
        print("\033[1;35m========================================\033[0m")
        print("\033[1;32m      CREATOR MASTER CONTROL PANEL      \033[0m")
        print("\033[1;35m========================================\033[0m")
        print(" [1] 📁 ดูข้อมูลผู้ใช้งานทั้งหมด (Users)")
        print(" [2] 🖼️  ดูข้อมูลคู่รัก, รูปภาพ และถังขยะ")
        print(" [3] ⚠️  ตรวจสอบรายงานปัญหา (แอดมิน & ผู้ใช้)")
        print(" [4] 📢 ส่งประกาศด่วนจากเซิร์ฟเวอร์ (Broadcast)")
        print(" [5] 🚪 ออกจากระบบเทอร์มินัล")
        
        choice = input("\n\033[1;33mเลือกคำสั่ง (1-5): \033[0m").strip()
        
        if choice == '1':
            view_all_users()
        elif choice == '2':
            view_couples_and_media()
        elif choice == '3':
            view_reports_and_issues()
        elif choice == '4':
            send_creator_broadcast()
        elif choice == '5':
            print("\n\033[1;31m[!] ออกจากเทอร์มินัลผู้สร้างเรียบร้อยแล้ว\033[0m")
            break
        else:
            time.sleep(1)

if __name__ == "__main__":
    secure_auth()
    run_dashboard()
