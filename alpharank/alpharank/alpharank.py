import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import psycopg2
import psycopg2.extras
#from flask_sqlalchemy import SQLAlchemy
from alpharank.model import Queries, HierQuery, RangeQuery, SelectQuery

app = Flask(__name__)
conn=psycopg2.connect(dbname="dblp",user="meng")
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
