import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask import json,jsonify
import psycopg2
import psycopg2.extras
#from flask_sqlalchemy import SQLAlchemy
from alpharank.model import Queries, HierQuery, RangeQuery, SelectQuery, University, Faculty
import random
choose_vue=True
import requests # to enable backend API provides
from flask_cors import CORS
import csv
import sys
from sys import getsizeof
from collections import defaultdict
import jsonpickle


# TO avoid {{}} conflict with Vue
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))


app = CustomFlask(__name__,
static_folder='../../dist/static',
template_folder='../../dist') # To use frontend built files



# use this only when need external visit from frontend
cors=CORS(app, resources={r"/api/*":{"origins":"*"}})

conn=psycopg2.connect(dbname="dblp",user="meng")

app.config["DEBUG"]=True
app.config['SECRET_KEY']="hehe"

UniversityDict={}
FacultyDict={}
NameToScholarId={}

#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/dblp'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#db=SQLAlchemy(app)

queries=Queries()
def init_model():
    area=HierQuery()
    area.childrens=[]
    area.genre="Artificial Intelligence"
    sub_area_1=HierQuery()
    sub_area_1.genre="Computer Vision"
    sub_area_2=HierQuery()
    sub_area_2.genre="Natural Language Processing"
    sub_area_3=HierQuery()
    sub_area_3.genre="Recommendation Algorithm"
    sub_area_4=HierQuery()
    sub_area_4.genre="Robotics"
    area.include(sub_area_1)
    area.include(sub_area_2)
    area.include(sub_area_3)
    area.include(sub_area_4)

    rang = RangeQuery()
    rang.genre="Time"
    rang.left_val=1995
    rang.right_val=2018

    sele = SelectQuery()
    sele.genre="Region"
    sele.val="America"

    queries.include(area)
    queries.include(sele)
    queries.include(rang)


"""
app.config.update(dict(
    DATABASE="dblp",
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
    ))
app.config.from_envvar('ALPHARANK_SETTINGS',silent=True)
"""

"""
def connect_db():
    rv=psy.connect(host="localhost",
            port="5432",
            dbname=app.config['DATABASE'],
            user="meng")
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db=connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db=get_db()
    with app.open_resource('schema.sql',mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Initialized the database")

@app.route('/')
def show_entries():
    db=get_db()
    cur=db.execute('select title, text from entries order by id desc')
    entries=cur.fetchall()
    return render_template('show_entries.html',entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db=get_db()
    db.execute('insert into entries (title, text) values (?,?)',[request.form['title'],request.form['text']])
    db.commit()
    flash("New entry was successfully posted")
    return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method=="POST":
        if request.form["username"]!=app.config["USERNAME"]:
            error='Invalid username'
        elif request.form['password']!=app.config["PASSWORD"]:
            error="Invalid password"
        else:
            session["logged_in"]=True
            flash("You were logged in")
            return redirect(url_for("show_entries"))
    return render_template("login.html",error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash("You were logged out")
    return redirect(url_for("show_entries"))
"""

@app.route('/')
def index():
    loadFromCSRanking()
    return render_template("index.html")

'''
@app.route('api/sth')
def related_sth():
    params=request.args["params"]

    do-sth....

    response={
        'data':data
    }
    return jsonify(response)
'''

@app.route('/api/random')
def random_number():
    response={
        'randomNumber': random.randint(1,100)
    }
    return jsonify(response)

@app.route('/api/subset')
def subset():
    setlen=request.args["setlen"]

    cur=conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute("SELECT * FROM pubSchema limit "+str(setlen)+" ;")
    res=cur.fetchall()
    cur.close()
    response={
        'subSet':res
    }
    return jsonify(response)

@app.route('/api/confcount/')
def confcount():
    conf=request.args["data"]

    cur=conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    print("SELECT * FROM pubSchema where booktitle=\'"+conf+"\' limit 10;")
    cur.execute("SELECT * FROM pubSchema where booktitle=\'"+conf+"\' limit 10;")
    res=cur.fetchall()
    cur.close()
    response={
        'subSet':res
    }
    return jsonify(response)

