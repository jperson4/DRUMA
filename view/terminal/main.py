from druma.druma import Druma
from view.terminal.drumaView import DrumaView
from view.terminal.utils import clear_terminal

async def mainview(druma: Druma):
    clock = druma.get_Clock()
    drumaview = DrumaView(druma)
    while True:
        await clock.wait()
        d = drumaview.display()
        clear_terminal()
        print(d)