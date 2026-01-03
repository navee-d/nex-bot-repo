import telebot
import requests
import json

# --- සැකසුම් (Settings) ---

# 1. Telegram Token
TELEGRAM_BOT_TOKEN = '8357214957:AAHLy0pWFRqfftLiFAeIGi_9gdLQ54WbjsA'

# 2. DigitalOcean Agent Endpoint (දැන් මේක හරියටම හරි: /chat/completions එක්ක)
DO_AGENT_ENDPOINT = 'https://kl65swm6imyoj2f4aierpt5a.agents.do-ai.run/api/v1/chat/completions'

# 3. DigitalOcean Key
DO_AGENT_KEY = 'kiVZqAXSpIaNUBxsnMg5NGOTTpiyoAib'

# Bot එක පණගන්වමු
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
print("Nex AI Bot is starting...")

@bot.message_handler(func=lambda message: True)
def send_to_agent(message):
    user_text = message.text
    print(f"User ({message.chat.username}): {user_text}")
    
    # "Typing..." කියලා පෙන්වමු
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DO_AGENT_KEY}"
        }
        
        # දත්ත යවන ආකෘතිය වෙනස් කළා (Docs වලට අනුව)
        payload = {
            "messages": [
                {"role": "user", "content": user_text}
            ]
        }
        
        # Agent වෙත යැවීම
        response = requests.post(DO_AGENT_ENDPOINT, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            # පිළිතුර ගන්නා විදියත් වෙනස් කළා (Chat Completion format)
            try:
                ai_reply = data['choices'][0]['message']['content']
            except (KeyError, IndexError):
                # වෙන ක්‍රමයකට ආවොත් මේකෙන් ගමු
                ai_reply = data.get('response') or str(data)
                
            bot.reply_to(message, ai_reply)
        else:
            bot.reply_to(message, f"Error from AI Brain: {response.status_code}\n{response.text}")
            
    except Exception as e:
        bot.reply_to(message, f"System Error: {str(e)}")

# Bot එක දිගටම run කර තැබීම
print("Bot is ready! Go to Telegram and search for 'naveed_box_bot'")
bot.infinity_polling()