from src.game import Game
from src.entities.player import Player
import utilities

class MenuScreen():
    def __init__(self, app):
        self.app = app
        utilities.game = Game()

    def update(self, input_state):
        if input_state.fire_pressed:
            from src.screens.play import PlayScreen
            play_screen = PlayScreen(self.app)
            self.app.change_screen(play_screen)
            utilities.game = Game(Player())
        else:
            utilities.game.update(input_state)

    def draw(self, screen):
        utilities.game.draw(screen)
        screen.blit("title", (0, 0))
        anim_frame = min(((utilities.game.timer + 40) % 160) // 4, 9)
        screen.blit("space" + str(anim_frame), (130, 280))