import vectorizeWordDiego as vwd
import trie as t
import cleanText
import time

def closestWords(matrix, words,cantTextos):
    closest = []
    if len(words) > 4:
        toGetClosest = False
    else:
        toGetClosest = True
        
    if len(words) > 15:
        return words
    
    for word in words:
        closest.append(word)
        closeWords = vwd.getClosestWords(matrix,word,len(matrix[word]),cantTextos,toGetClosest)
        if closeWords is not None:
            for closeWord in closeWords:
                closest.append(closeWord)
    closest = [word for word in closest if word.strip() != '']
    return closest


def splitTextsParagraphs(texts):
    texts = vwd.splitTexts(texts)
    for text in range(len(texts)):
        texts[text] = cleanText.cleanText(texts[text])
    return texts
        

def checkWordInMatrix(matrix,strInput):
    arrayInput = []
    for word in strInput:
        if vwd.existInMatrix(matrix, word):
            arrayInput.append(word)
    return arrayInput


def rankDocumentsTest(trie,words,cantTextos,pdfNames):
    documents = {pdfNames[i]: 0 for i in range(cantTextos)}
    for i in range(cantTextos):
        documents[i] = 0
    dictWords = t.searchTrieDict(trie,words)
    for word in dictWords:
        if dictWords[word] is not None:
            for doc in dictWords[word]:
                if doc is not None:
                    documents[pdfNames[doc]] += 1    
    
    documents = {k: v for k, v in documents.items() if v != 0}
                
    documents = sorted(documents.items(), key=lambda x: x[1], reverse=True)
    documents = [x[0] for x in documents]
    return documents


def getClosest(consulta,T,amountDocuments, pdfNames,matrix):
    arrayInput = checkWordInMatrix(matrix,consulta)
    if len(arrayInput) == 0:
        return "Document not found"
    else:
        time1 = time.time()
        closest = closestWords(matrix,arrayInput,len(pdfNames))
        time1 = time.time() - time1
        print("Time to get closest words: ", time1)
        print('')
        print(closest)
        return rankDocumentsTest(T,closest,amountDocuments,pdfNames)
    
    