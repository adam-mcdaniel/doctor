from easy_mobile.setup import SCREEN_WIDTH, SCREEN_HEIGHT
from easy_mobile.sprite import Sprite

from .__init__ import *
from .tiles import *
from .pieces import *
from .player import *


class TapButton(Sprite):
    def __init__(self, x, y, image, pressed_image, width=SCREEN_WIDTH, height=HEIGHT):
        super().__init__(x, y, image=image, width=width, height=height)
        self.normal_image = image
        self.pressed_image = pressed_image
        self.pressed = False

    def Press(self):
        self.pressed = True

    def update(self, screen):
        if self.getTouchDown():
            self.Press()
            self.setImage(self.pressed_image)
        else:
            self.setImage(self.normal_image)

    def getPressed(self):
        if self.pressed:
            self.pressed = False
            return True

        return False


class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        self.credits_button = TapButton(0, START_HEIGHT, "img/credits.png", "img/credits.png",
                                        width=SCREEN_WIDTH, height=SCREEN_WIDTH/4)
        self.screen.append(self.credits_button)

        self.start_button = TapButton(0, START_HEIGHT + SCREEN_WIDTH/4, "img/start.png", "img/start.png",
                                      width=SCREEN_WIDTH, height=SCREEN_WIDTH/4)
        self.screen.append(self.start_button)

        self.start = False
        self.credits = False

    def getStart(self):
        return self.start

    def getCredits(self):
        return self.credits

    def update(self):
        if self.start_button.getPressed():
            self.start = True
        if self.credits_button.getPressed():
            self.credits = True


class PatientMenu:
    def __init__(self, screen):
        # from .__init__ import NUMBER_OF_PATIENTS_UNLOCKED
        self.screen = screen
        self.NUMBER_OF_PATIENTS_UNLOCKED = 1
        self.readPatientFromFile()

        self.screen.append(Sprite(0, (SCREEN_HEIGHT-SCREEN_WIDTH/4),
                                  image="img/choose_patient_top.png", width=SCREEN_WIDTH, height=SCREEN_WIDTH/4))

        self.ryan = TapButton(0, (SCREEN_HEIGHT-SCREEN_WIDTH/4)-SCREEN_WIDTH/3,
                              "img/ryan.png", "img/ryan.png",
                              width=SCREEN_WIDTH/3, height=SCREEN_WIDTH/3)

        self.mark = TapButton(SCREEN_WIDTH/3, (SCREEN_HEIGHT-SCREEN_WIDTH/4)-SCREEN_WIDTH/3,
                              "img/mark.png", "img/mark.png",
                              width=SCREEN_WIDTH/3, height=SCREEN_WIDTH/3)

        self.lucy = TapButton(2 * SCREEN_WIDTH/3, (SCREEN_HEIGHT-SCREEN_WIDTH/4)-SCREEN_WIDTH/3,
                              "img/lucy.png", "img/lucy.png",
                              width=SCREEN_WIDTH/3, height=SCREEN_WIDTH/3)

        self.ava = TapButton(0 * SCREEN_WIDTH/3, (SCREEN_HEIGHT-SCREEN_WIDTH/4)-2*SCREEN_WIDTH/3,
                             "img/ava.png", "img/ava.png",
                             width=SCREEN_WIDTH/3, height=SCREEN_WIDTH/3)

        # print(NUMBER_OF_PATIENTS_UNLOCKED)
        self.selected = None
        self.patients = {
            self.ryan: Ryan(self.screen),
            self.mark: Mark(self.screen),
            self.lucy: Lucy(self.screen),
            self.ava:  Ava(self.screen),
            None: None
        }
        self.list_of_patients = list(self.patients.keys())
        self.list_of_patients.remove(None)
        self.screen.add(
            self.list_of_patients[:self.NUMBER_OF_PATIENTS_UNLOCKED])

    def newestPatient(self):
        return self.patients[self.list_of_patients[min(self.NUMBER_OF_PATIENTS_UNLOCKED-1, len(self.list_of_patients)-1)]]

    def isLastPatient(self):
        return self.NUMBER_OF_PATIENTS_UNLOCKED == len(self.list_of_patients)

    def getPatient(self):
        return self.patients[self.selected]

    def update(self):
        for patient in self.list_of_patients:
            if patient.getPressed():
                self.selected = patient

    def readPatientFromFile(self):
        with open("save/number_of_patients_unlocked") as f:
            self.NUMBER_OF_PATIENTS_UNLOCKED = int(f.read().replace('\n', ''))
            f.close()
        print("Read patient: #{}".format(self.NUMBER_OF_PATIENTS_UNLOCKED))

    def unlockPatient(self):
        print("Old patient: #{}".format(self.NUMBER_OF_PATIENTS_UNLOCKED))
        self.NUMBER_OF_PATIENTS_UNLOCKED += 1
        with open("save/number_of_patients_unlocked", 'w') as f:
            f.write(str(self.NUMBER_OF_PATIENTS_UNLOCKED))
            f.close()

        self.readPatientFromFile()
        print("New patient: #{}".format(self.NUMBER_OF_PATIENTS_UNLOCKED))
