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

    pattern_apice_max = re.compile('(?=.*[a4]+[\W_]*p+[\W_]*[i1]+[\W_]*c+[\W_]*[e3]+)(?=.*((m|/\\\\/\\\\)+[\W_]*[a4]+[\W_]*(x+|s+[\W_]*[i1]+)|b+[\W_]*r+[\W_]*u+[\W_]*n+[\W_]*[i1]+)).*', re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(Filters.regex(pattern_apice_max), trentaelodemax, allow_edited=True))

    pattern_apice = re.compile('(?=.*[a4]+[\W_]*p+[\W_]*[i1]+[\W_]*c+[\W_]*[e3]+)', re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(Filters.regex(pattern_apice), trentaelode, allow_edited=True))

    pattern_max = re.compile('(?=.*((m|/\\\\/\\\\)+[\W_]*[a4]+[\W_]*(x+|s+[\W_]*[i1]+)|b+[\W_]*r+[\W_]*u+[\W_]*n+[\W_]*[i1]+))(?=.*([0-9]+[\W_]*[0-9o]+|t+[\W_]*r+[\W_]*[e3]+[\W_]*n+[\W_]*t+[\W_]*[a4]+|l+[\W_]*(o|0)+[\W_]*d+[\W_]*[e3]+)).*', re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(Filters.regex(pattern_max), delete_message, allow_edited=True))

    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

if __name__ == '__main__':
    main()
