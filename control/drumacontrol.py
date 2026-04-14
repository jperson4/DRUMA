from control.message import *
# Recibe el imput del midi

class SequencerControl:
    '''
        Actua de traductor entre los mensajes del midi o del teclado y las acciones del secuenciador
    
    
        TODO 
        hay muchas cosas por hacer como que hacer con los controles de pitch y de volumen
        y que hacer con lo de las octavas    
    '''
    def __init__(self, druma):
        self.druma = druma
        self.selected_instrument = None
        # self.selected_pitch = 1.0
        # self.selected_volume = 1.0 # TODO podria hacer que la velocity estuviera ligada al volumen

    def handle_msg(self, msg):
        ''' Ejecuta la acción correspondiente al mensaje traducido
        
            Tipos de mensajes:
            - Seleccionar instrumento
            - Activar/desactivar paso del secuenciador
            - Incrementar/decrementar volumen del instrumento seleccionado
            - Incrementar/decrementar pitch del instrumento seleccionado
            - Mutear/desmutear instrumento seleccionado
            - Solo/unsolo instrumento seleccionado
            - Activar/desactivar efectos
        
        '''
        if msg.type == MessageType.INSTRUMENT:
            self.selected_instrument = msg.instrument
            self.druma.set_instrument(msg.instrument)
            
        elif msg.type == MessageType.STEP:
            self.druma.set_step(msg.step, self.selected_instrument) # TODO ver si hay que pasarle el instrumento o no
            
        elif msg.type == MessageType.VOLUME_INCREMENT:
            new_volume = msg.volume + self.druma.get_instrument_volume(self.selected_instrument)
            new_volume = max(0, new_volume) # limitar el volumen entre 0 y 1
            self.druma.set_volume(new_volume, self.selected_instrument)
            
        elif msg.type == MessageType.PITCH_INCREMENT:
            new_pitch = msg.pitch + self.druma.get_instrument_pitch(self.selected_instrument)
            self.druma.set_pitch(new_pitch, self.selected_instrument)

        elif msg.type == MessageType.MUTE:
            self.selected_instrument = msg.instrument or self.selected_instrument # el mute pueden venir o no con el instrumento
            self.druma.toggle_mute(self.selected_instrument)
            
        elif msg.type == MessageType.SOLO:
            self.selected_instrument = msg.instrument or self.selected_instrument
            self.druma.toggle_solo(self.selected_instrument)