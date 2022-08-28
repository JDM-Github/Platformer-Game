# Kivy Main Auto Template
from configuration import WINDOW_WIDTH, WINDOW_HEIGHT
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from src import GameWidget

Config.set("graphics", "width", WINDOW_WIDTH)
Config.set("graphics", "height", WINDOW_HEIGHT)
Config.set("graphics", "resizable", False)
Config.write()


class GameApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Platform Games"

    def get_game_widget(self):
        self.game_screen = Screen()
        self.game_widget = GameWidget()
        self.game_screen.add_widget(self.game_widget)
        self.sm.add_widget(self.game_screen)

    def build(self):
        self.sm = ScreenManager()
        self.get_game_widget()
        return self.sm


if __name__ == "__main__":
    GameApp().run()
