from enum import Enum

class MessageType(Enum):
    STARTSTOP = 0
    START = 1
    STOP = 2
    STEP = 3
    INSTRUMENT = 4
    VOLUME = 5
    VOLUME_INCREMENT = 6
    PITCH = 7
    PITCH_INCREMENT = 8
    MUTE = 9

class Message:
    def __init__(self, type):
        self.type = type

class MsgStartStop(Message):
    def __init__(self):
        super().__init__(MessageType.STARTSTOP)

class MsgStart(Message):
    def __init__(self):
        super().__init__(MessageType.START)

class MsgStop(Message):
    def __init__(self):
        super().__init__(MessageType.STOP)

class MsgStep(Message):
    def __init__(self, step):
        super().__init__(MessageType.STEP)
        self.step = step

class MsgInstrument(Message):
    def __init__(self, instrument):
        super().__init__(MessageType.INSTRUMENT)
        self.instrument = instrument

class MsgVolume(Message):
    def __init__(self, volume):
        ''' El volumen es un valor entre 0 y 1 que indica el volumen absoluto'''
        super().__init__(MessageType.VOLUME, volume)
        self.volume = volume

class MsgVolume_Increment(Message):
    def __init__(self, volume):
        ''' El volumen es un valor entre 0 y 1 que indica el incremento o decremento del volumen actual'''
        super().__init__(MessageType.VOLUME_INCREMENT, volume)
        self.volume = volume

class MsgPitch(Message):
    def __init__(self, pitch):
        ''' El pitch es un valor que indica la altura del sonido'''
        super().__init__(MessageType.PITCH, pitch)
        self.pitch = pitch

class MsgPitch_Increment(Message):
    def __init__(self, pitch):
        ''' El pitch es un valor que indica el incremento o decremento del pitch actual'''
        super().__init__(MessageType.PITCH_INCREMENT, pitch)
        self.pitch = pitch

class MsgMute(Message):
    def __init__(self):
        super().__init__(MessageType.MUTE)