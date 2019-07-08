from telegram.ext import Updater, MessageHandler, Filters
import os
import re

def trentaelode(bot, update):
    message = update.message or update.edited_message
    message.reply_text('30 e lode')

def trentaelodemax(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Apice 30 e lode, Max bocciato')

def delete_message(bot, update):
    message = update.message or update.edited_message
    bot.deleteMessage(chat_id=message.chat.id, message_id=message.message_id)

def main():
    TOKEN = os.getenv("TOKEN")

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    pattern_apice_max = re.compile('(?=.*(a|4)\s*p\s*(i|1)\s*c\s*(e|3))(?=.*m\s*(a|4)\s*(x|s\s*s\s*(i|1))).*', re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(Filters.regex(pattern_apice_max), trentaelodemax, allow_edited=True))

    pattern_apice = re.compile('(?=.*(a|4)\s*p\s*(i|1)\s*c\s*(e|3))', re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(Filters.regex(pattern_apice), trentaelode, allow_edited=True))

    pattern_max = re.compile('(?=.*m\s*(a|4)\s*(x|s\s*s\s*(i|1)))(?=.*([0-9]\s*[0-9]|t\s*r\s*(e|3)\s*n\s*t\s*(a|4)|l\s*(o|0)\s*d\s*(e|3)|3o)).*', re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(Filters.regex(pattern_max), delete_message, allow_edited=True))

    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

if __name__ == '__main__':
    main()
