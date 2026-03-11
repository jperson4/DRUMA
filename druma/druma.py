import asyncio
from clock import Clock
from sequencer import Sequencer
from sampler import Sampler
from player import Player

class Druma:
    ''' Gestiona los componentes y conecta todo'''

    def __init__(self, bpm=120, steps=16):
        self.CV = asyncio.Event()
        self.clock = Clock(CV=self.CV, bpm=bpm, steps=steps)
        self.sampler = Sampler()
        self.sequencer = Sequencer(self.sampler, steps=steps)
        self.player = Player()
        self.playing = False

        self.selected_instrument = 0

    async def start(self):
        clock_task = asyncio.create_task(self.clock.start())
        while self.playing:
            await self.CV.wait()
            self.CV.clear()
            self.sequencer.next_step(self.clock.current_step)
            sound = self.sampler.play()
            self.player.play(sound)
        await clock_task

    def stop(self):
        self.playing = False
        self.clock.stop()

    def set_instrument(self, instrument):
        self.selected_instrument = instrument

    def set_beat(self, step, instrument=None):
        _ins = instrument or self.selected_instrument
        ins_name = self.sampler.get_instrument_name(_ins)
        if ins_name is not None:
            self.sequencer.set_beat(step, ins_name)

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
