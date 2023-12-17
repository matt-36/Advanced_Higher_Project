from classes.search import Query
from classes.holiday import Holiday
import flask
from flask import redirect, render_template, request

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
        query = Query()
        global_store['query'] = query
        res = query.query()
        global_store['results'] = res
        return redirect("/results")

@app.route('/results')
def results():
    res = global_store['results']
    ret = ""
    for h in res:
        ret += str(h) + "<br>"

    return ret


app.run()