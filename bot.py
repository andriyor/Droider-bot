import os
import time
from threading import Thread

import feedparser
import telebot

from models import User, Droider, YouTube

token = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token)

youtube_link = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCY03gpyR__MuJtBpoSyIGnw'
droider = 'http://droider.ru/feed/'
d = feedparser.parse(droider)
y = feedparser.parse(youtube_link)


def send_you():
    l = [i.link for i in YouTube.objects]
    for v in y.entries:
        if v.link not in l:
            YouTube(title=v.title, link=v.link, published=v.published).save()
            for user in User.objects:
                bot.send_message(user.chat_id, v.link)


def send_dro():
    l = [i.link for i in Droider.objects]
    for v in d.entries:
        if v.link not in l:
            Droider(title=v.title, link=v.link, published=v.published).save()
            for user in User.objects:
                bot.send_message(user.chat_id, v.link)


def event_loopy():
    while True:
        send_you()
        send_dro()
        time.sleep(30)

Thread(target=event_loopy).start()


@bot.message_handler(commands=['start'])
def handle_start(message):
    user = User.get_by_chat_id(message.chat.id)
    if user is None:
        User(first_name=message.chat.first_name, last_name=message.chat.last_name,
             chat_id=message.chat.id, username=message.chat.username).save()
    bot.send_message(message.chat.id, 'Hello')


if __name__ == '__main__':
    bot.polling()
