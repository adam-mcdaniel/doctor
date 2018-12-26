import time
from random import randint, choice

from easy_mobile.setup import SCREEN_WIDTH, SCREEN_HEIGHT
from easy_mobile.sprite import Sprite

from .__init__ import *
from .tiles import *
from .pieces import *


class Player:
    def __init__(self, screen, cutscene, text):
        from .__init__ import WIDTH, HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, START_HEIGHT
        self.screen = screen
        self.winner = None
        self.cutscene = cutscene

        self.time = time.time()

        self.next_init = None
        self.next_update = None

        self.veil = Sprite(0, SCREEN_HEIGHT - START_HEIGHT+WIDTH/8,
                           image=BS, width=SCREEN_WIDTH, height=START_HEIGHT)

        self.first = True
        self.wait_time = time.time() - 4
        self.index = -1
        self.list_of_texts = text
        self.text = Sprite(0, SCREEN_HEIGHT - START_HEIGHT,
                           image=self.list_of_texts[self.index], width=SCREEN_WIDTH, height=SCREEN_WIDTH/4)
        self.text_time = time.time()

        self.state = lambda: self.transition(self.speak, self.state)
        # self.state()

    def speak(self):
        if len(self.list_of_texts) > 0:
            self.text.color[3] = 0
            self.screen.remove(self.text)
            self.index = (self.index + 1) % (len(self.list_of_texts))
            self.text = Sprite(0, SCREEN_HEIGHT - START_HEIGHT,
                               image=self.list_of_texts[self.index], width=SCREEN_WIDTH, height=SCREEN_WIDTH/4)
            self.text.color[3] = 0
            self.text_time = time.time()
            self.screen.append(self.text)
        else:
            self.screen.remove(self.text)

        if self.first:
            del self.list_of_texts[0]
            self.first = False
            self.index = -1
        else:
            self.wait_time = time.time()

    def update(self):
        if time.time() - self.wait_time > 3:
            self.state()
        if time.time() - self.text_time > 0.1:
            self.text.color[3] = 1
            self.text_time = time.time() + 1000000000000000000000000

    def show(self):
        for sprite in self.screen:
            sprite.color[3] = 1

    def hide(self):
        for sprite in self.screen:
            sprite.color[3] = 0

    def getWinner(self):
        winner = None
        lenWhite = 0
        lenBlack = 0
        for sprite in self.screen:
            if isinstance(sprite, WhitePiece):
                lenWhite += 1
            if isinstance(sprite, BlackPiece):
                lenBlack += 1

        if not lenWhite > 0:
            winner = "black"
        elif not lenBlack > 0:
            winner = "white"

        return winner

    def move(self):
        # time.sleep(0.1)

        test_time = time.time()

        best_value = -10000000000000000000
        best_move = None
        for sprite in self.screen:
            if isinstance(sprite, BlackPiece):
                for move in sprite.getMoves(self.screen):
                    sx, sy = sprite.toBoardPos(sprite.getX(),
                                               sprite.getY())
                    value = evalMove(self.screen, *move, sx, sy,
                                     isQueen=isinstance(sprite, BlackQueen))
                    current_value = evalMove(self.screen, sx, sy,
                                             isQueen=isinstance(sprite, BlackQueen))
                    if value > best_value and value > current_value:
                        best_move = (sprite, move)
                        best_value = value

                    if time.time() - test_time > 0.8:
                        break

        if best_move:
            print(best_value)
            best_move[0].movePiece(*best_move[1])
        else:
            print("no best move")
            done = False
            n = 0
            while not done:
                for sprite in self.screen:
                    if isinstance(sprite, BlackPiece):
                        if not randint(0, 10):
                            moves = list(sprite.getMoves(self.screen))
                            if len(moves) > 0:
                                sprite.movePiece(*choice(moves))
                                done = True
                                break
                            n += 1
                if n > 20:
                    break

        print(time.time() - test_time)
        print("black player moved")

    def buildGame(self):
        self.hide()
        self.screen.clear()

        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))

        for x in range(0, BOARD_WIDTH):
            self.screen.append(
                Sprite(
                    x*WIDTH,
                    BOARD_HEIGHT*WIDTH + START_HEIGHT,
                    image='img/BorderBottomSide.png',
                    width=WIDTH,
                    height=HEIGHT
                )
            )
            self.screen.append(
                Sprite(
                    x*WIDTH,
                    -WIDTH + START_HEIGHT,
                    image='img/BorderTopSide.png',
                    width=WIDTH,
                    height=HEIGHT
                )
            )

        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if not y in [int(BOARD_HEIGHT/2), int(BOARD_HEIGHT/2)-1]:
                    # if not y in [int(BOARD_HEIGHT/2)-1, int(BOARD_HEIGHT/2), int(BOARD_HEIGHT/2)+1]:
                    self.screen.append(
                        Tile(
                            x*WIDTH,
                            y*WIDTH + START_HEIGHT,
                            image=WS if (x+y) % 2 == 1 else BS,
                            width=WIDTH,
                            height=HEIGHT
                        )
                    )
                else:
                    if x in [1, 2, 3, 4, 5]:
                        self.screen.append(
                            Tile(
                                x*WIDTH,
                                y*WIDTH + START_HEIGHT,
                                image=WS if (x+y) % 2 == 1 else BS,
                                width=WIDTH,
                                height=HEIGHT
                            )
                        )
                    else:
                        if y == int(BOARD_HEIGHT/2)-1:
                            if x == 0:
                                self.screen.append(
                                    EmptyTile(
                                        x*WIDTH,
                                        y*WIDTH + START_HEIGHT,
                                        image='img/BorderBottomRight.png',
                                        width=WIDTH,
                                        height=HEIGHT
                                    )
                                )
                            if x == 3:
                                self.screen.append(
                                    EmptyTile(
                                        x*WIDTH,
                                        y*WIDTH + START_HEIGHT,
                                        image='img/BorderBottomHalf.png',
                                        width=WIDTH,
                                        height=HEIGHT
                                    )
                                )
                            if x == 6:
                                self.screen.append(
                                    EmptyTile(
                                        x*WIDTH,
                                        y*WIDTH + START_HEIGHT,
                                        image='img/BorderBottomLeft.png',
                                        width=WIDTH,
                                        height=HEIGHT
                                    )
                                )
                        else:
                            if x == 0:
                                self.screen.append(
                                    EmptyTile(
                                        x*WIDTH,
                                        y*WIDTH + START_HEIGHT,
                                        image='img/BorderTopRight.png',
                                        width=WIDTH,
                                        height=HEIGHT
                                    )
                                )
                            if x == 3:
                                self.screen.append(
                                    EmptyTile(
                                        x*WIDTH,
                                        y*WIDTH + START_HEIGHT,
                                        image='img/BorderTopHalf.png',
                                        width=WIDTH,
                                        height=HEIGHT
                                    )
                                )
                            if x == 6:
                                self.screen.append(
                                    EmptyTile(
                                        x*WIDTH,
                                        y*WIDTH + START_HEIGHT,
                                        image='img/BorderTopLeft.png',
                                        width=WIDTH,
                                        height=HEIGHT
                                    )
                                )

        # self.screen.append(WhitePawn(3, 0))
        # self.screen.append(BlackPawn(4, BOARD_HEIGHT-1))
        for y in range(0, 3):
            for x in range(0, BOARD_WIDTH):
                if y == 1:
                    if x % 2 == 0:
                        self.screen.append(choice([WhitePawn if x != 0 and x != 6 else WhiteKnight,
                                                   WhitePawn if x != 0 and x != 6 else WhiteCastle,
                                                   WhitePawn if x != 0 and x != 6 else WhiteKing,
                                                   WhitePawn if x != 0 and x != 6 else WhiteKnight,
                                                   WhiteKnight, WhiteKnight, WhiteCastle, WhiteKing, WhiteQueen])(x, y))
                else:
                    if x in [0, 1, 3, 5, 6]:
                        self.screen.append(choice([WhitePawn if x != 0 and x != 6 and x != 3 else WhiteCastle,
                                                   WhitePawn if x != 0 and x != 6 and x != 3 else WhiteKing,
                                                   WhitePawn if x != 0 and x != 6 and x != 3 else WhiteKnight,
                                                   WhiteCastle, WhiteCastle, WhiteKnight, WhiteKnight, WhiteKing, WhiteKing, WhiteQueen])(x, y))

        for y in range(0, 3):
            for x in range(0, BOARD_WIDTH):
                if y == 1:
                    if x % 2 == 0:
                        self.screen.append(choice([BlackPawn if x != 0 and x != 6 else BlackCastle,
                                                   BlackCastle, BlackCastle, BlackKnight, BlackKing, BlackQueen, BlackQueen])(x, BOARD_HEIGHT - y - 1))
                else:
                    if x in [0, 1, 3, 5, 6]:
                        self.screen.append(
                            choice([BlackCastle, BlackQueen])(x, BOARD_HEIGHT - y - 1))

    def veilInit(self):
        self.veil.color[3] = 0
        self.time = time.time()
        self.screen.append(self.veil)

    def veilUpdateOne(self):
        if not self.veil.color[3] >= 1:
            self.veil.color[3] += (time.time() - self.time)/250
        else:
            self.next_init()
            self.screen.remove(self.veil)
            self.screen.append(self.veil)
            self.time = time.time() + 3
            self.state = self.veilUpdateTwo

    def veilUpdateTwo(self):
        if not self.veil.color[3] <= 0:
            self.veil.color[3] -= (time.time() - self.time)/300
        else:
            self.screen.remove(self.veil)
            self.state = self.next_update
            self.wait_time = time.time()

    def transition(self, init, update):
        self.next_init = init
        self.next_update = update

        self.veilInit()
        self.state = self.veilUpdateOne


