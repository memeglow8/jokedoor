import os
from flask import Flask, request, Response
from telebot import TeleBot, types
from config import *

app = Flask(__name__)
bot = TeleBot(BOT_TOKEN)

def send_verify_button(channel_id, message_text):
    """Create and send message with verify button"""
    markup = types.InlineKeyboardMarkup()
    verify_button = types.InlineKeyboardButton(text="✅ Verify Now", url=VERIFY_URL)
    markup.add(verify_button)
    
    return bot.send_message(channel_id, message_text, reply_markup=markup)

@app.route('/', methods=['POST'])
def webhook():
    """Handle webhook requests from Telegram"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return Response('ok', status=200)
    else:
        return Response('error', status=403)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """Forward messages to channel with verify button"""
    # Check if sender is admin
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    is_admin = chat_member.status in ['creator', 'administrator']
    
    if is_admin:
        # Forward the message to channel with verify button
        send_verify_button(CHANNEL_ID, message.text)

def main():
    """Main function to start the bot"""
    # Set webhook
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + '/')
    
    # Start Flask app
    # In production (Render), the SSL is handled by the platform
    if os.environ.get('RENDER'):
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8443)))
    else:
        # Local development with SSL
        app.run(host='0.0.0.0', port=8443, ssl_context=('cert.pem', 'key.pem'))

if __name__ == '__main__':
    main()