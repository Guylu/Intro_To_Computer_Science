import random
import time
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from .ai import AI
from .game import Game


def forget_wrapper(func):
    """
        when moving between windows we forget the current window in order to hide it
        :param func: func that is used to move to another window
        :return:pointer to the function that will pack forget and change window
        """

    def forget(self, *args, **kwargs):
        self.pack_forget(*args, **kwargs)
        return func(self)

    return forget


class BaseGraphics(tk.Canvas):
    """
    basic window functionality and data
    """
    BUTTON_SIZE = 10
    BUTTON_MARGIN = 50
    WINDOW_WIDTH = 642
    WINDOW_HEIGHT = 442
    PLAYER = "player"
    AI = "ai"
    NEXT_ELEMENT = "run_next"
    FONT = "helvetica 12"
    PLAYER1 = 1
    PLAYER2 = 2
    COLORS = {
        PLAYER1: "blue",
        PLAYER2: "red"
    }

    def __init__(self, parent, controller, **kwargs):
        """
        basic graphic initializer
        :param parent: a root canvas that contains everyone else
        :param controller: the tk root in which the window resides
        :param kwargs:
        """
        super().__init__(parent)
        self.controller = controller
        self.configure(width=self.WINDOW_WIDTH,
                       height=self.WINDOW_HEIGHT, bg="white")

        self.__board_i = tk.PhotoImage(file="ex12/field.png")
        self.create_image(1, 1, image=self.__board_i, anchor=tk.NW)

    def get_button_padding(self, size, elements):
        """
        used to calculate the space between buttons in different windows
        :param size: the size in which the buttons should spread
        :param elements: the number of elements to divide the size between
        :return: the size given for each element to inhibit
        """
        return max(size / (elements + 1), self.BUTTON_MARGIN)

    @forget_wrapper
    def exit(self):
        """
        exists the game
        :return:
        """
        self.destroy()
        self.controller.destroy()


