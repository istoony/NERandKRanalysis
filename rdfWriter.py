import datastructure
import wordUri


class RdfWriter:
    def __init__(self, nlp, sentence, nounArray, verbArray):
        self.nlp = nlp
        self.doc = nlp(sentence)
        self.sentence = sentence
        self.nounArray = nounArray
        self.verbArray = verbArray
        self.file = open("questionFile.txt","w")

    def writeNamesPropery(self):
        for noun in self.nounArray:

            #######################
            noun.addUri(noun.word + "URI")  #
            ###################à###

    def writeVerbProperty(self):
        for verb in self.verbArray:
            #######################
            verb.addUri(verb.root + "URI")  #
            ###################à###

    def writerdf(self):
        for sentence in self.doc.sents:
            print(sentence.orth_)
            self.findFirst(sentence)

    def findFirst(self, sentence):
        sentenceDoc = self.nlp(sentence.orth_)
        for word in sentenceDoc:
            if word.dep_ == "nsubj":
                temp = self.nounArray.findWord(word.orth_)
                self.findSecond(sentenceDoc, temp)
                break

    def findSecond(self, sentenceDoc, subject):
        for word in sentenceDoc:
            if word.dep_ == "ROOT":
                verb = self.verbArray.findWord(word.orth_)

                children = []
                for ch in word.children:
                    children.append(ch)
                self.findThird(sentenceDoc, subject, verb, children)
                break

    def findThird(self, sentenceDoc, subject, verb, children):
        found = False
        for child in children:

            if child.dep_ == "attr":
                temp = self.nounArray.findWord(child.orth_)
                if temp is None:
                    w = datastructure.Word(child.orth_)
                    w.addType(child.pos_)
                    w.addUri(wordUri.findUri(child.lemma_))
                    #w.addUri(w.word + "URI")
                    print(subject.uri, "- " + verb.uri + " -", w.uri)
                    self.file.write(subject.uri + "; " + verb.uri + "; " + w.uri + "\n")
                else:
                    print(subject.uri, "- " + verb.uri + " -", temp.uri)
                    self.file.write(subject.uri + "; " + verb.uri + "; " + temp.uri + "\n")
                self.recoursiveFind(sentenceDoc, subject, verb, child)
                found = True
        if not found:
            for word in sentenceDoc:
                if word.dep_ == "ROOT":
                    verbDoc = word
                    break
            self.recoursiveFind(sentenceDoc, subject, verb, verbDoc)

    def recoursiveFind(self, sentenceDoc, subject, verb, root):
        pred = verb.word
        adv = findVerbModifier(sentenceDoc)
        flag = True
        if adv:
            pred = pred + adv.orth_
            flag = False
            root = adv
        for child in root.children:
            if child.dep_ == "prep":
                for proj in child.children:
                    if proj.dep_ == "pobj":
                        temp = self.nounArray.findWord(proj.orth_)
                        if flag:
                            newWord = datastructure.Word(child.orth_)
                            newWord.addType(child.pos_)
                            newWord.addUri(wordUri.findUri(newWord))
                            #newWord.addUri(newWord.word + "URI")
                            print(subject.uri, "- " + newWord.uri + " -", temp.uri)
                            self.file.write(subject.uri + "; " + newWord.uri + "; " + temp.uri + "\n")
                        else:
                            newWord = datastructure.Word(adv.orth_)
                            newWord.addType(adv.pos_)
                            newWord.addUri(wordUri.findUri(newWord))
                            #newWord.addUri(newWord.word + "URI")
                            print(subject.uri, "- " + newWord.uri + " -", temp.uri)
                            self.file.write(subject.uri + "; " + newWord.uri + "; " + temp.uri + "\n")
                        break


def findVerbModifier(sentenceDoc):

    modifiersList = ["advmod", "acomp"]

    for word in sentenceDoc:
        if word.dep_ in modifiersList:
            return word
    return False
