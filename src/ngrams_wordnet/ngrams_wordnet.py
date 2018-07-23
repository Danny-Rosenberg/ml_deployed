'''This file is an end to end model for ngrams and synsets. Users provide a training and a validation file, and this file will output predictions on the validation file'''
from sklearn.preprocessing import scale
import pandas as pd
import numpy as np
import argparse
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import xgboost as xgb
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.corpus import wordnet as wn
import pickle


stops = set(stopwords.words('english'))

#When removing stopwords, this prevents question words from being removed
#stops.remove("who")
#stops.remove("what")
#stops.remove("where")
#stops.remove("why")
#stops.remove("how")
#stops.remove("when")

tokenizer = RegexpTokenizer(r'\w+')
parser = argparse.ArgumentParser()

parser.add_argument('--trainfile', type=str, required=True)
parser.add_argument('--valfile', type=str, required=True)

def parse_files(train, val):
  '''read the files and create data frames'''
  train = pd.read_csv(train).as_matrix()
  val = pd.read_csv(val).as_matrix()
  print(type(val))
  print(type(train))
  print(train.shape)
  print(val.shape)

  x_train = train[:, 3:5] #want columns 3,4
  y_train = train[:,5:] #want column 5
  x_val = val[:, 3:5]
  y_val = val[:, 5:]
  
  return x_train, y_train, x_val, y_val 


def ngram(sentences, n):
  '''takes two sentence strings, and n, and returns the #of ngrams they share in common'''

  sent1 = sentences[0]
  sent2 = sentences[1]
  
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


def get_wordnet_pos(tag):
  if tag.startswith('J'):
      return wn.ADJ
  elif tag.startswith('V'):
      return wn.VERB
  elif tag.startswith('N'):
      return wn.NOUN
  elif tag.startswith('R'):        
    return wn.ADV
  else:
    return ''


def syns_feature(sentences):
  '''adds the wordnet synonym feature'''
  sent1 = sentences[0]
  sent2 = sentences[1] 
   
  sent1 = str(sent1) if type(sent1) != 'str' else sent1
  sent2 = str(sent2) if type(sent2) != 'str' else sent2
 
  sent1_tok = tokenizer.tokenize(sent1)
  sent2_tok = tokenizer.tokenize(sent2)

  sent1 = []
  sent2 = []

  #removing stopwords
  for w in sent1_tok:
    if w.lower() not in stops:
      sent1.append(w)

  for w in sent2_tok:
    if w.lower() not in stops:
      sent2.append(w)

  sent1 = nltk.pos_tag(sent1)
  sent2 = nltk.pos_tag(sent2) 

  sent1_tags = [get_wordnet_pos(x[1]) for x in sent1]
  sent2_tags = [get_wordnet_pos(x[1]) for x in sent2] 
  
  count_syn = 0

  syns = defaultdict(set)

  #adding the original sentence
  for i in range(len(sent1)):
    syns[sent1_tags[i]].add(sent1[i][0].lower())
  
  for i in range(len(sent1)):
    synonyms = wn.synsets(sent1[i][0], sent1_tags[i])
    for syn in synonyms:
      w = syn.name().split('.')[0]
      [syns[sent1_tags[i]].add(w.lower()) for word in sent1] 
  
  for i in range(len(sent2)):
    count_syn += 1 if sent2[i][0] in syns[sent2_tags[i]] else 0

  return count_syn 
     

def add_syns_feature(x_train):
  '''adding a column of synonym counts, then scaling it'''

  new_col = np.apply_along_axis(syns_feature, 1, x_train)
  with open("scales_syn.txt", "a+") as s:
    me = str(np.mean(new_col))
    sd = str(np.std(new_col))
    st = "mean: " + me + ", standard deviation: " + sd
    s.write("\n" + st)

  new_col = scale(new_col, axis=0, with_mean=True, with_std=True, copy=True)
  x_train = np.column_stack((x_train, new_col.T)) 
  return x_train


def add_ngram_feature(x_train, n):
  '''adding a column of common ngrams, then scaling it'''
  
  new_col = np.apply_along_axis(ngram, 1, x_train, n)
  new_col = scale(new_col, axis=0, with_mean=True, with_std=True, copy=True)
  
  with open("scales_ngram.txt", "a+") as s:
    me = str(np.mean(new_col))
    sd = str(np.std(new_col))
    st = "mean: " + me + ", standard deviation: " + sd 
    s.write("\n" + st)
  
  print(x_train.shape)
  print(new_col.shape)
  x_train = np.column_stack((x_train, new_col.T)) 
  print(x_train.shape)
  return x_train


def length_feature(sentences):
  '''returns the average length of the two sentences'''

  sent1 = sentences[0]
  sent2 = sentences[1] 
  sent1 = str(sent1) if type(sent1) != 'str' else sent1
  sent2 = str(sent2) if type(sent2) != 'str' else sent2

  return (len(sent1) + len(sent2)) / 2


def add_length_feature(x_train):
  new_col = np.apply_along_axis(length_feature, 1, x_train)
  new_col = scale(new_col, axis=0, with_mean=True, with_std=True, copy=True)
    
  with open("len_scales.txt", "a+") as s:
    me = str(np.mean(new_col))
    sd = str(np.std(new_col))
    st = "mean: " + me + ", standard deviation: " + sd 
    s.write("\n" + st)
 
  print(x_train.shape)
  print(new_col.shape)
  x_train = np.column_stack((x_train, new_col.T))
  print(x_train.shape)
  return x_train
 

def output_pred(preds):
  '''expects an array of predictions, writes to a prediction file in submission format'''
  with open("output.txt", 'w') as out:
    for i in range(len(preds)):
      out.write('%s,%s\n'%(i, preds[i]))
  


def model(x_train, y_train, x_test, y_test):
  '''the contents of this function can be interchanged depending on model'''
  '''will return list of predictions'''
  
  #label = np.random.randint(2)
  x_train = xgb.DMatrix(x_train, label=y_train)
  
  #y_train = xgb.DMatrix(y_train)
  #in this context, as the validation set, I assume the 'label' part of the matrix is only being used
  #for computing the final outcome statistics
  x_test = xgb.DMatrix(x_test, label=y_test)
    

  params = {}
  params['objective'] = 'binary:logistic'
  params['eval_metric'] = 'logloss'
  params['eta'] = .02
  params['max_depth'] = 2 

  watchlist = [(x_train, 'train'), (x_test, 'valid')]
  model = xgb.train(params, x_train, 400, watchlist, early_stopping_rounds=50)
  
  #addition for mlapp
  #model.dump_model('ngrams_raw.txt')
  #model.save_model('ngrams.model')

  pickle.dump(model, open("ngrams.pickle.dat", "wb"))
  
  pred = model.predict(x_test, ntree_limit=model.best_ntree_limit)
  return pred


def main():
  args = parser.parse_args()
  print("starting the program")
  x_train, y_train, x_val, y_val = parse_files(args.trainfile, args.valfile)
 
  x_train = add_ngram_feature(x_train, 1)
  x_val = add_ngram_feature(x_val, 1)

  x_train = add_length_feature(x_train)
  x_val = add_length_feature(x_val)

  x_train = add_syns_feature(x_train)
  x_val = add_syns_feature(x_val)

  #with open("gold_val", 'w') as val: 
  #  for i in range(len(x_val)):
  #   ######################
  #    val.write('%s,%s\n'%(i, x_val[i][2]))

  pred = model(x_train[:,2:], y_train, x_val[:,2:], y_val)
  output_pred(pred)
  

if __name__ == '__main__':
  main() 
