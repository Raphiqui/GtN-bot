import random


def guess_set_up(sup_bound):
    number_to_guess = random.randint(1, sup_bound)
    return number_to_guess


def check_if_dead(lives):
    if lives == 0:
        return True
    else:
        return False


def update_end():
    return True


def update_lives(lives_used, lives):
    lives_used += 1
    lives -= 1
    return lives_used, lives


def update_step(step):
    """
    Used to update the global variable in charge of the process of the game
    :return: the global variable + 1
    """
    step += 1
    return step


def destroy_params():
    step = 0
    lives_used = 0
    lives = 0
    sup_bound = 0
    end = False
    return step, lives_used, lives, sup_bound, end


def update_game_params(lives_param, sup_bound_param):
    lives = lives_param
    sup_bound = sup_bound_param
    return lives, sup_bound
