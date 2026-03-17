import asyncio
from druma.druma import Druma
from druma.sampler import Sampler
from view.terminal.main import mainview
from control.keyboardcontrol import keyboardControl

async def main():

    sampler = Sampler({
        'kick': ('path', 1, 1),
        'hihat': ('aa', 1, 1)
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