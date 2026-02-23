import os
import time
import cv2
import requests
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==========================================
# ⚙️ 1-QADAM: SOZLAMALARNI KIRITING ||| Nursaidov.uz
# ==========================================
TELEGRAM_BOT_TOKEN = "BOT_TOKENNI_SHU_YERGA_YOZING"
TELEGRAM_CHAT_ID = "CHAT_ID_SHU_YERGA_YOZING"

# Qopqon papkasi (Ish stolida yaratiladi)
BAIT_FOLDER = os.path.join(os.path.expanduser('~'), 'Desktop', 'MAXFIY_HUJJATLAR')

class GhostCanaryHandler(FileSystemEventHandler):
    def __init__(self):
        self.lock = threading.Lock()
        self.last_trigger = 0

    def on_any_event(self, event):
        """Papkada har qanday harakat (ochish, o'zgartirish) bo'lganda ishlaydi"""
        # Papkaning o'zi yaratilayotganda yolg'on signal bermasligi uchun
        if event.src_path == BAIT_FOLDER and event.event_type == 'created':
            return
            
        self.execute_trap(event.src_path, event.event_type)

    def execute_trap(self, filepath, event_type):
        with self.lock:
            # Har 15 soniyada faqat bitta rasm jo'natadi (Spamdan himoya)
            if time.time() - self.last_trigger < 15:
                return
            self.last_trigger = time.time()

        print(f"[!] QOPQON ISHGA TUSHDI! Harakat: {event_type}")
        
        # Rasmga olishni alohida oqimda (asinxron) bajarish tizimni qotirmaydi
        threading.Thread(target=self.capture_and_send, args=(filepath,)).start()

    def capture_and_send(self, filepath):
        photo_path = "ghost_capture.jpg"
        
        try:
            # Kamerani ochish (DSHOW Windows uchun tez va jim ishlaydi)
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            
            if not cap.isOpened():
                print("❌ Kamera topilmadi yoki band!")
                return

            # Fokus to'g'rilanishi uchun kameraga 1 soniya vaqt beramiz
            time.sleep(1.0) 
            ret, frame = cap.read()
            cap.release() # Kamerani darhol yopish (yashil chiroqni tez o'chirish)

            if ret:
                cv2.imwrite(photo_path, frame)
                
                user_name = os.getlogin()
                file_name = os.path.basename(filepath)
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                
                # Telegram API orqali jo'natish
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
                caption = (f"🚨 <b>Z-PEGASUS: GHOST TRAP</b>\n\n"
                           f"👁️ <b>DIQQAT!</b> Noutbukingizda kimdir maxfiy papkaga kirdi!\n\n"
                           f"📁 <b>Nishon:</b> {file_name}\n"
                           f"👤 <b>PC User:</b> {user_name}\n"
                           f"🕒 <b>Vaqt:</b> {current_time}")

                with open(photo_path, "rb") as photo:
                    payload = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption, "parse_mode": "HTML"}
                    response = requests.post(url, data=payload, files={"photo": photo})
                    
                    if response.status_code == 200:
                        print(f"✅ Telegramga rasm muvaffaqiyatli jo'natildi! ({current_time})")
                    else:
                        print(f"❌ Telegramga jo'natishda xatolik: {response.text}")
                
                # Jinoyat izini yo'qotish (rasmni noutbukdan o'chirib tashlash)
                if os.path.exists(photo_path):
                    os.remove(photo_path)
                    
        except Exception as e:
            print(f"Kritik Xato: {e}")

def create_bait_system():
    """Qopqon papka va jozibador fayllarni tayyorlash"""
    if not os.path.exists(BAIT_FOLDER):
        os.makedirs(BAIT_FOLDER)
    
    bait_file = os.path.join(BAIT_FOLDER, "Parollar_Ro'yxati.txt")
    if not os.path.exists(bait_file):
        with open(bait_file, 'w', encoding='utf-8') as f:
            f.write("Diqqat! Bu fayl shifrlangan va xavfsizlik tizimi orqali kuzatilmoqda.\n\n"
                    "Z-PEGASUS CORE: Active\n"
                    "Instagram: inst_user_992\n"
                    "Crypto Wallet Key: 0x8923...F92A")
        print(f"📁 Qopqon papka yaratildi: {BAIT_FOLDER}")

if __name__ == "__main__":
    print("="*50)
    print("🛡️ Z-PEGASUS GHOST PROTOCOL ISHGA TUSHMOQDA...")
    print("="*50)
    
    # 1. Qopqonni yaratish
    create_bait_system()
    
    # 2. Kuzatuvchini sozlash
    event_handler = GhostCanaryHandler()
    observer = Observer()
    # Butun papkani kuzatamiz, chunki Windowsda papkaga kirish tezroq qayd etiladi
    observer.schedule(event_handler, BAIT_FOLDER, recursive=True)
    observer.start()
    
    print("\n✅ Tizim faol! Orqa fonda jimgina kuzatilmoqda...")
    print("O'chirish uchun qora ekranda: Ctrl+C bosing.\n")
    
    try:
        # Dastur cheksiz ishlashi uchun tsikl
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Tizim to'xtatilmoqda...")
        observer.stop()
    
    observer.join()
    print("👋 Xavfsizlik tizimi yopildi.")