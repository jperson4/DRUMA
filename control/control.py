import mido
from message import *
# Recibe el imput del midi

class SequencerControl:
    '''TODO 
        hay muchas cosas por hacer como que hacer con los controles de pitch y de volumen
        y que hacer con lo de las octavas    
    '''
    def __init__(self, druma, midi_in):
        self.druma = druma
        self.midi_in = midi_in

        self.selected_instrument = None
        self.selected_pitch = 1.0
        self.selected_volume = 1.0 # TODO podria hacer que la velocity estuviera ligada al volumen

    def start(self):
        with mido.open_input(self.midi_in) as inport:
            for msg in inport:
                m = self.translate_msg(msg)
                if m is not None:
                    self.handle_msg(m)

    def translate_msg(self, msg):
        ''' Traduce el mensaje del midi a una acción en el secuenciador'''
        # TODO
        # ejemplo:
        if msg.type == 'note_on':
            return self.translate_note(msg.note)
        return None

    def translate_note(self, nota):
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

    def handle_msg(self, msg):
        ''' Ejecuta la acción correspondiente al mensaje traducido'''
        if msg.type == MessageType.INSTRUMENT:
            self.selected_instrument = msg.instrument
            self.druma.set_instrument(msg.instrument)
        elif msg.type == MessageType.STEP:
            self.druma.set_step(msg.step, self.selected_instrument)
        elif msg.type == MessageType.VOLUME:
            self.selected_volume = msg.volume
            self.druma.set_volume(msg.volume, self.selected_instrument)
        elif msg.type == MessageType.PITCH:
            self.selected_pitch = msg.pitch
            self.druma.set_pitch(msg.pitch, self.selected_instrument)
