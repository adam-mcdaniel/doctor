# set screen dimensions on Desktop
from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '1000')

# make screen instance
from easy_mobile.setup import *
screen = setup(title='doctor')


# import game object
from games.doctor import Doctor
d = Doctor(screen)


# give the screen instance the event loop and run it
screen.run(d.update)
