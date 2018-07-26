
import NerAnalysis
import rdfWriter

string = "Puise is a village and it is north of Matsalu bay." \
        "Tallinn is in Estonia." \
        "Milano is in Italy." \
        "Italy is a country." \
        "Milano is a city." \
        "Tallinn is a city." \
        "Estonia is a country."\
        "Italy is in Europe."\
        "Estonia is in Europe." \
        "Europe is a continent." \
        "Rome is bigger than tartu."
        #"Milano is far from Tallinn." \
        #"Estonia is in Europe." \
        #"Tallinn is close to the sea." \
        #"Rome is bigger than Tartu."


nlp = NerAnalysis.getNlp()
NER = NerAnalysis.NerAnalysis(string, nlp)

noPronounsStr = NER.removePronouns()
NER.changeDoc(noPronounsStr)
print("----NO PRONOUNS----")
print(noPronounsStr)
print("-------------------")

newString = NER.simplifyMultipleSentences()

print("----NEW STRING----")
print(newString)
print("------------------")

NER.changeDoc(newString)
NER.printTree()

nounArray = NER.findNouns()
print("----------------")
print(nounArray)
print("----------------")
verbArray = NER.findVerbs()
print("----------------")
print(verbArray)
print("----------------")

NER.printInformation()

rdf = rdfWriter.RdfWriter(nlp, newString, nounArray, verbArray)

#rdf.writeNamesPropery()
#rdf.writeVerbProperty()

rdf.writerdf()