class MainMenu(BaseGraphics):
    """
    main menu functionality and data
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = [
            tk.Button(self, text="Play", command=self.__play,
                      anchor=tk.CENTER, width=self.BUTTON_SIZE),
            tk.Button(self, text="Exit", command=self.exit,
                      anchor=tk.CENTER, width=self.BUTTON_SIZE),
        ]

        self.__title_i = tk.PhotoImage(file="ex12/title.png")
        self.create_image(self.WINDOW_WIDTH / 2, self.BUTTON_MARGIN / 1.5,
                          image=self.__title_i, anchor=tk.N)
        self.__top_margin = + self.__title_i.height()

        margin = self.get_button_padding(
            self.WINDOW_HEIGHT - self.__top_margin, len(self.buttons))

        for i, button in enumerate(self.buttons):
            self.create_window((self.WINDOW_WIDTH - self.BUTTON_SIZE) / 2,
                               self.__top_margin + margin + (i * margin),
                               window=button)

    @forget_wrapper
    def __play(self):
        """
        move to the following window, pre play, which is one step before the actual game
        :return:
        """
        return self.controller.show_window(PrePlay)


class PrePlay(BaseGraphics):
    """
    game settings before actually starting
    """

    class PlayerType:
        """
        holds the data of a single player identity human/ai
        including the buttons and labels required to display and change this data
        """
        HUMAN = "Player"
        AI = "Machine"

        def __init__(self, controller, player_name, initial_margin, color):
            self.controller = controller
            self.initial_margin = initial_margin
            self.padding = 25
            self.color = color

            self.label = "{} {}".format(self.HUMAN, player_name)

            self.choice = tk.StringVar()
            self.choice.set(PrePlay.PLAYER)

            self.player_choice = tk.Radiobutton(
                self.controller, text=self.HUMAN,
                variable=self.choice, value=PrePlay.PLAYER)
            self.machine_choice = tk.Radiobutton(
                self.controller, text=self.AI,
                variable=self.choice, value=PrePlay.AI)

        def show(self):
            """
            func to display the gui required to control the players identity
            :return:
            """
            self.controller.create_text(
                (PrePlay.WINDOW_WIDTH - len(self.label)) / 2,
                self.initial_margin, fill=self.color,
                text=self.label, font=self.controller.FONT)

            self.controller.create_window(
                (PrePlay.WINDOW_WIDTH - PrePlay.BUTTON_SIZE) / 2,
                self.initial_margin + self.padding,
                window=self.player_choice)

            self.controller.create_window(
                (PrePlay.WINDOW_WIDTH - PrePlay.BUTTON_SIZE) / 2,
                self.initial_margin + (2 * self.padding),
                window=self.machine_choice)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player1 = self.PLAYER
        self.player2 = self.PLAYER

        margin = self.get_button_padding(self.WINDOW_HEIGHT, 3)

        self.player1 = self.PlayerType(self, "One", margin, self.COLORS[1])
        self.player1.show()

        self.player2 = self.PlayerType(self, "Two", 2 * margin, self.COLORS[2])
        self.player2.show()

        self.__play_b = tk.Button(self, text="Go! ", command=self.__play,
                                  anchor=tk.CENTER, width=self.BUTTON_SIZE)

        self.create_window(
            (self.WINDOW_WIDTH - self.BUTTON_SIZE) / 2,
            self.WINDOW_HEIGHT - margin,
            window=self.__play_b)

    @forget_wrapper
    def __play(self):
        """
        set the players as determined in this window and move to the game window
        :return:
        """
        self.controller.windows[GameLoop].set_player(
            self.PLAYER1, self.player1.choice.get())
        self.controller.windows[GameLoop].set_player(
            self.PLAYER2, self.player2.choice.get())
        return self.controller.show_window(GameLoop)


class GameLoop(BaseGraphics):
    """
    data and functionality of a single game
    """
    __SIDE_PANE = 96
    __TOP_PANE = 96
    __GRID_WIDTH = BaseGraphics.WINDOW_WIDTH - (2 * __SIDE_PANE)
    __GRID_LINE = 7
    __BOTTOM_FILL = 5
    __BOARD_WIDTH = __GRID_WIDTH - __GRID_LINE
    __BOARD_HEIGHT = BaseGraphics.WINDOW_HEIGHT - (__TOP_PANE + __BOTTOM_FILL)
    __PEG_X = __BOARD_WIDTH / Game.get_cols()
    __PEG_Y = __BOARD_HEIGHT / Game.get_rows()
    __X_PADDING = 3
    __Y_PADDING = 2
    __AI_DELAY = 1000
    __ANIMATION_DELAY = 0.3
    __ANIMATE_ITERATIONS = 2
    __PLAYER_FLAG = 20
    __WARNINGS = [
        "What are you doing?!",
        "Be careful!",
        "Try again",
        "Not today!",
    ]

    def __init__(self, game=None, **kwargs):
        super().__init__(**kwargs)
        self.__backend = Game() if game is None else game
        self.__pegs = {}
        self.__scheduled = None
        self.players = {
            self.PLAYER1: self.PLAYER,
            self.PLAYER2: self.PLAYER
        }
        self.ais = []
        self.turn_label = None

        self.__load_graphics()

        self.bind("<Button-1>", self.__click_move)

        self.__scheduled = self.controller.after(self.__AI_DELAY, self.__ai_scheduler)

        self.__show_turn()

    def __load_graphics(self):
        """
        all graphics initialization is done here so the init will be neat
        :return:
        """
        self.__board_img = tk.PhotoImage(file="ex12/grid.png")
        self.create_image(self.__SIDE_PANE, self.__TOP_PANE, image=self.__board_img, anchor=tk.NW)

        self.player1_i = tk.PhotoImage(file="ex12/player1.png")
        self.create_image((self.__SIDE_PANE - self.player1_i.width()) / 2,
                          self.__TOP_PANE - self.__PLAYER_FLAG, image=self.player1_i, anchor=tk.NW)

        self.player2_i = tk.PhotoImage(file="ex12/player2.png")
        self.create_image(self.WINDOW_WIDTH - self.__SIDE_PANE + (self.player2_i.width() / 3),
                          self.__TOP_PANE - self.__PLAYER_FLAG, image=self.player2_i, anchor=tk.NW)

        self.__pegs_i = {
            self.PLAYER1: tk.PhotoImage(file="ex12/peg1.png"),
            self.PLAYER2: tk.PhotoImage(file="ex12/peg2.png")
        }

        self.__flames = {
            self.PLAYER1: [],
            self.PLAYER2: []
        }

        for file_name in ["small", "mid", "large"]:
            self.__flames[self.PLAYER1].append(
                tk.PhotoImage(file="ex12/blue_{}.png".format(file_name)))
            self.__flames[self.PLAYER2].append(
                tk.PhotoImage(file="ex12/red_{}.png".format(file_name)))

        self.__lightning_i = Image.open("ex12/lightning.png")
        self.__animation_id = None

    def exit(self):
        """
        set ret to True so a new graphic instance will be initialized
        (we do this cause resetting graphics sucks XD)
        :return:
        """
        self.controller.ret = True

        super().exit()

    def set_player(self, player, player_type):
        """
        enable the pre play window to initialize ai players if required
        :param player: the number of player 1/2
        :param player_type: human/ai
        :return:
        """
        self.players[player] = player_type
        if player_type == self.AI:
            self.ais.append(AI(self.__backend, player))

    def __ai_scheduler(self):
        """
        run ai moves ina scheduled matter
        :return:
        """
        for ai in self.ais:
            try:
                ai.find_legal_move()
                self.__make_move(ai.get_last_found_move(), ai.get_player())
            except (ValueError, KeyError):
                continue
            break

        if self.__scheduled is not None:
            self.__scheduled = self.controller.after(
                self.__AI_DELAY, self.__ai_scheduler)

    def __show_turn(self):
        """
        display the current players turn on screen
        :return:
        """
        player = self.__backend.get_current_player()
        label = "Player {} turn".format(player)

        if self.turn_label is not None:
            self.itemconfigure(self.turn_label, text=label,
                               fill=self.COLORS[player])
        else:
            self.turn_label = self.create_text(
                (self.WINDOW_WIDTH - len(label)) / 2,
                self.__TOP_PANE / 3, text=label, font=self.FONT,
                fill=self.COLORS[player])

    def __get_location(self, row, col):
        """
        calculate an elements location in the canvas based on it's board coordinate
        :param row: row in board
        :param col: col in board
        :return:
        """
        return (
            self.__GRID_LINE + self.__SIDE_PANE + (col * self.__PEG_X),
            self.__TOP_PANE + (row * self.__PEG_Y),
        )

    def __generate_lightning(self, row, col):
        """
        calculate the size and location of lightning image
        and create a generator that will return the relevant function for the animation to appear
        :param row:
        :param col:
        :return:
        """
        # calculate and resize
        x, y = self.__get_location(row, col)
        image = ImageTk.PhotoImage(self.__lightning_i.resize(
            (int(self.__lightning_i.width),
             int(self.__lightning_i.height + self.__PEG_Y - (self.WINDOW_HEIGHT - y))),
            Image.ANTIALIAS))

        for i in range(self.__ANIMATE_ITERATIONS):
            if i % 2 == 0:
                yield self.create_image, \
                      (x + self.__X_PADDING - (self.__lightning_i.width / 3), 0), \
                      {"image": image, "anchor": tk.NW}, (i + 1) % 2
            else:
                yield self.delete, (self.__animation_id,), {}, (i + 1) % 2

    def __summon_peg(self, animator, row, col, player):
        """
        add a lightning animation before drawing the relevant peg
        this function also takes care of disabling player movements during animation time
        """
        sched_ai = False

        if self.players[player] == self.PLAYER and self.__scheduled is not None:
            self.controller.after_cancel(self.__scheduled)
            self.__scheduled = None
            sched_ai = True

        self.bind("<Button-1>", lambda event: event)

        for animate, args, kwargs, delay_factor in animator:
            self.__animation_id = animate(*args, **kwargs)
            self.controller.update()
            time.sleep(self.__ANIMATION_DELAY * delay_factor)

        self.__draw_peg(row, col, player)

        self.bind("<Button-1>", self.__click_move)

        if sched_ai:
            self.__scheduled = self.controller.after(
                self.__AI_DELAY, self.__ai_scheduler)

    def __draw_peg(self, row, col, player):
        """
        draw a peg based on the player and given location in board
        :param row:
        :param col:
        :param player:
        :return:
        """
        x, y = self.__get_location(row, col)

        peg = self.create_image(
            self.__X_PADDING + x, self.__Y_PADDING + y,
            image=self.__pegs_i[player], anchor=tk.NW)
        self.__pegs[(row, col)] = peg

    def __show_end(self, player):
        """
        display an ending message when the game is finished
        :param player: the winning player if exits, 0 represents a tie
        :return:
        """
        message = "It's a tie!" if player == 0 \
            else "Winner is player {}!".format(player)

        messagebox.showinfo("Game Over", message)
        self.exit()

    def __draw_flames(self, pegs, image, player):
        """
        a scheduled task that draws flames over the winning sequence creating an
        animation affect of summoned flames
        :param pegs: winning sequence coordinates
        :param image: current flames to display
        :param player: winning player, determines flames colors
        :return:
        """
        if len(pegs) == 0 or image >= len(self.__flames[player]):
            self.__show_end(player)
            return

        for peg in pegs:
            x, y = self.__get_location(*peg)
            self.create_image(
                x, y + self.__PEG_Y,
                image=self.__flames[player][image], anchor=tk.SW)

        self.controller.update()
        time.sleep(self.__ANIMATION_DELAY)
        self.__draw_flames(pegs, image + 1, player)

    def __check_winner(self, row, col):
        """
        after making a move check if the game is over and we have a winner/tie
        :param row: last move row
        :param col: last move col
        :return:
        """
        winning_player = self.__backend.get_winner()

        if winning_player is None:
            return False

        if self.__scheduled is not None:
            self.controller.after_cancel(self.__scheduled)
            self.__scheduled = None

        win_seq = list()
        for seq in self.__backend.created_sequences(row, col, winning_player):
            if len(seq) >= self.__backend.SEQ_LENGTH:
                win_seq.extend(seq)

        self.__draw_flames(win_seq, 0, winning_player)

        return True

    def __make_move(self, col, player):
        """
        try to make a required move on the backend that holds game functionality
        if the move is made successfully update the gui as well
        in the end check if the game is over
        :param col:
        :param player:
        :return:
        """
        row = self.__backend.make_move(col)

        try:
            self.__summon_peg(self.__generate_lightning(row, col), row, col, player)
        except tk.TclError:
            # catch error's that are thrown when window is closed while animation is running
            return

        if not self.__check_winner(row, col):
            self.__show_turn()

    def __click_move(self, event):
        """
        a bind function for user input to enable a human player to make moves
        :param event:
        :return:
        """
        if event.x <= self.__SIDE_PANE or event.x >= self.WINDOW_WIDTH - self.__SIDE_PANE:
            return

        player = self.__backend.get_current_player()

        if self.players[player] == self.AI:
            return

        col = int((event.x - self.__SIDE_PANE) / self.__PEG_X)
        try:
            self.__make_move(col, player)
        except KeyError as e:
            tk.messagebox.showwarning(
                title=str(e).strip("'"),
                message="{:21s}".format(random.choice(self.__WARNINGS)))


class FourInaRow(tk.Tk):
    """
    a tk root class that holds the loaded windows
    """

    def __init__(self, game=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ret = False
        self.title("Heroes of Pegs and Magic")
        container = tk.Canvas(self)

        container.pack()

        self.windows = {}
        for window in [MainMenu, PrePlay, GameLoop]:
            if window == GameLoop and game is not None:
                canvas = window(parent=container, controller=self, game=game)
            else:
                canvas = window(parent=container, controller=self)
            self.windows[window] = canvas

        self.resizable(0, 0)

        self.show_window(MainMenu)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def show_window(self, window):
        """
        display the given window
        :param window: a window to display to the user
        :return:
        """
        canvas = self.windows[window]
        canvas.pack()
        self.lift(canvas)
