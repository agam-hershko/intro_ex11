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
