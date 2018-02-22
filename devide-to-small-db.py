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
t1=time.time()
f=open('publist.json','r')
j=json.load(f)

"""
>>> j["areas"][0]["subareas"][0]["confs"][0]["keywords"]
['AAAI']
"""

conf_list=[]

for area in j["areas"]:
    for subarea in area["subareas"]:
        for conf in subarea["confs"]:
            conf_list.append(conf["keywords"])

#print(conf_list)
# conf_list=[["AAAI"]]
# conf_list.append(['CVPR', 'CVPR (1)', 'CVPR (2)'])
# conf_list.append(['IEEE_SAP', 'IEEE Symposium on Security and Privacy','USENIX Security Symposium'])
# conf_list+=[['NDSS'], ['SIGMOD', 'SIGMOD Conference'], ['VLDB']]
# conf_list+=[["SIGGRAPH_Asia"]]
print(conf_list)
#


# def_name="name text, year text, title text, conf text, area text, institution text, startpage text, pagecount text"
# batchsize=10
conn_string="dbname='dblp' user='meng'"
conn=psycopg2.connect(conn_string)
cur1=conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
# cur1.itersize=batchsize
count=0
for keywords in conf_list:
    print(keywords)
    cur1.execute('DROP TABLE IF EXISTS '+keywords[0]+';')

    # create table new_table
    # as
    # select t1.col1, t2.col2
    # from some_table t1
    # join t2 on t1.id = t2.some_id;

    sth=",".join(["\'"+word+"\'" for word in keywords])
    # cur1.execute('SELECT COUNT(*) from pubSchema '+
    # ' WHERE \"booktitle\" IN ('+ sth +');')
    if "SIGGRAPH_Asia" in keywords:
        cur1.execute('CREATE TABLE '+keywords[0]+
        ' AS SELECT * from pubSchema '+
        ' WHERE UPPER(\"booktitle\") like \'%SIGGRAPH ASIA%\';')
    else:
        cur1.execute('CREATE TABLE '+keywords[0]+
        ' AS SELECT * from pubSchema '+
        ' WHERE \"booktitle\" IN ('+ sth +');')
    cur1.execute('SELECT COUNT(*) FROM '+keywords[0]+';')
    s=cur1.fetchall()
    count+=s[0].count
    print(str(s)+"\r\n")
    print("sum",count)
# cur1.execute('CREATE TABLE articles ({0});'.format(def_name))
#
# for record in j:
#     cur1.execute("""
#      INSERT INTO articles VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
#      """,
#      (record["name"],
#      record["year"],
#      record["title"],
#      record["conf"],
#      record["area"],
#      record["institution"],
#      record["startPage"],
#      record["pageCount"]))
#
# f.close()
conn.commit()
# cur1.close()
t2=time.time()
print("finished",t2-t1,"s")
