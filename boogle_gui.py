# Imports
import tkinter as tk
from boggle_board_randomizer import randomize_board, LETTERS
from file_handler import create_set
import time

# Constants
BOARD_ROWS = 4
BOARD_COLS = 4
TIME_IN_SECS = 180
BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = 'royal blue'
BUTTON_STYLE = {"font": ("Courier", 25),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}
LABEL_STYLE = {"font": ("Courier", 15), "bg": REGULAR_COLOR}


class BoogleGUI:
    """Class that implements gui of boogle game and has attributes of objects
    on the screen"""

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

        # Creating board frame which contains buttons
        self.__board = tk.Frame(self.__outer_frame)
        self.__board.place(relheight=0.6, relwidth=0.6, relx=0.1, rely=0.3)
        self.__configure_board()

        # Creating 2D list: board of letters buttons: initialize with None
        self.__letters_in_board = [[None] * BOARD_COLS for _ in
                                   range(BOARD_ROWS)]

        # Creating display label of word
        self.__word_display = tk.Label(self.__outer_frame, **BUTTON_STYLE)
        self.__word_display.place(relheight=0.05, relwidth=0.2, relx=0.3,
                                  rely=0.1)

        # Create timer
        self.__timer = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__present_time(TIME_IN_SECS // 60, TIME_IN_SECS % 60)
        self.__timer.place(relheight=0.05, relwidth=0.2, relx=0.05, rely=0.1)

        # Creating labels of score and total scores
        self.__score = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__score.config(text="score:0")  # Init score text
        self.__score.place(relheight=0.05, relwidth=0.2, relx=0.47, rely=0.1)
        self.__total_score = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__total_score.config(
            text="total score:0")  # Init total score text
        self.__total_score.place(relheight=0.05, relwidth=0.2, relx=0.5,
                                 rely=0.05)

        # Creating list of founded words
        self.__words_list = tk.Listbox(self.__outer_frame, **LABEL_STYLE)
        self.__words_list.place(relheight=0.6, relwidth=0.2, relx=0.75,
                                rely=0.3)

        # Creates game objects
        self.__letters_in_word = []
        self.__create_empty_letters_buttons()
        self.__create_start_button()
        self.__create_submit_button()
        self.__create_clear_button()

    def __configure_board(self):
        """The function Configures board frame (for letters buttons)"""
        for row in range(BOARD_ROWS):
            self.__board.rowconfigure(row, weight=1)

        for col in range(BOARD_ROWS):
            self.__board.columnconfigure(col, weight=1)

    def __clear_word(self) -> None:
        """The function clears the current word: display and letters list
         and removes letters marks and activate all disabled buttons"""
        self.__letters_in_word = []
        self.__word_display.config(text="")

        # Remove all letters marks and activate all buttons
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__letters_in_board[row][col].config(bg=REGULAR_COLOR)
                self.__letters_in_board[row][col].config(state="normal")

    def __disable_click_on_invalid_letters(self, current_row: int,
                                           current_col: int) -> None:
        """The function gets location of button and disables clicking on
         not close buttons"""
        # todo- document
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if ((row == current_row and col == current_col) or
                        (1 < abs(row - current_row) or
                         1 < abs(col - current_col)) or
                        self.__letters_in_board[row][
                            col] in self.__letters_in_word):
                    self.__letters_in_board[row][col].config(state='disabled')
                else:
                    self.__letters_in_board[row][col].config(
                        state='normal')

    def __get_word_from_letters(self):
        """The function takes a list of letters buttons and returns word"""
        letters = map(lambda letter: letter.cget("text"),
                      self.__letters_in_word)
        return ''.join(letters)

    def __create_letter_button(self, row: int, col: int,
                               content: str = "") -> None:
        """The function gets location of button in board and its content and
        creates letter button and appends it to GUI board (grid)
        and buttons matrix"""
        button = tk.Button(self.__board, text=content, **BUTTON_STYLE)
        # Create grid: sticky "news" means locate in center (all direction)
        button.grid(row=row, column=col, sticky="news")
        self.__letters_in_board[row][col] = button

        # Handling events
        def click_on_letter(event):
            # Ignore the click event if the button is disabled
            if button['state'] == 'disabled':
                return

            # Activate the click disabling only on board with letters
            if content:  # todo- document or change
                self.__disable_click_on_invalid_letters(row, col)
            button.config(bg=BUTTON_ACTIVE_COLOR)

            # Getting button's letter, updating the list of word buttons
            # and displaying it
            self.__letters_in_word.append(button)
            current_word = self.__get_word_from_letters()
            self.__word_display.config(text=current_word)

        button.bind("<Button-1>", click_on_letter)  # Click on letter button
        # Get over button, change background if button is not clicked
        button.bind("<Enter>",
                    lambda event: button.config(
                        bg=BUTTON_HOVER_COLOR) if button.cget(
                        "bg") != BUTTON_ACTIVE_COLOR else button.config(
                        bg=BUTTON_ACTIVE_COLOR))
        # Leave widget area,  change background if button is not clicked
        button.bind("<Leave>", lambda event: button.config(
            bg=REGULAR_COLOR) if button.cget(
            "bg") != BUTTON_ACTIVE_COLOR else button.config(
            bg=BUTTON_ACTIVE_COLOR))

    def __create_empty_letters_buttons(self) -> None:
        """The function create empty buttons for preview before playing
        and appends them to GUI"""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__create_letter_button(row, col)
                # todo- init not clicked

    def __create_letters_buttons(self) -> None:
        """The function create letters buttons with randomized letters
        and appends them to GUI"""
        # Creating 2D list of random letters (using randomizer file)
        board = randomize_board(LETTERS)

        # Creating buttons
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__create_letter_button(row, col, board[row][col])

    def __reset_words_list(self):
        """The function resets the words list"""
        self.__words_list.delete(0, tk.END)

    def __create_start_button(self):
        """The function creates start button """
        button = tk.Button(self.__outer_frame, text="START", **BUTTON_STYLE)
        button.place(relheight=0.05, relwidth=0.1, relx=0.1, rely=0.2)

        def click_on_start(event):
            # If the game is played, change label from start to reset
            if button.cget("text") == "START":
                button.config(text="RESET")

            self.__create_timer()
            self.__clear_word()
            self.__create_letters_buttons()
            self.__score.config(text="score: 0")
            self.__reset_words_list()

        # Handling events
        button.bind("<Button-1>", click_on_start)  # Click on start button
        button.bind("<Enter>",  # Get over button
                    lambda event: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>",  # Leave widget area
                    lambda event: button.config(bg=REGULAR_COLOR))

    def __create_submit_button(self):
        """The function creates submit button """
        button = tk.Button(self.__outer_frame, text="SUBMIT", **BUTTON_STYLE)
        button.place(relheight=0.05, relwidth=0.1, relx=0.35, rely=0.2)

        def click_on_submit(event):
            current_word = self.__get_word_from_letters()
            words = create_set("boggle_dict.txt")

            if current_word in words \
                    and current_word not in \
                    self.__words_list.get(0, "end"):  # If word not in list
                current_score = len(current_word) ** 2
                score = self.__score.cget("text").split(":")[1]
                self.__score.config(
                    text="score: " + str((current_score + int(score))))
                total_score = self.__total_score.cget("text").split(":")[1]
                self.__total_score.config(
                    text="total score: " + str(
                        (current_score + int(total_score))))

                self.__words_list.insert(0, current_word)

            self.__clear_word()

        # Handling events
        button.bind("<Button-1>", click_on_submit)  # Click on submit
        button.bind("<Enter>",  # Get over button
                    lambda event: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>",  # Leave widget area
                    lambda event: button.config(bg=REGULAR_COLOR))

    def __create_clear_button(self):
        """The function creates submit button """
        button = tk.Button(self.__outer_frame, text="CLEAR",
                           **BUTTON_STYLE)
        button.place(relheight=0.05, relwidth=0.1, relx=0.6, rely=0.2)

        def click_on_clear(event):
            self.__clear_word()

        # Handling events
        button.bind("<Button-1>", click_on_clear)  # Click on submit
        button.bind("<Enter>",  # Get over button
                    lambda event: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>",  # Leave widget area
                    lambda event: button.config(bg=REGULAR_COLOR))

    def __present_time(self, minutes_left, seconds_left):
        # If the number of minutes left is whole
        if seconds_left == 0:
            seconds_left = "00"
        else:
            minutes_left -= 1
            # If the number of seconds (without minutes) is positive
            # and has one digit
            if seconds_left < 10:
                seconds_left = "0" + str(seconds_left)

        self.__timer.config(
            text=f"Timer: {minutes_left}:{seconds_left}")

    def __create_timer(self):
        """ Update the timer to present time and to stop after 3 minutes """

        def update_timer():
            # Calculating c
            elapsed_time = time.time() - self.__start_time
            minutes_left = TIME_IN_SECS // 60 - int(elapsed_time) // 60
            secs_left = 60 - int(elapsed_time) % 60
            secs_left = 0 if secs_left == 60 else secs_left
            self.__present_time(minutes_left, secs_left)

            if elapsed_time < TIME_IN_SECS:  # Stop the timer after 3 minutes
                self.__timer.after(1000, update_timer)

        self.__start_time = time.time()
        update_timer()

    def run(self):
        """The function runs the game"""
        self.__window.mainloop()


if __name__ == '__main__':
    gui = BoogleGUI()
    gui.run()
