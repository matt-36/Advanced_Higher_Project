from classes import Query, Holiday
import flask
from flask import render_template, request

app = flask.Flask(__name__)

global_store = {
    "query": Query(),
    "results": [Holiday()]
}

@app.route('/', methods=['GET', 'POST']) # Index
def index():
    if request.method == "GET":

        return render_template('search.html')
    else:
        # Logic for calling query function
        ...
    
    return "You shouldnt be seeing this"

@app.route('/results')
def results():


    return render_template(
        'results.html',\
        
    )

app.run()