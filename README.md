# Text-to-Speak-

⚙️ Step-by-Step Setup (Termux में चलाने के लिए)

🐍 1. Python इंस्टॉल करें
```bash 
pkg update && pkg upgrade -y
pkg install python -y
```

🎧 2. जरूरी लाइब्रेरी इंस्टॉल करें

```bash
pip install python-telegram-bot==13.15 gtts pydub
pkg install ffmpeg -y
```

> ⚠️ ffmpeg जरूरी है ताकि background music और audio mixing सही चले।


🤖 5. बॉट चलाइए
```bash 
python bot.py
```

> अगर सब सही है तो टर्मिनल में ये दिखेगा:
> 🚀 Premium Voice Bot Running...


💬 6. Telegram में जाकर अपने Bot को ओपन करें:

1. @BotFather से बनाया हुआ Bot टोकन आपने पहले ही लगाया है


2. अब Telegram में जाकर उस Bot को /start भेजें


3. फिर किसी भी टेक्स्ट को भेजें → आपको उसका voice reply मिलेगा 🎙️

# 🧠 Useful Commands (Telegram में भेजने के लिए):

Command	Function

/setlang hi	भाषा हिंदी करें
/setlang en	भाषा अंग्रेज़ी करें
/speed slow	धीरे बोलने वाला वॉइस
/speed normal	नॉर्मल स्पीड
/voice male	मेल टोन
/voice female	फीमेल टोन
/music on	बैकग्राउंड म्यूजिक ऑन
/music off	बैकग्राउंड म्यूजिक ऑफ

✅ 100% Working Fix (for Termux)

Step 1. पहले पुराने version uninstall करें
```bash 
pip uninstall python-telegram-bot -y
pip uninstall urllib3 -y
pip uninstall six -y
```

---

Step 2. फिर dependencies clean reinstall करें
```bash 
pip install urllib3==1.26.20 six==1.16.0
```


---

Step 3. अब सही compatible version इंस्टॉल करें

> python-telegram-bot के v20+ versions Termux में errors देते हैं।
इसलिए हम v13.15 version install करेंगे (यह आपके कोड के साथ compatible है)।


```bash 
pip install python-telegram-bot==13.15
```

---

Step 4. Verify Installation

ये चलाकर चेक करें 👇
```bash 
python -m telegram
```

अगर कोई error नहीं आया तो ✅ सब ठीक है।


---

Step 5. फिर अपना bot चलाएँ
```bash 
python bot.py
```

---

⚡ अगर फिर भी वही error आए:

तो ये दो कमांड चलाइए (force reinstall):

```bash
pip install --upgrade --force-reinstall python-telegram-bot==13.15
pip install --upgrade --force-reinstall urllib3==1.26.20 six==1.16.0
```
फिर दोबारा:
```bash 
python bot.py
```
अब आपका bot चल जाएगा बिना किसी warning/error के 🚀


# ⚙️ Auto-Start Setup for Termux (Voice Bot)

मान लेते हैं कि आपका बॉट /data/data/com.termux/files/home/VoiceBot/bot.py में सेव है।
अगर आपने मेरा पहले वाला setup फॉलो किया था — तो यही path होगा ✅


---

🧩 1. Termux boot script पैकेज इंस्टॉल करें

pkg install termux-api -y
pkg install termux-services -y


---

🚀 2. Termux-Boot App इंस्टॉल करें

> Termux को boot के साथ चलाने के लिए आपको एक helper ऐप चाहिए।
यह F-Droid या GitHub से फ्री में मिलेगा।



Download Link:
👉 https://f-droid.org/en/packages/com.termux.boot/

इंस्टॉल करने के बाद:

1. Termux-Boot को ओपन करें


2. Permission allow करें


3. फिर Termux को एक बार restart करें




---

📁 3. Boot Script बनाइए

अब ये कमांड चलाइए 👇

mkdir -p ~/.termux/boot
cd ~/.termux/boot
nano autostart.sh

अब इसमें ये कोड पेस्ट करें 👇

#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/VoiceBot
python bot.py

फिर:

CTRL + O → Save

ENTER

CTRL + X → Exit



---

🔒 4. Script को executable बनाइए

chmod +x ~/.termux/boot/autostart.sh


---

✅ 5. अब टेस्ट करें

अब जब आप Termux या अपना फ़ोन रीस्टार्ट करेंगे,
Termux-Boot अपने-आप चालू होकर ये स्क्रिप्ट चलाएगा 👇

🚀 Premium Voice Bot Running...

यानि आपका Telegram Voice Bot auto-start हो जाएगा हर बार boot पर 🔁


---

💡 Bonus Tip:

अगर आप चाहते हैं कि यह script background में quietly चले (बिना window खुले), तो आप इसे Termux:Tasker या Termux-WakeLock के साथ भी चला सकते हैं:

termux-wake-lock
nohup python /data/data/com.termux/files/home/VoiceBot/bot.py &

इससे आपका बॉट बंद नहीं होगा जब स्क्रीन बंद हो जाएगी 🔋


---

क्या चाहेंगे कि मैं इसी बॉट के लिए
📦 Termux one-click installer script (setup.sh) भी बना दूँ
जिससे कोई भी नया यूज़र बस bash setup.sh चलाकर पूरा बॉट इंस्टॉल कर ले?

