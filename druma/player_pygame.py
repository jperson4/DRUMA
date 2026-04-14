import pygame

class Player:
    def __init__(self):
        pygame.mixer.init()

    def play(self, sound):
        if sound is not None and sound.size > 0:
            # Convertir el array de sonido a un objeto Sound de Pygame
            sound_data = (sound * 32767).astype('int16')  # Convertir a int16
            sound_obj = pygame.sndarray.make_sound(sound_data)
            sound_obj.play()
            
    def stop(self):
        pygame.mixer.stop()