@app.route('/api/naivemetrics/')
def naivemetrics():
    sub_area_str=request.args["data"]
    range_str=request.args["range"]
    region_str=request.args["region"]
    search_str=request.args["searched"]
    res=naiveHandler(sub_area_str,range_str,region_str,search_str)
    response={
        'subSet':res
    }
    return jsonify(response)

def naiveHandler(sub_area_str,range_str,region_str, search_str):
    region="".join(region_str.lower().split(" "))
    print(region)
    loadFromCSRanking(region)
    result=[]
    sub_area_list=json.loads(sub_area_str)
    range_list=json.loads(range_str)
    search_str=search_str.strip().lower()
    # print("region=="+region_str)

    cur=conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    M=len(sub_area_list)

    for university in UniversityDict.values():
        university.allocate(M)

    for i,subArea in enumerate(sub_area_list):
        for conf in subArea:
            searchSQL=""
            if len(search_str)!=0:
                searchSQL="AND LOWER(\"title\") like \'%{0}%\'".format(search_str)
            SQL="SELECT * FROM {0} WHERE CAST(\"year\" AS INTEGER)>={1} AND CAST(\"year\" AS INTEGER)<={2} {3} ;".format(conf,range_list[0],range_list[1],searchSQL)
            cur.execute(SQL)
            res=cur.fetchall()

            for record in res:
                # print(record.author)
                author_list=record.author.split(",")
                N=len(author_list)
                credit=1.0/N
                #when receive credit ,first update faculty, then update university
                for author in author_list:
                    if author in NameToScholarId:
                        faculty=FacultyDict[NameToScholarId[author]]
                        university=UniversityDict[faculty.affiliation]

                        faculty.updateP()
                        faculty.updateC(credit)
                        university.updateG(credit,i)

    for university in UniversityDict.values():
        university.calF()
        university.calG()

    # print(UniversityDict)
    result=sorted(UniversityDict.values(),key=lambda x: x.g, reverse=True)
    for x in result:
        x.sort()

    return [x.dump() for x in result if x.valid()]

    #print(result[:3])
    #return json_str #([[str(x),[]] for x in result])

def loadFromCSRanking(region):
    global UniversityDict
    global FacultyDict
    global NameToScholarId
    UniversityDict={}
    FacultyDict={}
    NameToScholarId={}
    cntDict=defaultdict(int)
    cnt=0
    with open('../country-info.csv','r') as F:
        #TODO This should somehow move to initial part cause it won't change
        judger=csv.DictReader(F)
        schoolSet=set()
        if region!= "world":
            for rec in judger:
                if region=="theusa":
                    schoolSet.add(rec["institution"])
                elif rec["region"]==region:
                        schoolSet.add(rec["institution"])

        with open('../faculty.txt','r') as f:
            reader=csv.DictReader(f)#,delimiter='\,')
            for rec in reader:
                school = rec["affiliation"]
                if region=="theusa":
                    if school in schoolSet:
                        continue
                elif region!="world" and school not in schoolSet:
                    continue
                shnid=genShnid(rec["scholarid"],rec["homepage"])
                NameToScholarId[rec["name"]]=shnid
                if rec["affiliation"] not in UniversityDict:
                    university = University()
                    university.name=rec["affiliation"]
                    UniversityDict[rec["affiliation"]]=university
                else:
                    university=UniversityDict[rec["affiliation"]]
                if shnid not in FacultyDict:
                    faculty = Faculty()
                    faculty.scholarid = rec["scholarid"]
                    faculty.name.append(rec["name"])
                    faculty.affiliation=rec["affiliation"]
                    faculty.homepage=rec["homepage"]
                    FacultyDict[shnid]=faculty
                    university.faculties.append(faculty)
                else:
                    faculty=FacultyDict[shnid]
                    isSame=False
                    cnt+=1
                    for name in faculty.name:
                        if areTwoNameSame(name,rec["name"],faculty.homepage) or areTwoNameSame(rec["name"],name,faculty.homepage):
                            #print("\t",cnt,rec["name"],"~",name)
                            isSame=True
                            faculty.name.append(rec["name"])
                            break

                    if isSame==False:
                        #print(faculty.homepage)
                        #print("\t",cnt,rec["name"],"DIFF!!!","not ", ",".join(faculty.name))
                        newFaculty=Faculty()
                        newFaculty.scholarid = rec["scholarid"]
                        newFaculty.name.append(rec["name"])
                        newFaculty.affiliation=rec["affiliation"]
                        newFaculty.homepage=rec["homepage"]
                        cntDict[shnid]+=1
                        new_shnid=genShnid(rec["scholarid"],rec["homepage"],cntDict[shnid])
                        NameToScholarId[rec["name"]]=new_shnid
                        FacultyDict[new_shnid]=newFaculty
                        university.faculties.append(newFaculty)

