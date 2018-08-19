#need to create an DMatrix: x_test = xgb.DMatrix(x_test) 
#-xtest can be loaded from a file: dtest = xgb.DMatrix('demo/data/agaricus.txt.test'
#-or from a pandas matrix (probably numpy also):
#should this be a daemon? Probably better than reloading everytime. 


#TODO: change this to one or two methods, pass params as a dict

import numpy as np
import xgboost as xgb
import pickle
#the feature modules we'll need to build the DMatrix
import sys

def predict(x_test):
	'''
	expects an (x, 3) np matrix
	returns a float prediction
	'''
	
	loaded_model = pickle.load(open("../ngrams_wordnet/ngrams.pickle.dat", "rb"))

	data = xgb.DMatrix(x_test)
	prediction = loaded_model.predict(data)
	print("prediction is: ", prediction)
	return prediction
