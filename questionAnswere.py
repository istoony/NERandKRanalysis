import SupportMethod
import wordUri


file = open("testfile.txt", "r")

content = file.readlines()
content = [x.strip() for x in content]

print(content)

for i in range(0, content.__len__()):
    content[i] = content[i].split(";")

print(content)

for x in content:
    for i in range(0, x.__len__()):
        x[i] = x[i].lstrip()
    #x.remove('');

print(content)

"""
rdf("http://en.wikipedia.org/wiki/Barack_Obama",
      "id:type",
      "http://conceptnet5.media.mit.edu/web/c/en/person").
"""

otter = open("otter.txt", "w")

otter.write("""
% clear automatic strategy selection
clear(auto).

% use capital letters (A,X,T,...) as vars
set(prolog_style_variables).

% select the search strategy
set(hyper_res). % an alternative is to use set(binary_res).
set(factor).

% select sensible amount of output
clear(print_given). % uncomment to see input and process
set(print_kept).  % this is important: prints all generated and kept clauses
assign(stats_level, 0).

% just make it stop after N secs
assign(max_seconds, 10).

list(sos).

% example data
""")

verbList = []
beList = []

beURI = "http://api.conceptnet.io/c/en/is"

for sentence in content:
    otter.write("rdf(\"" + sentence[0] + "\",\"" + sentence[1] + "\",\"" + sentence[2] + "\").\n")
    print("rdf(\"" + sentence[0] + "\",\"" + sentence[1] + "\",\"" + sentence[2] + "\").")

    if sentence[1] not in verbList:
        verbList.append(sentence[1])

    if sentence[1] == beURI and not sentence[2] in beList:
        beList.append(sentence[2])


SupportMethod.Transitivity(otter, "http://api.conceptnet.io/c/en/in")
SupportMethod.exclusively(otter,beList,beURI)

otter.write("%generated from concept5\n")

for lis in verbList:
    syn = wordUri.findUriPartOf(lis)
    print("partof ->" + syn)
    #SupportMethod.synonym(otter, syn)

for lis in verbList:
    syn = wordUri.findUriSynonym(lis)
    print("Syn-> " + syn)
    # SupportMethod.synonym(otter, syn)

for lis in verbList:
    syn = wordUri.findUriAntonym(lis)
    print("Anton->" + syn)
    # SupportMethod.antonym(otter, syn)
    

otter.write("%Questions\n")
SupportMethod.QuestionAnalyzer(otter)

otter.write("end_of_list.")

