#TASK: To transform raw Pub and Field to some tables that are useful
#First try to test on miniset-> miniPub and miniField, which are 1% */
#We should have a big table at all with foreign key 'pub-info', and many small table for fast query (this should be in small subsubarea domain)

import os
import json
import psycopg2
import psycopg2.extras
import time
from collections import defaultdict

import sys
import csv
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True
# table_source="Field"
# batchsize=10
# testsize=100000
#
# print("Start transform...")
# t1=time.time()
# conn_string="dbname='dblp' user='meng'"
# conn=psycopg2.connect(conn_string)
# cur1=conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
# cur1.itersize=batchsize
# cur1.execute('DROP TABLE IF EXISTS PubSchema;')
# # for loop drop from json
# with open('publist.json','r') as f:
# 	data=json.load(f)
#
# # for area in data["areas"]:
# # 	for subarea in area["subareas"]:
# # 		for conf in subarea["confs"]:
# # 			cur1.execute('DROP TABLE IF EXISTS '+'\"'+conf["name"]+'\"'+';')
# 			#cur.execute('CREATE TABLE '+'\"'+conf["name"]+'\"'+';')
#
# # define what to grasp and change to what
order=["key","title","author","conf","journal","year","url"]
tran={
"key":"key",
"title":"title",
"author":"author",
"booktitle":"conf",
"journal":"journal",
"year":"year",
"url":"url"
}
#
# # define new table
# def_name=", ".join(["{0} text".format(x) for x in tran.values()])
# type_name=", ".join(["{0}".format(x) for x in tran.values()])
# spac_name=",".join(["%s" for x in tran.keys()])
# cur1.execute('CREATE TABLE PubSchema ({0});'.format(def_name))
# cur1.close()
#
# # define state variables
index=0
upd=defaultdict(str)
# # iter through
# cur2=conn.cursor('cursor_2',cursor_factory=psycopg2.extras.NamedTupleCursor)
# cur2.itersize=batchsize
# cur2.execute('SELECT * FROM '+table_source+';')
# #res=cur2.fetchmany(batchsize)
# #while len(res)!=0:
# 	#for record in res:
# 		#index=(int)(record["i"])
# for record in cur2:
# 	if record.i=="0":
# 		if upd["author"]!="":
# 			#type_name=", ".join(["{0}".format(x) for x in upd.keys()])
# 			#val_name=", ".join(["\'{0}\'".format(x) for x in upd.values()])
# 			val_name=tuple([upd[tran[y]] for y in tran.keys()])
# 			#print(type_name, val_name)
# 			#SQL="INSERT INTO PubSchema ({0}) VALUES (%s);".format(type_name)
# 			#print("SQL=",SQL)
# 			#data=("{0}".format(val_name),)
# 			SQL="INSERT INTO PubSchema ({0}) VALUES ({1});".format(type_name,spac_name)
# 			# print(SQL)
# 			# print(val_name)
# 			#cur1=conn.cursor('cursor_1',cursor_factory=psycopg2.extras.NamedTupleCursor)
# 			#cur1.itersize=batchsize
# 			#cur1.execute(SQL,val_name)
# 		upd=defaultdict(str)
# 		upd["author"]=record.v
# 		upd["key"]=record.k
# 	else:
# 		if record.p=="author":
# 			upd["author"]+=","+record.v
# 		elif record.p in tran.keys():
# 			upd[tran[record.p]]=record.v
# #	res=cur2.fetchmany(batchsize)
#
# if upd["author"]!="":
# 	#type_name=", ".join(["{0}".format(x) for x in upd.keys()])
# 	#val_name=", ".join(["\'{0}\'".format(x) for x in upd.values()])
# 	val_name=tuple([upd[tran[y]] for y in tran.keys()])
# 	#print(type_name, val_name)
# 	#SQL="INSERT INTO PubSchema ({0}) VALUES (%s);".format(type_name)
# 	#print("SQL=",SQL)
# 	#data=("{0}".format(val_name),)
# 	SQL="INSERT INTO PubSchema ({0}) VALUES ({1});".format(type_name,spac_name)
# 	# print(SQL)
# 	# print(val_name)
# 	#cur1=conn.cursor('cursor_1',cursor_factory=psycopg2.extras.NamedTupleCursor)
# 	#cur1.itersize=batchsize
# 	#cur1.execute(SQL,val_name)
# #readCSV= csv.reader('fieldFile.txt',delimiter='\t')
#
# t2=time.time()
# print("Finished with",t2-t1,"s")
# conn.commit()
#
# conn.close()
t3=time.time()
f1=open("fieldFile.txt","r")#("simerr.txt","r")#
reader=csv.DictReader(f1,delimiter='\t',quotechar=None ,quoting=csv.QUOTE_NONE,fieldnames=["k","i","p","v"])
f2=open("pubSchema-new.csv","w")
writer = csv.writer(f2, delimiter='\t', quotechar='@', lineterminator="\n")
cnt=0
for record in reader:
	#print(record)
	# cnt+=1
	# if cnt>5000000:
	# 	break
	if record["i"]=="0":
		if upd["author"]!="":
			#type_name=", ".join(["{0}".format(x) for x in upd.keys()])
			#val_name=", ".join(["\'{0}\'".format(x) for x in upd.values()])
			val_name=[upd[y] for y in order]
			#print(type_name, val_name)
			#SQL="INSERT INTO PubSchema ({0}) VALUES (%s);".format(type_name)
			#print("SQL=",SQL)
			#data=("{0}".format(val_name),)
			#SQL="INSERT INTO PubSchema ({0}) VALUES ({1});".format(type_name,spac_name)
			# print(SQL)
			# print(val_name)
			#cur1=conn.cursor('cursor_1',cursor_factory=psycopg2.extras.NamedTupleCursor)
			#cur1.itersize=batchsize
			#cur1.execute(SQL,val_name)
			writer.writerow(val_name)
		upd=defaultdict(str)
		upd["author"]=record["v"]
		upd["key"]=record["k"]
	else:
		if record["p"]=="author":
			upd["author"]+=","+record["v"]
		elif record["p"]=="url":
			if upd["url"]=="":
				upd["url"]=record["v"]
			else:
				upd["url"]+=","+record["v"]
		elif record["p"] in tran.keys():
			upd[tran[record["p"]]]=record["v"]
if upd["author"]!="":
	val_name=[upd[y] for y in order]
	writer.writerow(val_name)

f1.close()
f2.close()
t4=time.time()
print("Finished",t4-t3,"s")
