import os
import time
import cv2
import requests
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==========================================
# ⚙️ STEP 1: CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

# Bait folder (Created automatically on the Desktop)
BAIT_FOLDER = os.path.join(os.path.expanduser('~'), 'Desktop', 'SECRET_FILES')

class GhostCanaryHandler(FileSystemEventHandler):
    def __init__(self):
        self.lock = threading.Lock()
        self.last_trigger = 0

    def on_any_event(self, event):
        """Triggers on any activity (open, modify) in the folder"""
        # Prevent false alarms when the folder itself is being created
        if event.src_path == BAIT_FOLDER and event.event_type == 'created':
            return
            
        self.execute_trap(event.src_path, event.event_type)

    def execute_trap(self, filepath, event_type):
        with self.lock:
            # Sends only one photo every 15 seconds (Spam protection)
            if time.time() - self.last_trigger < 15:
                return
            self.last_trigger = time.time()

        print(f"[!] TRAP TRIGGERED! Action: {event_type}")
        
        # Running the camera capture in a separate thread prevents system lag
        threading.Thread(target=self.capture_and_send, args=(filepath,)).start()

    def capture_and_send(self, filepath):
        photo_path = "ghost_capture.jpg"
        
        try:
            # Open camera (DSHOW works fast and silently on Windows)
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            
            if not cap.isOpened():
                print("❌ Camera not found or currently in use!")
                return

            # Give the camera 1 second to adjust focus
            time.sleep(1.0) 
            ret, frame = cap.read()
            cap.release() # Close camera immediately to quickly turn off the green light

            if ret:
                cv2.imwrite(photo_path, frame)
                
                user_name = os.getlogin()
                file_name = os.path.basename(filepath)
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                
                # Send via Telegram API
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
                caption = (f"🚨 <b>Z-PEGASUS: GHOST TRAP</b>\n\n"
                           f"👁️ <b>ALERT!</b> Someone accessed the secret folder on your laptop!\n\n"
                           f"📁 <b>Target:</b> {file_name}\n"
                           f"👤 <b>PC User:</b> {user_name}\n"
                           f"🕒 <b>Time:</b> {current_time}")

                with open(photo_path, "rb") as photo:
                    payload = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption, "parse_mode": "HTML"}
                    response = requests.post(url, data=payload, files={"photo": photo})
                    
                    if response.status_code == 200:
                        print(f"✅ Photo successfully sent to Telegram! ({current_time})")
                    else:
                        print(f"❌ Error sending to Telegram: {response.text}")
                
                # Destroy evidence (delete the photo from the laptop)
                if os.path.exists(photo_path):
                    os.remove(photo_path)
                    
        except Exception as e:
            print(f"Critical Error: {e}")

def create_bait_system():
    """Create the bait folder and tempting files"""
    if not os.path.exists(BAIT_FOLDER):
        os.makedirs(BAIT_FOLDER)
    
    bait_file = os.path.join(BAIT_FOLDER, "Passwords_List.txt")
    if not os.path.exists(bait_file):
        with open(bait_file, 'w', encoding='utf-8') as f:
            f.write("Warning! This file is encrypted and monitored by a security system.\n\n"
                    "Z-PEGASUS CORE: Active\n"
                    "Instagram: inst_user_992\n"
                    "Crypto Wallet Key: 0x8923...F92A")
        print(f"📁 Bait folder created: {BAIT_FOLDER}")

if __name__ == "__main__":
    print("="*50)
    print("🛡️ Z-PEGASUS GHOST PROTOCOL INITIALIZING...")
    print("="*50)
    
    # 1. Create the trap
    create_bait_system()
    
    # 2. Setup the observer
    event_handler = GhostCanaryHandler()
    observer = Observer()
    # Monitor the entire folder as Windows registers folder access faster
    observer.schedule(event_handler, BAIT_FOLDER, recursive=True)
    observer.start()
    
    print("\n✅ System active! Silently monitoring in the background...")
    print("Press Ctrl+C in the console to stop.\n")
    
    try:
        # Infinite loop to keep the program running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 System shutting down...")
        observer.stop()
    
    observer.join()
    print("👋 Security system closed.")
