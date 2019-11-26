#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
writes exported similarity data to database
assumes you have downloaded the patentsview data
using script from https://github.com/ryanwhalen/patentsview_data_download
'''

import sqlite3
import csv
import json
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


conn = sqlite3.connect('patent_db_test.sqlite')
cur = conn.cursor()


def import_cite_sims():
    '''reads citation similarity into patent database'''
    print('Importing cite_sims.csv')
    cur.execute('''CREATE TABLE cite_similarity
    (patent_id text, citation_id text, similarity real)
    ''')
    
    infile = open('cite_sims.csv','r',encoding='utf-8')
    reader = csv.reader(infile)
    
    count = 0
    for row in reader:
        count += 1
        if count == 1: continue #skip header row
        cur.execute('''INSERT INTO cite_similarity VALUES (?,?,?)''',row)
    conn.commit()


def import_vectors():
    '''reads vectors.json into patent database'''
    print('Importing vectors.json')
    cur.execute('''CREATE TABLE doc2vec (patent_id text, vector text)
    ''')
    
    infile = open('vectors.json','r',encoding='utf-8')
    
    for vector in infile:
        vector = json.loads(vector)
        patent = vector[0]
        vector = vector[1]
        row = [json.dumps(patent), json.dumps(vector)]
        cur.execute('''INSERT INTO doc2vec VALUES (?,?)''',row)
    conn.commit()
    
      
def import_most_sim():
    '''reads most similar invention file into database'''
    print('Importing most_sim.json')
    infile = open('most_sim.json','r',encoding='utf-8')
    
    cur.execute('''CREATE TABLE most_similar (patent_id text, top_100 text)''')
    
    for sim in infile:
        sim = json.loads(sim)
        patent = sim[0]
        sims = sim[1]
        row = [json.dumps(patent), json.dumps(sims)]
        cur.execute('''INSERT INTO most_similar VALUES (?,?)''',row)
    conn.commit()
    
if __name__ == '__main__':
    import_cite_sims()
    import_vectors()
    import_most_sim()
    
conn.close()
