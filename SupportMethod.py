import NerAnalysis
import analizeQuestion

def Transitivity(otter, inURI):
    otter.write("\n%In Transitivity\n")
    otter.write("-rdf(X,\""+ inURI+ "\",Y) | -rdf(Y,\""+ inURI+ "\",Z) | (rdf(X,\""+ inURI+ "\",Z)).\n")


def exclusively(otter, beList, beURI):
    otter.write("\n%Exclusively\n")
    for i in range(0, beList.__len__()):
        otter.write("rdf(X,\"" + beURI + "\",\"" + beList[i] + "\")")
        for j in range(0, beList.__len__()):
            if i != j:
                otter.write(" & -rdf(X,\"" + beURI + "\",\"" + beList[j] + "\")")
        otter.write(".\n")


def synonym(otter, synURI):
    otter.write("\n%Synonym A => B =====> -A | B\n")
    for i in range(0, synURI.__len__() - 1):
        for j in range(i+1, synURI.__len__()):
            if i != j:
                otter.write("-rdf(X,\"" + synURI[i] + "\", Y)")
                otter.write(" | rdf(X,\"" + synURI[j] + "\",Y).\n")

def antonym(otter, synURI):
    otter.write("\n%Antonym A => -B =====> -A | -B\n")
    for i in range(0, synURI.__len__() - 1):
        for j in range(i+1, synURI.__len__()):
            if i != j:
                otter.write("-rdf(X,\"" + synURI[i] + "\", Y)")
                otter.write(" | -rdf(X,\"" + synURI[j] + "\",Y).\n")

def QuestionAnalyzer(otter):
    #nlp = spacy.load('E:\Programmi\Anaconda\envs\spacy\Lib\site-packages\en_core_web_md\en_core_web_md-1.2.1')

    #question = input("What's your question? -> ")
    string = "is Tallinn in Estonia?"
    #doc = nlp(question)

    nlp = NerAnalysis.getNlp()
    NER = NerAnalysis.NerAnalysis(string, nlp)

    NER.printTree()
    NER.printInformation()

    nounArray = NER.findNouns()
    print("----------------")
    print(nounArray)
    print("----------------")
    verbArray = NER.findVerbs()
    print("----------------")
    print(verbArray)
    print("----------------")

    rdf = analizeQuestion.Question(nlp, otter, nounArray, verbArray)

    rdf.findFirst(string)



