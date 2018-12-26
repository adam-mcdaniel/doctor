from kivy.config import Config
Config.set('graphics', 'resizable', False)

__all__ = ["camera", "setup", "sprite", "sound"]
from . import *