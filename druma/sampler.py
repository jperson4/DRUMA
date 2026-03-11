import numpy as np

class Sampler:
    def __init__(self):
        self.instruments = {} # nombre, (wavfile, volumen, pitch)
        self.instruments_ord = [] # para mantener el orden de los instrumentos
        self.currently_playing = []

    def get_instrument_name(self, index):
        if index < len(self.instruments_ord):
            return self.instruments_ord[index]
        return None

    def add_instrument(self, name, wavfile, volume=1.0, pitch=1.0):
        self.instruments[name] = (wavfile, volume, pitch)
        self.instruments_ord.append(name)

    def add_to_play(self, instrument):
        if instrument in self.instruments:
            self.currently_playing.append(self.instruments[instrument])
            
    def play(self):
        ''' Devuelve un np.array con la mezcla de los sonidos que se deben reproducir en el siguiente tick del reloj'''
        ret = np.empty(0)
        for wavfile, volume, pitch in self.currently_playing:
            sound = self._process_sound(wavfile, volume, pitch)
            if ret.size < sound.size:
                ret = np.pad(ret, (0, sound.size - ret.size))
            elif sound.size < ret.size:
                sound = np.pad(sound, (0, ret.size - sound.size))
            ret = np.add(ret, sound)
        self.currently_playing = []
        return ret

    
    def _process_sound(self, wavfile, volume, pitch):
        ''' Devuelve un np.array con el sonido procesado con el volumen y el pitch'''
        # Aquí se debería cargar el wavfile, aplicar el volumen y el pitch, y devolver el resultado como un np.array
        pass


    def set_volume(self, volume, instrument):
        if instrument in self.instruments:
            wavfile, _, pitch = self.instruments[instrument]
            self.instruments[instrument] = (wavfile, volume, pitch)

    def set_pitch(self, pitch, instrument):
        if instrument in self.instruments:
            wavfile, volume, _ = self.instruments[instrument]
            self.instruments[instrument] = (wavfile, volume, pitch)