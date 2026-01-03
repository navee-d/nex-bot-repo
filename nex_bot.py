import telebot
import requests
from rembg import remove
from PIL import Image
import io

# --- සැකසුම් (Settings) ---
TELEGRAM_BOT_TOKEN = '8357214957:AAHLy0pWFRqfftLiFAeIGi_9gdLQ54WbjsA'
DO_AGENT_ENDPOINT = 'https://kl65swm6imyoj2f4aierpt5a.agents.do-ai.run/api/v1/chat/completions'
DO_AGENT_KEY = 'kiVZqAXSpIaNUBxsnMg5NGOTTpiyoAib'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
print("Nex AI Bot is starting...")

# 1. TEXT MESSAGES (චැට් කිරීම සඳහා)
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DO_AGENT_KEY}"
        }
        payload = {
            "messages": [{"role": "user", "content": message.text}]
        }
        
        response = requests.post(DO_AGENT_ENDPOINT, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            try:
                ai_reply = data['choices'][0]['message']['content']
            except:
                ai_reply = "Hmm, I couldn't understand that."
            bot.reply_to(message, ai_reply)
        else:
            bot.reply_to(message, "AI Brain Error.")
            
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# 2. PHOTOS (Background Remove කිරීම සඳහා)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "📸 Photo detected! Removing background... (Please wait)")
        bot.send_chat_action(message.chat.id, 'upload_photo')

        # 1. ෆොටෝ එක Download කරගැනීම
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # 2. පසුබිම ඉවත් කිරීම (Processing)
        input_image = Image.open(io.BytesIO(downloaded_file))
        output_image = remove(input_image)
        
        # 3. නැවත එවීම
        bio = io.BytesIO()
        output_image.save(bio, format="PNG")
        bio.seek(0)
        
        bot.send_document(message.chat.id, bio, caption="Here is your transparent image! 🎨")
        
    except Exception as e:
        bot.reply_to(message, f"Oops! Error removing background: {e}")

# Bot එක පණගන්වමු
print("Bot is ready!")
bot.infinity_polling()