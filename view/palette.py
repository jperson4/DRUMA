from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from textual.widget import Widget


THEME_COLORS = [
    "$primary", "$secondary", "$accent", "$background", "$surface",
    "$panel", "$boost", "$success", "$warning", "$error",
    "$primary-background", "$secondary-background", "$accent-background",
    "$success-background", "$warning-background", "$error-background",
    "$primary-muted", "$secondary-muted", "$accent-muted",
    "$success-muted", "$warning-muted", "$error-muted",
]


class ColorSwatch(Static):
    def __init__(self, color: str):
        super().__init__(color.replace("$", ""))
        self.color_var = color

    def on_mount(self):
        color = self.app.theme_variables.get(self.color_var.replace("$", ""), "#444")
        self.styles.background = color
        self.styles.width = 12
        self.styles.height = 3
        self.styles.content_align = ("center", "middle")
        self.styles.margin = (0, 0, 0, 0)


class Palette(Widget):
    def compose(self) -> ComposeResult:
        with Vertical():
            row = []
            for i, color in enumerate(THEME_COLORS):
                row.append(color)
                if len(row) == 4 or i == len(THEME_COLORS) - 1:
                    with Horizontal():
                        for c in row:
                            yield ColorSwatch(c)
                    row = []
