This extension combines two features of similarity, ngram and wordnet synonyms, and uses XGBoost as the model. To see features in isolation, 
you can comment out any of the 'add_ex_feature()' methods within main(). 

Sample input:
python ngrams_wordnet.py train.csv --trainfile val.csv --valfile
This will output a file called 'output.txt' with predictions in the desired format for score.py. 
