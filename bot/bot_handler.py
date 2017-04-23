import telebot
import os

from telebot import types

from django.core.exceptions import ObjectDoesNotExist

from accounts.models import User, Connection

if "BOTCASTER_BOT_TOKEN" not in os.environ:
    raise AssertionError("Please configure BOTCASTER_BOT_TOKEN as an environment variable")

bot = telebot.TeleBot(os.environ["BOTCASTER_BOT_TOKEN"])

## Messages ##

text_messages = {
    'help':
        u'BotCaster is a simple bot that allows you to follow links shared by others.\n'
        u'To follow: /follow <username>\n',
    'unknown_message':
        u'I didn\'t understand that.\n'
        u'For help: /help\n',
    'already_registerd':
        u'You already have an account with us!\n',
}

## Handle Links ##

@bot.message_handler(func=lambda m: is_link(m))
def handle_link(message):
    bot.reply_to(message, "That's a link, do you want to publish it to your feed?")
    # TODO: handle state

def is_link(message):
    if (message.entities):
        for entity in message.entities:
            if entity.type == "url":
                return True
    return False

## Handle commands ##

@bot.message_handler(commands=['follow'])
def handle_follow(message):
    # TODO: allow /follow username in one line
    user = User.objects.get(pk=message.chat.id)
    user.set_state(1)
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, 'username to follow', reply_markup = markup)

@bot.message_handler(func=lambda m: User.objects.get(pk=m.chat.id).get_state() == 1)
def handle_follow_1(message):
    follower = User.objects.get(pk=message.chat.id)
    try:
        following = User.objects.get(username=message.text)
        c = Connection(follower=follower, following=following)
        c.save()
        follower.set_state = 0
        bot.send_message(message.chat.id, 'Following @' + following.username)
    except ObjectDoesNotExist:
        bot.send_message(message.chat.id, 'username not found in our system')
        handle_follow(message) 

@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        user = User.objects.get(pk=message.chat.id)
        bot.send_message(message.chat.id, text_messages['already_registerd'])
    except ObjectDoesNotExist:
        user = User(
                    id=message.chat.id,
                    first_name=message.chat.first_name,
                    last_name=message.chat.last_name,
                    username=message.chat.username
        )
        user.save()
        bot.send_message(message.chat.id, text_messages['help'])

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, text_messages['help'])

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, text_messages['unknown_message'])

def main():
    bot.polling()

if __name__ == '__main__':
    main()