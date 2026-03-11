

class Sequencer:
    def __init__(self, sampler, steps=16):
        ''' El sampler se encarga de repoducir los sonidos y de administar que sonidos hay disponibles'''
        self.sampler = sampler
        self.steps = steps
        self.patterns = {}
        for instrument in self.sampler.instruments:
            self.patterns[instrument] = [0] * self.steps

    def set_beat(self, instrument, step):
        if instrument in self.patterns:
            self.patterns[instrument][step] = 0 if self.patterns[instrument][step] == 1 else 1

    def next_step(self, step):
        ''' Carga los sonidos de los instrumentos que deben sonar del sampler en el siguiente tick del reloj'''
        for instrument, pattern in self.patterns.items():
            if pattern[step] == 1:
                self.sampler.add_to_play(instrument) # añade el sonido del instrumento a la lista de sonidos a reproducir en el siguiente tick del reloj

         