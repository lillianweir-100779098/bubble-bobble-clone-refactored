# Refactored Bubble Bobble Clone Design

### Screens architecture

* Each screen is a class
* Starts by creating a MenuScreen instance
* Passes the main application App instance into MenuScreen, so that change_screens can happen during the menu screen
* Changes screen to the menu screen
* Will then rotate between MenuScreen, PlayScreen, and GameOverScreen instances, passing the main application instance between them
* MenuScreen changes screen to PlayScreen, Playscreen -> GameOverScreen, GameOverScreen -> MenuScreen
* Each Screen Class has their own update and draw functions that are called by the main application instance, default Pygame Zero "screen" variable is passed to the draw function in each screen class to enable functionality
* The previous class dictates the type of Game the next screen will be using, whether it has a Player or not
* Game type is stored in utilities.py to enable global usage

### Input Design

* All logic is handled in InputState.get_keyboard()
* Edge detection is done simply by having current and previous variables for the needed keys, checking if the key is currently being pressed now and not previously, and updates the previous variable in the same function call (will only be true for one frame)
* Edge detection is used for starting the game, firing a bubble, and pausing/unpausing
* All other keys are simple keyboard checks which are stored
* input_state is passed from main.py to the screen, and then from the screen to the game, and if there's a player, passed again from the game to the player to be consumed for character movement

### How Pause Works

* PlayScreen has functionality to check if the pause button edge detection is true
* If it is, a PauseScreen instance is created, and the screen is changed
* The game state is still drawn, but not updated (like the game over screen)
* The PauseScreen waits for the pause button edge detection to be triggered again, and then changes into a new PlayScreen with the game state unchanged