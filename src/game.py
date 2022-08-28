from random import randint
from configuration import BLOCK_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from entity import Entity, Player, Field


class GameWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_variable()
        self.all_widget()
        self.setup_window()

    def setup_window(self):
        self._move_key()
        self._keyboard = Window.request_keyboard(self._keyboard_close, self)
        self._keyboard.bind(on_key_down=self._keyboard_down_key)
        self._keyboard.bind(on_key_up=self._keyboard_up_key)

    def _keyboard_close(self):
        self._keyboard.unbind(on_key_down=self._keyboard_down_key)
        self._keyboard.unbind(on_key_up=self._keyboard_up_key)
        self._keyboard = None

    def _keyboard_down_key(self, _, key, *__):
        if key[1] == "spacebar" and self.move_jump is False and self.player.jump_cooldown <= 0:
            self.move_jump = True
        elif key[1] == "shift":
            self.move_sprint = True
        elif key[1] == "w":
            self.move_up = True
            self.move_down = False
        elif key[1] == "s":
            self.move_down = True
            self.move_up = False
        elif key[1] == "a":
            self.move_left = True
            self.move_right = False
            self.player.automatic_x = False
        elif key[1] == "d":
            self.move_right = True
            self.move_left = False
            self.player.automatic_x = False
        if key[1] in ["w", "a", "s", "d", "shift", "spacebar"] and self.start_gravity is False:
            self.start_gravity = True
            self.start_loop()
        print(key[1])

    def _keyboard_up_key(self, _, key, *__):
        if key[1] == "spacebar":
            self.move_jump = False
        elif key[1] == "shift":
            self.move_sprint = False
        elif key[1] == "w":
            self.move_up = False
        elif key[1] == "s":
            self.move_down = False
        elif key[1] == "a":
            self.move_left = False
        elif key[1] == "d":
            self.move_right = False

    def _move_key(self):
        self.move_jump = False
        self.move_sprint = False
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def move_player(self):
        adder = 2 if self.move_sprint else 1
        if self.move_right and self.move_left is False:
            self.camera_x -= adder
        elif self.move_left and self.move_right is False:
            self.camera_x += adder
        # elif self.move_up and self.move_down is False:
        #     self.camera_y -= adder
        # elif self.move_down and self.move_up is False:
        #     self.camera_y += adder

    def start_loop(self):
        self.start_clock = Clock.schedule_interval(
            self.game_loop, 1.0/60.0)

    def game_loop(self, dt):
        self.delta_time = dt
        self.move_player()
        self.player.update()
        for field in self.all_field.children:
            field.update()
        for entity in self.all_entity.children:
            entity.update()

        # Spawn Entity || Comment it if you want :)
        if randint(0, 200) == 200:
            self.add_entity()

    def all_variable(self):
        self.start_gravity = False
        self.camera_x = 0
        self.camera_y = 0

    def all_widget(self):
        self.player = Player(
            ((WINDOW_WIDTH/2)-(BLOCK_SIZE/2), 200))
        self.all_entity = Widget()
        self.all_field = Widget()
        # self.all_field.add_widget(
        #     Field((0, self.player.y-BLOCK_SIZE), (WINDOW_WIDTH, BLOCK_SIZE)))
        for i in range(10):
            self.all_field.add_widget(
                Field((0+(i*100), (self.player.y-BLOCK_SIZE)-(i*80)), (WINDOW_WIDTH, 20)))
        self.add_widget(self.all_field)
        self.add_widget(self.all_entity)
        self.add_widget(self.player)

    def add_entity(self):
        self.all_entity.add_widget(
            Entity((randint(0, self.player.x + (
                WINDOW_WIDTH-BLOCK_SIZE)), WINDOW_HEIGHT)))
