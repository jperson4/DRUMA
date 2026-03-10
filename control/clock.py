import asyncio

class Clock:
    def __init__(self, bpm=120, steps=16):
        self.bpm = bpm
        self.steps = steps
        self.signature = 4  # 4/4 time
        self.current_step = 0
        self.running = False
        
    def tick(self):
        self.current_step = (self.current_step + 1) % self.steps
        
    def set_bpm(self, bpm):
        self.bpm = bpm
        
    async def start(self):
        self.running = True
        while self.running:
            self.tick()
            await asyncio.sleep(60 / self.bpm / self.signature)
            
    def stop(self):
        self.running = False