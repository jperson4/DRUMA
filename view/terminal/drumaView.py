from druma.druma import Druma
from view.terminal.utils import color

# INSTRUMENT_KEYS = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k']

class DrumaView:
    def __init__(self, druma: Druma):
        self.druma = druma

    def display(self):
        patterns = self.druma.get_patterns()
        instruments = self.druma.get_instruments()
        curr_step = self.druma.get_current_step()
        ret = "Druma view\n"
        ret += "Instruments:\n"
        for i, (name, volume, pitch) in enumerate(instruments):
            # inst = f"{i}{INSTRUMENT_KEYS[i%len(INSTRUMENT_KEYS)]}: {name} (vol: {volume}, pitch: {pitch})\n"
            inst = f"{i+1}: {name} (vol: {volume}, pitch: {pitch})\n"
            if i == self.druma.get_selected_instrument():
                inst = color(inst, 'bright_yellow')
            ret += inst
            
        ret += "\nPatterns:\n"
        ret += self.display_controls(curr_step) + " : Current step\n"
        for name, _, _ in instruments:
            ret += f"{self.display_pattern(patterns[name], curr_step)} : {name}\n"
        return ret
    
    def display_controls(self, curr_step):
        
        c = 'qwertyuiasdfghjk'
        ret = ''
        for step, value in enumerate(c):
            if step % 4 == 0:
                ret += ' '
            if step == curr_step:
                ret += color(value, 'yellow')
            else:
                ret += value
        return ret
            

    def display_pattern(self, pattern, curr_step):
        ret = ""
        for step, value in enumerate(pattern):
            if step % 4 == 0:
                ret += " "
            if step == curr_step:
                if value == 2:
                    ret += color('▮', 'yellow')
                elif value == 1:
                    ret += color('▮', 'bright_yellow')
                elif value > 0:
                    ret += color('▮', 'bright_yellow')
                else:
                    ret += color('▯', 'bright_yellow')
            else:
                if value == 2:
                    ret += "▮"
                elif value == 1:
                    ret += "▮"
                elif value > 0:
                    ret += "▮"
                else:
                    ret += "▯"
        return ret
