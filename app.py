import json
import time
import pprint
import random
import telepot
import requests
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

BOT_TOKEN = None
GUESS = None
LIVES = None
LIVES_USED = 0
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

        elif STEP == 1:
            result = program_selection(int(msg.get("text")))
            update_step()
            guess_set_up()
            print('Number to guess', GUESS)
            bot.sendMessage(chat_id, result)

        elif STEP == 2:
            update_lives()
            result = guess_session(int(msg.get("text")))
            bot.sendMessage(chat_id, result)
        elif STEP == 3:
            bot.sendMessage(chat_id, 'Mmmmh, not sure about what to do now .....')
        else:
            result = features(msg.get("text").lower())
            if result:
                bot.sendMessage(chat_id, result)


# TODO: add it into another file to import it
def update_game_params(lives_param, sup_bound_param):
    global LIVES, SUP_BOUND
    LIVES = lives_param
    SUP_BOUND = sup_bound_param
    return LIVES, SUP_BOUND


def check_if_dead():
    if LIVES == 0:
        return True
    else:
        return False
    # if LIVES == 0:
        # print(Fore.RED + 'Sorry, you loose !')
        # print(Fore.CYAN + 'Would you like to restart ? (Answer by Y/N)')
        # user_input_choice = input()
        #
        # if user_input_choice == 'Y':
        #     program_selection()
        # else:
        #     print(Fore.CYAN + 'Ok, see you soon !')
    #
    # else:
    #     print(Fore.YELLOW + 'You should try again, but be careful, you\'ve got {0} live(s) left'.format(lives))
    #     getting_user_input(lives, guess, lives_used, sup_bound)


def guess_session(user_input_number):
    if user_input_number == GUESS:
        return '🎉 You\'ve found it using '+ str(LIVES_USED) +' live(s), congratulations ! 🎉'
    elif user_input_number > GUESS:
        is_dead = check_if_dead()
        if is_dead:
            update_step()
            return '👎 Too bad, you loose 👎'
        else:
            return 'The number is lower than that'
    elif user_input_number < GUESS:
        is_dead = check_if_dead()
        if is_dead:
            update_step()
            return 'Too bad, you loose'
        else:
            return 'The number is higher than that'


# TODO: add it into another file to import it
def update_lives():
    global LIVES_USED, LIVES
    LIVES_USED += 1
    LIVES -= 1
    return LIVES_USED, LIVES


def program_selection(number_selected):
    if number_selected == 1:
        update_game_params(10, 10)
        return 'Easy mode have been selected || parameters: '+ str(LIVES) +' lives and number is between 0 and '+ str(SUP_BOUND)
    elif number_selected == 2:
        update_game_params(5, 15)
        return 'Medium mode have been selected || parameters: '+ str(LIVES) +' lives and number is between 0 and '+ str(SUP_BOUND)
    elif number_selected == 3:
        update_game_params(1, 20)
        return 'Hard mode have been selected || parameters: '+ str(LIVES) +' live and number is between 0 and '+ str(SUP_BOUND)


# TODO: add it into another file to import it
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


# TODO: add it into another file to import it
def guess_set_up():
    global GUESS
    GUESS = random.randint(1, SUP_BOUND)


def fetch_conf():
    with open('conf.json') as json_data_file:
        data = json.load(json_data_file)
    return data["bot_token"]


if __name__ == '__main__':
    BOT_TOKEN = fetch_conf()
    bot = telepot.Bot(BOT_TOKEN)

    bot.message_loop(handle)

    print('Listening ...')
    while True:
        time.sleep(1)


