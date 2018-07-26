import requests
import datastructure


# This function utilizes the Python Requests module to process requests to both DBPedia and ConceptNet.
def findUri(word):
    url = ''
    if word:
        print(word.word, " - ", word.type)
        # If word is of type PROPN, it replaces all spaces and capitalizes the first letter of the word. It then
        # proceeds with a request to DBPedia in order to find the Wikipedia URL for the word.
        if word.type == 'PROPN':
            if word.word != '':
                name_holder = word.word.replace(' ', '_').title()
                data = requests.get('http://dbpedia.org/data/' + name_holder + '.json').json()
                try:
                    resource_holder = data['http://dbpedia.org/resource/' + name_holder]
                    url = resource_holder['http://xmlns.com/foaf/0.1/isPrimaryTopicOf'][0]['value']
                except KeyError:
                    pass
            else:
                print('Word has no searchable value defined')
        # Same case as for PROPN, this one uses the word type "NOUN".
        if word.type == 'NOUN':
            if word.word != '':
                name_holder = word.word.replace(' ', '_').title()
                data = requests.get('http://dbpedia.org/data/' + name_holder + '.json').json()
                try:
                    resource_holder = data['http://dbpedia.org/resource/' + name_holder]
                    url = resource_holder['http://xmlns.com/foaf/0.1/isPrimaryTopicOf'][0]['value']
                except KeyError:
                    pass
            else:
                print('Word has no searchable value defined')

        # For the word type ADJ (adjective) we decided to provide a ConceptNet URL which links to the URI of the word.
        if word.type == 'ADJ':
            data = requests.get('http://api.conceptnet.io/c/en/' + word.word).json()

            if data.items:
                try:
                    print(data['error']['details'])
                except KeyError:
                    url = 'http://api.conceptnet.io' + data['@id']
                    pass

        # Same case as for ADJ, in this case we use the word type VERB.
        if word.type == 'VERB':
            data = requests.get('http://api.conceptnet.io/c/en/' + word.word).json()

            if data.items:
                try:
                    print(data['error']['details'])
                except KeyError:
                    url = 'http://api.conceptnet.io' + data['@id']
                    pass

        # Same case as for ADJ, in this case we use the word type ADP.
        if word.type == 'ADP':
            data = requests.get('http://api.conceptnet.io/c/en/' + word.word).json()

            if data.items:
                try:
                    print(data['error']['details'])
                except KeyError:
                    url = 'http://api.conceptnet.io' + data['@id']
                    pass

        if url != '':
            return url

        else:
            print("Error finding URL.")
            return word.word
    else:
        print("Error with word.")
        return word.word


def findUriAntonym(uri):
    antonymUri = ''
    if uri:
        uri = uri[0].lower() + uri[1:]
        print(uri)
        data = requests.get(uri).json()
        if data.items:
            try:
                print(data['error']['details'])
            except KeyError:
                antonymData = requests.get(
                    'http://api.conceptnet.io/query?node=' + data['@id'] + '&rel=/r/Antonym').json()
                if not antonymData['edges']:
                    print("Unable to find antonyms")
                else:
                    antonymUri = antonymData['edges'][0]['start']['@id']
                pass
        if antonymUri != '':
            return antonymUri
        else:
            print("Error finding antonym URI.")
            return uri
    else:
        print("Error with URI.")
        return uri


def findUriPartOf(uri):
    partUri = ''
    if uri:
        uri = uri[0].lower() + uri[1:]
        data = requests.get(uri).json()
        if data.items:
            try:
                print(data['error']['details'])
            except KeyError:
                partData = requests.get(
                    'http://api.conceptnet.io/query?node=' + data['@id'] + '&rel=/r/PartOf').json()
                if not partData['edges']:
                    print("Unable to find part of")
                else:
                    partUri = partData['edges'][0]['start']['@id']
                pass
        if partUri != '':
            return partUri
        else:
            print("Error finding partof URI.")
            return uri
    else:
        print("Error with URI.")
        return uri


def findUriSynonym(uri):
    synonymUri = ''
    if uri:
        uri = uri[0].lower() + uri[1:]
        print(uri)
        data = requests.get(uri).json()
        if data.items:
            try:
                print(data['error']['details'])
            except KeyError:
                synonymData = requests.get(
                    'http://api.conceptnet.io/query?node=' + data['@id'] + '&rel=/r/Synonym').json()
                if not synonymData['edges']:
                    print("Unable to find synonyms")
                else:
                    synonymUri = synonymData['edges'][0]['start']['@id']
                pass
        if synonymUri != '':
            return synonymUri
        else:
            print("Error finding synonym URI.")
            return uri
    else:
        print("Error with URI.")
        return uri
