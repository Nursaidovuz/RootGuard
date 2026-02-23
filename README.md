**Ha, albatta! Yuz foiz tiqish kerak.**

Siz yozgan bu qismlar `README.md` faylining **eng muhim (yurak) qismi** hisoblanadi. Chunki GitHub'ga kirgan boshqa dasturchilar yoki kiberxavfsizlik mutaxassislari kodingizni qanday o'rnatishni, qanday sozlashni va nima maqsadda yozilganini aynan shu yerdan o'qib bilib olishadi. Ayniqsa **Disclaimer (Ogohlantirish)** qismi sizni har qanday huquqiy javobgarlikdan himoya qiladi.

Hammasi bitta joyda chiroyli va professional ko'rinishi uchun, `README.md` faylingizning ichi **to'liq** mana bu matndan iborat bo'lishi kerak (shundayligicha nusxalab olasiz):

```markdown
# 🛡️ RootGuard: Stealth Canary Trap

RootGuard is a lightweight, zero-trace security protocol designed to catch unauthorized physical access to your computer. It acts as a "Silent Sentinel" by monitoring a bait folder. 

If an intruder opens the bait file, RootGuard instantly and silently captures their photo using the webcam and sends a real-time alert to your Telegram.

## 🚀 Features
* **Zero UI:** Runs completely in the background.
* **Instant Reaction:** Millisecond response time using `watchdog`.
* **Anti-Spam:** Built-in cooldown limits to prevent Telegram spam.
* **Undetectable:** Does not use keyloggers or suspicious libraries that trigger Antivirus software.

## 🛠️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/Nursaidovuz/RootGuard.git](https://github.com/Nursaidovuz/RootGuard.git)

```

2. Install requirements:
```bash
pip install opencv-python requests watchdog

```


3. Open the Python script and add your Telegram credentials:
```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

```


4. Run the script. A bait folder will be automatically created on your Desktop.

## ⚠️ Disclaimer

This tool is created for educational and personal security purposes only. The author is not responsible for any misuse or damage caused by this program.

```

