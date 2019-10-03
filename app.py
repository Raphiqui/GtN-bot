import json
import time
import pprint
import telepot
import requests
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

BOT_TOKEN = None
LIVES = None
SUP_BOUND = None
GRETTINGS = ["hello", "good morning", "good afternoon", "good evening", "hi", "hey", "morning"]
STEP = 0

def handle(msg):
    """tion.
    :param msg: Message received by the bot
    """
    # Receive message and pass the command to call the corresponding func
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(f'Content type: {content_type} || chat type: {chat_type} || chat id: {chat_id}')
    # you can add more content type, like if someone send a picture
    if content_type == 'text':
        if msg['text'] == '/start':
            bot.sendMessage(chat_id, 'Hello there, we\'re about to start a little game called \'guess the number\', would you ike to join ?',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
                                ],
                                one_time_keyboard= True
                            ))
        elif msg['text'] == 'Yes' and STEP == 0:
            result = program_rules()
            update_step()
            print(STEP)
            for token, item in enumerate(result):
                if item and token == 3:
                    bot.sendMessage(chat_id, item)
                else:
                    bot.sendMessage(chat_id, item,
                                    reply_markup=ReplyKeyboardMarkup(
                                        keyboard=[
                                            [KeyboardButton(text="1"), KeyboardButton(text="2"),
                                             KeyboardButton(text="3")]
                                        ],
                                        one_time_keyboard=True
                                    ))

        # elif STEP == 1:
        #     program_selection(int(msg.get("text")))
        #     STEP += 1
            # for token, item in enumerate(result):
            #     if item and token == 3:
            #         bot.sendMessage(chat_id, item)
            #     else:
            #         bot.sendMessage(chat_id, item,
            #                         reply_markup=ReplyKeyboardMarkup(
            #                             keyboard=[
            #                                 [KeyboardButton(text="1"), KeyboardButton(text="2"),
            #                                  KeyboardButton(text="3")]
            #                             ],
            #                             one_time_keyboard=True
            #                         ))
        else:
            result = features(msg.get("text").lower())
            if result:
                bot.sendMessage(chat_id, result)


def program_selection(msg):
    print(msg)
    print(type(msg))


def update_step():
    """
    Used to update the global variable in charge of the process of the game
    :return: the global variable + 1
    """
    global STEP
    STEP += 1
    return STEP


def program_rules():

    selection_message = ['Choose a program',
                         'Program 1 || easy mode || 10 lives || number between 0 and 10',
                         'Program 2 || medium mode || 5 lives || number between 0 and 15',
                         'Program 3 || hard mode || 1 lives || number between 0 and 20']
    return selection_message

    # program_input = input()
    #
    # try:
    #     program_input = int(program_input)
    #     if program_input == 1:
    #         lives = 10
    #         sup_bound = 10
    #         print('Easy mode have been selected || parameters: {0} lives and number is between 0 and {1}'
    #               .format(lives, sup_bound))
    #         start(lives, sup_bound)
    #     elif program_input == 2:
    #         lives = 5
    #         sup_bound = 15
    #         print('Medium mode have been selected || parameters: {0} lives and number is between 0 and {1}'
    #               .format(lives, sup_bound))
    #         start(lives, sup_bound)
    #     elif program_input == 3:
    #         lives = 1
    #         sup_bound = 20
    #         print('Hard mode have been selected || parameters: {0} live and number is between 0 and {1}'
    #               .format(lives, sup_bound))
    #         start(lives, sup_bound)
    #     elif program_input > 3:
    #         print('Please enter a number between 1 and 3 !')
    #         program_selection()
    #     elif program_input < 1:
    #         print('Please enter a number between 1 and 3 !')
    #         program_selection()
    # except ValueError:
    #     print('Only integer values are allowed !')
    #     program_selection()


def features(command):
    """ Regroup all commands"""
    print(f'Command received: {command}')
    if any(ext in command for ext in GRETTINGS):
        return say_hello()
    # elif command == 'yes' and STEP == 0:
    #     return program_selection()
    # elif command == 'no':
    #     return start()
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
    bot = telepot.Bot(BOT_TOKEN)
    start()
    bot.message_loop(handle)

    print('Listening ...')
    while True:
        time.sleep(1)


