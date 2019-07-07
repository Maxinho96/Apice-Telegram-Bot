from telegram.ext import Updater, MessageHandler, Filters
import os
import re

def trentaelode(bot, update):
    update.message.reply_text('30 e lode')

def delete_message(bot, update):
    bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

def main():
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN)
    
    dp = updater.dispatcher
    pattern_apice = re.compile('apice', re.IGNORECASE)
    dp.add_handler(MessageHandler(Filters.regex(pattern_apice), trentaelode))
    pattern_max = re.compile('max.*(3[0-9]|trenta)|(3[0-9]|trenta).*max', re.IGNORECASE)
    dp.add_handler(MessageHandler(Filters.regex(pattern_max), delete_message))

    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

if __name__ == '__main__':
    main()
