class Word:

    def __init__(self, word):
        self.word = word
        self.type = "UNKNOWN"
        self.uri = ""

    def addUri(self, uri):
        self.uri = uri

    def addType(self, types):
        if self.type == "UNKNOWN":
            self.type = types

    def __repr__(self):
        return self.word

    def __eq__(self, other):
        return self.word == other.word


class Noun(Word):
    def __init__(self, word):
        super(Noun, self).__init__(word)
        self.category = ""
        self.unit = ""

    def addCategory(self, category):
        self.category = category

    def addUnit(self, unit):
        self.unit = unit

    def __repr__(self):
        return str(self.word) + "->" + str(self.category) + "->" + str(self.type)


class Verb(Word):

    def __init__(self, word):
        super(Verb, self).__init__(word)
        self.time = "now"
        self.root = ""
        self.attribute = ""

    def addRoot(self, root):
        self.root = root

    def addtime(self, time):
        self.time = time

    def addAttr(self, attr):
        self.attribute = attr

    def __repr__(self):
        return str(self.word) + "-->" + str(self.root)


class Other(Word):

    def __init__(self, word):
        super(Other, self).__init__(word)
        self.time = ""
        self.extrainfo = ""

    def addTime(self, time):
        self.time = time

    def addExtrainfo(self, extrainfo):
        self.extrainfo = extrainfo
