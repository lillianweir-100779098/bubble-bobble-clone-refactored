def init():
    global game
    game = None

WIDTH = 800
HEIGHT = 480
TITLE = "Cavern"

NUM_ROWS = 18
NUM_COLUMNS = 28

LEVEL_X_OFFSET = 50
GRID_BLOCK_SIZE = 25

ANCHOR_CENTRE = ("center", "center")
ANCHOR_CENTRE_BOTTOM = ("center", "bottom")

LEVELS = [ ["XXXXX     XXXXXXXX     XXXXX",
            "","","","",
            "   XXXXXXX        XXXXXXX   ",
            "","","",
            "   XXXXXXXXXXXXXXXXXXXXXX   ",
            "","","",
            "XXXXXXXXX          XXXXXXXXX",
            "","",""],

           ["XXXX    XXXXXXXXXXXX    XXXX",
            "","","","",
            "    XXXXXXXXXXXXXXXXXXXX    ",
            "","","",
            "XXXXXX                XXXXXX",
            "      X              X      ",
            "       X            X       ",
            "        X          X        ",
            "         X        X         ",
            "","",""],

           ["XXXX    XXXX    XXXX    XXXX",
            "","","","",
            "  XXXXXXXX        XXXXXXXX  ",
            "","","",
            "XXXX      XXXXXXXX      XXXX",
            "","","",
            "    XXXXXX        XXXXXX    ",
            "","",""]]


# Widths of the letters A to Z in the font images
CHAR_WIDTH = [27, 26, 25, 26, 25, 25, 26, 25, 12, 26, 26, 25, 33, 25, 26,
              25, 27, 26, 26, 25, 26, 26, 38, 25, 25, 25]

def char_width(char):
    # Return width of given character. For characters other than the letters A to Z (i.e. space, and the digits 0 to 9),
    # the width of the letter A is returned. ord gives the ASCII/Unicode code for the given character.
    index = max(0, ord(char) - 65)
    return CHAR_WIDTH[index]

IMAGE_WIDTH = {"life":44, "plus":40, "health":40}

def sign(x):
    # Returns -1 or 1 depending on whether number is positive or negative
    return -1 if x < 0 else 1