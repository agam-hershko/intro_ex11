#################################################################
# FILE : boggle.py
# WRITERS : 1) Agam Hershko Dekel, id_214193831 , 214193831
#           2) Itzhak Fagebaume, itzhakfage, 666225701
# EXERCISE : intro2cs2 ex11 2023
# DESCRIPTION: A program that implements GUI of Boogle game
# STUDENTS I DISCUSSED THE EXERCISE WITH: -
# NOTES: -
#################################################################

# Imports
import tkinter as tk
import tkinter.messagebox
from boggle_board_randomizer import randomize_board, LETTERS
from file_handler import create_words_set
import time
from ex11_utils import *
from typing import Optional

# Constants
BOARD_ROWS = 4
BOARD_COLS = 4
TIME_IN_SECS = 180
# Design Constants
BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = 'gray25'
BUTTON_STYLE = {"borderwidth": 1,
                "relief": tk.RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}
LABEL_STYLE = {"bg": REGULAR_COLOR}
# Constant for window configuring
LETTERS_DIVISOR = 25
LABELS_DIVISOR = 60
BUTTONS_DIVISOR = 40


class BoogleGUI:
    """ Class that implements gui of boogle game and has attributes of objects
    on the screen """

    def __init__(self):
        self.__window = tk.Tk()  # Create window from tk
        # While press window's close button, activate closing protocol
        self.__window.protocol("WM_DELETE_WINDOW", self.__close_window)
        self.__window.title("Boogle")  # Title the window`

        # Creating frames
        self.__create_outer_frame()
        self.__create_board_frame()

        # Creating 2D list: board of letters buttons: initialize with None
        self.__letters_in_board = [[None] * BOARD_COLS for _ in
                                   range(BOARD_ROWS)]
        self.__letters_in_word = []

        # Create game objects
        self.__create_empty_letters_buttons()
        self.__create_timer()
        self.__create_word_display()
        self.__create_found_words()
        self.__create_scores()
        self.__create_game_buttons()
        self.__create_longest_word()

        # Create set of all valid words and current random board (from files)
        self.__all_words = create_words_set("boggle_dict.txt")
        self.__current_board = randomize_board(LETTERS)

        # Configure the window
        self.__window.bind("<Configure>", self.__configure_window)

    def __configure_window(self, _) -> None:
        """
        The function configures the window size and adjust button font size
        accordingly
        """
        window_width = self.__window.winfo_width()
        window_height = self.__window.winfo_height()
        font_size = min(window_width, window_height)

        # Update font size for letter buttons
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                button = self.__letters_in_board[row][col]
                button.config(font=("Courier", font_size // LETTERS_DIVISOR))

        # Update font size for other buttons
        for widget in [self.__start_button, self.__submit_button,
                       self.__clear_button, self.__close_button]:
            widget.config(font=("Courier", font_size // BUTTONS_DIVISOR))

        # Update font size for other labels
        for widget in [self.__word_display, self.__timer, self.__score,
                       self.__total_score, self.__words_list,
                       self.__best_score, self.__longest_word]:
            widget.config(font=("Courier", font_size // LABELS_DIVISOR))

    def __configure_finished_game_window(self, event) -> None:
        """
        The function configures the window size and adjust button font size
        accordingly
        """
        window_width = self.__window.winfo_width()
        window_height = self.__window.winfo_height()
        font_size = min(window_width, window_height)

        # Update font size for buttons
        for widget in [self.__no_button, self.__yes_button]:
            widget.config(font=("Courier", font_size // BUTTONS_DIVISOR))

        # Update font size for other labels
        for widget in [self.__game_message, self.__last_score,
                       self.__new_game]:
            widget.config(font=("Courier", font_size // LABELS_DIVISOR))

        self.__configure_window(event)

    def __create_outer_frame(self) -> None:
        """ Creating outer frame which contains all objects """
        self.__outer_frame = tk.Frame(self.__window, bg=REGULAR_COLOR,
                                      highlightbackground=REGULAR_COLOR,
                                      highlightthickness=5)
        self.__outer_frame.place(relheight=0.98, relwidth=0.98, relx=0.01,
                                 rely=0.01)

    def __create_board_frame(self) -> None:
        """ Creating board frame which contains buttons """
        self.__board_frame = tk.Frame(self.__outer_frame)
        self.__board_frame.place(relheight=0.6, relwidth=0.6, relx=0.1,
                                 rely=0.3)

        self.__configure_board()

    def __create_game_buttons(self) -> None:
        """ Creating button for game: start(reset), submit, clear and close """
        self.__create_start_button()
        self.__create_submit_button()
        self.__create_clear_button()
        self.__create_close_button()

    def __create_word_display(self) -> None:
        """ Creating display label of  the current word """
        self.__word_display = tk.Label(self.__outer_frame, **BUTTON_STYLE)
        self.__word_display.place(relheight=0.05, relwidth=0.2, relx=0.3,
                                  rely=0.1)

    def __create_timer(self) -> None:
        """The function creates timer label in gui (later will be activated)"""
        self.__timer = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__present_time(TIME_IN_SECS // 60, TIME_IN_SECS % 60)
        self.__timer.place(relheight=0.05, relwidth=0.2, relx=0.05, rely=0.1)

        self.__is_timer_active = True  # Setting the timer state as active

    def __configure_board(self):
        """ The function Configures board frame (for letters buttons) """
        for row in range(BOARD_ROWS):
            self.__board_frame.rowconfigure(row, weight=1)

        for col in range(BOARD_ROWS):
            self.__board_frame.columnconfigure(col, weight=1)

    def __create_found_words(self):
        """ Creating list of found words and scrollbar """
        self.__words_list = tk.Listbox(self.__outer_frame, **LABEL_STYLE)
        self.__words_list.place(relheight=0.6, relwidth=0.2, relx=0.75,
                                rely=0.3)
        scrollbar = tk.Scrollbar(self.__outer_frame, orient="vertical")
        scrollbar.config(command=self.__words_list.yview)
        scrollbar.place(relheight=0.6, relwidth=0.02, relx=0.95, rely=0.3)
        self.__words_list.config(yscrollcommand=scrollbar.set)

    def __create_scores(self):
        """ Creating labels of game score, total score and best score """
        self.__score = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__score.config(text="score: 0")  # Init score text
        self.__score.place(relheight=0.05, relwidth=0.2, relx=0.5, rely=0.1)

        self.__total_score = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__total_score.config(
            text="total score: 0")  # Init total score text
        self.__total_score.place(relheight=0.05, relwidth=0.2, relx=0.53,
                                 rely=0.05)

        self.__best_score = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__best_score.config(text="best score: 0")  # Init best score text
        self.__best_score.place(relheight=0.05, relwidth=0.2, relx=0.75,
                                rely=0.15)

    def __create_longest_word(self):
        """ Creating label of the longest word """
        self.__longest_word = tk.Label(self.__outer_frame, **LABEL_STYLE)
        self.__longest_word.config(text="longest word: ")  # Init word text
        self.__longest_word.place(relheight=0.05, relwidth=0.2, relx=0.75,
                                  rely=0.2)

    def __clear_word(self) -> None:
        """
        The function clears the current word: display and letters list
        and removes letters marks and activate all disabled buttons
        """
        self.__letters_in_word = []
        self.__word_display.config(text="")

        # Remove all letters marks and activate all buttons
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__letters_in_board[row][col].config(bg=REGULAR_COLOR)
                self.__letters_in_board[row][col].config(state="normal")

    def __disable_invalid_clicks(self, current_row: int,
                                 current_col: int) -> None:
        """
        The function gets location of button and disables clicking on
        invalid buttons: not close buttons or buttons which are already
        clicked
        """
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

    def __able_clicks_around(self, current_row: int, current_col: int) -> None:
        """
        The function gets location of button and ables clicking on
        buttons around: close buttons including the button itself
        """
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if ((row == current_row and col == current_col) or
                        (1 < abs(row - current_row) or
                         1 < abs(col - current_col))):
                    self.__letters_in_board[row][col].config(state='normal')

    def __get_word_from_letters(self) -> str:
        """ The function takes a list of letters buttons and returns word """
        letters = map(lambda letter: letter.cget("text"),
                      self.__letters_in_word)
        return ''.join(letters)

    def __create_empty_button(self, row: int, col: int) -> None:
        """
        The function gets location of button in board and
        creates empty button and appends it to GUI board (grid)
        and buttons matrix
        """
        button = tk.Button(self.__board_frame, **BUTTON_STYLE)
        button.config(state="disabled")
        # Grid: sticky "news" means locate in center (all direction)
        button.grid(row=row, column=col, sticky="news")
        self.__letters_in_board[row][col] = button

    def __get_last_button_coors(self) -> Optional[Tuple[int, int]]:
        """
        The function get the coordinates in board of the last button, which
        holds the last letter on word
        """
        if not self.__letters_in_word:
            return None

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.__letters_in_word[-1] \
                        == self.__letters_in_board[row][col]:
                    return row, col

    def __create_empty_letters_buttons(self) -> None:
        """
        The function create empty buttons for preview before playing
        and appends them to GUI
        """
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__create_empty_button(row, col)

    def __create_letter_button(self, row: int, col: int,
                               content: str = "") -> None:
        """
        The function gets location of button in board and its content and
        creates letter button and appends it to GUI board (grid)
        and buttons matrix
        """
        button = tk.Button(self.__board_frame, text=content, **BUTTON_STYLE)
        # Create grid: sticky "news" means locate in center (all direction)
        button.grid(row=row, column=col, sticky="news")
        self.__letters_in_board[row][col] = button

        def click_on_letter(_) -> None:
            if button['state'] == 'disabled':
                # Ignore the click event if the button is disabled when it
                #  isn't the last one to be clicked (if letters were be chosen)
                if (self.__letters_in_word
                        and button != self.__letters_in_word[-1]):
                    return None

                else:  # If click on the last clicked button, unclick it
                    button.config(bg=REGULAR_COLOR)
                    # If letters were be chosen, removing current button
                    if self.__letters_in_word:
                        self.__letters_in_word.pop()

                    # Able clicks around the current button and disable clicks
                    # around last buttons (if letters were be chosen)
                    self.__able_clicks_around(row, col)
                    if self.__get_last_button_coors():
                        last_row, last_col = self.__get_last_button_coors()
                        self.__disable_invalid_clicks(last_row, last_col)

            else:  # If button is not clicked
                button.config(bg=BUTTON_ACTIVE_COLOR)
                self.__disable_invalid_clicks(row, col)
                self.__letters_in_word.append(button)  # Appending button

            # Updating the list of word buttons and displaying it
            current_word = self.__get_word_from_letters()
            self.__word_display.config(text=current_word)

        # Handling events
        button.bind("<Button-1>", click_on_letter)  # Click on submit

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

    def __create_letters_buttons(self) -> None:
        """
        The function create letters buttons with randomized letters
        and appends them to GUI
        """
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__create_letter_button(row, col,
                                            self.__current_board[row][col])

    def __reset_words_list(self) -> None:
        """ The function resets the words list """
        self.__words_list.delete(0, tk.END)

    def __create_start_button(self) -> None:
        """ The function activates start button """
        # Creating start button
        self.__start_button = tk.Button(self.__outer_frame, text="START",
                                        **BUTTON_STYLE)
        self.__start_button.place(relheight=0.05, relwidth=0.1, relx=0.1,
                                  rely=0.2)

        def click_on_start(_) -> None:
            # Ignore the click event if the button is disabled when it
            if self.__start_button.cget("state") == 'disabled':
                return None

            # If the game is played, change label from start to reset
            if self.__start_button.cget("text") == "START":
                self.__start_button.config(text="RESET")

            self.__update_best_score()
            self.__clear_word()
            self.__reset_words_list()
            self.__activate__timer()
            self.__current_board = randomize_board(LETTERS)  # Reset board
            self.__create_letters_buttons()
            self.__score.config(text="score: 0")  # Init the score

        # Handling events
        self.__start_button.bind("<Button-1>", click_on_start)  # Click start
        self.__start_button.bind("<Enter>",  # Get over button
                                 lambda event: self.__start_button.config(
                                     bg=BUTTON_HOVER_COLOR))
        self.__start_button.bind("<Leave>",  # Leave widget area
                                 lambda event: self.__start_button.config(
                                     bg=REGULAR_COLOR))

    def __update_scores(self, current_word: str) -> None:
        """ The function gets current word and updates scores: game score and
        total score """
        current_score = len(current_word) ** 2
        score = int(self.__score.cget("text").split(":")[1])
        self.__score.config(
            text="score: " + str(current_score + score))

        total_score = int(
            self.__total_score.cget("text").split(":")[1])
        self.__total_score.config(
            text="total score: " + str(current_score + total_score))

    def __update_longest_word(self, current_word: str) -> None:
        """ The function gets the current word and updates the longest word
         (first in this length) """
        longest_word = self.__longest_word.cget("text").split(": ")[1]

        if len(current_word) > len(longest_word):
            self.__longest_word.config(
                text="longest word: " + current_word)

    def __were_all_words_found(self) -> bool:
        """ The function gets if all words were found"""
        return int(self.__score.cget("text").split(":")[
                       1].strip()) == get_max_score(self.__current_board,
                                                    self.__all_words)

    def __create_submit_button(self) -> None:
        """ The function creates submit button """
        self.__submit_button = tk.Button(self.__outer_frame, text="SUBMIT",
                                         **BUTTON_STYLE)
        self.__submit_button.place(relheight=0.05, relwidth=0.1, relx=0.35,
                                   rely=0.2)

        def click_on_submit(_) -> None:
            current_word = self.__get_word_from_letters()

            if current_word in self.__all_words \
                    and current_word not in \
                    self.__words_list.get(0, "end"):  # If word wasn't found
                # Insert score to words list
                self.__words_list.insert(0, current_word)
                # Update score and longest word with current word
                self.__update_scores(current_word)
                self.__update_longest_word(current_word)

                # If we find all words, finish the game and stop timer
                if self.__were_all_words_found():
                    self.__is_timer_active = False
                    self.__finish_the_game()

            self.__clear_word()

        # Handling events
        self.__submit_button.bind("<Button-1>",
                                  click_on_submit)  # Click on submit
        self.__submit_button.bind("<Enter>",  # Get over button
                                  lambda event: self.__submit_button.config(
                                      bg=BUTTON_HOVER_COLOR))
        self.__submit_button.bind("<Leave>",  # Leave widget area
                                  lambda event: self.__submit_button.config(
                                      bg=REGULAR_COLOR))

    def __create_clear_button(self) -> None:
        """ The function creates clear button """
        self.__clear_button = tk.Button(self.__outer_frame, text="CLEAR",
                                        **BUTTON_STYLE)
        self.__clear_button.place(relheight=0.05, relwidth=0.1, relx=0.6,
                                  rely=0.2)

        # Handling events
        self.__clear_button.bind("<Button-1>",  # Click on clear button
                                 lambda event: self.__clear_word())
        self.__clear_button.bind("<Enter>",  # Get over button
                                 lambda event: self.__clear_button.config(
                                     bg=BUTTON_HOVER_COLOR))
        self.__clear_button.bind("<Leave>",  # Leave widget area
                                 lambda event: self.__clear_button.config(
                                     bg=REGULAR_COLOR))

    def __create_close_button(self) -> None:
        """ The function creates close button which is close the window """
        self.__close_button = tk.Button(self.__outer_frame, text="CLOSE",
                                        **BUTTON_STYLE)
        self.__close_button.place(relheight=0.05, relwidth=0.1, relx=0.9,
                                  rely=0.0)

        # Handling events
        self.__close_button.bind("<Button-1>",  # Click on close button
                                 lambda event: self.__close_window())
        self.__close_button.bind("<Enter>",  # Get over button
                                 lambda event: self.__close_button.config(
                                     bg=BUTTON_HOVER_COLOR))
        self.__close_button.bind("<Leave>",  # Leave widget area
                                 lambda event: self.__close_button.config(
                                     bg=REGULAR_COLOR))

    def __present_time(self, minutes: int, seconds: int) -> None:
        """
        The function gets minutes and seconds and display on window as
        a regular timer
        """
        # If the number of minutes left is whole
        if seconds == 0:
            seconds = "00"
        else:
            # If the number of seconds (without minutes) is positive
            # and has one digit
            if seconds < 10:
                seconds = "0" + str(seconds)

        if minutes == 0 and int(seconds) <= 10:
            self.__timer.config(text=f"Timer: {minutes}:{seconds}", fg="red")
        else:
            self.__timer.config(text=f"Timer: {minutes}:{seconds}", fg="black")

    def __activate__timer(self) -> None:
        """ Update the timer to present time and to stop after 3 minutes """

        def update_timer() -> None:
            # Calculating clapsed time
            elapsed_time = int(time.time() - self.__start_time)

            # Calculating minutes and seconds for timer
            minutes_left = (TIME_IN_SECS - elapsed_time) // 60
            secs_left = (TIME_IN_SECS - elapsed_time) % 60
            secs_left = 0 if secs_left == 60 else secs_left

            self.__present_time(minutes_left, secs_left)

            if elapsed_time < TIME_IN_SECS:  # Stop the timer after 3 minutes
                if self.__is_timer_active:
                    self.__timer.after(1000, update_timer)
            else:
                self.__finish_the_game()

        self.__start_time = time.time()
        update_timer()

    def __create_yes_button(self) -> None:
        self.__yes_button = tk.Button(self.__board_frame, text="YES",
                                      **BUTTON_STYLE)
        self.__yes_button.place(relheight=0.15, relwidth=0.1, relx=0.65,
                                rely=0.7)

        def click_on_yes(_) -> None:
            # Recreate board
            self.__configure_board()
            self.__current_board = randomize_board(LETTERS)  # Reset board
            self.__create_letters_buttons()

            # Reactivate buttons
            self.__start_button.config(state="normal")
            self.__submit_button.config(state="normal")
            self.__clear_button.config(state="normal")

            # Reset game objects
            self.__score.config(text="score: 0")
            self.__reset_words_list()
            # Reactivate timer
            self.__is_timer_active = True
            self.__activate__timer()

        # Handling events
        self.__yes_button.bind("<Button-1>", click_on_yes)  # Click on yes
        self.__yes_button.bind("<Enter>",  # Get over button
                               lambda event: self.__yes_button.config(
                                   bg=BUTTON_HOVER_COLOR))
        self.__yes_button.bind("<Leave>",  # Leave widget area
                               lambda event: self.__yes_button.config(
                                   bg=REGULAR_COLOR))

    def __create_no_button(self) -> None:
        self.__no_button = tk.Button(self.__board_frame, text="NO",
                                     **BUTTON_STYLE)
        self.__no_button.place(relheight=0.15, relwidth=0.1, relx=0.8,
                               rely=0.7)

        # Handling events
        self.__no_button.bind("<Button-1>",  # Click on no button
                              lambda event: self.__close_window())
        self.__no_button.bind("<Enter>",  # Get over button
                              lambda event: self.__no_button.config(
                                  bg=BUTTON_HOVER_COLOR))
        self.__no_button.bind("<Leave>",  # Leave widget area
                              lambda event: self.__no_button.config(
                                  bg=REGULAR_COLOR))

    def __update_best_score(self) -> None:
        """ The function updates the best score """
        current_score = int(self.__score.cget("text").split(":")[1])

        # Checking if the current score is higher than the best
        if current_score > int(self.__best_score.cget("text").split(":")[1]):
            self.__best_score.config(
                text="best score: " + str(current_score))

    def __create_game_message(self) -> None:
        """ Creating label with information of ending game """
        self.__game_message = tk.Label(self.__board_frame, **LABEL_STYLE)
        self.__game_message.place(relheight=0.15, relwidth=0.4, relx=0.3,
                                  rely=0.1)

        if self.__were_all_words_found():
            self.__game_message.config(text="All words were found!")
        else:  # The only other option for game finishing is if time's up
            self.__game_message.config(text="Time is up!")

    def __create_last_score(self) -> None:
        """ Creating label with information of score in last game """
        self.__last_score = tk.Label(self.__board_frame, **LABEL_STYLE)
        self.__last_score.config(text=self.__score.cget("text"))
        self.__last_score.place(relheight=0.15, relwidth=0.2, relx=0.4,
                                rely=0.4)

    def __create_new_game_label(self) -> None:
        """ Creating label with question about new game """
        self.__new_game = tk.Label(self.__board_frame, **LABEL_STYLE)
        self.__new_game.place(relheight=0.15, relwidth=0.5, relx=0.1,
                              rely=0.7)
        self.__new_game.config(text="Do you want to play again?")

    def __finish_the_game(self) -> None:
        # Reinitialize board frame
        self.__board_frame = tk.Frame(self.__outer_frame)
        self.__board_frame.place(relheight=0.6, relwidth=0.6, relx=0.1,
                                 rely=0.3)

        # Disable buttons and clear word on display
        self.__start_button.config(state="disabled")
        self.__submit_button.config(state="disabled")
        self.__clear_button.config(state="disabled")

        # Clear word on display and update best score
        self.__clear_word()
        self.__update_best_score()

        # Create board objects
        self.__create_game_message()
        self.__create_last_score()
        self.__create_new_game_label()
        # Create buttons to answer the question (about new game)
        self.__create_yes_button()
        self.__create_no_button()

        # Configure the window
        self.__window.bind("<Configure>",
                           self.__configure_finished_game_window)

    def __goodbye_window(self) -> None:
        """
        The function activates messagebox with goodbye greeting and total score
        """
        message = "Thanks for playing!\n" + self.__total_score.cget("text")
        tk.messagebox.showinfo("Goodbye", message)

    def __close_window(self) -> None:
        """ The function show messagebox and closes the window """
        self.__is_timer_active = False  # Stop the timer
        self.__goodbye_window()
        self.__window.destroy()

    def run(self) -> None:
        """ The function runs the game """
        self.__window.mainloop()


if __name__ == '__main__':
    gui = BoogleGUI()
    gui.run()
