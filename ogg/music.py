from easy_mobile.sound import Sound


class MusicManager:
    def __init__(self, music):
        self.music = music
        if music:
            self.index = self.loadIndex()
            self.sound = Sound(self.music[self.index])
            self.sound.play()

    def loadIndex(self):
        with open("save/music_index") as f:
            index = int(f.read().replace('\n', ''))
            f.close()
        return index

    def saveIndex(self):
        with open("save/music_index", 'w') as f:
            f.write(str(self.index))
            f.close()

    def update(self):
        if self.music and self.sound.state != 'play':
            self.index = (self.index + 1) % (len(self.music))
            print(self.index)
            self.sound = Sound(self.music[self.index])
            self.sound.play()

            self.saveIndex()
