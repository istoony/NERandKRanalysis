import datastructure
import wordUri


class Question:
    def __init__(self, nlp, otter, nounArray, verbArray):
        self.nlp = nlp
        self.nounArray = nounArray
        self.verbArray = verbArray
        self.file = otter


    def findFirst(self, sentence):
        sentenceDoc = self.nlp(sentence)
        for word in sentenceDoc:
            if word.dep_ == "ROOT":
                verb = self.verbArray.findWord(word.orth_)

                children = []
                for ch in word.children:
                    children.append(ch)
                self.findSecond(sentenceDoc, verb, children)
                break

    def findSecond(self, sentenceDoc, verb, children):

        for child in children:
            if child.dep_ == "attr" or child.dep_ == "nsubj":
                temp = self.nounArray.findWord(child.orth_)

                subjectChildren = []
                for ch in child.children:
                    subjectChildren.append(ch)

                if not subjectChildren:
                    subjectChildren = children
                    subjectChildren.remove(child)
                self.findThird(sentenceDoc, temp, verb, subjectChildren, False)
                break

    def findThird(self, sentenceDoc, subject, verb, children, flag):
        for child in children:
            if child.dep_ == "appos" or child.dep_ == "pobj":
                temp = self.nounArray.findWord(child.orth_)
                if temp is None:
                    w = datastructure.Word(child.orth_)
                    w.addType(child.pos_)
                    w.addUri(wordUri.findUri(w))
                    #w.addUri(w.word + "URI")
                    print(subject.uri, "- " + verb.uri + " -", w.uri)

                    self.writeOtter(subject.uri, verb.uri, w.uri)

                else:
                    print(subject.uri, "- " + verb.uri + " -", temp.uri)
                    self.writeOtter(subject.uri, verb.uri, temp.uri)

                #self.recoursiveFind(sentenceDoc, subject, verb, child)
            if child.dep_ == "prep" or child.dep_ == "acomp":
                if not flag:
                    verb = datastructure.Word(child.orth_)
                    verb.addType(child.pos_)
                    verb.addUri(wordUri.findUri(verb))

                verbChildren = []
                for ch in child.children:
                    verbChildren.append(ch)

                self.findThird(sentenceDoc, subject, verb, verbChildren, True)

    def writeOtter(self, first, second, third):
        self.file.write("-rdf(\"" + first + "\", \"" + second + "\", \"" + third + "\").\n")
