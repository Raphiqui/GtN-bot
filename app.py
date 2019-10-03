import json
import time
import pprint
import telepot
import requests
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

BOT_TOKEN = None
GRETTINGS = ["hello", "good morning", "good afternoon", "good evening", "hi", "hey", "morning"]

def greetings():
    return 'Hello there, we\'re about to start a little game called \'guess the number\', would you ike to join ?'

def handle(msg):
    """tion.
    :param msg: Message received by the bot
    """
    # Receive message and pass the command to call the corresponding func
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(f'Content type: {content_type} || chat type: {chat_type} || chat id: {chat_id}')
    # you can add more content type, like if someone send a picture
    if content_type == 'text':
        if msg['text'] == 'test':
            bot.sendMessage(chat_id, 'testing custom keyboard',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
                                ],
                                one_time_keyboard= True
                            ))
        else:
            result = features(msg.get("text").lower())
            if result:
                bot.sendMessage(chat_id, result) # send the response to the user


def features(command):
    """ Regroup all commands"""
    print(f'Command received: {command}')
    if any(ext in command for ext in GRETTINGS):
        return say_hello()
    elif command == '/start':
        return greetings()
    elif command.find('dog') != -1:
        return find_dog()


def say_hello():
    return 'Hello you, would you like a dog ?'


def find_dog():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def start():
    print(f'Hello there')


def fetch_conf():
    with open('conf.json') as json_data_file:
        data = json.load(json_data_file)
    return data["bot_token"]


if __name__ == '__main__':
    BOT_TOKEN = fetch_conf()
    pprint.pprint(BOT_TOKEN)
    bot = telepot.Bot(BOT_TOKEN)
    start()
    bot.message_loop(handle)

    print('Listening ...')
    while True:
        time.sleep(1)