class Mark(Player):
    def __init__(self, screen):
        super().__init__(screen,
                         Sprite(0, START_HEIGHT, image='img/mark_intro.png',
                                width=SCREEN_WIDTH, height=SCREEN_WIDTH),
                         [
                               'img/mark_speak/hello.png',
                             #   'img/mark_speak/i_dont_feel_well.png',
                             #   'img/mark_speak/my_heart_is_heavy.png',
                             #   'img/mark_speak/i_feel_alone.png',
                             #   'img/mark_speak/what_do_i_do.png',
                             #   'img/mark_speak/im_glad.png',
                             #   'img/mark_speak/i_get_afraid.png',
                             #   'img/mark_speak/and_youre_nice.png',
                             #   'img/mark_speak/i_would_be_gone.png',
                             #   'img/mark_speak/in_my_bed.png',
                             #   'img/mark_speak/in_peaceful_sleep.png',
                             #   'img/mark_speak/i_wouldnt_hurt.png',
                             #   'img/mark_speak/maybe.png',
                             #   'img/mark_speak/would_be_better.png',
                             #   'img/mark_speak/if_i_were_gone.png',
                             #   'img/mark_speak/if_this_is_the_last.png',
                             #   'img/mark_speak/i_want_you_to_know.png',
                             #   'img/mark_speak/you_did_your_best.png',
                             #   'img/mark_speak/im_too_broken.png',
                             #   'img/mark_speak/so_goodbye.png',
                             #   'img/mark_speak/goodbye.png',
                         ])


