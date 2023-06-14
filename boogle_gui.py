# Imports
import tkinter as tk
from boggle_board_randomizer import randomize_board, LETTERS

# Constants
BOARD_ROWS = 4
BOARD_COLS = 4
BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = 'royal blue'
BUTTON_STYLE = {"font": ("Courier", 25),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}


class BoogleGUI:
    """Class that implements gui of boogle game and has attributes of objects
    on the screen"""

    def __init__(self):
        root = tk.Tk()
        self.__window = root
        root.title("Boogle")

        # Creating board which contains letters buttons: initialize with None
        self.__letters = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

        # Creating outer frame which contains all objects
        self.__outer_frame = tk.Frame(root, bg=REGULAR_COLOR,
                                      highlightbackground=REGULAR_COLOR,
                                      highlightthickness=5)
        self.__outer_frame.place(relheight=0.98, relwidth=0.98, relx=0.01,
                                 rely=0.01)

        # Creating board frame which contains buttons
        self.__board = tk.Frame(self.__outer_frame)
        self.__board.place(relheight=0.6, relwidth=0.6, relx=0.2, rely=0.2)
        self.__configure_board()

        # Creates game objects
        self.__create_empty_letters_buttons()
        self.__create_start_button()

    def __configure_board(self):
        """The function Configures board frame (for letters buttons)"""
        for row in range(BOARD_ROWS):
            self.__board.rowconfigure(row, weight=1)

        for col in range(BOARD_ROWS):
            self.__board.columnconfigure(col, weight=1)

    def __create_letter_button(self, row: int, col: int,
                               content: str = "") -> None:
        """The function gets location of button in board and its content and
        creates letter button and appends it to GUI board (grid)
        and buttons matrix"""
        button = tk.Button(self.__board, text=content, **BUTTON_STYLE)
        # Create grid: sticky "news" means locate in center (all direction)
        button.grid(row=row, column=col, sticky="news")
        self.__letters[row][col] = button

        # Handling events
        button.bind("<Enter>",
                    lambda event: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>",
                    lambda event: button.config(bg=REGULAR_COLOR))

    def __create_empty_letters_buttons(self) -> None:
        """The function create empty buttons for preview before playing
        and appends them to GUI"""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__create_letter_button(row, col)

    def __create_letters_buttons(self) -> None:
        """The function create letters buttons with randomized letters
        and appends them to GUI"""
        # Creating 2D list of random letters (using randomizer file)
        board = randomize_board(LETTERS)

        # Creating buttons
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__create_letter_button(row, col, board[row][col])

    def __create_start_button(self):
        button = tk.Button(self.__outer_frame, text="START", **BUTTON_STYLE)
        button.place(relheight=0.05, relwidth=0.1, relx=0.45, rely=0.1)

        def click_on_start(event):
            self.__create_letters_buttons()
            button.configure(text="RESET")

        # Handling events
        button.bind("<Button-1>", click_on_start)
        button.bind("<Enter>",
                    lambda event: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>",
                    lambda event: button.config(bg=REGULAR_COLOR))

    def run(self):
        """The function runs the game"""
        self.__window.mainloop()


if __name__ == '__main__':
    gui = BoogleGUI()
    gui.run()
