
import os
import threading
import telebot
from gtts import gTTS
from flask import Flask

# आपका टेलीग्राम बॉट टोकन
BOT_TOKEN = '8877867670:AAEsvaytzN_IsR-I_e4VRidriSYD_Aciogw'

# बॉट इनिशियलाइज करें
bot = telebot.TeleBot(BOT_TOKEN)

# Render को लाइव रखने के लिए एक छोटा सा वेब सर्वर
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "नमस्ते रौनक बाबू! मुझे कोई भी टेक्स्ट भेजिए, मैं उसे वॉइस नोट में बदल दूंगा।")

@bot.message_handler(func=lambda message: True)
def text_to_speech(message):
    text_to_convert = message.text
    file_name = f"voice_{message.from_user.id}.mp3"
    
    status_msg = bot.reply_to(message, "⏳ आपकी वॉइस फ़ाइल तैयार हो रही है...")
    
    try:
        # gTTS से टेक्स्ट को वॉइस में बदलना
        tts = gTTS(text=text_to_convert, lang='hi', slow=False)
        tts.save(file_name)
        
        # वॉइस फ़ाइल भेजना
        with open(file_name, 'rb') as audio:
            bot.send_voice(message.chat.id, audio, reply_to_message_id=message.message_id, caption="लो बाबू, आपकी वॉइस तैयार है! 😎")
            
        # ऍफ़एम मैसेज डिलीट करना
        bot.delete_message(message.chat.id, status_msg.message_id)
        
    except Exception as e:
        bot.reply_to(message, "माफ़ कीजिएगा, वॉइस कन्वर्ट करने में कुछ दिक्कत आ रही है।")
        print(f"Error: {e}")
        
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == '__main__':
    print("बॉट बिना किसी एरर के सफलतापूर्वक स्टार्ट हो गया है...")
    # Flask को अलग थ्रेड में चलाना
    t = threading.Thread(target=run_flask)
    t.start()
    
    # टेलीग्राम बॉट पोलिंग शुरू करना
    bot.infinity_polling()
