from ex12.game import Game
from ex12.graphics import FourInaRow


def graphics(game=None):
    """
    func to run the entire game through graphics
    :return: whether the user wants to continue playing
    """
    game = FourInaRow(game=game)
    game.mainloop()
    return game.ret


# test function for ai approaching the end of the game
# def tie_board():
#     game = Game()
#     for i in range(Game.get_rows()):
#         game.make_move(0)
#
#     for i in range(Game.get_rows()):
#         game.make_move(1)
#
#     game.make_move(4)
#
#     for i in range(Game.get_rows()):
#         game.make_move(2)
#
#     for i in range(Game.get_rows()):
#         game.make_move(3)
#
#     for i in range(Game.get_rows() - 1):
#         game.make_move(4)
#
#     for i in range(Game.get_rows()):
#         game.make_move(5)
#
#     for i in range(Game.get_rows() - 4):
#         game.make_move(6)
#
#     return game


if __name__ == "__main__":
    run = True
    while run:
        run = graphics()
