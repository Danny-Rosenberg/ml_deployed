#a script to insert question pairs in the sqlite database

import sqlite3
import sys
import random
##using a Go struct in python????

conn = sqlite3.connect('central.db')

q1 = sys.argv[1]
q2 = sys.argv[2]
is_duplicate = sys.argv[3]

qid1 = random.randint(1, 100000)
qid2 = random.randint(1, 100000)


#need to add the numbered id row explicitly?
cursor = conn.execute('''INSERT INTO train(qid1, qid2, question1, question2, is_duplicate) VALUES(?,?,?,?,?)''', (qid1, qid2, q1, q2, is_duplicate))
print("row of questions inserted")

#or could maintain the id system
#would have to do some hashing to maintain identities of IDs


id = cursor.lastrowid
print('last row id %d' % id)

conn.commit()

conn.close()
