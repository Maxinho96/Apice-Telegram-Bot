import os
import re

from telegram.ext import Filters, MessageHandler, Updater

from custom_filters import RegexPreprocessingFilter
from promotec import get_lockers_state, get_lockers_amount

TOKEN = os.getenv("TOKEN")
APICE_ID = int(os.getenv("APICE_ID"))
MAX_ID = os.getenv("MAX_ID")
ANNA_ID = os.getenv("ANNA_ID")

def lotito(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Lotito!')

def apice(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Apice entrerà in Banca d\'Italia SICURO!')

def max(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Max farà entrare Apice in Prima SICURO!')

def apice_max(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Apice entrerà in Banca d\'Italia, altrimenti Max farà entrare Apice in Prima SICURO!')

def roma(bot, update):
    message = update.message or update.edited_message
    message.reply_text('as roma MERDA! 💩')

def lazio(bot, update):
    message = update.message or update.edited_message
    message.reply_text('Avanti Lazio! 🦅')

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

last_lockers_state = {}
last_lockers_amount = None

def check_lockers_state(bot, job):
    global last_lockers_state
    current_lockers_state = get_lockers_state()
    if current_lockers_state and current_lockers_state != last_lockers_state:
        used_lockers = [num for num, is_available in current_lockers_state.items() if not is_available]
        unused_lockers = [num for num, is_available in current_lockers_state.items() if is_available]

        locker_rows = sorted(
            current_lockers_state.items(),
            key=lambda item: (str(item[0]).isdigit(), str(item[0]))
        )
        locker_list = "\n".join(
            f"{locker_num} {'🟢' if is_available else '🔴'}"
            for locker_num, is_available in locker_rows
        )

        message = (
            "Stato locker aggiornato\n"
            f"🔴 Usati: {len(used_lockers)} | 🟢 Liberi: {len(unused_lockers)}\n"
            f"{locker_list}"
        )
        bot.send_message(
            chat_id=ANNA_ID, 
            text=message
        )
        bot.send_message(
            chat_id=MAX_ID, 
            text=message
        )

        last_lockers_state = current_lockers_state

def check_lockers_amount(bot, job):
    global last_lockers_amount
    current_lockers_amount = get_lockers_amount()
    if current_lockers_amount and current_lockers_amount != last_lockers_amount:
        amount_line = f"💰 Totale incassi: {current_lockers_amount:.2f} €"

        if last_lockers_amount is not None:
            delta = current_lockers_amount - last_lockers_amount
            trend_emoji = "📈" if delta > 0 else "📉" if delta < 0 else "➖"
            trend_line = f"\n{trend_emoji} Variazione: {delta:.2f} €"
            amount_line += trend_line

        message = (
            f"Incassi aggiornati\n{amount_line}"
        )
        bot.send_message(
            chat_id=ANNA_ID, 
            text=message
        )
        bot.send_message(
            chat_id=MAX_ID, 
            text=message
        )

        last_lockers_amount = current_lockers_amount

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    job_queue = updater.job_queue
    job_queue.run_repeating(check_lockers_state, interval=60*5, first=0)
    job_queue.run_repeating(check_lockers_amount, interval=60*5, first=0)

    regex_apice = "(" + word_to_regex("apice") + "|" + word_to_regex("チェ") + ")"
    regex_max = "(" + word_to_regex("max") + "|" + word_to_regex("massi") + "|" + word_to_regex("bruni") + ")"
    regex_stocazzo = word_to_regex("sto cazzo")
    regex_lotito = "[^A-z]chi[^A-z]|^chi[^A-z]|[^A-z]chi$|^chi$$"
    regex_roma = word_to_regex("roma")
    regex_lazio = word_to_regex("lazio")

    pattern_apice_max = re.compile(regex_apice + regex_max, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_apice_max), apice_max, edited_updates=True))

    pattern_apice = re.compile(regex_apice, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_apice), apice, edited_updates=True))
    
    pattern_max = re.compile(regex_max, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_max), max, edited_updates=True))

    pattern_stocazzo = re.compile(regex_stocazzo, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_stocazzo) & Filters.user(user_id=APICE_ID), apice, edited_updates=True))

    pattern_lotito = re.compile(regex_lotito, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_lotito), lotito, edited_updates=True))

    pattern_roma = re.compile(regex_roma, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_roma), roma, edited_updates=True))

    pattern_lazio = re.compile(regex_lazio, re.IGNORECASE | re.DOTALL)
    dp.add_handler(MessageHandler(RegexPreprocessingFilter(pattern_lazio), lazio, edited_updates=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
