import time
from random import randint, choice

from easy_mobile.setup import SCREEN_WIDTH, SCREEN_HEIGHT
from easy_mobile.sprite import Sprite

from entities import *
from entities.tiles import *
from entities.pieces import *
from entities.menus import *

from ogg.music import MusicManager


class Doctor:
    def __init__(self, screen):
        self.music = MusicManager([
            'ogg/disintegration.ogg',
            'ogg/collapse.ogg',
            'ogg/dont_die.ogg',
            'ogg/hopeless.ogg',
            'ogg/rise_and_fall.ogg'
        ])

        self.screen = screen

        self.player = None

        self.menu = None
        self.moved = 3

        self.time = time.time()

        self.next_init = None
        self.next_update = None

        self.veil = Sprite(
            0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

        self.state = self.introInit

        # uncomment to skip intro
        # self.transition(self.mainMenuInit, self.mainMenuUpdate)

        self.state()

    # intro

    def introInit(self):
        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))
        self.screen.append(Sprite(0, (SCREEN_HEIGHT - SCREEN_WIDTH)/2,
                                  image="presplash.png", width=SCREEN_WIDTH, height=SCREEN_WIDTH))
        self.state = self.introUpdate

    def introUpdate(self):
        if time.time() - self.time > 4:
            self.transition(self.welcomeDoctorInit,
                            self.welcomeDoctorUpdate)

    def welcomeDoctorInit(self):
        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))
        self.screen.append(Sprite(0, (SCREEN_HEIGHT - SCREEN_WIDTH)/2,
                                  image="img/welcome_doctor.png", width=SCREEN_WIDTH, height=SCREEN_WIDTH))

    def welcomeDoctorUpdate(self):
        if time.time() - self.time > 5:
            self.transition(self.playAGameInit,
                            self.playAGameUpdate)

    def playAGameInit(self):
        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))
        self.screen.append(Sprite(0, (SCREEN_HEIGHT - SCREEN_WIDTH)/2,
                                  image="img/play_a_game.png", width=SCREEN_WIDTH, height=SCREEN_WIDTH))

    def playAGameUpdate(self):
        if time.time() - self.time > 5:
            self.transition(self.mainMenuInit,
                            self.mainMenuUpdate)

    # end intro

    def mainMenuInit(self):
        self.screen.clear()
        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))
        self.menu = MainMenu(self.screen)

    def mainMenuUpdate(self):
        self.menu.update()
        if self.menu.getStart():
            self.transition(self.selectPatientInit,
                            self.selectPatientUpdate)
        elif self.menu.getCredits():
            self.transition(self.creditsInit,
                            self.creditsUpdate)

    def selectPatientInit(self):
        self.screen.clear()
        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))
        self.menu = PatientMenu(self.screen)

    def selectPatientUpdate(self):
        self.menu.update()
        self.player = self.menu.getPatient()
        if self.player:
            def f():
                time.sleep(5)
                self.transition(self.gameInit,
                                self.gameUpdate)

            self.transition(
                self.playerCutscene,
                f
            )

    def playerCutscene(self):
        self.screen.clear()
        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))
        self.screen.append(self.player.cutscene)

    def creditsInit(self):
        self.screen.clear()
        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))
        print("credits")

    def creditsUpdate(self):
        self.transition(self.mainMenuInit,
                        self.mainMenuUpdate)

    def gameInit(self):
        self.screen.clear()
        self.screen.append(
            Sprite(0, 0, image=BS, width=SCREEN_WIDTH, height=SCREEN_HEIGHT))
        self.player.buildGame()
        self.startingGame = True

    def gameUpdate(self):
        self.player.update()

        winner = self.player.getWinner()

        if winner:
            print("winner is", winner)
            if winner == "white":
                if type(self.menu.newestPatient()) is type(self.player):
                    unlockPatient()
            self.transition(self.selectPatientInit,
                            self.selectPatientUpdate)

        if self.moved == 2:
            print("white player moved")
            self.player.move()
            self.moved = 3
        else:
            if self.moved < 2:
                self.moved += 1

        for sprite in self.screen:
            if isinstance(sprite, WhitePiece):
                if sprite.getMoved():
                    self.moved = 0

    # tools

    def update(self):
        self.state()
        self.music.update()

    def veilInit(self):
        self.veil.color[3] = 0
        self.time = time.time()
        self.screen.append(self.veil)

    def veilUpdateOne(self):
        if not self.veil.color[3] >= 1:
            self.veil.color[3] += (time.time() - self.time)/200
        else:
            self.next_init()
            self.screen.remove(self.veil)
            self.screen.append(self.veil)
            self.time = time.time()
            self.state = self.veilUpdateTwo

    def veilUpdateTwo(self):
        if not self.veil.color[3] <= 0:
            self.veil.color[3] -= (time.time() - self.time)/200
        else:
            self.screen.remove(self.veil)
            self.state = self.next_update

    def transition(self, init, update):
        self.next_init = init
        self.next_update = update

        self.veilInit()
        self.state = self.veilUpdateOne

    # end tools
