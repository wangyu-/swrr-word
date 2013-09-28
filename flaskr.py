# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for,abort, render_template, flash
from BeautifulSoup import BeautifulSoup
#from flask.ext.admin import Admin, BaseView, expose

# configuration
DATABASE = '/Users/wangyu/wyflask/flaskr.db'
EN_DB = '/Users/wangyu/wyflask/english.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
#app.config['DATABASE']='/tmp/flaskr.db'
app.config.from_object(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#app.config.from_envvar('FLASKR_SETTINGS')

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])
def connect_en_db():
	return sqlite3.connect(app.config['EN_DB'])

from contextlib import closing

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


@app.before_request
def before_request():
	g.db = connect_db()
	g.en_db=connect_en_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    en_db=getattr(g,'en_db',None)
    if en_db is not None:
	en_db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/en_db/<word>')
def en_db(word):
    cur = g.en_db.execute(word)
    tmp=[row for row in cur.fetchall()]
    return render_template('db.html', item_list=tmp)

@app.route('/xml_dict/')
def xml_dict():
    cur = g.en_db.execute('select word from xml order by word')
    word_list = [row[0] for row in cur.fetchall()]
    return render_template('collins_dict.html', word_list=word_list)

@app.route('/xml_dict/<word>')
def show_xml_word(word):
	cur=g.en_db.execute('select value from xml where word =?',(word,))
	value=[row[0] for row in cur.fetchall()][0]
	return value

@app.route('/collins_dict/')
def collins_dict():
    cur = g.en_db.execute('select word from collins order by word')
    word_list = [row[0] for row in cur.fetchall()]
    return render_template('collins_dict.html', word_list=word_list)

@app.route('/collins_dict/<word>')
def show_user_profile(word):
	cur=g.en_db.execute('select value from collins where word =?',(word,))
	value=[row[0] for row in cur.fetchall()][0]
	return value

@app.route('/paser_dict/<word>')
def paser_dict(word):
	cur=g.en_db.execute('select value from collins where word =?',(word,))
	value=[row[0] for row in cur.fetchall()][0]
	soup = BeautifulSoup(''.join(value))
	aaa=str(soup.find("div",attrs={"class":"collins_content"}))
#str=soup.prettify()
	return aaa

@app.route('/paser_dict2/<word>')
def paser_dict2(word):
	cur=g.en_db.execute('select value from collins where word =?',(word,))
	value=[row[0] for row in cur.fetchall()][0]
	soup = BeautifulSoup(''.join(value))
	collins=soup.find("div",attrs={"class":"collins_content"})
#str=soup.prettify()
	return str(collins.content[0])

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/reg', methods=['GET', 'POST'])
def reg():
	error = None
	if request.method == 'POST':
		name=request.form['username']
		pwd=request.form['password']
		g.en_db.execute('insert into user (user,passwd) values (?,?)',[name,pwd])	
		g.en_db.commit()
		return redirect("../")
	return render_template("reg.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	name=request.form['username']
	pwd=request.form['password']
	cu=g.en_db.execute('select * from user where user="%s"'%name)
	my_list=[row for row in cu.fetchall()]
	if(len(my_list)==0 or my_list[0][1]!=pwd):
#print my_list[0][1]
		error='err passwd'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
