from random import choice
from pgzero.builtins import Actor
from src.entities.gravity_actor import GravityActor
from src.entities.robot import Robot
import utilities

class Fruit(GravityActor):
    APPLE = 0
    RASPBERRY = 1
    LEMON = 2
    EXTRA_HEALTH = 3
    EXTRA_LIFE = 4

    def __init__(self, pos, trapped_enemy_type=0):
        super().__init__(pos)

        # Choose which type of fruit we're going to be.
        if trapped_enemy_type == Robot.TYPE_NORMAL:
            self.type = choice([Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON])
        else:
            # If trapped_enemy_type is 1, it means this fruit came from bursting an orb containing the more dangerous type
            # of enemy. In this case there is a chance of getting an extra help or extra life power up
            # We create a list containing the possible types of fruit, in proportions based on the probability we want
            # each type of fruit to be chosen
            types = 10 * [Fruit.APPLE, Fruit.RASPBERRY, Fruit.LEMON]    # Each of these appear in the list 10 times
            types += 9 * [Fruit.EXTRA_HEALTH]                           # This appears 9 times
            types += [Fruit.EXTRA_LIFE]                                 # This only appears once
            self.type = choice(types)                                   # Randomly choose one from the list

        self.time_to_live = 500 # Counts down to zero

    def update(self):
        super().update()

        # Does the player exist, and are they colliding with us?
        if utilities.game.player and utilities.game.player.collidepoint(self.center):
            if self.type == Fruit.EXTRA_HEALTH:
                utilities.game.player.health = min(3, utilities.game.player.health + 1)
                utilities.game.play_sound("bonus")
            elif self.type == Fruit.EXTRA_LIFE:
                utilities.game.player.lives += 1
                utilities.game.play_sound("bonus")
            else:
                utilities.game.player.score += (self.type + 1) * 100
                utilities.game.play_sound("score")

            self.time_to_live = 0   # Disappear
        else:
            self.time_to_live -= 1

        if self.time_to_live <= 0:
            # Create 'pop' animation
            utilities.game.pops.append(Pop((self.x, self.y - 27), 0))

        anim_frame = str([0, 1, 2, 1][(utilities.game.timer // 6) % 4])
        self.image = "fruit" + str(self.type) + anim_frame

class Pop(Actor):
    def __init__(self, pos, type):
        super().__init__("blank", pos)

        self.type = type
        self.timer = -1

    def update(self):
        self.timer += 1
        self.image = "pop" + str(self.type) + str(self.timer // 2)