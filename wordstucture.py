class WordStructure:

    """
        identifier
        words = []
        full word
        wiki reference
        type = "NOUN - VERB - ADJECTIVE - PREPOSITION - ..."
        other information
    """
    def __init__(self, id, words, fullstring, wikireference, type, other):
        self.id = id
        self.words = words
        self.fullstring = fullstring
        self.wikireference = wikireference
        self.type = type
        self.other = other


