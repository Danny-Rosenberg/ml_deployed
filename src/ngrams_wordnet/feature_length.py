

def length_feature(sent1, sent2):
  '''takes two sentences, returns average length'''
  sent1 = str(sent1) if type(sent1) != 'str' else sent1
  sent2 = str(sent2) if type(sent2) != 'str' else sent2

  return (len(sent1) + len(sent2)) / 2
