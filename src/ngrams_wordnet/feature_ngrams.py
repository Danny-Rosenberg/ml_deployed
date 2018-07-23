from sklearn.preprocessing import scale
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.corpus import wordnet as wn


stops = set(stopwords.words('english'))

tokenizer = RegexpTokenizer(r'\w+')

def ngram(sent1, sent2, n):
  '''takes two sentence strings, and n, and returns the #of ngrams they share in common'''
  '''how to scale this number?'''
  
  sent1 = str(sent1) if type(sent1) != 'str' else sent1
  sent2 = str(sent2) if type(sent2) != 'str' else sent2
   
  ngrams = []
  num_common_ngrams = 0
  
  long_sent = sent1 if len(sent1) > len(sent2) else sent2
  short_sent = sent1 if long_sent == sent2 else sent2
  
  long_sent_tok = tokenizer.tokenize(long_sent)
  short_sent_tok = tokenizer.tokenize(short_sent)

  long_sent = []
  short_sent = []


  #removing stopwords
  for w in long_sent_tok:
    if w not in stops:
      long_sent.append(w)

  for w in short_sent_tok:
    if w not in stops:
      short_sent.append(w)


  for i in range(n-1, len(long_sent)):
    ngrams.append(long_sent[i-n+1:i+1])


  for i in range(n-1, len(short_sent)):
    if short_sent[i-n+1:i+1] in ngrams:
      num_common_ngrams +=1

  return num_common_ngrams
