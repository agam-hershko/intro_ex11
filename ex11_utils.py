from typing import *
from boggle_board_randomizer import randomize_board
import string

Board = List[List[str]]
Path = List[Tuple[int, int]]

# Generate a random board
Board = randomize_board()


def create_dict(index_file):
    """
    Create a dictionary of all words from the index file.
    Keys: letters of the alphabet
    Values: set of all the words that begin with this letter
    """
    all_letters = list(string.ascii_uppercase)
    all_letters.append("QU")
    dict_words = {letter: set() for letter in all_letters}
    with open(index_file, 'r') as index:
        words = index.readlines()
        for word in words:
            word = word.replace('\n', '')
            dict_words[word[0]].add(word)
    return dict_words


def create_set(index_file):
    """
    Create a set of all the words in the index file
    """
    set_words = set()
    with open(index_file, 'r') as index:
        words = index.readlines()
        for word in words:
            word = word.replace('\n', '')
            set_words.add(word)
    return set_words


def dist(coor1, coor2):
    """
    Calculate the distance between two coordinates
    """
    return (abs(coor1[0] - coor2[0]), abs(coor1[1] - coor2[1]))


def is_valid_path(board, path, words):
    """
    Check if a given path on the board is valid
    """
    # Verification of the path:
    num_row = len(board)
    num_col = len(board[0])

    # Verification of unique coordinates
    list_max_paths = set()
    for index, (x, y) in enumerate(path):
        if (x, y) in list_max_paths:
            return None
        else:
            list_max_paths.add((x, y))

        # Verification of board boundaries
        if not (0 <= y < num_row and 0 <= x < num_col):
            return None

        # Verification of adjacent coordinates
        if index != len(path) - 1 and dist(path[index + 1], (x, y)) not in {(1, 0), (0, 1), (1, 1)}:
            return None

    # Check if the word formed by the path exists in the word list
    word = ""
    for y, x in path:
        word += board[y][x]

    return word if word in words else None


def add_letter(board, y: int, x: int, path):
    """
    Generator to yield coordinates and paths of adjacent letters on the board
    """
    for row,col in [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                     (y, x - 1), (y, x + 1),
                     (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]:
        if row >= 0 and col >= 0 and row < len(board) and col < len(board[0]):
            yield (path + [(row, col)], (row, col))


def helper_find(n, board, words, x, y, path):
    """
    Recursive helper function to find all paths of length n on the board
    """
    if len(path) == n:
        if is_valid_path(board, path, words):
            yield path
            return

    for next_path, (row, col) in list(add_letter(board, x, y, path)):
        old_path = path
        path = list(next_path)
        if len(path) <= n:
            yield from helper_find(n, board, words, row, col, path)
        path = old_path


def find_all_length_n_paths(n: int, board, words):
    """
    Find all paths of length n on the board
    """
    for index_row, row in enumerate(board):
        for index_col, letter in enumerate(row):
            yield (helper_find(n, board, words, index_row, index_col, [(index_row, index_col)]))


def find_length_n_paths(n: int, board, words):
    """
    Find all paths of length n on the board that form valid words
    """
    ans = []
    for result in find_all_length_n_paths(n, board, words):
        if result:
            for sub_result in result:
                ans.append(sub_result)
    return ans


def create_word(path, board):
    """
    Create a word from a given path on the board
    """
    word = ""
    for y, x in path:
        word += board[y][x]

    return word


def helper_find_word(n, board, words, x, y, path):
    """
    Recursive helper function to find all paths of length n on the board that form valid words
    """
    if len(path) == n:
        if is_valid_path(board, path, words) and len(create_word(path, board)) == n:
            yield path
            return

    for next_path, (row, col) in list(add_letter(board, x, y, path)):
        old_path = path
        path = list(next_path)
        if len(path) <= n:
            yield from helper_find_word(n, board, words, row, col, path)
        path = old_path


def find_all_length_n_word(n: int, board, words):
    """
    Find all paths of length n on the board that form valid words
    """
    for index_row, row in enumerate(board):
        for index_col, letter in enumerate(row):
            yield (helper_find_word(n, board, words, index_row, index_col, [(index_row, index_col)]))


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    Find all paths of length n on the board that form valid words
    """
    ans = []
    for result in find_all_length_n_word(n, board, words):
        if result:
            for sub_result in result:
                ans.append(sub_result)
    return ans


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    Find all paths on the board that yield maximum score based on word lengths
    """
    n = len(board) + len(board[0])
    list_max_paths = []
    for iter in range(n + 1):
        all_word_len_iter = find_length_n_words(iter, board, words)
        for coor in all_word_len_iter:
            if coor in list_max_paths:
                continue
            else:
                list_max_paths.append(coor)
    return list_max_paths

