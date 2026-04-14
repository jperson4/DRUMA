import asyncio

class Clock:
    def __init__(self, CV:asyncio.Event, bpm=120, steps=16):
        self.bpm = bpm
        self.steps = steps
        self.signature = 4  # 4/4 time
        self.current_step = 0
        self.running = False
        self.CV = CV

    def get_current_step(self):
        return self.current_step
        
    def set_bpm(self, bpm):
        self.bpm = bpm
        
    async def start(self):
        self.running = True
        while self.running:
            self.tick() # avanza un paso de reloj y activa el CV 
            await asyncio.sleep(60 / (self.bpm * self.signature))
            
    def stop(self):
        self.running = False

    def tick(self): 
        self.CV.set()
        self.current_step = (self.current_step + 1) % self.steps

    async def wait(self):
        ''' En cuanto se activa el CV, se desbloquea esta función y se vuelve a bloquear el CV para esperar al siguiente tick del reloj'''
        await self.CV.wait()
        self.CV.clear()
