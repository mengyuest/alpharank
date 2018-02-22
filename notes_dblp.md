# Alpharank notes

## Feb 18

## Install PostgreSQL
> referenced from https://www.postgresql.org/download/linux/ubuntu/
1. Create a file at `/etc/apt/sources.list.d/pgdg.list` and add a line `deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main`
2. Import repo and update: `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - & sudo apt-get update `
3. Install: `sudo apt-get install postgresql-9.6`
4. Add user with superuser privilege: `sudo -u postgres psql` and then (in psql command) `CREATE USER meng WITH SUPERUSER;` then (logout by `\q` and ) type `exit` to back to normal user in terminal
5. Create a database `createdb dblp`
6. psql in certain database `psql -d dblp`

## Preprocess Data
> referenced from https://courses.cs.washington.edu/courses/cse544/15wi/hw/hw1/hw1.html
1. Download dataset(dblp.dtd, dblp.xml.gz) from [dblp website](http://dblp.uni-trier.de/xml/) and gunzip with it
2. Transfer to txt file(mind path and in python3, modify wrapper.py from starter code to no encoding... because str->str). Then `python wrapper.py` to get data(may take 10 mins or so)
3. Use sql file to dump data to database: `psql -f createRawSchema.sql dblp`
4. Check with command in psql: `select * from Pub limit 50`, `select * from Field limit 50;`
5. Data transformation: ...

## Build website
1. Since we use postgresql, we need to install psycopg2 and sqlalchemy for flask-postgresql utils (further see [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.3/quickstart/#a-minimal-application))
2. Actually, we can just use psycopg2...
3. Use `cur=conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)` can show query result in dictionary way (visited by col name)

## TODO
1. Still don't know whether we should ORM somehow... As here we don't allow users to modify our data in database(maybe we can add revision function some time...)
2. Need to build the front-end and leave todo-API for backend (basic layout and listview)
3. Need to reshape our database to some kind of better structured
4. Need to implement the database search function


## Feb 19

## Bear in mind
1. Don't debug on huge things. Try to build minimal-error-system to reproduce the error and find the error.

## Database
1. postgresql uses `;` at end. 
2. `select DISITINCT what from tablename;` to find different keys.
3. `select count(what) from tablename;` to find sum
4. `select what from tablename where "colname"='word'` to find exact match
5. `select what from tablename where "colname" like '%pattern%'` to find pattern match
6. Cursor can use multis
7. `fetchmany` to fetch several, `fetchone` is just one, `fetchall` is all
8. Cursor has client-side and server-side. Normally we use client-side and when do insert/alter/updates changes we actually take up in memory.

## CSV
1. Use csv.DictReader to show member in field as dict (but if don't have header, should use `fieldname` to explicit declare the headers)
2. If don't know what is for quotation, just use `quotechar=None` and `quoting=csv.QUOTE_NONE`
3. If you select quotation, and try to read sth in, then you shouldn't have those kind of quotation in your raw-text. Or else it is wrong!

## When stuck under Ubuntu
1. Press `ctrl+alt+F1` to enter tty-1 mode
2. Use `top` to find which goes wrong and its PID
3. Use `sudo kill [pid]` with its PID to stop it.
4. Back to desktop using `ctrl+alt+F7`

## When stuck in vim
1. You probably pressed `ctrl+s`(perhaps want to save sth), just use `ctrl+q` to release.

## TODO
1. Vue (Try to implement function and query display listviews)
2. Link with faculty/institution
3. Deployment on webserver
3. Updates in Google form