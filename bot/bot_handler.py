import telebot
import os

from telebot import types

if "BOTCASTER_BOT_TOKEN" not in os.environ:
    raise AssertionError("Please configure BOTCASTER_BOT_TOKEN as environment variable")

bot = telebot.TeleBot(os.environ["BOTCASTER_BOT_TOKEN"])

@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    bot.reply_to(message, "Hi, I am botcaster")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def main():
    bot.polling()

if __name__ == '__main__':
    main()