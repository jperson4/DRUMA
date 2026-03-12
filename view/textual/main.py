from textual.app import App, ComposeResult, Widget
from textual.widgets import Button, Footer, Header
from textual.containers import Grid
from drumMachine import DrumMachineWidget
from palette import Palette


class MainApp(App):
    
    def on_mount(self) -> None: 
        self.theme = "gruvbox"
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # yield Header() 
        yield DrumMachineWidget(vertical=True)
        yield Palette()
        # yield Footer()



def main():
    app = MainApp()
    app.run()
    
    
if __name__ == "__main__":
    main()