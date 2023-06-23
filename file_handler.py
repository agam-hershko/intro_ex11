#################################################################
# FILE : file_handler.py
# WRITER : agam hershko, id_214193831 , 214193831
# EXERCISE : intro2cs2 ex11 2023
# DESCRIPTION: A program that implements handling text files
# STUDENTS I DISCUSSED THE EXERCISE WITH: -
# NOTES: -
#################################################################

def create_words_set(index_file):
    """
    create a set of all the words in the index file
    """
    set_words = set()
    with open(index_file, 'r') as index:
        words = index.readlines()
        for word in words:
            word = word.replace('\n', '')
            set_words.add(word)
    return set_words