def genShnid(scholarId, homepage, confusedId=0):
    return scholarId+"|"+homepage+"|"+str(confusedId)

def areTwoNameSame(x,y,homepage):
    xs=x.split(" ")
    ys=y.split(" ")

    "If already confused ided... like Zhang San 0001"
    if (xs[-1].isdigit() or ys[-1].isdigit()) and xs[-1]!=ys[-1]:
        return False

    if xs[-1].isdigit() and ys[-1].isdigit() and xs[-1]==ys[-1] and (xs[0] in ys[0] or xs[-2] in ys[-2]):
        return True

    "Omit mid-name"
    if (len(xs)>1 and xs[0]==ys[0] and xs[-1]==ys[-1]):
        return True

    """A. Blabla ~ Apple Blabla or Alex Blabla ~ Alexander Blabla"""
    if (xs[-1]==ys[-1] and xs[0][0]==ys[0][0] and len(xs[0])>1 and (xs[0][1]=="." or xs[0] in ys[0])):
        return True

    """Allison B. Lewko ~ Allison Bishop"""
    if (xs[0]==ys[0] and xs[1][0]==ys[1][0] and len(xs[1])>1 and xs[1][1]=="."):
        return True

    if (xs[0]==ys[0] and xs[1] in ys[1]):
        return True

    if (len(xs)>1 and len(ys)>1 and xs[0]==ys[0] and xs[1]==ys[1]):
        return True

    if (xs[-1]==ys[0]):
        return True

    if (xs[-1]==ys[-1] and len(xs[0])>2 and len(ys[0])>2 and xs[0][0:3]==ys[0][0:3]):
        return True

    """RISKY~"""
    for item in xs:
        if len(item) > 4:
            if item in ys:
                return True

            """Foreign word similarity eg: Öznur Özkasap ~  Oznur Ozkasap"""
            for yss in ys:
                if theyAreVerySimilar(item, yss):
                    return True

    """set like x y z ~ x y"""
    if set(xs) == (set(xs) or set(ys)):
       return True

    return False

def theyAreVerySimilar(x,y):
    if len(x)!=len(y):
        return False

    threshold=0.7
    crt=0
    for i,j in zip(x,y):
        crt+=int(i==j)
    return 1.0*crt/len(x)>threshold


@app.route('/',defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    #if app.debug:
        #return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")



"""
@app.route('/')
def index():
    init_model()
    session["logged_in"]=True
    print(len(queries.HierQueries))
    for que in queries.HierQueries:
        print(que)
    return render_template('layout.html', queries=queries)

@app.route('/show')
def show_items():
    cur=conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute("SELECT * FROM Field limit 50;")
    res=cur.fetchall()
    return render_template('show_entries.html',entries=res)

if __name__== '__main__':
    app.debug=True
    app.run(host="0.0.0.0")
"""