class Lucy(Player):
    def __init__(self, screen):
        super().__init__(screen,
                         Sprite(0, START_HEIGHT, image='img/lucy_intro.png',
                                width=SCREEN_WIDTH, height=SCREEN_WIDTH),
                         [
                             'img/lucy_speak/hello.png',
                            #  'img/lucy_speak/i_had_an_episode.png',
                            #  'img/lucy_speak/i_sat_in_my_room.png',
                            #  'img/lucy_speak/im_so_sorry.png',
                            #  'img/lucy_speak/i_grabbed_my_knife.png',
                            #  'img/lucy_speak/and_i_felt_the_blade.png',
                            #  'img/lucy_speak/it_made_me_feel_at_home.png',
                            #  'img/lucy_speak/it_didnt_feel_good.png',
                            #  'img/lucy_speak/but_it_felt_easier.png',
                         ])

    def buildGame(self):
        self.hide()
        self.screen.clear()

        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))

        for x in range(1, BOARD_WIDTH-1):
            self.screen.append(
                EmptyTile(
                    x*WIDTH,
                    (BOARD_HEIGHT-1)*WIDTH + START_HEIGHT,
                    image='img/BorderBottomSide.png',
                    width=WIDTH,
                    height=HEIGHT
                )
            )
            self.screen.append(
                EmptyTile(
                    x*WIDTH,
                    START_HEIGHT,
                    image='img/BorderTopSide.png',
                    width=WIDTH,
                    height=HEIGHT
                )
            )

        self.screen.append(
            EmptyTile(
                0*WIDTH,
                START_HEIGHT,
                image='img/CornerTopRight.png',
                width=WIDTH,
                height=HEIGHT
            )
        )
        self.screen.append(
            EmptyTile(
                (BOARD_WIDTH-1)*WIDTH,
                START_HEIGHT,
                image='img/CornerTopLeft.png',
                width=WIDTH,
                height=HEIGHT
            )
        )

        self.screen.append(
            EmptyTile(
                0*WIDTH,
                START_HEIGHT + (BOARD_HEIGHT-1)*HEIGHT,
                image='img/CornerBottomRight.png',
                width=WIDTH,
                height=HEIGHT
            )
        )
        self.screen.append(
            EmptyTile(
                (BOARD_WIDTH-1)*WIDTH,
                START_HEIGHT + (BOARD_HEIGHT-1)*HEIGHT,
                image='img/CornerBottomLeft.png',
                width=WIDTH,
                height=HEIGHT
            )
        )

        for y in range(1, BOARD_HEIGHT-1):
            self.screen.append(
                EmptyTile(
                    0*WIDTH,
                    y*HEIGHT + START_HEIGHT,
                    image='img/BorderRightSide.png',
                    width=WIDTH,
                    height=HEIGHT
                )
            )
            self.screen.append(
                EmptyTile(
                    (BOARD_WIDTH-1)*WIDTH,
                    y*HEIGHT + START_HEIGHT,
                    image='img/BorderLeftSide.png',
                    width=WIDTH,
                    height=HEIGHT
                )
            )

        for y in range(1, BOARD_HEIGHT-1):
            for x in range(1, BOARD_WIDTH-1):
                self.screen.append(
                    Tile(
                        x*WIDTH,
                        y*WIDTH + START_HEIGHT,
                        image=WS if (x+y) % 2 == 1 else BS,
                        width=WIDTH,
                        height=HEIGHT
                    )
                )

        self.screen.append(WhiteBishop(2, 4))
        self.screen.append(WhiteBishop(2, 3))
        self.screen.append(WhiteBishop(4, 4))
        self.screen.append(WhiteBishop(4, 3))

        self.screen.append(WhiteCastle(3, 5))
        self.screen.append(WhiteCastle(3, 2))

        self.screen.append(WhitePawn(3, 4))
        self.screen.append(WhitePawn(3, 3))

        for y in range(1, BOARD_HEIGHT-1):
            for x in range(1, BOARD_WIDTH-1):
                if (y < 2 or y > BOARD_HEIGHT-3 or x < 2 or x > BOARD_WIDTH-3) and (((x + y) % 2 == 0 and y <= BOARD_HEIGHT/2) or ((x + y) % 2 == 1 and y >= BOARD_HEIGHT/2)):
                    self.screen.append(
                        choice([


                            BlackCastle,
                            BlackQueen,
                            BlackKnight,
                            BlackKnight,
                            BlackBishop,
                            BlackBishop


                        ])(x, BOARD_HEIGHT - y - 1)
                    )


