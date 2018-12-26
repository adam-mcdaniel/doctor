from .sprite import *
from .camera import *
from kivy.config import Config
from kivy.core.window import Window

SCREEN_WIDTH = int(Window.width)
SCREEN_HEIGHT = int(Window.height)

LEVEL_WIDTH, LEVEL_HEIGHT = 320, 240


def setup(**kwargs):
    global LEVEL_WIDTH, LEVEL_HEIGHT


    if "title" not in kwargs:
        title = ''
    else:
        title = kwargs["title"]


    if "level_width" not in kwargs:
        LEVEL_WIDTH = SCREEN_WIDTH
    else:
        LEVEL_WIDTH = kwargs["level_width"]

    if "level_height" not in kwargs:
        LEVEL_HEIGHT = SCREEN_HEIGHT
    else:
        LEVEL_HEIGHT = kwargs["level_height"]


    Config.set('graphics', 'fullscreen', 1)
    Config.set('kivy', 'show_fps', '1')

    Screen.setTitle(title)
    # Config.set('modules', 'monitor', '1')

    return Screen(SCREEN_WIDTH, SCREEN_HEIGHT, Camera(complex_camera, LEVEL_WIDTH, LEVEL_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

# def setup()
