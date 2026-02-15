from utilities import ANCHOR_CENTRE_BOTTOM, HEIGHT, sign
from src.entities.collide_actor import CollideActor

class GravityActor(CollideActor):
    MAX_FALL_SPEED = 10

    def __init__(self, pos):
        super().__init__(pos, ANCHOR_CENTRE_BOTTOM)

        self.vel_y = 0
        self.landed = False

    def update(self, detect=True):
        # Apply gravity, without going over the maximum fall speed
        self.vel_y = min(self.vel_y + 1, GravityActor.MAX_FALL_SPEED)

        # The detect parameter indicates whether we should check for collisions with blocks as we fall. Normally we
        # want this to be the case - hence why this parameter is optional, and is True by default. If the player is
        # in the process of losing a life, however, we want them to just fall out of the level, so False is passed
        # in this case.
        if detect:
            # Move vertically in the appropriate direction, at the appropriate speed
            if self.move(0, sign(self.vel_y), abs(self.vel_y)):
                # If move returned True, we must have landed on a block.
                # Note that move doesn't apply any collision detection when the player is moving up - only down
                self.vel_y = 0
                self.landed = True

            if self.top >= HEIGHT:
                # Fallen off bottom - reappear at top
                self.y = 1
        else:
            # Collision detection disabled - just update the Y coordinate without any further checks
            self.y += self.vel_y