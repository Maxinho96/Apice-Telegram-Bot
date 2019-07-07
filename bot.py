from telegram.ext import Updater, MessageHandler, Filters
import os
import re

def trentaelode(bot, update):
    update.message.reply_text('30 e lode')

def main():
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN)
    
    dp = updater.dispatcher
    pattern = re.compile('apice', re.IGNORECASE)
    dp.add_handler(MessageHandler(Filters.regex(pattern), trentaelode))

    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

if __name__ == '__main__':
    main()
