import os
import json
import psycopg2
import psycopg2.extras
import time
from collections import defaultdict

import sys
import csv

# >>> f=open('articles.json','r')
# >>> j=json.load(f)
# >>> j[0]
# {'pageCount': 6, 'name': 'A. Aldo Faisal', 'startPage': 3295, 'institution': 'Imperial College London', 'area': 'icra', 'year': 2016, 'title': '3D gaze cursor: Continuous calibration and end-point grasp control of robotic actuators.', 'conf': 'ICRA'}
# >>> len(j)
# 113168
# >>> j[0]["name"]
# 'A. Aldo Faisal'
# >>> j[0]["year"]
# 2016
f=open('articles.json','r')
j=json.load(f)
def_name="name text, year text, title text, conf text, area text, institution text, startpage text, pagecount text"
batchsize=10
conn_string="dbname='dblp' user='meng'"
conn=psycopg2.connect(conn_string)
cur1=conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
cur1.itersize=batchsize
cur1.execute('DROP TABLE IF EXISTS articles;')
cur1.execute('CREATE TABLE articles ({0});'.format(def_name))

for record in j:
    cur1.execute("""
     INSERT INTO articles VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
     """,
     (record["name"],
     record["year"],
     record["title"],
     record["conf"],
     record["area"],
     record["institution"],
     record["startPage"],
     record["pageCount"]))

f.close()
conn.commit()
cur1.close()
