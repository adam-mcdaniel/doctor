from easy_mobile.setup import SCREEN_WIDTH, SCREEN_HEIGHT

NUMBER_OF_PATIENTS_UNLOCKED = 1
with open("save/number_of_patients_unlocked") as f:
    NUMBER_OF_PATIENTS_UNLOCKED = int(f.read().replace('\n', ''))
    NUMBER_OF_PATIENTS_UNLOCKED = max(NUMBER_OF_PATIENTS_UNLOCKED, 1)
    f.close()


def unlockPatient():
    global NUMBER_OF_PATIENTS_UNLOCKED
    NUMBER_OF_PATIENTS_UNLOCKED += 1
    with open("save/number_of_patients_unlocked", 'w') as f:
        # NUMBER_OF_PATIENTS_UNLOCKED = int(f.read().replace('\n', ''))
        f.write(str(NUMBER_OF_PATIENTS_UNLOCKED))
        f.close()


WS = 'img/WhiteSquare.png'
BS = 'img/BlackSquare.png'
ES = 'img/EmptySquare.png'

BOARD_HEIGHT = 8
BOARD_WIDTH = 7

WIDTH = SCREEN_WIDTH / BOARD_WIDTH
HEIGHT = WIDTH

START_HEIGHT = (SCREEN_HEIGHT - (HEIGHT * BOARD_HEIGHT))/2


# def setBoardSize(w, h):
#     global BOARD_HEIGHT, BOARD_WIDTH

#     BOARD_HEIGHT = h
#     BOARD_WIDTH = w

#     WIDTH = SCREEN_WIDTH / BOARD_WIDTH
#     HEIGHT = WIDTH

#     START_HEIGHT = (SCREEN_HEIGHT - (HEIGHT * BOARD_HEIGHT))/2
