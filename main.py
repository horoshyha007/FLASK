from flask import Flask, request, render_template, g, current_app
import random
from datetime import datetime
import pytz
import psycopg2
import psycopg2.extras 
from flask.cli import with_appcontext
import click

app = Flask(__name__)

def debug(s):
    """Prints a message to the screen (not web browser) 
    if FLASK_DEBUG is set."""
    if app.config['DEBUG']:
        print(s)


@app.route("/")
def hello_world():
  return render_template("home.html")

@app.route("/time")
def get_time():
    now = datetime.now().astimezone(pytz.timezone("US/Central"))
    timestring = now.strftime("%Y-%m-%d %H:%M:%S")  
    beginning = "<html><body><h1>The time is: "
    ending = "</h1></body></html>"
    return beginning + timestring + ending

@app.route("/random")
def pick_number():
    n = random.randint(0, 2)
    s = {"Катерина","Хороших","САД-21"}
    sList = list(s)
    return render_template("random.html", String=sList[n])

def connect_db():
    debug("Connecting to DB.")
    conn = psycopg2.connect(host="localhost", user="postgres", password="htgawm", dbname="practice")
    return conn


def get_db():
    """Retrieve the database connection or initialize it. The connection
    is unique for each request and will be reused if this is called again.
    """
    if "db" not in g:
        g.db = connect_db()

    return g.db

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
        debug("Closing DB")

@app.cli.command("initdb")
def init_db():
    """Clear existing data and create new tables."""
    conn = get_db()
    cur = conn.cursor()
    try:
        with current_app.open_resource("schema.sql") as file: 
            alltext = file.read() 
            cur.execute(alltext) 
        conn.commit()
        print("Initialized the database.")
    except psycopg2.Error as errorMsg:
        print(errorMsg)        
        conn.rollback()


@app.cli.command('populate')
def populate_db():
    conn = get_db()
    cur = conn.cursor()
    try:
        with current_app.open_resource("populate.sql") as file: 
            alltext = file.read() 
            cur.execute(alltext) 
        conn.commit()
        print("Populated DB with sample data.")
        dump_entries()
    except psycopg2.Error as errorMsg:
        print(errorMsg)        
        conn.rollback()

@app.route("/dump")
def dump_entries():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rows = cursor.fetchall()
    output = ""
    for r in rows:
        print(r)
        row_dict = {"id": r[0], "date": r[1], "title": r[2], "content": r[3]}
        debug(str(row_dict))
        output += str(row_dict)
        output += "\n"
    return "<pre>" + output + "</pre>"

@app.route("/browse")
def browse():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rowlist = cursor.fetchall()
    print(rowlist)
    return render_template('browse.html', entries=rowlist)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

def get_db(): 
    """Retrieve the database connection or initialize it. The connection 
    is unique for each request and will be reused if this is called again. 
    """ 
    if "db" not in g: 
        g.db = connect_db() 
 
    return g.db

def connect_db():
    """Connects to the database."""
    debug("Connecting to DB.")
    conn = psycopg2.connect(host="localhost", user="postgres", password="p1ngv1n", dbname="practice", 
        cursor_factory=psycopg2.extras.DictCursor)
    return conn

@app.cli.command("initdb")
def init_db():
    """Clear existing data and create new tables."""
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("schema.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Initialized the database.")

@app.teardown_appcontext
def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
        debug("Closing DB")