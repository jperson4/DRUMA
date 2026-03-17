from druma.sampler import Sampler

class Sequencer:
    def __init__(self, sampler: Sampler, steps=16):
        ''' El sampler se encarga de repoducir los sonidos y de administar que sonidos hay disponibles'''
        self.sampler = sampler
        self.steps = steps
        self.patterns = {}
        for instrument in self.sampler.instruments:
            self.patterns[instrument] = [0] * self.steps

    def set_step(self, step, instrument, vol=1):
        if instrument in self.patterns:
            self.patterns[instrument][step] = 0 if self.patterns[instrument][step] > 0 else vol

    def next_step(self, step):
        ''' Carga los sonidos de los instrumentos que deben sonar del sampler en el siguiente tick del reloj'''
        for instrument, pattern in self.patterns.items():
            
            if pattern[step] == 2:
                self.sampler.add_to_play(instrument, 1, accent=True)

            if pattern[step] <= 1 and pattern[step] > 0:
                self.sampler.add_to_play(instrument, pattern[step]) # añade el sonido del instrumento a la lista de sonidos a reproducir en el siguiente tick del reloj

    def get_patterns(self):
        return self.patterns
         