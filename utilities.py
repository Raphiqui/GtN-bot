import random


def guess_set_up(sup_bound):
    """
    Set up the number to guess according to the mode selected by the user
    :param sup_bound: max range which can be selected
    :return: integer as the number to guess
    """
    number_to_guess = random.randint(1, sup_bound)
    return number_to_guess


def check_if_dead(lives):
    """
    Check if the user looses the game
    :param lives: lives which remains to the user
    :return: boolean as if the user looses or not
    """
    if lives == 0:
        return True
    else:
        return False


def update_end():
    """
    Update the value of ending session to go to 'play again' mode
    :return: boolean as if the game session is over or not
    """
    return True


def update_lives(lives_used, lives):
    """
    Updates the lives which remains to the user
    :param lives_used: integer for how many lives hes has used
    :param lives: integer for how many lives remains
    :return: integers, the lives used and how many remains
    """
    lives_used += 1
    lives -= 1
    return lives_used, lives


def update_step(step):
    """
    Used to update the global variable in charge of the process of the game to
    see at which step of the game we're
    :return: the global variable + 1
    """
    step += 1
    return step


def reset_params():
    """
    Reset all params selected during the previous session
    :return: all params reseated
    """
    step = 0
    lives_used = 0
    lives = 0
    sup_bound = 0
    end = False
    return step, lives_used, lives, sup_bound, end


def update_game_params(lives_param, sup_bound_param):
    """
    Set up the game parameters according to the mode selected
    :param lives_param: integers for how many lives the user will get
    :param sup_bound_param: interger for what's the range of number
    :return: integers for lives and range selected
    """
    lives = lives_param
    sup_bound = sup_bound_param
    return lives, sup_bound
