import flask
from flask import redirect, render_template, request, session

from classes.search import Query, Searchbar

app = flask.Flask(__name__)
app.secret_key = "secretkey"

offers = {}
searchbar = Searchbar()

@app.route('/', methods=['GET', 'POST']) # Index
def index():
    if request.method == "GET":
        session["query"] = None
        session["results"] = None
        return render_template('search.html')
    else:
        req = flask.request
        _from = req.form['from']
        _to = req.form['to']
        _when = req.form['when']
        _duration = req.form['duration']
        _who = req.form['who']
        # Logic for calling query function
        query = Query(_when, int(_duration), _from, _to, _who) 
        res = query.query()
        offers[str(query)] = {"results": res, "query": query}
        return redirect(f"/results/{str(query)}")

@app.route('/results/<queryid>')
def results(queryid: str):
    try:
        res = offers[queryid]["results"]
        query = offers[queryid]["query"]
    except Exception:
        return redirect("/")
    # delete results from storage after access
    del offers[queryid]
    print(type(res[0].rating))
    return render_template("results.html", results = res, query = query)

@app.route('/searchbar/<query>')
def get_searchbar(query: str):
    return searchbar.fetch_results(query)
    # return [{"test": "test"}]
app.run("0.0.0.0")