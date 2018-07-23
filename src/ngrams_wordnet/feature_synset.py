from nltk.corpus import wordnet as wn
from collections import defaultdict
from nltk import pos_tag

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


def syns_feature(sent1, sent2):
  sent1 = pos_tag(sent1)
  sent2 = pos_tag(sent2) 

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