class Ryan(Player):
    def __init__(self, screen):
        super().__init__(screen,
                         Sprite(0, START_HEIGHT, image='img/lucy_intro.png',
                                width=SCREEN_WIDTH, height=SCREEN_WIDTH),
                         [
                             'img/lucy_speak/hello.png',
                            #  'img/lucy_speak/i_had_an_episode.png',
                            #  'img/lucy_speak/i_sat_in_my_room.png',
                            #  'img/lucy_speak/im_so_sorry.png',
                            #  'img/lucy_speak/i_grabbed_my_knife.png',
                            #  'img/lucy_speak/and_i_felt_the_blade.png',
                            #  'img/lucy_speak/it_made_me_feel_at_home.png',
                            #  'img/lucy_speak/it_didnt_feel_good.png',
                            #  'img/lucy_speak/but_it_felt_easier.png',
                         ])

    def buildGame(self):
        self.hide()
        self.screen.clear()

        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))

        for x in range(0, BOARD_WIDTH):
            self.screen.append(
                EmptyTile(
                    x*WIDTH,
                    (BOARD_HEIGHT-1)*WIDTH + START_HEIGHT,
                    image='img/BorderBottomSide.png',
                    width=WIDTH,
                    height=HEIGHT
                )
            )
            self.screen.append(
                Sprite(
                    x*WIDTH,
                    START_HEIGHT-WIDTH,
                    image='img/BorderTopSide.png',
                    width=WIDTH,
                    height=HEIGHT
                )
            )

        for y in range(0, BOARD_HEIGHT-1):
            for x in range(0, BOARD_WIDTH):
                self.screen.append(
                    Tile(
                        x*WIDTH,
                        y*WIDTH + START_HEIGHT,
                        image=WS if (x+y) % 2 == 1 else BS,
                        width=WIDTH,
                        height=HEIGHT
                    )
                )

        for x in range(0, 7):
            self.screen.append(BlackPawn(x, 5))

        self.screen.append(BlackCastle(0, 6))
        self.screen.append(BlackCastle(6, 6))

        self.screen.append(BlackKnight(1, 6))
        self.screen.append(BlackKnight(5, 6))

        self.screen.append(BlackBishop(2, 6))
        self.screen.append(BlackBishop(4, 6))

        self.screen.append(BlackQueen(3, 6))

        for x in range(0, 7):
            self.screen.append(WhitePawn(x, 1))

        self.screen.append(WhiteCastle(0, 0))
        self.screen.append(WhiteCastle(6, 0))

        self.screen.append(WhiteKnight(1, 0))
        self.screen.append(WhiteKnight(5, 0))

        self.screen.append(WhiteBishop(2, 0))
        self.screen.append(WhiteBishop(4, 0))

        self.screen.append(WhiteQueen(3, 0))

        # for y in range(1, BOARD_HEIGHT-1):
        #     for x in range(1, BOARD_WIDTH-1):
        #         if (y < 2 or y > BOARD_HEIGHT-3 or x < 2 or x > BOARD_WIDTH-3) and (((x + y) % 2 == 0 and y <= BOARD_HEIGHT/2) or ((x + y) % 2 == 1 and y >= BOARD_HEIGHT/2)):
        #             self.screen.append(
        #                 choice([

        #                 BlackCastle,
        #                 BlackQueen,
        #                 BlackKnight,
        #                 BlackKnight,
        #                 BlackBishop,
        #                 BlackBishop

        #                 ])(x, BOARD_HEIGHT - y - 1)
        #                 )
