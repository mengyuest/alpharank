apt-get update
apt-get install gunzip -y
wget http://dblp.uni-trier.de/xml/dblp.dtd
wget http://dblp.uni-trier.de/xml/dblp.xml.gz
gunzip dblp.xml.gz
python wrapper.py
python transform.py
psql -f createPubSchema.sql dblp
pip3 install -U pip3
pip3 install psycopg2
pip3 install Flask
pip3 install Flask-SQLAlchemy
