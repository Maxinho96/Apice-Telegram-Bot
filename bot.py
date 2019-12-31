from telegram.ext import Updater, MessageHandler, Filters
import os
import re


def trentaelode(bot, update):
    message = update.message or update.edited_message
    message.reply_text('30 e lode')

def trentaelodemax(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Apice 30 e lode, Max bocciato')

def stocazzo(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Sto cazzo!')

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
    dic = {"a": "a4",
           "b": "b",
           "c": "c",
           "d": "d",
           "e": "e3",
           "i": "i1",
           "l": "l",
           "m": "m",
           "n": "n",
           "o": "o0",
           "p": "p",
           "r": "r",
           "s": "s",
           "t": "t",
           "u": "u",
           "x": "x",
           "z": "z2",
           " ": " "}
    return dic[letter]


def main():
    TOKEN = os.getenv("TOKEN")

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # pattern_apice_max = re.compile('(?=.*[a4]+[\W_]*p+[\W_]*[i1]+[\W_]*c+[\W_]*[e3]+)(?=.*((m|/\\\\/\\\\)+[\W_]*[a4]+[\W_]*(x+|s+[\W_]*[i1]+)|b+[\W_]*r+[\W_]*u+[\W_]*n+[\W_]*[i1]+)).*', re.IGNORECASE | re.DOTALL)
    regex_apice = word_to_regex("apice")
    regex_max = "(" + word_to_regex("max") + "|" + word_to_regex("massi") + "|" + word_to_regex("bruni") + ")"
    regex_30L = "(" + word_to_regex("trenta") + "|" + word_to_regex("lode") + "|" + "(?=.*3[\W_]*[0-9o]+)" + ")"
    regex_stocazzo = word_to_regex("sto cazzo")

    pattern_apice_max = re.compile(regex_apice + regex_max, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(Filters.regex(pattern_apice_max), trentaelodemax, edited_updates=True))

    # pattern_apice = re.compile('(?=.*[a4]+[\W_]*p+[\W_]*[i1]+[\W_]*c+[\W_]*[e3]+)', re.IGNORECASE | re.DOTALL)
    pattern_apice = re.compile(regex_apice, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(Filters.regex(pattern_apice), trentaelode, edited_updates=True))

    # pattern_max = re.compile('(?=.*((m|/\\\\/\\\\)+[\W_]*[a4]+[\W_]*(x+|s+[\W_]*[i1]+)|b+[\W_]*r+[\W_]*u+[\W_]*n+[\W_]*[i1]+))(?=.*([0-9]+[\W_]*[0-9o]+|t+[\W_]*r+[\W_]*[e3]+[\W_]*n+[\W_]*t+[\W_]*[a4]+|l+[\W_]*(o|0)+[\W_]*d+[\W_]*[e3]+)).*', re.IGNORECASE | re.DOTALL)
    pattern_max30L = re.compile(regex_max + regex_30L)
    dp.add_handler(MessageHandler(Filters.regex(pattern_max30L), stocazzo, edited_updates=True))

    pattern_stocazzo = re.compile(regex_stocazzo)
    dp.add_handler(MessageHandler(Filters.regex(regex_stocazzo) | Filters.user(user_id="256936733"), trentaelode, edited_updates=True))

    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))


if __name__ == '__main__':
    main()
