from kivy.uix.image import Image
from configuration import BLOCK_SIZE


class Entity(Image):

    def __init__(self, pos=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.size = BLOCK_SIZE, BLOCK_SIZE
        self.pos = pos
        self.old_x = pos[0]
        self.old_y = pos[1]
        self.grab_x = None
        self.grab_y = None
        self.gravity_variable()

    def gravity_variable(self):
        self.negate_gravity = False
        self.cooldown = 5
        self.jump_cooldown = 0
        self.jumped = False
        self.gravity = 1000
        self.gravity_cap = 800
        self.accelaration = 0.0
        self.velocity = 0.0

    def update(self):
        self.apply_gravity()
        self.update_position()
        self.check_box_collision()

    def update_position(self):
        self.x = self.old_x + self.parent.parent.camera_x
        self.y = self.old_y + self.parent.parent.camera_y

    def apply_gravity(self):
        if self.negate_gravity is False:
            self.accelaration += (self.gravity * self.parent.parent.delta_time)
            if self.accelaration >= self.gravity_cap:
                self.accelaration = self.gravity_cap
            self.velocity += self.accelaration * \
                self.parent.parent.delta_time
            self.old_y -= (self.velocity * self.parent.parent.delta_time)

    def check_box_collision(self):
        for box in (self.parent.parent.all_field.children):
            distance_x = abs(box.x-self.x) - \
                (self.width if self.x < box.x else box.width)
            distance_y = abs(box.y-self.y) - \
                (self.height if self.y < box.y else box.height)
            if (distance_x < 0 and distance_y < 0):
                if (abs(distance_x) > abs(distance_y)):
                    self.old_y -= abs(distance_y) \
                        if (abs(box.y > self.y)) else -abs(distance_y)
                else:
                    self.old_x -= abs(distance_x) \
                        if (abs(box.x > self.x)) else -abs(distance_x)
                self.velocity = 0
                self.update_position()
                return True
        return False

    def entity_jump(self):
        self.jumped = True
        self.accelaration = 0
        self.velocity = -(self.gravity / 4)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.grab_x = touch.x - self.old_x
            self.grab_y = touch.y - self.old_y
            touch.grab(self)
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.negate_gravity = True
            self.old_x = touch.x - self.grab_x
            self.old_y = touch.y - self.grab_y
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.negate_gravity = False
            touch.ungrab(self)
        return super().on_touch_up(touch)
