import mido   
from control.message import *
 
class MidiControl:
    def __init__(self, midi_in, drumaControl):
        self.midi_in = midi_in
        self.drumaControl = drumaControl

    def start(self):
        with mido.open_input(self.midi_in) as inport:
            for msg in inport: # TODO ver como hacer cuando haya varios controllers
                m = self.drumaControl.translate_msg(msg)
                if m is not None:
                    self.drumaControl.handle_msg(m)

    def translate_msg(self, msg) -> Message:
        ''' Traduce el mensaje del midi a una acción en el secuenciador'''
        # TODO
        # ejemplo:
        if msg.type == 'note_on':
            return self.translate_note(msg.note)
        return None

    def translate_note(self, nota) -> Message:
        ''' Traduce el número de nota a un instrumento o a un paso del secuenciador'''
        # las negras corresponden con un instrumento y las blancas con un paso del secuenciador
        # (menos la ultima negra que es el ultimo paso del secuenciador)
        negras = [36, 38, 40, 41, 43, 45, 47, 48]
        if nota in negras:
            # TODO traducir nota a instrumento index
            index = nota
            return MsgInstrument(index)
        else:
            # TODO traducir nota a step
            step = nota
            return MsgStep(step)