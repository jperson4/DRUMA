import asyncio
import keyboard
from control.message import *
from control.drumacontrol import SequencerControl

class keyboardControl:
    def __init__(self, druma):
        self.drumaControl = SequencerControl(druma)

    async def start(self):
        
        loop = asyncio.get_event_loop()

        def on_key(event):
            if event.event_type == keyboard.KEY_DOWN:
                m = self.translate_msg(event)
                if m is not None:
                    # llama al handler de forma thread-safe
                    loop.call_soon_threadsafe(self.drumaControl.handle_msg, m)

        keyboard.hook(on_key)
        while True:
            await asyncio.sleep(1) # mantener el loop corriendo

    def translate_msg(self, event) -> Message:
        ''' Traduce el evento del teclado a una acción en el secuenciador'''
        k = event.name
        if k == '1':
            return MsgStep(0)
        elif k == 'q':
            return MsgStep(1)
        elif k == '2':
            return MsgStep(2)
        elif k == 'w':
            return MsgStep(3)
        elif k == '3':
            return MsgStep(4)
        elif k == 'e':
            return MsgStep(5)
        elif k == '4':
            return MsgStep(6)
        elif k == 'r':
            return MsgStep(7)
        elif k == '5':
            return MsgStep(8)
        elif k == 't':
            return MsgStep(9)
        elif k == '6':
            return MsgStep(10)
        elif k == 'y':
            return MsgStep(11)
        elif k == '7':
            return MsgStep(12)
        elif k == 'u':
            return MsgStep(13)
        elif k == '8':
            return MsgStep(14)
        elif k == 'i':
            return MsgStep(15)
        elif k == 'a':
            return MsgInstrument(0)
        elif k == 's':
            return MsgInstrument(1)
        elif k == 'd':
            return MsgInstrument(2)
        elif k == 'f':
            return MsgInstrument(3)
        elif k == 'g':
            return MsgInstrument(4)
        elif k == 'h':
            return MsgInstrument(5)
        elif k == 'j':
            return MsgInstrument(6)
        elif k == 'up':
            return MsgVolume_Increment(.1)
        elif k == 'down':
            return MsgVolume_Increment(-.1)
        elif k == 'left':
            return MsgPitch_Increment(-.1)
        elif k == 'right':
            return MsgPitch_Increment(.1)
        elif k == 'space':
            return MsgMute()
        else:
            return None
