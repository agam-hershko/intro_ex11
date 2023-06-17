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
BUTTON_ACTIVE_COLOR = 'gray30'
BUTTON_STYLE = {"font": ("Courier", 25),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}
LABEL_STYLE = {"font": ("Courier", 15), "bg": REGULAR_COLOR}


class BoogleGUI:
    """ Class that implements gui of boogle game and has attributes of objects
    on the screen """

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
        self.__create_close_button()

    def __configure_board(self):
        """ The function Configures board frame (for letters buttons) """
        for row in range(BOARD_ROWS):
            self.__board.rowconfigure(row, weight=1)

        for col in range(BOARD_ROWS):
            self.__board.columnconfigure(col, weight=1)

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

    def __get_word_from_letters(self):
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
        button = tk.Button(self.__board, **BUTTON_STYLE)
        button.config(state="disabled")
        # Grid: sticky "news" means locate in center (all direction)
        button.grid(row=row, column=col, sticky="news")
        self.__letters_in_board[row][col] = button

    def __get_last_button_coors(self):
        """
        The function get the coordinates in board of the last button, which
        holds the last letter on word
        """
        if not self.__letters_in_word:
            return None

        last_button = self.__letters_in_word[-1]

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if last_button == self.__letters_in_board[row][col]:
                    return row, col

    def __create_letter_button(self, row: int, col: int,
                               content: str = "") -> None:
        """
        The function gets location of button in board and its content and
        creates letter button and appends it to GUI board (grid)
        and buttons matrix
        """
        button = tk.Button(self.__board, text=content, **BUTTON_STYLE)
        # Create grid: sticky "news" means locate in center (all direction)
        button.grid(row=row, column=col, sticky="news")
        self.__letters_in_board[row][col] = button

        def click_on_letter(event):
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

    def __create_empty_letters_buttons(self) -> None:
        """
        The function create empty buttons for preview before playing
        and appends them to GUI
        """
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__create_empty_button(row, col)

    def __create_letters_buttons(self) -> None:
        """
        The function create letters buttons with randomized letters
        and appends them to GUI
        """
        # Creating 2D list of random letters (using randomizer file)
        board = randomize_board(LETTERS)

        # Creating buttons
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.__create_letter_button(row, col, board[row][col])

    def __reset_words_list(self):
        """ The function resets the words list"""
        self.__words_list.delete(0, tk.END)

    def __create_start_button(self):
        """ The function activates start button """
        # Creating start button
        self.__start_button = tk.Button(self.__outer_frame, text="START",
                                        **BUTTON_STYLE)
        self.__start_button.place(relheight=0.05, relwidth=0.1, relx=0.1,
                                  rely=0.2)

        def click_on_start(event):
            # Ignore the click event if the button is disabled when it
            if self.__start_button.cget("state") == 'disabled':
                return None

            # If the game is played, change label from start to reset
            if self.__start_button.cget("text") == "START":
                self.__start_button.config(text="RESET")

            self.__create_timer()
            self.__clear_word()
            self.__create_letters_buttons()
            self.__score.config(text="score: 0")
            self.__reset_words_list()

        # Handling events
        self.__start_button.bind("<Button-1>", click_on_start)  # Click start
        self.__start_button.bind("<Enter>",  # Get over button
                                 lambda event: self.__start_button.config(
                                     bg=BUTTON_HOVER_COLOR))
        self.__start_button.bind("<Leave>",  # Leave widget area
                                 lambda event: self.__start_button.config(
                                     bg=REGULAR_COLOR))

    def __create_submit_button(self):
        """ The function creates submit button """
        self.__submit_button = tk.Button(self.__outer_frame, text="SUBMIT",
                                         **BUTTON_STYLE)
        self.__submit_button.place(relheight=0.05, relwidth=0.1, relx=0.35,
                                   rely=0.2)

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
        self.__submit_button.bind("<Button-1>",
                                  click_on_submit)  # Click on submit
        self.__submit_button.bind("<Enter>",  # Get over button
                                  lambda event: self.__submit_button.config(
                                      bg=BUTTON_HOVER_COLOR))
        self.__submit_button.bind("<Leave>",  # Leave widget area
                                  lambda event: self.__submit_button.config(
                                      bg=REGULAR_COLOR))

    def __create_clear_button(self):
        """ The function creates clear button """
        self.__clear_button = tk.Button(self.__outer_frame, text="CLEAR",
                                        **BUTTON_STYLE)
        self.__clear_button.place(relheight=0.05, relwidth=0.1, relx=0.6,
                                  rely=0.2)

        def click_on_clear(event):
            self.__clear_word()

        # Handling events
        self.__clear_button.bind("<Button-1>",
                                 click_on_clear)  # Click on submit
        self.__clear_button.bind("<Enter>",  # Get over button
                                 lambda event: self.__clear_button.config(
                                     bg=BUTTON_HOVER_COLOR))
        self.__clear_button.bind("<Leave>",  # Leave widget area
                                 lambda event: self.__clear_button.config(
                                     bg=REGULAR_COLOR))

    def __present_time(self, minutes, seconds):
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

        self.__timer.config(
            text=f"Timer: {minutes}:{seconds}")

    def __create_timer(self):
        """ Update the timer to present time and to stop after 3 minutes """

        def update_timer():
            # Calculating clapsed time
            elapsed_time = int(time.time() - self.__start_time)

            # Calculating minutes and seconds for timer
            minutes_left = (TIME_IN_SECS - elapsed_time) // 60
            secs_left = (TIME_IN_SECS - elapsed_time) % 60
            secs_left = 0 if secs_left == 60 else secs_left

            self.__present_time(minutes_left, secs_left)

            if elapsed_time < TIME_IN_SECS:  # Stop the timer after 3 minutes
                self.__timer.after(1000, update_timer)
            else:
                self.__finish_the_game()

        self.__start_time = time.time()
        update_timer()

    def __create_yes_button(self):
        button = tk.Button(self.__board, text="YES",
                           **BUTTON_STYLE)
        button.place(relheight=0.15, relwidth=0.1, relx=0.65, rely=0.7)

        def click_on_yes(event):
            # Recreate board
            self.__configure_board()
            self.__create_letters_buttons()
            # Activate buttons
            self.__start_button.config(state="normal")
            self.__submit_button.config(state="normal")
            self.__clear_button.config(state="normal")
            # Reset game objects
            self.__create_timer()
            self.__score.config(text="score: 0")
            self.__reset_words_list()

        # Handling events
        button.bind("<Button-1>", click_on_yes)  # Click on submit
        button.bind("<Enter>",  # Get over button
                    lambda event: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>",  # Leave widget area
                    lambda event: button.config(bg=REGULAR_COLOR))

    def __create_no_button(self):
        button = tk.Button(self.__board, text="NO",
                           **BUTTON_STYLE)
        button.place(relheight=0.15, relwidth=0.1, relx=0.8, rely=0.7)

        def click_on_no(event):
            # Todo- add pop window with message and total score (also in close)
            self.__window.destroy()

        # Handling events
        button.bind("<Button-1>", click_on_no)  # Click on submit
        button.bind("<Enter>",  # Get over button
                    lambda event: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>",  # Leave widget area
                    lambda event: button.config(bg=REGULAR_COLOR))

    def __finish_the_game(self):
        self.__board = tk.Frame(self.__outer_frame)
        self.__board.place(relheight=0.6, relwidth=0.6, relx=0.1, rely=0.3)

        # Disable buttons and clear word on display
        self.__start_button.config(state="disabled")
        self.__submit_button.config(state="disabled")
        self.__clear_button.config(state="disabled")
        self.__clear_word()

        # Create label with information of ending game
        game_message = tk.Label(self.__board, **LABEL_STYLE)
        game_message.place(relheight=0.15, relwidth=0.3, relx=0.35,
                           rely=0.1)
        game_message.config(text="Your time is up!")

        # Creating label with information of score in last game
        last_score = tk.Label(self.__board, **LABEL_STYLE)
        last_score.config(text=self.__score.cget("text"))
        last_score.place(relheight=0.15, relwidth=0.2, relx=0.4,
                         rely=0.4)

        # Creating label with question about new game
        new_game = tk.Label(self.__board, **LABEL_STYLE)
        new_game.place(relheight=0.15, relwidth=0.5, relx=0.1,
                       rely=0.7)
        new_game.config(text="Do you want to play again?")
        # Create buttons to answer the question
        self.__create_yes_button()
        self.__create_no_button()

    def __create_close_button(self):
        """ The function creates close button which is close the window """
        button = tk.Button(self.__outer_frame, text="CLOSE",
                           **BUTTON_STYLE)
        button.place(relheight=0.05, relwidth=0.1, relx=0.9, rely=0.0)

        def click_on_close(event):
            self.__window.destroy()

        # Handling events
        button.bind("<Button-1>", click_on_close)  # Click on submit
        button.bind("<Enter>",  # Get over button
                    lambda event: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>",  # Leave widget area
                    lambda event: button.config(bg=REGULAR_COLOR))

    def run(self):
        """ The function runs the game """
        self.__window.mainloop()


if __name__ == '__main__':
    gui = BoogleGUI()
    gui.run()
