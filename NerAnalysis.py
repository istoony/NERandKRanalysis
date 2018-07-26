"""
    NOUN -> obj.word = "china"
            obj.type = "PROPN" "NOUN" ... -> google pos standard
            obj.category = "GPE" "ORG" ...  -> spacy/usage/entity-recognition

    VERB -> obj.word = "is" "play" ...
            obj.type = "VERB"
            obj.root = "be" "play" -> the root of the verb
"""

import spacy
import nltk.tree
from WordArray import WordArray
import datastructure
import wordUri


def getNlp():
    return spacy.load('E:\Programmi\Anaconda\envs\spacy\Lib\site-packages\en_core_web_md\en_core_web_md-1.2.1')
    # return spacy.load('E:\Programmi\Anaconda\envs\spacy\Lib\site-packages\en_core_web_sm\en_core_web_sm-1.2.0')


class NerAnalysis:
    def __init__(self, sentence, nlp):
        self.nlp = nlp
        self.doc = self.nlp(sentence)

    def changeDoc(self, sentence):
        self.doc = self.nlp(sentence)

    def printTree(self):
        [self.to_nltk_tree(sent.root, self.doc).pretty_print() for sent in self.doc.sents]

    def to_nltk_tree(self, node, doc):
        if node.n_lefts + node.n_rights > 0:
            return nltk.tree.Tree(node.orth_, [self.to_nltk_tree(child, doc) for child in node.children])
        else:
               return node.orth_ + node.dep_

    def findNouns(self):
        nounArray = WordArray()
        entities = list(self.doc.ents)
        # print("There were {} entities found".format(len(entities)))
        # print(entities)
        for e in [entity for entity in entities if entity.label_ not in ['DATE', 'TIME', 'PERCENT', 'CARDINAL', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']]:
            temp = datastructure.Noun(e.orth_)
            temp.addCategory(e.label_)
            end = True
            for w in self.doc:
                if end:
                    string = e.orth_.split()
                    if w.orth_ in string:
                        temp.addType(w.pos_)
                        temp.addUri(wordUri.findUri(temp))
                        end = False

            nounArray.addWord(temp)

        for word in self.doc.noun_chunks:
            temp = datastructure.Noun(word.orth_)
            temp.addCategory("UNKNOWN")
            temp.addType("NOUN")
            if temp not in nounArray:
                temp.addUri(wordUri.findUri(temp))
                nounArray.addWord(temp)
                print(temp)

        for word in self.doc:
            # print(nc.orth_)
            if word.pos_ == 'NOUN' or word.pos_ == "PROPN":
                temp = datastructure.Noun(word.orth_)
                temp.addCategory("UNKNOWN")
                temp.addType(word.pos_)
                temp.addUri(wordUri.findUri(temp))
                if temp not in nounArray:
                    nounArray.addWord(temp)

        nounArray = purifyNounArray(nounArray)
        nounArray = removeArticles(nounArray, self.doc)

        return nounArray

    def findVerbs(self):
        verbsArray = WordArray()
        temp = []
        for word in self.doc:
            if word.pos_ == 'VERB' and word.orth_ not in temp:

                temp.append(word.orth_)
                verb = datastructure.Verb(word.orth_)
                verb.addRoot(word.lemma_)
                verb.addType(word.pos_)

                verb.addUri(wordUri.findUri(verb))

                verbsArray.addWord(verb)

        return verbsArray

    def simplifyMultipleSentences(self):
        result = ""
        for sent in self.doc.sents:
            print(sent.orth_)
            doc = self.nlp(sent.orth_)
            result = result + splitConjunction(doc) + " "
        result = result[:-1]
        return result

    def removePronouns(self):
        result = ""
        for sent in self.doc.sents:
            print(sent.orth_)
            doc = self.nlp(sent.orth_)
            result = result + removePronounsForSentence(doc) + " "
        result = result[:-1]
        return result

    def printInformation(self):
        for w in self.doc:
            printWordInformation(w)


def purifyNounArray(nounArray):
    print(nounArray)
    temp = []
    for i in range(0, len(nounArray)):
        for j in range(0, len(nounArray)):
            if nounArray[i].word in nounArray[j].word and i != j:
                if nounArray[i].category != "UNKNOWN":
                    nounArray[j].addCategory(nounArray[i].category)
                if nounArray[i].type != "UNKNOWN":
                    nounArray[j].addType(nounArray[i].type)
                temp.append(nounArray[i])
    print(temp)
    array = [x for x in nounArray.word if x not in temp]
    realArray = WordArray()
    for a in array:
        realArray.addWord(a)
    return realArray


def removeArticles(nounArray, doc):

    removeList = ["det", "amod", "nummod"]

    for word in nounArray:
        if len(word.word.split()) > 1 and word.type != "PROPN":
            for w in doc:
                if w.orth_ in word.word.split() and w.dep_ in removeList:
                    temp = word.word.split()
                    string = ""
                    for t in temp:
                        if w.orth_ != t:
                            string = string + t + " "
                    word.word = string[:-1]
        word.addUri(wordUri.findUri(word))
    return nounArray


def splitConjunction(doc):
    verb_count = 0
    end = True

    for word in doc:

        if word.dep_ == "cc":
            cc_count = word.i
            noun_count = word.i - 1
            conj_count = word.i + 1
            end = False

        if word.pos_ == "VERB":
            verb_count = verb_count + 1

    result = ""
    if end:
        return doc.text

    if verb_count == 2:
        for w in doc:
            if w.i != cc_count and w.orth_ != "." and w.i != 0:
                result = result + " " + w.orth_
            elif w.i != cc_count and w.orth_ != "." and w.i == 0:
                result = w.orth_
            elif w.orth_ == ".":
                result = result + w.orth_
            else:
                result = result + "."

    elif verb_count == 1:
        for i in range(0, 2):
            for w in doc:
                if w.i != cc_count:
                    if i == 0 and w.i != conj_count and w.i != 0:
                        result = result + " " + w.orth_
                    elif i == 0 and w.i != conj_count and w.i == 0:
                        result = w.orth_

                    if i == 1 and w.i != noun_count:
                        result = result + " " + w.orth_
            result = result[:-2]
            result = result + "."

    return result


def printWordInformation(word):
        print(word.orth_)
        print("pos_ -> ", word.pos_)
        print("dep_ -> ", word.dep_)
        print("lemma_ ->", word.lemma_)
        print("children", [child.orth_ for child in word.children])
        print("conjuncts", [child.orth_ for child in word.conjuncts])
        print("subtree", [child.orth_ for child in word.subtree])
        print("ancestors", [child.orth_ for child in word.ancestors])


def removePronounsForSentence(sentenceDoc):
    result = ""
    flag = True
    for w in sentenceDoc:
        if w.pos_ == "PRON" and w.dep_ == "nsubj":
            print("WORD FOUND -> ", w.orth_)
            prop_count = w.i
            flag = False

    if flag:
        return sentenceDoc.text

    for k in sentenceDoc:

        if k.dep_ == "nsubj" and (k.pos_ == "PROPN" or k.pos_ == "NOUN"):
            temp = k.orth_

        if k.i == 0 and k.i != prop_count:
            result = k.orth_
        elif k.i != 0 and k.i != prop_count:
            result = result + " " + k.orth_
        else:
            result = result + " " + temp
    result = result[:-2]
    result = result + "."
    return result

