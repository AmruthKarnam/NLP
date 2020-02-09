# Starting part

import nltk
from nltk.corpus import stopwords 
from nltk.corpus import inaugural
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer,WordNetLemmatizer
import pyphen
import spacy
#nltk.download('inaugural')
#nltk.download('stopwords')
#nltk.download('punkt')
a=inaugural.fileids()
length1=len(a)
index=length1-1
speech=[]
count=0
while(count <5):
    speech.append(a[index])
    index=index-1
    count=count+1


# A part 

TrumpSpeech=inaugural.raw(speech[0])
Obama1Speech=inaugural.raw(speech[1])
Obama2Speech=inaugural.raw(speech[2])
Bush1Speech=inaugural.raw(speech[3])
Bush2Speech=inaugural.raw(speech[4])

# part B

TrumpSpeechSentence=nltk.sent_tokenize(TrumpSpeech)
Obama1SpeechSentence=nltk.sent_tokenize(Obama1Speech)
Obama2SpeechSentence=nltk.sent_tokenize(Obama2Speech)
Bush1SpeechSentence=nltk.sent_tokenize(Bush1Speech)
Bush2SpeechSentence=nltk.sent_tokenize(Bush2Speech)

#Part C

'''
    TrumpSpeechWord=[]
    for i in TrumpSpeechSentence:
        temp=nltk.word_tokenize(i)
        for j in temp:
            TrumpSpeechWord.append(j)

    print(TrumpSpeechWord)
'''

TrumpSpeechWord=nltk.word_tokenize(TrumpSpeech)
Obama1SpeechWord=nltk.word_tokenize(Obama1Speech)
Obama2SpeechWord=nltk.word_tokenize(Obama2Speech)
Bush1SpeechWord=nltk.word_tokenize(Bush1Speech)
Bush2SpeechWord=nltk.word_tokenize(Bush2Speech)

#part D

def removeInflexitions(tokens):
    res=""
    stp=list(set(stopwords.words('english')))
    for i in tokens:
        if i in stp:
            tokens.remove(i)
    ps=PorterStemmer()
    l=[]
    for i in tokens:
        l.append(ps.stem(i))
    return l

TrumpSpeechSentenceNew=removeInflexitions(TrumpSpeechSentence)
Obama1SpeechWordNew=removeInflexitions(Obama1SpeechWord)
Obama2SpeechWordNew=removeInflexitions(Obama2SpeechWord)
Bush1SpeechWordNew=removeInflexitions(Bush1SpeechWord)
Bush2SpeechWordNew=removeInflexitions(Bush2SpeechWord)
