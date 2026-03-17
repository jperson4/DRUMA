import asyncio
from druma.druma import Druma
from druma.sampler import Sampler
from view.terminal.main import mainview
from control.keyboardcontrol import keyboardControl

async def main():

    sampler = Sampler({
        # name, (path, volume, pitch)
        'kick': ('samples/909_simple/Kick.wav', 1, 1),
        'hh_open': ('samples/909_simple/HHOpen.wav', 1, 1),
        'hh_closed': ('samples/909_simple/HHClosed.wav', 1, 1),
        'snare': ('samples/909_simple/Snare.wav', 1, 1),
        'clap': ('samples/909_simple/Clap.wav', 1, 1),
    })

    druma = Druma(
        bpm=140,
        sampler=sampler
    )
    
    controller = keyboardControl(druma)

    # crear tareas concurrentes
    druma_task = asyncio.create_task(druma.start())
    view_task = asyncio.create_task(mainview(druma))
    controller_task = asyncio.create_task(controller.start())

    # esperar a que ambas terminen
    await asyncio.gather(druma_task, view_task, controller_task)

if __name__ == "__main__":
    asyncio.run(main())