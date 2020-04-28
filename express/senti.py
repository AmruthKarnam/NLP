from textblob import TextBlob
import csv
import sys
import statistics 
import re
import operator
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import operator
from sklearn.metrics import f1_score,accuracy_score,confusion_matrix,recall_score,precision_score
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords 
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from spellchecker import SpellChecker


def tweetAsAnInput(sentence):
                    tweet= {}
                    tweet['orig'] = sentence
                    if re.match(r'^RT.*', tweet['orig']):
                        return "Not a proper Tweet"
                    tweet['clean'] = tweet['orig']

                    #tweet['clean'] = strip_non_ascii(tweet['clean'])

                    tweet['clean'] = tweet['clean'].lower()
                    
                    #tweet['clean'] = lemmatize(tweet['clean'])
                    
                    #tweet['clean'] = removeStopWords(tweet['clean'])
                    tweet['clean'] = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet['clean'])

                    tweet['clean'] = re.sub(r'\bthats\b', 'that is', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bive\b', 'i have', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bim\b', 'i am', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bya\b', 'yeah', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bcant\b', 'can not', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bwont\b', 'will not', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bid\b', 'i would', tweet['clean'])
                    tweet['clean'] = re.sub(r'wtf', 'what the fuck', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bwth\b', 'what the hell', tweet['clean'])
                    tweet['clean'] = re.sub(r'\br\b', 'are', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bu\b', 'you', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bk\b', 'OK', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bsux\b', 'sucks', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bno+\b', 'no', tweet['clean'])
                    tweet['clean'] = re.sub(r'\bcoo+\b', 'cool', tweet['clean'])
                    
                    #tweet['clean'] = correctSpelling(tweet['clean'])
    
                    tweet['TextBlob'] = TextBlob(tweet['clean'])
                    tweet['polarity'] = float(tweet['TextBlob'].sentiment.polarity)
                    if tweet['polarity'] >= 0.1:
                        tweet['sentiment'] = 'positive'
                    elif tweet['polarity'] <= -0.1:
                        tweet['sentiment'] = 'negative'
                    else:
                        tweet['sentiment'] = 'neutral'
                    return tweet['sentiment']
                    
s=sys.argv[1:]
s=" ".join(s)
output= tweetAsAnInput(s)
print(output)
