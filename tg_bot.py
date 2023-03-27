import os as _os
import time as _time

import dotenv as _env
import telebot as _tgbot

import services as _services

_env.load_dotenv()

token = _os.environ["TOKEN"]
channel = _os.environ["CHANNEL"]

bot = _tgbot.TeleBot(token)

is_running = False


def _parser():
    post_slug = ""
    posts2 = {}
    while is_running:
        posts = _services.check_news(post_slug, posts2)
        if posts != posts2:
            posts2 = _services.get_news()

        if posts != {}:
            post_slug = list(posts.keys())[0]
            for _, value in posts.items():
                title = value["title"]
                link = value["link"]
                bot.send_message(channel, f"{title}\n{link}")
        _time.sleep(15)


@bot.message_handler(commands=["start"])
def start_commands(message):
    global is_running
    if not is_running:
        is_running = True
        bot.reply_to(message, "Parser started.")
        _parser()
    else:
        bot.reply_to(message, "Parser is already running.")


@bot.message_handler(commands=["stop"])
def stop_commands(message):
    global is_running
    if is_running:
        is_running = False
        bot.reply_to(message, "Parser stopped.")
    else:
        bot.reply_to(message, "Parser is not running.")


bot.polling()
