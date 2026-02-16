from random import choice, randint, random
from utilities import sign
from src.entities.gravity_actor import GravityActor
from src.entities.bolt import Bolt

class Robot(GravityActor):
    TYPE_NORMAL = 0
    TYPE_AGGRESSIVE = 1

    def __init__(self, pos, type, game):
        super().__init__(pos)

        self.game = game

        self.type = type

        self.speed = randint(1, 3)
        self.direction_x = 1
        self.alive = True

        self.change_dir_timer = 0
        self.fire_timer = 100

    def update(self):
        super().update()

        self.change_dir_timer -= 1
        self.fire_timer += 1

        # Move in current direction - turn around if we hit a wall
        if self.move(self.direction_x, 0, self.speed):
            self.change_dir_timer = 0

        if self.change_dir_timer <= 0:
            # Randomly choose a direction to move in
            # If there's a player, there's a two thirds chance that we'll move towards them
            directions = [-1, 1]
            if self.game.player:
                directions.append(sign(self.game.player.x - self.x))
            self.direction_x = choice(directions)
            self.change_dir_timer = randint(100, 250)

        # The more powerful type of robot can deliberately shoot at orbs - turning to face them if necessary
        if self.type == Robot.TYPE_AGGRESSIVE and self.fire_timer >= 24:
            # Go through all orbs to see if any can be shot at
            for orb in self.game.orbs:
                # The orb must be at our height, and within 200 pixels on the x axis
                if orb.y >= self.top and orb.y < self.bottom and abs(orb.x - self.x) < 200:
                    self.direction_x = sign(orb.x - self.x)
                    self.fire_timer = 0
                    break

        # Check to see if we can fire at player
        if self.fire_timer >= 12:
            # Random chance of firing each frame. Likelihood increases 10 times if player is at the same height as us
            fire_probability = self.game.fire_probability()
            if self.game.player and self.top < self.game.player.bottom and self.bottom > self.game.player.top:
                fire_probability *= 10
            if random() < fire_probability:
                self.fire_timer = 0
                self.game.play_sound("laser", 4)

        elif self.fire_timer == 8:
            #  Once the fire timer has been set to 0, it will count up - frame 8 of the animation is when the actual bolt is fired
            self.game.bolts.append(Bolt((self.x + self.direction_x * 20, self.y - 38), self.direction_x))

        # Am I colliding with an orb? If so, become trapped by it
        for orb in self.game.orbs:
            if orb.trapped_enemy_type == None and self.collidepoint(orb.center):
                self.alive = False
                orb.floating = True
                orb.trapped_enemy_type = self.type
                self.game.play_sound("trap", 4)
                break

        # Choose and set sprite image
        direction_idx = "1" if self.direction_x > 0 else "0"
        image = "robot" + str(self.type) + direction_idx
        if self.fire_timer < 12:
            image += str(5 + (self.fire_timer // 4))
        else:
            image += str(1 + ((self.game.timer // 4) % 4))
        self.image = image