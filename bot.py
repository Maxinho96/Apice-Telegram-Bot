from telegram.ext import Updater, MessageHandler, Filters
import os
import re
from custom_filters import RegexPreprocessingFilter


def trentaelode(bot, update):
    message = update.message or update.edited_message
    message.reply_text('110 e lode')

def trentaelodemax(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Apice 110 e lode, Max bocciato')

def stocazzo(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Sto cazzo!')

def lotito(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Lotito!')

def prima(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Apice entra in Prima SICURO!')

def maxfigli(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Max avrà figli SICURO!')

def primamaxfigli(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Apice entra in Prima SICURO, Max avrà figli SICURO!')

# def delete_message(bot, update):
#     message = update.message or update.edited_message
#     bot.deleteMessage(chat_id=message.chat.id, message_id=message.message_id)

# Given a word, returns a regex which is robust to spaces, dots and repetitions to find that word in the sentence
def word_to_regex(word):
    regex = "(?=.*"
    for i, c in enumerate(word):
        regex += "[" + letter_to_chars(c) + "]+"
        if i < len(word) - 1:
            regex += "[\W_]*"
    regex += ")"
    return regex

# Given a letters, returns all chars similar to that letter (e.g. a is similar to 4)
def letter_to_chars(letter):
    dic = {"a": "a4🅰️",
           "b": "b🅱️",
           "c": "c",
           "d": "d",
           "e": "e3",
           "h": "h",
           "i": "i1",
           "l": "l",
           "m": "m",
           "n": "n",
           "o": "o0🅾️",
           "p": "p",
           "r": "r",
           "s": "s5",
           "t": "t7",
           "u": "u",
           "x": "x",
           "z": "z2",
           " ": " ",
           "?": "?"}
    return dic.get(letter, letter)


def main():
    TOKEN = os.getenv("TOKEN")
    APICE_ID = int(os.getenv("APICE_ID"))

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # pattern_apice_max = re.compile('(?=.*[a4]+[\W_]*p+[\W_]*[i1]+[\W_]*c+[\W_]*[e3]+)(?=.*((m|/\\\\/\\\\)+[\W_]*[a4]+[\W_]*(x+|s+[\W_]*[i1]+)|b+[\W_]*r+[\W_]*u+[\W_]*n+[\W_]*[i1]+)).*', re.IGNORECASE | re.DOTALL)
    regex_apice = "(" + word_to_regex("apice") + "|" + word_to_regex("チェ") + ")"
    regex_max = "(" + word_to_regex("max") + "|" + word_to_regex("massi") + "|" + word_to_regex("bruni") + ")"
    regex_30L = "(" + word_to_regex("trenta") + "|" + word_to_regex("lode") + "|" + "(?=.*3[\W_]*[0-9o]+)" + ")"
    regex_stocazzo = word_to_regex("sto cazzo")
    regex_lotito = "[^A-z]chi[^A-z]|^chi[^A-z]|[^A-z]chi$|^chi$$"
    regex_prima = word_to_regex("prima")

    pattern_apice_max = re.compile(regex_apice + regex_max, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_apice_max), primamaxfigli, edited_updates=True))

    # pattern_apice = re.compile('(?=.*[a4]+[\W_]*p+[\W_]*[i1]+[\W_]*c+[\W_]*[e3]+)', re.IGNORECASE | re.DOTALL)
    pattern_apice = re.compile(regex_apice, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_apice), prima, edited_updates=True))
    
    pattern_prima = re.compile(regex_prima, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_prima), prima, edited_updates=True))

    # pattern_max = re.compile('(?=.*((m|/\\\\/\\\\)+[\W_]*[a4]+[\W_]*(x+|s+[\W_]*[i1]+)|b+[\W_]*r+[\W_]*u+[\W_]*n+[\W_]*[i1]+))(?=.*([0-9]+[\W_]*[0-9o]+|t+[\W_]*r+[\W_]*[e3]+[\W_]*n+[\W_]*t+[\W_]*[a4]+|l+[\W_]*(o|0)+[\W_]*d+[\W_]*[e3]+)).*', re.IGNORECASE | re.DOTALL)
    pattern_max = re.compile(regex_max, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_max), maxfigli, edited_updates=True))

    pattern_stocazzo = re.compile(regex_stocazzo, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_stocazzo) & Filters.user(user_id=APICE_ID), prima, edited_updates=True))

    pattern_lotito = re.compile(regex_lotito, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_lotito), lotito, edited_updates=True))

    # PORT = int(os.environ.get("PORT", "8443"))
    # HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    # updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    # updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
