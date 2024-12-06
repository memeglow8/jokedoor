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

@app.route('/', methods=['POST', 'GET', 'HEAD'])
def webhook():
    """Handle webhook requests from Telegram"""
    if request.method == 'POST':
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return Response('ok', status=200)
        else:
            return Response('error', status=403)
    else:
        # Handle HEAD and GET requests
        return Response('Bot webhook is active', status=200)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """Forward messages to channel with verify button"""
    try:
        # Forward the message to channel with verify button
        send_verify_button(CHANNEL_ID, message.text)
        # Send confirmation to the sender
        bot.reply_to(message, "Message forwarded to channel successfully!")
    except Exception as e:
        print(f"Error forwarding message: {e}")
        bot.reply_to(message, "Sorry, couldn't forward your message. Please try again.")

def main():
    """Main function to start the bot"""
    # Set webhook
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + '/')
    
    # Start Flask app
    # In production (Render), the SSL is handled by the platform
    if os.environ.get('RENDER'):
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
    else:
        # Local development without SSL for testing
        app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    main()
