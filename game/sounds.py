import pygame,os

class SoundHandler():
    def play(self, sound):
        pygame.mixer.Sound.play(sound)

class Sound(pygame.mixer.Sound):
    def __init__(self, name, volume):
        super().__init__(os.path.join('assets', 'sounds', f'{name}.wav'))
        self.set_volume(volume)