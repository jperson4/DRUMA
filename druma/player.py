import sounddevice as sd
import numpy as np

SRATE = 44100
CHUNK = 1024//2 # TODO probar distintos tamaños


class Player:
    def __init__(self):
        self.stream = sd.OutputStream(samplerate=SRATE, channels=1, blocksize=CHUNK, callback=self.callback)
        self.stream.start()
        print(sd.query_devices())
        self.buffer = np.empty(0)

    def callback(self, outdata, frames, time, status):
        # print(self.buffer)
        available = min(self.buffer.size, frames)
        if available > 0:
            outdata[:available, 0] = self.buffer[:available]
            outdata[available:] = 0
            self.buffer = self.buffer[available:]
            print(f'sonido reproducido: {outdata[:available, 0].max():.4f}')
        else:
            outdata.fill(0)
        

    def play(self, sound):
        ''' Llamamos a esta funcion al inicio de cada tick
            Lo que hay en el buffer serán las colas de sonidos antiguos
            LO que hacemos es sumar los nuevos sonidos a los antiguos
            Hay otra opción que sería borrar los antiguos sonidos y poner solo los nuevos
            TODO tengo que investigar qué es lo que hacen las cajas de ritmos, (también podría poner un bool y ya)
        '''
        # TODO ver que pasa con la sincronización y el acceso desde el callback al buffer y eso
        if sound is None or sound.size == 0:
            return  # ← no hacer nada si no hay sonido
        
        print(f'play llamado, sound.size={sound.size}, dtype={sound.dtype}, max={sound.max():.4f}')
        if self.buffer.size < sound.size:
            self.buffer = np.pad(self.buffer, (0, sound.size - self.buffer.size))
        elif sound.size < self.buffer.size:
            sound = np.pad(sound, (0, self.buffer.size - sound.size))
        
        self.buffer = np.add(self.buffer, sound)
        print(f'buffer actualizado, size={self.buffer.size}, max={self.buffer.max():.4f}')
        