import asyncio
import evdev
from evdev import ecodes
from control.message import *
from control.drumacontrol import SequencerControl

class keyboardControl:
    # TODO cada controller deberia tener un print con sus instrucciones, de forma que druma solo imprima el secuenciador
    
    def __init__(self, druma):
        self.drumaControl = SequencerControl(druma)
        self.device = self._find_keyboard()

    def _find_keyboard(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        
        # for d in devices:
            # print(f"{d.path} | {d.name} | caps: {list(d.capabilities().keys())}")
        
        # filtra por nombre (ajusta el string a tu teclado)
        keyboards = [
            d for d in devices
            if ecodes.EV_KEY in d.capabilities()
            and ecodes.EV_REL not in d.capabilities()  # excluye ratones
            and len(d.capabilities()[ecodes.EV_KEY]) > 20  # excluye botones simples
        ]
        
        if not keyboards:
            raise RuntimeError("No keyboard found")
        
        # coge el que más teclas tiene
        best = max(keyboards, key=lambda d: len(d.capabilities()[ecodes.EV_KEY]))
        # print(f"Using device: {best.name} ({best.path})")
        return best

    async def start(self):
        loop = asyncio.get_event_loop()
        async for event in self.device.async_read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = evdev.categorize(event)
                if key_event.keystate == evdev.KeyEvent.key_down:
                    # print(f"Key pressed: {key_event.keycode}")
                    m = self.translate_msg(key_event)
                    if m is not None:
                        self.drumaControl.handle_msg(m)

    KEYMAP = {
        "1": MsgStep(0),  "q": MsgStep(1),
        "2": MsgStep(2),  "w": MsgStep(3),
        "3": MsgStep(4),  "e": MsgStep(5),
        "4": MsgStep(6),  "r": MsgStep(7),
        "5": MsgStep(8),  "t": MsgStep(9),
        "6": MsgStep(10), "y": MsgStep(11),
        "7": MsgStep(12), "u": MsgStep(13),
        "8": MsgStep(14), "i": MsgStep(15),
        "a": MsgInstrument(0), "s": MsgInstrument(1),
        "d": MsgInstrument(2), "f": MsgInstrument(3),
        "g": MsgInstrument(4), "h": MsgInstrument(5),
        "j": MsgInstrument(6),
        "up":    MsgVolume_Increment(.1),
        "down":  MsgVolume_Increment(-.1),
        "left":  MsgPitch_Increment(-.1),
        "right": MsgPitch_Increment(.1),
        "space": MsgMute(),
        "shift": MsgSolo(),
    }
    
    KEYMAP_2 = {
        "1": MsgStep(0),  "q": MsgStep(8),
        "2": MsgStep(1),  "w": MsgStep(9),
        "3": MsgStep(2),  "e": MsgStep(10),
        "4": MsgStep(3),  "r": MsgStep(11),
        "5": MsgStep(4),  "t": MsgStep(12),
        "6": MsgStep(5), "y": MsgStep(13),
        "7": MsgStep(6), "u": MsgStep(14),
        "8": MsgStep(7), "i": MsgStep(15),
        "a": MsgInstrument(0), "s": MsgInstrument(1),
        "d": MsgInstrument(2), "f": MsgInstrument(3),
        "g": MsgInstrument(4), "h": MsgInstrument(5),
        "j": MsgInstrument(6),
        "up":    MsgVolume_Increment(.1),
        "down":  MsgVolume_Increment(-.1),
        "left":  MsgPitch_Increment(-.1),
        "right": MsgPitch_Increment(.1),
        "space": MsgMute(),
        "shift": MsgSolo(),
    }
    
    KEYMAP_3 = {
        "q": MsgStep(0),  "a": MsgStep(8),
        "w": MsgStep(1),  "s": MsgStep(9),
        "e": MsgStep(2),  "d": MsgStep(10),
        "r": MsgStep(3),  "f": MsgStep(11),
        "t": MsgStep(4),  "g": MsgStep(12),
        "y": MsgStep(5), "h": MsgStep(13),
        "u": MsgStep(6), "j": MsgStep(14),
        "i": MsgStep(7), "k": MsgStep(15),
        "1": MsgInstrument(0), "2": MsgInstrument(1),
        "3": MsgInstrument(2), "4": MsgInstrument(3),
        "5": MsgInstrument(4), "6": MsgInstrument(5),
        "7": MsgInstrument(6), "8": MsgInstrument(7),
        "9": MsgInstrument(8), "0": MsgInstrument(9),
        "up":    MsgVolume_Increment(.1),
        "down":  MsgVolume_Increment(-.1),
        "left":  MsgPitch_Increment(-.1),
        "right": MsgPitch_Increment(.1),
        "space": MsgMute(),
        "leftshift": MsgSolo(),
    }

    def translate_msg(self, key) -> Message:
        try:
            k = key.keycode.replace("KEY_", "").lower()
        except AttributeError:
            return None
        print(f"Key pressed: {k}")
        return self.KEYMAP_3.get(k, None)
