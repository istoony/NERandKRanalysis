class WordArray():

    def __init__(self):
        self.word = []

    def addWord(self, word):
        for w in self.word:
            if w.word == word.word:
                return
        self.word.append(word)

    def getDimension(self):
        return len(self.word)

    def __repr__(self):
        temp = []
        for w in self.word:
            temp.append(w.__repr__())
        return temp.__repr__()

    def __iter__(self):
        return iter(self.word)

    def __len__(self):
        return len(self.word)

    def __getitem__(self, item):
        return self.word[item]

    def __setitem__(self, key, value):
        self.word[key] = value

    def __delitem__(self, key):
        self.word.__delitem__(key)

    def findWord(self, word):
        for w in self.word:
            if word in w.word.split():
                return w
        return None;
