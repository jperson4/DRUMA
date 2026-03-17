from control.message import *
# Recibe el imput del midi

class SequencerControl:
    '''TODO 
        hay muchas cosas por hacer como que hacer con los controles de pitch y de volumen
        y que hacer con lo de las octavas    
    '''
    def __init__(self, druma):
        self.druma = druma

        self.selected_instrument = None
        self.selected_pitch = 1.0
        self.selected_volume = 1.0 # TODO podria hacer que la velocity estuviera ligada al volumen

    def handle_msg(self, msg):
        ''' Ejecuta la acción correspondiente al mensaje traducido'''
        if msg.type == MessageType.INSTRUMENT:
            self.selected_instrument = msg.instrument
            self.druma.set_instrument(msg.instrument)
        elif msg.type == MessageType.STEP:
            self.druma.set_step(msg.step, self.selected_instrument) # TODO ver si hay que pasarle el instrumento o no
        elif msg.type == MessageType.VOLUME:
            self.selected_volume = msg.volume
            self.druma.set_volume(msg.volume, self.selected_instrument)
        elif msg.type == MessageType.PITCH:
            self.selected_pitch = msg.pitch
            self.druma.set_pitch(msg.pitch, self.selected_instrument)
