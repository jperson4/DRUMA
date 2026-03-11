from enum import Enum

class MessageType(Enum):
    START = 1
    STOP = 2
    STEP = 3
    INSTRUMENT = 4
    VOLUME = 5
    PITCH = 6

class Message:
    def __init__(self, type):
        self.type = type

class MsgStep(Message):
    def __init__(self, step):
        super().__init__(MessageType.STEP)
        self.step = step

class MsgInstrument(Message):
    def __init__(self, instrument):
        super().__init__(MessageType.INSTRUMENT)
        self.instrument = instrument

