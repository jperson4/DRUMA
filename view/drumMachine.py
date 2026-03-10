from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Horizontal, HorizontalScroll, Vertical, VerticalScroll
from textual.events import Click
from textual.message import Message


class Step(Static):    
    
    COLORS = {
        'off': "$surface",
        'on': "$primary",
        'muted': "$primary-muted",
        'playing': "$accent"
    }
    
    def __init__(self, number: int, state: str = "", playing: bool = False, **kwargs):
        super().__init__(str(number), **kwargs)
        self.number = number
        self.state = state
        self.playing = playing
        self._update_style()
        
    def on_mount(self):
        self._update_style()
            
    def on_click(self, event: Click) -> None:
        self.post_message(DrumMachineWidget.StepClicked(self.number))
        
    def set_state(self, state: str):
        self.state = state
        self._update_style()
        self.refresh()
        
    def _get_color(self, color: str):
        return self.app.theme_variables.get(color.replace("$", ""), "#444")
        
    def _update_style(self):
        color = self._get_color(self.COLORS.get(self.state, self.COLORS['off']))
        self.styles.background = color
        if self.playing:
            self.styles.border = ("heavy", self._get_color(self.COLORS['playing']))
        else:
            self.styles.border = ("heavy", color)


class DrumMachineWidget(Widget):

    class StepClicked(Message):
        def __init__(self, step: int):
            super().__init__()
            self.step = step

    DEFAULT_CSS = """
        DrumMachineWidget {
            height: auto;
            background: $panel;
        }
        DrumMachineWidget HorizontalScroll {
            height: auto;
            width: auto;
        }
        
        DrumMachineWidget Vertical {
            height: auto;
        }
        DrumMachineWidget Horizontal {
            height: auto;
        }
        
        DrumMachineWidget Step {
            margin: 0 1 1 0;
            width: 6;
            height: 3;
            min-height: 3;
            min-width: 6;
            content-align: center middle;
        }

        .separator {
            width: 1;
            min-width: 1;
        }
    """

    def __init__(self, vertical: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.vertical = vertical
        self.steps = 16
        self.steps_state = ["off"] * self.steps
        self.step_playing = 0
        # DEBUG
        # self.step_playing = 1
        # self.steps_state[6] = "on"
        # self.steps_state[10] = "on"

    def compose(self) -> ComposeResult:
        if self.vertical:
            yield from self._compose_vertical()
        else:
            yield from self._compose_horizontal()

    def _compose_vertical(self) -> ComposeResult:
        with Vertical():
            for row in range(4):
                with Horizontal():
                    for col in range(1, 5):
                        i = row * 4 + col
                        yield Step(i, id=f"step_{i}", state=self.steps_state[i - 1], playing=(i == self.step_playing))

    def _compose_horizontal(self) -> ComposeResult:
        with HorizontalScroll():
            for i in range(1, 17):
                yield Step(i, id=f"step_{i}", state=self.steps_state[i - 1], playing=(i == self.step_playing))
                if i % 4 == 0 and i != 16:
                    yield Static("", classes="separator")
                    
    def set_playing_step(self, step: int):
        self.step_playing = step
        self.refresh()

    def set_step_state(self, step: int, state: str):
        self.steps_state[step - 1] = state
        self.refresh()