import telebot
import os

from telebot import types

from django.core.exceptions import ObjectDoesNotExist

from accounts.models import User, Connection
from posts.models import Link

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
    markup = types.InlineKeyboardMarkup(row_width=2)
    yes = types.InlineKeyboardButton('Yes', callback_data="Y" + message.text)
    no = types.InlineKeyboardButton('No', callback_data="N")
    markup.add(yes, no)
    bot.send_message(message.chat.id, "That's a link, do you want to post it to your followers?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data[:1]=='Y')
def handle_link_callback_yes(call):
    #TODO get (optional) description for link object
    link = call.data[1:]
    user = User.objects.get(pk=call.from_user.id)
    Link(author=user, link=link, description="").save()
    followers = Connection.objects.filter(following__username=call.from_user.username)
    for f in followers:
        bot.send_message(f.follower.id,link)
    bot.edit_message_text(text="Sent to your followers!",chat_id=call.from_user.id, message_id=call.message.message_id)
    # bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id)
    bot.answer_callback_query(call.id, "") # may not be needed since removing markup

@bot.callback_query_handler(func=lambda call: call.data[:1]=='N')
def handle_link_callback_no(call):
    bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id)
    bot.answer_callback_query(call.id, "") # may not be needed since removing markup

def is_link(message):
    if (message.entities):
        for entity in message.entities:
            if entity.type == "url":
                return True
    return False

## Handle commands ##

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
        bot.send_message(message.chat.id, 'Following @' + following.username)
    except ObjectDoesNotExist:
        bot.send_message(message.chat.id, 'username not found in our system')
    finally:
        follower.set_state(0)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, text_messages['help'])

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    L = Link.objects.all()
    print(L)
    bot.send_message(message.chat.id, text_messages['unknown_message'])

def main():
    bot.polling()

if __name__ == '__main__':
    main()