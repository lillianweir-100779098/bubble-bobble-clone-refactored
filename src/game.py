from random import randint, shuffle
from utilities import LEVELS, NUM_COLUMNS, NUM_ROWS, GRID_BLOCK_SIZE, LEVEL_X_OFFSET, WIDTH, CHAR_WIDTH, IMAGE_WIDTH, char_width
from src.entities.robot import Robot
from src.entities.fruit import Fruit
from pgzero.builtins import sounds
import utilities

class Game:
    def __init__(self, player=None):
        self.player = player
        self.level_colour = -1
        self.level = -1

        self.next_level()

    def fire_probability(self):
        # Likelihood per frame of each robot firing a bolt - they fire more often on higher levels
        return 0.001 + (0.0001 * min(100, self.level))

    def max_enemies(self):
        # Maximum number of enemies on-screen at once - increases as you progress through the levels
        return min((self.level + 6) // 2, 8)

    def next_level(self):
        self.level_colour = (self.level_colour + 1) % 4
        self.level += 1

        # Set up grid
        self.grid = LEVELS[self.level % len(LEVELS)]

        # The last row is a copy of the first row
        # Note that we don't do 'self.grid.append(self.grid[0])'. That would alter the original data in the LEVELS list
        # Instead, what this line does is create a brand new list, which is distinct from the list in LEVELS, and
        # consists of the level data plus the first row of the level. It's also interesting to note that you can't
        # do 'self.grid += [self.grid[0]]', because that's equivalent to using append.
        # As an alternative, we could have copied the list on the line below '# Set up grid', by writing
        # 'self.grid = list(LEVELS...', then used append or += on the line below.
        self.grid = self.grid + [self.grid[0]]

        self.timer = -1

        if self.player:
            self.player.reset()

        self.fruits = []
        self.bolts = []
        self.enemies = []
        self.pops = []
        self.orbs = []

        # At the start of each level we create a list of pending enemies - enemies to be created as the level plays out.
        # When this list is empty, we have no more enemies left to create, and the level will end once we have destroyed
        # all enemies currently on-screen. Each element of the list will be either 0 or 1, where 0 corresponds to
        # a standard enemy, and 1 is a more powerful enemy.
        # First we work out how many total enemies and how many of each type to create
        num_enemies = 10 + self.level
        num_strong_enemies = 1 + int(self.level / 1.5)
        num_weak_enemies = num_enemies - num_strong_enemies

        # Then we create the list of pending enemies, using Python's ability to create a list by multiplying a list
        # by a number, and by adding two lists together. The resulting list will consist of a series of copies of
        # the number 1 (the number depending on the value of num_strong_enemies), followed by a series of copies of
        # the number zero, based on num_weak_enemies.
        self.pending_enemies = num_strong_enemies * [Robot.TYPE_AGGRESSIVE] + num_weak_enemies * [Robot.TYPE_NORMAL]

        # Finally we shuffle the list so that the order is randomised (using Python's random.shuffle function)
        shuffle(self.pending_enemies)

        self.play_sound("level", 1)

    def get_robot_spawn_x(self):
        # Find a spawn location for a robot, by checking the top row of the grid for empty spots
        # Start by choosing a random grid column
        r = randint(0, NUM_COLUMNS-1)

        for i in range(NUM_COLUMNS):
            # Keep looking at successive columns (wrapping round if we go off the right-hand side) until
            # we find one where the top grid column is unoccupied
            grid_x = (r+i) % NUM_COLUMNS
            if self.grid[0][grid_x] == ' ':
                return GRID_BLOCK_SIZE * grid_x + LEVEL_X_OFFSET + 12

        # If we failed to find an opening in the top grid row (shouldn't ever happen), just spawn the enemy
        # in the centre of the screen
        return WIDTH/2

    def update(self, input_state):
        self.timer += 1

        # Update all objects
        for obj in self.fruits + self.bolts + self.enemies + self.pops + self.orbs:
            if obj:
                obj.update()

        if self.player:
            self.player.update(input_state)

        # Use list comprehensions to remove objects which are no longer wanted from the lists. For example, we recreate
        # self.fruits such that it contains all existing fruits except those whose time_to_live counter has reached zero
        self.fruits = [f for f in self.fruits if f.time_to_live > 0]
        self.bolts = [b for b in self.bolts if b.active]
        self.enemies = [e for e in self.enemies if e.alive]
        self.pops = [p for p in self.pops if p.timer < 12]
        self.orbs = [o for o in self.orbs if o.timer < 250 and o.y > -40]

        # Every 100 frames, create a random fruit (unless there are no remaining enemies on this level)
        if self.timer % 100 == 0 and len(self.pending_enemies + self.enemies) > 0:
            # Create fruit at random position
            self.fruits.append(Fruit((randint(70, 730), randint(75, 400))))

        # Every 81 frames, if there is at least 1 pending enemy, and the number of active enemies is below the current
        # level's maximum enemies, create a robot
        if self.timer % 81 == 0 and len(self.pending_enemies) > 0 and len(self.enemies) < self.max_enemies():
            # Retrieve and remove the last element from the pending enemies list
            robot_type = self.pending_enemies.pop()
            pos = (self.get_robot_spawn_x(), -30)
            self.enemies.append(Robot(pos, robot_type, self))

        # End level if there are no enemies remaining to be created, no existing enemies, no fruit, no popping orbs,
        # and no orbs containing trapped enemies. (We don't want to include orbs which don't contain trapped enemies,
        # as the level would never end if the player kept firing new orbs)
        if len(self.pending_enemies + self.fruits + self.enemies + self.pops) == 0:
            if len([orb for orb in self.orbs if orb.trapped_enemy_type != None]) == 0:
                self.next_level()

    def draw(self, screen):
        # Draw appropriate background for this level
        screen.blit("bg%d" % self.level_colour, (0, 0))

        block_sprite = "block" + str(self.level % 4)

        # Display blocks
        for row_y in range(NUM_ROWS):
            row = self.grid[row_y]
            if len(row) > 0:
                # Initial offset - large blocks at edge of level are 50 pixels wide
                x = LEVEL_X_OFFSET
                for block in row:
                    if block != ' ':
                        screen.blit(block_sprite, (x, row_y * GRID_BLOCK_SIZE))
                    x += GRID_BLOCK_SIZE

        # Draw all objects
        all_objs = self.fruits + self.bolts + self.enemies + self.pops + self.orbs
        all_objs.append(self.player)
        for obj in all_objs:
            if obj:
                obj.draw()

    def play_sound(self, name, count=1):
        # Some sounds have multiple varieties. If count > 1, we'll randomly choose one from those
        # We don't play any sounds if there is no player (e.g. if we're on the menu)
        if self.player:
            try:
                # Pygame Zero allows you to write things like 'sounds.explosion.play()'
                # This automatically loads and plays a file named 'explosion.wav' (or .ogg) from the sounds folder (if
                # such a file exists)
                # But what if you have files named 'explosion0.ogg' to 'explosion5.ogg' and want to randomly choose
                # one of them to play? You can generate a string such as 'explosion3', but to use such a string
                # to access an attribute of Pygame Zero's sounds object, we must use Python's built-in function getattr
                sound = getattr(sounds, name + str(randint(0, count - 1)))
                sound.play()
            except Exception as e:
                # If no such sound file exists, print the name
                print(e)

def draw_status(screen):
    # Display score, right-justified at edge of screen
    number_width = CHAR_WIDTH[0]
    s = str(utilities.game.player.score)
    draw_text(screen, s, 451, WIDTH - 2 - (number_width * len(s)))

    # Display level number
    draw_text(screen, "LEVEL " + str(utilities.game.level + 1), 451)

    # Display lives and health
    # We only display a maximum of two lives - if there are more than two, a plus symbol is displayed
    lives_health = ["life"] * min(2, utilities.game.player.lives)
    if utilities.game.player.lives > 2:
        lives_health.append("plus")
    if utilities.game.player.lives >= 0:
        lives_health += ["health"] * utilities.game.player.health

    x = 0
    for image in lives_health:
        screen.blit(image, (x, 450))
        x += IMAGE_WIDTH[image]

def draw_text(screen, text, y, x=None):
    if x == None:
        # If no X pos specified, draw text in centre of the screen - must first work out total width of text
        x = (WIDTH - sum([char_width(c) for c in text])) // 2

    for char in text:
        screen.blit("font0"+str(ord(char)), (x, y))
        x += char_width(char)