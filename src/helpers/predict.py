#need to create an DMatrix: x_test = xgb.DMatrix(x_test) 
#-xtest can be loaded from a file: dtest = xgb.DMatrix('demo/data/agaricus.txt.test'
#-or from a pandas matrix (probably numpy also):
#should this be a daemon? Probably better than reloading everytime. 

import numpy as np
import xgboost as xgb


loaded_model = pickle.load(open("../ngrams_wordnet/ngrams.pickle.dat", "wb"))

#loading q1 and q2 into numpy array
questions = np.array(sys.argv[1:3])

xgb.DMatrix(questions)

