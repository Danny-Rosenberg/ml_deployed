#a script to insert question pairs in the sqlite database
#!/usr/local/bin/python


import sqlite3
import sys
import random

conn = sqlite3.connect('central.db')

q1 = sys.argv[1]
q2 = sys.argv[2]
is_duplicate = sys.argv[3]

qid1 = random.randint(1, 100000)
qid2 = random.randint(1, 100000)

row = 100000

print("inside insert")
print(q1)
print(q2)
print(is_duplicate)

#need to add the numbered id row explicitly?
cursor = conn.execute('''INSERT INTO train(id, qid1, qid2, question1, question2, is_duplicate) VALUES(?,?,?,?,?,?)''', (row, qid1, qid2, q1, q2, is_duplicate))
print("row of questions inserted")

#or could maintain the id system
#would have to do some hashing to maintain identities of IDs


idee = cursor.lastrowid
print('last row id %d' % idee)

f = open("checkFile.txt", "a+")
f.write("wrote a line: " + str(row) + str(qid1) + str(qid2) + q1 + q2 + str(is_duplicate) + "\n" )
f.close()

conn.commit()

conn.close()
