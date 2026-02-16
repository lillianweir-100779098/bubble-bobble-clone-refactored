from src.entities.collide_actor import CollideActor
import utilities

class Bolt(CollideActor):
    SPEED = 7

    def __init__(self, pos, dir_x):
        super().__init__(pos)

        self.direction_x = dir_x
        self.active = True

    def update(self):
        # Move horizontally and check to see if we've collided with a block
        if self.move(self.direction_x, 0, Bolt.SPEED):
            # Collided
            self.active = False
        else:
            # We didn't collide with a block - check to see if we collided with an orb or the player
            for obj in utilities.game.orbs + [utilities.game.player]:
                if obj and obj.hit_test(self):
                    self.active = False
                    break

        direction_idx = "1" if self.direction_x > 0 else "0"
        anim_frame = str((utilities.game.timer // 4) % 2)
        self.image = "bolt" + direction_idx + anim_frame