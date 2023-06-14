# Imports
import tkinter as tki
from boggle_board_randomizer import *

BOARD_SIZE = 4
BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = 'slateblue'

BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tki.RAISED,
                "bg": REGULAR_COLOR}


class BoogleGUI:
    __buttons = {}

    def __init__(self):
        root = tki.Tk()
        self.__main_window = root
        root.title("Boogle")

        self.__outer_frame = tki.Frame(root, bg=REGULAR_COLOR,
                                       highlightbackground=REGULAR_COLOR,
                                       highlightthickness=5)
        self.__outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self.__board = tki.Frame(self.__outer_frame)
        self.__board.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self.__create_buttons_in_board()

    def run(self):
        self.__main_window.mainloop()

    def __create_buttons_in_board(self):
        board = randomize_board(LETTERS)  # todo- generalize

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.__make_button(row, col, board[row][col])

    def __make_button(self, row: int, col: int,
                      button_char: str) -> tki.Button:
        button = tki.Button(self.__board, text=button_char, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=1, columnspan=1,
                    sticky=tki.NSEW)
        self.__buttons[button_char] = button

        return button


if __name__ == '__main__':
    gui = BoogleGUI()
    gui.run()
