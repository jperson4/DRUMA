import numpy as np
# from scipy.io import wavfile
import soundfile as sf
from druma.player import SRATE, CHUNK

class Sampler:
    def __init__(self, instruments={}):
        self.instruments = {}
        self.instruments_ord = []  # para mantener el orden de los instrumentos
        for name, (wavpath, volume, pitch) in instruments.items():
            self.update_instrument(name, wavpath, volume, pitch)
        # self.instruments_ord = list(self.instruments.keys())  # para mantener el orden de los instrumentos
        self.currently_playing = []
        
    def update_instrument(self, name, wavpath, volume=1.0, pitch=1.0):
        ''' Devuelve el wavfile cargado y procesado con el volumen y el pitch'''
        try:
            wav = self.process_instrument(name, wavpath, volume, pitch)
            if wav.ndim > 1:
                wav = wav.mean(axis=1)  # convertir a mono si es estéreo # TODO hacerlo stereo en el futuro
            wav = wav.astype(np.float32) / wav.max()
            print(max(wav), min(wav))

            self.instruments[name] = (wav, volume, pitch, wavpath)
            self.instruments_ord.append(name)
        except Exception as e:
            print(f"Error loading instrument {name} from {wavpath}: {e}")
        
    def process_instrument(self, name, wavpath, volume=1.0, pitch=1.0):
        ''' Carga el wavfile y lo procesa con el volumen y el pitch'''
        # TODO por ahora ignora el pitch
        data, rate = sf.read(wavpath)
        data = data * volume
        # adapar el rate a SRATE
        if rate != SRATE:
            dif = SRATE / rate
            data = np.interp(np.arange(0, len(data), dif), np.arange(0, len(data)), data)
        return data
    
    def get_instrument_name(self, index):
        if index < len(self.instruments_ord):
            return self.instruments_ord[index]
        return None
    
    def get_instrument_index(self, name):
        if name in self.instruments_ord:
            return self.instruments_ord.index(name)
        return None

    def add_to_play(self, instrument, vol=1, accent=False):
        if instrument in self.instruments:
            self.currently_playing.append((*self.instruments[instrument], vol, accent))

    def play(self):
        ''' Devuelve un np.array con la mezcla de los sonidos que se deben reproducir en el siguiente tick del reloj'''
        # TODO accent not implemented
        ret = np.empty(0)
        for wavfile, ins_vol, pitch, _, vol, accent in self.currently_playing:
            sound = self.process_sound(wavfile, ins_vol * vol, pitch)
            if ret.size < sound.size:
                ret = np.pad(ret, (0, sound.size - ret.size))
            elif sound.size < ret.size:
                sound = np.pad(sound, (0, ret.size - sound.size))
            ret = np.add(ret, sound)
        self.currently_playing = []
        if ret.size > 0:
            print(max(ret), min(ret))
        return ret

    
    def process_sound(self, wavfile, volume, pitch) -> np.array:
        ''' En este modelo de sampler, no hay que procesar el sonido a cada tick'''
        return wavfile


    def set_volume(self, volume, instrument):
        if instrument in self.instruments:
            _, _, pitch, wavpath = self.instruments[instrument]
            self.update_instrument(instrument, wavpath, volume, pitch)

    def set_pitch(self, pitch, instrument):
        if instrument in self.instruments:
            _, volume, _, wavpath = self.instruments[instrument]
            self.update_instrument(instrument, wavpath, volume, pitch)

    def get_instruments(self):
        ''' Devuelve una lista ordenada de tuplas con el nombre, el volumen y el pitch de cada instrumento'''
        ret = []
        for name in self.instruments_ord:
            wavfile, volume, pitch, wavpath = self.instruments[name]
            ret.append((name, volume, pitch))
        return ret