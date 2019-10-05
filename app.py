import json
import time
import pprint
import telepot
import requests
import utilities
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

END = False # Used to control at which step of the game we're
BOT_TOKEN = None # Store the bot token after parsing
declaration = lambda n: [0 for _ in range(n)]
GUESS, LIVES, LIVES_USED, SUP_BOUND, STEP = declaration(5) # Set up those parameters to 0
GRETTINGS = ["hello", "good morning", "good afternoon", "good evening", "hi", "hey", "morning"]

def handle(msg):
    """
    Check the input of the user to redirect it in the correct part of the game
    :param msg: input from the user
    :return: string ad message to display to the user with some customization
    """
    # Receive message and pass the command to call the corresponding func
    global GUESS, STEP, LIVES_USED, LIVES, SUP_BOUND, END
    print(STEP)
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(f'Content type: {content_type} || chat type: {chat_type} || chat id: {chat_id}')
    # you can add more content type, like if someone send a picture
    if content_type == 'text':
        if msg['text'] == '/start':
            bot.sendMessage(chat_id, 'Hello there, we\'re about to start a little game called \'guess the number\', would you like to join ?',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
                                ],
                                one_time_keyboard= True
                            ))
        elif msg['text'] == '/stop':
            utilities.destroy_params()
        elif (msg['text'] == 'Yes' and STEP == 0) or (msg['text'] == 'Yes' and STEP == 2):
            if STEP == 2:
                STEP, LIVES_USED, LIVES, SUP_BOUND, END = utilities.destroy_params()

            result = program_rules()
            STEP = utilities.update_step(STEP)
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
        elif (STEP == 2 and msg['text'] == 'No') or (STEP == 0 and msg['text'] == 'No'):
            STEP, LIVES_USED, LIVES, SUP_BOUND, END = utilities.destroy_params()
            bot.sendMessage(chat_id, 'Ok then, when you\'ll be in a better mood just ask me with "/start" 😉')
        elif STEP == 1:
            result = program_selection(int(msg.get("text")))
            STEP = utilities.update_step(STEP)
            GUESS = utilities.guess_set_up(SUP_BOUND)
            print('Number to guess', GUESS)
            bot.sendMessage(chat_id, result)
        elif STEP == 2:
            LIVES_USED, LIVES = utilities.update_lives(LIVES_USED, LIVES)
            result = guess_session(int(msg.get("text")))
            if END:
                STEP, LIVES_USED, LIVES, SUP_BOUND, END = utilities.destroy_params()
                bot.sendMessage(chat_id, result)
                bot.sendMessage(chat_id,
                                'Would you like to play again ?',
                                reply_markup=ReplyKeyboardMarkup(
                                    keyboard=[
                                        [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
                                    ],
                                    one_time_keyboard=True
                                ))
            else:
                bot.sendMessage(chat_id, result)
        else:
            result = features(msg.get("text").lower())
            if result:
                bot.sendMessage(chat_id, result)


def guess_session(user_input_number):
    """
    Game session which will check according to what the user has entered the result of the game
    :param user_input_number: integer entered by the user in order to find the correct answer
    :return: string to display if he has won, lost or if the number is higher or lower than his answer
    """
    global END
    if user_input_number == GUESS:
        END = utilities.update_end()
        return '🎉 You\'ve found it using '+ str(LIVES_USED) +' live(s), congratulations ! 🎉'
    elif user_input_number > GUESS:
        is_dead = utilities.check_if_dead(LIVES)
        if is_dead:
            END = utilities.update_end()
            return '👎 Too bad, you loose 👎'
        else:
            return 'The number is lower than that'
    elif user_input_number < GUESS:
        is_dead = utilities.check_if_dead(LIVES)
        if is_dead:
            END = utilities.update_end()
            return '👎 Too bad, you loose 👎'
        else:
            return 'The number is higher than that'


def program_selection(number_selected):
    """
    Display which mode has been selected by the user
    :param number_selected: integer corresponding to a mode of playing
    :return: string to display which mode has been selected
    """
    global LIVES, SUP_BOUND
    if number_selected == 1:
        LIVES, SUP_BOUND = utilities.update_game_params(10, 10)
        return 'Easy mode have been selected || parameters: '+ str(LIVES) +' lives and number is between 0 and '+ str(SUP_BOUND)
    elif number_selected == 2:
        LIVES, SUP_BOUND = utilities.update_game_params(5, 15)
        return 'Medium mode have been selected || parameters: '+ str(LIVES) +' lives and number is between 0 and '+ str(SUP_BOUND)
    elif number_selected == 3:
        LIVES, SUP_BOUND = utilities.update_game_params(1, 20)
        return 'Hard mode have been selected || parameters: '+ str(LIVES) +' live and number is between 0 and '+ str(SUP_BOUND)


def program_rules():
    """
    Display the rules of the game
    :return: array containing the rules
    """
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
    elif command.find('dog') != -1:
        return find_dog()


def say_hello():
    return 'Hello you, would you like a dog ?'


def find_dog():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def fetch_conf():
    """
    Parses the configuration file to fetch the bot's token
    :return: token as string from telegram bot application
    """
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


