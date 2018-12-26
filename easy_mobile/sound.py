from kivy.core.audio import SoundLoader


def Sound(path):
    return SoundLoader.load(path)
    