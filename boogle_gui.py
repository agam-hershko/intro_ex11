# Imports
import tkinter as tk
from boggle_board_randomizer import randomize_board, LETTERS

# Constants
BOARD_ROWS = 4
BOARD_COLS = 4
BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = 'slateblue'
BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": REGULAR_COLOR}


class BoogleGUI:
    """Class that implements gui of boogle game and has attributes of objects
    on the screen"""
    __buttons = [[None] * BOARD_COLS for row in range(BOARD_ROWS)]

    def __init__(self):
        root = tk.Tk()
        self.__window = root
        root.title("Boogle")

        # Creating outer frame which contains all objects
        self.__outer_frame = tk.Frame(root, bg=REGULAR_COLOR,
                                      highlightbackground=REGULAR_COLOR,
                                      highlightthickness=5)
        self.__outer_frame.place(relheight=0.98, relwidth=0.98, relx=0.01,
                                 rely=0.01)

        # Creating frame which contains the board
        self.__board = tk.Frame(self.__outer_frame)
        self.__board.place(relheight=0.6, relwidth=0.6, relx=0.2, rely=0.2)

        self.__create_buttons_in_board()

    def __create_button(self, row: int, col: int, content: str) -> None:
        """The function gets location of button in board and its content and
        creates button and appends it to GUI board (grid) and buttons matrix"""
        button = tk.Button(self.__board, text=content, **BUTTON_STYLE)
        # Create grid: sticky "news" means locate in center (all direction)
        button.grid(row=row, column=col, sticky="news")
        self.__buttons[row][col] = button

    def __create_buttons_in_board(self) -> None:
        """The function create buttons and appends them to GUI"""
        # Creating 2D list of random words (using randomizer file)
        board = randomize_board(LETTERS)

        # Configuring board frame (buttons)
        for row in range(BOARD_ROWS):
            self.__board.rowconfigure(row, weight=1)
        for col in range(BOARD_ROWS):
            self.__board.columnconfigure(col, weight=1)

        # Creating buttons
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__create_button(row, col, board[row][col])

    def run(self):
        """The function runs the game"""
        self.__window.mainloop()


if __name__ == '__main__':
    gui = BoogleGUI()
    gui.run()
