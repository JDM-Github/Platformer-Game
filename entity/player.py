from .entity import Entity


class Player(Entity):

    def update(self):
        self.check_jump_cooldown()
        self.apply_gravity()
        self.check_box_collision()

    def check_jump_cooldown(self):
        if self.velocity >= 0:
            self.jump_cooldown -= 1

    def apply_gravity(self):
        if self.parent.move_jump and self.jumped is False:
            self.entity_jump()
        self.accelaration += (self.gravity * self.parent.delta_time)
        if self.accelaration >= self.gravity_cap:
            self.accelaration = self.gravity_cap
        self.velocity += self.accelaration * \
            self.parent.delta_time
        self.parent.camera_y += (self.velocity * self.parent.delta_time)

    def check_box_collision(self):
        for box in (self.parent.all_field.children):
            distance_x = abs(box.x-self.x) - \
                (self.width if self.x < box.x else box.width)
            distance_y = abs(box.y-self.y) - \
                (self.height if self.y < box.y else box.height)
            if (distance_x < 0 and distance_y < 0):
                if (abs(distance_x) > abs(distance_y)):
                    if (abs(box.y > self.y)):
                        self.parent.camera_y += abs(distance_y)
                    else:
                        self.parent.camera_y -= abs(distance_y)
                        if self.jumped and self.jump_cooldown <= 0:
                            self.jump_cooldown = self.cooldown
                        self.jumped = False
                    self.accelaration = 0
                    self.velocity = 0
                else:
                    self.parent.camera_x += abs(distance_x) \
                        if (abs(box.x > self.x)) else -(abs(distance_x))
                return True
        return False
