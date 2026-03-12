import numpy as np

class Sampler:
    def __init__(self, instruments={}):
        self.instruments = instruments  # nombre, (wavfile, volumen, pitch)
        self.instruments_ord = list(instruments.keys())  # para mantener el orden de los instrumentos
        self.currently_playing = []

    def get_instrument_name(self, index):
        if index < len(self.instruments_ord):
            return self.instruments_ord[index]
        return None
    
    def get_instrument_index(self, name):
        if name in self.instruments_ord:
            return self.instruments_ord.index(name)
        return None

    def add_instrument(self, name, wavfile, volume=1.0, pitch=1.0):
        self.instruments[name] = (wavfile, volume, pitch)
        self.instruments_ord.append(name)

    def add_to_play(self, instrument, vol=1, accent=False):
        if instrument in self.instruments:
            self.currently_playing.append((*self.instruments[instrument], vol, accent))

    def play(self):
        ''' Devuelve un np.array con la mezcla de los sonidos que se deben reproducir en el siguiente tick del reloj'''
        # TODO accent not implemented
        ret = np.empty(0)
        for wavfile, ins_vol, pitch, vol, accent in self.currently_playing:
            sound = self._process_sound(wavfile, ins_vol * vol, pitch)
            if ret.size < sound.size:
                ret = np.pad(ret, (0, sound.size - ret.size))
            elif sound.size < ret.size:
                sound = np.pad(sound, (0, ret.size - sound.size))
            ret = np.add(ret, sound)
        self.currently_playing = []
        return ret

    
    def _process_sound(self, wavfile, volume, pitch) -> np.array:
        ''' Devuelve un np.array con el sonido procesado con el volumen y el pitch'''
        # TODO Aquí se debería cargar el wavfile, aplicar el volumen y el pitch, y devolver el resultado como un np.array
        return np.array([])


    def set_volume(self, volume, instrument):
        if instrument in self.instruments:
            wavfile, _, pitch = self.instruments[instrument]
            self.instruments[instrument] = (wavfile, volume, pitch)

    def set_pitch(self, pitch, instrument):
        if instrument in self.instruments:
            wavfile, volume, _ = self.instruments[instrument]
            self.instruments[instrument] = (wavfile, volume, pitch)

    def get_instruments(self):
        ''' Devuelve una lista ordenada de tuplas con el nombre, el volumen y el pitch de cada instrumento'''
        ret = []
        for name in self.instruments_ord:
            wavfile, volume, pitch = self.instruments[name]
            ret.append((name, volume, pitch))
        return ret