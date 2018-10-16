import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive TESTTEST</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/database/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('database2.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_movies = cur.execute('SELECT * FROM labels;').fetchall()

    return jsonify(all_movies)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/database', methods=['GET'])
def api_filter():
    conn = sqlite3.connect('database2.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query_parameters = request.args

    id = query_parameters.get('id')
    movie_title = query_parameters.get('movie_title')
    labels = query_parameters.get('labels')
   
    query = "SELECT * FROM labels WHERE"
    to_filter = []

    if id:
        to_filter.append(id)
        results = cur.execute( "SELECT * FROM labels WHERE Unamed: 0=?", (id,)).fetchall()

    if movie_title:
        to_filter.append(movie_title)
        results = cur.execute( "SELECT * FROM labels WHERE movie_title=?", (movie_title.capitalize(),)).fetchall()
        l = results[0]['labels']
        results2 =  cur.execute( "SELECT * FROM labels WHERE labels=?", (l,)).fetchall()
        results3 = results2[:4]

    if not (id or movie_title ):
        return page_not_found(404)

    query = query[:-4] + ';'


    print(results3)

    return jsonify(results3)

app.run()