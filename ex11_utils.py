from typing import *

Board = List[List[str]]
Path = List[Tuple[int, int]]


def get_max_score(board, words):
    """
    The function returns the max score in a game for the board
    """
    max_score = 0
    for path in max_score_paths(board, words):
        max_score += len(path) ** 2
    return max_score


def get_distance(coor1, coor2):
    """
    Calculate the distance between two coordinates
    """
    return abs(coor1[0] - coor2[0]), abs(coor1[1] - coor2[1])


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
        if index != len(path) - 1 and get_distance(path[index + 1], (x, y)) \
                not in {(1, 0), (0, 1), (1, 1)}:
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
    for row, col in [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                     (y, x - 1), (y, x + 1),
                     (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]:
        if 0 <= row < len(board) and 0 <= col < len(board[0]):
            path.append((row, col))
            yield path, (row, col)
            path.pop()


def helper_find(n, board, words, x, y, path):
    """
    Recursive helper function to find all paths of length n on the board
    """
    word = "".join(board[i][j] for i, j in path)
    words = [w for w in words if w.startswith(word)]

    if len(words) == 0:
        return
    if len(path) in n:
        if is_valid_path(board, path, words):
            yield path
    if len(path) == max(n):
        return

    for next_path, (row, col) in add_letter(board, x, y, path):
        if (row, col) in path[0:-2]:
            continue
        path = next_path
        yield from helper_find(n, board, words, row, col, path)


def find_all_length_n_paths(n: Set[int], board, words):
    """
    Find all paths of length n on the board
    """
    m = min(n)
    words = list(sorted(w for w in words if len(w) >= m))
    for index_row, row in enumerate(board):
        for index_col, _ in enumerate(row):
            yield from (helper_find(n, board, words, index_row, index_col,
                                    [(index_row, index_col)]))


def find_length_n_paths(n: int, board, words):
    """
    Find all paths of length n on the board that form valid words
    """
    ans = []
    for result in find_all_length_n_paths({n}, board, words):
        ans.append(result.copy())
    return ans


def helper_find_word(n, board, words, x, y, path):
    """
    Recursive helper function to find all paths of length n on the board that
    form valid words
    """

    word = "".join(board[i][j] for i, j in path)
    words = [w
             for w in words
             if w.startswith(word)]
    if len(words) == 0:
        return
    if len(word) == n:
        if is_valid_path(board, path, words):
            yield path
        return

    for next_path, (row, col) in add_letter(board, x, y, path):
        if (row, col) in path[0:-2]:
            continue
        path = next_path
        if len(path) <= n:
            yield from helper_find_word(n, board, words, row, col, path)


def find_all_length_n_words(n: int, board, words):
    """
    Find all paths of length n on the board that form valid words
    """
    for index_row, row in enumerate(board):
        for index_col, _ in enumerate(row):
            yield from (helper_find_word(n, board, words, index_row, index_col,
                                         [(index_row, index_col)]))


def find_length_n_words(n: int, board: Board, words: Iterable[str])\
        -> List[Path]:
    """
    Find all paths of length n on the board that form valid words
    """
    words = list(sorted(w for w in words if len(w) == n))
    ans = []
    for result in find_all_length_n_words(n, board, words):
        ans.append(result.copy())
    return ans


def create_word(path, board):
    """
    Create a word from a given path on the board
    """
    word = ""
    for y, x in path:
        word += board[y][x]

    return word


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    Find all paths on the board that yield maximum score based on word lengths
    """
    n = len(board) * len(board[0])

    list_max_paths = {}

    all_word_len_iter = find_all_length_n_paths(set(range(1, n + 1)), board,
                                                words)

    for path in all_word_len_iter:
        word = create_word(path, board)
        if word in list_max_paths:
            if len(path) > len(list_max_paths[word]):
                list_max_paths[word] = path.copy()
        else:
            list_max_paths[word] = path.copy()

    return list(list_max_paths.values())
