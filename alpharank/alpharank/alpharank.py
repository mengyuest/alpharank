import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask import jsonify
import psycopg2
import psycopg2.extras
#from flask_sqlalchemy import SQLAlchemy
from alpharank.model import Queries, HierQuery, RangeQuery, SelectQuery
import random
choose_vue=True
import requests # to enable backend API provides
from flask_cors import CORS

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
