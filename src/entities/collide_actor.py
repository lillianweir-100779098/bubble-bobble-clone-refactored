from pgzero.builtins import Actor
from utilities import ANCHOR_CENTRE, GRID_BLOCK_SIZE, LEVEL_X_OFFSET, NUM_COLUMNS, NUM_ROWS
import utilities

class CollideActor(Actor):
    def __init__(self, pos, anchor=ANCHOR_CENTRE):
        super().__init__("blank", pos, anchor)

    def move(self, dx, dy, speed):
        new_x, new_y = int(self.x), int(self.y)

        # Movement is done 1 pixel at a time, which ensures we don't get embedded into a wall we're moving towards
        for i in range(speed):
            new_x, new_y = new_x + dx, new_y + dy

            if new_x < 70 or new_x > 730:
                # Collided with edge of level
                return True

            # Normally you don't need brackets surrounding the condition for an if statement (unlike many other
            # languages), but in the case where the condition is split into multiple lines, using brackets removes
            # the need to use the \ symbol at the end of each line.
            # The code below checks to see if we're position we're trying to move into overlaps with a block. We only
            # need to check the direction we're actually moving in. So first, we check to see if we're moving down
            # (dy > 0). If that's the case, we then check to see if the proposed new y coordinate is a multiple of
            # GRID_BLOCK_SIZE. If it is, that means we're directly on top of a place where a block might be. If that's
            # also true, we then check to see if there is actually a block at the given position. If there's a block
            # there, we return True and don't update the object to the new position.
            # For movement to the right, it's the same except we check to ensure that the new x coordinate is a multiple
            # of GRID_BLOCK_SIZE. For moving left, we check to see if the new x coordinate is the last (right-most)
            # pixel of a grid block.
            # Note that we don't check for collisions when the player is moving up.
            if ((dy > 0 and new_y % GRID_BLOCK_SIZE == 0 or
                 dx > 0 and new_x % GRID_BLOCK_SIZE == 0 or
                 dx < 0 and new_x % GRID_BLOCK_SIZE == GRID_BLOCK_SIZE-1)
                and block(new_x, new_y)):
                    return True

            # We only update the object's position if there wasn't a block there.
            self.pos = new_x, new_y

        # Didn't collide with block or edge of level
        return False
    
def block(x,y):
    # Is there a level grid block at these coordinates?
    grid_x = (x - LEVEL_X_OFFSET) // GRID_BLOCK_SIZE
    grid_y = y // GRID_BLOCK_SIZE
    if grid_y > 0 and grid_y < NUM_ROWS:
        row = utilities.game.grid[grid_y]
        return grid_x >= 0 and grid_x < NUM_COLUMNS and len(row) > 0 and row[grid_x] != " "
    else:
        return False