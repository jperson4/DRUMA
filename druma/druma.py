import asyncio
from clock import Clock
from sequencer import Sequencer
from sampler import Sampler

class Druma:
    def __init__(self, bpm=120, steps=16):
        self.CV = asyncio.Event()
        self.clock = Clock(CV=self.CV, bpm=bpm, steps=steps)
        self.sampler = Sampler()
        self.sequencer = Sequencer(self.sampler, steps=steps)
        self.player = None # TODO reproductor 
        self.playing = False

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