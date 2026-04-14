from engine.core.game import Game
from game.scenes.menu_scene import MenuScene

game = Game()
game.current_scene = MenuScene(game)
game.run()