from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import helpers

def tokenize_sentences(sent1, sent2):
  '''uses the nltk tokenizer to split up all the words'''
  tokenizer = RegexpTokenizer(r'\w+')
     
  sent1 = str(sent1) if type(sent1) != 'str' else sent1
  sent2 = str(sent2) if type(sent2) != 'str' else sent2
 
  sent1_tok = tokenizer.tokenize(sent1)
  sent2_tok = tokenizer.tokenize(sent2)

  return sent1, sent2


def remove_stopwords(sent1, sent2):
  '''removes stopwords, returns two clean sentences'''
  stops = set(stopwords.words('english'))
 
  sent1 = []
  sent2 = []

  #removing stopwords
  for w in sent1_tok:
    if w.lower() not in stops:
      sent1.append(w)

  for w in sent2_tok:
    if w.lower() not in stops:
      sent2.append(w)

  return sent1, sent2


