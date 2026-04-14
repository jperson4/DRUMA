import numpy as np
# from scipy.io import wavfile
import soundfile as sf
from druma.player_sd import SRATE, CHUNK

class Sampler:
    def __init__(self, instruments={}):
        self.instruments = {}
        self.instruments_ord = []  # para mantener el orden de los instrumentos
        
        self.muted_instruments = set()
        self.solo_instruments = set()
        
        for name, (wavpath, volume, pitch) in instruments.items():
            self.update_instrument(name, wavpath, volume, pitch)
            self.instruments_ord.append(name)
        # self.instruments_ord = list(self.instruments.keys())  # para mantener el orden de los instrumentos
        self.currently_playing = []
        
    def update_instrument(self, name, wavpath, volume=1.0, pitch=1.0):
        ''' Devuelve el wavfile cargado y procesado con el volumen y el pitch'''
        try:
            wav = self.process_instrument(name, wavpath, volume, pitch)
            self.instruments[name] = (wav, volume, pitch, wavpath)
        except Exception as e:
            print(f"Error loading instrument {name} from {wavpath}: {e}")
        
    def process_instrument(self, name, wavpath, volume=1.0, pitch=1.0):
        ''' Carga el wavfile y lo procesa con el volumen y el pitch'''
        # TODO por ahora ignora el pitch
        data, rate = sf.read(wavpath)
        if data.ndim > 1:
            data = data.mean(axis=1)  # convertir a mono si es estéreo # TODO hacerlo stereo en el futuro
        data = data.astype(np.float32) / (max(abs(data)) + 1e-6)  # normalizar el wavfile
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
            if instrument in self.muted_instruments:# si esta muteado, no se reproduce
                return
            if len(self.solo_instruments) > 0:
                if instrument not in self.solo_instruments: # si hay instrumentos en solo, solo se reproducen esos
                    return
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
    
    def toggle_mute(self, instrument):
        if instrument in self.instruments:
            if instrument in self.muted_instruments:
                self.muted_instruments.remove(instrument)
            else:
                self.muted_instruments.add(instrument)
                
    def toggle_solo(self, instrument):
        if instrument in self.instruments:
            if instrument in self.muted_instruments:
                self.muted_instruments.remove(instrument)
            
            if instrument in self.solo_instruments:
                self.solo_instruments.remove(instrument)
            else:
                self.solo_instruments.add(instrument)