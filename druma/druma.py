import asyncio
from druma.clock import Clock
from druma.sequencer import Sequencer
from druma.sampler import Sampler
# from druma.player import Player
from druma.player_mock import Player

class Druma:
    ''' Gestiona los componentes y conecta todo'''

    def __init__(self, bpm=120, steps=16, sampler=Sampler()):
        self.clock = Clock(CV=asyncio.Event(), bpm=bpm, steps=steps)
        self.sampler = sampler
        self.sequencer = Sequencer(self.sampler, steps=steps)
        self.player = Player()
        self.playing = False

        self.selected_instrument = 0

    async def start(self):
        await asyncio.create_task(self.clock.start())
        while self.playing:
            await self.clock.wait() # se desbloquea cada ciclo del reloj
            self.sequencer.next_step(self.clock.current_step)
            sound = self.sampler.play()
            self.player.play(sound)

    def stop(self):
        self.playing = False
        self.clock.stop()

    def set_instrument(self, instrument):
        self.selected_instrument = instrument

    def set_step(self, step, instrument=None):
        _ins = instrument or self.selected_instrument
        ins_name = self.sampler.get_instrument_name(_ins)
        # ins_name = instrument or self.sampler.get_instrument_name(self.selected_instrument)
        if ins_name is not None:
            self.sequencer.set_step(step, ins_name)

    def set_volume(self, volume, instrument=None):
        _ins = instrument or self.selected_instrument
        ins_name = self.sampler.get_instrument_name(_ins)
        if ins_name is not None:
            self.sampler.set_volume(volume, ins_name)

    def set_pitch(self, pitch, instrument=None):
        _ins = instrument or self.selected_instrument
        ins_name = self.sampler.get_instrument_name(_ins)
        if ins_name is not None:
            self.sampler.set_pitch(pitch, ins_name)

    def get_patterns(self):
        return self.sequencer.get_patterns()
    
    def get_instruments(self):
        return self.sampler.get_instruments()

    def get_Clock(self):
        return self.clock
    
    def get_current_step(self):
        return self.clock.get_current_step()
    
    def get_selected_instrument(self):
        return self.selected_instrument
    
    def get_steps(self):
        return self.clock.steps