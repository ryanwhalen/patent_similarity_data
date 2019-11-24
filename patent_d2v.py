#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gensim
from gensim.models.doc2vec import TaggedDocument
import sqlite3 as sqlite
import multiprocessing
import re
import os
import timeit
import json


start = timeit.default_timer()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)



class DocIterator(object):
    """
    Streams corpus from patent sqlite database
    """
    def __init__(self, conn):
        self.conn = conn


    def __iter__(self):
        cur.execute('''SELECT patent_id, text FROM description''')
        count = 0
        for patent in cur:
            count += 1

            if count % 100000 == 0:
                print('Processing patent '+str(count))
                           
            number = patent[0]
            if number == None: #skip if no patent number
                continue
            desc = patent[1]
            if desc == None: #deal with older patents that cram everything into claims
                desc = ''
            if number.startswith('D'): #skip design patents
                continue
            

            claims = cur2.execute('''SELECT text FROM claim WHERE 
                                  patent_id = ? and dependent = -1''',
                                  [number]).fetchall()
            
            claims = [c[0] for c in claims if c[0] != None]
            claims = ' '.join(claims)
            desc = desc + claims


            desc = desc.replace('\n', ' ').strip()
            words = re.findall(r"[\w']+|[.,!?;]", desc)
            words = [word.lower() for word in words]
            if len(words) < 250:
                continue

            tags = [number]
            patents.add(number) #track patent numbers to get vectors

            yield TaggedDocument(words, tags)
            

def write_vectors():
    print('Writing vectors to DB')
    cur.execute('''DROP TABLE IF EXISTS doc2vec''')
    cur.execute('''CREATE TABLE doc2vec (patent_id TEXT, vector TEXT)''')
    conn.commit()
    
    skipped = 0
    #write JSON vectors
    for number in patents:
        try:
            vector = list(model.docvecs[number])
            vector = [float(v) for v in vector]
            cur.execute('''INSERT INTO doc2vec VALUES (?,?)''',[number, json.dumps(vector)])
        except:
            skipped += 1
    conn.commit()
    cur.execute('''CREATE INDEX vector_patent_id_index ON doc2vec (patent_id ASC)''')
    conn.commit()
    print(str(skipped)+' skipped')

                
if __name__ == '__main__':
    patents = set() 
    conn = sqlite.connect('patent_db.sqlite', check_same_thread=False)
    cur = conn.cursor()
    cur2 = conn.cursor()
    n_cpus = multiprocessing.cpu_count()
    
    doc_iterator = DocIterator(conn)
    model = gensim.models.Doc2Vec(
        documents=doc_iterator,
        workers=n_cpus,
        vector_size=300,
        epochs = 12
        )

    model.delete_temporary_training_data(keep_doctags_vectors = True, 
                                        keep_inference = True)
    model.save('patent_doc2v_12e.model')
    
    write_vectors()

    

stop = timeit.default_timer()
total_time = stop - start
mins, secs = divmod(total_time, 60)
hours, mins = divmod(mins, 60)

print("Total running time: %d:%d:%d. \n" % (hours, mins, secs))
