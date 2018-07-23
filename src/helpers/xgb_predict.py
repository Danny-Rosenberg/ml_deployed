#need to create an DMatrix: x_test = xgb.DMatrix(x_test) 
#-xtest can be loaded from a file: dtest = xgb.DMatrix('demo/data/agaricus.txt.test'
#-or from a pandas matrix (probably numpy also):
#should this be a daemon? Probably better than reloading everytime. 

import numpy as np
import xgboost as xgb
import pickle
#the feature modules we'll need to build the DMatrix
import sys
sys.path.insert(0, "../ngrams_wordnet")
import feature_length as fl
import feature_synset as fs
import feature_ngrams as fn


questions = np.array(sys.argv[1:3])
print(questions)


length = fl.length_feature(questions[0], questions[1])
ngrams = fn.ngram(questions[0], questions[1], 1)
synset = fs.syns_feature(questions[0], questions[1])

data = np.array([length, ngrams, synset])

loaded_model = pickle.load(open("../ngrams_wordnet/ngrams.pickle.dat", "rb"))

#is this correct?
data = data.reshape(1,-1)
#loading q1 and q2 into numpy array
print(data.shape)

data = xgb.DMatrix(data)
prediction = loaded_model.predict(data)
print("prediction is: ", prediction)
